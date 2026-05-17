# project/starter/app/schemas/task.py
# Module 5 Project — Task schemas
#
# TODO: Define TaskCreate, TaskPatch, TaskResponse

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from app.models.task import Priority


class TaskCreate(BaseModel):
    """Input for creating a task."""
     # TODO: title, description (optional), completed (default False)
    title: str = Field(min_length=1, max_length=200, description="title of task", examples=["Do Module 1"])
    description: Optional[str] = Field(None, max_length=2000, description="Optional Description for task", examples=["From Coding Temple"])
    completed: bool = Field(default=False)
    priority: Priority = Field(default=Priority.low)


class TaskPatch(BaseModel):
    """Input for partial task update."""
    # TODO: all Optional fields
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="title of task")
    description: Optional[str] = Field(None, min_length=1, max_length=2000, description="Optional Description for task")
    completed: Optional[bool] = Field(default=False)
    priority: Optional[Priority] = Field(default=Priority.low)

class TaskResponse(TaskCreate):
    """Returned to clients."""
    # TODO: id, owner_id + model_config
    id: int =Field(examples=[1])
    user_id: int=Field(examples=[1])
    model_config = ConfigDict(from_attributes=True)
