from typing import List, Optional
from fastapi import APIRouter, Query, status
from pydantic import BaseModel, Field

from app.core.errors import NotFoundError, BadRequestError
from app.models.content import ContentEnvelope, ProjectMetadata
from app.models.enums import ContentType, ContentStatus, DifficultyLevel, SourceType
from app.models.source import SourceProvenance
from app.models.seed import SEED_PROJECTS
from app.repositories.firestore import firestore_repository

router = APIRouter(prefix="/projects", tags=["projects"])

CONTENT_COLLECTION = "content"


class ProjectListResponse(BaseModel):
    projects: List[ContentEnvelope]
    total: int
    limit: int
    offset: int


class CreateProjectRequest(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    slug: Optional[str] = None
    summary: str = Field(min_length=5, max_length=1000)
    category: str = Field(default="projects")
    tags: List[str] = Field(default_factory=list)
    difficulty: DifficultyLevel = Field(default=DifficultyLevel.BEGINNER)
    status: ContentStatus = Field(default=ContentStatus.PUBLISHED)
    metadata: ProjectMetadata


async def _ensure_seed_projects():
    """Ensures base project fixtures exist in the vault."""
    for seed in SEED_PROJECTS:
        existing = await firestore_repository.get(CONTENT_COLLECTION, seed.id)
        if not existing:
            await firestore_repository.create(CONTENT_COLLECTION, seed.id, seed.model_dump())


@router.get("", response_model=ProjectListResponse)
async def list_projects(
    difficulty: Optional[DifficultyLevel] = Query(None, description="Filter by difficulty level"),
    q: Optional[str] = Query(None, description="Free-text search query across title, summary, skills, tools"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Lists paginated projects."""
    await _ensure_seed_projects()
    all_content = await firestore_repository.list(CONTENT_COLLECTION, limit=200)

    filtered: List[ContentEnvelope] = []
    q_lower = q.lower().strip() if q else None

    for item in all_content:
        c_type = item.get("type")
        if c_type != ContentType.PROJECT.value and c_type != ContentType.PROJECT:
            continue

        meta = item.get("metadata", {})

        if difficulty:
            if meta.get("difficulty_level") != difficulty.value and item.get("difficulty") != difficulty.value:
                continue

        if q_lower:
            title = (item.get("title") or "").lower()
            slug = (item.get("slug") or "").lower()
            summary = (item.get("summary") or "").lower()
            skills = " ".join(meta.get("skills_learned") or []).lower()
            tools = " ".join(meta.get("required_tools") or []).lower()
            tags = " ".join(item.get("tags") or []).lower()

            if (
                q_lower not in title
                and q_lower not in slug
                and q_lower not in summary
                and q_lower not in skills
                and q_lower not in tools
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

    return ProjectListResponse(
        projects=paged,
        total=total,
        limit=limit,
        offset=offset,
    )


async def _resolve_project(slug_or_id: str) -> ContentEnvelope:
    """Helper resolving project from direct ID, slug, or seed fallback."""
    direct_id = slug_or_id if slug_or_id.startswith("proj-") else f"proj-{slug_or_id}"
    doc = await firestore_repository.get(CONTENT_COLLECTION, direct_id)

    if not doc:
        all_content = await firestore_repository.list(CONTENT_COLLECTION, limit=200)
        for item in all_content:
            if item.get("type") in [ContentType.PROJECT.value, ContentType.PROJECT]:
                if item.get("slug") == slug_or_id or item.get("id") == slug_or_id:
                    doc = item
                    break

    if not doc:
        for seed in SEED_PROJECTS:
            if seed.slug == slug_or_id or seed.id == slug_or_id or seed.id == direct_id:
                await firestore_repository.create(CONTENT_COLLECTION, seed.id, seed.model_dump())
                return seed
        raise NotFoundError(f"Project with ID or slug '{slug_or_id}' not found.")

    return ContentEnvelope.model_validate(doc)


@router.get("/{slug_or_id}", response_model=ContentEnvelope)
async def get_project(slug_or_id: str):
    """Retrieves a single project entry by slug or ID."""
    await _ensure_seed_projects()
    return await _resolve_project(slug_or_id)


@router.post("", response_model=ContentEnvelope, status_code=status.HTTP_201_CREATED)
async def create_project(req: CreateProjectRequest):
    """Adds a new verified project record."""
    clean_slug = (req.slug or req.title).lower().strip().replace(" ", "-")
    proj_id = f"proj-{clean_slug}"

    existing = await firestore_repository.get(CONTENT_COLLECTION, proj_id)
    if existing:
        raise BadRequestError(f"Project with slug '{clean_slug}' already exists.")

    envelope = ContentEnvelope(
        id=proj_id,
        type=ContentType.PROJECT,
        title=req.title,
        slug=clean_slug,
        summary=req.summary,
        category=req.category,
        tags=req.tags,
        difficulty=req.difficulty,
        status=req.status,
        source=SourceProvenance(
            source_type=SourceType.MANUAL,
            source_id="projects-guild",
            source_name="Blacksmith Knight Guild",
            source_url=f"https://blacksmithknight.local/projects/{clean_slug}",
        ),
        metadata=req.metadata.model_dump(),
    )

    await firestore_repository.create(CONTENT_COLLECTION, proj_id, envelope.model_dump())
    return envelope
