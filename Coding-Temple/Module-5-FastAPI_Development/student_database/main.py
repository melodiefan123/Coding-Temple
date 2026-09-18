from fastapi import FastAPI
from app.config import settings
from app.routers.students import router
from app.database import Base, engine
from app.models.student import Student

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name, 
    description="A simple API for database students management", 
    version="1.0.0")

app.include_router(router)

@app.get("/")
def root(): 
    return {"app": settings.app_name, "docs": "/docs"}
