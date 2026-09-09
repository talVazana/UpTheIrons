from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseRepository(ABC):
    """Abstract interface for application storage.
    Shields domain and API layers from specific database technologies.
    """

    @abstractmethod
    async def create(self, collection: str, doc_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a document with the given ID."""
        pass

    @abstractmethod
    async def get(self, collection: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a document by collection and ID, or returns None."""
        pass

    @abstractmethod
    async def update(self, collection: str, doc_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Updates fields in an existing document."""
        pass

    @abstractmethod
    async def delete(self, collection: str, doc_id: str) -> bool:
        """Deletes a document by collection and ID."""
        pass

    @abstractmethod
    async def list(self, collection: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Lists documents in a collection."""
        pass
