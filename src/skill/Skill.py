from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from skill.Ability import Ability


@dataclass
class Skill(Ability):
    guards: list[dict[str, Any]] = field(default_factory=list)
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
    def _normalize_checks(value: Any) -> list[dict[str, Any]]:
        from util.GenericUtil import GenericUtil

        if not isinstance(value, list):
            return []

        normalized: list[dict[str, Any]] = []
        for entry in value:
            if isinstance(entry, str):
                text = entry.strip()
                if text:
                    normalized.append({"predicate": text})
                continue
            if not isinstance(entry, dict):
                continue
            check = GenericUtil.camel_to_snake_case(entry)
            predicate = str(check.get("predicate", check.get("lambda", "")) or "").strip()
            if not predicate:
                continue
            raw_message_key = str(check.get("message_key", "") or "").strip()
            normalized_message_key = ""
            if raw_message_key:
                normalized_message_key = next(iter(GenericUtil.camel_to_snake_case({raw_message_key: ""}).keys()), raw_message_key)
            normalized.append(
                {
                    "predicate": predicate,
                    "message_key": normalized_message_key,
                    "fallback": str(check.get("fallback", "") or ""),
                    "token_factory": str(check.get("token_factory", "") or "").strip(),
                }
            )
        return normalized

    @staticmethod
    def _normalize_mapping(value: Any) -> dict[str, Any]:
        from util.GenericUtil import GenericUtil

        if not isinstance(value, dict):
            return {}
        return GenericUtil.camel_to_snake_case(value)
