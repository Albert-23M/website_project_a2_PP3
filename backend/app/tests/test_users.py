import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_database():
    pass

def test_read_top5_matched_users(mock_database):
    keyword = "userTest"
    response = client.get(f"/api/v1/users/{keyword}")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    data = response.json()

    assert "data" in data
    assert isinstance(data["data"], list)

    if len(data["data"]) > 0:
        user = data["data"][0]
        assert "id_user" in user
        assert "name" in user
        assert "surname" in user
        assert "username" in user
        assert "email" in user

def test_read_users(mock_database):
    skip = 0
    limit = 10
    
    response = client.get(f"/api/v1/users/?skip={skip}&limit={limit}")
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    
    data = response.json()
    
    assert "data" in data
    assert isinstance(data["data"], list)
    assert isinstance(data["count"], int)
    assert len(data["data"]) <= limit
    
    if len(data["data"]) > 0:
        user = data["data"][0]
        assert "id_user" in user
        assert "name" in user
        assert "surname" in user
        assert "username" in user
        assert "email" in user



