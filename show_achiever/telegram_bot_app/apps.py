from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MainAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "telegram_bot_app"
    verbose_name = _("Telegram Bot")
