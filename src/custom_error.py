from enum import Enum
from typing import TypedDict
from fastapi import HTTPException, Request, FastAPI
from fastapi.responses import JSONResponse


class ErrorCode(Enum):
    SERVER_ERROR = "SERVER_ERROR"
    NOT_FOUND = "NOT_FOUND"
    REQUIRED = "REQUIRED"
    MISSING_INPUT = "MISSING_INPUT"
    VALIDATION_ERROR = "VALIDATION_ERROR"


class Error(TypedDict):
    errors: list[dict]
    error: ErrorCode
    has_error: bool


class CustomException(Exception):
    def __init__(self, error: list[Error], status_code: int) -> None:
        self.error = error
        self.status_code = status_code


def add_custom_error(app: FastAPI):
    @app.exception_handler(CustomException)
    async def custom_error(request: Request, error: CustomException):
        return JSONResponse(
            status_code=error.status_code,
            content={
                "error": error.error
            }
        )
