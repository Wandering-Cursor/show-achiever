from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING

from achiever_app.operations.attendee.attendee.create import register_attendee
from achiever_app.operations.attendee.attendee.read import find_attendee
from achiever_app.operations.event.read import (
    get_event_by_id,
    get_event_by_semi_unique_name,
    get_recent_events,
)
from achiever_app.schemas.attendee import AttendeeInfo
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
    return get_class(
        update.effective_user.language_code,
    )


@handler_decorator()
async def start_command(
    update: "Update",
    _context: "ContextTypes.DEFAULT_TYPE",
) -> None:
    translation = get_translation(update)

    try:
        attendee = await find_attendee_for_update(update)
    except NotFoundError:
        return await not_registered(
            update=update,
        )

    await update.message.reply_text(
        translation.START.format(
            attendee=attendee,
            update=update,
        )
    )

    return None


async def not_registered(
    update: "Update",
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
                    text=event.semi_unique_name,
                )
            ]
        )

    await update.message.reply_text(
        translation.REGISTER_EVENT,
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

    event = await get_event_by_semi_unique_name(
        semi_unique_name=update.message.text,
    )

    context.user_data["event_id"] = str(event.uuid)

    await update.message.reply_text(
        translation.REGISTER_FIRST_NAME.format(
            event=event,
            user=update.effective_user,
        ),
    )

    return ApplicationStates.REGISTER_FIRST_NAME


@handler_decorator()
async def provide_first_name(
    update: "Update",
    context: "ContextTypes.DEFAULT_TYPE",
) -> None:
    translation = get_translation(update)

    name = update.effective_user.first_name

    if update.message.text != "/skip":
        name = update.message.text

    context.user_data["first_name"] = name

    await update.message.reply_text(
        translation.REGISTER_LAST_NAME.format(
            user=update.effective_user,
        ),
    )

    return ApplicationStates.REGISTER_LAST_NAME


@handler_decorator()
async def provide_last_name(
    update: "Update",
    context: "ContextTypes.DEFAULT_TYPE",
) -> None:
    translation = get_translation(update)

    last_name = update.effective_user.last_name

    if update.message.text != "/skip":
        last_name = update.message.text
    if update.message.text == "/blank":
        last_name = ""

    context.user_data["last_name"] = last_name

    publicity_options = [
        KeyboardButton(
            text=translation.REGISTER_PUBLICITY__YES,
        ),
        KeyboardButton(
            text=translation.REGISTER_PUBLICITY__NO,
        ),
    ]

    await update.message.reply_text(
        translation.REGISTER_PUBLICITY.format(
            user=update.effective_user,
        ),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[publicity_options],
            one_time_keyboard=True,
        ),
    )

    return ApplicationStates.REGISTER_PUBLICITY


@handler_decorator()
async def provide_publicity(
    update: "Update",
    context: "ContextTypes.DEFAULT_TYPE",
) -> None:
    translation = get_translation(update)

    publicity = update.message.text == translation.REGISTER_PUBLICITY__YES

    context.user_data["publicity"] = publicity

    confirmation_options = [
        KeyboardButton(
            text=translation.REGISTER_CONFIRMATION__CONFIRM,
        ),
        KeyboardButton(
            text=translation.REGISTER_CONFIRMATION__START_OVER,
        ),
    ]

    await update.message.reply_text(
        translation.REGISTER_CONFIRMATION.format(
            event=await get_event_by_id(context.user_data["event_id"]),
            first_name=context.user_data["first_name"],
            last_name=context.user_data["last_name"],
            publicity=context.user_data["publicity"],
        ),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[confirmation_options],
            one_time_keyboard=True,
        ),
    )

    return ApplicationStates.REGISTER_CONFIRMATION


@handler_decorator()
async def confirm_registration(
    update: "Update",
    context: "ContextTypes.DEFAULT_TYPE",
) -> None:
    translation = get_translation(update)

    if update.message.text == translation.REGISTER_CONFIRMATION__CONFIRM:
        await register_attendee(
            attendee_info=AttendeeInfo(
                telegram_id=str(update.effective_user.id),
                first_name=context.user_data["first_name"],
                last_name=context.user_data["last_name"],
                username=update.effective_user.username,
                show_publicly=context.user_data["publicity"],
                following_event_id=context.user_data["event_id"],
            )
        )
        return -1

    await not_registered(
        update=update,
    )
    return ApplicationStates.REGISTER_EVENT


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
            ApplicationStates.REGISTER_FIRST_NAME: [
                MessageHandler(filters.TEXT | filters.Command(), provide_first_name),
            ],
            ApplicationStates.REGISTER_LAST_NAME: [
                MessageHandler(filters.TEXT | filters.Command(), provide_last_name),
            ],
            ApplicationStates.REGISTER_PUBLICITY: [
                MessageHandler(filters.TEXT, provide_publicity),
            ],
            ApplicationStates.REGISTER_CONFIRMATION: [
                MessageHandler(filters.TEXT, confirm_registration),
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
