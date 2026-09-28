from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class StudentBase(BaseModel):
    name: str
    email: EmailStr
    major: Optional[str] = None
    gpa: Optional[float] = Field(default=None, ge=0.0, le=4.0)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    # Full replacement requiring name and email, with optional major and gpa
    pass


class StudentPatch(BaseModel):
    # All fields optional for partial updates
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    major: Optional[str] = None
    gpa: Optional[float] = Field(default=None, ge=0.0, le=4.0)


class StudentResponse(StudentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)