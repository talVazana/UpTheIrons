from typing import List, Optional
from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.core.errors import NotFoundError
from app.models.content import ContentEnvelope
from app.models.enums import ContentType
from app.repositories.firestore import firestore_repository

router = APIRouter(prefix="/videos", tags=["videos"])

CONTENT_COLLECTION = "content"


class VideoListResponse(BaseModel):
    videos: List[ContentEnvelope]
    total: int
    limit: int
    offset: int


@router.get("", response_model=VideoListResponse)
async def list_videos(
    category: Optional[str] = Query(None, description="Filter by forge category"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    channel_id: Optional[str] = Query(None, description="Filter by YouTube channel ID"),
    limit: int = Query(24, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """
    Returns paginated video items from the forge knowledge vault.
    Supports filtering by category, tag, or channel.
    """
    all_content = await firestore_repository.list(CONTENT_COLLECTION, limit=200)

    # Filter to video content
    filtered: List[ContentEnvelope] = []
    for item in all_content:
        if item.get("type") != ContentType.VIDEO.value and item.get("type") != ContentType.VIDEO:
            continue

        if category and item.get("category") != category:
            continue

        if tag and tag not in item.get("tags", []):
            continue

        if channel_id:
            src = item.get("source", {})
            meta = item.get("metadata", {})
            if src.get("source_id") != channel_id and meta.get("channel_id") != channel_id:
                continue

        try:
            envelope = ContentEnvelope.model_validate(item)
            filtered.append(envelope)
        except Exception:
            # Fallback if raw dict matches schema
            continue

    # Sort reverse chronological by published_at or created_at
    filtered.sort(
        key=lambda x: x.published_at or x.created_at,
        reverse=True,
    )

    total = len(filtered)
    paged = filtered[offset : offset + limit]

    return VideoListResponse(
        videos=paged,
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{video_id}", response_model=ContentEnvelope)
async def get_video(video_id: str):
    """Retrieves a single video by ID (e.g. yt_abc123 or abc123)."""
    clean_id = video_id if video_id.startswith("yt_") else f"yt_{video_id}"
    doc = await firestore_repository.get(CONTENT_COLLECTION, clean_id)
    if not doc:
        raise NotFoundError(f"Video with ID '{video_id}' not found in knowledge vault.")
    return ContentEnvelope.model_validate(doc)
