import re
from enum import StrEnum


class Commands(StrEnum):
    START = "/start"
    BLANK = "/blank"
    SKIP = "/skip"

    BALANCES = "/show_balances"
    SETTINGS = "/show_settings"
    VIEW_WALLET = "/view_wallet {wallet.uuid}"

    TO_START = "to_start"

    CHANGE_EVENT = "change_event"
    CHANGE_EVENT_CONFIRMATION = "change_event {event.uuid}"

    TOGGLE_PUBLICITY = "toggle_publicity"
    REMOVE_ACCOUNT = "remove_account"

    @property
    def as_command(self) -> str:
        return self.value.replace("/", "")

    @property
    def as_regex(self) -> str:
        pattern = re.sub(r"\{[^}]+\}", ".*", self.as_command)
        return f"^{pattern}$"
