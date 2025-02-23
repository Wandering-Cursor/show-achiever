from achiever_app.schemas.base import Schema


class AttendeeInfo(Schema):
    telegram_id: str
    first_name: str
    last_name: str = ""
    username: str | None = None
    show_publicly: bool = False

    following_event_id: str
