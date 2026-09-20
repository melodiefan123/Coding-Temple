import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. Import database and FastAPI application
from app.database import Base, get_db
from main import app as fastapi_app

# 2. Import your SQLAlchemy models so Base knows about all tables
import app.models  # Ensure this points to your models module/package

# 3. Setup SQLite in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# 4. Apply override directly on the alias
fastapi_app.dependency_overrides[get_db] = override_get_db

# 5. Initialize TestClient with the alias
client = TestClient(fastapi_app)


# 6. Database Fixture (Placed BEFORE test execution)
@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# 7. Test Cases
def test_register_user():
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "secretpassword"},
    )
    assert response.status_code == 201


def test_login_user():
    # Register user first so login succeeds
    client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "secretpassword"},
    )

    # Send JSON body matching LoginRequest (email & password)
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "secretpassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"