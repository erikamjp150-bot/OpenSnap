from typing import List, Dict
from datetime import datetime

# This module manages moderation queue items for HITL review.
# In production, connect this service to the backend database and moderation logs.

moderation_queue: List[Dict] = []


def enqueue_content(content_id: int, content_type: str, preview_text: str, metadata: dict | None = None):
    item = {
        "content_id": content_id,
        "content_type": content_type,
        "preview_text": preview_text,
        "metadata": metadata or {},
        "status": "pending",
        "created_at": datetime.utcnow().isoformat(),
    }
    moderation_queue.append(item)
    return item


def list_pending() -> List[Dict]:
    return [item for item in moderation_queue if item["status"] == "pending"]


def update_status(content_id: int, status: str, reviewer_id: int | None = None):
    for item in moderation_queue:
        if item["content_id"] == content_id:
            item["status"] = status
            item["reviewed_by"] = reviewer_id
            item["reviewed_at"] = datetime.utcnow().isoformat()
            return item
    return None
