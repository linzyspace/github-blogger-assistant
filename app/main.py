from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ------------------------------
# CORS FIX (Blogger requires this)
# ------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],  
    allow_headers=["*"],  
    allow_credentials=False,
)

# ------------------------------
# Predefined Questions & Answers
# ------------------------------
PREDEFINED_QA = {
    "hello": "Hello! How can I help you today?",
    "who are you": "I am your Blogger AI Assistant!",
    "what is this blog about": "This blog shares articles on various topics depending on the author.",
    
    # Add your own custom Q&A
    "contact": "You can contact the blog owner through the Contact Form.",
    "about author": "The author writes about tech, lifestyle, and more.",
}

def search_predefined(question: str):
    """Return predefined answer if found."""
    question = question.lower().strip()

    # Exact match
    if question in PREDEFINED_QA:
        return PREDEFINED_QA[question]

    # Keyword / partial matching
    for key, value in PREDEFINED_QA.items():
        if key in question:
            return value

    return None


# ------------------------------------
# Payload model from Blogger widget
# ------------------------------------
class AskPayload(BaseModel):
    topic: str
    blogContent: str = ""   # will be sent by widget
    lang: str = "en"


# ------------------------------------
# Assistant Endpoint
# ------------------------------------
@app.post("/assistant")
async def assistant_endpoint(payload: AskPayload):
    user_question = payload.topic

    # 1. Check predefined answers first
    predefined_answer = search_predefined(user_question)
    if predefined_answer:
        return {
            "type": "predefined",
            "response": predefined_answer,
        }

    # 2. If no predefined, try blog content AI processing
    result = get_blog_based_answer(payload.topic, payload.blogContent)

    if result:
        return {
            "type": "blog",
            "response": result,
        }

    # 3. Nothing found
    return {
        "type": "none",
        "response": "No predefined answer or blog match found.",
    }


# ------------------------------------
# Dummy blog content analyzer (Replace with your logic)
# ------------------------------------
def get_blog_based_answer(question: str, blog_text: str):
    """
    Add any logic here:
    - Embedding search
    - LLM call
    - Keyword matching
    """
    if not blog_text.strip():
        return None

    # Example simple match:
    if question.lower() in blog_text.lower():
        return "I found something related to your question in the blog content."

    return None


# ------------------------------------
# Root endpoint
# ------------------------------------
@app.get("/")
async def root():
    return {"status": "ok"}
