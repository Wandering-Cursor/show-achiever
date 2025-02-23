from achiever_app.models.base import BaseMeta, BaseModel
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

    SEMI_UNIQUE_NAME_FORMAT = "{uuid} - {name}"

    @property
    def semi_unique_name(self) -> str:
        return self.SEMI_UNIQUE_NAME_FORMAT.format(
            uuid=str(self.uuid)[:8],
            name=self.name,
        )

    def __str__(self) -> str:
        return f"{_('Event')} - {self.name}"

    class Meta(BaseMeta):
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
