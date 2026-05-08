from fastapi import FastAPI
from app.config import settings
from app.routers import ingredients, recipes

app = FastAPI(
    title=settings.app_name, 
    description="A simple API for managing recipes and ingredients", 
    version="1.0.0")

app.include_router(recipes.router)
app.include_router(ingredients.router)

@app.get("/")
def root(): 
    return {"app": settings.app_name, "docs": "/docs"}
