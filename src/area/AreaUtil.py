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
    def cardinal_direction(room):
        directions = [
            ("North", room.exits.north),
            ("South", room.exits.south),
            ("East", room.exits.east),
            ("West", room.exits.west),
            ("Up", room.exits.up),
            ("Down", room.exits.down),
        ]

        return ", ".join(name for name, value in directions if value)

    @staticmethod
    def is_valid_direction(direction, room):
        for destination in room.exits:
            if destination.keyword == direction:
                return destination.to_room_id
        return None
