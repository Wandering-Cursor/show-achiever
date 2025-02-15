from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from telegram_bot_app.admin.base import BaseAdmin
from telegram_bot_app.models.bot import Bot


@admin.register(Bot)
class BotAdmin(BaseAdmin):
    fieldsets = (
        *BaseAdmin.fieldsets,
        (
            _("Bot"),
            {
                "fields": (
                    "platform",
                    "bot_token",
                    "webhook_secret",
                    "webhook_url_prefix",
                    "webhook_url",
                )
            },
        ),
    )

    list_display = (
        *BaseAdmin.list_display[: BaseAdmin.LIST_DISPLAY_START],
        "platform",
        "bot_token",
        *BaseAdmin.list_display[BaseAdmin.LIST_DISPLAY_END :],
    )

    readonly_fields = (
        *BaseAdmin.readonly_fields,
        "webhook_url",
    )

    LIST_DISPLAY_START = BaseAdmin.LIST_DISPLAY_START + 2
