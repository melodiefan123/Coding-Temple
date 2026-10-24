class AppException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

class NotFoundException(AppException):
    def __init__(self, entity_name: str, entity_id: int):
        super().__init__(status_code=404, detail=f"{entity_name} with ID {entity_id} not found")

class BadRequestException(AppException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)

class DuplicateException(AppException):
    def __init__(self, entity_name: str, field_name: str, value: str):
        super().__init__(status_code=409, detail=f"{entity_name} with {field_name} '{value}' already exists")

class UnauthorizedException(AppException):
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(status_code=401, detail=detail)