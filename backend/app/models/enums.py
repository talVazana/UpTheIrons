from enum import Enum


class ContentType(str, Enum):
    GUIDE = "guide"
    ARTICLE = "article"
    MATERIAL = "material"
    VIDEO = "video"
    PRODUCT = "product"
    PROJECT = "project"
    WORKSHOP_TIP = "workshop_tip"
    RULE = "rule"
    TOOL = "tool"


class ToolCategory(str, Enum):
    FORGING = "forging"
    HEATING = "heating"
    GRINDING = "grinding"
    FINISHING = "finishing"
    INFRASTRUCTURE = "infrastructure"


class ContentStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    FEATURED = "featured"
    PINNED = "pinned"
    VERIFIED = "verified"
    NEEDS_REVIEW = "needs_review"
    ARCHIVED = "archived"
    HIDDEN = "hidden"


class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class SourceType(str, Enum):
    YOUTUBE_CHANNEL = "youtube_channel"
    RSS_FEED = "rss_feed"
    PRODUCT_API = "product_api"
    MANUAL = "manual"


class SourceStatus(str, Enum):
    CONFIGURED = "configured"
    HEALTHY = "healthy"
    WARNING = "warning"
    FAILED = "failed"
    DISABLED = "disabled"


class TrustLabel(str, Enum):
    FACT = "fact"
    SOURCE_BACKED = "source_backed_recommendation"
    CRAFT_PRACTICE = "craft_practice"
    PERSONAL_EXPERIENCE = "personal_experience"
    HISTORICAL_INTERPRETATION = "historical_interpretation"
    AI_SUMMARY = "ai_summary"
    OPINION = "opinion"

