from typing import TYPE_CHECKING, TypeVar

from achiever_app.operations.attendee.attendee.read import find_attendee
from asgiref.sync import sync_to_async
from mysite.middleware import close_old_connections
from telegram_bot_app.enums.translation import get_class

if TYPE_CHECKING:
    from achiever_app.models.attendee.attendee import Attendee
    from telegram import Update
    from telegram_bot_app.enums.english import TelegramMessages


FunctionType = TypeVar("FunctionType")


def handler_decorator() -> FunctionType:
    def decorator(
        func: FunctionType,
    ) -> FunctionType:
        async def wrapper(
            *args,  # noqa: ANN002
            **kwargs,  # noqa: ANN003
        ) -> None:
            await sync_to_async(close_old_connections)()
            return await func(*args, **kwargs)

        return wrapper

    return decorator


async def find_attendee_for_update(
    update: "Update",
) -> "Attendee":
    return await find_attendee(
        external_id=update.effective_user.id,
    )


def get_translation(update: "Update") -> "type[TelegramMessages]":
    return get_class(
        update.effective_user.language_code,
    )
