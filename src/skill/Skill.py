from __future__ import annotations

import json

from dataclasses import dataclass, field
from typing import Any

from game.GamePayload import GamePayload


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
    payload: GamePayload = field(default_factory=GamePayload)
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
        if isinstance(data, str):
            data = json.loads(data)
        from util.GenericUtil import GenericUtil
        payload = GenericUtil.camel_to_snake_case(data)
        payload["id"] = cls._extract_id(data, payload)
        payload["payload"] = GamePayload.from_json(payload.get("payload"))
        payload["guards"] = cls._normalize_checks(payload.get("guards"))
        payload["fight_plan"] = cls._normalize_mapping(payload.get("fight_plan"))
        payload.pop("_id", None)
        return cls(**payload)

    def message(self, channel: str, key: str, fallback: str = "", **values) -> str:
        return self.payload.render(channel, key, fallback=fallback, **values)

    @staticmethod
    def _extract_id(source: dict[str, Any], payload: dict[str, Any]) -> str:
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
