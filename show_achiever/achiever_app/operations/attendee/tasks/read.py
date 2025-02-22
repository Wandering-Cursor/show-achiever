from typing import TYPE_CHECKING

from achiever_app.models.attendee.balance import AttendeeWalletBalance
from achiever_app.models.organization.task import PartnerTask
from asgiref.sync import sync_to_async
from django.core.paginator import Paginator

if TYPE_CHECKING:
    from achiever_app.models.attendee.attendee import Attendee
    from django.db.models.query import QuerySet


def paginate(
    qs: "QuerySet",
    page: int,
    per_page: int,
) -> tuple[list, int]:
    paginator = Paginator(
        object_list=qs,
        per_page=per_page,
        allow_empty_first_page=True,
    )

    return (
        list(paginator.page(page).object_list),
        qs.count(),
    )


async def get_tasks(
    attendee: "Attendee",
    page: int,
    *,
    per_page: int = 10,
    only_available: bool = False,
    only_completed: bool = False,
) -> tuple[list["PartnerTask"], int]:
    for_event = await attendee.following_event

    qs = PartnerTask.objects.filter(
        partner__for_event=for_event,
    )

    if only_available:
        used_partner_tasks = qs.filter(
            uuid__in=AttendeeWalletBalance.objects.filter(
                wallet__attendee=attendee,
            ).values("for_partner_task_item__task"),
        )
        qs = qs.exclude(
            uuid__in=used_partner_tasks,
        )
    if only_completed:
        qs = qs.filter(
            uuid__in=AttendeeWalletBalance.objects.filter(
                wallet__attendee=attendee,
            ).values("for_partner_task_item__task"),
        )

    qs = qs.order_by("-created_at")

    return await sync_to_async(paginate)(qs=qs, page=page, per_page=per_page)
