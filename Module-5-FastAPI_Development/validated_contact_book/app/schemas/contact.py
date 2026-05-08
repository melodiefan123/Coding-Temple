from pydantic import BaseModel, Field, field_validator
from enum import Enum
from typing import Optional

class Category(str, Enum):
    personal = "personal"
    work = "work"
    family = "family"

class ContactCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1,max_length=50)
    email: str
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    category: Category 
    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if "@" not in value:
            raise ValueError("Invalid email address")
        return value

class ContactUpdate(BaseModel):
    first_name: Optional[str] = Field(None,min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1,max_length=50)
    email: Optional[str] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    category: Optional[Category] = None
    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if value is not None and "@" not in value:
            raise ValueError("Invalid email address")
        return value

class ContactResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    category: Category
    created_at: str
