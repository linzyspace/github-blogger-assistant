from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

# ===== BLOGGER CONFIG =====
BLOGGER_API_KEY = "YOUR_BLOGGER_API_KEY"
BLOGGER_BLOG_ID = "YOUR_BLOG_ID"

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


# ============================================================
#   PREDEFINED QUESTIONS & ANSWERS (unchanged)
# ============================================================
PREDEFINED_REPLIES = [
    # ... all your predefined keywords here (unchanged)
]


def match_predefined_reply(text: str):
    text = text.lower().strip()
    for item in PREDEFINED_REPLIES:
        for word in item["keywords"]:
            if word in text:
                return item["reply"]
    return None


# ============================================================
#   BLOGGER API SEARCH
# ============================================================
async def blogger_search(query: str):
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOGGER_BLOG_ID}/posts/search"
    params = {"q": query, "key": BLOGGER_API_KEY}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, params=params)

            if r.status_code != 200:
                return None

            data = r.json()

            if "items" not in data or len(data["items"]) == 0:
                return None

            post = data["items"][0]

            return {
                "title": post.get("title"),
                "content": post.get("content"),
                "url": post.get("url")
            }

    except Exception:
        return None


# ============================================================
#   API ROUTES
# ============================================================
class AskPayload(BaseModel):
    topic: str
    lang: str = "en"


@app.post("/assistant")
async def assistant(payload: AskPayload):
    user_text = payload.topic.lower()

    # --------------------------------------------------------
    #  FIX B: Blogger search BEFORE predefined replies
    # --------------------------------------------------------
    if any(word in user_text for word in ["blog", "post", "article", "content", "show", "find"]):
        blog_data = await blogger_search(payload.topic)

        if blog_data:
            return {
                "type": "blogger",
                "title": blog_data["title"],
                "content": blog_data["content"],
                "url": blog_data["url"]
            }

    # --------------------------------------------------------
    #  Predefined replies (unchanged)
    # --------------------------------------------------------
    predefined = match_predefined_reply(payload.topic)
    if predefined:
        return {
            "type": "predefined",
            "response": predefined
        }

    # --------------------------------------------------------
    #  Nothing matched
    # --------------------------------------------------------
    return {
        "type": "none",
        "response": "No predefined answer or blog match found."
    }


@app.get("/")
async def root():
    return {"status": "ok"}
