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
