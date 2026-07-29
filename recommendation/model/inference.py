from typing import Any
from pydantic import BaseModel, Field, ValidationError
from fastapi import FastAPI, HTTPException, Query
from datetime import datetime, timedelta
import os

app = FastAPI(
    title="OpenSnap Recommendation Inference",
    description="Lightweight inference API for OpenSnap recommendations",
    version="0.1.0"
)

class RecommendationRequest(BaseModel):
    user_id: int = Field(..., gt=0)

class RecommendationItem(BaseModel):
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

class RecommendationResponse(BaseModel):
    user_id: int
    items: list[RecommendationItem]


def load_model() -> Any:
    # Placeholder for PyTorch model loading and Hopsworks feature retrieval.
    # In production, load a trained user-item ranking model here.
    return None

model = load_model()


def build_recommendations(user_id: int) -> list[dict]:
    now = datetime.utcnow()
    return [
        {
            "id": user_id * 100 + i,
            "type": "feed_item",
            "sender_id": None,
            "user_id": user_id,
            "media_url": f"https://cdn.opensnap.org/recommendations/{user_id}/{i}.jpg",
            "media_type": "image",
            "caption": f"OpenSnap trending story {i}",
            "created_at": (now - timedelta(minutes=i * 10)).isoformat(),
            "expires_at": (now + timedelta(hours=12)).isoformat(),
            "score": 0.6 + (0.1 * (5 - i)),
        }
        for i in range(1, 6)
    ]


@app.get("/infer", response_model=RecommendationResponse)
async def infer(user_id: int = Query(..., gt=0)):
    try:
        request = RecommendationRequest(user_id=user_id)
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=exc.errors())

    items = build_recommendations(request.user_id)
    return RecommendationResponse(user_id=request.user_id, items=items)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "opensnap-recommendation"}
