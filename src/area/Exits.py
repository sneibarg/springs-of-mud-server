from dataclasses import dataclass


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
    def from_json(cls, data):
        import json
        import ast
        from typing import Mapping
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            try:
                data = ast.literal_eval(data)
            except (SyntaxError, ValueError):
                data = json.loads(data.replace("'", '"'))

        if not isinstance(data, Mapping):
            raise TypeError(f"Exits.from_json expected mapping or JSON string, got {type(data).__name__}")

        return cls(**data)
