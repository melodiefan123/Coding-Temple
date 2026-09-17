from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.budget import Budget  # Adjust import based on your directory structure
from app.schemas.budget import BudgetCreate, BudgetResponse, BudgetUpdate
from app.auth import get_current_user
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.models.expense import Expense

router = APIRouter(prefix="/budgets", tags=["Budgets"])

@router.post("/", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
def create_or_update_budget(
    budget_in: BudgetCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Check if a budget for this category already exists for the user
    existing_budget = db.query(Budget).filter(
        Budget.user_id == current_user.id,
        Budget.category == budget_in.category
    ).first()

    if existing_budget:
        existing_budget.monthly_limit = budget_in.monthly_limit
        existing_budget.notes = budget_in.notes
        db.commit()
        db.refresh(existing_budget)
        return existing_budget

    new_budget = Budget(
        user_id=current_user.id,
        category=budget_in.category,
        monthly_limit=budget_in.monthly_limit,
        notes=budget_in.notes
    )
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    return new_budget

@router.post("/expenses", status_code=status.HTTP_201_CREATED)
def create_expense(payload: ExpenseCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        new_expense = Expense(
            description = payload.description, 
            category = payload.category, 
            amount = payload.amount, 
            card_id = payload.card_id,
            user_id=current_user.id
        )
        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)

        return new_expense
    except Exception as e:
        db.rollback()  # 👈 Critical: Roll back failed transaction
        print(f"❌ Backend Error on /budgets/expenses: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database commit failed: {str(e)}"
        )

@router.get("/expenses", response_model=List[ExpenseResponse])
def get_user_expenses(db: Session = Depends(get_db), 
                      current_user = Depends(get_current_user)):
    return db.query(Expense).filter(Expense.user_id == current_user.id).all()

@router.get("/", response_model=List[BudgetResponse])
def get_user_budgets(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Budget).filter(Budget.user_id == current_user.id).all()


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    budget_obj = db.query(Budget).filter(
        Budget.id == budget_id,
        Budget.user_id == current_user.id
    ).first()

    if not budget_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget entry not found"
        )

    db.delete(budget_obj)
    db.commit()
    return None