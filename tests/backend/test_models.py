import sys
from pathlib import Path
import pytest
from pydantic import ValidationError

backend_dir = Path(__file__).resolve().parent.parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.models.enums import ContentType, ContentStatus, DifficultyLevel, SourceType
from app.models.content import ContentEnvelope, MaterialMetadata
from app.models.source import SourceProvenance, SourceEntity, YouTubeChannelEntity
from app.models.deduplication import compute_deduplication_key, get_envelope_deduplication_key
from app.models.seed import seed_initial_data, SEED_MATERIALS
from app.repositories.base import BaseRepository


def test_content_envelope_validation():
    """Verify validation on required fields and slug normalization."""
    item = ContentEnvelope(
        id="test-item",
        type=ContentType.MATERIAL,
        title="Forge Hammer Basics",
        slug="Forge Hammer Basics ",
        summary="Understanding hammer weights and balance.",
        category="tools",
    )
    assert item.slug == "forge-hammer-basics"
    assert item.status == ContentStatus.PUBLISHED
    assert item.created_at is not None

    # Title too short
    with pytest.raises(ValidationError):
        ContentEnvelope(
            id="bad",
            type=ContentType.GUIDE,
            title="A",
            slug="a",
            summary="short",
            category="guides",
        )


def test_material_metadata_validation():
    """Verify metallurgical parameters reject out-of-bound percentages."""
    meta = MaterialMetadata(
        classification="High Carbon",
        carbon_pct=0.95,
        alloying_elements={"manganese": 0.3},
    )
    assert meta.carbon_pct == 0.95

    # Impossible carbon percentage
    with pytest.raises(ValidationError):
        MaterialMetadata(
            classification="High Carbon",
            carbon_pct=9.5,
        )


def test_youtube_channel_entity():
    """Verify channel management entity constraints."""
    channel = YouTubeChannelEntity(
        id="chan-001",
        name="Black Bear Forge",
        url="https://youtube.com/@blackbearforge",
        youtube_channel_id="UCxxx123",
        handle="@blackbearforge",
        priority=10,
    )
    assert channel.platform == "youtube"
    assert channel.type == SourceType.YOUTUBE_CHANNEL
    assert channel.enabled is True
    assert channel.priority == 10


def test_deterministic_deduplication_keys():
    """Verify deduplication engine generates deterministic keys."""
    # YouTube video
    yt_key1 = compute_deduplication_key(ContentType.VIDEO, external_id="dQw4w9WgXcQ")
    yt_key2 = compute_deduplication_key(ContentType.VIDEO, external_id=" dQw4w9WgXcQ ")
    assert yt_key1 == "video:youtube:dQw4w9WgXcQ"
    assert yt_key1 == yt_key2

    # Material slug
    mat_key = compute_deduplication_key(ContentType.MATERIAL, slug="1084")
    assert mat_key == "material:1084"

    # Canonical URL
    url1 = "https://example.com/guide/anvil-rebound/"
    url2 = "https://example.com/guide/anvil-rebound"
    url_key1 = compute_deduplication_key(ContentType.GUIDE, canonical_url=url1)
    url_key2 = compute_deduplication_key(ContentType.GUIDE, canonical_url=url2)
    assert url_key1 == url_key2

    # Envelope helper
    envelope = SEED_MATERIALS[0]
    envelope_key = get_envelope_deduplication_key(envelope)
    assert envelope_key == "material:1084"


@pytest.mark.anyio
async def test_seed_initial_data():
    """Verify seed strategy populates repository fixtures."""
    fake_db = {}

    class MockRepository(BaseRepository):
        async def create(self, collection: str, doc_id: str, data: dict):
            fake_db[f"{collection}/{doc_id}"] = data
            return data

        async def get(self, collection: str, doc_id: str):
            return fake_db.get(f"{collection}/{doc_id}")

        async def update(self, collection: str, doc_id: str, data: dict):
            return data

        async def delete(self, collection: str, doc_id: str):
            return True

        async def list(self, collection: str, limit: int = 50):
            return list(fake_db.values())

    repo = MockRepository()
    counts = await seed_initial_data(repo)

    assert counts["materials"] == 3
    assert counts["projects"] == 1
    assert "content/mat-1084" in fake_db
    assert "content/mat-1095" in fake_db
    assert "content/mat-5160" in fake_db
    assert "content/proj-s-hook" in fake_db
