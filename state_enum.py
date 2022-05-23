from enum import Enum, auto


class STATE(Enum):
    GREETING = auto()

    CREATE_PROFILE_NAME = auto()
    CONFIRM_NAME = auto()

    CREATE_PROFILE_PHRASE = auto()
    CONFIRM_PHRASE = auto()

    LOGIN_NAME_ENTRY = auto()
    CONFIRM_LOGIN_NAME = auto()

    LOGIN_PHRASE_ENTRY = auto()
    CONFIRM_LOGIN_PHRASE = auto()

    RUNNING = auto()
    ASK_WHAT_TO_DO = auto()

    CHECK_IF_NEW = auto()

    ADD_ENTRY = auto()
    VIEW_ENTRY = auto()

    QUIT = -1
