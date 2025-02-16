from decimal import Decimal
from typing import TYPE_CHECKING

from achiever_app.models.attendee.balance import AttendeeWalletBalance
from achiever_app.models.base import BaseMeta, BaseModel
from achiever_app.models.common.currency import Currency
from django.db import models
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    import asyncio

    from achiever_app.models.attendee.attendee import Attendee


class AttendeeWalletManager(models.Manager["AttendeeWallet"]):
    def create_for_attendee(self, attendee: "Attendee") -> "AttendeeWallet":
        for currency in Currency.objects.all():
            self.create(
                attendee=attendee,
                currency=currency,
            )


class AttendeeWallet(BaseModel):
    attendee: "asyncio.Future[Attendee] | Attendee" = models.ForeignKey(
        "achiever_app.Attendee",
        verbose_name=_("Attendee"),
        on_delete=models.CASCADE,
        related_name="wallets",
    )

    currency: "asyncio.Future[Currency] | Currency" = models.ForeignKey(
        "achiever_app.Currency",
        verbose_name=_("Currency"),
        on_delete=models.CASCADE,
    )

    @property
    def current_balance(self) -> Decimal:
        try:
            return (
                AttendeeWalletBalance.objects.filter(
                    wallet=self,
                )
                .latest()
                .amount
            )
        except AttendeeWalletBalance.DoesNotExist:
            return Decimal("0")

    @property
    async def current_balance_async(self) -> Decimal:
        try:
            balance = await AttendeeWalletBalance.objects.filter(
                wallet=self,
            ).alatest()
            return balance.amount
        except AttendeeWalletBalance.DoesNotExist:
            return Decimal("0")

    objects: AttendeeWalletManager = AttendeeWalletManager()

    def __str__(self) -> str:
        return f"{self.attendee} - {self.currency}"

    class Meta(BaseMeta):
        verbose_name = _("Attendee Wallet")
        verbose_name_plural = _("Attendee Wallets")
        constraints = (
            models.UniqueConstraint(
                fields=("attendee", "currency"),
                name="unique_attendee_currency",
            ),
        )
