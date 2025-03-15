from typing import Annotated
from uuid import uuid4

import pydantic
from achiever_app.schemas.task import CompleteTaskRequest, CompleteTaskResponse
from fastapi import Body, Path

from .router import task_router


@task_router.post(
    "/{partner_task_item_id}",
)
def complete_task(
    partner_task_item_id: Annotated[pydantic.UUID4, Path()],
    payload: Annotated[CompleteTaskRequest, Body()],
) -> CompleteTaskResponse:
    print(partner_task_item_id, payload)

    return CompleteTaskResponse(
        task_id=uuid4(),
        completed=True,
    )
