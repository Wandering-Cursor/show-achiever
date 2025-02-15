from achiever_app.admin.base import BaseAdmin
from achiever_app.admin.organization.goal import GoalInline
from achiever_app.admin.organization.partner import PartnerInline
from achiever_app.models.organization import Event
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.register(Event)
class EventAdmin(BaseAdmin):
    fieldsets = (
        *BaseAdmin.fieldsets,
        (
            _("Event"),
            {
                "fields": (
                    "name",
                    "description",
                    "poster",
                )
            },
        ),
    )

    list_display = (
        *BaseAdmin.list_display[: BaseAdmin.LIST_DISPLAY_START],
        "name",
        "description",
        *BaseAdmin.list_display[BaseAdmin.LIST_DISPLAY_END :],
    )

    LIST_DISPLAY_START = BaseAdmin.LIST_DISPLAY_START + 2

    inlines = (
        *BaseAdmin.inlines,
        GoalInline,
        PartnerInline,
    )
