from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging, RequestLoggingMiddleware
from app.core.errors import register_error_handlers
from app.api.router import api_router

# Initialize structured logging
logger = setup_logging(log_level=settings.LOG_LEVEL)

# Initialize application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    debug=settings.DEBUG,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)

# Error handling
register_error_handlers(app)

# API Routers
app.include_router(api_router)


@app.get("/", tags=["root"])
def read_root():
    """Root metadata endpoint."""
    return {
        "message": "Blacksmith Knight API online",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "ok",
    }


@app.get("/health", tags=["health"])
def read_health():
    """Root health probe endpoint."""
    return {"status": "ok"}
