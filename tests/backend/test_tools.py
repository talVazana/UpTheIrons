import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

backend_dir = Path(__file__).resolve().parent.parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.main import app
from app.models.content import ContentEnvelope, ToolMetadata, SafetyPrecaution, RelatedContentLink
from app.models.enums import ContentType, ToolCategory, DifficultyLevel, ContentStatus
from app.models.seed import SEED_TOOLS
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


def test_18_01_18_02_tool_metadata_model():
    """Verify ToolMetadata domain model and ToolCategory enum constraints."""
    tool_meta = ToolMetadata(
        tool_category=ToolCategory.FORGING,
        primary_purpose="Hardened striking surface for plastic deformation of hot iron.",
        essential_for=["Drawing out", "Upsetting"],
        selection_criteria=["High rebound percentage", "Solid cast steel body"],
        beginner_guidance="Start with a 100-150 lb anvil for personal workshop scale.",
        beginner_friendly=True,
        diy_buildable=False,
        diy_alternatives=["Railroad track post"],
        maintenance_protocols=["Radius sharp working edges to 1/8-inch"],
        safety_precautions=[
            SafetyPrecaution(
                level="critical",
                hazard="Spalling steel shards from direct hammer strikes.",
                mitigation="Never strike hardened hammer on bare hardened face.",
                ppe=["ANSI Z87.1 Safety Glasses"],
            )
        ],
        specifications={"weight_lbs": "120", "face_hardness": "56 HRC"},
    )

    envelope = ContentEnvelope(
        id="tool-test-anvil",
        type=ContentType.TOOL,
        title="Test Forging Anvil",
        slug="test-forging-anvil",
        summary="A test anvil entry for validation.",
        category="workshop",
        metadata=tool_meta.model_dump(),
    )

    assert envelope.type == ContentType.TOOL
    assert envelope.metadata["tool_category"] == "forging"
    assert envelope.metadata["beginner_friendly"] is True
    assert len(envelope.metadata["safety_precautions"]) == 1


def test_18_04_seeded_anvil_entry(client):
    """18.04: Verify retrieval and technical attributes of the London-pattern anvil entry."""
    response = client.get("/api/v1/tools/london-pattern-anvil")
    assert response.status_code == 200
    data = response.json()

    assert data["slug"] == "london-pattern-anvil"
    assert data["type"] == "tool"
    assert "London-Pattern" in data["title"]

    meta = data["metadata"]
    assert meta["tool_category"] == "forging"
    assert meta["beginner_friendly"] is True
    assert meta["diy_buildable"] is False
    assert len(meta["selection_criteria"]) >= 3
    assert len(meta["diy_alternatives"]) >= 2
    assert "rebound" in " ".join(meta["selection_criteria"]).lower()


def test_18_05_seeded_hammer_entry(client):
    """18.05: Verify retrieval and attributes of the Swedish cross-peen hammer entry."""
    response = client.get("/api/v1/tools/cross-peen-hammer")
    assert response.status_code == 200
    data = response.json()

    assert data["slug"] == "cross-peen-hammer"
    assert "Cross-Peen" in data["title"]

    meta = data["metadata"]
    assert meta["tool_category"] == "forging"
    assert meta["diy_buildable"] is True
    assert meta["beginner_friendly"] is True
    assert "hickory" in " ".join(meta["selection_criteria"]).lower()
    assert "crown" in " ".join(meta["maintenance_protocols"]).lower()


def test_18_06_seeded_grinder_entry(client):
    """18.06: Verify retrieval and attributes of the 2x72 industrial belt grinder entry."""
    response = client.get("/api/v1/tools/2x72-belt-grinder")
    assert response.status_code == 200
    data = response.json()

    assert data["slug"] == "2x72-belt-grinder"
    assert "2x72" in data["title"]

    meta = data["metadata"]
    assert meta["tool_category"] == "grinding"
    assert meta["beginner_friendly"] is False
    assert "vfd" in " ".join(meta["selection_criteria"]).lower()

    specs = meta["specifications"]
    assert "2 inches wide × 72 inches long" in specs.get("belt_size", "")


def test_18_07_tool_safety_metadata(client):
    """18.07: Verify rigorous safety metadata across all seeded workshop tools."""
    for tool in SEED_TOOLS:
        response = client.get(f"/api/v1/tools/{tool.slug}")
        assert response.status_code == 200
        meta = response.json()["metadata"]

        safety = meta.get("safety_precautions", [])
        assert len(safety) >= 1, f"Tool {tool.slug} must have explicit safety precautions"

        for p in safety:
            assert len(p["hazard"]) >= 5
            assert len(p["mitigation"]) >= 5
            assert len(p["ppe"]) >= 1, f"Safety warning in {tool.slug} must specify PPE checklist"


def test_18_08_related_tools(client):
    """18.08: Verify bidirectional or relevant cross-tool links."""
    response = client.get("/api/v1/tools/london-pattern-anvil")
    assert response.status_code == 200
    meta = response.json()["metadata"]

    related = meta.get("related_tools", [])
    assert len(related) >= 1
    related_slugs = [r["slug"] for r in related]
    assert "cross-peen-hammer" in related_slugs


def test_list_tools_and_filters(client):
    """Verify tool category, beginner friendliness, and DIY buildable filtering."""
    # List all tools
    all_res = client.get("/api/v1/tools")
    assert all_res.status_code == 200
    all_tools = all_res.json()
    assert all_tools["total"] >= 5

    # Filter by category: grinding
    grind_res = client.get("/api/v1/tools?category=grinding")
    assert grind_res.status_code == 200
    grind_tools = grind_res.json()["tools"]
    assert len(grind_tools) >= 1
    assert all(t["metadata"]["tool_category"] == "grinding" for t in grind_tools)

    # Filter by beginner-friendly only
    beg_res = client.get("/api/v1/tools?beginner_friendly=true")
    assert beg_res.status_code == 200
    beg_tools = beg_res.json()["tools"]
    assert len(beg_tools) >= 1
    assert all(t["metadata"]["beginner_friendly"] is True for t in beg_tools)

    # Filter by DIY buildable
    diy_res = client.get("/api/v1/tools?diy_buildable=true")
    assert diy_res.status_code == 200
    diy_tools = diy_res.json()["tools"]
    assert len(diy_tools) >= 1
    assert all(t["metadata"]["diy_buildable"] is True for t in diy_tools)


def test_tool_free_text_search(client):
    """Verify free-text search query across title, purpose, guidance, and tags."""
    res = client.get("/api/v1/tools?q=rebound")
    assert res.status_code == 200
    tools = res.json()["tools"]
    assert len(tools) >= 1
    assert any("anvil" in t["slug"] for t in tools)

    res_empty = client.get("/api/v1/tools?q=nonexistentcrypticterm123")
    assert res_empty.status_code == 200
    assert res_empty.json()["total"] == 0


def test_tool_not_found(client):
    """Verify 404 on non-existent tool identifier."""
    res = client.get("/api/v1/tools/non-existent-power-hammer")
    assert res.status_code == 404
    assert res.json()["error"]["code"] == "NOT_FOUND"


def test_create_tool_and_duplicate_prevention(client):
    """Verify creation of custom verified tool and duplicate rejection."""
    payload = {
        "title": "Spring Swage Tool",
        "slug": "spring-swage-tool",
        "summary": "Handy bottom/top combined tooling for forging round tenons and uniform cylindrical necks.",
        "category": "workshop",
        "tags": ["swage", "hardy-tool", "spring-swage"],
        "difficulty": "intermediate",
        "metadata": {
            "tool_category": "forging",
            "primary_purpose": "Forges round cross-sections quickly between matched radiused dies.",
            "essential_for": ["Forming round tenons"],
            "selection_criteria": ["4140 spring steel strap", "Smooth polished inner die radii"],
            "beginner_guidance": "Position in hardy hole or leg vise with stock at yellow heat.",
            "beginner_friendly": True,
            "diy_buildable": True,
            "diy_alternatives": ["Single bottom swage block with hand top swage"],
            "maintenance_protocols": ["Clean scale out of bottom cavity between passes"],
            "safety_precautions": [
                {
                    "level": "warning",
                    "hazard": "Hot scale blowout between dies during heavy hammer blow.",
                    "mitigation": "Angle the workpiece slightly downwards away from body.",
                    "ppe": ["Safety glasses"],
                }
            ],
            "specifications": {"die_diameter": "0.5 inch"},
        },
    }

    create_res = client.post("/api/v1/tools", json=payload)
    assert create_res.status_code == 201
    created = create_res.json()
    assert created["slug"] == "spring-swage-tool"
    assert created["id"] == "tool-spring-swage-tool"

    # Duplicate creation attempt
    dup_res = client.post("/api/v1/tools", json=payload)
    assert dup_res.status_code == 400
    assert dup_res.json()["error"]["code"] == "BAD_REQUEST"
