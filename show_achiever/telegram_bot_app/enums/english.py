# ruff: noqa: E501

from enum import StrEnum


class TelegramMessages(StrEnum):
    START = "Hello, {attendee.visible_name}!\nHere's your account information:"

    NOT_REGISTERED = "Dear {update.effective_user.first_name}, it seems that you are not registered. Let's fix this!"
    REGISTER_EVENT = "Please choose the event you want to register for:"
    REGISTER_FIRST_NAME = "You're registering for {event.name}.\nPlease, provide your first name, /skip to use your Telegram name ({user.first_name})."
    REGISTER_LAST_NAME = "Provide your last name, /skip to use your Telegram last name ({user.last_name}), or /blank to keep it blank."
    REGISTER_PUBLICITY = "Would you like to show your name in the public list of attendees?"
    REGISTER_PUBLICITY__YES = "Yes"
    REGISTER_PUBLICITY__NO = "No"
    REGISTER_CONFIRMATION = "Please confirm your registration for {event.name}.\n\nFirst name: {first_name}\nLast name: {last_name}\nPublicity: {publicity}"
    REGISTER_CONFIRMATION__CONFIRM = "Confirm"
    REGISTER_CONFIRMATION__START_OVER = "Start over"

    FALLBACK = "I'm sorry, I didn't understand that. Please try again."
