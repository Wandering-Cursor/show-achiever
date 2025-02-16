from achiever_app.models.attendee.attendee import Attendee
from achiever_app.models.attendee.wallet import AttendeeWallet
from achiever_app.schemas.attendee import AttendeeInfo
from asgiref.sync import sync_to_async


async def register_attendee(attendee_info: AttendeeInfo) -> Attendee:
    attendee = await Attendee.objects.acreate(
        **attendee_info.model_dump(),
    )

    await sync_to_async(AttendeeWallet.objects.create_for_attendee)(attendee=attendee)

    return attendee
