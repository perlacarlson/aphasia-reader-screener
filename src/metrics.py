# Aphasiology & readability formulas
import re
import unicodedata
import difflib
from typing import Tuple, List

CONCRETE_BENCHMARK_LEMMAS = {
    "doctor", "hospital", "family", "animal", "plant", "fruit", "river",
    "forest", "mountain", "house", "door", "table", "horse", "dog",
    "cat", "bird", "medicine", "train", "boat", "bread", "water",
    "problem", "person", "music", "garden", "market", "coast", "valley"
}

def strip_accents(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")

def count_spanish_syllables(word: str) -> int:
    word = re.sub(r"[^a-záéíóúüñ]", "", word.lower())
    if not word:
        return 0
    vowels = "aáeéoóiíuúü"
    strong = "aáeéoó"
    accented_weak = "íú"
    count, i, n = 0, 0, len(word)
    while i < n:
        if word[i] in vowels:
            count += 1
            if i + 1 < n and word[i+1] in vowels:
                v1, v2 = word[i], word[i+1]
                # If neither is a hiatus-forcing pair, merge as diphthong
                if not ((v1 in strong and v2 in strong) or (v1 in accented_weak or v2 in accented_weak)):
                    i += 1
        i += 1
    return max(1, count)

def calculate_fernandez_huerta(words: List[str], sentences: List[str]) -> float:
    total_words = len(words)
    total_sents = max(1, len(sentences))
    if total_words == 0:
        return 0.0
    total_syllables = sum(count_spanish_syllables(w) for w in words)
    syllables_per_word = total_syllables / total_words
    words_per_sent = total_words / total_sents
    return round(206.84 - (60 * syllables_per_word) - (1.02 * words_per_sent), 2)

def extract_dialogue_percentage(text: str, total_words: int) -> float:
    if total_words == 0:
        return 0.0
    dash_dialogue = re.findall(r"(?:^|\n)\s*[—–-]\s*(.*?)(?=[—–-]|\n|$)", text)
    quoted_dialogue = re.findall(r'[«"“](.*?)[»"”]', text)
    dialogue_words = len(re.findall(r"\b\w+\b", " ".join(dash_dialogue + quoted_dialogue)))
    return round((min(dialogue_words, total_words) / total_words) * 100, 2)

def calculate_cognate_density(words: List[str], total_words: int) -> float:
    if total_words == 0:
        return 0.0
    hits, seen = 0, set()
    for w in words:
        clean = strip_accents(w.lower())
        if len(clean) < 4 or clean in seen:
            continue
        for eng in CONCRETE_BENCHMARK_LEMMAS:
            if difflib.SequenceMatcher(None, clean, eng).ratio() >= 0.75:
                hits += 1
                seen.add(clean)
                break
    return round((hits / total_words) * 100, 2)
