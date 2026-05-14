from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS — allow our HTML frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Allow any origin (fine for local dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory task storage (resets when server restarts)
tasks = [
    {"id": 1, "title": "Learn HTML", "done": True},
    {"id": 2, "title": "Learn CSS", "done": True},
    {"id": 3, "title": "Learn JavaScript", "done": False},
    {"id": 4, "title": "Build Streamlit app", "done": False},
]
next_id = 5  # Track the next available ID

class TaskCreate(BaseModel):
    title: str

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    global next_id
    new_task = {"id": next_id, "title": task.title, "done": False}
    tasks.append(new_task)
    next_id += 1
    return new_task

@app.patch("/tasks/{task_id}")
def toggle_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]  # Toggle done/not done
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.get("/stats")
def get_stats():
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    return {"total": total, "done": done, "pending": total - done}