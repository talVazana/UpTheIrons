import sys
import asyncio
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

backend_dir = Path(__file__).resolve().parent.parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.main import app
from app.models.content import ContentEnvelope
from app.models.enums import ContentType, ContentStatus
from app.repositories.firestore import firestore_repository
from app.services.rules_service import rules_service, EditorialOverrideRequest
from app.services.rule_validator import rule_validator

client = TestClient(app)

EXPECTED_RULE_FILES = [
    "mission",
    "rules",
    "content_rules",
    "safety_rules",
    "source_rules",
    "product_rules",
    "metallurgy_rules",
    "editorial_style",
]


@pytest.fixture(autouse=True)
def reset_in_memory_firestore(monkeypatch):
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
        return [v for k, v in mock_db.items() if k.startswith(prefix)][:limit]

    monkeypatch.setattr(firestore_repository, "create", mock_create)
    monkeypatch.setattr(firestore_repository, "get", mock_get)
    monkeypatch.setattr(firestore_repository, "update", mock_update)
    monkeypatch.setattr(firestore_repository, "delete", mock_delete)
    monkeypatch.setattr(firestore_repository, "list", mock_list)


def test_15_01_15_02_rules_directory_and_master_files():
    """15.01, 15.02: Verifies all 8 modular rule files exist on disk in config/."""
    config_dir = Path(__file__).resolve().parent.parent.parent / "config"
    assert config_dir.exists(), "config directory must exist"

    for rule_stem in EXPECTED_RULE_FILES:
        target_path = config_dir / f"{rule_stem}.md"
        assert target_path.exists(), f"Expected rule file {target_path.name} to exist"
        content = target_path.read_text(encoding="utf-8")
        assert len(content) > 100, f"Rule file {target_path.name} must not be empty"


def test_15_03_content_inclusion_rules():
    """15.03: Verifies content rules encompass craft topics, audience, and rejection criteria."""
    doc = rules_service.get_rule("content_rules")
    assert doc is not None
    assert "Priority Craft Topics" in [s.title for s in doc.sections]
    assert "Mandatory Rejections" in [s.title for s in doc.sections]


def test_15_04_source_quality_rules():
    """15.04: Verifies source quality rules mandate attribution and anti-crawling."""
    doc = rules_service.get_rule("source_rules")
    assert doc is not None
    assert any("controlled" in s.title.lower() for s in doc.sections)
    assert any("standards" in s.title.lower() for s in doc.sections)


def test_15_05_safety_rules():
    """15.05: Verifies safety rules mandate PPE and workshop hazard awareness."""
    doc = rules_service.get_rule("safety_rules")
    assert doc is not None
    assert any("ppe" in s.title.lower() for s in doc.sections)
    assert any("hazards" in s.title.lower() for s in doc.sections)
    content_lower = doc.content.lower()
    assert "zinc" in content_lower
    assert "fiber" in content_lower or "kaowool" in content_lower
    assert "quench" in content_lower


def test_15_06_product_rules():
    """15.06: Verifies product rules mandate commercial neutrality and honest assessment."""
    doc = rules_service.get_rule("product_rules")
    assert doc is not None
    content_lower = doc.content.lower()
    assert "zero ranking distortion" in content_lower or "neutrality" in content_lower
    assert "pros" in content_lower and "cons" in content_lower
    assert "alternatives" in content_lower


def test_15_07_editorial_style_rules():
    """15.07: Verifies editorial style mandates anti-hype, craft-first voice."""
    doc = rules_service.get_rule("editorial_style")
    assert doc is not None
    content_lower = doc.content.lower()
    assert "terse" in content_lower
    assert "anti-hype" in content_lower


def test_15_08_rule_loading_service():
    """15.08: Verifies dynamic loading, section parsing, and caching in rules_service."""
    rules = rules_service.list_rules()
    assert len(rules) >= 8

    mission = rules_service.get_rule("mission")
    assert mission is not None
    assert "Blacksmith Knight" in mission.title and "Mission" in mission.title
    assert len(mission.sections) >= 2


def test_15_09_rule_validation_positive_and_negative():
    """15.09: Tests positive and negative validation cases."""
    # Positive case: valid blacksmithing guide
    pos_res = rule_validator.validate_content(
        title="Forging an S-Hook from 3/8 Inch Mild Steel",
        text="Beginner taper forging, scroll forming on anvil horn, and quenching in water.",
        tags=["blacksmithing", "forging", "tools"],
    )
    assert pos_res.valid is True
    assert pos_res.suggested_status == ContentStatus.PUBLISHED
    assert pos_res.relevance_score >= 0.5
    assert len(pos_res.issues) == 0

    # Negative case: commercial spam
    spam_res = rule_validator.validate_content(
        title="Best Forge 2026",
        text="Check out our limited time offer! Use promo code FORGE50 to order today and get 50% off!",
    )
    assert spam_res.valid is False
    assert spam_res.suggested_status == ContentStatus.NEEDS_REVIEW
    assert any(i.rule_category == "commercial_policy" for i in spam_res.issues)

    # Negative case: dangerous galvanized heating without warning
    galv_res = rule_validator.validate_content(
        title="Forging a Fire Poker",
        text="Found an old galvanized pipe in the yard, tossing it straight into the forge fire.",
    )
    assert galv_res.valid is False
    assert any("zinc" in i.message.lower() or "galvaniz" in i.message.lower() for i in galv_res.issues)

    # Positive case: galvanized heating WITH safety warnings
    safe_galv_res = rule_validator.validate_content(
        title="Safely Forging Reclaimed Galvanized Steel",
        text="MANDATORY: Soak in muriatic acid to strip all zinc coating to prevent toxic zinc fume fever before heating.",
        tags=["safety", "forging", "anvil"],
    )
    assert not any("zinc" in i.message.lower() for i in safe_galv_res.issues)


def test_15_10_editorial_override():
    """15.10: Verifies applying editorial overrides (pinned, featured, verified, hidden)."""
    async def _test():
        # Seed content
        await firestore_repository.create("content_vault", "item-override-1", {
            "id": "item-override-1",
            "type": "guide",
            "title": "Mastering the Distal Taper",
            "slug": "mastering-distal-taper",
            "summary": "Advanced bladesmithing technique.",
            "category": "bladesmithing",
            "status": "published",
            "metadata": {},
        })

        # Apply PINNED override
        override = EditorialOverrideRequest(
            is_pinned=True,
            is_verified=True,
            editorial_notes="Selected as apprentice cornerstone guide.",
        )
        updated = await rules_service.apply_editorial_override("item-override-1", override)
        assert updated is not None
        assert updated.metadata.get("is_pinned") is True
        assert updated.metadata.get("is_verified") is True
        assert updated.status == ContentStatus.PINNED or updated.status == ContentStatus.VERIFIED
        assert updated.metadata.get("editorial_notes") == "Selected as apprentice cornerstone guide."

    asyncio.run(_test())


def test_rules_api_endpoints():
    """Tests GET /api/v1/rules, GET /api/v1/rules/{id}, POST /reload, POST /validate."""
    # List rules
    list_resp = client.get("/api/v1/rules")
    assert list_resp.status_code == 200
    rule_list = list_resp.json()
    assert len(rule_list) >= 8

    # Detail rule
    detail_resp = client.get("/api/v1/rules/safety_rules")
    assert detail_resp.status_code == 200
    doc = detail_resp.json()
    assert doc["id"] == "safety_rules"
    assert len(doc["sections"]) > 0

    # Reload rules
    reload_resp = client.post("/api/v1/rules/reload")
    assert reload_resp.status_code == 200

    # Validate endpoint
    val_resp = client.post(
        "/api/v1/rules/validate",
        json={
            "title": "Quenching 1084 High Carbon Steel",
            "text": "Detailed normalizing, heating to 1500F, and quenching in warm canola oil.",
            "tags": ["heat-treatment", "steel"],
        },
    )
    assert val_resp.status_code == 200
    val_data = val_resp.json()
    assert val_data["valid"] is True
    assert val_data["relevance_score"] >= 0.3


def test_editorial_override_endpoint():
    """Tests POST /api/v1/rules/override/{id} endpoint."""
    async def _seed():
        await firestore_repository.create("content_vault", "article-override-test", {
            "id": "article-override-test",
            "type": "article",
            "title": "Hammer Dressing Guide",
            "slug": "hammer-dressing-guide",
            "summary": "Crown and chamfer edges.",
            "category": "tools",
            "status": "published",
            "metadata": {},
        })
    asyncio.run(_seed())

    resp = client.post(
        "/api/v1/rules/override/article-override-test",
        json={
            "status": "featured",
            "is_featured": True,
            "editorial_notes": "Essential beginner tooling guide.",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "featured"
    assert data["metadata"]["is_featured"] is True
    assert data["metadata"]["editorial_notes"] == "Essential beginner tooling guide."
