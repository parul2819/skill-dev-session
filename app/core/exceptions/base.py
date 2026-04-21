from typing import Any, Optional
from .error_codes import ErrorCode
from .error_messages import ERROR_MESSAGES


class AppException(Exception):
    def __init__(
        self,
        status_code: int = 400,
        error_code: ErrorCode = ErrorCode.BAD_REQUEST,
        message: Optional[str] = None,
        details: Optional[Any] = None
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message or details or ERROR_MESSAGES.get(error_code, "An error occured.")
        self.details = details

        super().__init__(self.message)