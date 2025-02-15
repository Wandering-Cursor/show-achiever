from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MainAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "achiever_app"
    verbose_name = _("Achiever App")
