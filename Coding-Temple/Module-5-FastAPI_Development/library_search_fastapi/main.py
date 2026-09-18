from fastapi import FastAPI
from app.config import settings
from app.routers import books
app = FastAPI(
    title=settings.app_name, 
    description="A simple API for library search functionality", 
    version="1.0.0")

app.include_router(books.router)

@app.get("/")
def root(): 
    return {"app": settings.app_name, "docs": "/docs"}
