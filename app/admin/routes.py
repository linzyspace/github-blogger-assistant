from fastapi import APIRouter
from pydantic import BaseModel
from .assistant import process_user_message

router = APIRouter()

class AskPayload(BaseModel):
    topic: str
    lang: str = "en"


@router.post("/assistant")
async def assistant_route(payload: AskPayload):
    result = await process_user_message(payload.topic, payload.lang)
    return result
