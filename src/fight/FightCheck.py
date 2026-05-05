from dataclasses import dataclass
from typing import Callable, Any

from fight.FightView import FightView


@dataclass(frozen=True)
class FightCheck:
    predicate: Callable[[FightView], bool]
    message_key: str
    fallback: str
    token_factory: Callable[[FightView], dict[str, Any]] = lambda v: {}
