import pytest
from fastapi.testclient import TestClient
from recommendation.model.inference import app

client = TestClient(app)

def test_infer_endpoint_valid_user():
    response = client.get("/infer?user_id=1")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert len(data["items"]) == 5
    assert all("media_url" in item for item in data["items"])

def test_infer_endpoint_invalid_user():
    response = client.get("/infer?user_id=0")
    assert response.status_code == 422
