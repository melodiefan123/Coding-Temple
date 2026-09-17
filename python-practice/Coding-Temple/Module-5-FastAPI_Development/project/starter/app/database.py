# project/starter/app/database.py
# Module 5 Project — Database setup
#
# TODO: Configure SQLAlchemy and implement the get_db dependency.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from typing import Generator
import os

# TODO: Load DATABASE_URL from environment (use python-dotenv or os.getenv)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./taskmanager.db")

# TODO: Create the engine
engine = create_engine(DATABASE_URL)

# TODO: Create SessionLocal
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# TODO: Implement get_db
def get_db() -> Generator[Session, None, None]:
    """Provides a DB session per request lifecycle."""
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()
