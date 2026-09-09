from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.api.v1.sources import router as sources_router
from app.api.v1.youtube import router as youtube_router
from app.api.v1.settings import router as settings_router
from app.api.v1.videos import router as videos_router
from app.api.v1.rss import router as rss_router
from app.api.v1.articles import router as articles_router

v1_router = APIRouter()
v1_router.include_router(health_router)
v1_router.include_router(sources_router)
v1_router.include_router(youtube_router)
v1_router.include_router(settings_router)
v1_router.include_router(videos_router)
v1_router.include_router(rss_router)
v1_router.include_router(articles_router)

