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
    to_area: dict[str, str] = field(default_factory=dict)
    to_world: dict[str, str] = field(default_factory=dict)
    to_wiznet: dict[str, str] = field(default_factory=dict)

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
            to_victim=cls._normalize_message_keys(normalized.get("to_victim", normalized.get("to_victim", {}))),
            to_area=cls._normalize_message_keys(normalized.get("to_area", {})),
            to_world=cls._normalize_message_keys(normalized.get("to_world", {})),
            to_wiznet=cls._normalize_message_keys(normalized.get("to_wiznet", {})),
        )

    def render(self, channel: str, key: str, fallback: str = "", **tokens) -> str:
        alias = "to_victim" if channel == "to_victim" else channel
        table = getattr(self, alias, {}) or {}
        template = table.get(key, fallback)
        rendered = str(template or "").format_map(_SafeTokens(tokens))
        legacy_tokens = {
            "%c": tokens.get("c", ""),
            "%t": tokens.get("t", ""),
            "%s": tokens.get("s", ""),
            "%d": tokens.get("d", ""),
            "%q": tokens.get("q", ""),
            "%p": tokens.get("p", ""),
            "%l": tokens.get("l", ""),
            "%T": tokens.get("T", ""),
        }
        for marker, value in legacy_tokens.items():
            rendered = rendered.replace(marker, str(value or ""))
        return rendered

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
