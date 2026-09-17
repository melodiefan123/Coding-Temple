from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base properties shared across schemas
class SubscriptionBase(BaseModel):
    name: str
    amount: float
    billing_cycle: Optional[str] = "monthly"
    next_billing_date: Optional[datetime] = None

# Schema used when CREATING a new subscription
class SubscriptionCreate(SubscriptionBase):
    card_id: int

# Schema returned in API responses
class SubscriptionResponse(SubscriptionBase):
    id: int
    card_id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Allows ORM model conversion