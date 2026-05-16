# project/starter/app/schemas/user.py
# Module 5 Project — User schemas
#
# TODO: Define UserCreate, UserResponse, TokenResponse

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    """Registration input."""
    pass  # TODO: username, email, password


class UserResponse(BaseModel):
    """Returned to clients — no password fields."""
    pass  # TODO: id, username, email + model_config


class TokenResponse(BaseModel):
    """JWT token response."""
    pass  # TODO: access_token, token_type
