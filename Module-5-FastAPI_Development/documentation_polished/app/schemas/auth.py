from pydantic import BaseModel, Field

class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=100,description="The email of the student")
    password: str = Field(min_length=8, max_length=100)
    class Config:
        json_schema_extra={
            "example": {
                "name": "test",
                "email":"test@email.com",
                "password": "testpassword"
            }
        }

class LoginRequest(BaseModel):
    email: str = Field(min_length=1, max_length=100,description="The email of the student")
    password: str = Field(min_length=8, max_length=100)
    class Config:
        json_schema_extra={
            "example": {
                "email":"test@email.com",
                "password": "testpassword"
            }
        }

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    class Config:
        json_schema_extra={
            "example": {
                "access_token": "jwt-token-here",
                "token_type": "bearer"
            }
        }