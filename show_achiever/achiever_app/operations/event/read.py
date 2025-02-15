from achiever_app.models.organization import Event
from django.core.exceptions import ValidationError
from mysite.errors.http_errors import NotFoundError


async def get_event_by_id(
    event_id: str,
) -> Event:
    try:
        return await Event.objects.aget(
            uuid=event_id,
        )
    except (Event.DoesNotExist, ValidationError) as e:
        raise NotFoundError(
            log_message={
                "msg": "Could not find event",
                "event_id": event_id,
            }
        ) from e


async def get_event_by_semi_unique_name(
    semi_unique_name: str,
) -> Event:
    uuid, name = semi_unique_name.split(" - ")
    try:
        return await Event.objects.aget(
            uuid__startswith=uuid,
            name=name,
        )
    except (Event.DoesNotExist, ValidationError) as e:
        raise NotFoundError(
            log_message={
                "msg": "Could not find event",
                "semi_unique_name": semi_unique_name,
            }
        ) from e


async def get_recent_events() -> list[Event]:
    iterator = Event.objects.aiterator(chunk_size=5)
    return [event async for event in iterator]
