import requests

from area.Room import Room
from registry.RegistryService import RegistryService
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class RoomService:
    def __init__(self, config: ServiceConfig, registry: RegistryService):
        self.__name__ = "RoomService"
        self.rooms_endpoint = config.rooms_endpoint
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry = registry
        self.load_rooms()
        self.logger.info("Initialized RoomService instance.")

    def load_room(self, room_id):
        from server.ServerUtil import ServerUtil
        url = self.rooms_endpoint + "/" + room_id
        room_json = requests.get(url).json()
        self.registry.register_room(Room.from_json(ServerUtil.camel_to_snake_case(room_json)))

    def load_rooms(self):
        from server.ServerUtil import ServerUtil
        response = requests.get(self.rooms_endpoint).json()
        for room_json in response:
            room = Room.from_json(ServerUtil.camel_to_snake_case(room_json))
            self.logger.debug("Registering room: "+str(room))
            self.registry.register_room(room)
