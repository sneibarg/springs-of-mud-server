from dataclasses import dataclass

from game.GamePayload import GamePayload
from interp.Context import Context


@dataclass(frozen=True)
class InterpView:
    context: Context
    payload: GamePayload
