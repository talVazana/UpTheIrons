from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
import httpx

from app.api.v1.settings import get_effective_youtube_api_key
from app.core.errors import SourceError

logger = logging.getLogger("blacksmith_knight.youtube_client")


class YouTubeClient:
    """
    Deterministic YouTube API client.
    Uses quota-efficient playlistItems API (1 unit per page vs 100 units for search).
    Falls back gracefully to deterministic offline fixtures when no API key is set.
    """

    BASE_URL = "https://www.googleapis.com/youtube/v3"

    @staticmethod
    def channel_id_to_uploads_playlist(channel_id: str) -> Optional[str]:
        """Converts channel ID (UC...) to its public uploads playlist ID (UU...)."""
        if channel_id and channel_id.startswith("UC") and len(channel_id) >= 20:
            return "UU" + channel_id[2:]
        return None

    async def fetch_channel_videos(
        self,
        channel_id: str,
        channel_name: str = "Unknown Channel",
        max_results: int = 15,
    ) -> List[Dict[str, Any]]:
        """
        Fetches the latest videos from a YouTube channel.
        Returns a list of normalized raw video payload dictionaries.
        """
        api_key = await get_effective_youtube_api_key()

        if not api_key:
            logger.info("No YouTube API key set. Returning deterministic offline video batch for %s", channel_id)
            return self._generate_offline_mock_videos(channel_id, channel_name)

        uploads_playlist_id = self.channel_id_to_uploads_playlist(channel_id)

        # If not standard UC ID, resolve uploads playlist from channels API
        if not uploads_playlist_id:
            uploads_playlist_id = await self._resolve_uploads_playlist(channel_id, api_key)

        if not uploads_playlist_id:
            logger.warning("Could not resolve uploads playlist for channel %s, using mock fallback", channel_id)
            return self._generate_offline_mock_videos(channel_id, channel_name)

        params = {
            "key": api_key,
            "playlistId": uploads_playlist_id,
            "part": "snippet,contentDetails",
            "maxResults": min(max_results, 50),
        }

        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                resp = await client.get(f"{self.BASE_URL}/playlistItems", params=params)

                if resp.status_code == 403:
                    error_data = resp.json().get("error", {})
                    reason = error_data.get("errors", [{}])[0].get("reason", "quotaExceeded")
                    logger.error("YouTube API quota/permission error: %s", reason)
                    raise SourceError(f"YouTube API quota or permission error: {reason}")

                if resp.status_code != 200:
                    logger.error("YouTube API returned status %s: %s", resp.status_code, resp.text)
                    raise SourceError(f"YouTube API returned error status {resp.status_code}")

                data = resp.json()
                items = data.get("items", [])
                parsed_videos = []

                for item in items:
                    snippet = item.get("snippet", {})
                    content_details = item.get("contentDetails", {})
                    video_id = content_details.get("videoId") or snippet.get("resourceId", {}).get("videoId")
                    if not video_id:
                        continue

                    thumbs = snippet.get("thumbnails", {})
                    thumbnail_url = (
                        thumbs.get("maxres", {}).get("url")
                        or thumbs.get("high", {}).get("url")
                        or thumbs.get("medium", {}).get("url")
                        or thumbs.get("default", {}).get("url")
                        or f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
                    )

                    parsed_videos.append({
                        "video_id": video_id,
                        "title": snippet.get("title", "Untitled Video"),
                        "description": snippet.get("description", ""),
                        "published_at": snippet.get("publishedAt", datetime.now(timezone.utc).isoformat()),
                        "channel_id": channel_id,
                        "channel_name": snippet.get("channelTitle", channel_name),
                        "thumbnail_url": thumbnail_url,
                        "duration_seconds": 0,
                    })

                logger.info("Fetched %d videos from YouTube API for channel %s", len(parsed_videos), channel_id)
                return parsed_videos

        except SourceError:
            raise
        except Exception as ex:
            logger.warning("Error querying YouTube API for channel %s (%s). Falling back to offline batch.", channel_id, str(ex))
            return self._generate_offline_mock_videos(channel_id, channel_name)

    async def fetch_video_details(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Fetches metadata for a single YouTube video by ID."""
        api_key = await get_effective_youtube_api_key()
        if api_key:
            params = {
                "key": api_key,
                "id": video_id,
                "part": "snippet,contentDetails",
            }
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    resp = await client.get(f"{self.BASE_URL}/videos", params=params)
                    if resp.status_code == 200:
                        items = resp.json().get("items", [])
                        if items:
                            snippet = items[0].get("snippet", {})
                            return {
                                "title": snippet.get("title", f"Direct Video: {video_id}"),
                                "description": snippet.get("description", "Added directly by Admin."),
                            }
            except Exception as ex:
                logger.debug("Failed fetching API details for video %s: %s", video_id, str(ex))

        # Fallback to oEmbed if no API key or API fails
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
                resp = await client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    return {
                        "title": data.get("title", f"Direct Video: {video_id}"),
                        "description": f"Video by {data.get('author_name', 'YouTube Creator')}.",
                    }
        except Exception as ex:
            logger.debug("Failed oEmbed fallback for video %s: %s", video_id, str(ex))

        return None

    async def _resolve_uploads_playlist(self, channel_identifier: str, api_key: str) -> Optional[str]:
        """Resolves the uploads playlist ID by querying the channels resource."""
        params = {"key": api_key, "part": "contentDetails"}
        if channel_identifier.startswith("UC"):
            params["id"] = channel_identifier
        elif channel_identifier.startswith("@"):
            params["forHandle"] = channel_identifier
        else:
            params["forUsername"] = channel_identifier

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(f"{self.BASE_URL}/channels", params=params)
                if resp.status_code == 200:
                    items = resp.json().get("items", [])
                    if items:
                        return items[0].get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")
        except Exception as ex:
            logger.debug("Failed resolving uploads playlist for %s: %s", channel_identifier, str(ex))
        return None

    def _generate_offline_mock_videos(self, channel_id: str, channel_name: str) -> List[Dict[str, Any]]:
        """Generates realistic offline mock videos for local testing without internet/API keys."""
        prefix = channel_id.replace("UC", "").replace("yt_", "")[:6]
        return [
            {
                "video_id": f"{prefix}_vid_001",
                "title": f"Forging a Traditional Anvil Hardy Tool | {channel_name}",
                "description": "Step-by-step master tutorial forging a hot cut hardy tool from high carbon 1045 steel. Learn taper forging and proper hammer angles.",
                "published_at": "2026-09-08T14:00:00Z",
                "channel_id": channel_id,
                "channel_name": channel_name,
                "thumbnail_url": f"https://images.unsplash.com/photo-1504917599217-d4dc5ebe6122?w=800&auto=format&fit=crop&q=80",
                "duration_seconds": 920,
            },
            {
                "video_id": f"{prefix}_vid_002",
                "title": f"Heat Treatment Mastery: 1084 & 1095 Knife Steel | {channel_name}",
                "description": "Crucial metallurgical secrets of normalizing, grain refinement, and canola vs parks 50 oil quenching for high carbon blades.",
                "published_at": "2026-09-05T18:30:00Z",
                "channel_id": channel_id,
                "channel_name": channel_name,
                "thumbnail_url": f"https://images.unsplash.com/photo-1533090161767-e6ffed986b88?w=800&auto=format&fit=crop&q=80",
                "duration_seconds": 1245,
            },
            {
                "video_id": f"{prefix}_vid_003",
                "title": f"Workshop Tong Making: Flat Jaw & Bolt Tongs | {channel_name}",
                "description": "Fundamental blacksmith skill: forging your own tongs from 1/2 inch mild steel bar. No expensive power hammer needed.",
                "published_at": "2026-09-01T10:15:00Z",
                "channel_id": channel_id,
                "channel_name": channel_name,
                "thumbnail_url": f"https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800&auto=format&fit=crop&q=80",
                "duration_seconds": 810,
            },
        ]


youtube_client = YouTubeClient()
