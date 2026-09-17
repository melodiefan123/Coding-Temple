from pydantic import BaseModel

class RecipeCreate(BaseModel):
    title: str
    cuisine: str
    prep_time_minutes: int
    servings: int

class RecipeResponse(BaseModel):
    id: int
    title: str
    cuisine: str
    prep_time_minutes: int
    servings: int


