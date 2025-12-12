from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.assistant import (
    get_predefined_response,
    get_blog_post_response
)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

class AskPayload(BaseModel):
    topic: str
    lang: str = "en"

@app.post("/assistant")
async def assistant(payload: AskPayload):
    query = payload.topic.strip()

    # 1) Attempt predefined lookup
    predefined = get_predefined_response(query)
    if predefined:
        return {"source": "predefined", "response": predefined}

    # 2) Fallback to blog post lookup
    blog_post = await get_blog_post_response(query)
    if blog_post:
        return {"source": "blog", "response": blog_post}

    # 3) Nothing found
    return {
        "source": "none",
        "response": f"No predefined answer or blog post found for '{query}'."
    }

@app.get("/")
async def root():
    return {"status": "ok"}
