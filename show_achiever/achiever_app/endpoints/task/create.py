from typing import Annotated

import pydantic
from achiever_app.operations.attendee.attendee.read import find_attendee
from achiever_app.operations.task.read import find_task_item
from achiever_app.operations.task.update import use_task_item
from achiever_app.schemas.task import CompleteTaskRequest, CompleteTaskResponse
from fastapi import Body, Path
from mysite.errors.http_errors import IntegrityError

from .router import task_router


@task_router.post(
    "/{partner_task_item_id}",
)
async def complete_task(
    partner_task_item_id: Annotated[pydantic.UUID4, Path()],
    payload: Annotated[CompleteTaskRequest, Body()],
) -> CompleteTaskResponse:
    attendee = await find_attendee(
        external_id=payload.attendee_id,
    )

    task_item = await find_task_item(
        partner_task_item_id=partner_task_item_id,
    )

    if task_item.is_used:
        raise IntegrityError(
            log_message={
                "msg": "Task item is already used",
                "partner_task_item_id": partner_task_item_id,
            },
            error_message="Task item is already used",
        )

    is_used = await use_task_item(
        attendee=attendee,
        task_item=task_item,
    )

    if not is_used:
        raise IntegrityError(
            log_message={
                "msg": "Task item is not used",
                "partner_task_item_id": partner_task_item_id,
            },
            error_message="Could not complete task",
        )

    return CompleteTaskResponse(
        task_id=task_item.task.uuid,
        completed=is_used,
    )
