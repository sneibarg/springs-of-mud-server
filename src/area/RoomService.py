from area import RomRoom
from registry import RegistryService
from server.LoggerFactory import LoggerFactory


class RoomService:
    def __init__(self, injector, room_config):
        self.injector = injector
        self.room_config = room_config
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry = self.injector.get(RegistryService)
        self.logger.info("Initialized RoomService instance.")

    def get_room(self, room_id) -> RomRoom:
        if room_id is None:
            self.logger.info("get_room: room_id is None")
            return None
        if room_id not in self.registry.room_registry:
            self.logger.info("get_room: room_id="+str(room_id)+" not in registry.")
            return None
        return self.registry.room_registry[room_id]

    def print_room(self, writer, character):
        room: RomRoom = self.registry.room_registry[character.room_id]
        writer.write(f'[{room.name}]'.encode('utf-8'))
        room.print_description(writer, room)
        self.print_exits(writer, room)

    def print_exits(self, writer, room):
        writer.write(str("Exits: ").encode('utf-8'))
        for room_exit in room.get_exits():
            if room_exit is not None and isinstance(room_exit, str):
                room = self.get_room(room_exit)
                if room is not None:
                    writer.write(str(room.name + " ").encode('utf-8'))
                else:
                    self.logger.debug("print_exits: get_room returned None.")
        writer.write("\r\n".encode('utf-8'))