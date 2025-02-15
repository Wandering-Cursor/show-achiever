from achiever_app.models.base import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Event(BaseModel):
    name = models.CharField(
        verbose_name=_("Event Name"),
        max_length=512,
    )

    description = models.TextField(
        verbose_name=_("Event Description"),
        blank=True,
    )

    poster = models.ImageField(
        verbose_name=_("Event Poster"),
        upload_to="event_posters/",
        blank=True,
    )

    def __str__(self) -> str:
        return f"{_('Event')} - {self.name}"

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
