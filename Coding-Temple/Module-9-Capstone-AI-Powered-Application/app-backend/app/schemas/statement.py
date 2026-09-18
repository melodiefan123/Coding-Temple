from pydantic import BaseModel, Field
from typing import List, Optional

# 1. Individual transaction (Keep this as-is)
class StatementTransaction(BaseModel):
    date: Optional[str] = Field(None, example="2026-07-15")
    description: str = Field(..., example="Stripe Payout Client A")
    amount: float = Field(..., example=1200.00)
    transaction_type: str = Field(..., example="income")  # "income" or "expense"
    category: Optional[str] = Field("Uncategorized", example="Freelance Income")

# 2. File Upload Response (REMOVED global transaction_type)
class StatementUploadResponse(BaseModel):
    filename: str
    total_extracted: int
    transactions: List[StatementTransaction]
    message: str = "Statement parsed successfully."

# 3. Confirm Request Payload (Keep as-is)
class StatementSyncRequest(BaseModel):
    transactions: List[StatementTransaction]

# 4. Final Sync Response (Keep as-is)
class StatementSyncResponse(BaseModel):
    status: str = "success"
    income_records_added: int
    expense_records_added: int
    message: str