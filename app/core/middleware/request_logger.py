import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        try:
            response = await call_next(request)
            duration = (time.perf_counter() - start_time) * 1000
            logger.info(
                f"Request duration : {duration}ms | "
                f"Request URL : {request.url} | "
                f"Request Method : {request.method} | "
                )

            return response
        except Exception as e:
            duration = (time.perf_counter() - start_time) * 1000
            logger.exception(
                f"Request duration : {duration}ms | "
                f"Request URL : {request.url} | "
                f"Request Method : {request.method} | "
            )

            raise                   