# project/starter/app/main.py
# Module 5 Project — AI-Ready Task Manager API
#
# Run with: uvicorn app.main:app --reload  (from project/starter/ folder)
# Docs at:  http://127.0.0.1:8000/docs

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# TODO: Import Base, engine from database
from app.database import Base, engine
from app.models import User, Task
# TODO: Import routers
from app.routers import auth, tasks, users
from app.exceptions import AppException
from fastapi.responses import JSONResponse

tags_metadata = [
    {
        "name": "auth",
        "description": "Authentication endpoints — register and login."
    },
    {
        "name": "tasks",
        "description": "Task management endpoints — create, read, update, delete."
    },
    {"name": "users", 
     "description": "User management endpoints - view user profile"}
]
app = FastAPI(
    title="AI-Ready Task Manager",
    openapi_tags=tags_metadata,
    description="A task management API with JWT auth and an AI suggestion endpoint.",
    version="1.0.0",
)

# TODO: Configure CORS (specific origins, not *)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8501"],  # TODO: update for production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)

# TODO: Create DB tables
Base.metadata.create_all(bind=engine)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "detail": exc.detail}
    )

# TODO: Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])


@app.get("/", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "Task Manager API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

