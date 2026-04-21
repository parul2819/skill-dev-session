from .error_codes import ErrorCode

ERROR_MESSAGES = {
    ErrorCode.INTERNAL_SERVER_ERROR: "An unexpected error occurred.",
    ErrorCode.NOT_FOUND: "The requested resource was not found.",
    ErrorCode.VALIDATION_ERROR: "Invalid input provided.",
    ErrorCode.UNAUTHORIZED: "You are not authorized to perform this resource.",
    ErrorCode.FORBIDDEN: "You do not have permission to access this resource.",
    ErrorCode.BAD_REQUEST: "The request could not be understood or was missing required parameters."
}