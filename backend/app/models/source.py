from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl
from app.models.enums import SourceType, SourceStatus


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class SourceProvenance(BaseModel):
    """Metadata tracking the exact origin of an ingested item."""

    source_type: SourceType
    source_id: str
    source_name: str
    source_url: str
    retrieved_at: datetime = Field(default_factory=utc_now)
    source_updated_at: Optional[datetime] = None


class SourceEntity(BaseModel):
    """Base source entity stored in the source registry."""

    id: str
    name: str = Field(min_length=2)
    type: SourceType
    platform: str
    url: str
    enabled: bool = True
    priority: int = Field(default=10, ge=1, le=100)
    categories: List[str] = Field(default_factory=list)
    status: SourceStatus = SourceStatus.CONFIGURED
    last_synced_at: Optional[datetime] = None
    last_error: Optional[str] = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class YouTubeChannelEntity(SourceEntity):
    """YouTube-specific channel entity in the user-managed channel registry."""

    type: SourceType = SourceType.YOUTUBE_CHANNEL
    platform: str = "youtube"
    youtube_channel_id: str = Field(min_length=5)
    handle: Optional[str] = None
    thumbnail_url: Optional[str] = None
    video_count: int = 0
