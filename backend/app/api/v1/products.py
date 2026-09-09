import re
from typing import List, Optional
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from app.core.errors import NotFoundError, BadRequestError
from app.models.content import ContentEnvelope
from app.models.enums import ContentType, SourceType, SourceStatus
from app.models.source import ProductSourceEntity, utc_now
from app.repositories.firestore import firestore_repository
from app.services.product_ingestion import product_ingestion_service, ProductSyncSummary

router = APIRouter(prefix="/products", tags=["products"])

CONTENT_COLLECTION = "content"
PRODUCT_SOURCES_COLLECTION = "product_sources"
SOURCES_COLLECTION = "sources"


class CreateProductSourceRequest(BaseModel):
    catalog_url: str = Field(min_length=5, max_length=500)
    name: str = Field(min_length=2, max_length=150)
    platform: Optional[str] = Field(default="vendor", max_length=50)
    priority: int = Field(default=10, ge=1, le=100)
    categories: List[str] = Field(default_factory=lambda: ["tools"])


class UpdateProductSourceRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    enabled: Optional[bool] = None
    priority: Optional[int] = Field(default=None, ge=1, le=100)
    categories: Optional[List[str]] = None
    status: Optional[SourceStatus] = None


class ProductListResponse(BaseModel):
    products: List[ContentEnvelope]
    total: int
    limit: int
    offset: int


def _derive_source_slug(url: str) -> str:
    clean = re.sub(r"^[a-zA-Z0-9]+://", "", url.lower()).rstrip("/")
    clean = re.sub(r"[^\w]+", "-", clean).strip("-")
    return clean[:35]


# Source Management Endpoints
@router.post("/sources", response_model=ProductSourceEntity, status_code=201)
async def create_product_source(request: CreateProductSourceRequest):
    """Registers an approved tool vendor / catalog source."""
    cat_url = request.catalog_url.strip()
    if not (cat_url.startswith("http://") or cat_url.startswith("https://") or cat_url.startswith("test://")):
        raise BadRequestError("Catalog URL must start with http://, https://, or test://")

    slug = _derive_source_slug(cat_url)
    source_id = f"psrc_{slug}"

    existing = await firestore_repository.get(PRODUCT_SOURCES_COLLECTION, source_id)
    if existing:
        raise BadRequestError(f"Product source '{existing.get('name', source_id)}' already registered.")

    source_entity = ProductSourceEntity(
        id=source_id,
        name=request.name.strip(),
        type=SourceType.PRODUCT_API,
        platform=request.platform or "vendor",
        url=cat_url,
        catalog_url=cat_url,
        vendor_name=request.name.strip(),
        enabled=True,
        priority=request.priority,
        categories=request.categories,
        status=SourceStatus.CONFIGURED,
        item_count=0,
        created_at=utc_now(),
        updated_at=utc_now(),
    )

    s_dict = source_entity.model_dump(mode="json")
    await firestore_repository.create(PRODUCT_SOURCES_COLLECTION, source_id, s_dict)
    try:
        await firestore_repository.create(SOURCES_COLLECTION, source_id, s_dict)
    except Exception:
        pass

    return source_entity


@router.get("/sources")
async def list_product_sources(enabled: Optional[bool] = Query(None)):
    """Returns list of approved product/gear sources."""
    sources = await firestore_repository.list(PRODUCT_SOURCES_COLLECTION, limit=100)
    if enabled is not None:
        sources = [s for s in sources if s.get("enabled", True) == enabled]
    return {"sources": sources, "total": len(sources)}


@router.get("/sources/{source_id}", response_model=ProductSourceEntity)
async def get_product_source(source_id: str):
    doc = await firestore_repository.get(PRODUCT_SOURCES_COLLECTION, source_id)
    if not doc:
        raise NotFoundError(f"Product source '{source_id}' not found.")
    return ProductSourceEntity.model_validate(doc)


@router.patch("/sources/{source_id}", response_model=ProductSourceEntity)
async def update_product_source(source_id: str, request: UpdateProductSourceRequest):
    existing = await firestore_repository.get(PRODUCT_SOURCES_COLLECTION, source_id)
    if not existing:
        raise NotFoundError(f"Product source '{source_id}' not found.")

    update_dict = {}
    if request.name is not None:
        update_dict["name"] = request.name.strip()
    if request.enabled is not None:
        update_dict["enabled"] = request.enabled
    if request.priority is not None:
        update_dict["priority"] = request.priority
    if request.categories is not None:
        update_dict["categories"] = request.categories
    if request.status is not None:
        update_dict["status"] = request.status.value

    update_dict["updated_at"] = utc_now().isoformat()
    updated = await firestore_repository.update(PRODUCT_SOURCES_COLLECTION, source_id, update_dict)
    return ProductSourceEntity.model_validate(updated)


@router.delete("/sources/{source_id}")
async def delete_product_source(source_id: str):
    existing = await firestore_repository.get(PRODUCT_SOURCES_COLLECTION, source_id)
    if not existing:
        raise NotFoundError(f"Product source '{source_id}' not found.")

    await firestore_repository.delete(PRODUCT_SOURCES_COLLECTION, source_id)
    try:
        await firestore_repository.delete(SOURCES_COLLECTION, source_id)
    except Exception:
        pass

    return {"message": f"Product source '{source_id}' removed.", "deleted": True, "id": source_id}


# Synchronization Endpoints
@router.post("/sources/{source_id}/sync", response_model=ProductSyncSummary)
async def sync_product_source(source_id: str):
    """Synchronizes items from an approved product source."""
    return await product_ingestion_service.sync_source(source_id)


@router.post("/sync", response_model=List[ProductSyncSummary])
async def sync_all_product_sources():
    """Synchronizes all enabled product sources."""
    return await product_ingestion_service.sync_all_enabled_sources()


# Product Catalog Query Endpoints
@router.get("", response_model=ProductListResponse)
async def list_products(
    category: Optional[str] = Query(None, description="Filter by category (tools, anvils, etc.)"),
    tag: Optional[str] = Query(None, description="Filter by tag (anvil, forge, grinder, tongs)"),
    beginner_only: Optional[bool] = Query(None, description="Show only beginner-suitable gear"),
    max_price: Optional[float] = Query(None, ge=0.0, description="Maximum price filter"),
    limit: int = Query(24, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """
    Returns products ingested from approved sources.
    13.09 Commercial Bias Check: Ranking is strictly alphabetical by title or by price,
    never prioritizing affiliate products over non-affiliate tools.
    """
    all_content = await firestore_repository.list(CONTENT_COLLECTION, limit=200)

    filtered: List[ContentEnvelope] = []
    for item in all_content:
        if item.get("type") != ContentType.PRODUCT.value and item.get("type") != ContentType.PRODUCT:
            continue

        if category and item.get("category") != category:
            continue

        if tag and tag not in item.get("tags", []):
            continue

        meta = item.get("metadata", {})
        if beginner_only is True and not meta.get("beginner_suitable", True):
            continue

        if max_price is not None and float(meta.get("price", 0.0)) > max_price:
            continue

        try:
            envelope = ContentEnvelope.model_validate(item)
            filtered.append(envelope)
        except Exception:
            continue

    # Non-commercial unbiased sort: order by price ascending, then title
    filtered.sort(key=lambda x: (float(x.metadata.get("price", 0.0)), x.title))

    total = len(filtered)
    paged = filtered[offset : offset + limit]

    return ProductListResponse(
        products=paged,
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{product_id}", response_model=ContentEnvelope)
async def get_product(product_id: str):
    """Retrieves single tool/gear entry by ID."""
    clean_id = product_id if product_id.startswith("prod_") else f"prod_{product_id}"
    doc = await firestore_repository.get(CONTENT_COLLECTION, clean_id)
    if not doc:
        raise NotFoundError(f"Product '{product_id}' not found in knowledge vault.")
    return ContentEnvelope.model_validate(doc)
