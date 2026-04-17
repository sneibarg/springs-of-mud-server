import json

from dataclasses import dataclass, field

from game.AffectData import AffectData


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
    source_file: str = ""
    function_name: str = ""
    affects: list[AffectData] = field(default_factory=list)

    @classmethod
    def from_json(cls, data) -> Spell:
        if isinstance(data, str):
            data = json.loads(data)
        from game.GenericUtil import GenericUtil
        payload = GenericUtil.camel_to_snake_case(data)
        raw_affects = payload.get("affects", []) or []
        payload["affects"] = [AffectData.from_json(a) for a in raw_affects]
        payload["id"] = str(payload.get("id", payload.get("_id", "")))
        return cls(**payload)

