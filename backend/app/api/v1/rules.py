from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.models.content import ContentEnvelope
from app.models.enums import ContentStatus
from app.services.rules_service import (
    RuleDocument,
    EditorialOverrideRequest,
    rules_service,
)
from app.services.rule_validator import (
    ContentValidationResult,
    rule_validator,
)

router = APIRouter(prefix="/rules", tags=["rules"])


class RuleSummary(BaseModel):
    id: str
    filename: str
    title: str
    description: Optional[str] = None
    section_count: int
    updated_at: str


class ValidateContentRequest(BaseModel):
    title: str = Field(min_length=2, max_length=300)
    text: str = Field(min_length=5)
    tags: Optional[List[str]] = Field(default_factory=list)
    source_name: Optional[str] = None


@router.get("", response_model=List[RuleSummary])
async def list_rules():
    """Returns summaries of all active rules loaded from config directory."""
    docs = rules_service.list_rules()
    return [
        RuleSummary(
            id=d.id,
            filename=d.filename,
            title=d.title,
            description=d.description,
            section_count=len(d.sections),
            updated_at=d.updated_at,
        )
        for d in docs
    ]


@router.get("/{rule_id}", response_model=RuleDocument)
async def get_rule_detail(rule_id: str):
    """Returns full content and parsed sections of a specific rule document."""
    doc = rules_service.get_rule(rule_id)
    if not doc:
        raise HTTPException(
            status_code=404,
            detail=f"Rule document '{rule_id}' not found in configuration.",
        )
    return doc


@router.post("/reload", response_model=List[RuleSummary])
async def reload_rules():
    """Reloads all rule configuration files from disk without backend restart."""
    docs = rules_service.load_all()
    return [
        RuleSummary(
            id=d.id,
            filename=d.filename,
            title=d.title,
            description=d.description,
            section_count=len(d.sections),
            updated_at=d.updated_at,
        )
        for d in docs.values()
    ]


@router.post("/validate", response_model=ContentValidationResult)
async def validate_content(request: ValidateContentRequest):
    """
    Validates content against safety, anti-spam, clickbait, and craft relevance rules.
    Returns detected violations, relevance score, and recommended content status.
    """
    return rule_validator.validate_content(
        title=request.title,
        text=request.text,
        tags=request.tags,
        source_name=request.source_name,
    )


@router.post("/override/{content_id}", response_model=ContentEnvelope)
async def apply_editorial_override(content_id: str, request: EditorialOverrideRequest):
    """
    Applies an editorial override (featured, pinned, verified, needs_review, hidden)
    to a content item in the vault.
    """
    updated = await rules_service.apply_editorial_override(content_id, request)
    if not updated:
        raise HTTPException(
            status_code=404,
            detail=f"Content item '{content_id}' not found in vault.",
        )
    return updated
