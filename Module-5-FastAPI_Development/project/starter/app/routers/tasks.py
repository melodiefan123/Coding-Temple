# project/starter/app/routers/tasks.py
# Module 5 Project — Task endpoints (auth-scoped)
#
# TODO: Implement full task CRUD, all endpoints protected by get_current_user
# All queries must filter by current_user.id (users can only see their own tasks)

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.schemas.task import TaskCreate, TaskPatch, TaskResponse
from app.database import get_db

router = APIRouter()


# TODO: POST /tasks
@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    pass


# TODO: GET /tasks
@router.get("/", response_model=list[TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    pass


# TODO: GET /tasks/{task_id}
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    pass


# TODO: PATCH /tasks/{task_id}
@router.patch("/{task_id}", response_model=TaskResponse)
def patch_task(task_id: int, task_data: TaskPatch, db: Session = Depends(get_db)):
    pass


# TODO: DELETE /tasks/{task_id}
@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    pass


# TODO: GET /tasks/{task_id}/suggest — placeholder for AI suggestion
@router.get("/{task_id}/suggest")
def suggest_task_action(task_id: int, db: Session = Depends(get_db)):
    """
    Placeholder endpoint for AI-powered task suggestions.
    TODO: Return a mock suggestion dict.
    """
    pass
