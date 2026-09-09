import logging
from typing import Any, Dict, List, Optional

from app.core.config import settings
from app.models.content import ContentEnvelope, utc_now
from app.models.enums import ContentType
from app.repositories.firestore import firestore_repository
from app.services.ai.base import BaseAIProvider, AIEnrichmentResult
from app.services.ai.gemini import GeminiProvider
from app.services.ai.mock import MockAIProvider

logger = logging.getLogger("blacksmith_knight.ai.service")

CONTENT_VAULT_COLLECTION = "content_vault"


class AIService:
    """
    Orchestration layer for optional AI content enrichment.
    Enforces local-first, deterministic-first philosophy:
    system functions normally even if AI provider is disabled, unconfigured, or failing.
    """

    def __init__(self, override_provider: Optional[BaseAIProvider] = None):
        self._override_provider = override_provider

    async def get_provider(self) -> Optional[BaseAIProvider]:
        if self._override_provider:
            return self._override_provider

        provider_name = settings.AI_PROVIDER.lower().strip()
        if provider_name == "disabled":
            return None

        if provider_name == "mock":
            return MockAIProvider()

        # Dynamic key resolution (Firestore -> env)
        from app.api.v1.settings import get_effective_ai_api_key
        api_key = await get_effective_ai_api_key()

        if not api_key:
            logger.info("AI provider is %s but no API key configured. Operating in disabled mode.", provider_name)
            return None

        if provider_name == "gemini":
            return GeminiProvider(api_key=api_key, model=settings.AI_MODEL)

        # Fallback to mock if provider is unknown
        logger.warning("Unknown AI provider '%s'. Defaulting to mock.", provider_name)
        return MockAIProvider()

    async def get_status(self) -> Dict[str, Any]:
        from app.api.v1.settings import get_effective_ai_api_key
        api_key = await get_effective_ai_api_key()
        provider_name = settings.AI_PROVIDER.lower().strip()

        configured = bool(api_key) if provider_name != "mock" else True
        enabled = provider_name != "disabled" and configured

        return {
            "provider": provider_name,
            "model": settings.AI_MODEL,
            "configured": configured,
            "enabled": enabled,
        }

    async def enrich_envelope(self, envelope: ContentEnvelope) -> ContentEnvelope:
        """
        Enriches a ContentEnvelope with structured AI metadata.
        If AI is unavailable or fails, returns original envelope unmodified (resilience).
        """
        provider = await self.get_provider()
        if not provider:
            return envelope

        # Build context from existing envelope fields
        context_parts = [envelope.title, envelope.summary]
        if envelope.tags:
            context_parts.append(f"Tags: {', '.join(envelope.tags)}")
        
        # Include product/video specific context if available
        if envelope.metadata:
            for k in ["pros", "cons", "techniques", "channel_name"]:
                if k in envelope.metadata and envelope.metadata[k]:
                    val = envelope.metadata[k]
                    context_parts.append(f"{k}: {val}")

        full_text = "\n".join(context_parts)

        try:
            result = await provider.enrich_content(
                title=envelope.title,
                text=full_text,
                content_type=envelope.type.value if hasattr(envelope.type, "value") else str(envelope.type),
            )
        except Exception as exc:
            logger.error("AI enrichment call failed on envelope %s: %s", envelope.id, exc)
            return envelope

        if not result:
            return envelope

        # Preserve original summary before overriding
        if "original_summary" not in envelope.metadata and result.summary:
            envelope.metadata["original_summary"] = envelope.summary

        if result.summary:
            envelope.summary = result.summary

        if result.category:
            envelope.category = result.category

        if result.difficulty and not envelope.difficulty:
            envelope.difficulty = result.difficulty

        # Merge extracted tags with existing tags
        combined_tags = list(dict.fromkeys(envelope.tags + result.tags))
        envelope.tags = combined_tags

        # Persist structured enrichment metadata
        envelope.metadata["ai_processed"] = True
        envelope.metadata["ai_enriched_at"] = utc_now().isoformat()
        envelope.metadata["ai_provider"] = result.ai_provider
        envelope.metadata["ai_model"] = result.ai_model
        envelope.metadata["techniques"] = result.techniques
        envelope.metadata["materials_mentioned"] = result.materials_mentioned
        envelope.updated_at = utc_now()

        return envelope

    async def enrich_and_save_by_id(self, content_id: str) -> Optional[ContentEnvelope]:
        """Loads envelope from database, enriches it, and saves it back."""
        data = await firestore_repository.get(CONTENT_VAULT_COLLECTION, content_id)
        if not data:
            return None

        envelope = ContentEnvelope.model_validate(data)
        enriched = await self.enrich_envelope(envelope)
        await firestore_repository.create(CONTENT_VAULT_COLLECTION, content_id, enriched.model_dump(mode="json"))
        return enriched

    async def batch_enrich_pending(
        self,
        limit: int = 10,
        content_type: Optional[ContentType] = None,
    ) -> Dict[str, Any]:
        """
        Batch enrich un-enriched content.
        Enforces Cost Boundary (14.10): Only processes items where ai_processed != True,
        capped strictly by limit.
        """
        docs = await firestore_repository.list(CONTENT_VAULT_COLLECTION, limit=100)

        # Filter in-memory for matching type if provided
        if content_type:
            target_type = content_type.value if hasattr(content_type, "value") else str(content_type)
            docs = [d for d in docs if d.get("type") == target_type]

        # Filter in-memory for un-enriched items
        pending_docs = [
            d for d in docs
            if not d.get("metadata", {}).get("ai_processed")
        ]

        batch = pending_docs[:limit]
        processed_count = 0
        success_count = 0
        failed_count = 0
        enriched_items: List[Dict[str, Any]] = []

        for doc in batch:
            doc_id = doc.get("id")
            if not doc_id:
                continue
            processed_count += 1
            try:
                envelope = ContentEnvelope.model_validate(doc)
                enriched = await self.enrich_envelope(envelope)
                await firestore_repository.create(
                    CONTENT_VAULT_COLLECTION,
                    doc_id,
                    enriched.model_dump(mode="json"),
                )
                if enriched.metadata.get("ai_processed"):
                    success_count += 1
                    enriched_items.append({
                        "id": doc_id,
                        "title": enriched.title,
                        "category": enriched.category,
                        "difficulty": enriched.difficulty.value if enriched.difficulty else None,
                        "tags": enriched.tags,
                    })
                else:
                    failed_count += 1
            except Exception as exc:
                failed_count += 1
                logger.error("Batch enrichment failed for doc %s: %s", doc_id, exc)

        return {
            "total_pending": len(pending_docs),
            "processed": processed_count,
            "success": success_count,
            "failed": failed_count,
            "enriched_items": enriched_items,
        }


ai_service = AIService()
