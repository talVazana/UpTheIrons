import re
from datetime import datetime
from typing import List, Optional
from urllib.parse import urlparse
from fastapi import APIRouter, Query
import httpx
from pydantic import BaseModel, Field

from app.core.config import settings
from app.core.errors import NotFoundError, BadRequestError, StorageError
from app.models.enums import SourceType, SourceStatus
from app.models.source import SourceEntity, YouTubeChannelEntity, utc_now
from app.repositories.firestore import firestore_repository
from app.api.v1.settings import get_effective_youtube_api_key
from app.services.youtube_ingestion import youtube_ingestion_service, SyncSummary, SYNC_LOGS_COLLECTION

router = APIRouter(prefix="/youtube", tags=["youtube"])

YOUTUBE_COLLECTION = "youtube_channels"
SOURCES_COLLECTION = "sources"


class CreateYouTubeChannelRequest(BaseModel):
    url_or_handle: str = Field(min_length=2, max_length=500, description="YouTube channel URL, @handle, or Channel ID")
    name: Optional[str] = Field(default=None, max_length=150)
    priority: int = Field(default=10, ge=1, le=100)
    categories: List[str] = Field(default_factory=list)
    thumbnail_url: Optional[str] = Field(default=None, max_length=500)


class UpdateYouTubeChannelRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    enabled: Optional[bool] = None
    priority: Optional[int] = Field(default=None, ge=1, le=100)
    categories: Optional[List[str]] = None
    thumbnail_url: Optional[str] = Field(default=None, max_length=500)
    status: Optional[SourceStatus] = None


class ResolveChannelRequest(BaseModel):
    query: str = Field(min_length=2, max_length=500, description="Channel URL, handle, or ID to inspect")


class ChannelListResponse(BaseModel):
    channels: List[YouTubeChannelEntity]
    total: int


def _clean_handle(raw_handle: str) -> str:
    """Standardizes handle with leading @ symbol."""
    trimmed = raw_handle.strip().lstrip("@")
    return f"@{trimmed}"


def parse_channel_identifier(input_str: str):
    """
    Parses an arbitrary YouTube URL, @handle, or channel ID into components.
    Returns a dict with resolved components.
    """
    cleaned = input_str.strip()
    
    # Direct handle input, e.g. @BlackBearForge or BlackBearForge
    if cleaned.startswith("@"):
        handle = _clean_handle(cleaned)
        return {
            "handle": handle,
            "channel_id": f"yt_{handle.lstrip('@').lower()}",
            "canonical_url": f"https://www.youtube.com/{handle}",
            "derived_name": handle.lstrip("@"),
        }

    # URL parsing
    if "youtube.com" in cleaned or "youtu.be" in cleaned:
        # Match handle in URL: youtube.com/@handle
        handle_match = re.search(r"youtube\.com/@([A-Za-z0-9_\-\.]+)", cleaned)
        if handle_match:
            handle = f"@{handle_match.group(1)}"
            return {
                "handle": handle,
                "channel_id": f"yt_{handle.lstrip('@').lower()}",
                "canonical_url": f"https://www.youtube.com/{handle}",
                "derived_name": handle.lstrip("@"),
            }
        
        # Match channel ID in URL: youtube.com/channel/UC...
        channel_id_match = re.search(r"youtube\.com/channel/(UC[A-Za-z0-9_\-]{20,24})", cleaned)
        if channel_id_match:
            cid = channel_id_match.group(1)
            return {
                "handle": None,
                "channel_id": cid,
                "canonical_url": f"https://www.youtube.com/channel/{cid}",
                "derived_name": f"Channel {cid[:8]}",
            }
        
        # Match custom URL: youtube.com/c/CustomName or /user/UserName
        custom_match = re.search(r"youtube\.com/(?:c|user)/([A-Za-z0-9_\-\.]+)", cleaned)
        if custom_match:
            cname = custom_match.group(1)
            return {
                "handle": f"@{cname}",
                "channel_id": f"yt_{cname.lower()}",
                "canonical_url": f"https://www.youtube.com/c/{cname}",
                "derived_name": cname,
            }

    # Direct Channel ID pattern: UC... (24 chars)
    if re.match(r"^UC[A-Za-z0-9_\-]{20,24}$", cleaned):
        return {
            "handle": None,
            "channel_id": cleaned,
            "canonical_url": f"https://www.youtube.com/channel/{cleaned}",
            "derived_name": f"Channel {cleaned[:8]}",
        }

    # If it's a plain slug / word without spaces, assume it's a handle
    if re.match(r"^[A-Za-z0-9_\-\.]+$", cleaned):
        handle = f"@{cleaned}"
        return {
            "handle": handle,
            "channel_id": f"yt_{cleaned.lower()}",
            "canonical_url": f"https://www.youtube.com/{handle}",
            "derived_name": cleaned,
        }

    raise BadRequestError(
        f"Unable to parse YouTube channel identifier '{input_str}'. "
        f"Provide a valid @handle, full channel URL, or UC... channel ID."
    )


async def resolve_with_youtube_api(parsed_info: dict) -> dict:
    """
    If YouTube API key is configured (via settings or env), calls YouTube Data API v3 channels endpoint.
    Otherwise returns parsed info with fallback defaults.
    """
    effective_key = await get_effective_youtube_api_key()
    api_key = effective_key.strip() if effective_key else None
    result = {
        "youtube_channel_id": parsed_info["channel_id"],
        "handle": parsed_info["handle"],
        "canonical_url": parsed_info["canonical_url"],
        "name": parsed_info["derived_name"],
        "thumbnail_url": f"https://api.dicebear.com/7.x/identicon/svg?seed={parsed_info['channel_id']}",
        "video_count": 0,
        "resolved_via_api": False,
    }

    if not api_key:
        return result

    # Query YouTube Data API
    params = {"key": api_key, "part": "snippet,statistics"}
    if parsed_info["channel_id"].startswith("UC"):
        params["id"] = parsed_info["channel_id"]
    elif parsed_info["handle"]:
        params["forHandle"] = parsed_info["handle"]
    else:
        return result

    try:
        async with httpx.AsyncClient(timeout=4.0) as client:
            resp = await client.get("https://www.googleapis.com/youtube/v3/channels", params=params)
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("items", [])
                if items:
                    item = items[0]
                    snippet = item.get("snippet", {})
                    stats = item.get("statistics", {})
                    result["youtube_channel_id"] = item.get("id", result["youtube_channel_id"])
                    result["name"] = snippet.get("title", result["name"])
                    result["handle"] = snippet.get("customUrl", result["handle"])
                    result["video_count"] = int(stats.get("videoCount", 0))
                    result["thumbnail_url"] = (
                        snippet.get("thumbnails", {}).get("medium", {}).get("url")
                        or snippet.get("thumbnails", {}).get("default", {}).get("url")
                        or result["thumbnail_url"]
                    )
                    result["resolved_via_api"] = True
    except Exception:
        # Fall back gracefully to local parsed info if API call fails
        pass

    return result


@router.post("/resolve")
async def resolve_channel(req: ResolveChannelRequest):
    """
    Validates and resolves a YouTube channel identifier before adding it to the registry.
    Can be used by the frontend to display a preview.
    """
    parsed = parse_channel_identifier(req.query)
    resolved = await resolve_with_youtube_api(parsed)
    return resolved


@router.post("/channels", response_model=YouTubeChannelEntity, status_code=201)
async def create_channel(req: CreateYouTubeChannelRequest):
    """
    Registers an approved YouTube channel into the channel registry.
    Strictly forbids autonomous crawler discovery; explicit user addition only.
    """
    parsed = parse_channel_identifier(req.url_or_handle)
    resolved = await resolve_with_youtube_api(parsed)

    channel_name = req.name.strip() if (req.name and req.name.strip()) else resolved["name"]
    thumb_url = req.thumbnail_url or resolved["thumbnail_url"]
    canonical_id = resolved["youtube_channel_id"]
    record_id = f"yt_{canonical_id.lower()}" if not canonical_id.startswith("yt_") else canonical_id.lower()

    # Check for duplicate
    existing = await firestore_repository.get(YOUTUBE_COLLECTION, record_id)
    if existing:
        raise BadRequestError(f"YouTube channel '{channel_name}' ({canonical_id}) is already registered.")

    now = utc_now()
    entity = YouTubeChannelEntity(
        id=record_id,
        name=channel_name,
        type=SourceType.YOUTUBE_CHANNEL,
        platform="youtube",
        url=resolved["canonical_url"],
        youtube_channel_id=canonical_id,
        handle=resolved["handle"],
        thumbnail_url=thumb_url,
        video_count=resolved.get("video_count", 0),
        enabled=True,
        priority=req.priority,
        categories=[c.lower().strip() for c in req.categories],
        status=SourceStatus.CONFIGURED,
        created_at=now,
        updated_at=now,
    )

    # Persist to youtube_channels collection
    dumped = entity.model_dump(mode="json")
    stored = await firestore_repository.create(YOUTUBE_COLLECTION, record_id, dumped)

    # Synchronize mirror in general sources registry
    source_mirror = SourceEntity(
        id=record_id,
        name=entity.name,
        type=SourceType.YOUTUBE_CHANNEL,
        platform="youtube",
        url=entity.url,
        enabled=entity.enabled,
        priority=entity.priority,
        categories=entity.categories,
        status=entity.status,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
    await firestore_repository.create(SOURCES_COLLECTION, record_id, source_mirror.model_dump(mode="json"))

    return YouTubeChannelEntity(**stored)


@router.get("/channels", response_model=ChannelListResponse)
async def list_channels(
    enabled: Optional[bool] = None,
    status: Optional[SourceStatus] = None,
    category: Optional[str] = None,
    limit: int = Query(default=50, ge=1, le=100),
):
    """
    Lists user-approved YouTube channels with optional filters.
    """
    try:
        raw_items = await firestore_repository.list(YOUTUBE_COLLECTION, limit=limit)
    except StorageError:
        return ChannelListResponse(channels=[], total=0)

    channels = [
        YouTubeChannelEntity(**item)
        for item in raw_items
        if "id" in item and "youtube_channel_id" in item
    ]

    if enabled is not None:
        channels = [c for c in channels if c.enabled == enabled]
    if status is not None:
        channels = [c for c in channels if c.status == status]
    if category is not None:
        cat_lower = category.lower().strip()
        channels = [c for c in channels if cat_lower in c.categories]

    channels = sorted(channels, key=lambda c: (-c.priority, c.name.lower()))
    return ChannelListResponse(channels=channels, total=len(channels))


@router.get("/channels/{channel_id}", response_model=YouTubeChannelEntity)
async def get_channel(channel_id: str):
    """
    Retrieves a single YouTube channel from the registry.
    """
    canonical_id = channel_id.lower() if channel_id.startswith("yt_") else f"yt_{channel_id.lower()}"
    stored = await firestore_repository.get(YOUTUBE_COLLECTION, canonical_id)
    if not stored:
        stored = await firestore_repository.get(YOUTUBE_COLLECTION, channel_id)
    if not stored:
        raise NotFoundError(f"YouTube channel with ID '{channel_id}' not found in registry.")

    return YouTubeChannelEntity(**stored)


@router.patch("/channels/{channel_id}", response_model=YouTubeChannelEntity)
async def update_channel(channel_id: str, req: UpdateYouTubeChannelRequest):
    """
    Updates channel settings (enabled, priority, categories, status).
    When disabled, collectors in Milestone 11 will exclude it.
    """
    canonical_id = channel_id.lower() if channel_id.startswith("yt_") else f"yt_{channel_id.lower()}"
    existing = await firestore_repository.get(YOUTUBE_COLLECTION, canonical_id)
    if not existing:
        stored_raw = await firestore_repository.get(YOUTUBE_COLLECTION, channel_id)
        if stored_raw:
            canonical_id = channel_id
            existing = stored_raw
        else:
            raise NotFoundError(f"YouTube channel with ID '{channel_id}' not found in registry.")

    update_fields = req.model_dump(exclude_unset=True, mode="json")
    if "categories" in update_fields and update_fields["categories"]:
        update_fields["categories"] = [c.lower().strip() for c in update_fields["categories"]]

    update_fields["updated_at"] = utc_now().isoformat()

    updated = await firestore_repository.update(YOUTUBE_COLLECTION, canonical_id, update_fields)

    # Mirror updates to sources collection if applicable
    source_fields = {k: v for k, v in update_fields.items() if k in ("enabled", "priority", "categories", "status", "name", "updated_at")}
    if source_fields:
        try:
            await firestore_repository.update(SOURCES_COLLECTION, canonical_id, source_fields)
        except Exception:
            pass

    return YouTubeChannelEntity(**updated)


@router.delete("/channels/{channel_id}")
async def delete_channel(channel_id: str):
    """
    Removes an approved YouTube channel from the registry.
    Per Milestone 10.07: Historical video records in content collection are retained.
    """
    canonical_id = channel_id.lower() if channel_id.startswith("yt_") else f"yt_{channel_id.lower()}"
    existing = await firestore_repository.get(YOUTUBE_COLLECTION, canonical_id)
    if not existing:
        stored_raw = await firestore_repository.get(YOUTUBE_COLLECTION, channel_id)
        if stored_raw:
            canonical_id = channel_id
            existing = stored_raw
        else:
            raise NotFoundError(f"YouTube channel with ID '{channel_id}' not found in registry.")

    await firestore_repository.delete(YOUTUBE_COLLECTION, canonical_id)
    try:
        await firestore_repository.delete(SOURCES_COLLECTION, canonical_id)
    except Exception:
        pass

    return {"message": f"YouTube channel '{canonical_id}' deleted successfully.", "deleted": True, "id": canonical_id}


@router.post("/channels/{channel_id}/sync", response_model=SyncSummary)
async def trigger_channel_sync(channel_id: str):
    """
    Executes real ingestion sync for an approved channel.
    Deduplicates videos and stores new items in the knowledge vault.
    Disabled channels are rejected.
    """
    canonical_id = channel_id.lower() if channel_id.startswith("yt_") else f"yt_{channel_id.lower()}"
    existing = await firestore_repository.get(YOUTUBE_COLLECTION, canonical_id)
    if not existing:
        # Check direct channel ID
        existing = await firestore_repository.get(YOUTUBE_COLLECTION, channel_id)
        if existing:
            canonical_id = channel_id
        else:
            raise NotFoundError(f"YouTube channel with ID '{channel_id}' not found in registry.")

    return await youtube_ingestion_service.sync_channel(canonical_id)


@router.post("/sync", response_model=List[SyncSummary])
async def trigger_all_channels_sync():
    """
    Executes synchronization across all enabled approved YouTube channels.
    Isolates partial failures so healthy channels succeed.
    """
    return await youtube_ingestion_service.sync_all_enabled_channels()


@router.get("/sync-logs")
async def list_sync_logs(limit: int = Query(20, ge=1, le=100)):
    """Returns recent synchronization run logs."""
    logs = await firestore_repository.list(SYNC_LOGS_COLLECTION, limit=limit)
    logs.sort(key=lambda x: x.get("started_at", ""), reverse=True)
    return {"logs": logs, "total": len(logs)}
