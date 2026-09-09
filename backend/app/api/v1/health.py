from fastapi import APIRouter
import socket
from app.core.config import settings

router = APIRouter(tags=["health"])


def check_emulator_connectivity(host_port: str) -> bool:
    """Non-blocking TCP socket check to verify emulator availability."""
    try:
        parts = host_port.split(":")
        host = parts[0]
        port = int(parts[1]) if len(parts) > 1 else 8080
        with socket.create_connection((host, port), timeout=0.3):
            return True
    except Exception:
        return False


@router.get("/health")
def get_health():
    """Health check endpoint returning system status and component diagnostics."""
    emulator_reachable = check_emulator_connectivity(settings.FIRESTORE_EMULATOR_HOST)

    return {
        "status": "ok",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENV,
        "diagnostics": {
            "firestore_emulator": {
                "host": settings.FIRESTORE_EMULATOR_HOST,
                "project_id": settings.FIREBASE_PROJECT_ID,
                "reachable": emulator_reachable,
            }
        },
    }
