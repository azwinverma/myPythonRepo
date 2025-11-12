import os
import re
import time
import requests
from typing import List, Dict, Tuple

HF_TOKEN = (os.getenv("HF_TOKEN") or "").strip()

DEFAULT_STYLES: Dict[str, str] = {
    "friendly": "Warm, friendly, short. 1–2 sentences.",
    "minimal":  "Minimal, aesthetic, few words, no emojis.",
    "story":    "Conversational, tiny story, upbeat, 2–3 sentences.",
    "sales":    "Call-to-action, value-driven, concise, 1–2 sentences.",
    "poetic":   "Poetic, metaphorical, short.",
}

SAMPLE_HASHTAGS: Dict[str, List[str]] = {
    "fitness":     ["#fitness", "#workout", "#gym", "#health", "#fitlife", "#wellness"],
    "meditation":  ["#meditation", "#mindfulness", "#dailypractice", "#breathe", "#calm"],
    "reading":     ["#reading", "#bookstagram", "#booklover", "#readmore"],
    "lifestyle":   ["#lifestyle", "#daily", "#selfcare", "#goals", "#habits"],
}

def pick_hashtags(topic: str, max_tags: int = 10) -> List[str]:
    pool = SAMPLE_HASHTAGS.get(topic.lower(), SAMPLE_HASHTAGS["lifestyle"])
    return pool[:max_tags]

def trim_text(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    cut = text[:limit]
    last_space = cut.rfind(" ")
    return cut if last_space < 0 else cut[:last_space]

def local_template(prompt: str, tone: str, add_emojis: bool) -> str:
    style = DEFAULT_STYLES.get(tone.lower(), DEFAULT_STYLES["friendly"])
    _ = style  # not deeply used; could guide more transforms later
    emo = " ✨💫" if add_emojis else ""
    base = f"{prompt.strip()}. {emo}".strip()
    if "minimal" in tone.lower():
        base = re.sub(r"[.!?]\s*$", "", base)
    return base

def hf_generate(prompt: str, model: str = "meta-llama/Llama-3.1-8B-Instruct") -> Tuple[str, str]:
    """Return (text, used_model). Raises on HTTP errors."""
    if not HF_TOKEN:
        raise RuntimeError("HF_TOKEN missing")
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 120, "temperature": 0.8, "return_full_text": False},
        "options": {"wait_for_model": True},
    }
    r = requests.post(api_url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    if isinstance(data, list) and data and "generated_text" in data[0]:
        return data[0]["generated_text"].strip(), f"HuggingFace ({model})"
    if isinstance(data, dict) and "generated_text" in data:
        return data["generated_text"].strip(), f"HuggingFace ({model})"
    return str(data), f"HuggingFace ({model})"
