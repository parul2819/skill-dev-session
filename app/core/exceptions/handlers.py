from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from .base import AppException


async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "error_code": exc.error_code,
            "message": exc.message,
            "details": exc.details
        }
    )

def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(AppException, app_exception_handler)