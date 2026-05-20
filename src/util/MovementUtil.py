from __future__ import annotations

from util.GenericUtil import GenericUtil


class MovementUtil:
    DIR_NAME = ["north", "east", "south", "west", "up", "down"]
    REV_DIR = [2, 3, 0, 1, 5, 4]
    MOVEMENT_LOSS = [1, 2, 2, 3, 4, 6, 4, 1, 6, 10, 6]

    @staticmethod
    def direction_index(direction: str) -> int:
        token = (direction or "").strip().lower()
        mapping = {
            "n": 0, "north": 0,
            "e": 1, "east": 1,
            "s": 2, "south": 2,
            "w": 3, "west": 3,
            "u": 4, "up": 4,
            "d": 5, "down": 5,
        }
        return mapping.get(token, -1)

    @staticmethod
    def find_exit(room, direction: int):
        if room is None:
            return None
        if hasattr(room, "get_exit"):
            return room.get_exit(direction)
        for ex in room.exits:
            if int(getattr(ex, "direction", -1)) == int(direction):
                return ex
        return None

    @staticmethod
    def find_door(room, arg: str) -> int:
        if room is not None and hasattr(room, "find_door"):
            return room.find_door(arg)
        direction = MovementUtil.direction_index(arg)
        if direction >= 0:
            return direction if MovementUtil.find_exit(room, direction) is not None else -1

        wanted = (arg or "").strip().lower()
        if not wanted or room is None:
            return -1
        for ex in room.exits:
            keyword = (getattr(ex, "keyword", "") or "").lower()
            if wanted == keyword or wanted in keyword.split():
                return int(getattr(ex, "direction", -1))
        return -1

    @staticmethod
    def has_key(character, key: int) -> bool:
        if hasattr(character, "has_key"):
            return character.has_key(key)
        if key is None or GenericUtil.to_int(key, -1) < 0:
            return False
        wanted = str(key)
        for item in list(getattr(character, "loot", []) or []):
            if str(getattr(item, "vnum", "")) == wanted:
                return True
        return False

    @staticmethod
    def get_exit_flag(exit_flags_enum, *names: str) -> int:
        if exit_flags_enum is None:
            return 0
        for name in names:
            member = getattr(exit_flags_enum, name, None)
            if member is not None:
                return int(member.value)
        return 0

    @staticmethod
    def sector_cost(sector_type: int) -> int:
        idx = GenericUtil.to_int(sector_type, 0)
        idx = max(0, min(idx, len(MovementUtil.MOVEMENT_LOSS) - 1))
        return MovementUtil.MOVEMENT_LOSS[idx]
