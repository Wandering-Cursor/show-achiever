from typing import TYPE_CHECKING

from achiever_app.errors.task import TaskItemUsedError
from achiever_app.operations.attendee.tasks.create import complete_task

if TYPE_CHECKING:
    from achiever_app.models.attendee.attendee import Attendee
    from achiever_app.models.organization.task import PartnerTaskItem


async def use_task_item(
    attendee: "Attendee",
    task_item: "PartnerTaskItem",
) -> bool:
    if task_item.is_used:
        raise TaskItemUsedError("Task item is already used")

    is_completed = await complete_task(
        attendee=attendee,
        task_item=task_item,
    )

    if not is_completed:
        return False

    task_item.is_used = True

    await task_item.asave()

    return True
