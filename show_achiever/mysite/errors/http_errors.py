"""
Various HTTP errors that can be raised by the API.
"""

from .base import BaseError


class InternalServerError(BaseError):
    error_name: str = "InternalServerError"
    error_message: str = "Internal Server Error"


class BadGatewayError(BaseError):
    status_code: int = 502
    error_name: str = "BadGateway"
    error_message: str = "Bad Gateway"


class BadRequestError(BaseError):
    status_code: int = 400
    error_name: str = "BadRequest"
    error_message: str = "Bad Request"


class UnauthorizedError(BaseError):
    status_code: int = 401
    error_name: str = "Unauthorized"
    error_message: str = "Unauthorized"


class ForbiddenError(BaseError):
    status_code: int = 403
    error_name: str = "Forbidden"
    error_message: str = "Forbidden"


class NotFoundError(BaseError):
    status_code: int = 404
    error_name: str = "NotFound"
    error_message: str = "Not Found"


class IntegrityError(BaseError):
    status_code: int = 409
    error_name: str = "IntegrityError"
    error_message: str = "Integrity Error"


class InvalidRequestError(BaseError):
    status_code: int = 422
    error_name: str = "InvalidRequest"
    error_message: str = "Invalid Request"
