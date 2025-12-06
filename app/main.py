import os
import requests
from difflib import SequenceMatcher
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
# ENV VARIABLES FOR CLOUD RUN
# ------------------------------------------------------------
BLOG_ID = os.getenv("BLOG_ID")
BLOGGER_API_KEY = os.getenv("BLOGGER_API_KEY")

# ============================================================
#   PREDEFINED QUESTIONS & ANSWERS (UNCHANGED)
# ============================================================

PREDEFINED_REPLIES = [
    # ------------------ GREETINGS ------------------
    { "keywords": ["hello", "hi", "hey", "yo", "hiya", "helo", "sup", "wassup"],
      "reply": "Hello! How can I help you today? 😊" },
    { "keywords": ["good morning", "morning"], "reply": "Good morning! Hope your day starts amazing!" },
    { "keywords": ["good afternoon"], "reply": "Good afternoon! How’s your day going?" },
    { "keywords": ["good evening", "evening"], "reply": "Good evening! Need help with anything?" },
    { "keywords": ["greetings"], "reply": "Warm greetings! How may I assist you today?" },

    # ------------------ SMALL TALK ------------------
    { "keywords": ["how are you", "how r u", "how you doing"],
      "reply": "I'm doing great, thanks for asking! How about you?" },
    { "keywords": ["what's up", "whats up", "sup", "wassup"],
      "reply": "All good here! What’s going on with you?" },
    { "keywords": ["who are you", "your name", "what are you"],
      "reply": "I’m your friendly AI assistant!" },
    { "keywords": ["where are you"], "reply": "I live inside your browser—pretty cool right? 😄" },

    # ------------------ THANKS ------------------
    { "keywords": ["thank you", "thanks", "thx", "ty"],
      "reply": "You're welcome! Happy to help! 😊" },
    { "keywords": ["appreciate"], "reply": "Aww, I appreciate you too! ❤️" },

    # ------------------ GOODBYES ------------------
    { "keywords": ["bye", "goodbye", "see you", "cya", "take care"],
      "reply": "Goodbye! Take care! 👋" },
    { "keywords": ["good night", "night"], "reply": "Good night! Sleep well! 🌙" },

    # ------------------ BLOGGER ------------------
    { "keywords": ["blog", "post", "article", "blogger"],
      "reply": "I can help you find blog posts or answer questions about Blogger!" },
    { "keywords": ["image", "photo", "picture", "img"],
      "reply": "If the post contains images, I’ll pull them up for you!" },
    { "keywords": ["pdf", "document", "word", "file"],
      "reply": "I can fetch PDFs or documents if they exist in the post." },
    { "keywords": ["video", "youtube", "yt"],
      "reply": "I can show YouTube or embedded videos from your blog posts." },
    { "keywords": ["seo", "ranking"],
      "reply": "Improving your SEO starts with keywords, quality content, and clean structure." },

    # ------------------ TECH & AI ------------------
    { "keywords": ["ai", "artificial intelligence"],
      "reply": "AI simulates human intelligence in machines." },
    { "keywords": ["machine learning", "ml"],
      "reply": "Machine learning helps computers learn from data." },
    { "keywords": ["deep learning", "dl"],
      "reply": "Deep learning uses layered neural networks to learn patterns." },
    { "keywords": ["chatbot", "bot"],
      "reply": "Chatbots simulate conversations using natural language models." },
    { "keywords": ["coding", "programming"],
      "reply": "Coding is fun! What language are you working on?" },
    { "keywords": ["javascript"], "reply": "JavaScript powers dynamic web pages!" },
    { "keywords": ["python"], "reply": "Python is beginner-friendly and powerful!" },
    { "keywords": ["html", "css"], "reply": "HTML builds the page, CSS makes it beautiful!" },

    # ------------------ SLANG ------------------
    { "keywords": ["lol", "lmao", "rofl"], "reply": "Haha! Glad it made you laugh 😄" },
    { "keywords": ["omg", "wow"], "reply": "I know, right? 😄" },
    { "keywords": ["brb"], "reply": "Sure! I'll be here when you're back!" },

    # ------------------ FEEDBACK ------------------
    { "keywords": ["good", "great", "doing fine", "awesome", "fantastic", "happy", "cool", "excellent"],
      "reply": "I'm glad to hear that! 😊 Hope your day keeps going well!" },
    { "keywords": ["okay", "k", "ok", "fine", "alright", "not bad"],
      "reply": "Got it! Thanks for letting me know 😊" },
    { "keywords": ["not good", "no", "not really", "so so", "just ok", "bad", "sad", "tired", "angry", "upset"],
      "reply": "Oh, I’m sorry to hear that. I’m here if you want to chat or need a joke to cheer up 😄" },

    # ------------------ SPORTS ------------------
    { "keywords": ["sports"], "reply": "Sports are great! What sport do you like?" },
    { "keywords": ["basketball"], "reply": "Basketball is exciting—who’s your favorite player?" },
    { "keywords": ["soccer", "football"], "reply": "Soccer is the world’s favorite sport! ⚽" },
    { "keywords": ["boxing", "mma"], "reply": "Combat sports require discipline and strength!" },
]


# ----------- HELPER: Match predefined answers -----------
def match_predefined_reply(text: str):
    text = text.lower().strip()
    for item in PREDEFINED_REPLIES:
        for word in item["keywords"]:
            if word in text:
                return item["reply"]
    return None


# ============================================================
#   IMPROVED BLOGGER CONTENT FETCH (GUARANTEED MATCH)
# ============================================================

def fetch_blogger_post_content(query: str):
    """Fetch Blogger content with fallback and fuzzy matching."""

    if not BLOG_ID or not BLOGGER_API_KEY:
        return None

    try:
        # 1️⃣ TRY SEARCH FIRST
        search_url = (
            f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/search"
            f"?q={query}&key={BLOGGER_API_KEY}"
        )
        search_result = requests.get(search_url, timeout=10).json()
        posts = search_result.get("items", [])

        # 2️⃣ IF SEARCH FAILS → GET ALL POSTS
        if not posts:
            list_url = (
                f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts"
                f"?maxResults=50&key={BLOGGER_API_KEY}"
            )
            list_result = requests.get(list_url, timeout=10).json()
            posts = list_result.get("items", [])

        if not posts:
            return None

        # 3️⃣ FUZZY MATCH BEST RESULT
        q = query.lower()

        def score(post):
            text = (
                f"{post.get('title', '')} "
                f"{post.get('content', '')}"
            ).lower()
            return SequenceMatcher(None, q, text).ratio()

        best_post = max(posts, key=score)

        return {
            "title": best_post.get("title", ""),
            "content": best_post.get("content", "")
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
    # 1️⃣ CHECK PREDEFINED KEYWORDS
    predefined = match_predefined_reply(payload.topic)
    if predefined:
        return {
            "type": "predefined",
            "response": predefined
        }

    # 2️⃣ BLOGGER FALLBACK
    blog_post = fetch_blogger_post_content(payload.topic)
    if blog_post:
        return {
            "type": "blog",
            "title": blog_post["title"],
            "response": blog_post["content"]
        }

    # 3️⃣ NOTHING FOUND
    return {
        "type": "none",
        "response": "No predefined answer or blog post found."
    }


@app.get("/")
async def root():
    return {"status": "ok"}
