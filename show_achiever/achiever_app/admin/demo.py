from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from achiever_app.admin.base import BaseAdmin
from achiever_app.models.demo import DemoModel


@admin.register(DemoModel)
class DemoAdmin(BaseAdmin):
    fieldsets = (
        *BaseAdmin.fieldsets,
        (
            _("Demo Model"),
            {"fields": ("name",)},
        ),
    )

    list_display = (
        *BaseAdmin.list_display[: BaseAdmin.KEEP_LIST_DISPLAY],
        "name",
        *BaseAdmin.list_display[BaseAdmin.KEEP_LIST_DISPLAY :],
    )

    KEEP_LIST_DISPLAY = BaseAdmin.KEEP_LIST_DISPLAY + 1
