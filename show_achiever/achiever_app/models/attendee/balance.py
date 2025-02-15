from typing import TYPE_CHECKING

from achiever_app.models.base import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from achiever_app.models.attendee.wallet import AttendeeWallet
    from achiever_app.models.organization.task import PartnerTaskItem


class AttendeeWalletBalance(BaseModel):
    wallet: "AttendeeWallet" = models.ForeignKey(
        "achiever_app.AttendeeWallet",
        verbose_name=_("Wallet"),
        on_delete=models.CASCADE,
        related_name="balances",
    )

    amount = models.DecimalField(
        verbose_name=_("Amount"),
        max_digits=20,
        decimal_places=4,
    )

    for_partner_task_item: "PartnerTaskItem" = models.ForeignKey(
        "achiever_app.PartnerTaskItem",
        verbose_name=_("Partner Task Item"),
        on_delete=models.CASCADE,
        related_name="wallet_balances",
    )

    def __str__(self) -> str:
        return f"{self.wallet} - {self.amount}"

    class Meta:
        verbose_name = _("Attendee Wallet Balance")
        verbose_name_plural = _("Attendee Wallet Balances")
        constraints = (
            models.UniqueConstraint(
                fields=("wallet", "for_partner_task_item"),
                name="unique_wallet_task",
            ),
        )
