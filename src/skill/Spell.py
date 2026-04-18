import json

from dataclasses import dataclass, field

from object.Effect import Effect


@dataclass
class Spell:
    id: str
    name: str
    kind: str
    handler_id: str
    target: str
    min_position: str
    slot: int
    min_mana: int
    beats: int
    noun_damage: str
    msg_off: str
    msg_obj: str
    level_by_class: dict[str, int]
    rating_by_class: dict[str, int]
    function_name: str = ""
    affect_data: list[Effect] = field(default_factory=list)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.id == other.id
        return False

    @classmethod
    def from_json(cls, data) -> Spell:
        if isinstance(data, str):
            data = json.loads(data)
        from game.GenericUtil import GenericUtil
        payload = GenericUtil.camel_to_snake_case(data)
        raw_affects = payload.get("affect_data", []) or []
        payload["affect_data"] = [Effect.from_json(a) for a in raw_affects]
        payload["id"] = str(payload.get("id", payload.get("_id", "")))
        return cls(**payload)

