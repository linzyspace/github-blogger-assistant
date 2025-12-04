from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List
import uuid

router = APIRouter()

# Simple in-memory store for demo; replace with DB in production
_posts = []

class PostCreate(BaseModel):
    title: str
    content: str
    category: str | None = None

class PostOut(PostCreate):
    id: str

@router.post("/posts", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate):
    post = payload.dict()
    post["id"] = str(uuid.uuid4())
    _posts.append(post)
    return post

@router.get("/posts", response_model=List[PostOut])
def list_posts():
    return _posts

@router.get("/posts/{post_id}", response_model=PostOut)
def get_post(post_id: str):
    for p in _posts:
        if p["id"] == post_id:
            return p
    raise HTTPException(status_code=404, detail="Post not found")
