import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.exceptions import AppException

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests and responses."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log request
        logger.info(f"Request: {request.method} {request.url}")

        try:
            response = await call_next(request)

            # Log response
            process_time = time.time() - start_time
            logger.info(
                f"Response: {request.method} {request.url} "
                f"Status: {response.status_code} "
                f"Duration: {process_time:.3f}s"
            )

            return response
        except AppException as e:
            # Our custom exceptions are already formatted correctly
            raise e
        except Exception as e:
            # Unexpeced errors logging
            logger.error(
                f"Error processing request: {request.method} {request.url} "
                f"Error: {str(e)}"
            )
            raise
