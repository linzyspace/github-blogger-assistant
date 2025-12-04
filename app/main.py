from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.assistant import get_predefined_or_blog_response

app = FastAPI()

# ------------------------------
# CORS FIX (Blogger requires this)
# ------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # allow Blogger
    allow_methods=["*"],            # allow POST
    allow_headers=["*"],            # allow JSON
    allow_credentials=False,
)

class AskPayload(BaseModel):
    topic: str
    lang: str = "en"

@app.post("/assistant")
async def assistant_endpoint(payload: AskPayload):
    result = get_predefined_or_blog_response(payload.topic, payload.lang)

    if result:
        return result

    return {
        "type": "none",
        "response": "No predefined answer or blog match found."
    }

@app.get("/")
async def root():
    return {"status": "ok"}
