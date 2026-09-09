import logging
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional
import httpx


from app.core.config import settings
from app.core.errors import StorageError, NotFoundError
from app.repositories.base import BaseRepository

logger = logging.getLogger("blacksmith_knight")


def to_firestore_value(val: Any) -> Dict[str, Any]:
    """Converts a standard Python value to Firestore REST typed value."""
    if val is None:
        return {"nullValue": None}
    if isinstance(val, bool):
        return {"booleanValue": val}
    if isinstance(val, int):
        return {"integerValue": str(val)}
    if isinstance(val, float):
        return {"doubleValue": val}
    if isinstance(val, str):
        return {"stringValue": val}
    if isinstance(val, list):
        return {"arrayValue": {"values": [to_firestore_value(item) for item in val]}}
    if isinstance(val, dict):
        return {"mapValue": {"fields": {k: to_firestore_value(v) for k, v in val.items()}}}
    return {"stringValue": str(val)}


def from_firestore_value(val_dict: Dict[str, Any]) -> Any:
    """Converts a Firestore REST typed value to a standard Python value."""
    if "nullValue" in val_dict:
        return None
    if "booleanValue" in val_dict:
        return val_dict["booleanValue"]
    if "integerValue" in val_dict:
        return int(val_dict["integerValue"])
    if "doubleValue" in val_dict:
        return float(val_dict["doubleValue"])
    if "stringValue" in val_dict:
        return val_dict["stringValue"]
    if "timestampValue" in val_dict:
        return val_dict["timestampValue"]
    if "arrayValue" in val_dict:
        values = val_dict["arrayValue"].get("values", [])
        return [from_firestore_value(v) for v in values]
    if "mapValue" in val_dict:
        fields = val_dict["mapValue"].get("fields", {})
        return {k: from_firestore_value(v) for k, v in fields.items()}
    return None


def dict_to_firestore(data: Dict[str, Any]) -> Dict[str, Any]:
    """Converts a dictionary to a Firestore REST document payload."""
    clean_data = {k: v for k, v in data.items() if not k.startswith("_")}
    return {"fields": {k: to_firestore_value(v) for k, v in clean_data.items()}}


def firestore_to_dict(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Converts a Firestore REST document payload to a dictionary with _id."""
    fields = doc.get("fields", {})
    result = {k: from_firestore_value(v) for k, v in fields.items()}
    name = doc.get("name", "")
    if name:
        result["_id"] = name.split("/")[-1]
    return result


class FirestoreRepository(BaseRepository):
    """Repository implementation utilizing the Firestore REST API and Local Emulator."""

    def __init__(
        self,
        host: Optional[str] = None,
        project_id: Optional[str] = None,
        client: Optional[httpx.AsyncClient] = None,
    ):
        self.host = host or settings.FIRESTORE_EMULATOR_HOST
        self.project_id = project_id or settings.FIREBASE_PROJECT_ID
        self.base_url = f"http://{self.host}/v1/projects/{self.project_id}/databases/(default)/documents"
        self._external_client = client

    @asynccontextmanager
    async def _client_scope(self):
        if self._external_client is not None:
            yield self._external_client
        else:
            async with httpx.AsyncClient(timeout=3.0) as client:
                yield client

    async def create(self, collection: str, doc_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates or overwrites a document with the given doc_id."""
        url = f"{self.base_url}/{collection}/{doc_id}"
        payload = dict_to_firestore(data)

        async with self._client_scope() as client:
            try:
                response = await client.patch(url, json=payload)
                if response.status_code not in (200, 201):
                    raise StorageError(
                        f"Failed to create document {collection}/{doc_id}: {response.text}",
                        details={"status_code": response.status_code},
                    )
                return firestore_to_dict(response.json())
            except (httpx.ConnectError, httpx.TimeoutException) as exc:
                logger.error(f"Firestore emulator unavailable at {self.host}: {str(exc)}")
                raise StorageError(f"Storage unavailable: cannot reach Firestore emulator at {self.host}")

    async def get(self, collection: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a document by collection and doc_id."""
        url = f"{self.base_url}/{collection}/{doc_id}"

        async with self._client_scope() as client:
            try:
                response = await client.get(url)
                if response.status_code == 404:
                    return None
                if response.status_code != 200:
                    raise StorageError(
                        f"Failed to retrieve document {collection}/{doc_id}: {response.text}",
                        details={"status_code": response.status_code},
                    )
                return firestore_to_dict(response.json())
            except (httpx.ConnectError, httpx.TimeoutException) as exc:
                logger.error(f"Firestore emulator unavailable at {self.host}: {str(exc)}")
                raise StorageError(f"Storage unavailable: cannot reach Firestore emulator at {self.host}")

    async def update(self, collection: str, doc_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Updates fields in an existing document."""
        # Check existence first
        existing = await self.get(collection, doc_id)
        if existing is None:
            raise NotFoundError(f"Cannot update nonexistent document {collection}/{doc_id}")

        # Merge with existing
        merged = {**existing, **data}
        return await self.create(collection, doc_id, merged)

    async def delete(self, collection: str, doc_id: str) -> bool:
        """Deletes a document by collection and doc_id."""
        url = f"{self.base_url}/{collection}/{doc_id}"

        async with self._client_scope() as client:
            try:
                response = await client.delete(url)
                if response.status_code in (200, 204):
                    return True
                if response.status_code == 404:
                    return False
                raise StorageError(
                    f"Failed to delete document {collection}/{doc_id}: {response.text}",
                    details={"status_code": response.status_code},
                )
            except (httpx.ConnectError, httpx.TimeoutException) as exc:
                logger.error(f"Firestore emulator unavailable at {self.host}: {str(exc)}")
                raise StorageError(f"Storage unavailable: cannot reach Firestore emulator at {self.host}")

    async def list(self, collection: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Lists documents in a collection."""
        url = f"{self.base_url}/{collection}"
        params = {"pageSize": limit}

        async with self._client_scope() as client:
            try:
                response = await client.get(url, params=params)
                if response.status_code == 404:
                    return []
                if response.status_code != 200:
                    raise StorageError(
                        f"Failed to list collection {collection}: {response.text}",
                        details={"status_code": response.status_code},
                    )
                data = response.json()
                documents = data.get("documents", [])
                return [firestore_to_dict(doc) for doc in documents]
            except (httpx.ConnectError, httpx.TimeoutException) as exc:
                logger.error(f"Firestore emulator unavailable at {self.host}: {str(exc)}")
                raise StorageError(f"Storage unavailable: cannot reach Firestore emulator at {self.host}")



# Default singleton instance
firestore_repository = FirestoreRepository()
