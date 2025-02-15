from django.db import models
from django.utils.translation import gettext_lazy as _


class BotPlatforms(models.TextChoices):
    TELEGRAM = "telegram", _("Telegram")
