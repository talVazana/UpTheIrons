import os
import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.core.config import Settings, settings


def test_default_settings():
    assert settings.PROJECT_NAME == "Blacksmith Knight API"
    assert settings.FIREBASE_PROJECT_ID == "blacksmith-knight-local"
    assert "127.0.0.1:8080" in settings.FIRESTORE_EMULATOR_HOST
    assert isinstance(settings.CORS_ORIGINS, list)
    assert any("localhost:3000" in origin for origin in settings.CORS_ORIGINS)


def test_custom_environment_settings(monkeypatch):
    monkeypatch.setenv("APP_ENV", "testing")
    monkeypatch.setenv("APP_DEBUG", "true")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("FIREBASE_PROJECT_ID", "custom-forge-id")
    monkeypatch.setenv("CORS_ORIGINS", "http://example.com, https://app.example.com")

    custom = Settings()
    assert custom.ENV == "testing"
    assert custom.DEBUG is True
    assert custom.LOG_LEVEL == "DEBUG"
    assert custom.FIREBASE_PROJECT_ID == "custom-forge-id"
    assert custom.CORS_ORIGINS == ["http://example.com", "https://app.example.com"]
