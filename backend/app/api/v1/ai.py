from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.models.content import ContentEnvelope
from app.models.enums import ContentType
from app.services.ai.base import AIEnrichmentResult
from app.services.ai.service import ai_service

router = APIRouter(prefix="/ai", tags=["ai"])


class AIStatusResponse(BaseModel):
    provider: str
    model: str
    configured: bool
    enabled: bool


class AIPreviewRequest(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    text: str = Field(min_length=5, max_length=5000)
    content_type: str = Field(default="video")


class BatchEnrichResponse(BaseModel):
    total_pending: int
    processed: int
    success: int
    failed: int
    enriched_items: List[Dict[str, Any]]


@router.get("/status", response_model=AIStatusResponse)
async def get_ai_status():
    """Returns AI enrichment layer provider, configuration, and enabled status."""
    status = await ai_service.get_status()
    return AIStatusResponse(**status)


@router.post("/preview", response_model=Optional[AIEnrichmentResult])
async def preview_enrichment(request: AIPreviewRequest):
    """
    Directly runs enrichment on given text without reading or writing database.
    Useful for testing guardrails and verifying classifications.
    """
    provider = await ai_service.get_provider()
    if not provider:
        raise HTTPException(
            status_code=503,
            detail="AI enrichment provider is not configured or is disabled.",
        )
    result = await provider.enrich_content(
        title=request.title,
        text=request.text,
        content_type=request.content_type,
    )
    if not result:
        raise HTTPException(
            status_code=502,
            detail="AI provider failed to enrich content. Check provider connection and credentials.",
        )
    return result


@router.post("/enrich/{content_id}", response_model=ContentEnvelope)
async def enrich_content_item(content_id: str):
    """
    Enriches a single content item in the vault using AI.
    Preserves original values in metadata if modified.
    """
    enriched = await ai_service.enrich_and_save_by_id(content_id)
    if not enriched:
        raise HTTPException(
            status_code=404,
            detail=f"Content item '{content_id}' not found in vault.",
        )
    return enriched


@router.post("/enrich-pending", response_model=BatchEnrichResponse)
async def enrich_pending_content(
    limit: int = Query(default=10, ge=1, le=50, description="Cost boundary: maximum items to process"),
    content_type: Optional[ContentType] = Query(default=None, description="Optional content type filter"),
):
    """
    Batch enriches un-enriched items in the vault.
    Enforces cost boundary (14.10): processes only items where ai_processed != True up to limit.
    """
    results = await ai_service.batch_enrich_pending(limit=limit, content_type=content_type)
    return BatchEnrichResponse(**results)
