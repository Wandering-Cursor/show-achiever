from typing import TYPE_CHECKING

from achiever_app.models.base import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from achiever_app.models.common.currency import Currency


class AttendeeWallet(BaseModel):
    attendee = models.ForeignKey(
        "achiever_app.Attendee",
        verbose_name=_("Attendee"),
        on_delete=models.CASCADE,
        related_name="wallets",
    )

    currency: "Currency" = models.ForeignKey(
        "achiever_app.Currency",
        verbose_name=_("Currency"),
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.attendee} - {self.currency}"

    class Meta:
        verbose_name = _("Attendee Wallet")
        verbose_name_plural = _("Attendee Wallets")
        constraints = (
            models.UniqueConstraint(
                fields=("attendee", "currency"),
                name="unique_attendee_currency",
            ),
        )
