from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Query, status
from pydantic import BaseModel, Field

from app.core.errors import NotFoundError, ValidationError, BadRequestError
from app.models.content import ContentEnvelope, GuideMetadata
from app.models.enums import ContentType, ContentStatus, DifficultyLevel, TrustLabel, SourceType
from app.models.source import SourceProvenance
from app.models.seed import SEED_GUIDES
from app.repositories.firestore import firestore_repository
from app.services.rule_validator import rule_validator

router = APIRouter(prefix="/guides", tags=["guides"])

CONTENT_COLLECTION = "content"


class GuideListResponse(BaseModel):
    guides: List[ContentEnvelope]
    total: int
    limit: int
    offset: int


class CreateGuideRequest(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    slug: Optional[str] = None
    summary: str = Field(min_length=5, max_length=1000)
    category: str = Field(default="guides")
    tags: List[str] = Field(default_factory=list)
    difficulty: DifficultyLevel = Field(default=DifficultyLevel.BEGINNER)
    status: ContentStatus = Field(default=ContentStatus.PUBLISHED)
    metadata: GuideMetadata


class UpdateGuideRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=200)
    slug: Optional[str] = None
    summary: Optional[str] = Field(None, min_length=5, max_length=1000)
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    difficulty: Optional[DifficultyLevel] = None
    status: Optional[ContentStatus] = None
    metadata: Optional[GuideMetadata] = None


async def _ensure_seed_guides():
    """Lazily populates seed master guides in storage if missing."""
    for seed in SEED_GUIDES:
        existing = await firestore_repository.get(CONTENT_COLLECTION, seed.id)
        if not existing:
            await firestore_repository.create(CONTENT_COLLECTION, seed.id, seed.model_dump())


@router.get("", response_model=GuideListResponse)
async def list_guides(
    category: Optional[str] = Query(None, description="Filter by craft category"),
    difficulty: Optional[DifficultyLevel] = Query(None, description="Filter by difficulty level"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    trust_label: Optional[TrustLabel] = Query(None, description="Filter by technical trust classification"),
    q: Optional[str] = Query(None, description="Free-text search query"),
    limit: int = Query(24, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Retrieves paginated master craft guides from the Knowledge Library."""
    await _ensure_seed_guides()
    all_content = await firestore_repository.list(CONTENT_COLLECTION, limit=200)

    filtered: List[ContentEnvelope] = []
    q_lower = q.lower().strip() if q else None

    for item in all_content:
        # Match guide content type
        c_type = item.get("type")
        if c_type != ContentType.GUIDE.value and c_type != ContentType.GUIDE:
            continue

        # Status filter - only show published/featured/pinned/verified in public list
        item_status = item.get("status")
        if item_status == ContentStatus.HIDDEN.value or item_status == ContentStatus.ARCHIVED.value:
            continue

        if category and category != "all" and item.get("category") != category:
            continue

        if difficulty and item.get("difficulty") != difficulty.value and item.get("difficulty") != difficulty:
            continue

        if tag and tag not in item.get("tags", []):
            continue

        meta = item.get("metadata", {})
        if trust_label:
            guide_trust = meta.get("trust_label")
            if guide_trust != trust_label.value and guide_trust != trust_label:
                continue

        # Text search matching title, summary, tags, or markdown content
        if q_lower:
            title = (item.get("title") or "").lower()
            summary = (item.get("summary") or "").lower()
            tags = " ".join(item.get("tags") or []).lower()
            content_md = (meta.get("content_markdown") or "").lower()
            if q_lower not in title and q_lower not in summary and q_lower not in tags and q_lower not in content_md:
                continue

        try:
            envelope = ContentEnvelope.model_validate(item)
            filtered.append(envelope)
        except Exception:
            continue

    # Sort pinned first, then featured, then newest
    def sort_key(env: ContentEnvelope):
        pin_priority = 2 if env.status == ContentStatus.PINNED else (1 if env.status == ContentStatus.FEATURED else 0)
        timestamp = env.published_at or env.created_at
        return (pin_priority, timestamp)

    filtered.sort(key=sort_key, reverse=True)

    total = len(filtered)
    paged = filtered[offset : offset + limit]

    return GuideListResponse(
        guides=paged,
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{slug_or_id}", response_model=ContentEnvelope)
async def get_guide(slug_or_id: str):
    """Retrieves a single complete guide by slug or ID with full markdown and metadata."""
    await _ensure_seed_guides()

    # Try direct ID lookup first
    direct_id = slug_or_id if slug_or_id.startswith("guide-") else f"guide-{slug_or_id}"
    doc = await firestore_repository.get(CONTENT_COLLECTION, direct_id)

    # If not found by direct ID, scan for matching slug
    if not doc:
        all_content = await firestore_repository.list(CONTENT_COLLECTION, limit=200)
        for item in all_content:
            if item.get("type") in [ContentType.GUIDE.value, ContentType.GUIDE]:
                if item.get("slug") == slug_or_id or item.get("id") == slug_or_id:
                    doc = item
                    break

    if not doc:
        # Check if in SEED_GUIDES as fallback
        for seed in SEED_GUIDES:
            if seed.slug == slug_or_id or seed.id == slug_or_id or seed.id == direct_id:
                await firestore_repository.create(CONTENT_COLLECTION, seed.id, seed.model_dump())
                return seed
        raise NotFoundError(f"Master guide '{slug_or_id}' not found in knowledge library.")

    return ContentEnvelope.model_validate(doc)


@router.post("", response_model=ContentEnvelope, status_code=status.HTTP_201_CREATED)
async def create_guide(req: CreateGuideRequest):
    """Creates and validates a new master craft guide against editorial rules and standards."""
    clean_slug = (req.slug or req.title).lower().strip().replace(" ", "-")
    guide_id = f"guide-{clean_slug}"

    existing = await firestore_repository.get(CONTENT_COLLECTION, guide_id)
    if existing:
        raise BadRequestError(f"A guide with slug/ID '{clean_slug}' already exists in library.")

    envelope = ContentEnvelope(
        id=guide_id,
        type=ContentType.GUIDE,
        title=req.title,
        slug=clean_slug,
        summary=req.summary,
        category=req.category,
        tags=req.tags,
        difficulty=req.difficulty,
        status=req.status,
        source=SourceProvenance(
            source_type=SourceType.MANUAL,
            source_id="editorial-guild",
            source_name="Blacksmith Knight Guild",
            source_url=f"https://blacksmithknight.local/guides/{clean_slug}",
        ),
        metadata=req.metadata.model_dump(),
    )

    # Run editorial compliance & safety validation
    text_to_validate = f"{envelope.summary}\n{envelope.metadata.get('content_markdown', '')}"
    validation_result = rule_validator.validate_content(
        title=envelope.title,
        text=text_to_validate,
        tags=envelope.tags,
        source_name=envelope.source.source_name if envelope.source else None,
    )
    if not validation_result.valid:
        error_messages = [i.message for i in validation_result.issues if i.severity == "error"]
        raise ValidationError(f"Guide failed editorial validation standards: {'; '.join(error_messages)}")

    await firestore_repository.create(CONTENT_COLLECTION, guide_id, envelope.model_dump())
    return envelope


@router.patch("/{slug_or_id}", response_model=ContentEnvelope)
async def update_guide(slug_or_id: str, req: UpdateGuideRequest):
    """Updates an existing master guide."""
    existing = await get_guide(slug_or_id)
    existing_dict = existing.model_dump()

    if req.title is not None:
        existing_dict["title"] = req.title
    if req.slug is not None:
        existing_dict["slug"] = req.slug.lower().strip().replace(" ", "-")
    if req.summary is not None:
        existing_dict["summary"] = req.summary
    if req.category is not None:
        existing_dict["category"] = req.category
    if req.tags is not None:
        existing_dict["tags"] = req.tags
    if req.difficulty is not None:
        existing_dict["difficulty"] = req.difficulty
    if req.status is not None:
        existing_dict["status"] = req.status
    if req.metadata is not None:
        existing_dict["metadata"] = req.metadata.model_dump()

    updated_envelope = ContentEnvelope.model_validate(existing_dict)

    # Re-validate with rule engine
    text_to_validate = f"{updated_envelope.summary}\n{updated_envelope.metadata.get('content_markdown', '')}"
    validation_result = rule_validator.validate_content(
        title=updated_envelope.title,
        text=text_to_validate,
        tags=updated_envelope.tags,
        source_name=updated_envelope.source.source_name if updated_envelope.source else None,
    )
    if not validation_result.valid:
        error_messages = [i.message for i in validation_result.issues if i.severity == "error"]
        raise ValidationError(f"Updated guide failed editorial standards: {'; '.join(error_messages)}")

    await firestore_repository.update(CONTENT_COLLECTION, existing.id, updated_envelope.model_dump())
    return updated_envelope
