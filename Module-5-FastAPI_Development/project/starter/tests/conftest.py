# project/starter/tests/conftest.py
# Module 5 Project — Test fixture skeleton

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture
def client():
    """
    TODO: Implement the test client fixture with DB override.
    Same pattern as L11 — see solutions/test-suite/tests/conftest.py for reference.
    """
     # TODO: implement
    Base.metadata.create_all(bind=test_engine)
    
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def auth_headers(client):
    response = client.post("/auth/register", json={
        "username": "test1",
        "email": "test1@email.com",
        "password": "testpassword",
    })
    token = response.json()['access_token']
    return ({"Authorization": f"Bearer {token}"}, client)

@pytest.fixture
def sample_task(auth_headers):
    """Create and return a sample user for tests that need existing data."""
    client = auth_headers[1]
    response = client.post("/tasks", headers=auth_headers[0],json={
            "title": "task1",
            "description": "things to do",
            "priority": "medium", 
            "completed": False,
    })
    return response.json()
