"""
Makes a list of responses for FastAPI to use in the OpenAPI schema.
"""

import pydantic

from . import http_errors


class ErrorDetail(pydantic.BaseModel):
    loc: list | None = None
    msg: str
    type: str = "Undefined"


class BaseErrorModel(pydantic.BaseModel):
    detail: list[ErrorDetail]


errors: list[http_errors.BaseError] = [
    http_errors.InternalServerError,
    http_errors.InvalidRequestError,
    http_errors.BadRequestError,
    http_errors.UnauthorizedError,
    http_errors.ForbiddenError,
    http_errors.NotFoundError,
    http_errors.IntegrityError,
]

responses = {
    error.status_code: {
        "model": BaseErrorModel,
        "content": {
            "application/json": {
                "example": BaseErrorModel(
                    detail=[
                        ErrorDetail(
                            type=error.error_name,
                            msg=error.error_message,
                        )
                    ]
                ).model_dump(),
            },
        },
    }
    for error in errors
}
