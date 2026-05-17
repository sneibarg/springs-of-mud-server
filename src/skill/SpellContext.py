from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from api.CharacterApi import CharacterApi


@dataclass
class SpellContext:
    actor: Any
    spell: Any
    handler: Any
    room: Any
    target: Any = None
    target_name: str = ""
    target_kind: str = ""
    source: str = "player"
    command_context: Any = None
    payloads: list[dict] = field(default_factory=list)
    aliases: dict[str, Any] = field(default_factory=dict)
    done: bool = False
    performed: bool = False
    failed: bool = False

    def __post_init__(self):
        self.aliases.setdefault("actor", self.actor)
        self.aliases.setdefault("spell", self.spell)
        self.aliases.setdefault("room", self.room)
        self.aliases.setdefault("target", self.target)
        self.aliases.setdefault("target_name", self.target_name)
        if self.is_character_target():
            self.aliases.setdefault("victim", self.target)
        if self.is_object_target():
            self.aliases.setdefault("obj", self.target)

    def __getattr__(self, item: str):
        api = getattr(self.handler, "spell_api", None)
        if api is not None and hasattr(api, item):
            def _call(*args, **kwargs):
                return getattr(api, item)(self, *args, **kwargs)
            return _call
        raise AttributeError(item)

    @property
    def level(self) -> int:
        return int(getattr(self.actor, "level", 0) or 0)

    def finish(self):
        self.done = True

    def mark_performed(self) -> bool:
        self.performed = True
        return True

    def stop(self) -> bool:
        self.finish()
        return False

    def queue_payload(self, payload: Optional[dict]):
        if payload:
            self.payloads.append(payload)

    def fail(self, text: str = "") -> bool:
        self.failed = True
        self.done = True
        if text and self.source == "player" and not CharacterApi.is_npc(self.actor):
            self.queue_payload({"to_char": text})
        return False

    def set_target(self, value: Any, kind: str = ""):
        self.target = value
        if kind:
            self.target_kind = str(kind)
        self.aliases["target"] = value
        if self.is_character_target():
            self.aliases["victim"] = value
        if self.is_object_target():
            self.aliases["obj"] = value
        return value

    def set_alias(self, name: str, value: Any):
        self.aliases[str(name)] = value
        return value

    def get_alias(self, name: str, default: Any = None):
        return self.aliases.get(str(name), default)

    def resolve(self, alias_or_value: Any):
        if isinstance(alias_or_value, str) and alias_or_value in self.aliases:
            return self.aliases[alias_or_value]
        return alias_or_value

    @property
    def victim(self):
        return self.target if self.is_character_target() else None

    @property
    def obj(self):
        return self.target if self.is_object_target() else None

    @property
    def is_player_source(self) -> bool:
        return self.source == "player" and not CharacterApi.is_npc(self.actor)

    def is_character_target(self) -> bool:
        target = self.target
        return target is not None and not self.is_object_target()

    def is_object_target(self) -> bool:
        target = self.target
        return target is not None and hasattr(target, "item_type")
