from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.database import get_db
from app.models.income import Income
from app.auth import get_current_user
from app.schemas.income import IncomeCreate, IncomeResponse

router = APIRouter(prefix="/income", tags=["Income"])

@router.post("/", response_model=IncomeResponse, status_code=status.HTTP_201_CREATED)
def add_income(
    income_in: IncomeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    income_data = income_in.model_dump(exclude_unset=True)
    
    new_income = Income(
        user_id=current_user.id,
        **income_data
    )
    db.add(new_income)
    db.commit()
    db.refresh(new_income)
    return new_income

@router.get("/", response_model=List[IncomeResponse])
def get_user_incomes(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Income).filter(Income.user_id == current_user.id).all()