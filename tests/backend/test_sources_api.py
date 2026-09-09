import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

backend_dir = Path(__file__).resolve().parent.parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.main import app
from app.repositories.firestore import firestore_repository

client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_in_memory_firestore(monkeypatch):
    """Provides an in-memory dictionary backing firestore_repository for API tests."""
    mock_db = {}

    async def mock_create(collection: str, doc_id: str, data: dict):
        key = f"{collection}/{doc_id}"
        stored = {**data, "_id": doc_id}
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


def test_create_and_get_source():
    """Verify source registration and retrieval."""
    payload = {
        "name": "Black Bear Forge",
        "type": "youtube_channel",
        "platform": "youtube",
        "url": "https://www.youtube.com/@blackbearforge",
        "priority": 15,
        "categories": ["blacksmithing", "toolmaking"],
        "enabled": True,
    }

    # 1. Create
    res = client.post("/api/sources", json=payload)
    assert res.status_code == 201
    source = res.json()
    assert source["name"] == "Black Bear Forge"
    assert source["priority"] == 15
    assert source["status"] == "configured"
    source_id = source["id"]

    # 2. Get by ID
    get_res = client.get(f"/api/sources/{source_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == source_id


def test_source_validation_rejects_bad_url():
    """Verify malformed URLs are rejected with 400 Bad Request."""
    bad_payload = {
        "name": "Bad Feed",
        "type": "rss_feed",
        "platform": "rss",
        "url": "not-a-real-url",
        "priority": 5,
    }
    res = client.post("/api/sources", json=bad_payload)
    assert res.status_code == 400
    assert res.json()["error"]["code"] == "BAD_REQUEST"


def test_list_and_filter_sources():
    """Verify list filtering by source type and enabled status."""
    # Add YouTube source
    client.post("/api/sources", json={
        "name": "Alec Steele",
        "type": "youtube_channel",
        "platform": "youtube",
        "url": "https://www.youtube.com/@AlecSteele",
        "priority": 20,
        "enabled": True,
    })

    # Add RSS source (disabled)
    client.post("/api/sources", json={
        "name": "Blade Magazine RSS",
        "type": "rss_feed",
        "platform": "rss",
        "url": "https://blademag.com/feed",
        "priority": 5,
        "enabled": False,
    })

    # List all
    all_res = client.get("/api/sources")
    assert all_res.status_code == 200
    assert len(all_res.json()) >= 2

    # Filter by enabled=true
    enabled_res = client.get("/api/sources?enabled=true")
    assert all(s["enabled"] is True for s in enabled_res.json())

    # Filter by type=rss_feed
    rss_res = client.get("/api/sources?type=rss_feed")
    assert all(s["type"] == "rss_feed" for s in rss_res.json())


def test_update_and_disable_source():
    """Verify PATCH can toggle enabled state and adjust priority."""
    res = client.post("/api/sources", json={
        "name": "Torbjorn Ahman",
        "type": "youtube_channel",
        "platform": "youtube",
        "url": "https://www.youtube.com/@torbjornahman",
        "priority": 10,
        "enabled": True,
    })
    source_id = res.json()["id"]

    # Disable source
    patch_res = client.patch(f"/api/sources/{source_id}", json={"enabled": False, "priority": 30})
    assert patch_res.status_code == 200
    assert patch_res.json()["enabled"] is False
    assert patch_res.json()["priority"] == 30


def test_delete_source():
    """Verify deleting removes source from registry."""
    res = client.post("/api/sources", json={
        "name": "Temporary Source",
        "type": "product_api",
        "platform": "amazon",
        "url": "https://amazon.com/tools",
    })
    source_id = res.json()["id"]

    del_res = client.delete(f"/api/sources/{source_id}")
    assert del_res.status_code == 200

    # Next GET returns 404
    after_res = client.get(f"/api/sources/{source_id}")
    assert after_res.status_code == 404
