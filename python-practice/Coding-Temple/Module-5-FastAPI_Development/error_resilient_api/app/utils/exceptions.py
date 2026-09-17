# BadRequestException — for invalid business logic (400), e.g., trying to delete an active user
class AppException(Exception):
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)

# NotFoundException — for missing resources (404)
class NotFoundException(AppException):
    def __init__(self, resource: str, resource_id):
        super().__init__(
            detail = f"{resource} with id {resource_id} not found",
            status_code = 404
        )

# DuplicateException — for unique constraint violations (409)
class DuplicateException(AppException):
    def __init__(self, resource: str, field: str, value):
        super().__init__(
            detail = f"{resource} with {field} '{value}' already exists",
            status_code = 409
        )
