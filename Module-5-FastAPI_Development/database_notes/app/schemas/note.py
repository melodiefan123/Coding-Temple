from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200, description="The title of the note")
    content: str = Field(min_length=1, description="The content of the note")
    category: Optional[str] = Field(None, min_length=1, max_length=50, description="The category of the note")
    is_pinned: bool = Field(False, description="Whether the note is pinned")

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    category: Optional[str]
    is_pinned: bool
    created_at: datetime

    class Config:
        from_attributes = True