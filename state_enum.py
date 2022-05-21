from enum import Enum, auto

class STATE(Enum):
    GREETING = auto()
    RUNNING=auto()
    ASKED_NAME=auto()
    QUIT=auto()