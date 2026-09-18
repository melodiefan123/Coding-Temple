# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from app.database import Base, get_db
from sqlalchemy.pool import StaticPool


TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass = StaticPool)
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def auth_headers(client):
    response = client.post("/auth/register", json={
        "name": "student1",
        "email": "student1@email.com",
        "password": "testpassword",
    })
    token = response.json()['access_token']
    return ({"Authorization": f"Bearer {token}"}, client)
    

@pytest.fixture
def sample_student(auth_headers):
    """Create and return a sample student for tests that need existing data."""
    client = auth_headers[1]
    response = client.post("/students", headers=auth_headers[0],json={
        "name": "student2",
        "email": "student2@email.com",
        "grade_level": 8, 
        "gpa": 3.5, 
        "is_enrolled": False
    })
    return response.json()