import json

from dataclasses import dataclass, field

from item.Effect import Effect
from skill.Ability import Ability


@dataclass
class Spell(Ability):
    function_name: str = ""
    lambdas: list[str] = field(default_factory=list)
    affect_data: list[Effect] = field(default_factory=list)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Spell):
            return self.id == other.id
        return False

    @classmethod
    def from_json(cls, data) -> Spell:
        if isinstance(data, str):
            data = json.loads(data)
        payload = cls._base_payload_from_json(data)
        raw_affects = payload.get("affect_data", []) or []
        payload["affect_data"] = [Effect.from_json(a) for a in raw_affects]
        payload["lambdas"] = cls._normalize_lambdas(payload.get("lambdas"))
        return cls(**payload)

    @staticmethod
    def _normalize_lambdas(value) -> list[str]:
        if isinstance(value, list):
            return [str(entry).strip() for entry in value if str(entry).strip()]
        if isinstance(value, str) and value.strip().startswith("lambda "):
            return [value.strip()]
        return []

