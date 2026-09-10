from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Query, status
from pydantic import BaseModel, Field

from app.core.errors import NotFoundError, ValidationError, BadRequestError
from app.models.content import ContentEnvelope, MaterialMetadata
from app.models.enums import ContentType, ContentStatus, DifficultyLevel, SourceType
from app.models.source import SourceProvenance
from app.models.seed import SEED_MATERIALS
from app.repositories.firestore import firestore_repository

router = APIRouter(prefix="/materials", tags=["materials"])

CONTENT_COLLECTION = "content"


class MaterialListResponse(BaseModel):
    materials: List[ContentEnvelope]
    total: int
    limit: int
    offset: int


class MaterialComparisonItem(BaseModel):
    id: str
    slug: str
    title: str
    classification: str
    steel_category: str
    carbon_pct: float
    alloying_elements: Dict[str, float]
    forging_temp_range_f: Optional[str]
    hardening_temp_f: Optional[int]
    quench_medium: Optional[str]
    target_hardness_hrc: Optional[str]
    beginner_suitability: bool
    confidence_score: float
    confidence_level: str
    source_reference: Optional[str]


class MaterialComparisonResponse(BaseModel):
    items: List[MaterialComparisonItem]
    compared_elements: List[str]
    toughness_rank: List[str]
    edge_retention_rank: List[str]
    quench_speed_summary: Dict[str, str]


class CreateMaterialRequest(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    slug: Optional[str] = None
    summary: str = Field(min_length=5, max_length=1000)
    category: str = Field(default="materials")
    tags: List[str] = Field(default_factory=list)
    difficulty: DifficultyLevel = Field(default=DifficultyLevel.BEGINNER)
    status: ContentStatus = Field(default=ContentStatus.PUBLISHED)
    metadata: MaterialMetadata


async def _ensure_seed_materials():
    """Ensures base metallurgy fixtures exist in the vault."""
    for seed in SEED_MATERIALS:
        existing = await firestore_repository.get(CONTENT_COLLECTION, seed.id)
        if not existing:
            await firestore_repository.create(CONTENT_COLLECTION, seed.id, seed.model_dump())


@router.get("", response_model=MaterialListResponse)
async def list_materials(
    steel_category: Optional[str] = Query(None, description="Filter by category (carbon_steel, tool_steel, spring_steel)"),
    beginner_friendly: Optional[bool] = Query(None, description="Filter by beginner suitability"),
    min_carbon: Optional[float] = Query(None, ge=0.0, le=5.0, description="Minimum carbon percentage"),
    max_carbon: Optional[float] = Query(None, ge=0.0, le=5.0, description="Maximum carbon percentage"),
    q: Optional[str] = Query(None, description="Free-text search query across designation, applications, mistakes"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Lists paginated materials and steel alloys from the Metallurgy Vault."""
    await _ensure_seed_materials()
    all_content = await firestore_repository.list(CONTENT_COLLECTION, limit=200)

    filtered: List[ContentEnvelope] = []
    q_lower = q.lower().strip() if q else None

    for item in all_content:
        c_type = item.get("type")
        if c_type != ContentType.MATERIAL.value and c_type != ContentType.MATERIAL:
            continue

        meta = item.get("metadata", {})

        if steel_category and steel_category != "all":
            if meta.get("steel_category") != steel_category:
                continue

        if beginner_friendly is not None:
            if meta.get("beginner_suitability") != beginner_friendly:
                continue

        carbon = meta.get("carbon_pct")
        if carbon is not None:
            if min_carbon is not None and carbon < min_carbon:
                continue
            if max_carbon is not None and carbon > max_carbon:
                continue

        if q_lower:
            title = (item.get("title") or "").lower()
            slug = (item.get("slug") or "").lower()
            summary = (item.get("summary") or "").lower()
            classif = (meta.get("classification") or "").lower()
            apps = " ".join(meta.get("common_applications") or []).lower()
            mistakes = " ".join(meta.get("common_mistakes") or []).lower()
            tags = " ".join(item.get("tags") or []).lower()

            if (
                q_lower not in title
                and q_lower not in slug
                and q_lower not in summary
                and q_lower not in classif
                and q_lower not in apps
                and q_lower not in mistakes
                and q_lower not in tags
            ):
                continue

        try:
            envelope = ContentEnvelope.model_validate(item)
            filtered.append(envelope)
        except Exception:
            continue

    # Sort descending by carbon %
    filtered.sort(key=lambda x: x.metadata.get("carbon_pct", 0.0), reverse=True)

    total = len(filtered)
    paged = filtered[offset : offset + limit]

    return MaterialListResponse(
        materials=paged,
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/compare", response_model=MaterialComparisonResponse)
async def compare_materials(
    ids: str = Query(..., description="Comma-separated steel slugs or IDs (e.g. 1084,1095,5160)"),
):
    """Compares 2 to 4 steels side-by-side with composition and heat treatment trade-offs."""
    await _ensure_seed_materials()
    id_list = [i.strip() for i in ids.split(",") if i.strip()]
    if len(id_list) < 2:
        raise BadRequestError("At least 2 steel IDs or slugs required for comparison.")
    if len(id_list) > 4:
        raise BadRequestError("Maximum 4 steels can be compared simultaneously.")

    items: List[MaterialComparisonItem] = []
    all_elements_set = set(["carbon", "manganese"])

    for target in id_list:
        envelope = await _resolve_material(target)
        meta = envelope.metadata
        ht = meta.get("heat_treatment") or {}

        elements = meta.get("alloying_elements", {})
        for el in elements.keys():
            all_elements_set.add(el.lower())

        comp_item = MaterialComparisonItem(
            id=envelope.id,
            slug=envelope.slug,
            title=envelope.title,
            classification=meta.get("classification", envelope.title),
            steel_category=meta.get("steel_category", "carbon_steel"),
            carbon_pct=meta.get("carbon_pct", 0.0),
            alloying_elements=elements,
            forging_temp_range_f=meta.get("forging_temp_range_f"),
            hardening_temp_f=ht.get("hardening_temp_f"),
            quench_medium=ht.get("quench_medium"),
            target_hardness_hrc=ht.get("target_hardness_hrc"),
            beginner_suitability=meta.get("beginner_suitability", True),
            confidence_score=meta.get("confidence_score", 0.95),
            confidence_level=meta.get("confidence_level", "handbook_verified"),
            source_reference=meta.get("source_reference"),
        )
        items.append(comp_item)

    # Deterministic ranking:
    # 1. Edge retention correlates directly with carbon % and carbide-forming alloys
    sorted_edge = sorted(items, key=lambda x: (x.carbon_pct, len(x.alloying_elements)), reverse=True)
    edge_rank = [s.title for s in sorted_edge]

    # 2. Impact toughness correlates inversely with carbon % (e.g. 5160 > 1084 > 1095)
    sorted_toughness = sorted(items, key=lambda x: (x.carbon_pct, -x.alloying_elements.get("chromium", 0.0)))
    toughness_rank = [s.title for s in sorted_toughness]

    quench_summary = {
        item.title: item.quench_medium or "Oil Quench" for item in items
    }

    return MaterialComparisonResponse(
        items=items,
        compared_elements=sorted(list(all_elements_set)),
        toughness_rank=toughness_rank,
        edge_retention_rank=edge_rank,
        quench_speed_summary=quench_summary,
    )


async def _resolve_material(slug_or_id: str) -> ContentEnvelope:
    """Helper resolving material from direct ID, slug, or seed fallback."""
    direct_id = slug_or_id if slug_or_id.startswith("mat-") else f"mat-{slug_or_id}"
    doc = await firestore_repository.get(CONTENT_COLLECTION, direct_id)

    if not doc:
        all_content = await firestore_repository.list(CONTENT_COLLECTION, limit=200)
        for item in all_content:
            if item.get("type") in [ContentType.MATERIAL.value, ContentType.MATERIAL]:
                if item.get("slug") == slug_or_id or item.get("id") == slug_or_id:
                    doc = item
                    break

    if not doc:
        for seed in SEED_MATERIALS:
            if seed.slug == slug_or_id or seed.id == slug_or_id or seed.id == direct_id:
                await firestore_repository.create(CONTENT_COLLECTION, seed.id, seed.model_dump())
                return seed
        raise NotFoundError(f"Material with ID or slug '{slug_or_id}' not found in metallurgy vault.")

    return ContentEnvelope.model_validate(doc)


@router.get("/{slug_or_id}", response_model=ContentEnvelope)
async def get_material(slug_or_id: str):
    """Retrieves a single material record by slug or ID."""
    await _ensure_seed_materials()
    return await _resolve_material(slug_or_id)


@router.post("", response_model=ContentEnvelope, status_code=status.HTTP_201_CREATED)
async def create_material(req: CreateMaterialRequest):
    """Adds a new verified material record to the metallurgy vault."""
    clean_slug = (req.slug or req.title).lower().strip().replace(" ", "-")
    material_id = f"mat-{clean_slug}"

    existing = await firestore_repository.get(CONTENT_COLLECTION, material_id)
    if existing:
        raise BadRequestError(f"Material with slug '{clean_slug}' already exists.")

    # Metallurgical precision check: must cite verifiable handbook/manufacturer source
    if not req.metadata.source_reference or len(req.metadata.source_reference.strip()) < 5:
        raise ValidationError("Mandatory source reference required per Metallurgical Standard (Section 15.06).")

    envelope = ContentEnvelope(
        id=material_id,
        type=ContentType.MATERIAL,
        title=req.title,
        slug=clean_slug,
        summary=req.summary,
        category=req.category,
        tags=req.tags,
        difficulty=req.difficulty,
        status=req.status,
        source=SourceProvenance(
            source_type=SourceType.MANUAL,
            source_id="metallurgy-vault",
            source_name="Blacksmith Knight Metallurgy Vault",
            source_url=f"https://blacksmithknight.local/materials/{clean_slug}",
        ),
        metadata=req.metadata.model_dump(),
    )

    await firestore_repository.create(CONTENT_COLLECTION, material_id, envelope.model_dump())
    return envelope
