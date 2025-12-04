from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from .assistant import get_predefined_or_blog_response
from .admin.routes import router as admin_router
import os

app = FastAPI(title="Blogger Assistant")

# Include admin router under /admin
app.include_router(admin_router, prefix="/admin", tags=["admin"])

# Allow simple CORS for testing; tune in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=JSONResponse)
def root():
    return {"status": "ok"}

@app.get("/health", response_class=PlainTextResponse)
def health():
    return "ok"

@app.post("/assistant")
async def assistant_endpoint(payload: dict):
    topic = (payload.get("topic") or "").strip()
    lang = payload.get("lang", "en")
    if not topic:
        return JSONResponse({"type": "error", "response": "Missing topic"}, status_code=400)

    result = get_predefined_or_blog_response(topic, lang)
    return JSONResponse(result)

# Optional: global exception handler to ensure errors get logged and return 500
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # In production, log the exception to a structured logger
    return JSONResponse({"detail": "Internal server error"}, status_code=500)
