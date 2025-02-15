from enum import StrEnum


class ApplicationStates(StrEnum):
    # Registration flow states
    REGISTER_CONVRESATION = "register"
    REGISTER_EVENT = "register_event"
    REGISTER_FIRST_NAME = "register_name"
    REGISTER_LAST_NAME = "register_last_name"
    REGISTER_USERNAME = "register_username"
    REGISTER_PUBLICITY = "register_publicity"
    REGISTER_CONFIRMATION = "register_confirmation"

    # Event flow states
