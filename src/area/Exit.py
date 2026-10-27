from game.EnumProvider import EnumProvider
from dataclasses import dataclass
import ast
import json
from typing import Any, Mapping, ClassVar



@dataclass
class Exit:
    DIRECTION_NAMES: ClassVar[tuple[str, ...]] = ("north", "east", "south", "west", "up", "down")

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

    @classmethod
    def direction_label(cls, direction) -> str:
        if direction is None:
            return ""
        index = int(direction)
        return cls.DIRECTION_NAMES[index].capitalize() if 0 <= index < len(cls.DIRECTION_NAMES) else ""

    def format_destination(self, description: str, vnum=None, width: int = 10) -> str:
        label = self.direction_label(self.direction)
        suffix = "" if vnum is None else f" ({vnum})"
        return f"{label:{width}}- {description}{suffix}"

    def apply_door_reset(self, lock_state: int, exit_flags_enum) -> None:
        closed = EnumProvider.value(exit_flags_enum, "CLOSED", "EX_CLOSED")
        locked = EnumProvider.value(exit_flags_enum, "LOCKED", "EX_LOCKED")
        flags = int(self.exit_flags or 0)
        if lock_state == 0:
            flags &= ~closed
            flags &= ~locked
        elif lock_state == 1:
            flags |= closed
            flags &= ~locked
        elif lock_state == 2:
            flags |= closed
            flags |= locked
        self.exit_flags = flags
