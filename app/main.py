from fastapi import FastAPI
from assistant import router as assistant_router

app = FastAPI(title="Blogger Assistant")

# Include the assistant routes
app.include_router(assistant_router)

@app.get("/")
async def root():
    return {"status": "ok"}
