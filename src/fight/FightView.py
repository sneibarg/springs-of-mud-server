from dataclasses import dataclass, field
from typing import Any

from game.GamePayload import GamePayload
from interp.Context import Context


@dataclass(frozen=True)
class FightView:
    context: Context
    payload: GamePayload
    victim: Any = None
    skill: Any = None
    spell: Any = None
    extra: dict[str, Any] = field(default_factory=dict)

    @property
    def actor(self) -> Any:
        return self.context.character

    @property
    def command(self) -> Any:
        return self.context.command

    @property
    def room(self) -> Any:
        if "room" in self.extra:
            return self.extra.get("room")
        return self.context.room

    @property
    def argument(self) -> str:
        return str(self.extra.get("argument", "") or "")

    @property
    def current_fighting(self) -> Any:
        actor = self.actor
        return getattr(actor, "fighting", None) if actor is not None else None

    @property
    def safe(self) -> bool:
        return bool(self.extra.get("safe", False))

    @property
    def safe_message(self) -> str:
        return str(self.extra.get("safe_message", "") or "")
