# ruff: noqa: E501

from enum import StrEnum

from telegram_bot_app.enums.commands import Commands


class TelegramMessages(StrEnum):
    START = 'Hello, {attendee.visible_name}!\nYou\'re attending "{event.name}".\nUse buttons below to manage your account.'

    NOT_REGISTERED = "Dear {update.effective_user.first_name}, it seems that you are not registered. Let's fix this!"
    REGISTER_EVENT = "Please choose the event you want to register for:"
    REGISTER_FIRST_NAME = f"You're registering for {{event.name}}.\nPlease, provide your first name, {Commands.SKIP} to use your Telegram name ({{user.first_name}})."
    REGISTER_LAST_NAME = f"Provide your last name, {Commands.SKIP} to use your Telegram last name ({{user.last_name}}), or {Commands.BLANK} to keep it blank."

    REGISTER_PUBLICITY = "Would you like to show your name in the public list of attendees?"
    REGISTER_PUBLICITY__YES = "Yes"
    REGISTER_PUBLICITY__NO = "No"

    REGISTER_CONFIRMATION = "Please confirm your registration for {event.name}.\n\nFirst name: {first_name}\nLast name: {last_name}\nPublicity: {publicity}"

    REGISTER_CONFIRMATION__CONFIRM = "Confirm"
    REGISTER_CONFIRMATION__START_OVER = "Start over"

    REGISTERED = "You have been successfully registered for the event!"

    FALLBACK = "I'm sorry, I didn't understand that. Please try again."

    BALANCES = "Here are your balances:"

    WALLET__REPRESENTATION = "{wallet_currency} - {wallet_balance}"

    # Menu Buttons

    MENU__BALANCES = "Balances 💰"
    MENU__SETTINGS = "Settings ⚙️"
    MENU__TO_START = "To Start Menu 🏠"

    # Settings

    SETTINGS = "Account Settings:"

    SETTINGS__CHANGE_EVENT = "Change Event"
    SETTINGS__TOGGLE_PUBLICITY__ON = "Show My Name"
    SETTINGS__TOGGLE_PUBLICITY__OFF = "Hide My Name"
    SETTINGS__REMOVE_ACCOUNT = "Remove Account"

    # Callback Query

    ANSWER = "Processing your request..."
