from typing import TYPE_CHECKING

from achiever_app.models.organization.task import PartnerTaskItem
from mysite.errors.http_errors import NotFoundError

if TYPE_CHECKING:
    from pydantic import UUID4


async def find_task_item(
    partner_task_item_id: "UUID4",
) -> PartnerTaskItem:
    try:
        return await PartnerTaskItem.objects.aget(
            uuid=partner_task_item_id,
        )
    except PartnerTaskItem.DoesNotExist as e:
        raise NotFoundError(
            log_message={
                "msg": "Task item not found",
                "partner_task_item_id": partner_task_item_id,
            }
        ) from e
