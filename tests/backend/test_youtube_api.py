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


def test_resolve_endpoint():
    # Test resolving by handle
    resp = client.post("/api/youtube/resolve", json={"query": "@BlackBearForge"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["handle"] == "@BlackBearForge"
    assert "canonical_url" in data
    assert data["canonical_url"] == "https://www.youtube.com/@BlackBearForge"
    assert data["name"] == "BlackBearForge"

    # Test resolving by channel URL
    resp_url = client.post(
        "/api/youtube/resolve",
        json={"query": "https://www.youtube.com/channel/UCb_S38Vp_k_u3K9v1A5H0pw"},
    )
    assert resp_url.status_code == 200
    data_url = resp_url.json()
    assert data_url["youtube_channel_id"] == "UCb_S38Vp_k_u3K9v1A5H0pw"
    assert data_url["canonical_url"] == "https://www.youtube.com/channel/UCb_S38Vp_k_u3K9v1A5H0pw"


def test_resolve_invalid_query():
    resp = client.post("/api/youtube/resolve", json={"query": "not a valid handle or url !@#$%"})
    assert resp.status_code == 400
    data = resp.json()
    assert data["error"]["code"] == "BAD_REQUEST"


def test_create_and_get_youtube_channel():
    payload = {
        "url_or_handle": "https://www.youtube.com/@BlackBearForge",
        "name": "Black Bear Forge",
        "priority": 25,
        "categories": ["Forging", "Anvil Techniques", "Tool Making"],
    }
    resp = client.post("/api/youtube/channels", json=payload)
    assert resp.status_code == 201
    created = resp.json()
    channel_id = created["id"]
    assert channel_id == "yt_blackbearforge"
    assert created["name"] == "Black Bear Forge"
    assert created["handle"] == "@BlackBearForge"
    assert created["enabled"] is True
    assert created["priority"] == 25
    assert "forging" in created["categories"]

    # Verify GET by id
    get_resp = client.get(f"/api/youtube/channels/{channel_id}")
    assert get_resp.status_code == 200
    fetched = get_resp.json()
    assert fetched["id"] == channel_id
    assert fetched["name"] == "Black Bear Forge"

    # Verify v1 path also works
    v1_resp = client.get(f"/api/v1/youtube/channels/{channel_id}")
    assert v1_resp.status_code == 200


def test_prevent_duplicate_channel():
    payload = {
        "url_or_handle": "@BlackBearForge",
        "name": "Black Bear Forge",
    }
    resp1 = client.post("/api/youtube/channels", json=payload)
    assert resp1.status_code == 201

    # Attempt second registration with same handle
    resp2 = client.post("/api/youtube/channels", json=payload)
    assert resp2.status_code == 400
    assert "already registered" in resp2.json()["error"]["message"]


def test_list_and_filter_channels():
    client.post(
        "/api/youtube/channels",
        json={"url_or_handle": "@BlackBearForge", "name": "Black Bear Forge", "priority": 30, "categories": ["Forging"]},
    )
    client.post(
        "/api/youtube/channels",
        json={"url_or_handle": "@ChristCenteredIronworks", "name": "Christ Centered Ironworks", "priority": 20, "categories": ["Tools"]},
    )

    list_resp = client.get("/api/youtube/channels")
    assert list_resp.status_code == 200
    data = list_resp.json()
    assert data["total"] == 2
    # Prioritized ordering
    assert data["channels"][0]["name"] == "Black Bear Forge"
    assert data["channels"][1]["name"] == "Christ Centered Ironworks"

    # Filter by category
    filter_resp = client.get("/api/youtube/channels?category=tools")
    assert filter_resp.status_code == 200
    cat_data = filter_resp.json()
    assert cat_data["total"] == 1
    assert cat_data["channels"][0]["name"] == "Christ Centered Ironworks"


def test_update_and_disable_channel():
    resp = client.post("/api/youtube/channels", json={"url_or_handle": "@TorbjornAhman", "name": "Torbjorn Ahman"})
    assert resp.status_code == 201
    cid = resp.json()["id"]

    # Update enabled to False
    patch_resp = client.patch(f"/api/youtube/channels/{cid}", json={"enabled": False, "priority": 50})
    assert patch_resp.status_code == 200
    updated = patch_resp.json()
    assert updated["enabled"] is False
    assert updated["priority"] == 50

    # Filter by enabled=True returns empty
    active_resp = client.get("/api/youtube/channels?enabled=true")
    assert active_resp.json()["total"] == 0

    # Filter by enabled=False returns 1
    disabled_resp = client.get("/api/youtube/channels?enabled=false")
    assert disabled_resp.json()["total"] == 1


def test_channel_sync_endpoint():
    resp = client.post("/api/youtube/channels", json={"url_or_handle": "@AlecSteele", "name": "Alec Steele"})
    cid = resp.json()["id"]

    # Sync succeeds when channel is enabled
    sync_resp = client.post(f"/api/youtube/channels/{cid}/sync")
    assert sync_resp.status_code == 200
    sync_data = sync_resp.json()
    assert sync_data["status"] == "SUCCESS"
    assert sync_data["new_items"] >= 0
    # Channel entity in registry is marked healthy
    ch_check = client.get(f"/api/youtube/channels/{cid}")
    assert ch_check.json()["status"] == "healthy"

    # Disable channel
    client.patch(f"/api/youtube/channels/{cid}", json={"enabled": False})

    # Sync fails with 400 Bad Request when channel is disabled
    sync_fail = client.post(f"/api/youtube/channels/{cid}/sync")
    assert sync_fail.status_code == 400
    assert "disabled" in sync_fail.json()["error"]["message"]


def test_delete_channel():
    resp = client.post("/api/youtube/channels", json={"url_or_handle": "@WalterSorrells", "name": "Walter Sorrells"})
    cid = resp.json()["id"]

    del_resp = client.delete(f"/api/youtube/channels/{cid}")
    assert del_resp.status_code == 200
    assert del_resp.json()["deleted"] is True

    get_resp = client.get(f"/api/youtube/channels/{cid}")
    assert get_resp.status_code == 404
