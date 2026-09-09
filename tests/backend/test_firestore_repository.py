import sys
from pathlib import Path
import pytest
import httpx

backend_dir = Path(__file__).resolve().parent.parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.core.errors import StorageError, NotFoundError
from app.repositories.firestore import (
    FirestoreRepository,
    to_firestore_value,
    from_firestore_value,
    dict_to_firestore,
    firestore_to_dict,
)


def test_type_serialization_and_deserialization():
    """Verify that Python primitives map correctly to and from Firestore REST representations."""
    test_dict = {
        "title": "Anvil Technique",
        "hardness_rc": 58,
        "temperature_c": 820.5,
        "verified": True,
        "notes": None,
        "tags": ["forging", "heat-treatment"],
        "composition": {"carbon": 0.84, "manganese": 0.75},
    }

    # Dict -> Firestore REST payload
    fs_payload = dict_to_firestore(test_dict)
    assert "fields" in fs_payload
    fields = fs_payload["fields"]
    assert fields["title"] == {"stringValue": "Anvil Technique"}
    assert fields["hardness_rc"] == {"integerValue": "58"}
    assert fields["temperature_c"] == {"doubleValue": 820.5}
    assert fields["verified"] == {"booleanValue": True}
    assert fields["notes"] == {"nullValue": None}
    assert "arrayValue" in fields["tags"]
    assert "mapValue" in fields["composition"]

    # Firestore REST doc -> Dict
    doc_wrapper = {
        "name": "projects/test-proj/databases/(default)/documents/smoke/anvil_01",
        "fields": fields,
    }
    recovered = firestore_to_dict(doc_wrapper)
    assert recovered["_id"] == "anvil_01"
    assert recovered["title"] == "Anvil Technique"
    assert recovered["hardness_rc"] == 58
    assert recovered["temperature_c"] == 820.5
    assert recovered["verified"] is True
    assert recovered["notes"] is None
    assert recovered["tags"] == ["forging", "heat-treatment"]
    assert recovered["composition"] == {"carbon": 0.84, "manganese": 0.75}


@pytest.mark.anyio
async def test_repository_crud_with_mock_transport():
    """Verify repository create, get, update, delete, and list operations."""
    store = {}

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        method = request.method
        doc_key = path.split("/documents/")[-1]

        if method == "PATCH":
            import json
            body = json.loads(request.content)
            store[doc_key] = body.get("fields", {})
            return httpx.Response(
                200,
                json={"name": f"projects/test/databases/(default)/documents/{doc_key}", "fields": store[doc_key]},
            )

        if method == "GET":
            if doc_key in store:
                return httpx.Response(
                    200,
                    json={"name": f"projects/test/databases/(default)/documents/{doc_key}", "fields": store[doc_key]},
                )
            if doc_key == "materials" or doc_key.endswith("/materials"):
                docs = [
                    {"name": f"projects/test/databases/(default)/documents/{k}", "fields": v}
                    for k, v in store.items()
                ]
                return httpx.Response(200, json={"documents": docs})
            return httpx.Response(404, json={"error": "not found"})

        if method == "DELETE":
            if doc_key in store:
                del store[doc_key]
                return httpx.Response(200, json={})
            return httpx.Response(404, json={})

        return httpx.Response(400)

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as mock_client:
        repo = FirestoreRepository(host="127.0.0.1:8080", project_id="test-proj", client=mock_client)

        # 1. CREATE
        created = await repo.create("materials", "steel_1084", {"name": "1084", "carbon": 0.84})
        assert created["_id"] == "steel_1084"
        assert created["name"] == "1084"
        assert created["carbon"] == 0.84

        # 2. GET (found)
        retrieved = await repo.get("materials", "steel_1084")
        assert retrieved is not None
        assert retrieved["_id"] == "steel_1084"
        assert retrieved["carbon"] == 0.84

        # 3. GET (not found)
        missing = await repo.get("materials", "nonexistent")
        assert missing is None

        # 4. UPDATE
        updated = await repo.update("materials", "steel_1084", {"status": "verified"})
        assert updated["name"] == "1084"
        assert updated["status"] == "verified"

        # 5. LIST
        doc_list = await repo.list("materials")
        assert len(doc_list) == 1
        assert doc_list[0]["_id"] == "steel_1084"

        # 6. DELETE (existing)
        deleted = await repo.delete("materials", "steel_1084")
        assert deleted is True

        # 7. GET after DELETE
        after_delete = await repo.get("materials", "steel_1084")
        assert after_delete is None

        # 8. DELETE (already gone)
        deleted_again = await repo.delete("materials", "steel_1084")
        assert deleted_again is False


@pytest.mark.anyio
async def test_storage_unavailable_error():
    """Verify repository raises StorageError when connection fails."""
    def fail_handler(request: httpx.Request):
        raise httpx.ConnectError("Connection refused by emulator", request=request)

    transport = httpx.MockTransport(fail_handler)
    async with httpx.AsyncClient(transport=transport) as mock_client:
        repo = FirestoreRepository(host="127.0.0.1:9999", project_id="test-proj", client=mock_client)

        with pytest.raises(StorageError) as exc_info:
            await repo.get("materials", "test")
        assert "Storage unavailable" in str(exc_info.value)
