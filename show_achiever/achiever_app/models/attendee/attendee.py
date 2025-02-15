from typing import TYPE_CHECKING

from achiever_app.models.base import BaseMeta, BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from achiever_app.models.organization import Event


def get_randomized_name(user_hash: int) -> str:
    first_names = [
        "Happy",
        "Lucky",
        "Smart",
        "Brave",
        "Strong",
        "Fast",
        "Lazy",
        "Clever",
        "Wise",
        "Crazy",
    ]
    last_names = [
        "Fox",
        "Bear",
        "Wolf",
        "Tiger",
        "Lion",
        "Elephant",
        "Monkey",
        "Hedgehog",
        "Rabbit",
        "Panda",
    ]

    first_name = first_names[user_hash % len(first_names)]
    last_name = last_names[user_hash % len(last_names)]

    return f"{first_name} {last_name}"


class Attendee(BaseModel):
    telegram_id = models.CharField(
        verbose_name=_("Telegram ID"),
        max_length=128,
        unique=True,
    )

    first_name = models.CharField(
        verbose_name=_("First Name"),
        max_length=256,
    )

    last_name = models.CharField(
        verbose_name=_("Last Name"),
        max_length=256,
        blank=True,
    )

    username = models.CharField(
        verbose_name=_("Username"),
        max_length=256,
        blank=True,
    )

    show_publicly = models.BooleanField(
        verbose_name=_("Show Publicly"),
        help_text=_(
            "Should information about this attendee be shown publicly?"
            "(for example - name and username in the leaderboard)"
        ),
        default=False,
    )

    following_event: "Event" = models.ForeignKey(
        "achiever_app.Event",
        verbose_name=_("Following Event"),
        on_delete=models.CASCADE,
        related_name="attendees",
    )

    def __str__(self) -> str:
        return f"{_('Attendee')} - {self.first_name} {self.last_name}"

    @property
    def visible_name(self) -> str:
        if self.show_publicly:
            return f"{self.first_name} {self.last_name}"
        return get_randomized_name(
            hash(self.uuid),
        )

    class Meta(BaseMeta):
        verbose_name = _("Attendee")
        verbose_name_plural = _("Attendees")
