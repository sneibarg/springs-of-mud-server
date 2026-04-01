class AreaUtil:
    def __init__(self):
        pass

    @staticmethod
    def align_exits(direction: str, description: str, vnum: str, width: int = 10) -> str:
        return f"{direction:{width}}{'- '}{description} ({vnum})"

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
        exits = room.exits.get_exits()
        return exits[direction] if exits[direction] is not None else None
