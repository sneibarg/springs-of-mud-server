from enum import Enum, auto


class MessageType(Enum):
    SYSTEM = auto()
    ERROR = auto()
    AUTH = auto()
    GAME = auto()
