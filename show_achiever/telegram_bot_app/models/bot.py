import secrets

from django.db import models
from django.utils.translation import gettext_lazy as _
from telegram_bot_app.models.base import BaseModel
from telegram_bot_app.models.enums import BotPlatforms


class Bot(BaseModel):
    platform = models.CharField(
        max_length=256,
        choices=BotPlatforms.choices,
        default=BotPlatforms.TELEGRAM,
    )

    bot_token = models.CharField(
        max_length=256,
        unique=True,
    )
    webhook_secret = models.CharField(
        max_length=256,
        blank=True,
    )
    webhook_url_prefix = models.URLField(
        max_length=512,
    )

    @property
    def webhook_url(self) -> str:
        """
        Returns the webhook URL for the bot
        For example:
        https://example.com/api/webhook/telegram/secret_token/bot_token
        Where:
        - https://example.com/api/webhook/ is the webhook_url_prefix
        - telegram is the platform
        - secret_token is the webhook_secret
        - bot_token is the bot_token
        """
        return f"{self.webhook_url_prefix}/{self.platform}/{self.webhook_secret}/{self.bot_token}"

    def generate_secret(self) -> str:
        return secrets.token_urlsafe(32)

    def clean_webhook_secret(self) -> None:
        if not self.webhook_secret:
            self.webhook_secret = self.generate_secret()

    def clean(self) -> None:
        self.clean_webhook_secret()
        super().clean()

    def __str__(self) -> str:
        return f"{_('Bot')} - {self.platform}"

    class Meta(BaseModel.Meta):
        verbose_name = _("Bot")
        verbose_name_plural = _("Bots")
