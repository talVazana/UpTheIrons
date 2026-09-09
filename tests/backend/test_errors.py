import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.testclient import TestClient

backend_dir = Path(__file__).resolve().parent.parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.main import app
from app.core.errors import (
    register_error_handlers,
    AppException,
    NotFoundError,
    BadRequestError,
    SourceError,
)

client = TestClient(app)


def test_404_standard_format():
    """Verify that accessing a nonexistent route returns the structured error envelope."""
    response = client.get("/api/nonexistent-route-xyz")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "NOT_FOUND"
    assert "message" in data["error"]


def test_custom_app_exceptions():
    """Verify custom AppException classes map correctly to HTTP status codes and structure."""
    test_app = FastAPI()
    register_error_handlers(test_app)

    @test_app.get("/test-not-found")
    def raise_not_found():
        raise NotFoundError("Specific item was not found", details={"item_id": "test-123"})

    @test_app.get("/test-bad-request")
    def raise_bad_request():
        raise BadRequestError("Malformed query parameters")

    @test_app.get("/test-source-error")
    def raise_source_error():
        raise SourceError("YouTube API timeout")

    @test_app.get("/test-internal-error")
    def raise_internal():
        raise RuntimeError("Unexpected boom")

    test_client = TestClient(test_app, raise_server_exceptions=False)

    # 404
    res = test_client.get("/test-not-found")
    assert res.status_code == 404
    assert res.json()["error"]["code"] == "NOT_FOUND"
    assert res.json()["error"]["details"]["item_id"] == "test-123"

    # 400
    res = test_client.get("/test-bad-request")
    assert res.status_code == 400
    assert res.json()["error"]["code"] == "BAD_REQUEST"

    # 502
    res = test_client.get("/test-source-error")
    assert res.status_code == 502
    assert res.json()["error"]["code"] == "SOURCE_ERROR"

    # 500
    res = test_client.get("/test-internal-error")
    assert res.status_code == 500
    assert res.json()["error"]["code"] == "INTERNAL_SERVER_ERROR"
