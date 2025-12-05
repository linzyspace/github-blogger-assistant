import httpx
from .config import BLOGGER_API_KEY, BLOGGER_BLOG_ID


async def search_blogger_posts(query: str):
    """
    Search for posts on Blogger by keyword.
    Returns: title, content (HTML), url or None
    """

    if not BLOGGER_API_KEY or not BLOGGER_BLOG_ID:
        return None

    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOGGER_BLOG_ID}/posts/search"

    params = {
        "q": query,
        "key": BLOGGER_API_KEY
    }

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            r = await client.get(url, params=params)
        except Exception:
            return None

        if r.status_code != 200:
            return None

        data = r.json()

        if "items" not in data or len(data["items"]) == 0:
            return None

        post = data["items"][0]

        return {
            "title": post.get("title", ""),
            "content": post.get("content", ""),
            "url": post.get("url", "")
        }
