class RoomExitUtil:
    @staticmethod
    def find_exit(room, direction: int):
        if room is None:
            return None
        if hasattr(room, "get_exit"):
            return room.get_exit(direction)
        for exit_obj in room.exits:
            if int(getattr(exit_obj, "direction", -1)) == int(direction):
                return exit_obj
        return None
