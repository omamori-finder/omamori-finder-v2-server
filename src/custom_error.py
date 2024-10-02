from enum import Enum
from fastapi import HTTPException, Request, FastAPI
from fastapi.responses import JSONResponse


class ErrorCode(Enum):
    SERVER_ERROR = "SERVER_ERROR"
    NOT_FOUND = "NOT_FOUND"
    REQUIRED = "REQUIRED"
    MISSING_INPUT = "MISSING_INPUT"


class CustomException(Exception):
    def __init__(self, field: str, error_code: ErrorCode, status_code: int) -> None:
        self.field = field
        self.error_code = error_code
        self.status_code = status_code


def add_custom_error(app: FastAPI):
    @app.exception_handler(CustomException)
    async def custom_error(request: Request, error: CustomException):
        return JSONResponse(
            status_code=error.status_code,
            content={
                "field": error.field,
                "erroCode": error.error_code.value
            }
        )
