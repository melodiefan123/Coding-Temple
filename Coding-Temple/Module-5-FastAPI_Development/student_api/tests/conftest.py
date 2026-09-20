# tests/conftest.py
import pytest
from app.database import Base, SessionLocal, engine, get_db
from main import app
from app.models.user import User  # Adjust import to your user model module


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