from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.api.v1.sources import router as sources_router
from app.api.v1.youtube import router as youtube_router
from app.api.v1.settings import router as settings_router
from app.api.v1.videos import router as videos_router
from app.api.v1.rss import router as rss_router
from app.api.v1.articles import router as articles_router
from app.api.v1.products import router as products_router
from app.api.v1.ai import router as ai_router
from app.api.v1.rules import router as rules_router
from app.api.v1.guides import router as guides_router
from app.api.v1.materials import router as materials_router
from app.api.v1.tools import router as tools_router
from app.api.v1.projects import router as projects_router
from app.api.v1.auth import router as auth_router

v1_router = APIRouter()
v1_router.include_router(health_router)
v1_router.include_router(sources_router)
v1_router.include_router(youtube_router)
v1_router.include_router(settings_router)
v1_router.include_router(videos_router)
v1_router.include_router(rss_router)
v1_router.include_router(articles_router)
v1_router.include_router(products_router)
v1_router.include_router(ai_router)
v1_router.include_router(rules_router)
v1_router.include_router(guides_router)
v1_router.include_router(materials_router)
v1_router.include_router(tools_router)
v1_router.include_router(projects_router)
v1_router.include_router(auth_router)



