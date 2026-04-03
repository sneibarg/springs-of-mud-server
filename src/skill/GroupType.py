from dataclasses import dataclass
from typing import List


@dataclass
class GroupTable:
    name: str
    rating: List[int]
    spells: List[str]

    @classmethod
    def from_json(cls, data):
        from server.ServerUtil import ServerUtil
        data = ServerUtil.camel_to_snake_case(data)
        return cls(**data)
