import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

# ------------------------------------------------------------
# ENV VARIABLES (Set these in Cloud Run -> Variables)
# ------------------------------------------------------------
BLOG_ID = os.getenv("BLOG_ID")
BLOGGER_API_KEY = os.getenv("BLOGGER_API_KEY")

# ============================================================
#   PREDEFINED QUESTIONS & ANSWERS
# ============================================================

PREDEFINED_REPLIES = [
    # (UNCHANGED — all your predefined messages stay exactly the same)
]

# ----------- HELPER: Match predefined answers -----------
def match_predefined_reply(text: str):
    text = text.lower().strip()

    for item in PREDEFINED_REPLIES:
        for word in item["keywords"]:
            if word in text:
                return item["reply"]

    return None  # No match


# ============================================================
#   BLOGGER API FALLBACK
# ============================================================

def fetch_blogger_post_content(query: str):
    """Fetch posts from Blogger API when no predefined keywords match."""

    if not BLOG_ID or not BLOGGER_API_KEY:
        return None  # API not configured

    try:
        url = (
            f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/search"
            f"?q={query}&key={BLOGGER_API_KEY}"
        )

        response = requests.get(url, timeout=10)
        data = response.json()

        if "items" not in data:
            return None

        # Return first matching post
        post = data["items"][0]

        return {
            "title": post.get("title", ""),
            "content": post.get("content", "")
        }

    except Exception:
        return None  # Fallback gracefully


# ============================================================
#   API ROUTES
# ============================================================

class AskPayload(BaseModel):
    topic: str
    lang: str = "en"


@app.post("/assistant")
async def assistant(payload: AskPayload):
    # 1️⃣ Try predefined replies first
    predefined = match_predefined_reply(payload.topic)

    if predefined:
        return {
            "type": "predefined",
            "response": predefined
        }

    # 2️⃣ No predefined match → Try Blogger API
    blog_post = fetch_blogger_post_content(payload.topic)

    if blog_post:
        return {
            "type": "blog",
            "title": blog_post["title"],
            "response": blog_post["content"]
        }

    # 3️⃣ Nothing found
    return {
        "type": "none",
        "response": "No predefined answer or blog post found."
    }


@app.get("/")
async def root():
    return {"status": "ok"}
