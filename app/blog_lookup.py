import requests
from difflib import SequenceMatcher
from config import BLOG_ID, BLOGGER_API_KEY

def fetch_blogger_post_content(query: str):
    """Fetch blog content from Blogger API with fallback and fuzzy matching"""
    if not BLOG_ID or not BLOGGER_API_KEY:
        print("[ERROR] Missing BLOG_ID or BLOGGER_API_KEY")
        return None

    try:
        # 1️⃣ Search endpoint
        search_url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/search?q={query}&key={BLOGGER_API_KEY}"
        res = requests.get(search_url, timeout=10).json()
        posts = res.get("items", [])

        # 2️⃣ Fallback: get all posts
        if not posts:
            list_url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts?maxResults=50&key={BLOGGER_API_KEY}"
            res = requests.get(list_url, timeout=10).json()
            posts = res.get("items", [])

        if not posts:
            print("[WARNING] No posts found in Blogger")
            return None

        # 3️⃣ Fuzzy match best post
        query_lower = query.lower()
        def score(post):
            text = f"{post.get('title','')} {post.get('content','')}".lower()
            return SequenceMatcher(None, query_lower, text).ratio()

        best_post = max(posts, key=score)
        print(f"[INFO] Best matching post: {best_post.get('title','')}")
        return {"title": best_post.get("title",""), "content": best_post.get("content","")}

    except Exception as e:
        print(f"[ERROR] Blogger API exception: {e}")
        return None

