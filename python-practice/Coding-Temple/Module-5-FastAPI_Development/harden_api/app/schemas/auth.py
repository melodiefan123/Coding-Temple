from pydantic import BaseModel, Field

class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=100,description="The email of the student")
    password: str = Field(min_length=8, max_length=100)

class LoginRequest(BaseModel):
    email: str = Field(min_length=1, max_length=100,description="The email of the student")
    password: str = Field(min_length=8, max_length=100)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"