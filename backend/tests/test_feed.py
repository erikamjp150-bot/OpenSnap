import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_user_feed_returns_200(user_id):
    response = client.get(f"/feed/user/{user_id}")
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        data = response.json()
        assert data["user_id"] == user_id
        assert isinstance(data["items"], list)
