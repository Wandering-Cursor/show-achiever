from typing import TYPE_CHECKING

from achiever_app.operations.attendee.attendee.create import register_attendee
from achiever_app.operations.attendee.tasks.read import get_tasks
from achiever_app.operations.attendee.wallet.read import get_wallets
from achiever_app.operations.event.read import (
    get_event_by_id,
    get_event_by_semi_unique_name,
    get_recent_events,
)
from achiever_app.schemas.attendee import AttendeeInfo
from mysite.errors.http_errors import NotFoundError
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram_bot_app.enums.misc import TaskType
from telegram_bot_app.enums.states import ApplicationStates
from telegram_bot_app.operations.telegram import messages
from telegram_bot_app.operations.telegram.utils import (
    find_attendee_for_update,
    get_translation,
    handler_decorator,
)
from telegram_bot_app.schemas.pagination import PaginationMeta

if TYPE_CHECKING:
    from telegram.ext import ContextTypes


@handler_decorator()
async def start_command(
    update: "Update",
    context: "ContextTypes.DEFAULT_TYPE",
    *,
    as_new_message: bool = True,
) -> None:
    try:
        attendee = await find_attendee_for_update(update)
    except NotFoundError:
        return await messages.not_registered(
            update=update,
        )

    return await messages.main_menu(
        attendee=attendee,
        update=update,
        _context=context,
        as_new_message=as_new_message,
    )


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
async def update_event(
    update: "Update",
    context: "ContextTypes.DEFAULT_TYPE",
) -> None:
    events = await get_recent_events(limit=10)

    return await messages.choose_event(
        events=events,
        update=update,
        _context=context,
    )


@handler_decorator()
async def set_event(
    update: "Update",
    context: "ContextTypes.DEFAULT_TYPE",
) -> None:
    if not update.callback_query:
        return None

    query_payload = update.callback_query.data
    if not query_payload:
        return await messages.answer_query(
            update=update,
            alert=True,
            message="No query payload",
        )

    await messages.answer_query(update=update)

    event_id = query_payload.split(" ")[1]

    event = await get_event_by_id(
        event_id=event_id,
    )

    attendee = await find_attendee_for_update(update)

    attendee.following_event = event
    await attendee.asave()

    attendee = await find_attendee_for_update(update)

    return await messages.main_menu(
        attendee=attendee,
        update=update,
        _context=context,
        as_new_message=False,
    )


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
        await messages.clear_keyboards(
            message=translation.REGISTERED,
            update=update,
        )
        return await start_command(
            update=update,
            context=context,
        )

    await messages.not_registered(
        update=update,
    )

    return ApplicationStates.REGISTER_EVENT


@handler_decorator()
async def clear_keyboards(
    update: "Update",
    _context: "ContextTypes.DEFAULT_TYPE",
) -> None:
    await messages.clear_keyboards(
        message="Keyboards cleared",
        update=update,
    )


@handler_decorator()
async def show_balances(
    update: "Update",
    context: "ContextTypes.DEFAULT_TYPE",
) -> None:
    await messages.answer_query(update=update)

    try:
        attendee = await find_attendee_for_update(update)
    except NotFoundError:
        await messages.not_registered(
            update=update,
        )
        return await start_command(update)

    wallets = await get_wallets(
        attendee=attendee,
    )

    return await messages.show_balances(
        wallets=wallets,
        update=update,
        _context=context,
    )


@handler_decorator()
async def show_settings(
    update: "Update",
    context: "ContextTypes.DEFAULT_TYPE",
) -> None:
    await messages.answer_query(update=update)

    try:
        attendee = await find_attendee_for_update(update)
    except NotFoundError:
        await messages.not_registered(
            update=update,
        )
        return await start_command(update)

    return await messages.show_settings(
        attendee=attendee,
        update=update,
        _context=context,
    )


@handler_decorator()
async def to_start(
    update: "Update",
    _context: "ContextTypes.DEFAULT_TYPE",
) -> None:
    await messages.answer_query(update=update)

    return await start_command(
        update=update,
        context=_context,
        as_new_message=False,
    )


@handler_decorator()
async def toggle_publicity(
    update: "Update",
    context: "ContextTypes.DEFAULT_TYPE",
) -> None:
    await messages.answer_query(update=update)

    try:
        attendee = await find_attendee_for_update(update)
    except NotFoundError:
        await messages.not_registered(
            update=update,
        )
        return await start_command(update)

    attendee.show_publicly = not attendee.show_publicly
    await attendee.asave()

    return await messages.show_settings(
        attendee=attendee,
        update=update,
        _context=context,
    )


@handler_decorator()
async def remove_account(
    update: "Update",
    _context: "ContextTypes.DEFAULT_TYPE",
) -> None:
    try:
        await find_attendee_for_update(update)
    except NotFoundError:
        await messages.not_registered(
            update=update,
        )
        return await start_command(update)

    return await messages.answer_query(
        update=update,
        alert=True,
        message="Not implemented",
    )


@handler_decorator()
async def show_tasks(
    update: "Update",
    context: "ContextTypes.DEFAULT_TYPE",
) -> None:
    await messages.answer_query(update=update)

    try:
        attendee = await find_attendee_for_update(update)
    except NotFoundError:
        return await start_command(update)

    return await messages.show_tasks(
        attendee=attendee,
        update=update,
        _context=context,
    )


@handler_decorator()
async def show_tasks_pages(
    update: "Update",
    context: "ContextTypes.DEFAULT_TYPE",
) -> None:
    await messages.answer_query(update=update)

    try:
        attendee = await find_attendee_for_update(update)
    except NotFoundError:
        return await start_command(update)

    task_type = TaskType(update.callback_query.data.split()[1])
    page = int(update.callback_query.data.split()[3])
    per_page = 10

    only_available = False
    only_completed = False

    if task_type == TaskType.AVAILABLE:
        only_available = True
    if task_type == TaskType.COMPLETED:
        only_completed = True

    tasks, total = await get_tasks(
        attendee=attendee,
        page=page,
        per_page=per_page,
        only_available=only_available,
        only_completed=only_completed,
    )

    return await messages.show_tasks_page(
        page=tasks,
        pagination_data=PaginationMeta(
            page=page,
            per_page=per_page,
            total=total,
        ),
        event=attendee.following_event,
        update=update,
        _context=context,
    )
