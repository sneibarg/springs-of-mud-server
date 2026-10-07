from dataclasses import dataclass, fields
from enum import IntEnum


class InGameNoteEnum(IntEnum):
    NOTE_NOTE = 0
    NOTE_IDEA = 1
    NOTE_PENALTY = 2
    NOTE_NEWS = 3
    NOTE_CHANGES = 4


@dataclass
class InGameNote:
    id: str = ""
    valid: bool = True
    type: int = 0
    sender: str = ""
    date: str = ""
    to_list: str = ""
    subject: str = ""
    text: str = ""
    date_stamp: int = 0

    @classmethod
    def from_json(cls, data):
        from util.GenericUtil import GenericUtil
        data = GenericUtil.camel_to_snake_case(data)
        allowed = {field.name for field in fields(cls)}
        filtered = {key: value for key, value in data.items() if key in allowed}
        filtered.setdefault("valid", True)
        return cls(**filtered)

    def to_json(self):
        return {
            "id": self.id,
            "type": int(self.type),
            "sender": self.sender,
            "date": self.date,
            "toList": self.to_list,
            "subject": self.subject,
            "text": self.text,
            "dateStamp": int(self.date_stamp),
        }
