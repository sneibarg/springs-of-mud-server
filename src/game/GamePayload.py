from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from util.GenericUtil import GenericUtil


class _SafeTokens(dict):
    def __missing__(self, key):
        return ""


@dataclass(frozen=True)
class GamePayload:
    to_char: dict[str, str] = field(default_factory=dict)
    to_room: dict[str, str] = field(default_factory=dict)
    to_victim: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_json(cls, data: Any) -> "GamePayload":
        if isinstance(data, cls):
            return data
        if not isinstance(data, dict):
            return cls()
        normalized = GenericUtil.camel_to_snake_case(data)
        return cls(
            to_char=cls._normalize_message_keys(normalized.get("to_char", {})),
            to_room=cls._normalize_message_keys(normalized.get("to_room", {})),
            to_victim=cls._normalize_message_keys(normalized.get("to_victim", {})),
        )

    def render(self, channel: str, key: str, fallback: str = "", **tokens) -> str:
        table = getattr(self, channel, {}) or {}
        template = table.get(key, fallback)
        return str(template or "").format_map(_SafeTokens(tokens))

    @staticmethod
    def _normalize_message_keys(data: Any) -> dict[str, str]:
        if not isinstance(data, dict):
            return {}
        normalized: dict[str, str] = {}
        for key, value in data.items():
            converted = GenericUtil.camel_to_snake_case({str(key): value})
            normalized_key = next(iter(converted.keys()), str(key))
            normalized[normalized_key] = str(value)
        return normalized

