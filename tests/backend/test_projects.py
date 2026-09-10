import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

backend_dir = Path(__file__).resolve().parent.parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.main import app
from app.repositories.firestore import firestore_repository

@pytest.fixture(autouse=True)
def reset_in_memory_firestore(monkeypatch):
    """Provides an in-memory dictionary backing firestore_repository for tool tests."""
    mock_db = {}

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
        # Return all for simplicity
        return list(mock_db.values())

    monkeypatch.setattr(firestore_repository, "create", mock_create)
    monkeypatch.setattr(firestore_repository, "get", mock_get)
    monkeypatch.setattr(firestore_repository, "update", mock_update)
    monkeypatch.setattr(firestore_repository, "delete", mock_delete)
    monkeypatch.setattr(firestore_repository, "list", mock_list)

@pytest.fixture
def client():
    return TestClient(app)



def test_19_01_project_model_seeded(client):
    """19.01 Project Model: Verify beginner, intermediate, advanced seeded projects."""
    res = client.get("/api/v1/projects")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 3
    
    slugs = [p["slug"] for p in data["projects"]]
    assert "classic-s-hook" in slugs
    assert "wolf-jaw-tongs" in slugs
    assert "camp-knife" in slugs

def test_19_02_beginner_project(client):
    """19.02 Beginner Project: Verify S-Hook properties."""
    res = client.get("/api/v1/projects/classic-s-hook")
    assert res.status_code == 200
    data = res.json()
    meta = data["metadata"]
    assert meta["difficulty_level"] == "beginner"
    assert len(meta["steps"]) > 0
    assert "safety_precautions" in meta

def test_19_03_intermediate_project(client):
    """19.03 Intermediate Project: Verify Wolf Jaw Tongs properties."""
    res = client.get("/api/v1/projects/wolf-jaw-tongs")
    assert res.status_code == 200
    meta = res.json()["metadata"]
    assert meta["difficulty_level"] == "intermediate"

def test_19_04_advanced_project(client):
    """19.04 Advanced Project: Verify Camp Knife properties."""
    res = client.get("/api/v1/projects/camp-knife")
    assert res.status_code == 200
    meta = res.json()["metadata"]
    assert meta["difficulty_level"] == "advanced"

def test_19_05_list_and_filter(client):
    """19.05 Project Navigation: Filters."""
    res = client.get("/api/v1/projects?difficulty=beginner")
    assert res.status_code == 200
    projects = res.json()["projects"]
    assert len(projects) >= 1
    assert projects[0]["metadata"]["difficulty_level"] == "beginner"

def test_19_06_search_projects(client):
    """Search for skills learned or tools."""
    res = client.get("/api/v1/projects?q=tongs")
    assert res.status_code == 200
    assert res.json()["total"] >= 1
