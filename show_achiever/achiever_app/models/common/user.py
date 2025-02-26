from achiever_app.models.base import BaseMeta, BaseModel
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class EventAdmin(BaseModel):
    user = models.OneToOneField(
        User,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="event_admin",
    )
    event = models.ForeignKey(
        "achiever_app.Event",
        verbose_name=_("Event"),
        on_delete=models.CASCADE,
        related_name="users",
        blank=True,
        null=True,
    )
    events = models.ManyToManyField(
        "achiever_app.Event",
        verbose_name=_("Events"),
        related_name="event_administrators",
        blank=True,
    )

    def __str__(self) -> str:
        return self.user.username

    class Meta(BaseMeta):
        verbose_name = _("Event Admin")
        verbose_name_plural = _("Event Admins")
