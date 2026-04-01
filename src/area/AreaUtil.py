class AreaUtil:
    def __init__(self):
        pass

    @staticmethod
    def align_exits(direction: str, description: str, vnum: str, width: int = 10) -> str:
        return f"{direction:{width}}{'- '}{description} ({vnum})"

    @staticmethod
    def cardinal_direction(room):
        directions = [
            ("North", room.exit_north),
            ("South", room.exit_south),
            ("East", room.exit_east),
            ("West", room.exit_west),
            ("Up", room.exit_up),
            ("Down", room.exit_down),
        ]

        return ", ".join(name for name, value in directions if value)

    @staticmethod
    def is_valid_direction(direction, room):
        if "east" in direction:
            return room.exit_east
        if "west" in direction:
            return room.exit_west
        if "north" in direction:
            return room.exit_north
        if "south" in direction:
            return room.exit_south
        if "up" in direction:
            return room.exit_up
        if "down" in direction:
            return room.exit_down
        return None
