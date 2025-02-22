from typing import TYPE_CHECKING

from achiever_app.models.organization.task import PartnerTask
from achiever_app.operations.event.read import get_event_by_id, get_recent_events
from mysite.errors.http_errors import NotFoundError
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram_bot_app.enums.commands import Commands
from telegram_bot_app.enums.misc import TaskType
from telegram_bot_app.enums.states import ApplicationStates
from telegram_bot_app.operations.telegram.utils import get_translation
from telegram_bot_app.schemas.pagination import PaginationMeta

if TYPE_CHECKING:
    from achiever_app.models.attendee.attendee import Attendee
    from achiever_app.models.attendee.wallet import AttendeeWallet
    from achiever_app.models.organization import Event
    from telegram.ext import ContextTypes


async def main_menu(
    attendee: "Attendee",
    update: "Update",
    _context: "ContextTypes.DEFAULT_TYPE",
    *,
    as_new_message: bool = True,
) -> int:
    translation = get_translation(update)

    inline_menu = [
        [
            InlineKeyboardButton(
                text=translation.MENU__BALANCES,
                callback_data=Commands.BALANCES.as_command,
            ),
        ],
        [
            InlineKeyboardButton(
                text=translation.MENU__TASKS,
                callback_data=Commands.TASKS.as_command,
            )
        ],
        [
            InlineKeyboardButton(
                text=translation.MENU__SETTINGS,
                callback_data=Commands.SETTINGS.as_command,
            ),
        ],
    ]

    if as_new_message:
        await update.message.reply_text(
            translation.START.format(
                attendee=attendee,
                event=await attendee.following_event,
                update=update,
            ),
            reply_markup=InlineKeyboardMarkup(
                inline_menu,
            ),
        )
    else:
        await update.effective_message.edit_text(
            translation.START.format(
                attendee=attendee,
                event=await attendee.following_event,
                update=update,
            ),
            reply_markup=InlineKeyboardMarkup(
                inline_menu,
            ),
        )

    return -1


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


async def clear_keyboards(
    message: str,
    update: "Update",
) -> None:
    await update.message.reply_text(
        message,
        reply_markup=ReplyKeyboardRemove(),
    )


async def answer_query(
    update: "Update",
    *,
    alert: bool = False,
    message: str | None = None,
) -> None:
    if not update.callback_query:
        return

    translation = get_translation(update)

    message = message or translation.ANSWER

    await update.callback_query.answer(
        text=message,
        show_alert=alert,
    )


async def show_balances(
    wallets: "list[AttendeeWallet]",
    update: "Update",
    _context: "ContextTypes.DEFAULT_TYPE",
) -> None:
    translation = get_translation(update)

    inline_menu = []

    for wallet in wallets:
        inline_menu.append(
            [
                InlineKeyboardButton(
                    text=translation.WALLET__REPRESENTATION.format(
                        wallet_currency=(await wallet.currency).code,
                        wallet_balance=await wallet.current_balance_async,
                    ),
                    callback_data=f"{Commands.VIEW_WALLET.as_command.format(wallet=wallet)}",
                ),
            ],
        )

    inline_menu.append(
        [
            InlineKeyboardButton(
                text=translation.MENU__TO_START,
                callback_data=Commands.TO_START.as_command,
            ),
        ]
    )

    await update.effective_message.edit_text(
        translation.BALANCES,
        reply_markup=InlineKeyboardMarkup(
            inline_menu,
        ),
    )


async def show_settings(
    attendee: "Attendee",
    update: "Update",
    _context: "ContextTypes.DEFAULT_TYPE",
) -> None:
    translation = get_translation(update)

    publicity_update = (
        translation.SETTINGS__TOGGLE_PUBLICITY__OFF
        if attendee.show_publicly
        else translation.SETTINGS__TOGGLE_PUBLICITY__ON
    )

    inline_menu = [
        [
            InlineKeyboardButton(
                text=translation.SETTINGS__CHANGE_EVENT,
                callback_data=Commands.CHANGE_EVENT.as_command,
            ),
        ],
        [
            InlineKeyboardButton(
                text=publicity_update,
                callback_data=Commands.TOGGLE_PUBLICITY.as_command,
            ),
        ],
        [
            InlineKeyboardButton(
                text=translation.SETTINGS__REMOVE_ACCOUNT,
                callback_data=Commands.REMOVE_ACCOUNT.as_command,
            ),
        ],
        [
            InlineKeyboardButton(
                text=translation.MENU__TO_START,
                callback_data=Commands.TO_START.as_command,
            ),
        ],
    ]

    await update.effective_message.edit_text(
        translation.SETTINGS,
        reply_markup=InlineKeyboardMarkup(
            inline_menu,
        ),
    )


async def choose_event(
    events: list["Event"],
    update: "Update",
    _context: "ContextTypes.DEFAULT_TYPE",
) -> None:
    translation = get_translation(update)

    keyboard = []

    for event in events:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=event.name,
                    callback_data=Commands.CHANGE_EVENT_CONFIRMATION.as_command.format(
                        event=event,
                    ),
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text=translation.MENU__SETTINGS,
                callback_data=Commands.SETTINGS.as_command,
            ),
        ]
    )

    await update.effective_message.edit_text(
        translation.REGISTER_EVENT,
        reply_markup=InlineKeyboardMarkup(
            keyboard,
        ),
    )


async def show_tasks(
    attendee: "Attendee",
    update: "Update",
    _context: "ContextTypes.DEFAULT_TYPE",
) -> None:
    translation = get_translation(update)

    event = await attendee.following_event

    keyboard = [
        [
            InlineKeyboardButton(
                text=translation.AVAILABLE_TASKS,
                callback_data=Commands.AVAILABLE_TASKS.as_command.format(
                    event=event,
                    page=1,
                ),
            ),
        ],
        [
            InlineKeyboardButton(
                text=translation.COMPLETED_TASKS,
                callback_data=Commands.COMPLETED_TASKS.as_command.format(
                    event=event,
                    page=1,
                ),
            ),
        ],
        [
            InlineKeyboardButton(
                text=translation.MENU__TO_START,
                callback_data=Commands.TO_START.as_command,
            ),
        ],
    ]

    await update.effective_message.edit_text(
        translation.TASKS.format(
            event=event,
        ),
        reply_markup=InlineKeyboardMarkup(
            keyboard,
        ),
    )


async def show_tasks_page(
    page: list["PartnerTask"],
    pagination_data: PaginationMeta,
    event: "Event",
    update: "Update",
    _context: "ContextTypes.DEFAULT_TYPE",
) -> None:
    translation = get_translation(update)

    inline_menu = []

    for task in page:
        inline_menu.append(
            [
                InlineKeyboardButton(
                    text=task.name,
                    callback_data=Commands.SHOW_TASK.as_command.format(
                        task=task,
                    ),
                ),
            ],
        )

    previous_page_button = InlineKeyboardButton(
        text=translation.PAGINATION__PREVIOUS.format(
            previous=pagination_data.previous_page,
        ),
        callback_data=Commands.AVAILABLE_TASKS.as_command.format(
            event=event,
            page=pagination_data.previous_page,
        ),
    )

    next_page_button = InlineKeyboardButton(
        text=translation.PAGINATION__NEXT.format(
            next=pagination_data.next_page,
        ),
        callback_data=Commands.AVAILABLE_TASKS.as_command.format(
            event=event,
            page=pagination_data.next_page,
        ),
    )

    pagination_menu = []

    if pagination_data.previous_page:
        pagination_menu.append(previous_page_button)

    pagination_menu.append(
        InlineKeyboardButton(
            text=translation.MENU__TASKS,
            callback_data=Commands.TASKS.as_command,
        )
    )

    if pagination_data.next_page:
        pagination_menu.append(next_page_button)

    inline_menu.append(pagination_menu)

    await update.effective_message.edit_text(
        translation.TASKS_PAGINATION,
        reply_markup=InlineKeyboardMarkup(
            inline_menu,
        ),
    )
