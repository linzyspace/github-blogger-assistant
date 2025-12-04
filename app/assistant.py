from typing import Optional, Dict, Any
from .utils import load_yaml
import re

# Cache loaded YAML to avoid repeated I/O
_RESPONSES = None
_CATEGORIES = None

def _ensure_loaded():
    global _RESPONSES, _CATEGORIES
    if _RESPONSES is None:
        _RESPONSES = load_yaml("responses.yaml") or {}
    if _CATEGORIES is None:
        _CATEGORIES = load_yaml("categories.yaml") or {}

def find_predefined_response(topic: str, lang: str = "en") -> Optional[Dict[str, Any]]:
    """
    Try to find a predefined response by exact key or simple fuzzy match.
    """
    _ensure_loaded()
    # Prefer direct key match first
    key = topic.strip().lower()
    if key in _RESPONSES.get(lang, {}):
        return {"type": "predefined", "response": _RESPONSES[lang][key]}

    # Fuzzy search (simple substring)
    for k, v in _RESPONSES.get(lang, {}).items():
        if re.search(re.escape(key), k, re.IGNORECASE):
            return {"type": "predefined", "response": v}

    return None

def find_blog_match(topic: str, lang: str = "en") -> Optional[Dict[str, Any]]:
    """
    Dummy blog lookup function stub. Replace with DB or search later.
    """
    # For demo: search categories for match and return a fake blog pointer
    _ensure_loaded()
    key = topic.strip().lower()
    for cat_name, cat_meta in _CATEGORIES.items():
        if key in cat_name.lower() or key in " ".join(cat_meta.get("aliases", [])).lower():
            return {
                "type": "blog",
                "response": f"See posts in category: {cat_name}",
                "category": cat_name
            }
    return None

def get_predefined_or_blog_response(topic: str, lang: str = "en") -> Dict[str, Any]:
    if not topic:
        return {"type": "error", "response": "Missing topic"}
    resp = find_predefined_response(topic, lang)
    if resp:
        return resp
    blog = find_blog_match(topic, lang)
    if blog:
        return blog
    return {"type": "none", "response": "No predefined answer or blog post match found."}
