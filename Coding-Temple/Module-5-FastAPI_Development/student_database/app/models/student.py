from sqlalchemy import Column, Float, Integer, String
from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    major = Column(String, nullable=True, index=True)
    gpa = Column(Float, nullable=True)