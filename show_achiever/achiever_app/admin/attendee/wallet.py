from typing import TYPE_CHECKING

from achiever_app.admin.base import BaseAdmin
from achiever_app.models.attendee import AttendeeWallet
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from decimal import Decimal


@admin.register(AttendeeWallet)
class AttendeeWalletAdmin(BaseAdmin):
    fieldsets = (
        *BaseAdmin.fieldsets,
        (
            _("Attendee Wallet"),
            {
                "fields": (
                    "attendee",
                    "currency",
                    "current_balance",
                )
            },
        ),
    )

    list_display = (
        *BaseAdmin.list_display[: BaseAdmin.LIST_DISPLAY_START],
        "attendee",
        "currency",
        *BaseAdmin.list_display[BaseAdmin.LIST_DISPLAY_END :],
    )

    readonly_fields = (
        *BaseAdmin.readonly_fields,
        "current_balance",
    )

    list_filter = (
        *BaseAdmin.list_filter,
        "attendee",
    )

    LIST_DISPLAY_START = BaseAdmin.LIST_DISPLAY_START + 2

    def current_balance(self, obj: "AttendeeWallet") -> "Decimal":
        return obj.current_balance
