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
