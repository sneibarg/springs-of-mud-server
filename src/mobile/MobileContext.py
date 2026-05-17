from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from api.CharacterApi import CharacterApi


@dataclass
class MobileContext:
    actor: Any
    room: Any
    handler: Any
    special_name: str = ""
    aliases: dict[str, Any] = field(default_factory=dict)
    payloads: list[dict] = field(default_factory=list)
    done: bool = False
    performed: bool = False

    def __post_init__(self):
        self.aliases.setdefault("actor", self.actor)
        self.aliases.setdefault("room", self.room)

    def __getattr__(self, item: str):
        from api.MobileApi import MobileApi

        if hasattr(MobileApi, item):
            def _call(*args, **kwargs):
                return getattr(MobileApi, item)(self, *args, **kwargs)
            return _call
        raise AttributeError(item)

    def finish(self):
        self.done = True

    def queue_payload(self, payload: Optional[dict]):
        if payload:
            self.payloads.append(payload)

    def mark_performed(self) -> bool:
        self.performed = True
        return True

    def set_alias(self, name: str, value: Any):
        self.aliases[str(name)] = value
        return value

    def get_alias(self, name: str, default: Any = None):
        return self.aliases.get(str(name), default)

    def resolve(self, alias_or_value: Any):
        if isinstance(alias_or_value, str) and alias_or_value in self.aliases:
            return self.aliases[alias_or_value]
        return alias_or_value

    def eval_locals(self, **extras) -> dict[str, Any]:
        values = {"ctx": self, "actor": self.actor, "room": self.room}
        values.update(self.aliases)
        values.update(extras)
        return values

    def eval_bool(self, expression: str, **extras) -> bool:
        try:
            return bool(eval(str(expression), {"__builtins__": {}}, self.eval_locals(**extras)))
        except Exception:
            self.handler.logger.debug(f"Failed mobile expression '{expression}'", exc_info=True)
            return False

    def exec_expr(self, expression: str):
        return eval(str(expression), {"__builtins__": {}}, self.eval_locals())

    def is_npc(self, entity) -> bool:
        return CharacterApi.is_npc(entity)

    def same_special(self, entity) -> bool:
        return str(getattr(entity, "special_name", "") or "").strip().lower() == str(getattr(self.actor, "special_name", "") or "").strip().lower()

    def is_safe(self, entity) -> bool:
        safe, _ = self.handler.fight_handler.is_safe(self.actor, entity, room=self.room)
        return safe

    def room_players(self, exclude_ids: Optional[set[str]] = None) -> list[Any]:
        exclude = {str(value) for value in (exclude_ids or set())}
        return [player for player in self.room.players_in_room().values() if str(getattr(player, "id", "")) not in exclude]
