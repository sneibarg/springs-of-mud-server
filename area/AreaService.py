import requests

from area.RomArea import RomArea
from area.RomRoom import RomRoom
from registry import RegistryService
from utilities.server_util import camel_to_snake_case, is_valid_direction


class AreaService:
    def __init__(self, injector, area_config, room_config):
        self.__name__ = "AreaService"
        from server.LoggerFactory import LoggerFactory
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry = injector.get(RegistryService)
        self.injector = injector
        self.area_config = area_config['endpoints']
        self.room_config = room_config['endpoints']
        self.areas_endpoint = self.area_config['areas_endpoint']
        self.rooms_endpoint = self.room_config['rooms_endpoint']
        self.load_areas()
        self.load_rooms()
        self.logger.info("Initialized AreaService instance with "+str(len(self.registry.area_registry)) +
                         " areas and "+str(len(self.registry.room_registry))+" rooms in memory.")

    def get_registry(self):
        return self.registry

    def load_areas(self):
        response = requests.get(self.areas_endpoint).json()
        for area_json in response:
            area = RomArea.from_json(camel_to_snake_case(area_json))
            self.logger.debug("Registering area: "+str(area))
            self.registry.register_area(area)

    def load_area(self, area_id):
        url = self.areas_endpoint + "/" + area_id
        area_json = requests.get(url).json()
        self.registry.register_area(RomArea.from_json(camel_to_snake_case(area_json)))

    def load_room(self, room_id):
        url = self.rooms_endpoint + "/" + room_id
        room_json = requests.get(url).json()
        self.registry.register_room(RomRoom.from_json(camel_to_snake_case(room_json)))

    def load_rooms(self):
        response = requests.get(self.rooms_endpoint).json()
        for room_json in response:
            room = RomRoom.from_json(camel_to_snake_case(room_json))
            self.logger.debug("Registering room: "+str(room))
            self.registry.register_room(room)

    def get_room(self, room_id) -> RomRoom:
        if room_id is None:
            self.logger.info("get_room: room_id is None")
            return None
        if room_id not in self.registry.room_registry:
            self.logger.info("get_room: room_id="+str(room_id)+" not in registry.")
            return None
        return self.registry.room_registry[room_id]

    def print_description(self, writer, room):
        if writer is None or room is None:
            self.logger.info("print_description: writer="+str(writer)+", room="+str(room))
            return
        writer.write(str(room.description+"\r\n").encode('utf-8'))

    def print_exits(self, writer, room):
        writer.write(str("Exits: ").encode('utf-8'))
        for room_exit in room.get_exits():
            if room_exit is not None and isinstance(room_exit, str):
                room = self.get_room(room_exit)
                if room is not None:
                    writer.write(str(room.name+" ").encode('utf-8'))
                else:
                    self.logger.debug("print_exits: get_room returned None.")
        writer.write("\r\n".encode('utf-8'))

    def move_mobile(self, character, direction):
        room = self.registry.room_registry[character.room_id]
        destination = is_valid_direction(direction, room)
        if destination is not None:
            destination_room = self.registry.room_registry[destination]
            character.room_id = destination
            self.print_description(character.writer, destination_room)
        else:
            character.writer.write("You can't go that direction!\r\n".encode('utf-8'))



