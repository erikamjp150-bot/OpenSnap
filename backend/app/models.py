from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    bio = Column(Text)
    profile_picture_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    sent_snaps = relationship("Snap", foreign_keys="Snap.sender_id", back_populates="sender")
    received_snaps = relationship("Snap", foreign_keys="Snap.recipient_id", back_populates="recipient")
    stories = relationship("Story", back_populates="user")
    interactions = relationship("Interaction", back_populates="user")

class Snap(Base):
    __tablename__ = "snaps"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    media_url = Column(String(500), nullable=False)
    media_type = Column(String(20))  # image, video
    duration = Column(Integer)        # View duration in seconds
    is_viewed = Column(Boolean, default=False)
    viewed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)  # Auto-delete after viewing
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_snaps")
    recipient = relationship("User", foreign_keys=[recipient_id], back_populates="received_snaps")

class Story(Base):
    __tablename__ = "stories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    media_url = Column(String(500), nullable=False)
    media_type = Column(String(20))
    caption = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)  # 24-hour expiry
    is_private = Column(Boolean, default=False)    # Private stories (close friends)
    
    # Relationships
    user = relationship("User", back_populates="stories")

class Interaction(Base):
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_id = Column(Integer, nullable=False)    # Story ID or Snap ID
    content_type = Column(String(20))               # 'story', 'snap', 'feed_item'
    action = Column(String(20))                     # 'view', 'like', 'share', 'watch_time'
    value = Column(Integer)                         # e.g., seconds watched
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="interactions")

class ModerationLog(Base):
    __tablename__ = "moderation_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, nullable=False)
    content_type = Column(String(20))
    status = Column(String(20))                     # 'pending', 'approved', 'rejected'
    ai_score = Column(JSON)                         # {'violence': 0.95, 'hate_speech': 0.10}
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
