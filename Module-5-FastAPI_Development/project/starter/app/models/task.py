# project/starter/app/models/task.py
# Module 5 Project — Task model
#
# TODO: Define the Task ORM model
# Fields: id, title, description (optional), completed (bool, default False), owner_id (FK)
# Relationship: task belongs to a user

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey
from typing import Optional
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    # TODO: Add columns
    # TODO: Add owner_id ForeignKey to users.id
    # TODO: Add relationship to User (owner = relationship("User", back_populates="tasks"))
    pass
