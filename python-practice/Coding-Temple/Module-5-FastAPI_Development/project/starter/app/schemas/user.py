# project/starter/app/schemas/user.py
# Module 5 Project — User schemas
#
# TODO: Define UserCreate, UserResponse, TokenResponse

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    """Registration input."""
    # TODO: username, email, password
    username: str = Field(min_length=1, max_length=20, description="")
    email: str = Field(min_length=1, max_length=100,description="The email of the student")
    password:  str=Field(max_length=20, description="password")


class UserResponse(BaseModel):
    """Returned to clients — no password fields."""
     # TODO: id, username, email + model_config
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """JWT token response."""
    # TODO: access_token, token_type
    access_token: str
    token_type: str = "bearer"
