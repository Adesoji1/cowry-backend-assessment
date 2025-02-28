import pytest
from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_user_enrollment():
    payload = {
        "email": "adesoji.alu@gmail.com",
        "first_name": "Adesoji",
        "last_name": "Alu"
    }
    response = client.post("/users", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == payload["email"]
    assert "id" in data
