import re
import logging
from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from app.models.content import ContentEnvelope, utc_now
from app.models.enums import ContentStatus
from app.repositories.firestore import firestore_repository

logger = logging.getLogger("blacksmith_knight.rules")

CONTENT_VAULT_COLLECTION = "content_vault"


class RuleSection(BaseModel):
    title: str
    content: str


class RuleDocument(BaseModel):
    id: str
    filename: str
    title: str
    description: Optional[str] = None
    content: str
    sections: List[RuleSection] = Field(default_factory=list)
    updated_at: str = Field(default_factory=lambda: utc_now().isoformat())


class EditorialOverrideRequest(BaseModel):
    status: Optional[ContentStatus] = None
    is_pinned: Optional[bool] = None
    is_featured: Optional[bool] = None
    is_verified: Optional[bool] = None
    editorial_notes: Optional[str] = None


class RulesService:
    """
    Service responsible for loading, parsing, and serving markdown rule configurations.
    Enforces Master Spec Section 30 & 31:
    The rules directory is the central behavioral and editorial configuration of Blacksmith Knight.
    """

    def __init__(self, config_dir: Optional[Path] = None):
        if config_dir:
            self.config_dir = config_dir
        else:
            # Look up from backend/app/services to repo root / config
            self.config_dir = Path(__file__).resolve().parent.parent.parent.parent / "config"
        self._cache: Dict[str, RuleDocument] = {}
        self.load_all()

    def _parse_markdown(self, path: Path) -> RuleDocument:
        content = path.read_text(encoding="utf-8-sig")
        lines = content.splitlines()

        # Extract title from first # header
        title = path.stem.replace("_", " ").title()
        description = None

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("# ") or stripped.startswith("#"):
                clean_title = re.sub(r"^#+\s*", "", stripped).strip()
                if clean_title:
                    title = clean_title
                    break

        # Extract description from first non-empty, non-header line
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and not stripped.startswith("-"):
                description = stripped
                break

        # Parse sections (## Header)
        sections: List[RuleSection] = []
        current_section_title = None
        current_section_lines: List[str] = []

        for line in lines:
            if line.startswith("## "):
                if current_section_title:
                    sections.append(
                        RuleSection(
                            title=current_section_title,
                            content="\n".join(current_section_lines).strip(),
                        )
                    )
                current_section_title = line.lstrip("## ").strip()
                current_section_lines = []
            elif current_section_title is not None:
                current_section_lines.append(line)

        if current_section_title:
            sections.append(
                RuleSection(
                    title=current_section_title,
                    content="\n".join(current_section_lines).strip(),
                )
            )

        return RuleDocument(
            id=path.stem,
            filename=path.name,
            title=title,
            description=description,
            content=content,
            sections=sections,
        )

    def load_all(self) -> Dict[str, RuleDocument]:
        """Loads or reloads all .md files in config directory."""
        if not self.config_dir.exists():
            logger.warning("Config directory not found at %s", self.config_dir)
            return {}

        new_cache = {}
        for md_file in sorted(self.config_dir.glob("*.md")):
            try:
                doc = self._parse_markdown(md_file)
                new_cache[doc.id] = doc
            except Exception as exc:
                logger.error("Failed to parse rule file %s: %s", md_file, exc)

        self._cache = new_cache
        logger.info("Loaded %d rule documents from %s", len(self._cache), self.config_dir)
        return self._cache

    def get_rule(self, rule_id: str) -> Optional[RuleDocument]:
        return self._cache.get(rule_id)

    def list_rules(self) -> List[RuleDocument]:
        return list(self._cache.values())

    async def apply_editorial_override(
        self,
        content_id: str,
        override: EditorialOverrideRequest,
    ) -> Optional[ContentEnvelope]:
        """
        Applies editorial status and manual overrides to a ContentEnvelope.
        Supports 15.10: featured, pinned, verified, needs_review, hidden.
        """
        data = await firestore_repository.get(CONTENT_VAULT_COLLECTION, content_id)
        if not data:
            return None

        envelope = ContentEnvelope.model_validate(data)

        if override.status is not None:
            envelope.status = override.status

        if override.is_pinned is not None:
            envelope.metadata["is_pinned"] = override.is_pinned
            if override.is_pinned:
                envelope.status = ContentStatus.PINNED

        if override.is_featured is not None:
            envelope.metadata["is_featured"] = override.is_featured
            if override.is_featured:
                envelope.status = ContentStatus.FEATURED

        if override.is_verified is not None:
            envelope.metadata["is_verified"] = override.is_verified
            if override.is_verified:
                envelope.status = ContentStatus.VERIFIED

        if override.editorial_notes is not None:
            envelope.metadata["editorial_notes"] = override.editorial_notes

        envelope.updated_at = utc_now()

        await firestore_repository.create(
            CONTENT_VAULT_COLLECTION,
            content_id,
            envelope.model_dump(mode="json"),
        )
        return envelope


rules_service = RulesService()
