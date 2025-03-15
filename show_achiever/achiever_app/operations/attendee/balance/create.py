from typing import TYPE_CHECKING

from achiever_app.models.attendee.balance import AttendeeWalletBalance
from achiever_app.models.attendee.wallet import AttendeeWallet
from fastapi.logger import logger

if TYPE_CHECKING:
    from achiever_app.models.attendee.attendee import Attendee
    from achiever_app.models.organization.task import PartnerTask, PartnerTaskItem


async def create_balance_for_task(
    attendee: "Attendee",
    task_item: "PartnerTaskItem",
) -> bool:
    task: PartnerTask = await task_item.task

    wallet, _ = await AttendeeWallet.objects.aget_or_create(
        attendee=attendee,
        currency=(await task.reward_currency),
    )

    if await AttendeeWalletBalance.objects.filter(
        wallet=wallet,
        for_partner_task_item__task=task,
    ).aexists():
        # Prohibit completing the same task multiple times
        logger.warning(
            {
                "msg": "Task is already completed",
                "attendee": attendee,
                "task_item": task_item,
            }
        )

        return False

    await AttendeeWalletBalance.objects.acreate(
        wallet=wallet,
        amount=(await wallet.current_balance_async) + task.reward_amount,
        for_partner_task_item=task_item,
    )

    return True
