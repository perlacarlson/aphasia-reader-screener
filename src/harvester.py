# Gutendex API client & text cleaner
import os
import re
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import List, Dict, Tuple, Optional
from src.metrics import (
    calculate_fernandez_huerta,
    extract_dialogue_percentage,
    calculate_cognate_density
)

class GutenbergHarvester:
    BASE_URL = "https://gutendex.com/books/"

    def __init__(self, target_lang: str = "es", cache_dir: str = "data/raw_texts"):
        self.target_lang = target_lang
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
        self.session = self._build_resilient_session()

    def _build_resilient_session(self) -> requests.Session:
        """Configures a requests session with retries, exponential backoff, and polite headers."""
        session = requests.Session()
        retry_strategy = Retry(
            total=4,
            backoff_factor=2,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        session.headers.update({
            "User-Agent": "PSU-AphasiaProject-Research/1.0 (Academic Research; Speech & Hearing Sciences)"
        })
        return session

    def search_candidates(self, query: str, limit: int = 3) -> List[Dict]:
        """Queries Gutendex with a split connect/read timeout and error isolation."""
        try:
            res = self.session.get(
                self.BASE_URL,
                params={"languages": self.target_lang, "search": query},
                timeout=(10, 45)
            )
            res.raise_for_status()
            return res.json().get("results", [])[:limit]
        except requests.exceptions.RequestException as e:
            print(f"\n[Warning] Search query '{query}' failed after retries: {e}")
            return []

    def download_text(self, book_meta: Dict) -> Optional[str]:
        """
        Retrieves text from the local cache if available; 
        otherwise downloads from Gutenberg, strips headers, and saves to disk.
        """
        gid = book_meta.get("id")
        cache_path = os.path.join(self.cache_dir, f"{gid}.txt")

        # 1. Local Cache Check
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    print(f" -> [Cache Hit] Loaded Gutenberg #{gid} from disk.")
                    return f.read()
            except Exception as e:
                print(f" -> [Warning] Failed reading cached #{gid}: {e}. Re-downloading.")

        # 2. Remote Download
        formats = book_meta.get("formats", {})
        txt_url = formats.get("text/plain; charset=utf-8") or formats.get("text/plain")
        if not txt_url:
            return None

        try:
            print(f" -> [Downloading] Fetching Gutenberg #{gid} from {txt_url}...")
            res = self.session.get(txt_url, timeout=(10, 60))
            res.encoding = "utf-8"
            raw_text = res.text

            # Strip legal headers and footers
            start = re.search(r"\*\*\* START OF [^\n]*\*\*\*", raw_text, re.I)
            end = re.search(r"\*\*\* END OF [^\n]*\*\*\*", raw_text, re.I)
            start_idx = start.end() if start else 0
            end_idx = end.start() if end else len(raw_text)
            clean_text = raw_text[start_idx:end_idx].strip()

            # 3. Write to Disk
            with open(cache_path, "w", encoding="utf-8") as f:
                f.write(clean_text)
            print(f" -> [Cached] Saved Gutenberg #{gid} to '{cache_path}'.")

            return clean_text

        except requests.exceptions.RequestException as e:
            print(f"\n[Warning] Could not download text from {txt_url}: {e}")
            return None

    def split_into_stories(self, raw_text: str, default_title: str) -> List[Tuple[str, str]]:
        pattern = r"\n\s*\n\s*([A-ZÁÉÍÓÚÜÑ\s]{4,40})\s*\n\s*\n"
        splits = re.split(pattern, raw_text)
        if len(splits) > 2:
            stories = []
            for i in range(1, len(splits) - 1, 2):
                title = splits[i].strip()
                content = splits[i + 1].strip()
                if len(re.findall(r"\b\w+\b", content)) >= 200:
                    stories.append((title, content))
            if stories:
                return stories
        return [(default_title, raw_text)]

    def score_text(self, gutenberg_id: int, book_title: str, story_title: str, author: str, text: str) -> Dict:
        words = re.findall(r"\b[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]+\b", text)
        sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
        total_words = len(words)

        fh = calculate_fernandez_huerta(words, sentences)
        dial_pct = extract_dialogue_percentage(text, total_words)
        cognate_pct = calculate_cognate_density(words, total_words)

        reasons = []
        if not (400 <= total_words <= 1800):
            reasons.append(f"Word count ({total_words}) outside 400-1800")
        if dial_pct < 20.0:
            reasons.append(f"Dialogue ({dial_pct}%) < 20%")
        if fh < 65.0:
            reasons.append(f"Fernández Huerta ({fh}) < 65")

        return {
            "gutenberg_id": gutenberg_id,
            "book_title": book_title,
            "story_title": story_title,
            "author": author,
            "word_count": total_words,
            "dialogue_pct": dial_pct,
            "fernandez_huerta": fh,
            "cognate_density": cognate_pct,
            "viable": len(reasons) == 0,
            "rejection_reasons": "; ".join(reasons) if reasons else "None (Meets Criteria)"
        }
    