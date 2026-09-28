from pydantic import BaseModel, Field

class RecipeCreate(BaseModel):
    title: str = Field(..., min_length=1)
    cuisine: str = Field(..., min_length=1)
    prep_time_minutes: int = Field(..., gt=0)
    servings: int = Field(..., gt=0)

class RecipeResponse(BaseModel):
    id: int = Field(..., gt=0)
    title: str
    cuisine: str
    prep_time_minutes: int
    servings: int