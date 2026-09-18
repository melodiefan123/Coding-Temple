# app-backend/app/exceptions.py
from fastapi import HTTPException, status

class AppException(HTTPException):
    """Base application exception for standardized HTTP error handling."""
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "An application error occurred.",
        headers: dict = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class CredentialsException(AppException):
    """Raised when authentication fails (invalid token or credentials)."""
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class NotFoundException(AppException):
    """Raised when a requested resource is missing."""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )