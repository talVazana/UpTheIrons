import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

backend_dir = Path(__file__).resolve().parent.parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.main import app
from app.models.enums import ContentType, DifficultyLevel
from app.models.content import MaterialMetadata, HeatTreatmentRecipe
from app.models.seed import SEED_MATERIALS
from app.repositories.firestore import firestore_repository


@pytest.fixture(autouse=True)
def reset_in_memory_firestore(monkeypatch):
    """Provides an in-memory dictionary backing firestore_repository for material tests."""
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


def test_17_01_17_02_material_and_steel_model():
    """Validates MaterialMetadata model with alloying elements, category, and heat treatment."""
    ht = HeatTreatmentRecipe(
        normalizing_temp_f=1600,
        annealing_temp_f=1450,
        hardening_temp_f=1500,
        decalescence_temp_f=1425,
        quench_medium="Warmed canola oil or Parks 50",
        tempering_range_f="400°F - 450°F",
        target_hardness_hrc="58 - 61 HRC",
    )
    meta = MaterialMetadata(
        classification="High Carbon Steel (AISI 1084)",
        carbon_pct=0.84,
        alloying_elements={"manganese": 0.75, "silicon": 0.20},
        steel_category="carbon_steel",
        forging_temp_range_f="1650°F - 2100°F",
        heat_treatment=ht,
        spark_testing_profile="Dense burst of bright yellow starbursts.",
        grinding_characteristics="Smooth grinding, low burr.",
        confidence_score=0.99,
        confidence_level="handbook_verified",
        beginner_suitability=True,
        source_reference="ASM Handbook Vol 1",
    )

    assert meta.carbon_pct == 0.84
    assert meta.alloying_elements["manganese"] == 0.75
    assert meta.confidence_level == "handbook_verified"
    assert meta.beginner_suitability is True
    assert meta.heat_treatment.hardening_temp_f == 1500


def test_17_04_17_05_seeded_steels_retrieval(client):
    """Verifies that all 5 essential steels (1084, 1095, 5160, O1, W1) are seeded and retrievable."""
    for slug in ["1084", "1095", "5160", "o1", "w1"]:
        res = client.get(f"/api/v1/materials/{slug}")
        assert res.status_code == 200, f"Steel {slug} should return 200"
        data = res.json()
        assert data["slug"] == slug
        assert data["type"] == "material"
        assert "carbon_pct" in data["metadata"]
        assert data["metadata"]["confidence_score"] >= 0.90
        assert data["metadata"]["source_reference"] is not None


def test_17_06_17_07_composition_and_heat_treatment_display(client):
    """Verifies detailed chemical elements and thermal recipe values for 1084 and O1."""
    # 1084
    res_1084 = client.get("/api/v1/materials/1084")
    assert res_1084.status_code == 200
    meta_1084 = res_1084.json()["metadata"]
    assert meta_1084["carbon_pct"] == 0.84
    assert meta_1084["heat_treatment"]["hardening_temp_f"] == 1500
    assert len(meta_1084["heat_treatment"]["tempering_table"]) >= 3

    # O1 Tool Steel
    res_o1 = client.get("/api/v1/materials/o1")
    assert res_o1.status_code == 200
    meta_o1 = res_o1.json()["metadata"]
    assert meta_o1["carbon_pct"] == 0.90
    assert meta_o1["alloying_elements"]["tungsten"] == 0.50
    assert meta_o1["alloying_elements"]["vanadium"] == 0.20
    assert meta_o1["heat_treatment"]["soak_time_minutes"] == 10


def test_17_09_material_search_and_filtering(client):
    """Verifies search, category filtering, beginner friendliness, and carbon range queries."""
    # List all
    res_all = client.get("/api/v1/materials")
    assert res_all.status_code == 200
    assert res_all.json()["total"] >= 5

    # Filter by steel_category
    res_spring = client.get("/api/v1/materials?steel_category=spring_steel")
    assert res_spring.status_code == 200
    for m in res_spring.json()["materials"]:
        assert m["metadata"]["steel_category"] == "spring_steel"

    # Filter by beginner friendly
    res_beg = client.get("/api/v1/materials?beginner_friendly=true")
    assert res_beg.status_code == 200
    for m in res_beg.json()["materials"]:
        assert m["metadata"]["beginner_suitability"] is True

    # Filter by carbon percentage range
    res_carbon = client.get("/api/v1/materials?min_carbon=0.90&max_carbon=1.05")
    assert res_carbon.status_code == 200
    for m in res_carbon.json()["materials"]:
        c = m["metadata"]["carbon_pct"]
        assert 0.90 <= c <= 1.05

    # Free text search for "hamon"
    res_q = client.get("/api/v1/materials?q=hamon")
    assert res_q.status_code == 200
    slugs = [m["slug"] for m in res_q.json()["materials"]]
    assert "1095" in slugs or "w1" in slugs


def test_17_10_material_comparison_foundation(client):
    """Verifies deterministic comparison matrix across 3 steels (1084, 1095, 5160)."""
    res = client.get("/api/v1/materials/compare?ids=1084,1095,5160")
    assert res.status_code == 200
    data = res.json()

    # Verify compared items
    assert len(data["items"]) == 3
    slugs = [i["slug"] for i in data["items"]]
    assert "1084" in slugs
    assert "1095" in slugs
    assert "5160" in slugs

    # Verify element keys
    assert "carbon" in data["compared_elements"]
    assert "chromium" in data["compared_elements"]

    # Verify deterministic rankings
    # Edge retention: 1095 (0.95% C) > 1084 (0.84% C) > 5160 (0.60% C)
    assert data["edge_retention_rank"][0] == "1095 High Carbon Steel"
    assert data["edge_retention_rank"][-1] == "5160 Spring Steel"

    # Toughness ranking: 5160 > 1084 > 1095
    assert data["toughness_rank"][0] == "5160 Spring Steel"
    assert data["toughness_rank"][-1] == "1095 High Carbon Steel"

    # Quench speed summary
    assert "1095 High Carbon Steel" in data["quench_speed_summary"]


def test_material_comparison_validation(client):
    """Verifies boundary errors on comparison (too few or too many)."""
    # Too few
    res_one = client.get("/api/v1/materials/compare?ids=1084")
    assert res_one.status_code == 400

    # Too many
    res_many = client.get("/api/v1/materials/compare?ids=1084,1095,5160,o1,w1")
    assert res_many.status_code == 400


def test_create_material_and_validation(client):
    """Tests creating a new material and enforcing mandatory source citation."""
    valid_payload = {
        "title": "A2 Tool Steel",
        "slug": "a2",
        "summary": "Air-hardening tool steel (~1.00% C, 5.0% Cr, 1.0% Mo). Extreme wear resistance and toughness.",
        "category": "materials",
        "tags": ["steel", "tool-steel", "air-hardening"],
        "difficulty": "advanced",
        "status": "published",
        "metadata": {
            "classification": "Air-Hardening Tool Steel (AISI A2)",
            "carbon_pct": 1.00,
            "alloying_elements": {"chromium": 5.25, "molybdenum": 1.10, "vanadium": 0.25},
            "steel_category": "tool_steel",
            "beginner_suitability": False,
            "source_reference": "ASTM A681 Standard Specification for Tool Steels",
        },
    }
    res = client.post("/api/v1/materials", json=valid_payload)
    assert res.status_code == 201
    assert res.json()["slug"] == "a2"

    # Missing source reference should fail metallurgical validation
    invalid_payload = {
        "title": "Unknown Junk Steel",
        "slug": "unknown-junk",
        "summary": "Mystery steel found in a junkyard.",
        "category": "materials",
        "metadata": {
            "classification": "Mystery",
            "carbon_pct": 0.50,
            "source_reference": "",
        },
    }
    res_invalid = client.post("/api/v1/materials", json=invalid_payload)
    assert res_invalid.status_code in [400, 422]
