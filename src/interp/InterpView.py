from dataclasses import dataclass
from typing import Optional

from game.GamePayload import GamePayload
from interp.Context import Context


@dataclass(frozen=True)
class InterpView:
    context: Context
    payload: Optional[GamePayload] = None
