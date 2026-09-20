import os
import pytest
from fastapi.testclient import TestClient

# Adjust imports to match your project structure
from main import app
from app.database import Base, get_db, engine, SessionLocal
from app.models.user import User
from app.utils.security import create_access_token, hash_password

ACTIVITY_LOG = "activity_log.txt"
NOTIFICATION_LOG = "notification_log.txt"


@pytest.fixture(autouse=True)
def clean_log_files():
    """Remove log files before and after each test to ensure a clean state."""
    for filepath in [ACTIVITY_LOG, NOTIFICATION_LOG]:
        if os.path.exists(filepath):
            os.remove(filepath)
    yield
    for filepath in [ACTIVITY_LOG, NOTIFICATION_LOG]:
        if os.path.exists(filepath):
            os.remove(filepath)


# tests/test_notifications.py

@pytest.fixture
def auth_headers(setup_test_db, db_session):
    """Creates a mock user and returns a Bearer Authorization header."""
    user = User(
        email="testuser@example.com",
        hashed_password=hash_password("password123"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    token = create_access_token(data={"sub": str(user.id)})
    return {"Authorization": f"Bearer {token}"}


def test_post_student_triggers_background_logs(client: TestClient, auth_headers: dict):
    """Verify POST /students creates a record, logs activity, and sends notification."""
    payload = {
        "name": "Jane Doe",
        "email": "janedoe@example.com",
        "grade_level": 10,
        "gpa": 3.8,
        "is_enrolled": False,
    }

    response = client.post("/students/", json=payload, headers=auth_headers)
    assert response.status_code == 201

    # Verify activity_log.txt created and populated
    assert os.path.exists(ACTIVITY_LOG)
    with open(ACTIVITY_LOG, "r") as f:
        activity_content = f.read()
        assert "CREATED_STUDENT_RECORD_ID_" in activity_content

    # Verify notification_log.txt created and populated
    assert os.path.exists(NOTIFICATION_LOG)
    with open(NOTIFICATION_LOG, "r") as f:
        notification_content = f.read()
        assert "janedoe@example.com" in notification_content
        assert "was created successfully" in notification_content


def test_delete_student_triggers_activity_log(client: TestClient, auth_headers: dict):
    """Verify DELETE /students/{id} logs the deletion activity."""
    # 1. Create an unenrolled student directly or via API
    payload = {
        "name": "Alex Smith",
        "email": "alex@example.com",
        "grade_level": 11,
        "gpa": 3.5,
        "is_enrolled": False,
    }
    create_res = client.post("/students/", json=payload, headers=auth_headers)
    student_id = create_res.json()["id"]

    # Clear log created during post step to isolate the delete test
    if os.path.exists(ACTIVITY_LOG):
        os.remove(ACTIVITY_LOG)

    # 2. Delete the student
    delete_res = client.delete(f"/students/{student_id}", headers=auth_headers)
    assert delete_res.status_code == 204

    # 3. Assert activity log contains deletion record
    assert os.path.exists(ACTIVITY_LOG)
    with open(ACTIVITY_LOG, "r") as f:
        activity_content = f.read()
        assert f"DELETED_STUDENT_RECORD_ID_{student_id}" in activity_content