from typing import List, Optional
from fastapi import APIRouter, Query, status
from pydantic import BaseModel, Field

from app.core.errors import NotFoundError, BadRequestError
from app.models.content import ContentEnvelope, ToolMetadata
from app.models.enums import ContentType, ContentStatus, DifficultyLevel, SourceType, ToolCategory
from app.models.source import SourceProvenance
from app.models.seed import SEED_TOOLS
from app.repositories.firestore import firestore_repository

router = APIRouter(prefix="/tools", tags=["tools"])

CONTENT_COLLECTION = "content"


class ToolListResponse(BaseModel):
    tools: List[ContentEnvelope]
    total: int
    limit: int
    offset: int


class CreateToolRequest(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    slug: Optional[str] = None
    summary: str = Field(min_length=5, max_length=1000)
    category: str = Field(default="workshop")
    tags: List[str] = Field(default_factory=list)
    difficulty: DifficultyLevel = Field(default=DifficultyLevel.BEGINNER)
    status: ContentStatus = Field(default=ContentStatus.PUBLISHED)
    metadata: ToolMetadata


async def _ensure_seed_tools():
    """Ensures base workshop fixtures exist in the vault."""
    for seed in SEED_TOOLS:
        existing = await firestore_repository.get(CONTENT_COLLECTION, seed.id)
        if not existing:
            await firestore_repository.create(CONTENT_COLLECTION, seed.id, seed.model_dump())


@router.get("", response_model=ToolListResponse)
async def list_tools(
    category: Optional[str] = Query(None, description="Filter by tool category (forging, heating, grinding, finishing, infrastructure)"),
    beginner_friendly: Optional[bool] = Query(None, description="Filter by beginner suitability"),
    diy_buildable: Optional[bool] = Query(None, description="Filter by DIY buildable"),
    q: Optional[str] = Query(None, description="Free-text search query across title, purpose, criteria, tags"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Lists paginated workshop tools and infrastructure equipment."""
    await _ensure_seed_tools()
    all_content = await firestore_repository.list(CONTENT_COLLECTION, limit=200)

    filtered: List[ContentEnvelope] = []
    q_lower = q.lower().strip() if q else None

    for item in all_content:
        c_type = item.get("type")
        if c_type != ContentType.TOOL.value and c_type != ContentType.TOOL:
            continue

        meta = item.get("metadata", {})

        if category and category != "all":
            if meta.get("tool_category") != category:
                continue

        if beginner_friendly is not None:
            if meta.get("beginner_friendly") != beginner_friendly:
                continue

        if diy_buildable is not None:
            if meta.get("diy_buildable") != diy_buildable:
                continue

        if q_lower:
            title = (item.get("title") or "").lower()
            slug = (item.get("slug") or "").lower()
            summary = (item.get("summary") or "").lower()
            purpose = (meta.get("primary_purpose") or "").lower()
            guidance = (meta.get("beginner_guidance") or "").lower()
            essential = " ".join(meta.get("essential_for") or []).lower()
            tags = " ".join(item.get("tags") or []).lower()

            if (
                q_lower not in title
                and q_lower not in slug
                and q_lower not in summary
                and q_lower not in purpose
                and q_lower not in guidance
                and q_lower not in essential
                and q_lower not in tags
            ):
                continue

        try:
            envelope = ContentEnvelope.model_validate(item)
            filtered.append(envelope)
        except Exception:
            continue

    total = len(filtered)
    paged = filtered[offset : offset + limit]

    return ToolListResponse(
        tools=paged,
        total=total,
        limit=limit,
        offset=offset,
    )


async def _resolve_tool(slug_or_id: str) -> ContentEnvelope:
    """Helper resolving tool from direct ID, slug, or seed fallback."""
    direct_id = slug_or_id if slug_or_id.startswith("tool-") else f"tool-{slug_or_id}"
    doc = await firestore_repository.get(CONTENT_COLLECTION, direct_id)

    if not doc:
        all_content = await firestore_repository.list(CONTENT_COLLECTION, limit=200)
        for item in all_content:
            if item.get("type") in [ContentType.TOOL.value, ContentType.TOOL]:
                if item.get("slug") == slug_or_id or item.get("id") == slug_or_id:
                    doc = item
                    break

    if not doc:
        for seed in SEED_TOOLS:
            if seed.slug == slug_or_id or seed.id == slug_or_id or seed.id == direct_id:
                await firestore_repository.create(CONTENT_COLLECTION, seed.id, seed.model_dump())
                return seed
        raise NotFoundError(f"Tool with ID or slug '{slug_or_id}' not found in workshop vault.")

    return ContentEnvelope.model_validate(doc)


@router.get("/{slug_or_id}", response_model=ContentEnvelope)
async def get_tool(slug_or_id: str):
    """Retrieves a single workshop tool entry by slug or ID."""
    await _ensure_seed_tools()
    return await _resolve_tool(slug_or_id)


@router.post("", response_model=ContentEnvelope, status_code=status.HTTP_201_CREATED)
async def create_tool(req: CreateToolRequest):
    """Adds a new verified tool knowledge record to the workshop vault."""
    clean_slug = (req.slug or req.title).lower().strip().replace(" ", "-")
    tool_id = f"tool-{clean_slug}"

    existing = await firestore_repository.get(CONTENT_COLLECTION, tool_id)
    if existing:
        raise BadRequestError(f"Tool with slug '{clean_slug}' already exists.")

    envelope = ContentEnvelope(
        id=tool_id,
        type=ContentType.TOOL,
        title=req.title,
        slug=clean_slug,
        summary=req.summary,
        category=req.category,
        tags=req.tags,
        difficulty=req.difficulty,
        status=req.status,
        source=SourceProvenance(
            source_type=SourceType.MANUAL,
            source_id="workshop-guild",
            source_name="Blacksmith Knight Workshop Guild",
            source_url=f"https://blacksmithknight.local/workshop/{clean_slug}",
        ),
        metadata=req.metadata.model_dump(),
    )

    await firestore_repository.create(CONTENT_COLLECTION, tool_id, envelope.model_dump())
    return envelope
