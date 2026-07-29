from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, snaps, stories, feed
from .database import engine
from . import models

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="OpenSnap API",
    description="Open-source Snapchat alternative backend",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(snaps.router, prefix="/snaps", tags=["snaps"])
app.include_router(stories.router, prefix="/stories", tags=["stories"])
app.include_router(feed.router, prefix="/feed", tags=["feed"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "opensnap-backend"}
