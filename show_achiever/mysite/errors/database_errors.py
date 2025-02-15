from .http_errors import IntegrityError


class DatabaseIntegrityError(IntegrityError):
    def __init__(
        self: "DatabaseIntegrityError",
        log_message: str | dict | None = None,
        details: list[dict] | None = None,
        error_message: str | None = None,
    ) -> None:
        if log_message is None:
            log_message = {
                "msg": "Error when performing database operation",
                "details": details,
                "error_message": error_message,
            }

        super().__init__(log_message, details, error_message)
