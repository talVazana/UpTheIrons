from typing import List, Optional
import re
from datetime import datetime
from fastapi import APIRouter, Query, status
from pydantic import BaseModel, Field

from app.core.errors import NotFoundError, BadRequestError
from app.models.content import ContentEnvelope
from app.models.enums import ContentType, SourceType, ContentStatus, DifficultyLevel
from app.models.source import SourceProvenance
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


class AddDirectVideoRequest(BaseModel):
    url_or_id: str = Field(..., description="YouTube URL or Video ID")
    title: Optional[str] = None
    summary: Optional[str] = None


@router.post("/direct", response_model=ContentEnvelope, status_code=status.HTTP_201_CREATED)
async def add_direct_video(req: AddDirectVideoRequest):
    """Adds a single YouTube video directly."""
    # extract ID
    video_id = req.url_or_id
    if "youtube.com/watch?v=" in video_id:
        video_id = video_id.split("v=")[1].split("&")[0]
    elif "youtu.be/" in video_id:
        video_id = video_id.split("youtu.be/")[1].split("?")[0]
        
    clean_id = f"yt_{video_id}"
    
    existing = await firestore_repository.get(CONTENT_COLLECTION, clean_id)
    if existing:
        raise BadRequestError("This video is already in the vault.")
        
    envelope = ContentEnvelope(
        id=clean_id,
        type=ContentType.VIDEO,
        title=req.title or f"Direct Video: {video_id}",
        slug=clean_id,
        summary=req.summary or "Added directly by Admin.",
        category="forging",
        tags=["direct"],
        difficulty=DifficultyLevel.INTERMEDIATE,
        status=ContentStatus.PUBLISHED,
        source=SourceProvenance(
            source_type=SourceType.YOUTUBE,
            source_id="direct",
            source_name="Direct Links",
            source_url=f"https://www.youtube.com/watch?v={video_id}",
        ),
        metadata={
            "youtube_video_id": video_id,
            "channel_id": "direct",
            "channel_name": "Direct Links",
            "duration_seconds": 60,
            "ai_processed": False,
        },
        created_at=datetime.utcnow()
    )
    
    await firestore_repository.create(CONTENT_COLLECTION, clean_id, envelope.model_dump())
    return envelope


@router.delete("/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(video_id: str):
    """Deletes a video from the vault."""
    clean_id = video_id if video_id.startswith("yt_") else f"yt_{video_id}"
    doc = await firestore_repository.get(CONTENT_COLLECTION, clean_id)
    if not doc:
        raise NotFoundError("Video not found.")
    await firestore_repository.delete(CONTENT_COLLECTION, clean_id)
    return None
