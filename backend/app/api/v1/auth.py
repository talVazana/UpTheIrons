from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import secrets

from app.repositories.firestore import firestore_repository

router = APIRouter(prefix="/auth", tags=["auth"])

SETTINGS_COLLECTION = "system_config"
AUTH_DOC_ID = "admin_auth"

# In-memory session store for MVP
_sessions = set()

class LoginRequest(BaseModel):
    username: str
    password: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class TokenResponse(BaseModel):
    token: str

async def get_admin_credentials():
    doc = await firestore_repository.get(SETTINGS_COLLECTION, AUTH_DOC_ID)
    if doc and "username" in doc and "password" in doc:
        return doc["username"], doc["password"]
    return "Kiko", "Kiko"

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    valid_username, valid_password = await get_admin_credentials()
    if request.username == valid_username and request.password == valid_password:
        token = secrets.token_hex(32)
        _sessions.add(token)
        return TokenResponse(token=token)
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/change-password")
async def change_password(request: ChangePasswordRequest):
    valid_username, valid_password = await get_admin_credentials()
    if request.old_password != valid_password:
        raise HTTPException(status_code=401, detail="Invalid old password")
    
    update_dict = {"username": valid_username, "password": request.new_password}
    existing = await firestore_repository.get(SETTINGS_COLLECTION, AUTH_DOC_ID)
    if existing:
        await firestore_repository.update(SETTINGS_COLLECTION, AUTH_DOC_ID, update_dict)
    else:
        await firestore_repository.create(SETTINGS_COLLECTION, AUTH_DOC_ID, update_dict)
    
    return {"status": "success"}

@router.post("/verify")
async def verify_token(token_req: TokenResponse):
    if token_req.token in _sessions:
        return {"valid": True}
    raise HTTPException(status_code=401, detail="Invalid token")
