from fastapi import FastAPI
from app.config import settings
from app.routers.notes import router
from app.database import Base, engine
from app.models.note import Note

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name, 
    description="A simple API for database notes management", 
    version="1.0.0")

app.include_router(router)

@app.get("/")
def root(): 
    return {"app": settings.app_name, "docs": "/docs"}
