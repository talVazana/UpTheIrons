import json
import logging
import re
from typing import Optional
import httpx

from app.models.enums import DifficultyLevel
from app.services.ai.base import BaseAIProvider, AIEnrichmentResult
from app.services.ai.guardrails import GUARDRAIL_SYSTEM_PROMPT

logger = logging.getLogger("blacksmith_knight.ai.gemini")

GEMINI_API_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"


class GeminiProvider(BaseAIProvider):
    """
    Google Gemini AI enrichment provider.
    Connects to the official Gemini REST API with structured output and strict metallurgical guardrails.
    """

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash", timeout: float = 15.0):
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    async def enrich_content(
        self,
        title: str,
        text: str,
        content_type: str = "video",
    ) -> Optional[AIEnrichmentResult]:
        if not self.api_key:
            logger.warning("Gemini AI API key not configured. Enrichment skipped.")
            return None

        url = GEMINI_API_URL_TEMPLATE.format(model=self.model, key=self.api_key)

        prompt_content = (
            f"Analyze and enrich this blacksmithing content:\n"
            f"Title: {title}\n"
            f"Content Type: {content_type}\n"
            f"Content Body/Transcript:\n{text[:4000]}"
        )

        payload = {
            "systemInstruction": {
                "parts": [{"text": GUARDRAIL_SYSTEM_PROMPT.strip()}]
            },
            "contents": [
                {
                    "parts": [{"text": prompt_content}]
                }
            ],
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.2,
                "maxOutputTokens": 1024,
            },
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)

            if response.status_code != 200:
                logger.error(
                    "Gemini API returned status %d: %s",
                    response.status_code,
                    response.text[:200],
                )
                return None

            data = response.json()
            candidates = data.get("candidates", [])
            if not candidates:
                logger.warning("Gemini API returned no candidates.")
                return None

            raw_text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            if not raw_text:
                return None

            cleaned = raw_text.strip()
            if cleaned.startswith("```"):
                cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
                cleaned = re.sub(r"\s*```$", "", cleaned)

            parsed = json.loads(cleaned)

            difficulty_raw = parsed.get("difficulty")
            difficulty_enum = None
            if difficulty_raw:
                try:
                    difficulty_enum = DifficultyLevel(difficulty_raw.lower())
                except ValueError:
                    difficulty_enum = DifficultyLevel.INTERMEDIATE

            return AIEnrichmentResult(
                summary=parsed.get("summary"),
                category=parsed.get("category"),
                tags=parsed.get("tags", []),
                difficulty=difficulty_enum,
                techniques=parsed.get("techniques", []),
                materials_mentioned=parsed.get("materials_mentioned", []),
                ai_provider="gemini",
                ai_model=self.model,
            )

        except httpx.TimeoutException:
            logger.error("Gemini API request timed out after %.1fs", self.timeout)
            return None
        except httpx.RequestError as exc:
            logger.error("Gemini API connection error: %s", exc)
            return None
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            logger.error("Failed to parse Gemini API JSON response: %s", exc)
            return None
        except Exception as exc:
            logger.exception("Unexpected error calling Gemini API: %s", exc)
            return None
