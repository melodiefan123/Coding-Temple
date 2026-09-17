# project/starter/app/models/user.py
# Module 5 Project — User model
#
# TODO: Define the User ORM model
# Fields: id, username (unique), email (unique), hashed_password
# Relationship: one user has many tasks

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import String, Column, Integer, Boolean, DateTime
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    # TODO: Add columns
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(500), unique=True)
    hashed_password: Mapped[str] = mapped_column(String())
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime]=mapped_column(DateTime, server_default=func.now())
    # TODO: Add relationship to Task (tasks = relationship("Task", back_populates="owner"))
    tasks: Mapped[list["Task"]] = relationship(back_populates="owner")
