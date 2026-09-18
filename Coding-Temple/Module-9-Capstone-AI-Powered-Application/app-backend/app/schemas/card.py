from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class CardCreate(BaseModel):
    card_name: str = Field(..., min_length=1, max_length=50, description="Card nickname")
    card_type: str = Field(..., description="Visa, Mastercard, Amex, Discover, etc.")
    last_four: str = Field(..., min_length=4, max_length=4, description="Last 4 digits")
    credit_limit: Optional[float] = Field(default=0.0, ge=0)
    current_balance: Optional[float] = Field(default=0.0, ge=0)

class CardResponse(BaseModel):
    id: int
    user_id: int
    card_name: str
    card_type: str
    last_four: str
    credit_limit: float
    current_balance: float

    model_config = ConfigDict(from_attributes=True)