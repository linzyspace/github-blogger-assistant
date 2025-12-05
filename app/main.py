from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ------------------------------
# CORS (Required for Blogger & browser apps)
# ------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

# ============================================================
#   PREDEFINED QUESTIONS & ANSWERS
# ============================================================

PREDEFINED_REPLIES = [
    # ------------------ GREETINGS ------------------
    { "keywords": ["hello", "hi", "hey", "yo", "hiya", "helo", "sup", "wassup"], "reply": "Hello! How can I help you today? 😊" },
    { "keywords": ["good morning", "morning"], "reply": "Good morning! Hope your day starts amazing!" },
    { "keywords": ["good afternoon"], "reply": "Good afternoon! How’s your day going?" },
    { "keywords": ["good evening", "evening"], "reply": "Good evening! Need help with anything?" },
    { "keywords": ["greetings"], "reply": "Warm greetings! How may I assist you today?" },

    # ------------------ SMALL TALK ------------------
    { "keywords": ["how are you", "how r u", "how you doing"], "reply": "I'm doing great, thanks for asking! How about you?" },
    { "keywords": ["what's up", "whats up", "sup", "wassup"], "reply": "All good here! What’s going on with you?" },
    { "keywords": ["who are you", "your name", "what are you"], "reply": "I’m your friendly AI assistant!" },
    { "keywords": ["where are you"], "reply": "I live inside your browser—pretty cool right? 😄" },

    # ------------------ THANKS ------------------
    { "keywords": ["thank you", "thanks", "thx", "ty"], "reply": "You're welcome! Happy to help! 😊" },
    { "keywords": ["appreciate"], "reply": "Aww, I appreciate you too! ❤️" },

    # ------------------ GOODBYES ------------------
    { "keywords": ["bye", "goodbye", "see you", "cya", "take care"], "reply": "Goodbye! Take care! 👋" },
    { "keywords": ["good night", "night"], "reply": "Good night! Sleep well! 🌙" },

    # ------------------ BLOGGER ------------------
    { "keywords": ["blog", "post", "article", "blogger"], "reply": "I can help you find blog posts or answer questions about Blogger!" },
    { "keywords": ["image", "photo", "picture", "img"], "reply": "If the post contains images, I’ll pull them up for you!" },
    { "keywords": ["pdf", "document", "word", "file"], "reply": "I can fetch PDFs or documents if they exist in the post." },
    { "keywords": ["video", "youtube", "yt"], "reply": "I can show YouTube or embedded videos from your blog posts." },
    { "keywords": ["seo", "ranking"], "reply": "Improving your SEO starts with keywords, quality content, and clean structure." },

    # ------------------ TECH & AI ------------------
    { "keywords": ["ai", "artificial intelligence"], "reply": "AI simulates human intelligence in machines." },
    { "keywords": ["machine learning", "ml"], "reply": "Machine learning helps computers learn from data." },
    { "keywords": ["deep learning", "dl"], "reply": "Deep learning uses layered neural networks to learn patterns." },
    { "keywords": ["chatbot", "bot"], "reply": "Chatbots simulate conversations using natural language models." },
    { "keywords": ["coding", "programming"], "reply": "Coding is fun! What language are you working on?" },
    { "keywords": ["javascript"], "reply": "JavaScript powers dynamic web pages!" },
    { "keywords": ["python"], "reply": "Python is beginner-friendly and powerful!" },
    { "keywords": ["html", "css"], "reply": "HTML builds the page, CSS makes it beautiful!" },

    # ------------------ SLANG ------------------
    { "keywords": ["lol", "lmao", "rofl"], "reply": "Haha! Glad it made you laugh 😄" },
    { "keywords": ["omg", "wow"], "reply": "I know, right? 😄" },
    { "keywords": ["brb"], "reply": "Sure! I'll be here when you're back!" },

    # ------------------ USER FEEDBACK / SENTIMENT ------------------
    # Positive
    { "keywords": ["good", "great", "doing fine", "awesome", "fantastic", "happy", "cool", "excellent"], 
      "reply": "I'm glad to hear that! 😊 Hope your day keeps going well!" },
    # Neutral
    { "keywords": ["okay", "k", "ok" "fine", "alright", "not bad"], 
      "reply": "Got it! Thanks for letting me know 😊" },
    # Negative
    { "keywords": ["not good", "g", "gee", "no", "not really", "so so", "just ok", "gosh", "bad", "sad", "tired", "angry", "upset"], 
      "reply": "Oh, I’m sorry to hear that. I’m here if you want to chat or need a joke to cheer up 😄" },

    # ------------------ SPORTS ------------------
    { "keywords": ["sports"], "reply": "Sports are a great way to stay active! What sport do you like?" },
    { "keywords": ["basketball"], "reply": "Basketball is exciting—who’s your favorite player?" },
    { "keywords": ["soccer", "football"], "reply": "Soccer is the world’s favorite sport! ⚽" },
    { "keywords": ["boxing", "mma"], "reply": "Combat sports require discipline and strength!" },

    # ------------------ HOBBIES ------------------
    { "keywords": ["hobby", "hobbies"], "reply": "Hobbies help you grow! What do you enjoy doing?" },
    { "keywords": ["cooking"], "reply": "Cooking is both art and science. What's your favorite dish?" },
    { "keywords": ["music"], "reply": "Music makes life better! Who's your favorite artist?" },
    { "keywords": ["reading"], "reply": "Reading expands the mind—fiction or nonfiction?" },

    # ------------------ TRAVEL ------------------
    { "keywords": ["travel", "vacation", "trip"], "reply": "Travel opens your mind! Where do you want to go?" },
    { "keywords": ["beach"], "reply": "Beaches are amazing—sun, sand, and waves 🌊" },
    { "keywords": ["hotel"], "reply": "Looking for hotel suggestions? I can help!" },

    # ------------------ FUN ------------------
    { "keywords": ["comic"], "reply": "Comics are awesome! Marvel or DC?" },
    { "keywords": ["anime"], "reply": "Anime has amazing stories! What's your favorite?" },
    { "keywords": ["manga"], "reply": "Manga fans unite! What are you reading lately?" },
    { "keywords": ["joke"], "reply": "Why did the AI cross the road? To optimize the chicken’s path!" },
    { "keywords": ["riddle"], "reply": "I love riddles! Give me your best one 😄" },

    # ------------------ GAMES ------------------
    { "keywords": ["game", "gaming"], "reply": "Gaming is fun! What do you play?" },
    { "keywords": ["ps5", "playstation"], "reply": "PlayStation has amazing exclusives!" },
    { "keywords": ["xbox"], "reply": "Xbox is awesome for Game Pass users!" },
    { "keywords": ["nintendo", "switch"], "reply": "Nintendo brings pure fun and nostalgia!" },

    # ------------------ BUSINESS ------------------
    { "keywords": ["business"], "reply": "Business is about value, strategy, and innovation." },
    { "keywords": ["startup"], "reply": "Startups thrive on solving real problems creatively!" },
    { "keywords": ["marketing"], "reply": "Marketing is storytelling that sells!" },
    { "keywords": ["finance"], "reply": "Finance helps you manage money wisely." },

    # ------------------ EMOTIONS ------------------
    { "keywords": ["sad"], "reply": "I'm here for you. Want to talk about it?" },
    { "keywords": ["angry"], "reply": "Deep breath… you got this." },
    { "keywords": ["happy"], "reply": "Love that! Happiness is contagious 😄" },

    # ------------------ MULTI-LANGUAGE ------------------
    { "keywords": ["hola"], "reply": "¡Hola! How can I help? 😄" },
    { "keywords": ["bonjour"], "reply": "Bonjour! Comment puis-je vous aider?" },
    { "keywords": ["hallo"], "reply": "Hallo! Wie kann ich helfen?" },
    { "keywords": ["namaste"], "reply": "Namaste! How may I assist you today? 🙏" },
    { "keywords": ["salam", "assalamualaikum"], "reply": "Wa Alaikum Assalam! How can I assist?" },
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
#   API ROUTES
# ============================================================

class AskPayload(BaseModel):
    topic: str
    lang: str = "en"


@app.post("/assistant")
async def assistant(payload: AskPayload):
    predefined = match_predefined_reply(payload.topic)

    if predefined:
        return {
            "type": "predefined",
            "response": predefined
        }

    # Future: Blogger/YouTube/Custom search logic will plug in here
    return {
        "type": "none",
        "response": "No predefined answer or blog match found."
    }


@app.get("/")
async def root():
    return {"status": "ok"}
