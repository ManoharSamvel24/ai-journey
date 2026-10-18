from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_summarize_valid():
    response = client.post("/summarize", json={"text": "hello world"})
    assert response.status_code == 200
    assert "summary" in response.json()


def test_summarize_empty():
    response = client.post("/summarize", json={"text": "   "})
    assert response.status_code == 400
    assert response.json()["detail"] == "Text cannot be empty"