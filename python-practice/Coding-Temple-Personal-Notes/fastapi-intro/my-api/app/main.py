# my-api/app/main.py
from fastapi import FastAPI
from app.config import settings
from app.routers import books

app = FastAPI(
    title=settings.app_name,
    description="A properly structured FastAPI application",
    version="0.1.0"
)

app.include_router(books.router)

@app.get("/")
def root():
    return {"app": settings.app_name, "docs": "/docs"}