import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ------------------------------
# CORS
# ------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

# ------------------------------
# Blogger config from env vars
# ------------------------------
BLOG_ID = os.getenv("BLOGGER_BLOG_ID")
BLOGGER_API_KEY = os.getenv("BLOGGER_API_KEY")

if not BLOG_ID or not BLOGGER_API_KEY:
    raise RuntimeError("BLOGGER_BLOG_ID and BLOGGER_API_KEY must be set as environment variables.")

print("BLOG_ID:", BLOG_ID)
print("BLOGGER_API_KEY length:", len(BLOGGER_API_KEY))

# ------------------------------
# Predefined replies
# ------------------------------
PREDEFINED_REPLIES = [
    {"keywords": ["hello", "hi", "hey"], "reply": "Hello! How can I help you today? 😊"},
    {"keywords": ["bye", "goodbye"], "reply": "Goodbye! Take care! 👋"},
    {"keywords": ["thank you", "thanks"], "reply": "You're welcome! Happy to help! 😊"},
    {"keywords": ["blog", "post", "article", "blogger"], "reply": "I can help you find blog posts or answer questions about Blogger!"},
    # Add all your other predefined replies here...
]

def match_predefined_reply(text: str):
    text = text.lower().strip()
    for item in PREDEFINED_REPLIES:
        for word in item["keywords"]:
            if word in text:
                return item["reply"]
    return None

# ------------------------------
# Blogger API functions
# ------------------------------
def search_blogger_posts(query: str):
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/search?q={query}&key={BLOGGER_API_KEY}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if "error" in data:
            print("Blogger search API error:", data["error"])
            return None
        return data.get("items", [])
    except Exception as e:
        print("Blogger search exception:", e)
        return None

def get_latest_post():
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts?maxResults=1&key={BLOGGER_API_KEY}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        print("Latest post API response:", data)
        if "error" in data:
            print("Blogger latest post API error:", data["error"])
            return None
        items = data.get("items", [])
        return items[0] if items else None
    except Exception as e:
        print("Blogger latest post exception:", e)
        return None

# ------------------------------
# API routes
# ------------------------------
class AskPayload(BaseModel):
    topic: str
    lang: str = "en"

@app.post("/assistant")
async def assistant(payload: AskPayload):
    query = payload.topic.strip()

    # 1 — Predefined replies first
    predefined = match_predefined_reply(query)
    if predefined:
        return {"type": "predefined", "response": predefined}

    # 2 — Search Blogger posts by keyword
    posts = search_blogger_posts(query)
    if posts and len(posts) > 0:
        first_post = posts[0]
        match_type = "keyword"
    else:
        # 3 — Fallback to latest post if search fails
        first_post = get_latest_post()
        match_type = "latest" if first_post else None

    if first_post:
        return {
            "type": "blog",
            "match": match_type,
            "title": first_post.get("title", ""),
            "content": first_post.get("content", ""),
            "url": first_post.get("url", "")
        }

    # 4 — Nothing found
    return {"type": "none", "response": "No predefined answer and no blog posts found."}

@app.get("/")
async def root():
    return {"status": "ok"}

# ------------------------------
# Debug route to test Blogger API
# ------------------------------
@app.get("/debug-blogger")
async def debug_blogger():
    latest = get_latest_post()
    search = search_blogger_posts("test")
    return {"latest_post": latest, "search_test": search}
