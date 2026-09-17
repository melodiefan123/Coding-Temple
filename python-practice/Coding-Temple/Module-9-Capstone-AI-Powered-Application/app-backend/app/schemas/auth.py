from pydantic import BaseModel, Field
from typing import Optional

class RegisterUser(BaseModel):
    username: str = Field(..., min_length=1, max_length=20, description="The user's username")
    email: str = Field(..., min_length=1, max_length=100, description="The user's email address")
    password: str = Field(..., min_length=1, max_length=20, description="The user's password")

class LoginUser(BaseModel):
    username: Optional[str] = Field(None, min_length=1, max_length=20, description="The user's username")
    email: Optional[str] = Field(None, min_length=1, max_length=100, description="The user's email address")
    password: str = Field(..., min_length=1, max_length=20, description="The user's password")

class TokenResponse(BaseModel):
    access_token: str = Field(..., description="The access token for the user")
    token_type: str = Field("bearer", description="The type of the token, usually 'bearer'")