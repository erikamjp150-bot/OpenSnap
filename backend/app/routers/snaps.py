from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from ..models import Snap, User

router = APIRouter()

class SnapResponse(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    media_url: str
    media_type: str
    duration: int | None = None
    is_viewed: bool
    created_at: str
    expires_at: str

    class Config:
        orm_mode = True


@router.get("/", response_model=list[SnapResponse])
def list_snaps(db: Session = Depends(get_db)):
    snaps = db.query(Snap).order_by(Snap.created_at.desc()).limit(50).all()
    return snaps


@router.get("/{snap_id}", response_model=SnapResponse)
def get_snap(snap_id: int, db: Session = Depends(get_db)):
    snap = db.query(Snap).filter(Snap.id == snap_id).first()
    if not snap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Snap not found")
    return snap
