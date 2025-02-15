from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.authentication import AuthenticationError

from .base import BaseError
from .http_errors import InternalServerError


def any_exception(_request: "Request", exc: Exception) -> JSONResponse:
    """
    Ensures we always return a JSON response.

    Note: Doesn't work with `debug=True`. (quirks of FastAPI/Starlette)
    """

    exception = InternalServerError(
        log_message={
            "message": "An unhandled exception occurred.",
            "exception": exc,
        }
    )

    return JSONResponse(
        content={
            "detail": exception.details,
        },
        status_code=exception.status_code,
        headers={
            "X-Error-Name": exception.error_name,
        },
    )


def app_error_handler(_: "Request", exc: BaseError) -> JSONResponse:
    raise HTTPException(
        status_code=exc.status_code,
        detail=exc.details,
        headers={
            "X-Error-Name": exc.error_name,
        },
    )


def authentication_error(_: "Request", exc: AuthenticationError) -> JSONResponse:
    if (args := exc.args) and isinstance(args[0], BaseError):
        error = args[0]
        return JSONResponse(
            content={
                "detail": error.details,
            },
            status_code=error.status_code,
            headers={
                "X-Error-Name": error.error_name,
                "WWW-Authenticate": "Bearer",
            },
        )

    return JSONResponse(
        status_code=401,
        content={"detail": [{"msg": "Unauthorized"}]},
        headers={
            "WWW-Authenticate": "Bearer",
            "X-Error-Name": "Unauthorized",
        },
    )


error_handler_pairs = (
    (401, authentication_error),
    (500, any_exception),
    (BaseError, app_error_handler),
    (AuthenticationError, authentication_error),
)
