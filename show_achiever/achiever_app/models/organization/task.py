from typing import TYPE_CHECKING

from achiever_app.models.base import BaseModel
from achiever_app.models.organization.partner import Partner
from django.db import models
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from achiever_app.models.common.currency import Currency


class PartnerTask(BaseModel):
    partner = models.ForeignKey(
        Partner,
        verbose_name=_("Partner"),
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        verbose_name=_("Task Name"),
        max_length=512,
    )

    description = models.TextField(
        verbose_name=_("Task Description"),
        blank=True,
    )

    image = models.ImageField(
        verbose_name=_("Task Image"),
        upload_to="task_images/",
        blank=True,
    )

    reward_currency: "Currency" = models.ForeignKey(
        "achiever_app.Currency",
        verbose_name=_("Reward Currency"),
        on_delete=models.CASCADE,
    )

    reward_amount = models.DecimalField(
        verbose_name=_("Reward Amount"),
        max_digits=20,
        decimal_places=4,
    )

    def __str__(self) -> str:
        return f"{_('Partner Task')} - {self.name}"

    class Meta:
        verbose_name = _("Partner Task")
        verbose_name_plural = _("Partner Tasks")


class PartnerTaskItem(BaseModel):
    task = models.ForeignKey(
        PartnerTask,
        verbose_name=_("Task"),
        on_delete=models.CASCADE,
    )

    is_used = models.BooleanField(
        verbose_name=_("Is Used"),
        default=False,
    )

    def qr_code_data(self) -> str:
        return f"{self.task.pk}-{self.pk}"

    def __str__(self) -> str:
        return f"{_('Partner Task Item')} - {self.task.name} ({self.pk})"

    class Meta:
        verbose_name = _("Partner Task Item")
        verbose_name_plural = _("Partner Task Items")
