import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_duplicate_student():
    student_data = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "grade_level": 10,
        "gpa": 3.8,
        "is_enrolled": True
    }
    # First creation -> 201
    res1 = client.post("/students/", json=student_data)
    assert res1.status_code == 201

    # Duplicate creation -> 409
    res2 = client.post("/students/", json=student_data)
    assert res2.status_code == 409
    data = res2.json()
    assert data["error"] == "Duplicate Entry"
    assert data["status_code"] == 409

def test_get_nonexistent_student_returns_404():
    res = client.get("/students/999999")
    assert res.status_code == 404
    data = res.json()
    assert data["error"] == "Not Found"
    assert data["status_code"] == 404

def test_delete_enrolled_student_raises_validation_error():
    # Create student
    res = client.post("/students/", json={
        "name": "Alex Smith",
        "email": "alex@example.com",
        "is_enrolled": True
    })
    student_id = res.json()["id"]

    # Delete enrolled student -> 422 AppValidationError
    del_res = client.delete(f"/students/{student_id}")
    assert del_res.status_code == 422
    data = del_res.json()
    assert data["error"] == "Validation Error"
    assert data["status_code"] == 422