from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator
from app.models.enums import ContentType, ContentStatus, DifficultyLevel
from app.models.source import SourceProvenance


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ContentEnvelope(BaseModel):
    """Polymorphic content envelope used across the forge knowledge vault."""

    id: str
    type: ContentType
    title: str = Field(min_length=2, max_length=200)
    slug: str = Field(min_length=2, max_length=200)
    summary: str = Field(min_length=5, max_length=1000)
    category: str
    tags: List[str] = Field(default_factory=list)
    difficulty: Optional[DifficultyLevel] = None
    source: Optional[SourceProvenance] = None
    image_url: Optional[str] = None
    status: ContentStatus = ContentStatus.PUBLISHED
    published_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        clean = v.lower().strip().replace(" ", "-")
        return clean


class HeatTreatmentRecipe(BaseModel):
    """Specific heat treatment temperatures and quench medium."""

    normalizing_temp_f: Optional[int] = None
    annealing_temp_f: Optional[int] = None
    hardening_temp_f: Optional[int] = None
    quench_medium: Optional[str] = None
    tempering_range_f: Optional[str] = None
    target_hardness_hrc: Optional[str] = None
    notes: Optional[str] = None


class MaterialMetadata(BaseModel):
    """Domain model for materials and steel alloys."""

    classification: str
    carbon_pct: float = Field(ge=0.0, le=5.0)
    alloying_elements: Dict[str, float] = Field(default_factory=dict)
    forging_temp_range_f: Optional[str] = None
    heat_treatment: Optional[HeatTreatmentRecipe] = None
    beginner_suitability: bool = True
    common_applications: List[str] = Field(default_factory=list)
    common_mistakes: List[str] = Field(default_factory=list)
    source_reference: Optional[str] = None


class VideoMetadata(BaseModel):
    """Domain model for YouTube videos collected from approved channels."""

    youtube_video_id: str
    channel_id: str
    channel_name: str
    duration_seconds: int = Field(default=0, ge=0)
    view_count: Optional[int] = None


class ProjectMetadata(BaseModel):
    """Domain model for progressive apprentice projects."""

    level: int = Field(default=1, ge=1, le=4)
    estimated_time_minutes: int = Field(default=60, ge=5)
    required_tools: List[str] = Field(default_factory=list)
    required_materials: List[str] = Field(default_factory=list)
    skills_learned: List[str] = Field(default_factory=list)
    steps: List[str] = Field(default_factory=list)
    safety_warnings: List[str] = Field(default_factory=list)


class ProductMetadata(BaseModel):
    """Domain model for workshop gear and tools with transparent pricing & evaluation."""

    sku: str
    platform: str
    price: float = Field(ge=0.0)
    currency: str = Field(default="USD", max_length=3)
    price_updated_at: datetime = Field(default_factory=utc_now)
    purchase_url: str
    pros: List[str] = Field(default_factory=list)
    cons: List[str] = Field(default_factory=list)
    beginner_suitable: bool = True
    alternatives: List[str] = Field(default_factory=list)
    affiliate: bool = False
