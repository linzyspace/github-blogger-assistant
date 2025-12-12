import requests
from typing import Optional, Dict, Any, List
from app.config import get_settings

BASE_URL = "https://www.googleapis.com/blogger/v3/blogs"


class BlogLookup:
    """Handles searching and retrieving posts from Blogger API."""

    def __init__(self):
        self.settings = get_settings()
        self.blog_id = self.settings.BLOG_ID
        self.api_key = self.settings.BLOGGER_API_KEY

    # ------------------------
    # Internal GET request
    # ------------------------
    def _get(self, endpoint: str, params: dict = None) -> Optional[dict]:
        url = f"{BASE_URL}/{self.blog_id}/{endpoint}"
        params = params or {}
        params["key"] = self.api_key

        try:
            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code != 200:
                print(f"Blogger API error: {resp.status_code} - {resp.text}")
                return None
            return resp.json()
        except Exception as e:
            print("Blogger request exception:", e)
            return None

    # ------------------------
    # Search posts by keyword
    # ------------------------
    def search_posts(self, keyword: str) -> List[Dict[str, Any]]:
        data = self._get("posts/search", {"q": keyword})
        if not data or "items" not in data:
            return []
        return data["items"]

    # ------------------------
    # Get latest posts
    # ------------------------
    def get_latest_posts(self, max_results: int = 1) -> List[Dict[str, Any]]:
        data = self._get("posts", {"maxResults": max_results})
        if not data or "items" not in data:
            return []
        return data["items"]

    # ------------------------
    # Main method for assistant
    # ------------------------
    def get_post_content(self, keyword: Optional[str] = None) -> Dict[str, Any]:
        """Return matching post or fallback to latest."""
        # Try keyword search first
        if keyword:
            results = self.search_posts(keyword)
            if results:
                return {
                    "status": "found",
                    "match_type": "keyword",
                    "post": results[0]
                }

        # Fallback: latest post
        latest = self.get_latest_posts(1)
        if latest:
            return {
                "status": "fallback",
                "match_type": "latest",
                "post": latest[0]
            }

        # Nothing found
        return {
            "status": "error",
            "message": "Unable to fetch posts from Blogger API",
            "keyword": keyword
        }


# Shared instance to be imported by FastAPI
blog_lookup = BlogLookup()
