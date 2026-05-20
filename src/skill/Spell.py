import json

from dataclasses import dataclass, field

from game.GamePayload import GamePayload
from item.Item import Item
from item.Effect import Effect


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
    lambdas: list[str] = field(default_factory=list)
    affect_data: list[Effect] = field(default_factory=list)
    payload: GamePayload = field(default_factory=GamePayload)

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
        from util.GenericUtil import GenericUtil
        payload = GenericUtil.camel_to_snake_case(data)
        payload["id"] = cls._extract_id(data, payload)
        raw_affects = payload.get("affect_data", []) or []
        payload["affect_data"] = [Effect.from_json(a) for a in raw_affects]
        payload["lambdas"] = cls._normalize_lambdas(payload.get("lambdas"))
        # payload["payload"] = GamePayload.from_json(payload.get("payload"))
        payload.pop("_id", None)
        return cls(**payload)

    @staticmethod
    def _extract_id(source: dict, payload: dict) -> str:
        raw_id = payload.get("id")
        if isinstance(raw_id, str) and raw_id.strip():
            return raw_id.strip()

        nested_id = source.get("_id")
        if isinstance(nested_id, dict):
            oid = nested_id.get("$oid")
            if oid:
                return str(oid)

        if nested_id:
            return str(nested_id)
        return ""

    @staticmethod
    def _normalize_lambdas(value) -> list[str]:
        if isinstance(value, list):
            return [str(entry).strip() for entry in value if str(entry).strip()]
        if isinstance(value, str) and value.strip().startswith("lambda "):
            return [value.strip()]
        return []

    def message(self, channel: str, key: str, fallback: str = "", **values) -> str:
        return self.payload.render(channel, key, fallback=fallback, **values)
