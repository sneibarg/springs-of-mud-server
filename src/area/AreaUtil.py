from enum import IntEnum


class DirectionEnum(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    UP = 4
    DOWN = 5


class AreaUtil:
    def __init__(self):
        pass

    @staticmethod
    def align_exits(direction: int, description: str, vnum: str, width: int = 10) -> str:
        dir_name = ""
        if direction == DirectionEnum.NORTH:
            dir_name = "North"
        elif direction == DirectionEnum.EAST:
            dir_name = "East"
        elif direction == DirectionEnum.SOUTH:
            dir_name = "South"
        elif direction == DirectionEnum.WEST:
            dir_name = "West"
        elif direction == DirectionEnum.UP:
            dir_name = "Up"
        elif direction == DirectionEnum.DOWN:
            dir_name = "Down"
        return f"{dir_name:{width}}{'- '}{description} ({vnum})"

    @staticmethod
    def cardinal_direction(room) -> str:
        if not room.exits:
            return "none"

        dir_map = {
            DirectionEnum.NORTH: "North",
            DirectionEnum.EAST:  "East",
            DirectionEnum.SOUTH: "South",
            DirectionEnum.WEST:  "West",
            DirectionEnum.UP:    "Up",
            DirectionEnum.DOWN:  "Down",
        }

        visible = []
        for exit_obj in room.exits:
            if exit_obj.direction is not None:
                name = dir_map.get(DirectionEnum(exit_obj.direction))
                if name:
                    visible.append(name)

        return ", ".join(visible) if visible else "none"

    @staticmethod
    def is_valid_direction(direction, room):
        for destination in room.exits:
            if destination.direction == DirectionEnum[direction.upper()].value:
                return destination.to_room_id
        return None

    @staticmethod
    def get_exit_by_direction(room, direction: int):
        for exit_obj in room.exits:
            if int(getattr(exit_obj, "direction", -1)) == int(direction):
                return exit_obj
        return None

    @staticmethod
    def _exit_flag_value(exit_flags_enum, *names: str) -> int:
        if exit_flags_enum is None:
            return 0
        for name in names:
            member = getattr(exit_flags_enum, name, None)
            if member is not None:
                return int(member.value)
        return 0

    @staticmethod
    def apply_door_reset(exit_obj, lock_state: int, exit_flags_enum):
        if exit_obj is None:
            return
        is_door = AreaUtil._exit_flag_value(exit_flags_enum, "IS_DOOR", "EX_ISDOOR")
        closed = AreaUtil._exit_flag_value(exit_flags_enum, "CLOSED", "EX_CLOSED")
        locked = AreaUtil._exit_flag_value(exit_flags_enum, "LOCKED", "EX_LOCKED")
        flags = int(getattr(exit_obj, "exit_flags", 0) or 0)
        if is_door and (flags & is_door) == 0:
            return

        if lock_state == 0:
            flags &= ~closed
            flags &= ~locked
        elif lock_state == 1:
            flags |= closed
            flags &= ~locked
        elif lock_state == 2:
            flags |= closed
            flags |= locked
        exit_obj.exit_flags = flags

    @staticmethod
    def randomize_room_exits(room, max_exits: int, rng):
        if room is None or max_exits <= 1:
            return

        slots = {i: None for i in range(6)}
        for exit_obj in room.exits:
            direction = int(getattr(exit_obj, "direction", -1))
            if 0 <= direction <= 5:
                slots[direction] = exit_obj

        upper = min(max_exits, 6)
        for d0 in range(upper - 1):
            d1 = rng.number_range(d0, upper - 1)
            slots[d0], slots[d1] = slots[d1], slots[d0]

        rebuilt = []
        for direction in range(6):
            exit_obj = slots[direction]
            if exit_obj is not None:
                exit_obj.direction = direction
                rebuilt.append(exit_obj)
        room.exits = rebuilt
