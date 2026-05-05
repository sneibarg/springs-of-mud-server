from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class FightView:
    actor: Any
    command: Any
    room: Any
    argument: str = ""
    victim: Any = None
    skill: Any = None
    spell: Any = None
    current_fighting: Any = None
    safe: bool = False
    safe_message: str = ""
    extra: dict[str, Any] = field(default_factory=dict)
