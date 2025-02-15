from telegram_bot_app.enums.english import TelegramMessages


def get_class(language: str) -> type[TelegramMessages]:
    match language:
        case "en":
            return TelegramMessages
        case _:
            return TelegramMessages
