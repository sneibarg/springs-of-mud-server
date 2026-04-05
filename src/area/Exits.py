from dataclasses import dataclass
import ast
import json
from typing import Any, Mapping


@dataclass
class Exits:
    north: str
    south: str
    east: str
    west: str
    up: str
    down: str

    def get_exits(self) -> dict[str, str]:
        return {
            'north': self.north,
            'south': self.south,
            'east': self.east,
            'west': self.west,
            'up': self.up,
            'down': self.down
        }

    @classmethod
    def from_json(cls, data: Any):
        if isinstance(data, str):
            try:
                parsed = json.loads(data)
            except json.JSONDecodeError:
                try:
                    parsed = ast.literal_eval(data)
                except (SyntaxError, ValueError) as exc:
                    raise ValueError(f"Unable to parse exits value: {data!r}") from exc
        else:
            raise TypeError(f"Exits.from_json expected mapping, JSON string, or None; got {type(data).__name__}")

        return cls(**parsed)
