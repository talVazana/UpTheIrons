import re
from typing import List, Optional
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from app.core.errors import NotFoundError, BadRequestError
from app.models.enums import SourceType, SourceStatus
from app.models.source import RSSFeedEntity, utc_now
from app.repositories.firestore import firestore_repository
from app.services.rss_client import rss_client
from app.services.rss_ingestion import rss_ingestion_service, RSSSyncSummary

router = APIRouter(prefix="/rss", tags=["rss"])

RSS_COLLECTION = "rss_feeds"
SOURCES_COLLECTION = "sources"


class CreateRSSFeedRequest(BaseModel):
    url: str = Field(min_length=5, max_length=500, description="RSS or Atom feed URL")
    name: Optional[str] = Field(default=None, max_length=150)
    priority: int = Field(default=10, ge=1, le=100)
    categories: List[str] = Field(default_factory=list)


class UpdateRSSFeedRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    enabled: Optional[bool] = None
    priority: Optional[int] = Field(default=None, ge=1, le=100)
    categories: Optional[List[str]] = None
    status: Optional[SourceStatus] = None


class TestFeedRequest(BaseModel):
    url: str = Field(min_length=5, max_length=500)


def _derive_feed_slug(url: str) -> str:
    """Generates a clean slug from the feed domain and path."""
    clean = re.sub(r"^[a-zA-Z0-9]+://", "", url.lower()).rstrip("/")
    clean = re.sub(r"[^\w]+", "-", clean).strip("-")
    return clean[:40]


@router.post("/feeds", response_model=RSSFeedEntity, status_code=201)
async def create_rss_feed(request: CreateRSSFeedRequest):
    """
    Registers a new approved RSS/Atom feed in the forge source registry.
    Strictly validates URL and prevents duplicate feed registrations.
    """
    feed_url = request.url.strip()
    if not (feed_url.startswith("http://") or feed_url.startswith("https://") or feed_url.startswith("test://")):
        raise BadRequestError("Feed URL must start with http://, https://, or test://")

    slug = _derive_feed_slug(feed_url)
    feed_id = f"rss_{slug}"

    # Check duplicate by ID
    existing = await firestore_repository.get(RSS_COLLECTION, feed_id)
    if existing:
        raise BadRequestError(f"RSS feed '{existing.get('name', feed_id)}' is already registered (ID: {feed_id}).")

    # Check duplicate by URL in registry
    all_feeds = await firestore_repository.list(RSS_COLLECTION, limit=100)
    for f in all_feeds:
        if f.get("feed_url") == feed_url or f.get("url") == feed_url:
            raise BadRequestError(f"An RSS feed with URL '{feed_url}' already exists in registry.")

    name = request.name.strip() if request.name else f"Feed {slug}"

    feed_entity = RSSFeedEntity(
        id=feed_id,
        name=name,
        type=SourceType.RSS_FEED,
        platform="rss",
        url=feed_url,
        feed_url=feed_url,
        enabled=True,
        priority=request.priority,
        categories=request.categories,
        status=SourceStatus.CONFIGURED,
        article_count=0,
        created_at=utc_now(),
        updated_at=utc_now(),
    )

    feed_dict = feed_entity.model_dump(mode="json")
    await firestore_repository.create(RSS_COLLECTION, feed_id, feed_dict)

    # Sync into master sources collection
    try:
        await firestore_repository.create(SOURCES_COLLECTION, feed_id, feed_dict)
    except Exception:
        pass

    return feed_entity


@router.get("/feeds")
async def list_rss_feeds(
    enabled: Optional[bool] = Query(None),
    category: Optional[str] = Query(None),
):
    """Returns list of approved RSS feeds with optional filters."""
    all_feeds = await firestore_repository.list(RSS_COLLECTION, limit=100)
    filtered = []

    for f in all_feeds:
        if enabled is not None and f.get("enabled", True) != enabled:
            continue
        if category and category not in f.get("categories", []):
            continue
        filtered.append(f)

    return {"feeds": filtered, "total": len(filtered)}


@router.get("/feeds/{feed_id}", response_model=RSSFeedEntity)
async def get_rss_feed(feed_id: str):
    """Retrieves a single RSS feed by ID."""
    doc = await firestore_repository.get(RSS_COLLECTION, feed_id)
    if not doc:
        raise NotFoundError(f"RSS feed with ID '{feed_id}' not found.")
    return RSSFeedEntity.model_validate(doc)


@router.patch("/feeds/{feed_id}", response_model=RSSFeedEntity)
async def update_rss_feed(feed_id: str, request: UpdateRSSFeedRequest):
    """Updates RSS feed properties (enabled, priority, categories, status)."""
    existing = await firestore_repository.get(RSS_COLLECTION, feed_id)
    if not existing:
        raise NotFoundError(f"RSS feed with ID '{feed_id}' not found.")

    update_data = {}
    if request.name is not None:
        update_data["name"] = request.name.strip()
    if request.enabled is not None:
        update_data["enabled"] = request.enabled
    if request.priority is not None:
        update_data["priority"] = request.priority
    if request.categories is not None:
        update_data["categories"] = request.categories
    if request.status is not None:
        update_data["status"] = request.status.value

    update_data["updated_at"] = utc_now().isoformat()

    updated = await firestore_repository.update(RSS_COLLECTION, feed_id, update_data)
    try:
        await firestore_repository.update(SOURCES_COLLECTION, feed_id, update_data)
    except Exception:
        pass

    return RSSFeedEntity.model_validate(updated)


@router.delete("/feeds/{feed_id}")
async def delete_rss_feed(feed_id: str):
    """Deletes an RSS feed from registry. Historical articles remain in vault."""
    existing = await firestore_repository.get(RSS_COLLECTION, feed_id)
    if not existing:
        raise NotFoundError(f"RSS feed with ID '{feed_id}' not found.")

    await firestore_repository.delete(RSS_COLLECTION, feed_id)
    try:
        await firestore_repository.delete(SOURCES_COLLECTION, feed_id)
    except Exception:
        pass

    return {"message": f"RSS feed '{feed_id}' removed from registry.", "deleted": True, "id": feed_id}


@router.post("/feeds/{feed_id}/sync", response_model=RSSSyncSummary)
async def sync_rss_feed(feed_id: str):
    """Triggers deterministic ingestion for a single approved RSS feed."""
    return await rss_ingestion_service.sync_feed(feed_id)


@router.post("/sync", response_model=List[RSSSyncSummary])
async def sync_all_rss_feeds():
    """Synchronizes all enabled RSS feeds with partial failure isolation."""
    return await rss_ingestion_service.sync_all_enabled_feeds()


@router.post("/test")
async def test_rss_feed_connection(request: TestFeedRequest):
    """Tests connectivity and previews articles for an RSS URL without saving."""
    result = await rss_client.fetch_feed(request.url, max_items=5)
    return {
        "ok": True,
        "feed_title": result.get("feed_title"),
        "site_url": result.get("site_url"),
        "format": result.get("feed_format"),
        "sample_articles": result.get("articles", [])[:3],
    }
