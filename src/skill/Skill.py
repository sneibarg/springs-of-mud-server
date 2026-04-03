import json

from dataclasses import dataclass


@dataclass
class Skill:
    id: str
    name: str
    kind: str
    handler_id: str
    target: str
    min_position: str
    noun_damage: str
    msg_off: str
    msg_obj: str
    level_by_class: dict[str, int]
    rating_by_class: dict[str, int]
    slot: int
    min_mana: int
    beats: int

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Skill):
            return self.id == other.id
        return False

    @classmethod
    def from_json(cls, data) -> Skill:
        if isinstance(data, str):
            data = json.loads(data)
        from server.ServerUtil import ServerUtil
        data = ServerUtil.camel_to_snake_case(data)
        return cls(**data)
