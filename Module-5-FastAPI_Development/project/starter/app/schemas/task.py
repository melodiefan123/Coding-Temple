# project/starter/app/schemas/task.py
# Module 5 Project — Task schemas
#
# TODO: Define TaskCreate, TaskPatch, TaskResponse

from pydantic import BaseModel, ConfigDict
from typing import Optional


class TaskCreate(BaseModel):
    """Input for creating a task."""
    pass  # TODO: title, description (optional), completed (default False)


class TaskPatch(BaseModel):
    """Input for partial task update."""
    pass  # TODO: all Optional fields


class TaskResponse(TaskCreate):
    """Returned to clients."""
    pass  # TODO: id, owner_id + model_config
