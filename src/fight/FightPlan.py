from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class MessageRef:
    channel: str
    key: str
    fallback: str = ""
    tokens: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class FightPlan:
    stop: bool = True
    messages: tuple[MessageRef, ...] = ()
    executor: str = ""
    data: dict[str, Any] = field(default_factory=dict)
