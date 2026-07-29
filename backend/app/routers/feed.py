from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from ..database import get_db
from ..models import User, Story, Snap, Interaction
from ..config import settings
from datetime import datetime, timedelta
import requests

router = APIRouter()

class FeedItem(BaseModel):
    id: int
    type: str
    sender_id: int | None = None
    user_id: int | None = None
    media_url: str
    media_type: str
    caption: str | None = None
    created_at: datetime
    expires_at: datetime
    score: float = Field(..., ge=0.0, le=1.0)

class FeedResponse(BaseModel):
    user_id: int
    items: List[FeedItem]


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


@router.get("/user/{user_id}", response_model=FeedResponse)
async def get_user_feed(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Fetch recent stories from friends and suggested content via recommendation service
    stories = (
        db.query(Story)
        .filter(Story.is_private == False, Story.expires_at > datetime.utcnow())
        .order_by(Story.created_at.desc())
        .limit(20)
        .all()
    )

    # Minimal graph-based social feed: recent snaps received by this user
    snaps = (
        db.query(Snap)
        .filter(Snap.recipient_id == user_id, Snap.expires_at > datetime.utcnow())
        .order_by(Snap.created_at.desc())
        .limit(10)
        .all()
    )

    recommended_items = []
    try:
        response = requests.get(
            f"{settings.RECOMMENDATION_API_URL}/infer?user_id={user_id}",
            timeout=2,
        )
        if response.status_code == 200:
            recommended_items = response.json().get("items", [])
    except requests.RequestException:
        recommended_items = []

    feed_items = []
    for story in stories:
        feed_items.append(
            FeedItem(
                id=story.id,
                type="story",
                user_id=story.user_id,
                media_url=story.media_url,
                media_type=story.media_type,
                caption=story.caption,
                created_at=story.created_at,
                expires_at=story.expires_at,
                score=0.8,
            )
        )

    for snap in snaps:
        feed_items.append(
            FeedItem(
                id=snap.id,
                type="snap",
                sender_id=snap.sender_id,
                media_url=snap.media_url,
                media_type=snap.media_type,
                created_at=snap.created_at,
                expires_at=snap.expires_at,
                score=0.9,
            )
        )

    for item in recommended_items:
        if item.get("type") in {"story", "snap", "feed_item"}:
            feed_items.append(
                FeedItem(
                    id=item.get("id", 0),
                    type=item.get("type"),
                    sender_id=item.get("sender_id"),
                    user_id=item.get("user_id"),
                    media_url=item.get("media_url", ""),
                    media_type=item.get("media_type", "image"),
                    caption=item.get("caption"),
                    created_at=datetime.fromisoformat(item.get("created_at")) if item.get("created_at") else datetime.utcnow(),
                    expires_at=datetime.fromisoformat(item.get("expires_at")) if item.get("expires_at") else datetime.utcnow() + timedelta(hours=24),
                    score=float(item.get("score", 0.5)),
                )
            )

    # Sort combined feed by score and recency
    sorted_feed = sorted(feed_items, key=lambda item: (item.score, item.created_at), reverse=True)
    limited_feed = sorted_feed[:30]

    return FeedResponse(user_id=user_id, items=limited_feed)
