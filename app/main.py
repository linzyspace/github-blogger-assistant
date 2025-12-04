from fastapi import FastAPI, Request
from app.assistant import get_predefined_or_blog_response
from app.admin.routes import router as admin_router

app = FastAPI()


@app.get("/")
def root():
    return {"status": "running"}


@app.post("/assistant")
async def assistant(request: Request):
    payload = await request.json()
    topic = payload.get("topic", "").strip()
    lang = payload.get("lang", "en")

    if not topic:
        return {"type": "error", "response": "Missing topic"}

    result = get_predefined_or_blog_response(topic, lang)

    if result:
        return result

    return {
        "type": "none",
        "response": "No predefined answer or blog post match found."
    }


# Register /admin routes
app.include_router(admin_router, prefix="/admin")
