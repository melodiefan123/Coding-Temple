from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class UserCreate(BaseModel):
    username: str = Field(...,min_length=1, max_length=20, description="The user's username")
    email: str = Field(...,min_length=1, max_length=100, description="The user's email address")
    password: str = Field(min_length=1, max_length=20, description="The user's password")


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"