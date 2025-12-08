from fastapi import APIRouter, Request
from app.admin.validators import validate_admin_key

router = APIRouter()

@router.post("/add-response")
async def add_response(request: Request):
    validate_admin_key(request)
    return {"status": "ok", "message": "Response added (placeholder)"}


@router.get("/status")
async def admin_status():
    return {"admin": "online"}
