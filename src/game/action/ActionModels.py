from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Callable, Generic, Mapping, TypeVar

V = TypeVar("V")


def _empty_tokens(_view) -> Mapping[str, Any]:
    return {}


def _empty_plan(_view) -> "ActionPlan":
    return ActionPlan()


@dataclass(frozen=True)
class MessageRef:
    channel: str
    key: str
    fallback: str = ""
    tokens: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        object.__setattr__(self, "tokens", MappingProxyType(dict(self.tokens or {})))


@dataclass(frozen=True)
class ActionGuard(Generic[V]):
    predicate: Callable[[V], bool]
    message_key: str
    fallback: str = ""
    channel: str = "to_char"
    token_factory: Callable[[V], Mapping[str, Any]] = _empty_tokens


@dataclass(frozen=True)
class ActionPlan:
    stop: bool = True
    messages: tuple[MessageRef, ...] = ()
    operation: str = ""
    data: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        object.__setattr__(self, "messages", tuple(self.messages or ()))
        object.__setattr__(self, "data", MappingProxyType(dict(self.data or {})))


@dataclass(frozen=True)
class ActionDefinition(Generic[V]):
    name: str
    guards: tuple[ActionGuard[V], ...]
    plan_factory: Callable[[V], ActionPlan] = _empty_plan

    def __post_init__(self):
        object.__setattr__(self, "guards", tuple(self.guards or ()))
