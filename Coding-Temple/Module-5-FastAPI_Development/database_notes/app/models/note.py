from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    content = Column(String)
    category = Column(String(50), index=True, nullable=True)
    is_pinned = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
