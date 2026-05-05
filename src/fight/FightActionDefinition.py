from dataclasses import dataclass
from typing import Callable, Any

from fight.FightCheck import FightCheck
from fight.FightView import FightView


@dataclass(frozen=True)
class FightActionDefinition:
    name: str
    checks: tuple[FightCheck, ...]
    executor: str
    plan_factory: Callable[[FightView], dict[str, Any]] = lambda v: {}
