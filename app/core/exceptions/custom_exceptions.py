from .base import AppException
from .error_codes import ErrorCode


class NotFoundException(AppException):
    def __init__(self, message: str = None, status_code: int = 404, details: str = None):
        super().__init__(status_code=status_code, error_code=ErrorCode.NOT_FOUND, message=message, details=details)

class UnauthorizedException(AppException):
    def __init__(self, message: str = None, status_code: int = 401, details: str = None):
        super().__init__(status_code=status_code, error_code=ErrorCode.UNAUTHORIZED, message=message, details=details)

class ForbiddenException(AppException):
    def __init__(self, message: str = None, status_code: int = 403, details: str = None):
        super().__init__(status_code=status_code, error_code=ErrorCode.FORBIDDEN, message=message, details=details)

class BadRequestException(AppException):
    def __init__(self, message: str = None, status_code: int = 400, details: str = None):
        super().__init__(status_code=status_code, error_code=ErrorCode.BAD_REQUEST, message=message, details=details)

class InternalServerErrorException(AppException):
    def __init__(self, message: str = None, status_code: int = 500, details: str = None):
        super().__init__(status_code=status_code, error_code=ErrorCode.INTERNAL_SERVER_ERROR, message=message, details=details)