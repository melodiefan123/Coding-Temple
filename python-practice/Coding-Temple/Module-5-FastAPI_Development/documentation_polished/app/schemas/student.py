from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class StudentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200, description="name of the student", examples=["first_name last_name"])
    email: str = Field(min_length=1, max_length=100,description="The email of the student", examples=["student1@email.com"])
    grade_level: Optional[int] = Field(None, ge=1, le=12, description="The grade level of the student")
    gpa: float = Field(0.0, ge=0.0, le=4.0, description="The GPA of the student")
    is_enrolled: bool = Field(True, description="Whether the student is currently enrolled")

class StudentUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=200, description="name of the student")
    email: str = Field(min_length=1, max_length=100,description="The email of the student")
    grade_level: int = Field(ge=1, le=12, description="The grade level of the student")
    gpa: Optional[float] = Field(None, ge=0.0, le=4.0, description="The GPA of the student")
    is_enrolled: bool = Field(True, description="Whether the student is currently enrolled")

class StudentPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="name of the student")
    email: Optional[str] = Field(None, min_length=1, max_length=100,description="The email of the student")
    grade_level: Optional[int] = Field(None, ge=1, le=12, description="The grade level of the student")
    gpa: Optional[float] = Field(None, ge=0.0, le=4.0, description="The GPA of the student")
    is_enrolled: Optional[bool] = Field(None, description="Whether the student is currently enrolled")

class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    grade_level: Optional[int]
    gpa: Optional[float]
    is_enrolled: bool
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Alice Johnson",
                "email": "alice@example.com",
                "grade_level": 10,
                "gpa": 3.8,
                "is_enrolled": True
            }
        }