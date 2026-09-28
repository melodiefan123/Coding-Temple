from pydantic import BaseModel, Field

class IngredientCreate(BaseModel):
    name: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)

class IngredientResponse(BaseModel):
    id: int = Field(..., gt=0)
    name: str
    category: str