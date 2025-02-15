from achiever_app.models.attendee.attendee import Attendee
from achiever_app.schemas.attendee import AttendeeInfo


async def register_attendee(attendee_info: AttendeeInfo) -> Attendee:
    return await Attendee.objects.acreate(
        **attendee_info.model_dump(),
    )
