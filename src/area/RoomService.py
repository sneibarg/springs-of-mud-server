from injector import inject
from game.GameData import GameData
from area.Room import Room
from area.AreaUtil import AreaUtil
from registry.RegistryService import RegistryService
from server.LoggerFactory import LoggerFactory
from server.protocol.Message import Message, MessageType
from server.ServiceConfig import ServiceConfig
from server.messaging.MessageBus import MessageBus


class RoomService:
    @inject
    def __init__(self, config: ServiceConfig, registry: RegistryService, message_bus: MessageBus, game_data: GameData):
        self.__name__ = "RoomService"
        self.rooms_endpoint = config.rooms_endpoint
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry = registry
        self.message_bus = message_bus
        self.game_data = game_data
        self.logger.info("Initialized RoomService instance.")

    def get_room(self, room_id) -> Room | None:
        if room_id is None:
            self.logger.debug("get_room: room_id is None")
            return None
        if room_id not in self.registry.room_registry:
            self.logger.debug("get_room: room_id="+str(room_id)+" not in registry.")
            return None
        return self.registry.room_registry[room_id]

    async def print_room(self, player_id, room: Room):
        await self.message_bus.send_to_character(player_id, self.format_room_description(room.name, room.description, self.format_exits(room)))

    @staticmethod
    def format_exits(room) -> str:
        return AreaUtil.cardinal_direction(room)

    @staticmethod
    def format_room_description(room_name: str, description: str, exits: str) -> Message:
        text = f"[{room_name}]\r\n{description}\r\n[Exits: {exits}]"

        return Message(type=MessageType.GAME, data={'text': text})
