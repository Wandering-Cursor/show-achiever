from achiever_app.admin.base import BaseAdmin
from achiever_app.models.attendee import AttendeeWalletBalance
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.register(AttendeeWalletBalance)
class AttendeeWalletBalanceAdmin(BaseAdmin):
    fieldsets = (
        *BaseAdmin.fieldsets,
        (
            _("Attendee Wallet Balance"),
            {
                "fields": (
                    "wallet",
                    "amount",
                    "for_partner_task_item",
                )
            },
        ),
    )

    list_display = (
        *BaseAdmin.list_display[: BaseAdmin.LIST_DISPLAY_START],
        "wallet",
        "amount",
        "for_partner_task_item",
        *BaseAdmin.list_display[BaseAdmin.LIST_DISPLAY_END :],
    )

    list_filter = (
        *BaseAdmin.list_filter,
        "wallet",
        "for_partner_task_item",
    )

    LIST_DISPLAY_START = BaseAdmin.LIST_DISPLAY_START + 3
