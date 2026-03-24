import requests
from injector import inject

from area.AreaUtil import AreaUtil
from area.Area import Area
from area.Room import Room
from registry import RegistryService
from server.ServerUtil import ServerUtil
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class AreaService:
    @inject
    def __init__(self, config: ServiceConfig, registry: RegistryService):
        self.__name__ = "AreaService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry = registry
        self.areas_endpoint = config.areas_endpoint
        self.rooms_endpoint = config.rooms_endpoint
        self.load_areas()
        self.load_rooms()
        self.logger.info("Initialized AreaService instance with "+str(len(self.registry.area_registry)) +
                         " areas and "+str(len(self.registry.room_registry))+" rooms in memory.")

    def load_areas(self):
        response = requests.get(self.areas_endpoint).json()
        for area_json in response:
            area = Area.from_json(ServerUtil.camel_to_snake_case(area_json))
            self.logger.debug("Registering area: "+str(area))
            self.registry.register_area(area)

    def load_area(self, area_id):
        url = self.areas_endpoint + "/" + area_id
        area_json = requests.get(url).json()
        self.registry.register_area(Area.from_json(ServerUtil.camel_to_snake_case(area_json)))

    def load_room(self, room_id):
        url = self.rooms_endpoint + "/" + room_id
        room_json = requests.get(url).json()
        self.registry.register_room(Room.from_json(ServerUtil.camel_to_snake_case(room_json)))

    def load_rooms(self):
        response = requests.get(self.rooms_endpoint).json()
        for room_json in response:
            room = Room.from_json(ServerUtil.camel_to_snake_case(room_json))
            self.logger.debug("Registering room: "+str(room))
            self.registry.register_room(room)

    def passes_update_check(self, area_id, last_reset):
        return self.registry.area_registry[area_id].last_reset != last_reset

    def move_mobile(self, character, direction):
        room = self.registry.room_registry[character.room_id]
        destination = AreaUtil.is_valid_direction(direction, room)
        if destination is not None:
            destination_room = self.registry.room_registry[destination]
            character.room_id = destination
            room.print_description(character.writer, destination_room)
        else:
            character.writer.write("You can't go that direction!\r\n".encode('utf-8'))
