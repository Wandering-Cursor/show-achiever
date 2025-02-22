from typing import TYPE_CHECKING

from python_telegram_bot_django_persistence.persistence import DjangoPersistence
from telegram import Bot as TelegramBot
from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from telegram_bot_app.enums.commands import Commands
from telegram_bot_app.enums.states import ApplicationStates
from telegram_bot_app.operations.telegram import handlers

if TYPE_CHECKING:
    from telegram_bot_app.models.bot import Bot


class MyApp:
    _bots: dict[str, Application] = {}  # noqa: RUF012

    @classmethod
    async def get_bot(cls, bot: "Bot") -> Application:
        if bot.bot_token not in cls._bots:
            cls._bots[bot.bot_token] = await make_bot(bot)
        return cls._bots[bot.bot_token]

    @classmethod
    async def finish(cls, bot: "Bot") -> None:
        if bot.bot_token in cls._bots:
            await cls._bots[bot.bot_token].shutdown()
            del cls._bots[bot.bot_token]


async def make_bot(bot: "Bot") -> Application:
    persistance = DjangoPersistence(
        namespace=bot.bot_token,
    )

    application = (
        Application.builder()
        .token(bot.bot_token)
        .persistence(
            persistence=persistance,
        )
        .build()
    )

    register_handler = ConversationHandler(
        entry_points=[CommandHandler("start", handlers.start_command)],
        states={
            ApplicationStates.REGISTER_EVENT: [
                MessageHandler(filters.TEXT & (~filters.COMMAND), handlers.choose_event),
            ],
            ApplicationStates.REGISTER_FIRST_NAME: [
                MessageHandler(filters.TEXT | filters.Command(), handlers.provide_first_name),
            ],
            ApplicationStates.REGISTER_LAST_NAME: [
                MessageHandler(filters.TEXT | filters.Command(), handlers.provide_last_name),
            ],
            ApplicationStates.REGISTER_PUBLICITY: [
                MessageHandler(filters.TEXT, handlers.provide_publicity),
            ],
            ApplicationStates.REGISTER_CONFIRMATION: [
                MessageHandler(filters.TEXT, handlers.confirm_registration),
            ],
        },
        fallbacks=[CommandHandler("start", handlers.start_command)],
        name=ApplicationStates.REGISTER_CONVRESATION,
        persistent=True,
    )

    application.add_handler(register_handler)
    application.add_handler(
        CommandHandler(
            "clear_keyboard",
            handlers.clear_keyboards,
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            handlers.to_start,
            pattern=Commands.TO_START.as_regex,
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            handlers.show_balances,
            pattern=Commands.BALANCES.as_regex,
        ),
    )
    application.add_handler(
        CallbackQueryHandler(
            handlers.show_settings,
            pattern=Commands.SETTINGS.as_regex,
        ),
    )

    application.add_handler(
        CallbackQueryHandler(
            handlers.update_event,
            pattern=Commands.CHANGE_EVENT.as_regex,
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            handlers.set_event,
            pattern=Commands.CHANGE_EVENT_CONFIRMATION.as_regex,
        )
    )

    await application.initialize()

    return application


async def set_webhook(bot: "Bot") -> None:
    application = await MyApp.get_bot(bot)

    integration = application.bot
    if not isinstance(integration, TelegramBot):
        raise ValueError("Invalid bot instance")

    await integration.set_webhook(
        url=bot.webhook_url,
    )


async def convert_data_to_update(data: dict, bot: Application) -> "Update":
    return Update.de_json(
        data=data,
        bot=bot.bot,
    )
