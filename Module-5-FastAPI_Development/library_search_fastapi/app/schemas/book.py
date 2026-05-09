from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class Genre(str, Enum):
    fiction = "Fiction"
    nonfiction = "Non-Fiction"
    science = "Science"
    history = "History"


class Book(BaseModel):
    id: int
    title: str
    author: str
    genre: Genre
    year: int