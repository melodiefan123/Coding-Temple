# project/starter/app/models/user.py
# Module 5 Project — User model
#
# TODO: Define the User ORM model
# Fields: id, username (unique), email (unique), hashed_password
# Relationship: one user has many tasks

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.database import Base


class User(Base):
    __tablename__ = "users"

    # TODO: Add columns
    # TODO: Add relationship to Task (tasks = relationship("Task", back_populates="owner"))
    pass
