from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.core.config import settings
from app.repositories.firestore import firestore_repository

router = APIRouter(prefix="/settings", tags=["settings"])

SETTINGS_COLLECTION = "system_config"
API_KEYS_DOC_ID = "api_keys"

# In-memory cache for fast access
_cached_keys = {
    "youtube_api_key": None,
    "gemini_api_key": None,
}


def mask_key(key: Optional[str]) -> Optional[str]:
    """Masks secret key, revealing only first 6 and last 4 chars."""
    if not key or len(key) < 10:
        return "********" if key else None
    return f"{key[:6]}...{key[-4:]}"


async def get_effective_youtube_api_key() -> str:
    """
    Returns effective YouTube API key in priority order:
    1. Memory cache
    2. Firestore system_config/api_keys
    3. Environment variable YOUTUBE_API_KEY
    """
    if _cached_keys["youtube_api_key"]:
        return _cached_keys["youtube_api_key"]

    try:
        doc = await firestore_repository.get(SETTINGS_COLLECTION, API_KEYS_DOC_ID)
        if doc and doc.get("youtube_api_key"):
            _cached_keys["youtube_api_key"] = doc["youtube_api_key"]
            return doc["youtube_api_key"]
    except Exception:
        pass

    env_key = settings.YOUTUBE_API_KEY.strip()
    return env_key


async def get_effective_ai_api_key() -> str:
    """Returns effective AI API key (Firestore > env)."""
    if _cached_keys["gemini_api_key"]:
        return _cached_keys["gemini_api_key"]

    try:
        doc = await firestore_repository.get(SETTINGS_COLLECTION, API_KEYS_DOC_ID)
        if doc and doc.get("ai_api_key"):
            _cached_keys["gemini_api_key"] = doc["ai_api_key"]
            return doc["ai_api_key"]
    except Exception:
        pass

    return settings.AI_API_KEY.strip()


class UpdateApiKeysRequest(BaseModel):
    youtube_api_key: Optional[str] = Field(default=None, max_length=200)
    ai_api_key: Optional[str] = Field(default=None, max_length=200)


class ApiKeysStatusResponse(BaseModel):
    youtube_api_key_configured: bool
    youtube_api_key_masked: Optional[str]
    ai_api_key_configured: bool
    ai_api_key_masked: Optional[str]


@router.get("/keys", response_model=ApiKeysStatusResponse)
async def get_api_keys_status():
    """Returns configuration status of API keys with sensitive values masked."""
    yt_key = await get_effective_youtube_api_key()
    ai_key = await get_effective_ai_api_key()

    return ApiKeysStatusResponse(
        youtube_api_key_configured=bool(yt_key),
        youtube_api_key_masked=mask_key(yt_key) if yt_key else None,
        ai_api_key_configured=bool(ai_key),
        ai_api_key_masked=mask_key(ai_key) if ai_key else None,
    )


@router.post("/keys", response_model=ApiKeysStatusResponse)
async def set_api_keys(request: UpdateApiKeysRequest):
    """
    Sets API keys dynamically. Stores securely in Firestore and updates memory cache.
    Never requires backend restart.
    """
    update_dict = {}
    if request.youtube_api_key is not None:
        clean_yt = request.youtube_api_key.strip()
        update_dict["youtube_api_key"] = clean_yt
        _cached_keys["youtube_api_key"] = clean_yt

    if request.ai_api_key is not None:
        clean_ai = request.ai_api_key.strip()
        update_dict["ai_api_key"] = clean_ai
        _cached_keys["gemini_api_key"] = clean_ai

    if update_dict:
        existing = await firestore_repository.get(SETTINGS_COLLECTION, API_KEYS_DOC_ID)
        if existing:
            await firestore_repository.update(SETTINGS_COLLECTION, API_KEYS_DOC_ID, update_dict)
        else:
            await firestore_repository.create(SETTINGS_COLLECTION, API_KEYS_DOC_ID, update_dict)

    return await get_api_keys_status()
