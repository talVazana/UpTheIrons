from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.api.v1.sources import router as sources_router
from app.api.v1.youtube import router as youtube_router

v1_router = APIRouter()
v1_router.include_router(health_router)
v1_router.include_router(sources_router)
v1_router.include_router(youtube_router)

