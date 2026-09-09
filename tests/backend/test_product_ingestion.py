import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

backend_dir = Path(__file__).resolve().parent.parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.main import app
from app.repositories.firestore import firestore_repository
from app.services.product_ingestion import normalize_product_item, product_ingestion_service
from app.services.product_client import product_client
from app.models.enums import ContentType, SourceStatus

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_in_memory_firestore(monkeypatch):
    """Provides an in-memory dictionary backing firestore_repository for Product tests."""
    mock_db = {}

    async def mock_create(collection: str, doc_id: str, data: dict):
        key = f"{collection}/{doc_id}"
        stored = {**data, "_id": doc_id, "id": doc_id}
        mock_db[key] = stored
        return stored

    async def mock_get(collection: str, doc_id: str):
        return mock_db.get(f"{collection}/{doc_id}")

    async def mock_update(collection: str, doc_id: str, data: dict):
        key = f"{collection}/{doc_id}"
        if key not in mock_db:
            return None
        mock_db[key].update(data)
        return mock_db[key]

    async def mock_delete(collection: str, doc_id: str):
        key = f"{collection}/{doc_id}"
        if key in mock_db:
            del mock_db[key]
            return True
        return False

    async def mock_list(collection: str, limit: int = 50):
        prefix = f"{collection}/"
        return [v for k, v in mock_db.items() if k.startswith(prefix)]

    monkeypatch.setattr(firestore_repository, "create", mock_create)
    monkeypatch.setattr(firestore_repository, "get", mock_get)
    monkeypatch.setattr(firestore_repository, "update", mock_update)
    monkeypatch.setattr(firestore_repository, "delete", mock_delete)
    monkeypatch.setattr(firestore_repository, "list", mock_list)


def test_create_and_prevent_duplicate_product_source():
    """13.01, 13.02: Tests registering product source and rejecting duplicates."""
    source_payload = {
        "catalog_url": "test://centaur-forge-catalog",
        "name": "Centaur Forge",
        "platform": "vendor",
        "categories": ["tools", "anvils"],
    }
    resp = client.post("/api/v1/products/sources", json=source_payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Centaur Forge"
    assert data["platform"] == "vendor"
    assert data["id"].startswith("psrc_")

    # Duplicate rejected
    dup_resp = client.post("/api/v1/products/sources", json=source_payload)
    assert dup_resp.status_code == 400
    assert "already" in dup_resp.json()["error"]["message"].lower()


def test_normalize_product_item():
    """13.04: Tests mapping raw tool metadata into ContentEnvelope."""
    raw = {
        "sku": "ANV-TEST-100",
        "title": "100 lb Cast Steel Anvil",
        "platform": "ForgeWorks",
        "price": 499.00,
        "currency": "USD",
        "purchase_url": "https://forgeworks.com/anvils/100lb",
        "pros": ["True 55 HRC face", "Sharp hardy hole"],
        "cons": ["Heavy shipping weight"],
        "beginner_suitable": True,
        "alternatives": ["66lb model"],
        "affiliate": False,
    }
    envelope = normalize_product_item(raw, "psrc_forgeworks", "ForgeWorks")
    assert envelope.type == ContentType.PRODUCT
    assert envelope.title == "100 lb Cast Steel Anvil"
    assert envelope.metadata["sku"] == "ANV-TEST-100"
    assert envelope.metadata["price"] == 499.00
    assert envelope.metadata["currency"] == "USD"
    assert envelope.metadata["beginner_suitable"] is True
    assert "anvil" in envelope.tags


def test_sync_product_source_and_deduplication():
    """13.05, 13.10: Tests syncing product catalog, storing items, and deduplicating second run."""
    create_resp = client.post(
        "/api/v1/products/sources",
        json={"catalog_url": "test://tools-catalog", "name": "Tools Catalog"},
    )
    assert create_resp.status_code == 201
    src_id = create_resp.json()["id"]

    # First sync
    sync_resp = client.post(f"/api/v1/products/sources/{src_id}/sync")
    assert sync_resp.status_code == 200
    summary = sync_resp.json()
    assert summary["status"] == "SUCCESS"
    assert summary["new_items"] > 0
    assert summary["duplicates"] == 0
    initial_items = summary["new_items"]

    # Verify source item_count
    src_check = client.get(f"/api/v1/products/sources/{src_id}")
    assert src_check.json()["item_count"] == initial_items
    assert src_check.json()["status"] == SourceStatus.HEALTHY.value

    # Second sync -> zero new items, all duplicates
    sync_resp_2 = client.post(f"/api/v1/products/sources/{src_id}/sync")
    assert sync_resp_2.status_code == 200
    summary_2 = sync_resp_2.json()
    assert summary_2["new_items"] == 0
    assert summary_2["duplicates"] == initial_items


def test_dynamic_price_update(monkeypatch):
    """13.06: Tests price update without duplicating catalog documents."""
    # Register and initial sync
    client.post(
        "/api/v1/products/sources",
        json={"catalog_url": "test://price-test-source", "name": "Price Test Vendor"},
    )
    client.post("/api/v1/products/sources/psrc_price-test-source/sync")

    # Mock catalog returns updated price for 66lb anvil ($389 -> $449)
    async def mock_catalog_with_price_hike(catalog_url, max_items=50):
        base = product_client._generate_offline_mock_catalog(catalog_url)
        base["products"][0]["price"] = 449.00
        return base

    monkeypatch.setattr(product_client, "fetch_catalog", mock_catalog_with_price_hike)

    # Sync again
    sync_resp = client.post("/api/v1/products/sources/psrc_price-test-source/sync")
    assert sync_resp.status_code == 200
    summary = sync_resp.json()
    assert summary["price_updates"] == 1
    assert summary["new_items"] == 0

    # Verify updated price on item
    prod_resp = client.get("/api/v1/products/prod_centaurforge_fc-anv-66kg")
    assert prod_resp.status_code == 200
    assert prod_resp.json()["metadata"]["price"] == 449.00


def test_commercial_bias_check_and_filtering():
    """
    13.08, 13.09:
    Verifies transparent, non-commercial sorting (price/title) and beginner-suitable filtering.
    Affiliate tools are not artificially promoted over non-affiliate tools.
    """
    client.post(
        "/api/v1/products/sources",
        json={"catalog_url": "test://bias-check", "name": "Bias Check Vendor"},
    )
    client.post("/api/v1/products/sources/psrc_bias-check/sync")

    # List products
    resp = client.get("/api/v1/products")
    assert resp.status_code == 200
    products = resp.json()["products"]
    assert len(products) >= 3

    # Check ordering is strictly ascending by price, regardless of affiliate status
    prices = [p["metadata"]["price"] for p in products]
    assert prices == sorted(prices)

    # Test beginner_only filter
    beg_resp = client.get("/api/v1/products?beginner_only=true")
    assert beg_resp.status_code == 200
    beg_prods = beg_resp.json()["products"]
    for p in beg_prods:
        assert p["metadata"]["beginner_suitable"] is True

    # Test max_price filter
    max_resp = client.get("/api/v1/products?max_price=300")
    assert max_resp.status_code == 200
    for p in max_resp.json()["products"]:
        assert p["metadata"]["price"] <= 300.0


def test_sync_all_product_sources():
    """13.10: Tests batch sync across all enabled product sources."""
    client.post(
        "/api/v1/products/sources",
        json={"catalog_url": "test://vendor-a", "name": "Vendor A"},
    )
    client.post(
        "/api/v1/products/sources",
        json={"catalog_url": "test://vendor-b", "name": "Vendor B"},
    )

    resp = client.post("/api/v1/products/sync")
    assert resp.status_code == 200
    summaries = resp.json()
    assert len(summaries) >= 2
    assert all(s["status"] == "SUCCESS" for s in summaries)
