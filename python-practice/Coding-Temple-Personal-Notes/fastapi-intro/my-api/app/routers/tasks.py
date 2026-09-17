# app/routers/tasks.py
from fastapi import APIRouter, HTTPException
from app.schemas.task import TaskCreate, TaskResponse, Priority
from datetime import datetime

router = APIRouter(prefix="/tasks", tags=["Tasks"])

tasks_db: list[dict] = []
next_id: int = 1

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    """Create a new task with automatic validation."""
    global next_id
    new_task = {
        "id": next_id,
        **task.model_dump(),            # Convert Pydantic model to dict
        "completed": False,
        "created_at": datetime.now().isoformat()
    }
    tasks_db.append(new_task)
    next_id += 1
    return new_task

@router.get("/", response_model=list[TaskResponse])
def list_tasks(priority: Optional[Priority] = None):
    """List tasks, optionally filtered by priority."""
    if priority:
        return [t for t in tasks_db if t["priority"] == priority]
    return tasks_db

# Add to app/routers/tasks.py - key model.dump(exclude_unset=True)
# this only includes fields the client actually sent, not fields that defaulted to None. So sending {"completed": true} only changes the completed field, leaving everything else untouched.
@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updates: TaskUpdate):
    """Update a task — only provided fields are changed."""
    for task in tasks_db:
        if task["id"] == task_id:
            # Only update fields that were explicitly provided
            update_data = updates.model_dump(exclude_unset=True)
            task.update(update_data)
            return task
    raise HTTPException(status_code=404, detail="Task not found")