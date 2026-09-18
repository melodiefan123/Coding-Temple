from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class IncomeCreate(BaseModel):
    source: str = Field(..., min_length=1, max_length=100, description="Source of income")
    amount: float = Field(..., gt=0, description="Amount of income")
    date: Optional[datetime] = Field(default=None, description="Date of income")

class IncomeResponse(BaseModel):
    id: int
    user_id: int
    source: str
    amount: float
    date: datetime = Field(..., description="Date of income entry")

    model_config = ConfigDict(from_attributes=True)