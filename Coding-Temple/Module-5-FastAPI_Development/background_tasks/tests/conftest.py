# tests/conftest.py
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from app.database import Base, SessionLocal, engine, get_db
from app.models.user import User  # Adjust import to your user model module
from main import app


def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_test_db():
    # Override app's database dependency for test routes
    app.dependency_overrides[get_db] = override_get_db

    # Create tables
    Base.metadata.create_all(bind=engine)

    yield

    # Teardown
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture  # <--- ADD THIS DECORATOR
def client():
    """Provides a TestClient instance for API tests."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def db_session():
    """Provides a transactional database session for tests."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()