from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as main_router

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

# API routes
app.include_router(main_router)

@app.get("/")
async def root():
    return {"status": "ok"}
