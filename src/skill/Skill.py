from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from skill.Ability import Ability


@dataclass
class Skill(Ability):
    fight_executor: str = ""
    fight_plan: dict[str, Any] = field(default_factory=dict)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Skill):
            return self.id == other.id
        return False

    @classmethod
    def from_json(cls, data) -> Skill:
        payload = cls._base_payload_from_json(data)
        payload["guards"] = cls._normalize_checks(payload.get("guards"))
        payload["fight_plan"] = cls._normalize_mapping(payload.get("fight_plan"))
        return cls(**payload)

    @staticmethod
    def _normalize_mapping(value: Any) -> dict[str, Any]:
        from util.GenericUtil import GenericUtil

        if not isinstance(value, dict):
            return {}
        return GenericUtil.camel_to_snake_case(value)
