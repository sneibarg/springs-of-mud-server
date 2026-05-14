import json

from dataclasses import dataclass, field
from typing import Any, Optional

from game.GamePayload import GamePayload
from interp.HelpEntry import HelpEntry


@dataclass
class Command:
    _id: str
    id: str
    name: str
    shortcuts: str
    role: str
    position: str
    enabled: bool
    lambdas: list[str]
    function: list[str]
    usage: str
    level: int
    max_arguments: int
    pipeline: bool = False
    message: Optional[str] = None
    skill_id: Optional[str] = None
    log: Optional[str] = field(default=None)
    help: Optional[HelpEntry] = field(default=None)
    payload: GamePayload = field(default_factory=GamePayload)
    checks: list[dict[str, Any]] = field(default_factory=list)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Command):
            return self.id == other.id
        return False

    @classmethod
    def from_json(cls, data):
        if isinstance(data, str):
            data = json.loads(data)
        from util.GenericUtil import GenericUtil
        data['id'] = GenericUtil.generate_mongo_id()
        data['_id'] = GenericUtil.generate_mongo_id()
        data = GenericUtil.camel_to_snake_case(data)
        data["payload"] = GamePayload.from_json(data.get("payload"))
        data["checks"] = cls._normalize_checks(data.get("checks"))
        return cls(**data)

    def render_message(self, channel: str, key: str, fallback: str = "", **values) -> str:
        return self.payload.render(channel, key, fallback=fallback, **values)

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
                    "channel": str(check.get("channel", "") or "").strip(),
                    "message_key": normalized_message_key,
                    "fallback": str(check.get("fallback", "") or ""),
                    "token_factory": str(check.get("token_factory", "") or "").strip(),
                }
            )
        return normalized
