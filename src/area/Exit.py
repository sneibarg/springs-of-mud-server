from dataclasses import dataclass
import ast
import json
from typing import Any, Mapping


@dataclass
class Exit:
    direction: int
    description: str
    keyword: str
    exit_flags: int
    key: int
    to_room_vnum: int
    to_room_id: str
    room_id: str

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
        elif isinstance(data, Mapping):
            parsed = dict(data)
        else:
            raise TypeError(f"Exit.from_json expected mapping or JSON string; got {type(data).__name__}")

        if not isinstance(parsed, Mapping):
            raise TypeError(f"Parsed exit must be a mapping, got {type(parsed).__name__}")
        return cls(**parsed)
