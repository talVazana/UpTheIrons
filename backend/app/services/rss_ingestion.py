from datetime import datetime, timezone
import logging
import re
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.core.errors import NotFoundError, BadRequestError, SourceError
from app.models.content import ContentEnvelope, utc_now
from app.models.enums import ContentType, ContentStatus, DifficultyLevel, SourceType, SourceStatus
from app.models.source import SourceProvenance
from app.models.deduplication import compute_deduplication_key, compute_url_hash
from app.repositories.firestore import firestore_repository
from app.services.rss_client import rss_client

logger = logging.getLogger("blacksmith_knight.rss_ingestion")

CONTENT_COLLECTION = "content"
RSS_FEEDS_COLLECTION = "rss_feeds"
SYNC_LOGS_COLLECTION = "sync_logs"


class RSSSyncSummary(BaseModel):
    feed_id: str
    feed_name: str
    discovered: int = 0
    new_items: int = 0
    duplicates: int = 0
    errors: List[str] = Field(default_factory=list)
    started_at: datetime = Field(default_factory=utc_now)
    completed_at: Optional[datetime] = None
    status: str = "SUCCESS"


def _derive_article_category_and_tags(title: str, summary: str) -> tuple[str, List[str]]:
    """Derives domain forge category and tags from article text."""
    combined = f"{title} {summary}".lower()
    tags = set()

    keywords = {
        "steel": ["steel", "alloy", "carbon", "1084", "1095", "5160", "tool steel", "w1", "o1"],
        "heat-treatment": ["heat treat", "hardening", "tempering", "normalizing", "quench", "austenite"],
        "anvil": ["anvil", "hardy", "rebound", "horn"],
        "forge": ["forge", "coal", "gas burner", "firepot", "fire"],
        "bladesmithing": ["knife", "blade", "sword", "dagger", "bevel", "edge"],
        "welding": ["forge weld", "flux", "borax", "pattern weld", "damascus"],
        "safety": ["ventilation", "respirator", "hearing", "eye protection", "scale", "ppe"],
    }

    for tag_name, words in keywords.items():
        if any(w in combined for w in words):
            tags.add(tag_name)

    if not tags:
        tags.add("blacksmithing")

    if "steel" in tags:
        category = "materials"
    elif "heat-treatment" in tags:
        category = "heat-treatment"
    elif "anvil" in tags or "forge" in tags:
        category = "tools"
    elif "bladesmithing" in tags:
        category = "bladesmithing"
    else:
        category = "guides"

    return category, sorted(list(tags))


def normalize_rss_article(raw_article: Dict[str, Any], feed_id: str, feed_name: str) -> ContentEnvelope:
    """Transforms raw parsed RSS item into standard ContentEnvelope."""
    title = raw_article.get("title", "Untitled Article").strip()
    url = raw_article.get("url", "").strip()
    raw_summary = raw_article.get("summary", "").strip()
    published_str = raw_article.get("published_at")
    author = raw_article.get("author", feed_name)

    try:
        published_at = datetime.fromisoformat(published_str.replace("Z", "+00:00")) if published_str else utc_now()
    except Exception:
        published_at = utc_now()

    # URL-based canonical ID
    url_hash = compute_url_hash(url)
    envelope_id = f"art_{url_hash}"

    # Clean slug
    clean_title = re.sub(r"[^\w\s\-]", "", title).lower()
    slug = re.sub(r"[\s_]+", "-", clean_title).strip("-")[:80] or f"article-{url_hash}"

    # Clean summary (min 5, max 1000)
    summary = raw_summary.replace("\n", " ").strip()
    if len(summary) > 950:
        summary = summary[:947] + "..."
    if len(summary) < 5:
        summary = f"Practical blacksmithing article: {title} by {author}."

    category, tags = _derive_article_category_and_tags(title, summary)
    dedup_key = compute_deduplication_key(ContentType.ARTICLE, canonical_url=url)

    return ContentEnvelope(
        id=envelope_id,
        type=ContentType.ARTICLE,
        title=title[:200],
        slug=slug,
        summary=summary,
        category=category,
        tags=tags,
        difficulty=DifficultyLevel.INTERMEDIATE,
        source=SourceProvenance(
            source_type=SourceType.RSS_FEED,
            source_id=feed_id,
            source_name=feed_name,
            source_url=url,
            retrieved_at=utc_now(),
        ),
        image_url="https://images.unsplash.com/photo-1504917599217-d4dc5ebe6122?w=800&auto=format&fit=crop&q=80",
        status=ContentStatus.PUBLISHED,
        published_at=published_at,
        created_at=utc_now(),
        updated_at=utc_now(),
        metadata={
            "article_url": url,
            "author": author,
            "feed_id": feed_id,
            "feed_name": feed_name,
            "deduplication_key": dedup_key,
        },
    )


class RSSIngestionService:
    """Manages RSS feed harvesting, deduplication, and persistence."""

    async def sync_feed(self, feed_id: str, max_articles: int = 20) -> RSSSyncSummary:
        """
        Synchronizes a single user-configured RSS feed.
        Guarantees strict deduplication and zero spider-crawling.
        """
        feed_data = await firestore_repository.get(RSS_FEEDS_COLLECTION, feed_id)
        if not feed_data:
            raise NotFoundError(f"RSS feed with ID '{feed_id}' not found in registry.")

        if not feed_data.get("enabled", True):
            raise BadRequestError(f"Cannot synchronize disabled RSS feed '{feed_data.get('name', feed_id)}'.")

        feed_name = feed_data.get("name", "Unknown RSS Feed")
        feed_url = feed_data.get("feed_url") or feed_data.get("url")
        summary = RSSSyncSummary(feed_id=feed_id, feed_name=feed_name)

        try:
            # Fetch feed XML and parse items directly
            feed_result = await rss_client.fetch_feed(feed_url, max_items=max_articles)
            articles = feed_result.get("articles", [])
            summary.discovered = len(articles)

            # Ingest only items present in feed XML (Anti-Crawling rule)
            for raw_art in articles:
                try:
                    envelope = normalize_rss_article(raw_art, feed_id, feed_name)
                    existing_doc = await firestore_repository.get(CONTENT_COLLECTION, envelope.id)

                    if existing_doc:
                        summary.duplicates += 1
                        logger.debug("Deduplicated article: %s already exists", envelope.id)
                    else:
                        await firestore_repository.create(
                            CONTENT_COLLECTION,
                            envelope.id,
                            envelope.model_dump(mode="json"),
                        )
                        summary.new_items += 1
                        logger.info("Stored new article %s: %s", envelope.id, envelope.title)
                except Exception as ex:
                    err_msg = f"Failed normalizing article {raw_art.get('url')}: {str(ex)}"
                    logger.error(err_msg)
                    summary.errors.append(err_msg)

            # Update feed stats
            updated_article_count = feed_data.get("article_count", 0) + summary.new_items
            await firestore_repository.update(
                RSS_FEEDS_COLLECTION,
                feed_id,
                {
                    "article_count": updated_article_count,
                    "last_synced_at": utc_now().isoformat(),
                    "status": SourceStatus.HEALTHY.value,
                    "last_error": None,
                },
            )

        except Exception as ex:
            summary.status = "FAILED"
            summary.errors.append(str(ex))
            logger.error("RSS sync failed for feed %s: %s", feed_id, str(ex))
            await firestore_repository.update(
                RSS_FEEDS_COLLECTION,
                feed_id,
                {
                    "status": SourceStatus.FAILED.value,
                    "last_error": str(ex),
                },
            )

        summary.completed_at = utc_now()

        # Record sync log
        log_id = f"synclog_rss_{feed_id}_{int(summary.started_at.timestamp())}"
        try:
            await firestore_repository.create(
                SYNC_LOGS_COLLECTION,
                log_id,
                summary.model_dump(mode="json"),
            )
        except Exception:
            pass

        return summary

    async def sync_all_enabled_feeds(self, max_per_feed: int = 15) -> List[RSSSyncSummary]:
        """Synchronizes all enabled RSS feeds with partial failure isolation."""
        feeds = await firestore_repository.list(RSS_FEEDS_COLLECTION, limit=100)
        summaries: List[RSSSyncSummary] = []

        for f in feeds:
            if not f.get("enabled", True):
                continue

            feed_id = f["id"]
            try:
                summary = await self.sync_feed(feed_id, max_articles=max_per_feed)
                summaries.append(summary)
            except Exception as ex:
                fail_summary = RSSSyncSummary(
                    feed_id=feed_id,
                    feed_name=f.get("name", "Unknown Feed"),
                    status="FAILED",
                    errors=[str(ex)],
                    completed_at=utc_now(),
                )
                summaries.append(fail_summary)

        return summaries


rss_ingestion_service = RSSIngestionService()
