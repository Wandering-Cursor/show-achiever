from achiever_app.admin.base import BaseAdmin
from achiever_app.models.common import Currency
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.register(Currency)
class CurrencyAdmin(BaseAdmin):
    fieldsets = (
        *BaseAdmin.fieldsets,
        (
            _("Currency"),
            {
                "fields": (
                    "name",
                    "code",
                    "icon",
                )
            },
        ),
    )

    list_display = (
        *BaseAdmin.list_display[: BaseAdmin.LIST_DISPLAY_START],
        "name",
        "code",
        *BaseAdmin.list_display[BaseAdmin.LIST_DISPLAY_END :],
    )

    LIST_DISPLAY_START = BaseAdmin.LIST_DISPLAY_START + 2
