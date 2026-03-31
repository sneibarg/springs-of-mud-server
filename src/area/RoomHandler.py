from injector import inject
from area.AreaUtil import AreaUtil
from area.Room import Room
from registry import RegistryService
from server.LoggerFactory import LoggerFactory
from server.messaging import MessageBus
from server.protocol import Message, MessageType


class RoomHandler:
    @inject
    def __init__(self, message_bus: MessageBus, registry_service: RegistryService):
        self.__name__ = "RoomHandler"
        self.message_bus = message_bus
        self.registry_service = registry_service
        self.logger = LoggerFactory.get_logger(__name__)
        
    def get_room(self, room_id) -> Room | None:
        if room_id is None:
            self.logger.debug("get_room: room_id is None")
            return None
        if room_id not in self.registry_service.room_registry:
            self.logger.debug("get_room: room_id="+str(room_id)+" not in registry.")
            return None
        return self.registry_service.room_registry[room_id]

    async def move_mobile(self, character, direction):
        room = self.registry_service.room_registry[character.room_id]
        destination = AreaUtil.is_valid_direction(direction, room)
        player_id = self.registry_service.character_registry[character.id]['player_id']
        if destination is not None:
            destination_room = self.registry_service.room_registry[destination]
            character.room_id = destination
            await self.print_room(player_id, destination_room)
        else:
            await self.message_bus.send_to_character(player_id, Message(type=MessageType.GAME, data={'text': "You can't go that direction!\r\n"}))

    async def print_room(self, player_id, room: Room):
        await self.message_bus.send_to_character(player_id, self.format_room_description(room.name, room.description, self.format_exits(room)))

    def get_in_room(self, character):
        loiterers = []
        for registered_characters in self.registry_service.character_registry.values():
            if registered_characters.name == character.name:
                continue
            other = self.registry_service.character_registry[registered_characters.id]["current_character"]
            if other.get_room_id() == character.get_room_id():
                loiterers.append(other)
        return loiterers

    async def to_room(self, character, message, pattern):
        in_room = self.get_in_room(character)
        cloaked_name = "Someone"
        cloaked = character.cloaked
        character_name = character.name
        if pattern is not None:
            pattern = pattern.replace('%p', cloaked_name if cloaked else character_name)
            pattern = pattern.replace('%m', message)
            message = pattern + "\r\n"
        else:
            message = message + "\r\n"

        loiterers = []
        for pc in self.registry_service.character_registry.values():
            if not pc['id'] in in_room:
                continue
            loiterers.append(pc['id'])
        await self.message_bus.send_to_room(character.room_id, Message(type=MessageType.GAME, data={"text": message}), loiterers)

    @staticmethod
    def format_exits(room) -> str:
        return AreaUtil.cardinal_direction(room)

    @staticmethod
    def format_room_description(room_name: str, description: str, exits: str) -> Message:
        text = f"[{room_name}]\r\n{description}\r\n[Exits: {exits}]"

        return Message(type=MessageType.GAME, data={'text': text})