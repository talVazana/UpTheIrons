import json
import logging
import sys
from pathlib import Path
from fastapi.testclient import TestClient

backend_dir = Path(__file__).resolve().parent.parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.main import app
from app.core.logging import StructuredFormatter, setup_logging

client = TestClient(app)


def test_structured_formatter():
    formatter = StructuredFormatter()
    record = logging.LogRecord(
        name="test.logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=10,
        msg="Test forge event",
        args=(),
        exc_info=None,
    )
    record.extra_fields = {"steel_grade": "1095", "temperature_f": 1500}

    formatted = formatter.format(record)
    data = json.loads(formatted)

    assert data["level"] == "INFO"
    assert data["logger"] == "test.logger"
    assert data["message"] == "Test forge event"
    assert data["steel_grade"] == "1095"
    assert data["temperature_f"] == 1500
    assert "timestamp" in data


def test_request_logging_middleware_header():
    response = client.get("/health")
    assert response.status_code == 200
    assert "X-Process-Time-Ms" in response.headers
    process_time = float(response.headers["X-Process-Time-Ms"])
    assert process_time >= 0.0
