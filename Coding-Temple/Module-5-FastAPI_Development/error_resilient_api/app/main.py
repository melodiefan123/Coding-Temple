from fastapi import FastAPI, Request
from app.config import settings
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.routers.students import router
from app.database import Base, engine
from app.exceptions import (
    NotFoundError,
    DuplicateError,
    AppValidationError,
    not_found_error_handler,
    duplicate_error_handler,
    app_validation_error_handler
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name, 
    description="A simple API for database students management", 
    version="1.0.1")

app.add_exception_handler(NotFoundError, not_found_error_handler)
app.add_exception_handler(DuplicateError, duplicate_error_handler)
app.add_exception_handler(AppValidationError, app_validation_error_handler)

app.include_router(router)

@app.get("/")
def root(): 
    return {"app": settings.app_name, "docs": "/docs"}
