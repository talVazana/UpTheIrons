from enum import Enum


class ContentType(str, Enum):
    GUIDE = "guide"
    MATERIAL = "material"
    VIDEO = "video"
    PRODUCT = "product"
    PROJECT = "project"
    WORKSHOP_TIP = "workshop_tip"
    RULE = "rule"


class ContentStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    FEATURED = "featured"
    NEEDS_REVIEW = "needs_review"
    ARCHIVED = "archived"


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
