from enum import Enum, auto


class STATE(Enum):
    GREETING = auto()
    RUNNING = auto()

    CREATE_PROFILE_NAME = auto()
    CONFIRM_NAME = auto()

    CREATE_PROFILE_PHRASE = auto()
    CONFIRM_PHRASE = auto()

    CHECK_IF_NEW = auto()

    ADD_ENTRY = auto()
    VIEW_ENTRY = auto()

    QUIT = -1
