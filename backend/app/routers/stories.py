from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from ..models import Story

router = APIRouter()

class StoryResponse(BaseModel):
    id: int
    user_id: int
    media_url: str
    media_type: str
    caption: str | None = None
    created_at: str
    expires_at: str
    is_private: bool

    class Config:
        orm_mode = True


@router.get("/", response_model=list[StoryResponse])
def list_stories(db: Session = Depends(get_db)):
    stories = db.query(Story).order_by(Story.created_at.desc()).limit(50).all()
    return stories


@router.get("/{story_id}", response_model=StoryResponse)
def get_story(story_id: int, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")
    return story
