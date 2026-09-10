from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator
from app.models.enums import ContentType, ContentStatus, DifficultyLevel, TrustLabel, ToolCategory
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
    decalescence_temp_f: Optional[int] = None
    quench_medium: Optional[str] = None
    soak_time_minutes: Optional[int] = None
    tempering_range_f: Optional[str] = None
    target_hardness_hrc: Optional[str] = None
    tempering_table: Optional[List[Dict[str, Any]]] = None
    notes: Optional[str] = None


class MaterialMetadata(BaseModel):
    """Domain model for materials and steel alloys."""

    classification: str
    carbon_pct: float = Field(ge=0.0, le=5.0)
    alloying_elements: Dict[str, float] = Field(default_factory=dict)
    steel_category: str = Field(default="carbon_steel", description="carbon_steel, tool_steel, spring_steel, alloy_steel, stainless_steel")
    forging_temp_range_f: Optional[str] = None
    heat_treatment: Optional[HeatTreatmentRecipe] = None
    spark_testing_profile: Optional[str] = None
    grinding_characteristics: Optional[str] = None
    weldability: Optional[str] = None
    corrosion_resistance: Optional[str] = None
    confidence_score: float = Field(default=0.95, ge=0.0, le=1.0)
    confidence_level: str = Field(default="handbook_verified", description="handbook_verified, manufacturer_spec, empirical_test, unverified_estimate")
    beginner_suitability: bool = True
    common_applications: List[str] = Field(default_factory=list)
    common_mistakes: List[str] = Field(default_factory=list)
    source_reference: Optional[str] = None
    source_metadata: Dict[str, str] = Field(default_factory=dict)



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


class SourceReference(BaseModel):
    """Academic, historical, or guild citation backing guide claims."""

    title: str = Field(min_length=2, max_length=300)
    author: Optional[str] = None
    publication: Optional[str] = None
    year: Optional[int] = None
    url: Optional[str] = None
    trust_label: Optional[TrustLabel] = None
    citation_key: Optional[str] = None


class SafetyPrecaution(BaseModel):
    """Mandatory safety warning or critical craft hazard protocol."""

    level: str = Field(default="warning", description="critical, warning, caution, mandatory_ppe")
    hazard: str = Field(min_length=3, max_length=200)
    mitigation: str = Field(min_length=5, max_length=1000)
    ppe: List[str] = Field(default_factory=list)


class RelatedContentLink(BaseModel):
    """Bidirectional reference linking guides to materials, projects, videos, and tools."""

    content_id: str
    title: str
    type: ContentType
    slug: str
    relationship: str = Field(default="related", description="requires_material, related_technique, recommended_video, prerequisite_project")


class GuideMetadata(BaseModel):
    """Domain model for in-depth editorial craft guides with technical trust classifications."""

    reading_time_minutes: int = Field(default=5, ge=1)
    trust_label: TrustLabel = TrustLabel.CRAFT_PRACTICE
    author: str = Field(default="Blacksmith Knight Guild", min_length=2, max_length=100)
    version: str = Field(default="1.0", max_length=20)
    content_markdown: str = Field(min_length=10)
    source_references: List[SourceReference] = Field(default_factory=list)
    safety_precautions: List[SafetyPrecaution] = Field(default_factory=list)
    related_content: List[RelatedContentLink] = Field(default_factory=list)
    table_of_contents: List[Dict[str, str]] = Field(default_factory=list)


class ToolMetadata(BaseModel):
    """Domain model for structured workshop knowledge, equipment, and tooling."""

    tool_category: ToolCategory = Field(default=ToolCategory.FORGING)
    primary_purpose: str = Field(min_length=5, max_length=500)
    essential_for: List[str] = Field(default_factory=list)
    selection_criteria: List[str] = Field(default_factory=list)
    beginner_guidance: str = Field(min_length=10, max_length=1500)
    beginner_friendly: bool = Field(default=True)
    diy_buildable: bool = Field(default=False)
    diy_alternatives: List[str] = Field(default_factory=list)
    maintenance_protocols: List[str] = Field(default_factory=list)
    safety_precautions: List[SafetyPrecaution] = Field(default_factory=list)
    specifications: Dict[str, Any] = Field(default_factory=dict)
    related_tools: List[RelatedContentLink] = Field(default_factory=list)
    source_references: List[SourceReference] = Field(default_factory=list)

