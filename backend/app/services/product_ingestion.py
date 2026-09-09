from datetime import datetime, timezone
import logging
import re
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.core.errors import NotFoundError, BadRequestError, SourceError
from app.models.content import ContentEnvelope, ProductMetadata, utc_now
from app.models.enums import ContentType, ContentStatus, DifficultyLevel, SourceType, SourceStatus
from app.models.source import SourceProvenance
from app.models.deduplication import compute_deduplication_key
from app.repositories.firestore import firestore_repository
from app.services.product_client import product_client

logger = logging.getLogger("blacksmith_knight.product_ingestion")

CONTENT_COLLECTION = "content"
PRODUCT_SOURCES_COLLECTION = "product_sources"
SYNC_LOGS_COLLECTION = "sync_logs"


class ProductSyncSummary(BaseModel):
    source_id: str
    vendor_name: str
    discovered: int = 0
    new_items: int = 0
    duplicates: int = 0
    price_updates: int = 0
    errors: List[str] = Field(default_factory=list)
    started_at: datetime = Field(default_factory=utc_now)
    completed_at: Optional[datetime] = None
    status: str = "SUCCESS"


def normalize_product_item(raw_prod: Dict[str, Any], source_id: str, vendor_name: str) -> ContentEnvelope:
    """Normalizes raw product metadata into ContentEnvelope with transparent specs and pricing."""
    sku = str(raw_prod.get("sku", "GEN-SKU")).strip()
    title = str(raw_prod.get("title", "Forging Tool")).strip()
    platform = str(raw_prod.get("platform", vendor_name)).strip()
    price = float(raw_prod.get("price", 0.0))
    currency = str(raw_prod.get("currency", "USD")).upper()
    purchase_url = str(raw_prod.get("purchase_url", "")).strip()
    summary = str(raw_prod.get("summary", f"{title} available from {platform}.")).strip()
    category = str(raw_prod.get("category", "tools")).strip().lower()

    clean_platform = re.sub(r"[^\w]", "", platform.lower())[:15] or "vendor"
    clean_sku = re.sub(r"[^\w\-]", "", sku.lower())
    envelope_id = f"prod_{clean_platform}_{clean_sku}"
    slug = re.sub(r"[\s_]+", "-", re.sub(r"[^\w\s\-]", "", title.lower())).strip("-")[:80] or envelope_id

    # Tags derivation
    tags = ["tools", "gear"]
    if "anvil" in title.lower():
        tags.append("anvil")
    if "forge" in title.lower():
        tags.append("forge")
    if "grinder" in title.lower():
        tags.append("grinder")
    if "tongs" in title.lower():
        tags.append("tongs")

    dedup_key = compute_deduplication_key(ContentType.PRODUCT, external_id=sku, canonical_url=purchase_url)

    metadata = {
        "sku": sku,
        "platform": platform,
        "price": price,
        "currency": currency,
        "price_updated_at": utc_now().isoformat(),
        "purchase_url": purchase_url,
        "pros": raw_prod.get("pros", []),
        "cons": raw_prod.get("cons", []),
        "beginner_suitable": bool(raw_prod.get("beginner_suitable", True)),
        "alternatives": raw_prod.get("alternatives", []),
        "affiliate": bool(raw_prod.get("affiliate", False)),
        "deduplication_key": dedup_key,
    }

    return ContentEnvelope(
        id=envelope_id,
        type=ContentType.PRODUCT,
        title=title[:200],
        slug=slug,
        summary=summary[:950],
        category=category,
        tags=tags,
        difficulty=DifficultyLevel.BEGINNER if metadata["beginner_suitable"] else DifficultyLevel.INTERMEDIATE,
        source=SourceProvenance(
            source_type=SourceType.PRODUCT_API,
            source_id=source_id,
            source_name=vendor_name,
            source_url=purchase_url or "https://blacksmithknight.local/sources",
            retrieved_at=utc_now(),
        ),
        image_url=raw_prod.get("image_url", "https://images.unsplash.com/photo-1504917599217-d4dc5ebe6122?w=800&auto=format&fit=crop&q=80"),
        status=ContentStatus.PUBLISHED,
        published_at=utc_now(),
        created_at=utc_now(),
        updated_at=utc_now(),
        metadata=metadata,
    )


class ProductIngestionService:
    """Coordinates product source ingestion, price updates, and non-commercial ranking integrity."""

    async def sync_source(self, source_id: str, max_items: int = 50) -> ProductSyncSummary:
        """Synchronizes an approved product/gear source."""
        source_data = await firestore_repository.get(PRODUCT_SOURCES_COLLECTION, source_id)
        if not source_data:
            raise NotFoundError(f"Product source '{source_id}' not found in registry.")

        if not source_data.get("enabled", True):
            raise BadRequestError(f"Cannot synchronize disabled source '{source_data.get('name', source_id)}'.")

        vendor_name = source_data.get("name") or source_data.get("vendor_name", "Forge Vendor")
        catalog_url = source_data.get("catalog_url") or source_data.get("url", "")
        summary = ProductSyncSummary(source_id=source_id, vendor_name=vendor_name)

        try:
            catalog_res = await product_client.fetch_catalog(catalog_url, max_items=max_items)
            raw_products = catalog_res.get("products", [])
            summary.discovered = len(raw_products)

            for raw_prod in raw_products:
                try:
                    envelope = normalize_product_item(raw_prod, source_id, vendor_name)
                    existing_doc = await firestore_repository.get(CONTENT_COLLECTION, envelope.id)

                    if existing_doc:
                        # Check dynamic price change
                        old_meta = existing_doc.get("metadata", {})
                        old_price = float(old_meta.get("price", 0.0))
                        new_price = float(envelope.metadata.get("price", 0.0))

                        if abs(old_price - new_price) > 0.01:
                            # Update price and timestamp without duplicating record
                            old_meta["price"] = new_price
                            old_meta["price_updated_at"] = utc_now().isoformat()
                            await firestore_repository.update(
                                CONTENT_COLLECTION,
                                envelope.id,
                                {"metadata": old_meta, "updated_at": utc_now().isoformat()},
                            )
                            summary.price_updates += 1
                            logger.info("Updated price for %s: $%.2f -> $%.2f", envelope.id, old_price, new_price)
                        else:
                            summary.duplicates += 1
                    else:
                        # New product item
                        await firestore_repository.create(
                            CONTENT_COLLECTION,
                            envelope.id,
                            envelope.model_dump(mode="json"),
                        )
                        summary.new_items += 1
                        logger.info("Stored new tool/product %s: %s", envelope.id, envelope.title)

                except Exception as ex:
                    err = f"Failed processing product {raw_prod.get('sku')}: {str(ex)}"
                    logger.error(err)
                    summary.errors.append(err)

            # Update source stats
            updated_count = source_data.get("item_count", 0) + summary.new_items
            await firestore_repository.update(
                PRODUCT_SOURCES_COLLECTION,
                source_id,
                {
                    "item_count": updated_count,
                    "last_synced_at": utc_now().isoformat(),
                    "status": SourceStatus.HEALTHY.value,
                    "last_error": None,
                },
            )

        except Exception as ex:
            summary.status = "FAILED"
            summary.errors.append(str(ex))
            logger.error("Product sync failed for source %s: %s", source_id, str(ex))
            await firestore_repository.update(
                PRODUCT_SOURCES_COLLECTION,
                source_id,
                {
                    "status": SourceStatus.FAILED.value,
                    "last_error": str(ex),
                },
            )

        summary.completed_at = utc_now()

        # Audit logging
        log_id = f"synclog_prod_{source_id}_{int(summary.started_at.timestamp())}"
        try:
            await firestore_repository.create(
                SYNC_LOGS_COLLECTION,
                log_id,
                summary.model_dump(mode="json"),
            )
        except Exception:
            pass

        return summary

    async def sync_all_enabled_sources(self) -> List[ProductSyncSummary]:
        """Synchronizes all enabled product sources with partial failure isolation."""
        sources = await firestore_repository.list(PRODUCT_SOURCES_COLLECTION, limit=50)
        summaries: List[ProductSyncSummary] = []

        for s in sources:
            if not s.get("enabled", True):
                continue

            sid = s["id"]
            try:
                summary = await self.sync_source(sid)
                summaries.append(summary)
            except Exception as ex:
                summaries.append(ProductSyncSummary(
                    source_id=sid,
                    vendor_name=s.get("name", "Unknown Vendor"),
                    status="FAILED",
                    errors=[str(ex)],
                    completed_at=utc_now(),
                ))

        return summaries


product_ingestion_service = ProductIngestionService()
