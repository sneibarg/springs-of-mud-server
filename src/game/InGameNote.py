from dataclasses import dataclass
from enum import IntEnum


class InGameNoteEnum(IntEnum):
    NOTE_NOTE = 0
    NOTE_IDEA = 1
    NOTE_PENALTY = 2
    NOTE_NEWS = 3
    NOTE_CHANGES = 4


@dataclass
class InGameNote:
    valid: bool
    type: int
    sender: str
    date: str
    to_list: str
    subject: str
    text: str
    date_stamp: int
