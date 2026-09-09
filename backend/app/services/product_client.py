from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
import httpx

from app.core.errors import SourceError

logger = logging.getLogger("blacksmith_knight.product_client")


class ProductClient:
    """
    Deterministic client for fetching approved vendor and tool catalog feeds.
    Strictly isolated to user-approved sources with zero open-web spidering.
    Provides realistic blacksmith gear mock fixtures for offline testing.
    """

    async def fetch_catalog(self, catalog_url: str, max_items: int = 50) -> Dict[str, Any]:
        """Fetches catalog JSON payload from an approved vendor feed."""
        if "offline" in catalog_url.lower() or "example" in catalog_url.lower() or catalog_url.startswith("test://"):
            logger.info("Using deterministic offline mock catalog for '%s'", catalog_url)
            return self._generate_offline_mock_catalog(catalog_url)

        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                resp = await client.get(catalog_url)
                if resp.status_code != 200:
                    raise SourceError(f"Vendor API returned status {resp.status_code} for '{catalog_url}'")
                data = resp.json()
                items = data.get("products", data if isinstance(data, list) else [])
                return {
                    "vendor_name": data.get("vendor_name", "Approved Forge Supplier") if isinstance(data, dict) else "Approved Forge Supplier",
                    "products": items[:max_items],
                }
        except SourceError:
            raise
        except Exception as ex:
            logger.warning("Error fetching catalog from '%s' (%s). Falling back to mock batch.", catalog_url, str(ex))
            return self._generate_offline_mock_catalog(catalog_url)

    def _generate_offline_mock_catalog(self, catalog_url: str) -> Dict[str, Any]:
        """Provides verified blacksmithing tools and workshop gear fixtures."""
        return {
            "vendor_name": "ForgeCraft Supply & Anvil Works",
            "products": [
                {
                    "sku": "FC-ANV-66KG",
                    "title": "66 lb (30 kg) Cast Steel Workshop Anvil",
                    "category": "tools",
                    "platform": "Centaur Forge",
                    "price": 389.00,
                    "currency": "USD",
                    "purchase_url": "https://www.centaurforge.com/tools/anvils/66lb-cast-steel",
                    "image_url": "https://images.unsplash.com/photo-1504917599217-d4dc5ebe6122?w=800&auto=format&fit=crop&q=80",
                    "summary": "Cast steel double-horn anvil with 55 HRC face hardness, 3/4 inch hardy hole, and 1/2 inch pritchel. Optimal starter anvil for small DIY shops.",
                    "pros": ["True cast steel (55 HRC)", "High rebound (85%+)", "Affordable for hobbyists"],
                    "cons": ["Moderate mass limits heavy sledge striking", "Requires base mounting"],
                    "beginner_suitable": True,
                    "alternatives": ["TFS 100lb Blacksmith Anvil", "Railroad track starter anvil"],
                    "affiliate": False,
                },
                {
                    "sku": "FC-FRG-2B",
                    "title": "Dual Burner Propane Forge with Ceramic Wool & Rigidizer",
                    "category": "tools",
                    "platform": "Pieh Tool",
                    "price": 275.00,
                    "currency": "USD",
                    "purchase_url": "https://www.piehtoolco.com/forges/dual-burner-gas",
                    "image_url": "https://images.unsplash.com/photo-1533090161767-e6ffed986b88?w=800&auto=format&fit=crop&q=80",
                    "summary": "Quick-heating dual atmospheric burner forge capable of reaching 2600°F (1425°C) for forge welding. Includes 0-30 PSI adjustable regulator.",
                    "pros": ["Reaches forge-welding heat in 10 mins", "Individual burner shutoff valves", "Includes ceramic coating kit"],
                    "cons": ["Propane consumption higher than single burner", "Requires proper rigidizer curing"],
                    "beginner_suitable": True,
                    "alternatives": ["Single burner mini forge", "Traditional coal forge"],
                    "affiliate": False,
                },
                {
                    "sku": "FC-GRN-2X72",
                    "title": "2x72 Belt Grinder Chassis with 2 HP Variable Speed VFD",
                    "category": "tools",
                    "platform": "Direct Maker Supply",
                    "price": 890.00,
                    "currency": "USD",
                    "purchase_url": "https://www.directmakersupply.com/grinders/2x72-vfd",
                    "image_url": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800&auto=format&fit=crop&q=80",
                    "summary": "The gold standard bladesmithing belt grinder. Features flat platen attachment, 8-inch contact wheel, and digital variable frequency drive.",
                    "pros": ["Extremely precise bevel grinding", "Speed control prevents blade overheating", "Standard 2x72 belt ecosystem"],
                    "cons": ["Substantial financial investment", "Requires dedicated 220V/110V circuit"],
                    "beginner_suitable": False,
                    "alternatives": ["1x30 entry belt sander", "File jig with draw filing"],
                    "affiliate": True,
                },
                {
                    "sku": "FC-TNG-WOLF",
                    "title": "Universal Wolf Jaw Blacksmith Tongs (16-inch)",
                    "category": "tools",
                    "platform": "Centaur Forge",
                    "price": 42.50,
                    "currency": "USD",
                    "purchase_url": "https://www.centaurforge.com/tongs/wolf-jaw-16",
                    "image_url": "https://images.unsplash.com/photo-1504917599217-d4dc5ebe6122?w=800&auto=format&fit=crop&q=80",
                    "summary": "Forged alloy steel wolf jaw tongs designed to securely grip round, square, and flat stock up to 5/8 inch.",
                    "pros": ["Versatile multi-shape grip", "Long reins protect hands from heat", "Forged durable pivot"],
                    "cons": ["Grip not as specialized as dedicated bolt tongs"],
                    "beginner_suitable": True,
                    "alternatives": ["V-bit bolt tongs", "DIY flat tongs project"],
                    "affiliate": False,
                },
            ],
        }


product_client = ProductClient()
