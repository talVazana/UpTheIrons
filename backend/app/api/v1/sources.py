import re
import socket
import uuid
from typing import List, Optional
from urllib.parse import urlparse
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from app.core.errors import NotFoundError, BadRequestError, StorageError
from app.models.enums import SourceType, SourceStatus
from app.models.source import SourceEntity, utc_now
from app.repositories.firestore import firestore_repository

router = APIRouter(prefix="/sources", tags=["sources"])


class CreateSourceRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    type: SourceType
    platform: str = Field(min_length=2, max_length=50)
    url: str = Field(min_length=5, max_length=500)
    priority: int = Field(default=10, ge=1, le=100)
    categories: List[str] = Field(default_factory=list)
    enabled: bool = True


class UpdateSourceRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    enabled: Optional[bool] = None
    priority: Optional[int] = Field(default=None, ge=1, le=100)
    categories: Optional[List[str]] = None
    status: Optional[SourceStatus] = None


def validate_url(url: str) -> None:
    """Ensures URL has a valid scheme and netloc."""
    try:
        parsed = urlparse(url)
        if not (parsed.scheme in ("http", "https") and parsed.netloc):
            raise ValueError()
    except Exception:
        raise BadRequestError(f"Invalid URL format: '{url}'. Must start with http:// or https://")


@router.post("", response_model=SourceEntity, status_code=201)
async def create_source(req: CreateSourceRequest):
    """Registers a new approved source in the source registry."""
    validate_url(req.url)

    source_id = f"src_{uuid.uuid4().hex[:8]}"
    now = utc_now()

    source = SourceEntity(
        id=source_id,
        name=req.name.strip(),
        type=req.type,
        platform=req.platform.lower().strip(),
        url=req.url.strip(),
        enabled=req.enabled,
        priority=req.priority,
        categories=[c.lower().strip() for c in req.categories],
        status=SourceStatus.CONFIGURED,
        created_at=now,
        updated_at=now,
    )

    stored = await firestore_repository.create("sources", source.id, source.model_dump(mode="json"))
    return SourceEntity(**stored)


@router.get("", response_model=List[SourceEntity])
async def list_sources(
    type: Optional[SourceType] = None,
    enabled: Optional[bool] = None,
    limit: int = Query(default=50, ge=1, le=100),
):
    """Lists registered sources with optional filtering."""
    try:
        raw_items = await firestore_repository.list("sources", limit=limit)
    except StorageError:
        # Graceful fallback if emulator is offline during early frontend exploration
        return []

    sources = [SourceEntity(**item) for item in raw_items if "id" in item and "type" in item]

    if type is not None:
        sources = [s for s in sources if s.type == type]
    if enabled is not None:
        sources = [s for s in sources if s.enabled == enabled]

    return sorted(sources, key=lambda s: (-s.priority, s.name.lower()))


@router.get("/{source_id}", response_model=SourceEntity)
async def get_source(source_id: str):
    """Retrieves a single source by ID."""
    stored = await firestore_repository.get("sources", source_id)
    if not stored:
        raise NotFoundError(f"Source with id '{source_id}' not found.")
    return SourceEntity(**stored)


@router.patch("/{source_id}", response_model=SourceEntity)
async def update_source(source_id: str, req: UpdateSourceRequest):
    """Updates source settings (e.g. enable/disable, priority, categories)."""
    existing = await firestore_repository.get("sources", source_id)
    if not existing:
        raise NotFoundError(f"Source with id '{source_id}' not found.")

    update_fields = req.model_dump(exclude_unset=True, mode="json")
    if "categories" in update_fields and update_fields["categories"]:
        update_fields["categories"] = [c.lower().strip() for c in update_fields["categories"]]

    update_fields["updated_at"] = utc_now().isoformat()

    updated = await firestore_repository.update("sources", source_id, update_fields)
    return SourceEntity(**updated)


@router.delete("/{source_id}")
async def delete_source(source_id: str):
    """Removes a source from the registry."""
    existing = await firestore_repository.get("sources", source_id)
    if not existing:
        raise NotFoundError(f"Source with id '{source_id}' not found.")

    await firestore_repository.delete("sources", source_id)
    return {"message": f"Source '{source_id}' deleted successfully.", "deleted": True}


@router.post("/{source_id}/test")
async def test_source_connectivity(source_id: str):
    """Tests network reachability of a registered source."""
    existing = await firestore_repository.get("sources", source_id)
    if not existing:
        raise NotFoundError(f"Source with id '{source_id}' not found.")

    source = SourceEntity(**existing)
    parsed = urlparse(source.url)
    host = parsed.netloc.split(":")[0]
    port = parsed.port or (443 if parsed.scheme == "https" else 80)

    reachable = False
    details = ""
    try:
        with socket.create_connection((host, port), timeout=2.0):
            reachable = True
            details = f"Successfully connected to {host}:{port}"
    except Exception as exc:
        details = f"Connection failed to {host}:{port}: {str(exc)}"

    new_status = SourceStatus.HEALTHY if reachable else SourceStatus.WARNING
    await firestore_repository.update(
        "sources",
        source_id,
        {"status": new_status.value, "updated_at": utc_now().isoformat()},
    )

    return {
        "source_id": source_id,
        "name": source.name,
        "reachable": reachable,
        "status": new_status.value,
        "details": details,
    }
