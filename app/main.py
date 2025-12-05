from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

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
#   API KEYS
# ============================================================

BLOGGER_API_KEY = "YOUR_BLOGGER_API_KEY"
BLOG_ID = "YOUR_BLOG_ID"

YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"


# ============================================================
#   PREDEFINED QUESTIONS & ANSWERS  (unchanged)
# ============================================================

PREDEFINED_REPLIES = [
    { "keywords": ["hello", "hi", "hey"], "reply": "Hello! How can I help you today? 😊" },
    # ... (all your predefined replies remain unchanged)
]

def match_predefined_reply(text: str):
    text = text.lower().strip()
    for item in PREDEFINED_REPLIES:
        for word in item["keywords"]:
            if word in text:
                return item["reply"]
    return None


# ============================================================
#   BLOGGER API FETCHER
# ============================================================

async def fetch_blogger_post(query: str):
    """
    Searches blog posts by title/content using Blogger API
    """

    search_url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/search"
    params = {
        "q": query,
        "key": BLOGGER_API_KEY
    }

    async with httpx.AsyncClient() as client:
        r = await client.get(search_url, params=params)

        if r.status_code != 200:
            return None

        data = r.json()

        if "items" not in data or len(data["items"]) == 0:
            return None

        first_post = data["items"][0]

        return {
            "title": first_post.get("title"),
            "content": first_post.get("content"),
            "url": first_post.get("url")
        }


# ============================================================
#   YOUTUBE API FETCHER
# ============================================================

async def fetch_youtube_video(video_id: str):
    """
    Fetches YouTube video info like title, description, thumbnail.
    """
    url = "https://www.googleapis.com/youtube/v3/videos"

    params = {
        "id": video_id,
        "key": YOUTUBE_API_KEY,
        "part": "snippet,contentDetails"
    }

    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params)

        if r.status_code != 200:
            return None

        data = r.json()

        if "items" not in data or len(data["items"]) == 0:
            return None

        info = data["items"][0]["snippet"]

        return {
            "title": info["title"],
            "description": info["description"],
            "thumbnail": info["thumbnails"]["high"]["url"]
        }



# ============================================================
#   API ROUTES
# ============================================================

class AskPayload(BaseModel):
    topic: str
    lang: str = "en"


@app.post("/assistant")
async def assistant(payload: AskPayload):
    text = payload.topic.lower()

    # 1️⃣ Try predefined replies
    predefined = match_predefined_reply(text)
    if predefined:
        return {"type": "predefined", "response": predefined}

    # 2️⃣ Try to fetch a Blogger article
    blogger_post = await fetch_blogger_post(text)
    if blogger_post:
        return {
            "type": "blogger",
            "title": blogger_post["title"],
            "content": blogger_post["content"],
            "url": blogger_post["url"]
        }

    # 3️⃣ Try to fetch YouTube info if a YouTube link or ID is present
    if "youtube.com" in text or "youtu.be" in text or "video:" in text:
        # Extract video ID simplistically
        import re
        match = re.findall(r"(?:v=|youtu\.be/)([\w\-]+)", text)
        if match:
            video_data = await fetch_youtube_video(match[0])
            if video_data:
                return {
                    "type": "youtube",
                    "video": video_data
                }

    # 4️⃣ Nothing matched
    return {
        "type": "none",
        "response": "No predefined answer or content found from Blogger or YouTube."
    }


@app.get("/")
async def root():
    return {"status": "ok"}
