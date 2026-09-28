from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class Genre(str, Enum):
    fiction = "fiction"
    nonfiction = "nonfiction"
    science = "science"
    history = "history"


class Book(BaseModel):
    id: int
    title: str
    author: str
    genre: Genre
    year: int