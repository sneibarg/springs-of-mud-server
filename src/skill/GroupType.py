from dataclasses import dataclass
from typing import List


@dataclass
class GroupType:
    id: str
    name: str
    rating: List[int]
    spells: List[str]

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, GroupType):
            return self.id == other.id
        return False

    @classmethod
    def from_json(cls, data):
        from game.GenericUtil import GenericUtil
        data = GenericUtil.camel_to_snake_case(data)
        data['id'] = GenericUtil.generate_mongo_id()
        return cls(**data)
