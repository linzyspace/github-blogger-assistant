from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from app.assistant import get_predefined_or_blog_response
from app.admin.routes import router as admin_router

app = FastAPI(title="Blogger Assistant")

# Include admin router
app.include_router(admin_router, prefix="/admin", tags=["admin"])

@app.get("/", response_class=JSONResponse)
def root():
    return {"status": "ok"}

@app.get("/health", response_class=PlainTextResponse)
def health():
    return "ok"

@app.post("/assistant")
def assistant_endpoint(payload: dict):
    topic = (payload.get("topic") or "").strip()
    lang = payload.get("lang", "en")
    if not topic:
        return JSONResponse({"type": "error", "response": "Missing topic"}, status_code=400)
    result = get_predefined_or_blog_response(topic, lang)
    return JSONResponse(result)
