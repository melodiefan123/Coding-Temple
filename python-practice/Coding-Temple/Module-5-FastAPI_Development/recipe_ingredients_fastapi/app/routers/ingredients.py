from fastapi import APIRouter, HTTPException
from app.schemas.ingredient import IngredientCreate, IngredientResponse

router = APIRouter(prefix="/ingredients", tags=["ingredients"])
ingredients_db: list[dict] = []
next_ingredient_id = 1

@router.get("/", response_model=list[IngredientResponse])
def list_ingredients():
    return ingredients_db

@router.get("/{ingredient_id}", response_model=IngredientResponse)
def get_ingredient(ingredient_id: int):
    for ingredient in ingredients_db:
        if ingredient["id"] == ingredient_id:
            return ingredient
    raise HTTPException(status_code=404, detail="Ingredient not found")

@router.post("/", response_model=IngredientResponse, status_code=201)
def create_ingredient(ingredient: IngredientCreate):
    global next_ingredient_id
    new_ingredient = {
        "id": next_ingredient_id, **ingredient.model_dump()
    }
    ingredients_db.append(new_ingredient)
    next_ingredient_id += 1
    return new_ingredient