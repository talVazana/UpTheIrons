from typing import List, Optional
from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.core.errors import NotFoundError
from app.models.content import ContentEnvelope
from app.models.enums import ContentType
from app.repositories.firestore import firestore_repository

router = APIRouter(prefix="/articles", tags=["articles"])

CONTENT_COLLECTION = "content"


class ArticleListResponse(BaseModel):
    articles: List[ContentEnvelope]
    total: int
    limit: int
    offset: int


@router.get("", response_model=ArticleListResponse)
async def list_articles(
    category: Optional[str] = Query(None, description="Filter by category"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    feed_id: Optional[str] = Query(None, description="Filter by source feed ID"),
    limit: int = Query(24, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Returns paginated articles ingested from approved RSS feeds."""
    all_content = await firestore_repository.list(CONTENT_COLLECTION, limit=200)

    filtered: List[ContentEnvelope] = []
    for item in all_content:
        if item.get("type") != ContentType.ARTICLE.value and item.get("type") != ContentType.ARTICLE:
            continue

        if category and item.get("category") != category:
            continue

        if tag and tag not in item.get("tags", []):
            continue

        if feed_id:
            src = item.get("source", {})
            if src.get("source_id") != feed_id:
                continue

        try:
            envelope = ContentEnvelope.model_validate(item)
            filtered.append(envelope)
        except Exception:
            continue

    filtered.sort(
        key=lambda x: x.published_at or x.created_at,
        reverse=True,
    )

    total = len(filtered)
    paged = filtered[offset : offset + limit]

    return ArticleListResponse(
        articles=paged,
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{article_id}", response_model=ContentEnvelope)
async def get_article(article_id: str):
    """Retrieves a single article by ID."""
    clean_id = article_id if article_id.startswith("art_") else f"art_{article_id}"
    doc = await firestore_repository.get(CONTENT_COLLECTION, clean_id)
    if not doc:
        raise NotFoundError(f"Article with ID '{article_id}' not found in knowledge vault.")
    return ContentEnvelope.model_validate(doc)
