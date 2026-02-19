from enum import Enum, auto


class MessageType(Enum):
    """Enumeration of message types for client-server communication"""
    # System messages
    SYSTEM = auto()
    ERROR = auto()

    # Authentication
    AUTH_REQUEST = auto()
    AUTH_RESPONSE = auto()
    AUTH_SUCCESS = auto()
    AUTH_FAILURE = auto()
    AUTH_PAYLOAD = auto()  # Client sends full auth payload
    AUTH_VALIDATE = auto()  # Server validates payload

    # Character management
    CHAR_LIST = auto()
    CHAR_SELECT = auto()
    CHAR_SELECTED = auto()
    CHAR_LOGON = auto()  # Client requests character logon with payload

    # Room/Area information
    ROOM_DESCRIPTION = auto()
    ROOM_EXITS = auto()
    ROOM_PLAYERS = auto()

    # Player interaction
    PROMPT = auto()
    INPUT = auto()
    COMMAND = auto()

    # Communication
    SAY = auto()
    TELL = auto()
    EMOTE = auto()
    ROOM_MESSAGE = auto()

    # Combat
    COMBAT_START = auto()
    COMBAT_ACTION = auto()
    COMBAT_END = auto()

    # Status updates
    HEALTH_UPDATE = auto()
    MANA_UPDATE = auto()
    MOVEMENT_UPDATE = auto()
    STATS_UPDATE = auto()

    # Items/Inventory
    INVENTORY = auto()
    ITEM_GET = auto()
    ITEM_DROP = auto()
    ITEM_USE = auto()

    # Server control
    WELCOME = auto()
    DISCONNECT = auto()
    ANSI_PROMPT = auto()
