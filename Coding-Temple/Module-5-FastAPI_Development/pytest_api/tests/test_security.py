
import pytest
from fastapi import HTTPException
from jose import jwt
from app.config import settings
from app.utils.security import get_current_student  # Adjust import if function name differs
def test_duplicate_email_conflict(client, auth_headers):
    payload = {
        "name": "Duplicate User",
        "email": "unique_dup@example.com",
        "grade_level": 9,
        "is_enrolled": True
    }
    # Create initial student
    res1 = client.post("/students/", json=payload, headers=auth_headers)
    assert res1.status_code in (200, 201)

    # Attempt duplicate student email -> expect 409
    res2 = client.post("/students/", json=payload, headers=auth_headers)
    assert res2.status_code == 409

def test_invalid_malformed_token(client):
    headers = {"Authorization": "Bearer invalid_token_string_123"}
    response = client.get("/students/", headers=headers)
    assert response.status_code == 401

def test_missing_claims_token(client):
    # Pass a validly formatted fake JWT token without 'sub' or valid claims
    fake_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.t-ae1L8232b-3132"
    headers = {"Authorization": f"Bearer {fake_token}"}
    response = client.get("/students/", headers=headers)
    assert response.status_code == 401

def test_duplicate_user_auth_register_conflict(client):
    user_payload = {
        "name": "Dup User",
        "email": "existing@example.com",
        "password": "password123"
    }
    client.post("/auth/register", json=user_payload)
    
    # Second registration with same email expects 409
    res = client.post("/auth/register", json=user_payload)
    assert res.status_code == 409

def test_get_current_student_missing_sub(client):
    """Triggers line 39: payload has no 'sub' claim"""
    token_without_sub = jwt.encode(
        {"some_other_key": "val"},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    headers = {"Authorization": f"Bearer {token_without_sub}"}
    response = client.get("/students/", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


def test_get_current_student_not_found(client):
    """Triggers line 43: valid token format, but user ID 99999 does not exist in DB"""
    token_non_existent_user = jwt.encode(
        {"sub": "99999"},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    headers = {"Authorization": f"Bearer {token_non_existent_user}"}
    response = client.get("/students/", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "User not found"