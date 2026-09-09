from datetime import datetime, timezone
import logging
import re
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.core.errors import NotFoundError, BadRequestError, SourceError
from app.models.content import ContentEnvelope, utc_now
from app.models.enums import ContentType, ContentStatus, DifficultyLevel, SourceType, SourceStatus
from app.models.source import SourceProvenance
from app.models.deduplication import compute_deduplication_key
from app.repositories.firestore import firestore_repository
from app.services.youtube_client import youtube_client

logger = logging.getLogger("blacksmith_knight.youtube_ingestion")

CONTENT_COLLECTION = "content"
CHANNELS_COLLECTION = "youtube_channels"
SYNC_LOGS_COLLECTION = "sync_logs"


class SyncSummary(BaseModel):
    channel_id: str
    channel_name: str
    discovered: int = 0
    new_items: int = 0
    duplicates: int = 0
    errors: List[str] = Field(default_factory=list)
    started_at: datetime = Field(default_factory=utc_now)
    completed_at: Optional[datetime] = None
    status: str = "SUCCESS"


def _derive_category_and_tags(title: str, description: str) -> tuple[str, List[str]]:
    """Inspects text to assign initial forging categories and tags deterministically."""
    combined = f"{title} {description}".lower()
    tags = set()

    keywords = {
        "anvil": ["anvil", "hardy", "horn"],
        "heat-treatment": ["heat treat", "quench", "hardening", "tempering", "normalizing", "anneal"],
        "bladesmithing": ["knife", "blade", "sword", "dagger", "bevel", "damascus"],
        "tongs": ["tongs", "holding"],
        "hammer": ["hammer", "striking", "sledge"],
        "forge": ["forge", "coal", "gas", "burner", "fire"],
        "steel": ["1084", "1095", "5160", "tool steel", "mild steel", "carbon steel"],
        "grinding": ["grind", "belt", "abrasive", "wheel"],
    }

    for tag_name, word_list in keywords.items():
        if any(w in combined for w in word_list):
            tags.add(tag_name)

    if not tags:
        tags.add("blacksmithing")

    # Category determination
    if "bladesmithing" in tags or "knife" in combined:
        category = "bladesmithing"
    elif "heat-treatment" in tags:
        category = "heat-treatment"
    elif "hammer" in tags or "tongs" in tags or "anvil" in tags:
        category = "tools"
    else:
        category = "forging"

    return category, sorted(list(tags))


def normalize_youtube_video(raw_video: Dict[str, Any]) -> ContentEnvelope:
    """
    Transforms raw YouTube API / mock video payload into standardized ContentEnvelope.
    """
    video_id = raw_video["video_id"]
    title = raw_video["title"].strip()
    description = raw_video.get("description", "").strip()
    channel_id = raw_video["channel_id"]
    channel_name = raw_video.get("channel_name", "YouTube Creator")
    published_str = raw_video.get("published_at")

    # Clean published date
    if published_str:
        try:
            published_at = datetime.fromisoformat(published_str.replace("Z", "+00:00"))
        except Exception:
            published_at = utc_now()
    else:
        published_at = utc_now()

    # Clean slug
    clean_title = re.sub(r"[^\w\s\-]", "", title).lower()
    slug = re.sub(r"[\s_]+", "-", clean_title).strip("-")[:80] or f"video-{video_id}"

    # Clean summary (min 5, max 1000)
    summary = description.replace("\n", " ").strip()
    if len(summary) > 950:
        summary = summary[:947] + "..."
    if len(summary) < 5:
        summary = f"Blacksmithing video tutorial: {title} by {channel_name}."

    category, tags = _derive_category_and_tags(title, description)

    envelope_id = f"yt_{video_id}"
    dedup_key = compute_deduplication_key(ContentType.VIDEO, external_id=video_id)

    return ContentEnvelope(
        id=envelope_id,
        type=ContentType.VIDEO,
        title=title[:200],
        slug=slug,
        summary=summary,
        category=category,
        tags=tags,
        difficulty=DifficultyLevel.BEGINNER if "beginner" in title.lower() or "basics" in title.lower() else DifficultyLevel.INTERMEDIATE,
        source=SourceProvenance(
            source_type=SourceType.YOUTUBE_CHANNEL,
            source_id=channel_id,
            source_name=channel_name,
            source_url=f"https://www.youtube.com/watch?v={video_id}",
            retrieved_at=utc_now(),
        ),
        image_url=raw_video.get("thumbnail_url"),
        status=ContentStatus.PUBLISHED,
        published_at=published_at,
        created_at=utc_now(),
        updated_at=utc_now(),
        metadata={
            "youtube_video_id": video_id,
            "channel_id": channel_id,
            "channel_name": channel_name,
            "duration_seconds": raw_video.get("duration_seconds", 0),
            "embed_url": f"https://www.youtube.com/embed/{video_id}",
            "deduplication_key": dedup_key,
        },
    )


class YouTubeIngestionService:
    """Coordinates deterministic fetching, normalization, deduplication, and persistence."""

    async def sync_channel(self, channel_id: str, max_videos: int = 20) -> SyncSummary:
        """
        Synchronizes a single approved YouTube channel.
        Guarantees idempotency and deduplication.
        """
        # 1. Fetch channel entity
        channel_data = await firestore_repository.get(CHANNELS_COLLECTION, channel_id)
        if not channel_data:
            raise NotFoundError(f"YouTube channel with ID '{channel_id}' not found in registry.")

        if not channel_data.get("enabled", True):
            raise BadRequestError(f"Cannot synchronize disabled channel '{channel_data.get('name', channel_id)}'.")

        channel_name = channel_data.get("name", "Unknown Channel")
        summary = SyncSummary(channel_id=channel_id, channel_name=channel_name)

        try:
            # 2. Fetch raw video batch from client
            raw_videos = await youtube_client.fetch_channel_videos(
                channel_id=channel_id,
                channel_name=channel_name,
                max_results=max_videos,
            )
            summary.discovered = len(raw_videos)

            # 3. Process each video with deduplication
            for raw_video in raw_videos:
                try:
                    envelope = normalize_youtube_video(raw_video)
                    existing_doc = await firestore_repository.get(CONTENT_COLLECTION, envelope.id)

                    if existing_doc:
                        # Video already exists in vault - prevent duplicate write
                        summary.duplicates += 1
                        logger.debug("Deduplicated video: %s already exists", envelope.id)
                    else:
                        # New video: persist to vault
                        await firestore_repository.create(
                            CONTENT_COLLECTION,
                            envelope.id,
                            envelope.model_dump(mode="json"),
                        )
                        summary.new_items += 1
                        logger.info("Stored new video %s: %s", envelope.id, envelope.title)
                except Exception as ex:
                    err_msg = f"Failed processing video {raw_video.get('video_id')}: {str(ex)}"
                    logger.error(err_msg)
                    summary.errors.append(err_msg)

            # 4. Update channel statistics & health in registry
            updated_video_count = channel_data.get("video_count", 0) + summary.new_items
            await firestore_repository.update(
                CHANNELS_COLLECTION,
                channel_id,
                {
                    "video_count": updated_video_count,
                    "last_synced_at": utc_now().isoformat(),
                    "status": SourceStatus.HEALTHY.value,
                    "last_error": None,
                },
            )

        except Exception as ex:
            summary.status = "FAILED"
            summary.errors.append(str(ex))
            logger.error("Channel sync failed for %s: %s", channel_id, str(ex))
            # Record error on channel doc
            await firestore_repository.update(
                CHANNELS_COLLECTION,
                channel_id,
                {
                    "status": SourceStatus.ERROR.value,
                    "last_error": str(ex),
                },
            )

        summary.completed_at = utc_now()

        # 5. Persist sync log record
        log_id = f"synclog_{channel_id}_{int(summary.started_at.timestamp())}"
        try:
            await firestore_repository.create(
                SYNC_LOGS_COLLECTION,
                log_id,
                summary.model_dump(mode="json"),
            )
        except Exception as log_ex:
            logger.warning("Could not persist sync log: %s", str(log_ex))

        return summary

    async def sync_all_enabled_channels(self, max_per_channel: int = 15) -> List[SyncSummary]:
        """
        Synchronizes all enabled channels sequentially.
        Guarantees partial failure isolation: one channel failure does not halt others.
        """
        channels = await firestore_repository.list(CHANNELS_COLLECTION, limit=100)
        summaries: List[SyncSummary] = []

        for ch in channels:
            if not ch.get("enabled", True):
                continue

            channel_id = ch["id"]
            try:
                summary = await self.sync_channel(channel_id, max_videos=max_per_channel)
                summaries.append(summary)
            except Exception as ex:
                logger.error("Channel %s encountered unhandled sync exception: %s", channel_id, str(ex))
                fail_summary = SyncSummary(
                    channel_id=channel_id,
                    channel_name=ch.get("name", "Unknown Channel"),
                    status="FAILED",
                    errors=[str(ex)],
                    completed_at=utc_now(),
                )
                summaries.append(fail_summary)

        return summaries


youtube_ingestion_service = YouTubeIngestionService()
