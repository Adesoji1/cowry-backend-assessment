import pytest
from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_add_and_remove_book():
 
    book_payload = {
        "title": "New Admin Book",
        "publisher": "Manning",
        "category": "technology"
    }
    response = client.post("/books", json=book_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Admin Book"

    book_id = data["id"]

    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    assert "removed successfully" in response.json()["detail"]
