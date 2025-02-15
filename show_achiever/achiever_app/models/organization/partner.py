from typing import TYPE_CHECKING

from achiever_app.models.base import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from achiever_app.models.organization.event import Event


class Partner(BaseModel):
    name = models.CharField(
        verbose_name=_("Partner Name"),
        max_length=512,
    )

    description = models.TextField(
        verbose_name=_("Partner Description"),
        blank=True,
    )

    logo = models.ImageField(
        verbose_name=_("Partner Logo"),
        upload_to="partner_logos/",
        blank=True,
    )

    for_event: "Event" = models.ForeignKey(
        "achiever_app.Event",
        verbose_name=_("Event"),
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{_('Partner')} - {self.name}"

    class Meta:
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")
