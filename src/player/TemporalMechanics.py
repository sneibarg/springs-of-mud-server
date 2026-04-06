import json
import ast

from typing import Mapping
from dataclasses import dataclass


@dataclass
class TemporalMechanics:
    played: int
    logon: int
    pulse_wait: int
    pulse_daze: int

    @classmethod
    def from_json(cls, data):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            try:
                data = ast.literal_eval(data)
            except (SyntaxError, ValueError):
                data = json.loads(data.replace("'", '"'))

        if not isinstance(data, Mapping):
            raise TypeError(f"TemporalMechanics.from_json expected mapping or JSON string, got {type(data).__name__}")