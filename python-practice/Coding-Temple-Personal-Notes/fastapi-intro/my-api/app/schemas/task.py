# app/schemas/task.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
#Priority enum restricts the field to exactly four values. If someone sends "priority": "urgent", Pydantic rejects it with a message listing the valid options.
class Priority(str, Enum): 
    """Only allow these specific values for priority."""
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    priority: Priority = Priority.medium
    due_date: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: Priority
    due_date: Optional[str]
    completed: bool
    created_at: str

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    priority: Optional[Priority] = None
    due_date: Optional[str] = None
    completed: Optional[bool] = None