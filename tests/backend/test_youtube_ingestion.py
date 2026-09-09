import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

backend_dir = Path(__file__).resolve().parent.parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.main import app
from app.repositories.firestore import firestore_repository
from app.services.youtube_client import youtube_client
from app.services.youtube_ingestion import normalize_youtube_video, _derive_category_and_tags
from app.models.enums import ContentType, SourceStatus
from app.api.v1.settings import _cached_keys

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_in_memory_firestore(monkeypatch):
    """Provides an in-memory dictionary backing firestore_repository for API tests."""
    mock_db = {}
    _cached_keys["youtube_api_key"] = None
    _cached_keys["gemini_api_key"] = None

    async def mock_create(collection: str, doc_id: str, data: dict):
        key = f"{collection}/{doc_id}"
        stored = {**data, "_id": doc_id, "id": doc_id}
        mock_db[key] = stored
        return stored

    async def mock_get(collection: str, doc_id: str):
        return mock_db.get(f"{collection}/{doc_id}")

    async def mock_update(collection: str, doc_id: str, data: dict):
        key = f"{collection}/{doc_id}"
        if key not in mock_db:
            return None
        mock_db[key].update(data)
        return mock_db[key]

    async def mock_delete(collection: str, doc_id: str):
        key = f"{collection}/{doc_id}"
        if key in mock_db:
            del mock_db[key]
            return True
        return False

    async def mock_list(collection: str, limit: int = 50):
        prefix = f"{collection}/"
        return [v for k, v in mock_db.items() if k.startswith(prefix)]

    monkeypatch.setattr(firestore_repository, "create", mock_create)
    monkeypatch.setattr(firestore_repository, "get", mock_get)
    monkeypatch.setattr(firestore_repository, "update", mock_update)
    monkeypatch.setattr(firestore_repository, "delete", mock_delete)
    monkeypatch.setattr(firestore_repository, "list", mock_list)


def test_settings_api_keys_flow():
    """11.01: Tests setting API keys via API and masking response."""
    # 1. Check initial state
    resp = client.get("/api/v1/settings/keys")
    assert resp.status_code == 200
    data = resp.json()
    assert "youtube_api_key_configured" in data

    # 2. Update YouTube key
    update_payload = {"youtube_api_key": "AIzaSyRealForgeKey123456789"}
    resp = client.post("/api/v1/settings/keys", json=update_payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["youtube_api_key_configured"] is True
    assert data["youtube_api_key_masked"].startswith("AIzaSy")
    assert data["youtube_api_key_masked"].endswith("6789")
    assert "RealForgeKey" not in data["youtube_api_key_masked"]


def test_youtube_client_uploads_converter():
    """11.02: Tests conversion from UC channel ID to UU uploads playlist ID."""
    channel_id = "UC42V83RPrCEmaS5D4p_2b6A"
    uploads_id = youtube_client.channel_id_to_uploads_playlist(channel_id)
    assert uploads_id == "UU42V83RPrCEmaS5D4p_2b6A"


def test_normalize_youtube_video():
    """11.05: Tests normalization of raw YouTube metadata into ContentEnvelope."""
    raw = {
        "video_id": "test_123",
        "title": "Beginner Knife Making: Forging 1084 High Carbon Steel",
        "description": "How to forge and heat treat a knife blade using simple coal forge techniques.",
        "published_at": "2026-09-08T12:00:00Z",
        "channel_id": "yt_blackbearforge",
        "channel_name": "Black Bear Forge",
        "thumbnail_url": "https://example.com/thumb.jpg",
        "duration_seconds": 600,
    }
    envelope = normalize_youtube_video(raw)
    assert envelope.id == "yt_test_123"
    assert envelope.type == ContentType.VIDEO
    assert envelope.category == "bladesmithing"
    assert "steel" in envelope.tags or "bladesmithing" in envelope.tags
    assert envelope.source.source_name == "Black Bear Forge"
    assert envelope.metadata["youtube_video_id"] == "test_123"
    assert envelope.metadata["deduplication_key"] == "video:youtube:test_123"


def test_sync_channel_and_deduplication():
    """
    11.06, 11.07, 11.10:
    Tests synchronization of one channel, storing items, updating channel counts,
    and verifying second run deduplication.
    """
    # 1. Register approved channel
    create_resp = client.post(
        "/api/youtube/channels",
        json={
            "url_or_handle": "@TorbjornAhman",
            "name": "Torbjörn Åhman",
            "priority": 10,
            "categories": ["blacksmithing", "tools"],
        },
    )
    assert create_resp.status_code == 201
    channel_id = create_resp.json()["id"]

    # 2. First Sync -> stores new items
    sync_resp = client.post(f"/api/youtube/channels/{channel_id}/sync")
    assert sync_resp.status_code == 200
    summary = sync_resp.json()
    assert summary["status"] == "SUCCESS"
    assert summary["new_items"] > 0
    assert summary["duplicates"] == 0
    first_new = summary["new_items"]

    # Channel video count should be updated
    ch_resp = client.get(f"/api/youtube/channels/{channel_id}")
    assert ch_resp.status_code == 200
    assert ch_resp.json()["video_count"] == first_new
    assert ch_resp.json()["status"] == SourceStatus.HEALTHY.value

    # 3. Second Sync -> deduplication prevents duplicate insert
    sync_resp_2 = client.post(f"/api/youtube/channels/{channel_id}/sync")
    assert sync_resp_2.status_code == 200
    summary_2 = sync_resp_2.json()
    assert summary_2["status"] == "SUCCESS"
    assert summary_2["new_items"] == 0
    assert summary_2["duplicates"] == first_new


def test_videos_feed_api():
    """11.08, 11.09: Tests video listing, filtering, and single video retrieval."""
    # Register and sync a channel
    client.post(
        "/api/youtube/channels",
        json={"url_or_handle": "@BlackBearForge", "name": "Black Bear Forge"},
    )
    client.post("/api/youtube/channels/yt_blackbearforge/sync")

    # List videos
    resp = client.get("/api/v1/videos")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] > 0
    assert len(data["videos"]) > 0

    first_video = data["videos"][0]
    vid_id = first_video["id"]

    # Fetch single video
    single_resp = client.get(f"/api/v1/videos/{vid_id}")
    assert single_resp.status_code == 200
    assert single_resp.json()["id"] == vid_id


def test_sync_all_and_logs():
    """11.11, 11.12: Tests batch sync across all channels and viewing sync logs."""
    client.post(
        "/api/youtube/channels",
        json={"url_or_handle": "@AlecSteele", "name": "Alec Steele"},
    )
    client.post(
        "/api/youtube/channels",
        json={"url_or_handle": "@BlackBearForge", "name": "Black Bear Forge"},
    )

    # Trigger all channels sync
    resp = client.post("/api/youtube/sync")
    assert resp.status_code == 200
    summaries = resp.json()
    assert len(summaries) >= 2
    assert all(s["status"] == "SUCCESS" for s in summaries)

    # Check sync logs
    logs_resp = client.get("/api/youtube/sync-logs")
    assert logs_resp.status_code == 200
    logs_data = logs_resp.json()
    assert logs_data["total"] >= 2


def test_disabled_channel_cannot_sync():
    """11.10: Tests that disabled channels are rejected from sync."""
    create_resp = client.post(
        "/api/youtube/channels",
        json={"url_or_handle": "@DisabledMaker", "name": "Disabled Maker"},
    )
    ch_id = create_resp.json()["id"]

    # Disable channel
    client.patch(f"/api/youtube/channels/{ch_id}", json={"enabled": False})

    # Attempt sync
    sync_resp = client.post(f"/api/youtube/channels/{ch_id}/sync")
    assert sync_resp.status_code == 400
    assert "disabled" in sync_resp.json()["error"]["message"].lower()
