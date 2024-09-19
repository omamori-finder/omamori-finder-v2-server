from enum import Enum


class ErrorCode(Enum):
    SERVER_ERROR = 'SERVER_ERROR'
    NOT_FOUND = 'NOT_FOUND'
    REQUIRED = 'REQUIRED'
    MISSING_INPUT = 'MISSING_INPUT'
