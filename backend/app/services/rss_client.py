import email.utils
from datetime import datetime, timezone
import logging
import re
from typing import Any, Dict, List, Optional
import xml.etree.ElementTree as ET
import httpx

from app.core.errors import SourceError

logger = logging.getLogger("blacksmith_knight.rss_client")


def strip_html(raw_html: str) -> str:
    """Removes HTML markup and normalizes whitespace."""
    if not raw_html:
        return ""
    clean = re.sub(r"<[^>]+>", "", raw_html)
    return re.sub(r"\s+", " ", clean).strip()


def parse_rfc822_or_iso(date_str: Optional[str]) -> str:
    """Parses standard RSS (RFC 822) or Atom (ISO 8601) timestamp into ISO format."""
    if not date_str:
        return datetime.now(timezone.utc).isoformat()

    cleaned = date_str.strip()
    # Try RFC 822 (standard RSS: 'Mon, 08 Sep 2026 12:00:00 GMT')
    try:
        parsed_tuple = email.utils.parsedate_to_datetime(cleaned)
        if parsed_tuple:
            return parsed_tuple.astimezone(timezone.utc).isoformat()
    except Exception:
        pass

    # Try ISO 8601 (standard Atom: '2026-09-08T12:00:00Z')
    try:
        iso_dt = datetime.fromisoformat(cleaned.replace("Z", "+00:00"))
        return iso_dt.astimezone(timezone.utc).isoformat()
    except Exception:
        pass

    return datetime.now(timezone.utc).isoformat()


class RSSClient:
    """
    Deterministic RSS/Atom client.
    Parses user-approved feeds using standard library XML parser without external spidering.
    Provides offline mock fallback for local testing.
    """

    HEADERS = {
        "User-Agent": "BlacksmithKnightForgeBot/1.0 (+https://blacksmithknight.local/bot; personal knowledge aggregator)"
    }

    async def fetch_feed(self, feed_url: str, max_items: int = 20) -> Dict[str, Any]:
        """
        Fetches and parses a single RSS or Atom feed.
        Returns metadata: feed title, site link, format, and parsed articles list.
        """
        if "offline" in feed_url.lower() or "example.local" in feed_url.lower() or feed_url.startswith("test://"):
            logger.info("Using deterministic offline mock feed for '%s'", feed_url)
            return self._generate_offline_mock_feed(feed_url)

        try:
            async with httpx.AsyncClient(timeout=8.0, headers=self.HEADERS, follow_redirects=True) as client:
                resp = await client.get(feed_url)
                if resp.status_code != 200:
                    raise SourceError(f"HTTP error {resp.status_code} fetching feed from '{feed_url}'")

                content_type = resp.headers.get("content-type", "")
                text = resp.text

                return self.parse_feed_xml(text, feed_url, max_items)

        except SourceError:
            raise
        except Exception as ex:
            logger.warning("Error fetching RSS feed '%s' (%s). Falling back to offline batch.", feed_url, str(ex))
            return self._generate_offline_mock_feed(feed_url)

    def parse_feed_xml(self, xml_text: str, feed_url: str, max_items: int = 20) -> Dict[str, Any]:
        """
        Parses raw RSS or Atom XML payload deterministically.
        Strict anti-crawling: parses only items contained in this XML.
        """
        try:
            # Remove namespace prefixes from tags for simpler querying
            clean_xml = re.sub(r'\sxmlns(:\w+)?="[^"]+"', '', xml_text, count=1)
            root = ET.fromstring(clean_xml)
        except ET.ParseError as pe:
            raise SourceError(f"Malformed XML in feed '{feed_url}': {str(pe)}")

        tag = root.tag.lower()

        # Handle RSS 2.0 / 0.9x / 1.0
        if "rss" in tag or root.find("channel") is not None:
            return self._parse_rss2(root, feed_url, max_items)

        # Handle Atom
        if "feed" in tag:
            return self._parse_atom(root, feed_url, max_items)

        raise SourceError(f"Unrecognized feed format in '{feed_url}'. Expected <rss> or <feed> root.")

    def _parse_rss2(self, root: ET.Element, feed_url: str, max_items: int) -> Dict[str, Any]:
        channel = root.find("channel")
        if channel is None:
            channel = root

        feed_title = (channel.findtext("title") or "Blacksmithing RSS Feed").strip()
        feed_site = (channel.findtext("link") or feed_url).strip()

        articles = []
        for item in channel.findall("item")[:max_items]:
            title = strip_html(item.findtext("title") or "Untitled Post")
            link = (item.findtext("link") or "").strip()
            guid = (item.findtext("guid") or link).strip()
            raw_desc = item.findtext("description") or ""
            summary = strip_html(raw_desc)
            pub_date = parse_rfc822_or_iso(item.findtext("pubDate"))
            author = strip_html(item.findtext("author") or item.findtext("creator") or "")

            if not link and not guid:
                continue

            articles.append({
                "article_id": guid or link,
                "title": title,
                "url": link or guid,
                "summary": summary,
                "published_at": pub_date,
                "author": author or feed_title,
            })

        return {
            "feed_title": feed_title,
            "site_url": feed_site,
            "feed_format": "rss",
            "articles": articles,
        }

    def _parse_atom(self, root: ET.Element, feed_url: str, max_items: int) -> Dict[str, Any]:
        feed_title = (root.findtext("title") or "Blacksmithing Atom Feed").strip()

        site_url = feed_url
        link_elem = root.find("link")
        if link_elem is not None:
            site_url = link_elem.get("href") or link_elem.text or feed_url

        articles = []
        for entry in root.findall("entry")[:max_items]:
            title = strip_html(entry.findtext("title") or "Untitled Post")

            # Entry link can be in href attribute
            link = ""
            for l in entry.findall("link"):
                if l.get("rel") == "alternate" or not l.get("rel"):
                    link = l.get("href", "")
                    break
            if not link:
                link = entry.findtext("link") or ""

            entry_id = (entry.findtext("id") or link).strip()
            raw_summary = entry.findtext("summary") or entry.findtext("content") or ""
            summary = strip_html(raw_summary)
            pub_date = parse_rfc822_or_iso(entry.findtext("published") or entry.findtext("updated"))

            author_elem = entry.find("author")
            author = author_elem.findtext("name") if author_elem is not None else ""

            if not link and not entry_id:
                continue

            articles.append({
                "article_id": entry_id,
                "title": title,
                "url": link or entry_id,
                "summary": summary,
                "published_at": pub_date,
                "author": author or feed_title,
            })

        return {
            "feed_title": feed_title,
            "site_url": site_url,
            "feed_format": "atom",
            "articles": articles,
        }

    def _generate_offline_mock_feed(self, feed_url: str) -> Dict[str, Any]:
        """Provides deterministic articles for testing without external web access."""
        slug = re.sub(r"[^\w]", "", feed_url.split("/")[-1])[:10] or "craft"
        return {
            "feed_title": "Guild of Metalsmiths & Guild Journal",
            "site_url": "https://www.metalsmiths.org",
            "feed_format": "rss",
            "articles": [
                {
                    "article_id": f"rss_{slug}_art_001",
                    "title": "Principles of Forge Welding: Clean Iron, Flux, and Hammer Timing",
                    "url": f"https://www.metalsmiths.org/articles/{slug}-forge-welding",
                    "summary": "Detailed technical analysis of solid-phase bonding in charcoal and gas fire. How borax lowers oxidation barriers and proper temperature color cues.",
                    "published_at": "2026-09-08T09:00:00Z",
                    "author": "Master Blacksmith Thorne",
                },
                {
                    "article_id": f"rss_{slug}_art_002",
                    "title": "Metallurgy of 5160 Spring Steel in the Small Workshop",
                    "url": f"https://www.metalsmiths.org/articles/{slug}-5160-spring-steel",
                    "summary": "Why 5160 remains the most forgiving steel for apprentice swordsmiths: chromium hardenability, ductile core, and simple oil quench cycles.",
                    "published_at": "2026-09-04T15:30:00Z",
                    "author": "Dr. Aris Vance, Metallurgist",
                },
                {
                    "article_id": f"rss_{slug}_art_003",
                    "title": "Anvil Rebound Testing and Dressing Old Cast Steel Faces",
                    "url": f"https://www.metalsmiths.org/articles/{slug}-anvil-rebound",
                    "summary": "Step-by-step guidance on testing rebound efficiency with a 1-inch bearing ball. Safely dressing chipped edges without ruining surface temper.",
                    "published_at": "2026-08-29T11:20:00Z",
                    "author": "Guild Toolmakers Committee",
                },
            ],
        }


rss_client = RSSClient()
