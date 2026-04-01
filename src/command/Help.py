from dataclasses import dataclass


@dataclass
class Help:
    id: str
    level: int
    keyword: str
    text: str

    @classmethod
    def from_json(cls, data):
        return cls(**data)