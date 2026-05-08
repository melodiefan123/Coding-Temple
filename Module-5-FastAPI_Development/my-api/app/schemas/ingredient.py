from pydantic import BaseModel

class IngredientCreate(BaseModel):
    name: str
    category: str

class IngredientResponse(BaseModel):
    id: int
    name: str
    category: str