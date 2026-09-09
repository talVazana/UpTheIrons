import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

backend_dir = Path(__file__).resolve().parent.parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.main import app
from app.repositories.firestore import firestore_repository
from app.services.rss_client import rss_client
from app.services.rss_ingestion import normalize_rss_article
from app.models.enums import ContentType, SourceStatus

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_in_memory_firestore(monkeypatch):
    """Provides an in-memory dictionary backing firestore_repository for RSS API tests."""
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


def test_create_and_prevent_duplicate_rss_feed():
    """12.01, 12.02: Tests registering RSS feed and rejecting duplicates."""
    feed_payload = {
        "url": "https://www.metalsmiths.org/feed.xml",
        "name": "Guild of Metalsmiths",
        "priority": 10,
        "categories": ["blacksmithing", "materials"],
    }
    resp = client.post("/api/v1/rss/feeds", json=feed_payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Guild of Metalsmiths"
    assert data["platform"] == "rss"
    assert data["id"].startswith("rss_")

    # Duplicate registration by URL must be rejected
    dup_resp = client.post("/api/v1/rss/feeds", json=feed_payload)
    assert dup_resp.status_code == 400
    assert "already" in dup_resp.json()["error"]["message"].lower()


def test_reject_invalid_rss_url():
    """12.02: Tests rejection of non-http/https feed URLs."""
    resp = client.post("/api/v1/rss/feeds", json={"url": "ftp://invalid-feed.org/rss"})
    assert resp.status_code == 400
    assert "http" in resp.json()["error"]["message"].lower()


def test_rss2_xml_parser():
    """12.04: Tests RSS 2.0 XML parsing with standard library parser."""
    sample_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
      <channel>
        <title>Blacksmithing Journal</title>
        <link>https://example.com/journal</link>
        <item>
          <title>Heat Treating 1084 &amp; 1095</title>
          <link>https://example.com/journal/heat-treating</link>
          <description>&lt;p&gt;Crucial rules for hardening high carbon blades.&lt;/p&gt;</description>
          <pubDate>Mon, 08 Sep 2026 10:00:00 GMT</pubDate>
          <author>Master Smith</author>
        </item>
      </channel>
    </rss>
    """
    res = rss_client.parse_feed_xml(sample_xml, "https://example.com/feed.xml")
    assert res["feed_title"] == "Blacksmithing Journal"
    assert res["feed_format"] == "rss"
    assert len(res["articles"]) == 1
    art = res["articles"][0]
    assert art["title"] == "Heat Treating 1084 & 1095"
    assert art["url"] == "https://example.com/journal/heat-treating"
    assert art["summary"] == "Crucial rules for hardening high carbon blades."
    assert art["author"] == "Master Smith"


def test_atom_xml_parser():
    """12.04: Tests Atom XML parsing."""
    sample_atom = """<?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
      <title>Anvil &amp; Blade Atom Feed</title>
      <link href="https://example.com/atom" rel="self"/>
      <entry>
        <title>Dressing Your Anvil Face</title>
        <link href="https://example.com/articles/dressing-anvil" rel="alternate"/>
        <id>urn:uuid:12345-67890</id>
        <updated>2026-09-07T14:30:00Z</updated>
        <summary>How to dress edges with a flap disc without losing hardness.</summary>
        <author><name>Old Smith</name></author>
      </entry>
    </feed>
    """
    res = rss_client.parse_feed_xml(sample_atom, "https://example.com/atom.xml")
    assert res["feed_title"] == "Anvil & Blade Atom Feed"
    assert res["feed_format"] == "atom"
    assert len(res["articles"]) == 1
    art = res["articles"][0]
    assert art["title"] == "Dressing Your Anvil Face"
    assert art["url"] == "https://example.com/articles/dressing-anvil"
    assert art["author"] == "Old Smith"


def test_normalize_rss_article():
    """12.05, 12.11: Tests normalization to ContentEnvelope and source attribution."""
    raw = {
        "title": "Choosing Between 5160 and 1084 for Apprentice Knives",
        "url": "https://example.com/knife-steels",
        "summary": "Deep dive into alloy metallurgy, grain size, and quenching media.",
        "published_at": "2026-09-08T10:00:00Z",
        "author": "Dr. Vance",
    }
    envelope = normalize_rss_article(raw, "rss_metalsmiths", "Guild of Metalsmiths")
    assert envelope.type == ContentType.ARTICLE
    assert envelope.source.source_type == "rss_feed"
    assert envelope.source.source_name == "Guild of Metalsmiths"
    assert envelope.source.source_url == "https://example.com/knife-steels"
    assert envelope.metadata["author"] == "Dr. Vance"
    assert "steel" in envelope.tags or "bladesmithing" in envelope.tags


def test_sync_rss_feed_and_deduplication():
    """12.06, 12.07, 12.09: Tests feed sync, document storage, and deduplication on re-sync."""
    create_resp = client.post(
        "/api/v1/rss/feeds",
        json={"url": "test://metalsmiths-journal", "name": "Metalsmiths Journal"},
    )
    assert create_resp.status_code == 201
    feed_id = create_resp.json()["id"]

    # First sync
    sync_resp = client.post(f"/api/v1/rss/feeds/{feed_id}/sync")
    assert sync_resp.status_code == 200
    summary = sync_resp.json()
    assert summary["status"] == "SUCCESS"
    assert summary["new_items"] > 0
    assert summary["duplicates"] == 0
    first_count = summary["new_items"]

    # Verify feed article_count in registry
    feed_check = client.get(f"/api/v1/rss/feeds/{feed_id}")
    assert feed_check.json()["article_count"] == first_count
    assert feed_check.json()["status"] == SourceStatus.HEALTHY.value

    # Second sync -> verifies deduplication (zero new items)
    sync_resp_2 = client.post(f"/api/v1/rss/feeds/{feed_id}/sync")
    assert sync_resp_2.status_code == 200
    summary_2 = sync_resp_2.json()
    assert summary_2["new_items"] == 0
    assert summary_2["duplicates"] == first_count


def test_articles_feed_api():
    """12.08: Tests querying articles feed endpoint."""
    # Register and sync feed
    client.post(
        "/api/v1/rss/feeds",
        json={"url": "test://anvil-weekly", "name": "Anvil Weekly"},
    )
    client.post("/api/v1/rss/feeds/rss_anvil-weekly/sync")

    # List articles
    resp = client.get("/api/v1/articles")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] > 0
    assert len(data["articles"]) > 0

    first_article = data["articles"][0]
    art_id = first_article["id"]

    # Get single article
    single_resp = client.get(f"/api/v1/articles/{art_id}")
    assert single_resp.status_code == 200
    assert single_resp.json()["id"] == art_id


def test_disabled_rss_feed_cannot_sync():
    """12.09: Tests disabled RSS feeds cannot be synced."""
    create_resp = client.post(
        "/api/v1/rss/feeds",
        json={"url": "test://inactive-feed", "name": "Inactive Feed"},
    )
    feed_id = create_resp.json()["id"]

    # Disable feed
    client.patch(f"/api/v1/rss/feeds/{feed_id}", json={"enabled": False})

    # Attempt sync
    sync_resp = client.post(f"/api/v1/rss/feeds/{feed_id}/sync")
    assert sync_resp.status_code == 400
    assert "disabled" in sync_resp.json()["error"]["message"].lower()


def test_anti_crawling_boundary():
    """12.13: Explicit test verifying zero outbound link following during feed processing."""
    xml_with_outbound_links = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
      <channel>
        <title>Isolated Feed</title>
        <link>https://isolated.org</link>
        <item>
          <title>Article with External Links</title>
          <link>https://isolated.org/post-1</link>
          <description>Check out &lt;a href="https://arbitrary-spidered-site.com/deep/page"&gt;this link&lt;/a&gt; and &lt;a href="https://spam.com"&gt;that&lt;/a&gt;.</description>
          <pubDate>Mon, 08 Sep 2026 10:00:00 GMT</pubDate>
        </item>
      </channel>
    </rss>
    """
    res = rss_client.parse_feed_xml(xml_with_outbound_links, "https://isolated.org/feed.xml")
    # Verified only the 1 item from XML is parsed; external links in body are stripped to text
    assert len(res["articles"]) == 1
    assert res["articles"][0]["url"] == "https://isolated.org/post-1"
    assert "arbitrary-spidered-site" not in res["articles"][0]["url"]
    assert "Check out this link and that." == res["articles"][0]["summary"]
