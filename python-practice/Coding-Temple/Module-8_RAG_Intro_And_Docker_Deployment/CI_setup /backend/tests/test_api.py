from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
# Test that / returns 200
def test_root():
    response = client.get("/")
    assert response.status_code == 200
# Test that /health returns 200 with expected fields
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data or "chromadb" in data
# Test that /stats returns 200 with a document_count field
def test_stats():
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert "document_count" in data