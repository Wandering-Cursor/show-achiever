from typing import TYPE_CHECKING

from achiever_app.models.base import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from achiever_app.models.attendee.balance import AttendeeWalletBalance
    from achiever_app.models.common.currency import Currency
    from achiever_app.models.organization.event import Event


class Goal(BaseModel):
    name = models.CharField(
        verbose_name=_("Goal Name"),
        max_length=512,
    )

    description = models.TextField(
        verbose_name=_("Goal Description"),
        blank=True,
    )

    poster = models.ImageField(
        verbose_name=_("Goal Poster"),
        upload_to="goal_posters/",
        blank=True,
    )

    for_event: "Event" = models.ForeignKey(
        "achiever_app.Event",
        verbose_name=_("Event"),
        on_delete=models.CASCADE,
    )

    currency: "Currency" = models.ForeignKey(
        "achiever_app.Currency",
        verbose_name=_("Currency"),
        on_delete=models.CASCADE,
    )
    required_amount = models.DecimalField(
        verbose_name=_("Required Amount"),
        max_digits=20,
        decimal_places=4,
    )

    def __str__(self) -> str:
        return f"{_('Goal')} - {self.name}"

    class Meta:
        verbose_name = _("Goal")
        verbose_name_plural = _("Goals")


class GoalTransaction(BaseModel):
    goal: Goal = models.ForeignKey(
        Goal,
        verbose_name=_("Goal"),
        on_delete=models.CASCADE,
    )

    amount = models.DecimalField(
        verbose_name=_("Amount"),
        max_digits=20,
        decimal_places=4,
    )
    from_attendee_balance: "AttendeeWalletBalance" = models.ForeignKey(
        "achiever_app.AttendeeWalletBalance",
        verbose_name=_("From Attendee Balance"),
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.goal} - {self.amount}"

    class Meta:
        verbose_name = _("Goal Transaction")
        verbose_name_plural = _("Goal Transactions")


class GoalBalance(BaseModel):
    goal: Goal = models.ForeignKey(
        Goal,
        verbose_name=_("Goal"),
        on_delete=models.CASCADE,
    )

    amount = models.DecimalField(
        verbose_name=_("Amount"),
        max_digits=20,
        decimal_places=4,
    )
    goal_transaction = models.ForeignKey(
        GoalTransaction,
        verbose_name=_("Goal Transaction"),
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.goal} - {self.amount}"

    class Meta:
        verbose_name = _("Goal Balance")
        verbose_name_plural = _("Goal Balances")
