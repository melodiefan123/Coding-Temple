from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date, timezone
from typing import Optional
from enum import Enum

class InvoiceStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"
   
class InvoiceCreate(BaseModel):
    invoice_number: str = Field(...,  min_length=1, max_length=30,description="The invoice number")
    client_name: str = Field(..., min_length=1, max_length=100,description="The name of the client")
    amount: float = Field(..., gt=0,description="The amount of the invoice")
    status: InvoiceStatus = Field(default=InvoiceStatus.PENDING, description="The status of the invoice")
    issued_date: Optional[datetime | date] = Field(default_factory=lambda: datetime.now(timezone.utc), description="The date the invoice was issued")
    due_date: datetime | date = Field(..., description="The due date for the invoice")
    description: Optional[str] = None

class InvoiceResponse(BaseModel):
    id: int = Field(..., description="The unique identifier of the invoice")
    user_id: int = Field(..., description="The ID of the user who owns the invoice")
    invoice_number: str = Field(..., description="The invoice number")
    client_name: str = Field(..., description="The name of the client")
    amount: float = Field(..., description="The amount of the invoice")
    status: InvoiceStatus = Field(default=InvoiceStatus.PENDING, description="The status of the invoice")
    issued_date: datetime = Field(..., description="The date the invoice was issued")
    due_date: datetime = Field(..., description="The due date for the invoice")
    description: Optional[str] = Field(None, description="Description of invoice")
    chromadb_id: Optional[str] = Field(None, description="The ChromaDB ID associated with the invoice")
    

    model_config = ConfigDict(from_attributes=True)