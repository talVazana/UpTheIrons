from typing import Optional
import re

from app.models.enums import DifficultyLevel
from app.services.ai.base import BaseAIProvider, AIEnrichmentResult


class MockAIProvider(BaseAIProvider):
    """
    Deterministic offline AI provider.
    Enables full testing of enrichment pipelines, UI states, and persistence
    without external network dependencies or token costs.
    """

    async def enrich_content(
        self,
        title: str,
        text: str,
        content_type: str = "video",
    ) -> Optional[AIEnrichmentResult]:
        combined = f"{title} {text}".lower()

        # Heuristic category
        if "knife" in combined or "blade" in combined or "sword" in combined:
            category = "bladesmithing"
            techniques = ["bevel grinding", "edge geometry", "distal taper"]
        elif "heat treat" in combined or "quench" in combined or "normaliz" in combined:
            category = "heat-treatment"
            techniques = ["grain refinement", "critical temperature control", "oil quenching"]
        elif "anvil" in combined or "hammer" in combined or "tongs" in combined or "grinder" in combined:
            category = "tools"
            techniques = ["tool maintenance", "rebound testing", "face dressing"]
        elif "steel" in combined or "alloy" in combined or "iron" in combined:
            category = "materials"
            techniques = ["spark testing", "metallurgical inspection"]
        else:
            category = "forging"
            techniques = ["taper forging", "hot punching", "hammer control"]

        # Difficulty
        if "beginner" in combined or "basics" in combined or "starter" in combined or "how to" in combined:
            difficulty = DifficultyLevel.BEGINNER
        elif "advanced" in combined or "damascus" in combined or "complex" in combined:
            difficulty = DifficultyLevel.ADVANCED
        else:
            difficulty = DifficultyLevel.INTERMEDIATE

        # Materials
        materials = []
        for mat in ["1084", "1095", "5160", "w1", "o1", "mild steel", "cast steel", "wrought iron"]:
            if mat in combined:
                materials.append(f"{mat.upper()} steel" if not mat.endswith("steel") else mat)

        # Tags
        tags = [category]
        if materials:
            tags.append("metallurgy")
        if "anvil" in combined:
            tags.append("anvil")
        if "knife" in combined:
            tags.append("knife-making")

        clean_title = re.sub(r"[^\w\s]", "", title).strip()
        summary = f"Practical craft analysis of {clean_title}. Focuses on {', '.join(techniques[:2])}."

        return AIEnrichmentResult(
            summary=summary,
            category=category,
            tags=list(set(tags)),
            difficulty=difficulty,
            techniques=techniques,
            materials_mentioned=materials,
            ai_provider="mock",
            ai_model="offline-enricher-v1",
        )
