import os
from typing import List
from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Central configuration for Blacksmith Knight FastAPI backend."""

    PROJECT_NAME: str = "Blacksmith Knight API"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Forging Heaven — Backend API for Blacksmith Knight"

    # Environment
    ENV: str = Field(default_factory=lambda: os.getenv("APP_ENV", "development"))
    DEBUG: bool = Field(
        default_factory=lambda: os.getenv("APP_DEBUG", "false").lower() in ("true", "1", "yes")
    )

    # Server binding
    HOST: str = Field(default_factory=lambda: os.getenv("APP_HOST", "0.0.0.0"))
    PORT: int = Field(default_factory=lambda: int(os.getenv("APP_PORT", "8000")))

    # CORS origins
    CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: [
            origin.strip()
            for origin in os.getenv(
                "CORS_ORIGINS",
                "http://localhost:3000,http://127.0.0.1:3000",
            ).split(",")
            if origin.strip()
        ]
    )

    # Firebase / Firestore emulator configuration
    FIREBASE_PROJECT_ID: str = Field(
        default_factory=lambda: os.getenv("FIREBASE_PROJECT_ID", "blacksmith-knight-local")
    )
    FIRESTORE_EMULATOR_HOST: str = Field(
        default_factory=lambda: os.getenv("FIRESTORE_EMULATOR_HOST", "127.0.0.1:8080")
    )

    # Logging level
    LOG_LEVEL: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO").upper())

    # External APIs (placeholders - not committed to Git)
    YOUTUBE_API_KEY: str = Field(default_factory=lambda: os.getenv("YOUTUBE_API_KEY", ""))
    AI_API_KEY: str = Field(default_factory=lambda: os.getenv("AI_API_KEY", ""))
    AI_PROVIDER: str = Field(default_factory=lambda: os.getenv("AI_PROVIDER", "gemini"))
    AI_MODEL: str = Field(default_factory=lambda: os.getenv("AI_MODEL", "gemini-2.5-flash"))


settings = Settings()
