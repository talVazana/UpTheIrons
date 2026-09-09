import re
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from app.models.enums import ContentStatus

HYPE_PATTERNS = [
    r"\byou won't believe\b",
    r"\binsane secret\b",
    r"\bmiracle metal\b",
    r"\bholds an edge forever\b",
    r"\bunbreakable knife\b",
    r"\bnever dulls\b",
]

SPAM_PATTERNS = [
    r"\buse promo code\b",
    r"\blimited time offer\b",
    r"\border today and get \d+%\b",
    r"\bclick the link below to purchase\b",
    r"\bdiscount code at checkout\b",
]

CRAFT_KEYWORDS = [
    "blacksmith", "forge", "forging", "anvil", "hammer", "taper", "upset",
    "punch", "drift", "blade", "knife", "bevel", "quench", "temper",
    "normalize", "anneal", "steel", "1084", "1095", "5160", "4140",
    "o1", "w1", "grinder", "abrasive", "tongs", "heat treat"
]


class ValidationIssue(BaseModel):
    severity: str = Field(description="'error', 'warning', or 'info'")
    rule_category: str
    message: str


class ContentValidationResult(BaseModel):
    valid: bool
    relevance_score: float = Field(ge=0.0, le=1.0)
    suggested_status: ContentStatus
    issues: List[ValidationIssue] = Field(default_factory=list)
    craft_keywords_found: List[str] = Field(default_factory=list)


class RuleValidator:
    """
    Evaluates content items against Master Spec rules (Sections 15.03 - 15.07).
    Enforces safety verifications, anti-spam boundaries, clickbait filters,
    and metallurgical precision.
    """

    def validate_content(
        self,
        title: str,
        text: str,
        tags: Optional[List[str]] = None,
        source_name: Optional[str] = None,
    ) -> ContentValidationResult:
        combined = f"{title}\n{text}".lower()
        issues: List[ValidationIssue] = []

        # 1. Commercial Spam Check (15.06, 15.03)
        for pattern in SPAM_PATTERNS:
            if re.search(pattern, combined):
                issues.append(
                    ValidationIssue(
                        severity="error",
                        rule_category="commercial_policy",
                        message=f"Detected aggressive commercial promotional language matching '{pattern}'.",
                    )
                )

        # 2. Clickbait & Hype Check (15.07)
        for pattern in HYPE_PATTERNS:
            if re.search(pattern, combined):
                issues.append(
                    ValidationIssue(
                        severity="warning",
                        rule_category="editorial_style",
                        message=f"Detected exaggerated claim or sensationalist phrasing matching '{pattern}'.",
                    )
                )

        # 3. Critical Safety Checks (15.05)
        # 3a. Galvanized steel hazard
        if "galvaniz" in combined or "zinc" in combined:
            safe_zinc_terms = ["toxic", "fume", "fever", "strip", "muriatic", "acid", "poison", "ventilate"]
            if not any(t in combined for t in safe_zinc_terms):
                issues.append(
                    ValidationIssue(
                        severity="error",
                        rule_category="safety_rules",
                        message="Mentions heating or forging galvanized/zinc metal without mandatory toxic zinc fume fever hazard warnings.",
                    )
                )

        # 3b. Ceramic fiber blanket hazard
        if "kaowool" in combined or "ceramic blanket" in combined or "ceramic fiber" in combined:
            safe_fiber_terms = ["rigidiz", "seal", "satanite", "refractory", "respirator", "silica", "coat"]
            if not any(t in combined for t in safe_fiber_terms):
                issues.append(
                    ValidationIssue(
                        severity="error",
                        rule_category="safety_rules",
                        message="Mentions ceramic fiber blanket without mandatory rigidizer/refractory sealing or silica dust warnings.",
                    )
                )

        # 3c. Unsafe quenching practices
        if "quench" in combined and "water" in combined and ("1095" in combined or "o1" in combined or "file" in combined):
            issues.append(
                ValidationIssue(
                    severity="warning",
                    rule_category="safety_rules",
                    message="Water quenching high carbon alloy carries extreme catastrophic cracking risk; oil quench recommended.",
                )
            )

        # 4. Craft Relevance Scoring (15.03)
        found_keywords = [kw for kw in CRAFT_KEYWORDS if kw in combined]
        if tags:
            for t in tags:
                clean_t = t.lower().strip()
                if clean_t in CRAFT_KEYWORDS and clean_t not in found_keywords:
                    found_keywords.append(clean_t)

        raw_score = min(1.0, len(found_keywords) / 6.0)
        relevance_score = round(raw_score, 2)

        if relevance_score < 0.2:
            issues.append(
                ValidationIssue(
                    severity="warning",
                    rule_category="content_rules",
                    message="Low craft domain relevance. Few recognized blacksmithing or metalworking terms found.",
                )
            )

        # 5. Determine Validity & Suggested Status
        has_errors = any(i.severity == "error" for i in issues)
        valid = not has_errors and relevance_score >= 0.25

        if has_errors:
            suggested_status = ContentStatus.NEEDS_REVIEW
        elif relevance_score < 0.25:
            suggested_status = ContentStatus.HIDDEN
        else:
            suggested_status = ContentStatus.PUBLISHED

        return ContentValidationResult(
            valid=valid,
            relevance_score=relevance_score,
            suggested_status=suggested_status,
            issues=issues,
            craft_keywords_found=found_keywords,
        )


rule_validator = RuleValidator()
