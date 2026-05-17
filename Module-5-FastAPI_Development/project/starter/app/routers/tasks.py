# project/starter/app/routers/tasks.py
# Module 5 Project — Task endpoints (auth-scoped)
#
# TODO: Implement full task CRUD, all endpoints protected by get_current_user
# All queries must filter by current_user.id (users can only see their own tasks)

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.schemas.task import TaskCreate, TaskPatch, TaskResponse
from app.database import get_db
from app.auth import get_current_user, create_access_token
from app.models import Task
from app.exceptions import ForbiddenException, NotFoundException

router = APIRouter()

def log_task_created(user_id: int, task_title: str):
    print(f"User {user_id} created task: '{task_title}'")
# TODO: POST /tasks
@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, background_tasks: BackgroundTasks,db: Session = Depends(get_db), current_user = Depends(get_current_user)):
        """Creates a new task for the authenticated user."""
        task = Task(
            title = task.title,
            description = task.description,
            priority = task.priority, 
            completed = task.completed, 
            user_id = current_user.id
        )
        background_tasks.add_task(log_task_created,current_user.id, task.title)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task


# TODO: GET /tasks
@router.get("/", response_model=list[TaskResponse])
def list_tasks(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Lists all tasks for the authenticated user."""

    query = db.query(Task).filter( current_user.id== Task.user_id).all()
    return query


# TODO: GET /tasks/{task_id}
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Gets a specific task for the authenticated user."""
    task = db.query(Task).filter(task_id ==Task.id).first()
    if not task:  # checks if task exists
        raise NotFoundException("Task", task_id)
    if task.user_id != current_user.id:  # checks ownership
        raise ForbiddenException(task.user_id)
    return task
        
    


# TODO: PATCH /tasks/{task_id}
@router.patch("/{task_id}", response_model=TaskResponse)
def patch_task(task_id: int, task_data: TaskPatch, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """partially update the task for the authenticated user."""

    db_task = db.query(Task).filter(task_id ==Task.id).first()
    if not db_task:  # checks if task exists
        raise NotFoundException("Task", task_id)
    if db_task.user_id != current_user.id:  # checks ownership
        raise ForbiddenException(db_task.user_id)
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task


# TODO: DELETE /tasks/{task_id}
@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Deletes a task for the authenticated user."""

    db_task = db.query(Task).filter(task_id ==Task.id).first()
    if not db_task:  # checks if task exists
        raise NotFoundException("Task", task_id)
    if db_task.user_id != current_user.id:  # checks ownership
        raise ForbiddenException(db_task.user_id)
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}


# TODO: GET /tasks/{task_id}/suggest — placeholder for AI suggestion
@router.get("/{task_id}/suggest")
def suggest_task_action(task_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Placeholder endpoint for AI-powered task suggestions.
    """
    db_task = db.query(Task).filter(task_id ==Task.id).first()
    if not db_task:  # checks if task exists
        raise NotFoundException("Task", task_id)
    if db_task.user_id != current_user.id:  # checks ownership
        raise ForbiddenException(db_task.user_id)
    mock = {
        "task_id": task_id,
        "suggestion": f"Here's an AI suggestion for '{db_task.title}': Break this task into smaller steps and prioritize accordingly.",
        "model": "placeholder — AI coming in Module 7"
        }
    return mock
