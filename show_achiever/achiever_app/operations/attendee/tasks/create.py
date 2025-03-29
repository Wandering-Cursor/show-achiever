from typing import TYPE_CHECKING

from achiever_app.operations.attendee.balance.create import create_balance_for_task

if TYPE_CHECKING:
    from achiever_app.models.attendee.attendee import Attendee
    from achiever_app.models.organization.task import PartnerTaskItem


async def complete_task(
    attendee: "Attendee",
    task_item: "PartnerTaskItem",
) -> bool:
    created = await create_balance_for_task(
        attendee=attendee,
        task_item=task_item,
    )

    if not created:
        return False

    await send_task_completed_notification(
        attendee=attendee,
        task_item=task_item,
    )

    return True


async def send_task_completed_notification(
    attendee: "Attendee",
    task_item: "PartnerTaskItem",
) -> None:
    # TODO (@makisukurisu): Implement notification  # noqa: FIX002, TD003
    # We need to send a notification to the user
    # probably via all available bots :?
    pass
