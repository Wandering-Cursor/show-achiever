from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING

from achiever_app.operations.attendee.attendee.read import find_attendee
from achiever_app.operations.event.read import get_event_by_id, get_recent_events
from asgiref.sync import sync_to_async
from mysite.errors.http_errors import NotFoundError
from mysite.middleware import close_old_connections
from python_telegram_bot_django_persistence.persistence import DjangoPersistence
from telegram import Bot as TelegramBot
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from telegram_bot_app.enums.states import ApplicationStates
from telegram_bot_app.enums.translation import get_class

if TYPE_CHECKING:
    from achiever_app.models.attendee.attendee import Attendee
    from telegram_bot_app.enums.english import TelegramMessages
    from telegram_bot_app.models.bot import Bot


class MyApp:
    _bots: dict[str, Application] = {}

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


async def find_attendee_for_update(
    update: "Update",
) -> "Attendee":
    return await find_attendee(
        external_id=update.effective_user.id,
    )


def get_translation(update: "Update") -> "type[TelegramMessages]":
    return get_class("english")


@handler_decorator()
async def start_command(
    update: "Update",
    context: "ContextTypes.DEFAULT_TYPE",
) -> None:
    translation = get_translation(update)

    try:
        attendee = await find_attendee_for_update(update)
    except NotFoundError:
        return await not_registered(
            update=update,
            context=context,
        )

    await update.message.reply_text(translation.START.format(update=update))

    return None


async def not_registered(
    update: "Update",
    context: "ContextTypes.DEFAULT_TYPE",
) -> ApplicationStates:
    translation = get_translation(update)

    await update.message.reply_text(
        translation.NOT_REGISTERED.format(
            update=update,
        )
    )

    keyboard = []

    events = []
    additional_options = update.effective_message.text.split(" ")[0:]
    if len(additional_options) > 1:
        event_id = additional_options[1]

        try:
            events.append(
                await get_event_by_id(event_id=event_id),
            )
        except NotFoundError:
            events = await get_recent_events()
    else:
        events = await get_recent_events()

    for event in events:
        keyboard.append(
            [
                KeyboardButton(
                    text=event.name,
                )
            ]
        )

    await update.message.reply_text(
        translation.CHOOSE_EVENT,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard,
            one_time_keyboard=True,
        ),
    )

    return ApplicationStates.REGISTER_EVENT


@handler_decorator()
async def choose_event(
    update: "Update",
    context: "ContextTypes.DEFAULT_TYPE",
) -> None:
    translation = get_translation(update)

    await update.message.reply_text(str(context.user_data))

    await update.message.reply_text(
        translation.CHOOSE_EVENT.format(update=update),
    )


@handler_decorator()
async def fallback(
    update: "Update",
    context: "ContextTypes.DEFAULT_TYPE",
) -> None:
    translation = get_translation(update)

    await update.message.reply_text(translation.FALLBACK.format(update=update))


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
        entry_points=[CommandHandler("start", start_command)],
        states={
            ApplicationStates.REGISTER_EVENT: [
                MessageHandler(filters.TEXT & (~filters.COMMAND), choose_event),
            ],
        },
        fallbacks=[CommandHandler("start", start_command)],
        name=ApplicationStates.REGISTER_CONVRESATION,
        persistent=True,
    )

    application.add_handler(register_handler)

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
