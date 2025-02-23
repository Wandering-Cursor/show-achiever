from typing import TYPE_CHECKING

from asgiref.sync import async_to_sync
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from telegram_bot_app.admin.base import BaseAdmin
from telegram_bot_app.models.bot import Bot
from telegram_bot_app.operations.telegram.integration import set_webhook

if TYPE_CHECKING:
    from django.db.models.query import QuerySet


@admin.action(description=_("Update Webhook URLs"))
def update_webhook_urls(modeladmin, request, queryset: "QuerySet[Bot]") -> None:  # noqa: ANN001, ARG001
    for bot in queryset:
        async_to_sync(set_webhook)(bot=bot)


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

    actions = (
        *BaseAdmin.actions,
        update_webhook_urls,
    )
