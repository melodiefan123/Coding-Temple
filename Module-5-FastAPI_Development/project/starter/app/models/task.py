# project/starter/app/models/task.py
# Module 5 Project — Task model
#
# TODO: Define the Task ORM model
# Fields: id, title, description (optional), completed (bool, default False), owner_id (FK)
# Relationship: task belongs to a user

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import String, Boolean, ForeignKey, Column, Integer
from typing import Optional
from app.database import Base
from enum import Enum
from sqlalchemy import Enum as SAEnum, DateTime
from datetime import datetime
class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Task(Base):
    __tablename__ = "tasks"

    # TODO: Add columns
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(2000))
    priority: Mapped[Priority] = mapped_column(SAEnum(Priority))
    completed: Mapped[bool]=mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"]= relationship(back_populates="tasks")
    created_at: Mapped[datetime]=mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

  