import requests
import json

from injector import inject
from area.Exits import Exits
from area.Room import Room
from registry import RoomRegistry
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class RoomService:
    @inject
    def __init__(self, config: ServiceConfig, registry: RoomRegistry):
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
        room_exits = room_json.get('exits')
        room = Room.from_json(ServerUtil.camel_to_snake_case(room_json))
        if isinstance(room_exits, str):
            room_exits = json.loads(room_exits)
        room.exits = Exits.from_json(room_exits)
        self.registry.register_room(room)

    def load_rooms(self):
        from server.ServerUtil import ServerUtil
        response = requests.get(self.rooms_endpoint).json()
        for room_json in response:
            room_exits = Exits.from_json(room_json['exits'])
            room = Room.from_json(ServerUtil.camel_to_snake_case(room_json))
            room.exits = room_exits
            self.logger.debug("Registering room: "+str(room))
            self.registry.register_room(room)
