from fastapi import APIRouter
from pydantic import BaseModel
from responses import PREDEFINED_REPLIES
from blog_lookup import fetch_blogger_post_content

router = APIRouter()

class AskPayload(BaseModel):
    topic: str
    lang: str = "en"

def match_predefined_reply(text: str):
    text = text.lower().strip()
    for item in PREDEFINED_REPLIES:
        for word in item["keywords"]:
            if word in text:
                return item["reply"]
    return None

@router.post("/assistant")
async def assistant(payload: AskPayload):
    # 1️⃣ Predefined reply
    predefined = match_predefined_reply(payload.topic)
    if predefined:
        return {"type": "predefined", "response": predefined}

    # 2️⃣ Blogger fallback
    blog_post = fetch_blogger_post_content(payload.topic)
    if blog_post:
        return {"type": "blog", "title": blog_post["title"], "response": blog_post["content"]}

    # 3️⃣ Fallback
    return {"type": "none", "response": "No predefined answer or blog post found."}
