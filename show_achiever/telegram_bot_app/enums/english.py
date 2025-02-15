# ruff: noqa: E501

from enum import StrEnum


class TelegramMessages(StrEnum):
    START = "Hello, {update.effective_user.first_name}!\nHere's your account information:"
    NOT_REGISTERED = "Dear {update.effective_user.first_name}, it seems that you are not registered. Let's fix this!"
    CHOOSE_EVENT = "Please choose the event you want to register for:"
    FALLBACK = "I'm sorry, I didn't understand that. Please try again."
