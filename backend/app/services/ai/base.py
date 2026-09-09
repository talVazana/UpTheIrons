from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.models.enums import DifficultyLevel


class AIEnrichmentResult(BaseModel):
    """Normalized structured output from AI enrichment layer."""

    summary: Optional[str] = Field(default=None, description="Concise technical forge summary")
    category: Optional[str] = Field(default=None, description="Forging category classification")
    tags: List[str] = Field(default_factory=list, description="Extracted domain tags")
    difficulty: Optional[DifficultyLevel] = Field(default=None, description="Craft difficulty level")
    techniques: List[str] = Field(default_factory=list, description="Specific blacksmithing techniques identified")
    materials_mentioned: List[str] = Field(default_factory=list, description="Specific steel alloys or metals mentioned")
    ai_provider: str = Field(default="gemini", description="Provider used")
    ai_model: str = Field(default="gemini-2.5-flash", description="Model used")


class BaseAIProvider(ABC):
    """Abstract interface for pluggable AI enrichment providers (Gemini, Claude, DeepSeek, Mock)."""

    @abstractmethod
    async def enrich_content(
        self,
        title: str,
        text: str,
        content_type: str = "video",
    ) -> Optional[AIEnrichmentResult]:
        """Analyzes text and returns structured enrichment or None if unavailable."""
        pass

    async def classify(self, title: str, text: str) -> Optional[str]:
        """Classifies content domain."""
        res = await self.enrich_content(title, text)
        return res.category if res else None

    async def summarize(self, title: str, text: str) -> Optional[str]:
        """Generates concise technical summary."""
        res = await self.enrich_content(title, text)
        return res.summary if res else None

    async def extract(self, title: str, text: str) -> Dict[str, Any]:
        """Extracts technical entities (tags, techniques, materials, difficulty)."""
        res = await self.enrich_content(title, text)
        if not res:
            return {"tags": [], "techniques": [], "materials": [], "difficulty": None}
        return {
            "tags": res.tags,
            "techniques": res.techniques,
            "materials": res.materials_mentioned,
            "difficulty": res.difficulty.value if res.difficulty else None,
        }
