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

    # -------------------------------------------------------------
    # Internal helper to call Blogger API safely
    # -------------------------------------------------------------
    def _get(self, endpoint: str, params: dict = None) -> Optional[dict]:
        url = f"{BASE_URL}/{self.blog_id}/{endpoint}"
        params = params or {}
        params["key"] = self.api_key

        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code != 200:
                print("Blogger API error:", response.text)
                return None
            return response.json()
        except Exception as e:
            print("Blogger request failed:", e)
            return None

    # -------------------------------------------------------------
    # Primary search function
    # -------------------------------------------------------------
    def search_posts(self, keyword: str) -> List[Dict[str, Any]]:
        """Search for posts containing keyword.
        Returns empty list if none found.
        """
        data = self._get("posts/search", {"q": keyword})
        if not data or "items" not in data:
            return []
        return data["items"]

    # -------------------------------------------------------------
    # Fallback: get latest posts
    # -------------------------------------------------------------
    def get_latest_posts(self, max_results: int = 3) -> List[Dict[str, Any]]:
        data = self._get("posts", {"maxResults": max_results})
        if not data or "items" not in data:
            return []
        return data["items"]

    # -------------------------------------------------------------
    # Main method the assistant should call
    # -------------------------------------------------------------
    def get_post_content(self, keyword: Optional[str] = None) -> Dict[str, Any]:
        """Get best matching post or fallback to latest post."""

        # 1. If keyword provided → try search
        if keyword:
            results = self.search_posts(keyword)
            if results:
                return {
                    "status": "found",
                    "keyword": keyword,
                    "post": results[0],  # best match first
                }

        # 2. Fallback: latest post
        latest = self.get_latest_posts(1)
        if latest:
            return {
                "status": "fallback",
                "keyword": keyword,
                "post": latest[0],
            }

        # 3. Full failure
        return {
            "status": "error",
            "message": "Unable to fetch posts from Blogger API",
            "keyword": keyword,
        }


# Shared instance for the app
blog_lookup = BlogLookup()
