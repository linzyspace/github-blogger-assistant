import os
import requests

BLOG_ID = os.getenv("BLOGGER_BLOG_ID")
BLOGGER_API_KEY = os.getenv("BLOGGER_API_KEY")

def search_blogger_posts(query: str):
    """Search posts by keyword."""
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/search?q={query}&key={BLOGGER_API_KEY}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return []
        data = resp.json()
        return data.get("items", [])
    except Exception:
        return []

def get_latest_post():
    """Return the latest post."""
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts?maxResults=1&key={BLOGGER_API_KEY}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return None
        data = resp.json()
        items = data.get("items", [])
        return items[0] if items else None
    except Exception:
        return None

def find_blog_match(query: str):
    """Return a blog post dict, either by keyword or fallback latest."""
    posts = search_blogger_posts(query)
    if posts:
        post = posts[0]
        return {
            "title": post.get("title", ""),
            "content": post.get("content", ""),
            "url": post.get("url", "")
        }
    
    latest = get_latest_post()
    if latest:
        return {
            "title": latest.get("title", ""),
            "content": latest.get("content", ""),
            "url": latest.get("url", "")
        }
    
    return None
