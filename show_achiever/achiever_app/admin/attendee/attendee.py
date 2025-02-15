from achiever_app.admin.base import BaseAdmin
from achiever_app.models.attendee import Attendee
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.register(Attendee)
class AttendeeAdmin(BaseAdmin):
    fieldsets = (
        *BaseAdmin.fieldsets,
        (
            _("Attendee"),
            {
                "fields": (
                    "following_event",
                    "telegram_id",
                    "first_name",
                    "last_name",
                    "username",
                    "show_publicly",
                )
            },
        ),
    )

    list_display = (
        *BaseAdmin.list_display[: BaseAdmin.LIST_DISPLAY_START],
        "first_name",
        "last_name",
        "username",
        "following_event",
        "show_publicly",
        *BaseAdmin.list_display[BaseAdmin.LIST_DISPLAY_END :],
    )

    list_filter = (
        *BaseAdmin.list_filter,
        "following_event",
    )

    LIST_DISPLAY_START = BaseAdmin.LIST_DISPLAY_START + 4
