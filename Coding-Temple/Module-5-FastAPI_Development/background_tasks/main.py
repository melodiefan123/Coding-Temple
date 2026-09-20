from fastapi import FastAPI, Request
from app.config import settings
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.routers.students import router as students_router
from app.routers.auth import router as auth_router
from app.database import Base, engine
from app.utils.exceptions import AppException

# Import models so SQLAlchemy binds them to metadata
import app.models.student
import app.models.user

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name, 
    description="A simple API for database students management", 
    version="1.0.1"
)

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
        content={"error": True, "detail": "Invalid request data", "errors": errors}
    )

app.include_router(auth_router)
app.include_router(students_router)

@app.get("/")
def root(): 
    return {"app": settings.app_name, "docs": "/docs"}