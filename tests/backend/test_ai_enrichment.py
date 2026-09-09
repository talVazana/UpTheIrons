import sys
import asyncio
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

backend_dir = Path(__file__).resolve().parent.parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.main import app
from app.core.config import settings
from app.models.content import ContentEnvelope
from app.models.enums import ContentType, DifficultyLevel
from app.repositories.firestore import firestore_repository
from app.services.ai.base import BaseAIProvider, AIEnrichmentResult
from app.services.ai.mock import MockAIProvider
from app.services.ai.guardrails import GUARDRAIL_SYSTEM_PROMPT
from app.services.ai.service import AIService, ai_service

client = TestClient(app)


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

    # By default, use mock provider for offline deterministic test suite
    monkeypatch.setattr(settings, "AI_PROVIDER", "mock")


def test_14_01_ai_provider_interface():
    """14.01: Tests provider interface contract (classify, summarize, extract)."""
    async def _test():
        provider = MockAIProvider()
        title = "Forging a Camp Knife from 1084 High Carbon Steel"
        text = "Detailed guide on bevel grinding, distal taper, and oil quenching 1084 steel for beginners."

        result = await provider.enrich_content(title=title, text=text)
        assert result is not None
        assert isinstance(result, AIEnrichmentResult)
        assert result.category == "bladesmithing"
        assert result.difficulty == DifficultyLevel.BEGINNER
        assert any("1084" in m for m in result.materials_mentioned)
        assert "bevel grinding" in result.techniques

        # Test individual interface helpers
        category = await provider.classify(title, text)
        assert category == "bladesmithing"

        summary = await provider.summarize(title, text)
        assert summary is not None
        assert len(summary) > 10

        extracted = await provider.extract(title, text)
        assert "tags" in extracted
        assert "techniques" in extracted
        assert "materials" in extracted
        assert extracted["difficulty"] == "beginner"

    asyncio.run(_test())


def test_14_02_provider_configuration(monkeypatch):
    """14.02: Tests provider switching and configuration abstraction."""
    async def _test():
        # Test mock provider
        monkeypatch.setattr(settings, "AI_PROVIDER", "mock")
        svc = AIService()
        p_mock = await svc.get_provider()
        assert isinstance(p_mock, MockAIProvider)

        # Test disabled provider
        monkeypatch.setattr(settings, "AI_PROVIDER", "disabled")
        p_disabled = await svc.get_provider()
        assert p_disabled is None

    asyncio.run(_test())


def test_14_03_ai_disabled_mode(monkeypatch):
    """14.03: Ingestion & system continue cleanly when AI is disabled or key is absent."""
    async def _test():
        monkeypatch.setattr(settings, "AI_PROVIDER", "disabled")
        svc = AIService()

        envelope = ContentEnvelope(
            id="video:youtube:test_disabled",
            type=ContentType.VIDEO,
            title="Hammer Control Basics",
            slug="hammer-control-basics",
            summary="Basic hammer control and anvil posture.",
            category="forging",
        )

        # Envelope should be returned untouched with no exception
        enriched = await svc.enrich_envelope(envelope)
        assert enriched.id == envelope.id
        assert enriched.summary == "Basic hammer control and anvil posture."
        assert "ai_processed" not in enriched.metadata

    asyncio.run(_test())


def test_14_04_summary_enrichment():
    """14.04: Generates technical summary and preserves original in metadata."""
    async def _test():
        svc = AIService(override_provider=MockAIProvider())
        envelope = ContentEnvelope(
            id="article:forge:anvil-dressing",
            type=ContentType.ARTICLE,
            title="Dressing the Anvil Face and Horn",
            slug="dressing-anvil-face",
            summary="Short note on cleaning an old anvil.",
            category="tools",
        )

        enriched = await svc.enrich_envelope(envelope)
        assert enriched.metadata.get("ai_processed") is True
        assert enriched.metadata.get("original_summary") == "Short note on cleaning an old anvil."
        assert "anvil" in enriched.summary.lower() or "dressing" in enriched.summary.lower()

    asyncio.run(_test())


def test_14_05_14_06_14_07_classification_tags_difficulty():
    """14.05, 14.06, 14.07: Validates category classification, tag extraction, difficulty setting."""
    async def _test():
        svc = AIService(override_provider=MockAIProvider())
        envelope = ContentEnvelope(
            id="article:forge:heat-treat-basics",
            type=ContentType.ARTICLE,
            title="Quenching and Normalizing High Carbon Steel for Beginners",
            slug="heat-treat-basics",
            summary="Step-by-step beginner guide to heat treating 1084 and 5160 alloys in canola oil.",
            category="guides",
        )

        enriched = await svc.enrich_envelope(envelope)
        assert enriched.category == "heat-treatment"
        assert enriched.difficulty == DifficultyLevel.BEGINNER
        assert "heat-treatment" in enriched.tags
        assert "metallurgy" in enriched.tags
        assert any("1084" in m or "5160" in m for m in enriched.metadata.get("materials_mentioned", []))

    asyncio.run(_test())


def test_14_08_guardrails_prompt():
    """14.08: Verifies technical guardrails prompt enforces strict metallurgical integrity."""
    prompt = GUARDRAIL_SYSTEM_PROMPT.lower()
    assert "chemical composition" in prompt or "composition" in prompt
    assert "heat-treatment" in prompt or "temperature" in prompt
    assert "hardness" in prompt or "rockwell" in prompt
    assert "safety" in prompt
    assert "never hallucinate" in prompt or "never invent" in prompt


def test_14_09_ai_failure_resilience():
    """14.09: Force provider failure (exception/timeout); verify graceful degradation."""
    async def _test():
        class FailingProvider(BaseAIProvider):
            async def enrich_content(self, title: str, text: str, content_type: str = "video"):
                raise ConnectionError("Simulated remote LLM outage or timeout")

        svc = AIService(override_provider=FailingProvider())
        envelope = ContentEnvelope(
            id="video:youtube:resilience_test",
            type=ContentType.VIDEO,
            title="Making Tongs from Rebar",
            slug="making-tongs-from-rebar",
            summary="Beginner tongs project using cheap scrap rebar.",
            category="tools",
        )

        # Must NOT raise exception; returns envelope intact
        result = await svc.enrich_envelope(envelope)
        assert result.id == envelope.id
        assert result.summary == "Beginner tongs project using cheap scrap rebar."
        assert "ai_processed" not in result.metadata

    asyncio.run(_test())


def test_14_10_cost_boundary():
    """14.10: Cost boundary: batch enrichment processes only un-enriched items up to limit."""
    async def _test():
        # Pre-populate 3 items: 2 un-enriched, 1 already enriched
        await firestore_repository.create("content_vault", "item-1", {
            "id": "item-1",
            "type": "video",
            "title": "Blacksmithing Basics Ep 1",
            "slug": "blacksmithing-basics-1",
            "summary": "Introduction to forge safety and fire tending.",
            "category": "forging",
            "tags": ["basics"],
            "metadata": {"ai_processed": True},
        })
        await firestore_repository.create("content_vault", "item-2", {
            "id": "item-2",
            "type": "video",
            "title": "Blacksmithing Basics Ep 2",
            "slug": "blacksmithing-basics-2",
            "summary": "Drawing out tapers on the anvil face.",
            "category": "forging",
            "tags": ["basics"],
            "metadata": {"ai_processed": False},
        })
        await firestore_repository.create("content_vault", "item-3", {
            "id": "item-3",
            "type": "video",
            "title": "Blacksmithing Basics Ep 3",
            "slug": "blacksmithing-basics-3",
            "summary": "Punching holes hot at the anvil.",
            "category": "forging",
            "tags": ["basics"],
            "metadata": {},
        })

        svc = AIService(override_provider=MockAIProvider())
        # Limit batch to 1 item to test cost boundary limit
        batch_result = await svc.batch_enrich_pending(limit=1)

        assert batch_result["total_pending"] == 2
        assert batch_result["processed"] == 1
        assert batch_result["success"] == 1
        assert len(batch_result["enriched_items"]) == 1

    asyncio.run(_test())


def test_ai_status_endpoint():
    """Tests GET /api/v1/ai/status endpoint."""
    resp = client.get("/api/v1/ai/status")
    assert resp.status_code == 200
    data = resp.json()
    assert "provider" in data
    assert "model" in data
    assert "configured" in data
    assert "enabled" in data


def test_ai_preview_endpoint():
    """Tests POST /api/v1/ai/preview endpoint."""
    resp = client.post(
        "/api/v1/ai/preview",
        json={
            "title": "Forging a Hunting Knife",
            "text": "Using 1095 carbon steel, bevel grinding and quenching in Parks 50.",
            "content_type": "video",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["category"] == "bladesmithing"
    assert any("1095" in m for m in data["materials_mentioned"])


def test_ai_enrich_item_and_batch_endpoints():
    """Tests POST /api/v1/ai/enrich/{id} and POST /api/v1/ai/enrich-pending endpoints."""
    # Seed item
    async def _seed():
        await firestore_repository.create("content_vault", "video-seed-1", {
            "id": "video-seed-1",
            "type": "video",
            "title": "Heat Treating 1084 High Carbon Steel",
            "slug": "heat-treating-1084",
            "summary": "Detailed heat treat cycle for high carbon steel.",
            "category": "forging",
            "tags": ["forging"],
            "metadata": {},
        })
    asyncio.run(_seed())

    # Enrich single item
    resp = client.post("/api/v1/ai/enrich/video-seed-1")
    assert resp.status_code == 200
    item = resp.json()
    assert item["metadata"]["ai_processed"] is True
    assert item["category"] == "heat-treatment"

    # Batch enrich remaining (0 pending now)
    batch_resp = client.post("/api/v1/ai/enrich-pending?limit=5")
    assert batch_resp.status_code == 200
    batch_data = batch_resp.json()
    assert batch_data["total_pending"] == 0


def test_gemini_provider_unconfigured():
    """Verifies GeminiProvider returns None gracefully when no API key is set."""
    from app.services.ai.gemini import GeminiProvider

    async def _test():
        provider = GeminiProvider(api_key="")
        res = await provider.enrich_content("Title", "Body")
        assert res is None

    asyncio.run(_test())


def test_gemini_provider_mocked_http(monkeypatch):
    """Verifies GeminiProvider payload handling, JSON markdown unwrapping, and error resilience."""
    import httpx
    from app.services.ai.gemini import GeminiProvider

    class MockResponse:
        def __init__(self, status_code: int, json_data: dict, text: str = ""):
            self.status_code = status_code
            self._json = json_data
            self.text = text

        def json(self):
            return self._json

    # Test 1: Successful response with markdown wrapping
    async def mock_post_success(*args, **kwargs):
        return MockResponse(
            200,
            {
                "candidates": [
                    {
                        "content": {
                            "parts": [
                                {
                                    "text": "```json\n{\"summary\": \"Forging a camp axe from 4140.\", \"category\": \"forging\", \"difficulty\": \"intermediate\", \"tags\": [\"axe\", \"forging\"], \"techniques\": [\"drifting\"], \"materials_mentioned\": [\"4140 steel\"]}\n```"
                                }
                            ]
                        }
                    }
                ]
            },
        )

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post_success)

    async def _test_success():
        provider = GeminiProvider(api_key="test-api-key")
        res = await provider.enrich_content("Camp Axe", "Drifting eye on 4140 steel.")
        assert res is not None
        assert res.category == "forging"
        assert res.difficulty == DifficultyLevel.INTERMEDIATE
        assert "drifting" in res.techniques
        assert "4140 steel" in res.materials_mentioned

    asyncio.run(_test_success())

    # Test 2: HTTP 500 error resilience
    async def mock_post_500(*args, **kwargs):
        return MockResponse(500, {}, text="Internal Server Error")

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post_500)

    async def _test_500():
        provider = GeminiProvider(api_key="test-api-key")
        res = await provider.enrich_content("Camp Axe", "Body")
        assert res is None

    asyncio.run(_test_500())
