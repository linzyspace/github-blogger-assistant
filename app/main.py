import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

# Blogger config from env vars
BLOG_ID = os.getenv("BLOGGER_BLOG_ID")
BLOGGER_API_KEY = os.getenv("BLOGGER_API_KEY")

# ============================================================
# Keyword replies (same as your version)
# ============================================================

PREDEFINED_REPLIES = [...]
# keep your same list here


def match_predefined_reply(text: str):
    text = text.lower().strip()
    for item in PREDEFINED_REPLIES:
        for word in item["keywords"]:
            if word in text:
                return item["reply"]
    return None


# ============================================================
# BLOGGER API FUNCTIONS
# ============================================================

def search_blogger_posts(query: str):
    """Search posts using Blogger API."""
    url = (
        f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/search"
        f"?q={query}&key={API_KEY}"
    )
    resp = requests.get(url)
    if resp.status_code != 200:
        return None
    data = resp.json()
    return data.get("items", None)


def get_latest_post():
    """Return most recent post."""
    url = (
        f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts"
        f"?maxResults=1&key={API_KEY}"
    )
    resp = requests.get(url)
    if resp.status_code != 200:
        return None
    data = resp.json()
    items = data.get("items", [])
    return items[0] if items else None


# ============================================================
# API ROUTES
# ============================================================

class AskPayload(BaseModel):
    topic: str
    lang: str = "en"


@app.post("/assistant")
async def assistant(payload: AskPayload):
    query = payload.topic.strip()

    # 1 — Predefined replies first
    predefined = match_predefined_reply(query)
    if predefined:
        return {
            "type": "predefined",
            "response": predefined
        }

    # 2 — Search Blogger by keyword
    posts = search_blogger_posts(query)
    if posts:
        return {
            "type": "blog",
            "match": "keyword",
            "title": posts[0]["title"],
            "content": posts[0].get("content", "")
        }

    # 3 — Fallback → latest post
    latest = get_latest_post()
    if latest:
        return {
            "type": "blog",
            "match": "latest",
            "title": latest["title"],
            "content": latest.get("content", "")
        }

    # 4 — Nothing found
    return {
        "type": "none",
        "response": "No predefined answer and no blog posts found."
    }


@app.get("/")
async def root():
    return {"status": "ok"}
