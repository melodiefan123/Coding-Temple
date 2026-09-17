from pydantic import BaseModel

class ExpenseBreakdownItem(BaseModel):
    category: str
    amount: float

