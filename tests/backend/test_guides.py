import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

backend_dir = Path(__file__).resolve().parent.parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.main import app
from app.models.enums import ContentType, ContentStatus, DifficultyLevel, TrustLabel
from app.models.content import (
    ContentEnvelope,
    GuideMetadata,
    SourceReference,
    SafetyPrecaution,
    RelatedContentLink,
)
from app.models.seed import SEED_GUIDES


from app.repositories.firestore import firestore_repository


@pytest.fixture(autouse=True)
def reset_in_memory_firestore(monkeypatch):
    """Provides an in-memory dictionary backing firestore_repository for guide tests."""
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
        prefix = f"{collection}/"
        return [v for k, v in mock_db.items() if k.startswith(prefix)]

    monkeypatch.setattr(firestore_repository, "create", mock_create)
    monkeypatch.setattr(firestore_repository, "get", mock_get)
    monkeypatch.setattr(firestore_repository, "update", mock_update)
    monkeypatch.setattr(firestore_repository, "delete", mock_delete)
    monkeypatch.setattr(firestore_repository, "list", mock_list)


@pytest.fixture
def client():
    return TestClient(app)



def test_16_01_guide_metadata_model():
    """Validates GuideMetadata model serialization and trust labels."""
    ref = SourceReference(
        title="Anvils in America",
        author="Richard Postman",
        publication="Postman Publishing",
        year=1998,
        trust_label=TrustLabel.FACT,
        citation_key="Postman1998",
    )
    safety = SafetyPrecaution(
        level="critical",
        hazard="Acoustic hearing loss",
        mitigation="Wear NRR 28+ protection",
        ppe=["Earmuffs", "Safety Glasses"],
    )
    rel = RelatedContentLink(
        content_id="mat-1084",
        title="1084 Steel",
        type=ContentType.MATERIAL,
        slug="1084",
        relationship="requires_material",
    )

    meta = GuideMetadata(
        reading_time_minutes=8,
        trust_label=TrustLabel.SOURCE_BACKED,
        author="Master Blacksmith",
        version="1.2",
        content_markdown="# Test Guide Content\n\nTesting guide.",
        source_references=[ref],
        safety_precautions=[safety],
        related_content=[rel],
    )

    assert meta.reading_time_minutes == 8
    assert meta.trust_label == TrustLabel.SOURCE_BACKED
    assert len(meta.source_references) == 1
    assert meta.source_references[0].citation_key == "Postman1998"
    assert len(meta.safety_precautions) == 1
    assert meta.safety_precautions[0].level == "critical"
    assert len(meta.related_content) == 1


def test_16_02_16_09_master_guide_seeded(client):
    """Verifies that the complete master guide is seeded and retrievable by slug and id."""
    # Retrieve by slug
    res = client.get("/api/v1/guides/anvil-anatomy-selection-mounting")
    assert res.status_code == 200
    data = res.json()
    assert data["type"] == "guide"
    assert "The Anvil: Anatomy" in data["title"]
    assert data["slug"] == "anvil-anatomy-selection-mounting"
    assert data["difficulty"] == "beginner"

    meta = data["metadata"]
    assert meta["trust_label"] == "source_backed_recommendation"
    assert meta["reading_time_minutes"] >= 10
    assert len(meta["content_markdown"]) > 2000
    assert "## 4. Empirical Testing: The Ball-Bearing Rebound Test" in meta["content_markdown"]

    # Source references check (16.04)
    assert len(meta["source_references"]) >= 3
    ref_titles = [r["title"] for r in meta["source_references"]]
    assert any("Anvils in America" in t for t in ref_titles)

    # Safety section check (16.05)
    assert len(meta["safety_precautions"]) >= 2
    hazards = [p["hazard"] for p in meta["safety_precautions"]]
    assert any("Acoustic" in h or "Trauma" in h for h in hazards)

    # Related content check (16.07)
    assert len(meta["related_content"]) >= 2
    rel_slugs = [r["slug"] for r in meta["related_content"]]
    assert "1084" in rel_slugs

    # Retrieve by direct ID
    res_by_id = client.get("/api/v1/guides/guide-anvil-selection-mounting")
    assert res_by_id.status_code == 200
    assert res_by_id.json()["id"] == "guide-anvil-selection-mounting"


def test_16_03_heat_treatment_guide_seeded(client):
    """Verifies secondary master guide on heat treatment fundamentals."""
    res = client.get("/api/v1/guides/fundamentals-of-heat-treatment-high-carbon-steel")
    assert res.status_code == 200
    data = res.json()
    assert data["metadata"]["trust_label"] == "fact"
    assert "Decalescence" in data["metadata"]["content_markdown"]


def test_16_08_guide_list_and_filters(client):
    """Tests list endpoint with category, difficulty, trust_label, and search filters."""
    # List all
    res = client.get("/api/v1/guides")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 2
    assert len(data["guides"]) >= 2

    # Filter by category
    res_tools = client.get("/api/v1/guides?category=tools")
    assert res_tools.status_code == 200
    for g in res_tools.json()["guides"]:
        assert g["category"] == "tools"

    # Filter by difficulty
    res_diff = client.get("/api/v1/guides?difficulty=intermediate")
    assert res_diff.status_code == 200
    for g in res_diff.json()["guides"]:
        assert g["difficulty"] == "intermediate"

    # Filter by trust_label
    res_trust = client.get("/api/v1/guides?trust_label=fact")
    assert res_trust.status_code == 200
    for g in res_trust.json()["guides"]:
        assert g["metadata"]["trust_label"] == "fact"

    # Search query matching markdown text
    res_q = client.get("/api/v1/guides?q=rebound")
    assert res_q.status_code == 200
    assert res_q.json()["total"] >= 1
    assert any("rebound" in g["slug"] or "rebound" in g["title"].lower() for g in res_q.json()["guides"])


def test_guide_not_found(client):
    """Verifies 404 response on nonexistent guide."""
    res = client.get("/api/v1/guides/nonexistent-master-guide-xyz")
    assert res.status_code == 404
    assert "not found" in res.json()["error"]["message"].lower()


def test_create_guide_success_and_validation(client):
    """Tests creating a valid master guide through the API."""
    payload = {
        "title": "Tongs Selection and Safe Stock Gripping",
        "slug": "tongs-selection-stock-gripping",
        "summary": "Mastering blacksmith tongs: wolf jaw, v-bit, bolt tongs, and safe heat holding protocols.",
        "category": "tools",
        "tags": ["tongs", "tools", "safety", "forging"],
        "difficulty": "beginner",
        "status": "published",
        "metadata": {
            "reading_time_minutes": 6,
            "trust_label": "craft_practice",
            "author": "Blacksmith Knight Guild",
            "version": "1.0",
            "content_markdown": "# Tongs Selection\n\nAlways size your tongs to the bar stock to avoid flying projectiles.",
            "safety_precautions": [
                {
                    "level": "warning",
                    "hazard": "Slipping hot bar stock",
                    "mitigation": "Quench tongs frequently to maintain mechanical grip",
                    "ppe": ["Safety Glasses", "Leather Apron"],
                }
            ],
            "source_references": [],
            "related_content": [],
        },
    }

    res = client.post("/api/v1/guides", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["id"] == "guide-tongs-selection-stock-gripping"
    assert data["title"] == payload["title"]

    # Duplicate creation should fail
    dup_res = client.post("/api/v1/guides", json=payload)
    assert dup_res.status_code == 400


def test_create_guide_rejected_on_safety_violation(client):
    """Tests that rule validator rejects a guide recommending heating galvanized steel without warnings."""
    hazardous_payload = {
        "title": "Forging Scrap Galvanized Pipe",
        "slug": "forging-galvanized-pipe-hazard",
        "summary": "Heat up cheap galvanized conduit pipe in your forge to make fast tools.",
        "category": "tools",
        "tags": ["galvanized", "zinc"],
        "difficulty": "beginner",
        "status": "published",
        "metadata": {
            "reading_time_minutes": 5,
            "trust_label": "opinion",
            "author": "Careless Maker",
            "version": "1.0",
            "content_markdown": "# Forging Galvanized Steel\n\nFound old galvanized pipe in the yard, throwing it directly into the hot forge fire to start hammering.",
            "safety_precautions": [],
            "source_references": [],
            "related_content": [],
        },
    }

    res = client.post("/api/v1/guides", json=hazardous_payload)
    assert res.status_code == 422
    assert "editorial validation standards" in res.json()["error"]["message"]


def test_update_guide(client):
    """Tests updating an existing guide via PATCH."""
    update_payload = {
        "summary": "Updated comprehensive summary for anvil selection and rebound testing guide.",
        "difficulty": "intermediate",
    }
    res = client.patch("/api/v1/guides/anvil-anatomy-selection-mounting", json=update_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["summary"] == update_payload["summary"]
    assert data["difficulty"] == "intermediate"

