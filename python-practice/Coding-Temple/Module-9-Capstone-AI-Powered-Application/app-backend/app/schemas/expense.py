from pydantic import BaseModel, Field
from typing import Optional 
from datetime import datetime

class ExpenseBase(BaseModel):
    description: str = Field(...,example="Office Supplies")
    category: str = Field(default="General", example="Office")
    amount: float = Field(..., gt=0, example=49.99)
    card_id: Optional[int] = Field(default=None, exmaple=1)

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(BaseModel):
    description: Optional[str] = None
    category: Optional[str] = None 
    amount: Optional[float] = None 
    card_id: Optional[int] = None 

class ExpenseResponse(BaseModel):
    id: int
    description: str
    category: str
    amount: float
    card_id: Optional[int] = None
    user_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True