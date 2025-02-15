from achiever_app.models.base import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Currency(BaseModel):
    name = models.CharField(
        verbose_name=_("Full Currency Name"),
        max_length=255,
    )

    code = models.CharField(
        verbose_name=_("Currency Code"),
        max_length=5,
    )

    icon = models.ImageField(
        verbose_name=_("Currency Icon"),
        upload_to="currency_icons",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{_('Currency')}: {self.code}"

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")
        constraints = (
            models.UniqueConstraint(
                fields=["code"],
                name="unique_currency_code",
            ),
        )
