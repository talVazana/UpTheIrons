import hashlib
import re
from typing import Optional
from app.models.enums import ContentType
from app.models.content import ContentEnvelope


def normalize_title(title: str) -> str:
    """Lowercases, trims, and strips punctuation for content title fingerprinting."""
    cleaned = re.sub(r"[^\w\s]", "", title.lower())
    return re.sub(r"\s+", " ", cleaned).strip()


def compute_url_hash(url: str) -> str:
    """Generates a stable SHA256 hex digest prefix for canonical URLs."""
    canonical = url.strip().rstrip("/").lower()
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


def compute_deduplication_key(
    content_type: ContentType,
    *,
    external_id: Optional[str] = None,
    canonical_url: Optional[str] = None,
    slug: Optional[str] = None,
    title: Optional[str] = None,
) -> str:
    """Computes a deterministic unique key preventing duplicate content ingestion."""
    if content_type == ContentType.VIDEO and external_id:
        # YouTube video ID is primary unique key
        return f"video:youtube:{external_id.strip()}"

    if content_type == ContentType.MATERIAL and slug:
        return f"material:{slug.strip().lower()}"

    if canonical_url:
        url_hash = compute_url_hash(canonical_url)
        return f"{content_type.value}:url:{url_hash}"

    if external_id:
        return f"{content_type.value}:id:{external_id.strip()}"

    if title:
        title_hash = hashlib.sha256(normalize_title(title).encode("utf-8")).hexdigest()[:16]
        return f"{content_type.value}:title:{title_hash}"

    raise ValueError("Cannot compute deduplication key without external_id, url, slug, or title.")


def get_envelope_deduplication_key(envelope: ContentEnvelope) -> str:
    """Extracts the deduplication key directly from a ContentEnvelope."""
    ext_id = envelope.metadata.get("youtube_video_id") or envelope.metadata.get("external_id")
    canonical_url = envelope.source.source_url if envelope.source else None
    return compute_deduplication_key(
        envelope.type,
        external_id=ext_id,
        canonical_url=canonical_url,
        slug=envelope.slug,
        title=envelope.title,
    )
