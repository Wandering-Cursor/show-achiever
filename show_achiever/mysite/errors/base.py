import json

from fastapi.logger import logger


class BaseError(Exception):
    status_code: int = 500
    error_name: str = "BaseError"

    error_message: str = "An unexpected error occurred."

    def _get_main_detail(self: "BaseError") -> dict:
        return {
            "msg": self.error_message,
            "type": self.error_name,
        }

    def get_details(self: "BaseError") -> list[dict]:
        return [self._get_main_detail()]

    def __init__(
        self: "BaseError",
        log_message: str | dict | None = None,
        details: list[dict] | None = None,
        error_message: str | None = None,
        *,
        add_default_error: bool = False,
    ) -> None:
        self.error_message = error_message or self.__class__.error_message
        self.details = details or self.get_details()
        if add_default_error:
            self.details = self.get_details() + self.details

        if log_message is not None:
            logger.exception(
                json.dumps(
                    log_message,
                    default=repr,
                )
            )
