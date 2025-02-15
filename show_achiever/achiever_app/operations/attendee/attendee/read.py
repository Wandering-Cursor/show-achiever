from achiever_app.models.attendee.attendee import Attendee
from mysite.errors.http_errors import NotFoundError


async def find_attendee(
    external_id: str,
) -> Attendee:
    try:
        return await Attendee.objects.aget(
            telegram_id=external_id,
        )
    except Attendee.DoesNotExist as e:
        raise NotFoundError(
            log_message={
                "msg": "Attendee not found",
                "external_id": external_id,
            }
        ) from e
