from enum import StrEnum


class Commands(StrEnum):
    START = "/start"
    BLANK = "/blank"
    SKIP = "/skip"

    BALANCES = "/show_balances"
    SETTINGS = "/show_settings"
    VIEW_WALLET = "/view_wallet {wallet.uuid}"

    @property
    def as_handler(self) -> str:
        return self.value.replace("/", "")
