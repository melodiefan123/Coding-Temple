from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class ReceiptCreate(BaseModel):
    merchant_name: str = Field(..., description="The name of the merchant")
    total_amount: float = Field(..., gt=0, description="The total amount of the receipt")
    category: str = Field(default="Uncategorized",min_length=1, max_length=50, description="The category of the receipt")
    transaction_date: datetime = Field(..., description="The date of the transaction in YYYY-MM-DD format")
    is_verified: bool = Field(default=True, description="Whether the receipt is verified")

class ReceiptResponse(BaseModel):
    id: int = Field(..., description="The unique identifier of the receipt")
    user_id: int = Field(..., description="The ID of the user who owns the receipt")
    merchant_name: str = Field(..., description="The name of the merchant")
    total_amount: float = Field(..., gt=0, description="The total amount of the receipt")
    category: str = Field(default="Uncategorized",min_length=1, max_length=50, description="The category of the receipt")
    transaction_date: datetime = Field(..., description="The date of the transaction in YYYY-MM-DD format")
    uploaded_at: datetime = Field(..., description="The date and time the receipt was uploaded")
    is_verified: bool = Field(default=True, description="Whether the receipt is verified")
    chromadb_id: Optional[str] = Field(None,  description="The ChromaDB ID associated with the receipt")

    model_config = ConfigDict(from_attributes=True)