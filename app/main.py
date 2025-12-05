from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import re

app = FastAPI()

# ------------------------------
# CORS (Required for Blogger)
# ------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

# ============================================================
#   YOUR BLOGGER CONFIG
# ============================================================

BLOGGER_API_KEY = "YOUR_BLOGGER_API_KEY"
BLOG_ID = "YOUR_BLOGGER_BLOG_ID"


# ============================================================
#   PREDEFINED REPLIES
# ============================================================

PREDEFINED_REPLIES = [
    { "keywords": ["hello", "hi", "hey"], "reply": "Hello! How can I help you today? 😊" },
    { "keywords": ["blog", "article", "post"], "reply": "Sure! Tell me the blog title or paste the link." },
    { "keywords": ["bye"], "reply": "Goodbye! 👋" },
    # ... (keep the rest of your existing list)
]


def match_predefined_reply(text: str):
    text = text.lower().strip()

    for item in PREDEFINED_REPLIES:
        for word in item["keywords"]:
            if word in text:
                return item["reply"]
    return None


# ============================================================
#   BLOGGER HELPERS
# ============================================================

# Detect blogger URL in user message
BLOGGER_URL_REGEX = r"(https?://[A-Za-z0-9\-_.]+\.blogspot\.com/[^\s]+)"

async def fetch_post_by_url(url: str):
    """Extract post ID and fetch its content from Blogger API."""
    # Blogger always contains "post/" then ID
    match = re.search(r"/posts/(\d+)", url)
    if not match:
        return None

    post_id = match.group(1)

    api = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/{post_id}?key={BLOGGER_API_KEY}"

    async with httpx.AsyncClient() as client:
        r = await client.get(api)
        if r.status_code == 200:
            return r.json()
        return None


async def fetch_posts_by_keyword(keyword: str):
    """Search Blogger posts by title using query."""
    api = (
        f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/search?"
        f"q={keyword}&key={BLOGGER_API_KEY}"
    )

    async with httpx.AsyncClient() as client:
        r = await client.get(api)
        if r.status_code == 200:
            return r.json().get("items", [])
        return []


# ============================================================
#   API ROUTES
# ============================================================

class AskPayload(BaseModel):
    topic: str
    lang: str = "en"


@app.post("/assistant")
async def assistant(payload: AskPayload):

    user_text = payload.topic.lower().strip()

    # 1️⃣ PREDEFINED REPLY CHECK
    pre = match_predefined_reply(user_text)
    if pre:
        return {"type": "predefined", "response": pre}

    # 2️⃣ CHECK IF USER SENT A BLOGGER URL
    url_match = re.search(BLOGGER_URL_REGEX, user_text)
    if url_match:
        url = url_match.group(1)
        post = await fetch_post_by_url(url)

        if post:
            return {
                "type": "blog_post",
                "title": post.get("title"),
                "content": post.get("content"),
                "images": [img["url"] for img in post.get("images", [])] if "images" in post else [],
            }

        return {"type": "error", "response": "Invalid Blogger post URL or post not found."}

    # 3️⃣ SEARCH BLOGGER BY KEYWORD
    posts = await fetch_posts_by_keyword(user_text)
    if posts:
        return {
            "type": "blog_search",
            "count": len(posts),
            "posts": [
                {
                    "title": p.get("title"),
                    "url": p.get("url"),
                    "snippet": (p.get("content")[:200] + "...")
                }
                for p in posts
            ]
        }

    # 4️⃣ NOTHING FOUND
    return {
        "type": "none",
        "response": "No predefined answer or blog post found."
    }


@app.get("/")
async def root():
    return {"status": "ok"}
