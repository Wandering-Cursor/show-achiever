from typing import TYPE_CHECKING

from achiever_app.models.attendee.wallet import AttendeeWallet

if TYPE_CHECKING:
    from achiever_app.models.attendee.attendee import Attendee


async def get_wallets(attendee: "Attendee") -> list[AttendeeWallet]:
    iterator = AttendeeWallet.objects.filter(
        attendee=attendee,
    ).aiterator()

    return [wallet async for wallet in iterator]
