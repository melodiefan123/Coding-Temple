# app/routers/metrics.py
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from datetime import datetime, timedelta

from app.database import get_db
from app.models.invoice import Invoice
from app.models.income import Income
from app.models.budget import Budget
from app.models.user import User
from app.utils.security import get_current_user
from app.utils.helpers import parse_date
from app.models.expense import Expense

router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.get("/revenue-flow")
def get_revenue_flow(
    group_by: str = Query("monthly", pattern="^(monthly|weekly)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    try:
        invoices = db.query(Invoice).filter(
            Invoice.user_id == current_user.id,
            Invoice.status == "paid"
        ).all()
        
        incomes = db.query(Income).filter(
            Income.user_id == current_user.id
        ).all()

        date_format = "%b %Y" if group_by == "monthly" else "%Y-W%W"
        aggregated = {}

        for inv in invoices:
            inv_date = parse_date(getattr(inv, "issued_date", None))
            key = inv_date.strftime(date_format)
            aggregated[key] = aggregated.get(key, 0.0) + float(inv.amount or 0.0)

        for inc in incomes:
            inc_date = parse_date(getattr(inc, "created_at", None))
            key = inc_date.strftime(date_format)
            aggregated[key] = aggregated.get(key, 0.0) + float(inc.amount or 0.0)

        result = [{"date": k, "revenue": v} for k, v in aggregated.items()]
        return result if result else [{"date": "Current", "revenue": 0.0}]

    except Exception as e:
        print(f"Metrics Revenue Error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate revenue metrics: {str(e)}"
        )


@router.get("/expense-breakdown")
def get_expense_breakdown(
    period: str = Query("This Month"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Returns total expenses/budgets allocated per category.
    """
    results = db.query(
        Expense.category, 
        func.sum(Expense.amount).label("total")
    ).filter(
        Expense.user_id == current_user.id
    ).group_by(Expense.category).all()

    if not results: 
        return []

    return [
        {
            "category": category or "Uncategorized", 
            "amount": float(total_amount or 0.0)
        }
        for category, total_amount in results
    ]
