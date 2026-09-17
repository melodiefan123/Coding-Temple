from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), index=True)
    email = Column(String, unique=True, index=True)
    grade_level = Column(Integer, index=True, nullable=True)
    gpa = Column(Float, nullable=True)
    is_enrolled = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

