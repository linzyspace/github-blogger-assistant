from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.assistant import get_predefined_or_blog_response

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
    return get_predefined_or_blog_response(query)

@app.get("/")
async def root():
    return {"status": "ok"}
