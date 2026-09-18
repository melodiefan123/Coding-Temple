from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema for creating a budget entry
class BudgetCreate(BaseModel):
    category: str
    monthly_limit: float
    notes: Optional[str] = None

# Schema for updating an existing budget entry
class BudgetUpdate(BaseModel):
    category: Optional[str] = None
    monthly_limit: Optional[float] = None
    notes: Optional[str] = None

# Schema returned in API responses
class BudgetResponse(BudgetCreate):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True