import os
import requests
import re

BLOG_ID = os.getenv("BLOGGER_BLOG_ID")
API_KEY = os.getenv("BLOGGER_API_KEY")
API_URL = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts?key={API_KEY}"

def fetch_posts():
    """Fetch latest blog posts without AI."""
    try:
        r = requests.get(API_URL)
        return r.json().get("items", [])
    except:
        return []

def clean_html(text):
    return re.sub("<[^<]+?>", "", text or "").strip()

def search_blog_posts(query: str, limit=3):
    """Simple keyword scoring. No AI."""
    q = query.lower()
    posts = fetch_posts()
    matches = []

    for p in posts:
        title = p.get("title", "")
        content = clean_html(p.get("content", ""))

        score = 0
        if q in title.lower():
            score += 5
        if q in content.lower():
            score += 3

        for w in q.split():
            if w in title.lower():
                score += 2
            if w in content.lower():
                score += 1

        if score > 0:
            matches.append({
                "title": title,
                "url": p.get("url"),
                "snippet": content[:200] + "…",
                "score": score
            })

    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches[:limit]

