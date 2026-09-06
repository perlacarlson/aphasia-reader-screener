"""
ARASAAC REST Client & Local Image Cache
Department of Speech & Hearing Sciences | Portland State University
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

BASE_API_URL = "https://api.arasaac.org/api/pictograms"
STATIC_CDN_URL = "https://static.arasaac.org/pictograms"
CACHE_DIR = os.path.join("output", "assets", "pictograms")

# Clinically verified ARASAAC IDs for Jack London's "To Build a Fire"
VERIFIED_ARASAAC_IDS = {
    "pine_forest": 3246,     # Pinar / Pine forest
    "clock": 2487,           # Reloj / Clock
    "extreme_cold": 5453,    # Mucho frío / Extreme cold
    "husky_wolf_dog": 2838,  # Lobo / Wolf
    "fire": 2341,            # Fuego / Fire
    "boots": 2494,           # Botas / Boots (replaces broken 24174)
    "danger": 25315          # Peligro / Danger
}

def fetch_arasaac_id_by_keyword(keyword: str, locale: str = "en") -> Optional[int]:
    """Queries ARASAAC REST API for top matching pictogram ID."""
    encoded_query = urllib.parse.quote(keyword)
    url = f"{BASE_API_URL}/{locale}/search/{encoded_query}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "PSU-AphasiaReader/1.0 (Speech & Hearing Sciences)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                if data and len(data) > 0:
                    return data[0]["_id"]
    except (urllib.error.URLError, TimeoutError, KeyError, json.JSONDecodeError):
        pass
    return None

def download_arasaac_image(pictogram_id: int) -> str:
    """
    Downloads the 300px transparent PNG from ARASAAC static CDN,
    caches it locally, and returns the relative asset path.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    local_filename = f"{pictogram_id}.png"
    local_filepath = os.path.join(CACHE_DIR, local_filename)
    relative_web_path = f"assets/pictograms/{local_filename}"

    if os.path.exists(local_filepath) and os.path.getsize(local_filepath) > 0:
        return relative_web_path

    # ARASAAC CDN stores transparent raster assets at {id}/{id}_300.png
    cdn_url = f"{STATIC_CDN_URL}/{pictogram_id}/{pictogram_id}_300.png"
    req = urllib.request.Request(
        cdn_url,
        headers={"User-Agent": "PSU-AphasiaReader/1.0 (Speech & Hearing Sciences)"}
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                with open(local_filepath, "wb") as f:
                    f.write(response.read())
                print(f"  ✓ Cached ARASAAC asset: ID {pictogram_id} -> {local_filepath}")
                return relative_web_path
    except (urllib.error.URLError, TimeoutError) as err:
        print(f"  [!] CDN download failed for ID {pictogram_id} ({err}). Using CDN fallback.")

    return cdn_url

def resolve_anchor_visual(concept_key: str, fallback_emoji: str = "🌲") -> str:
    """Returns local cached image tag or fallback emoji markup."""
    picto_id = VERIFIED_ARASAAC_IDS.get(concept_key)
    if not picto_id:
        picto_id = fetch_arasaac_id_by_keyword(concept_key.replace("_", " "))

    if picto_id:
        img_src = download_arasaac_image(picto_id)
        return f'<img src="{img_src}" alt="{concept_key}" class="arasaac-icon" loading="lazy" />'

    return fallback_emoji