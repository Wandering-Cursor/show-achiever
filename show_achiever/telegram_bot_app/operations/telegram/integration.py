from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING

from asgiref.sync import sync_to_async
from mysite.middleware import close_old_connections
from telegram.ext import Application, CommandHandler, ContextTypes

if TYPE_CHECKING:
    from telegram import Update
    from telegram_bot_app.models.bot import Bot


def handler_decorator() -> Callable[
    [Callable[["Update", "ContextTypes.DEFAULT_TYPE"], Awaitable[None]]],
    Callable[["Update", "ContextTypes.DEFAULT_TYPE"], Awaitable[None]],
]:
    def decorator(
        func: Callable[["Update", "ContextTypes.DEFAULT_TYPE"], Awaitable[None]],
    ) -> Callable[["Update", "ContextTypes.DEFAULT_TYPE"], Awaitable[None]]:
        async def wrapper(update: "Update", context: "ContextTypes.DEFAULT_TYPE") -> None:
            await sync_to_async(close_old_connections)()
            return await func(update, context)

        return wrapper

    return decorator


@handler_decorator()
async def start_command(
    update: "Update",
    context: "ContextTypes.DEFAULT_TYPE",  # noqa: ARG001
) -> None:
    await update.message.reply_text("Hello!")


def make_bot(bot: "Bot") -> Application:
    application = Application.builder().token(bot.bot_token).build()

    application.add_handler(CommandHandler("start"), start_command)

    return application
