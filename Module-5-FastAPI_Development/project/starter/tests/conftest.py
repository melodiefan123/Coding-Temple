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
    pass  # TODO: implement
