from enum import Enum
from fastapi import HTTPException, Request, FastAPI
from fastapi.responses import JSONResponse


class ErrorCode(Enum):
    SERVER_ERROR = "SERVER_ERROR"
    NOT_FOUND = "NOT_FOUND"
    REQUIRED = "REQUIRED"
    MISSING_INPUT = "MISSING_INPUT"


class CustomException(Exception):
    def __init__(self, field: str, error_code: ErrorCode) -> None:
        self.field = field
        self.error_code = error_code


def add_internal_server_error(app: FastAPI):
    @app.exception_handler(CustomException)
    async def internal_server_error(request: Request, error: CustomException):
        return JSONResponse(
            status_code=500,
            content={
                "field": error.field,
                "erroCode": error.error_code.value
            }
        )
