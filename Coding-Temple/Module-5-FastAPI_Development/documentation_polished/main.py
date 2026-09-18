from fastapi import FastAPI, Request
from app.config import settings
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.routers.students import router as router_students
from app.routers.auth import router as router_auth
from app.database import Base, engine
from app.utils.exceptions import AppException
from fastapi.middleware.cors import CORSMiddleware 
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded #Rate Limit 
from app.utils.limiter import limiter

tags_metadata = [
    {"name": "Authentication", "description": "User registration and login. All protected endpoints require a Bearer token."},
    {"name": "students", "description": "CRUD operations for students. Most endpoints require authentication."},
]

app = FastAPI(
    title=settings.app_name, 
    description="""
        # Student Management API

        This API allows users to:

        - Manage student records
        - Authenticate users
        - Track enrollment information
        - Perform CRUD operations

        ## Features

        - JWT Authentication
        - Student management
        - GPA tracking
        - Enrollment status updates
    """, 
    version="1.0.1",
    openapi_tags=tags_metadata)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)

app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "detail": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [{
        "field": " ->".join(str(l) for l in e["loc"]), "message": e["msg"]}
        for e in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"error": True, "detail": "Invalid request data", "errors": errors  }
    )

app.include_router(router_students)
app.include_router(router_auth)

@app.get("/")
def root(): 
    return {"app": settings.app_name, "docs": "/docs"}
