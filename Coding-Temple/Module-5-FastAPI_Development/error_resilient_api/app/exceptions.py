from fastapi import Request
from fastapi.responses import JSONResponse


# Base Exception
class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400, error_type: str = "AppError"):
        self.message = message
        self.status_code = status_code
        self.error_type = error_type
        super().__init__(message)


# Custom Exception Classes requested by the assignment
class NotFoundError(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, status_code=404, error_type="Not Found")


class DuplicateError(AppException):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message=message, status_code=409, error_type="Duplicate Entry")


class AppValidationError(AppException):
    def __init__(self, message: str = "Domain validation error"):
        super().__init__(message=message, status_code=422, error_type="Validation Error")


# Async Exception Handlers returning consistent JSON format
async def not_found_error_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_type,
            "message": exc.message,
            "status_code": exc.status_code
        }
    )


async def duplicate_error_handler(request: Request, exc: DuplicateError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_type,
            "message": exc.message,
            "status_code": exc.status_code
        }
    )


async def app_validation_error_handler(request: Request, exc: AppValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_type,
            "message": exc.message,
            "status_code": exc.status_code
        }
    )