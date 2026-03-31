from injector import inject
from area.AreaUtil import AreaUtil
from area.Room import Room
from registry import RoomRegistry, CharacterRegistry
from server.LoggerFactory import LoggerFactory
from server.messaging import MessageBus
from server.protocol import Message, MessageType


class RoomHandler:
    @inject
    def __init__(self, message_bus: MessageBus, room_registry: RoomRegistry, character_registry: CharacterRegistry):
        self.__name__ = "RoomHandler"
        self.message_bus = message_bus
        self.room_registry = room_registry
        self.character_registry = character_registry
        self.logger = LoggerFactory.get_logger(__name__)
        
    def get_room(self, room_id) -> Room | None:
        if room_id is None:
            self.logger.debug("get_room: room_id is None")
            return None
        if room_id not in self.room_registry:
            self.logger.debug("get_room: room_id="+str(room_id)+" not in registry.")
            return None
        return self.room_registry.get_room_by_id(room_id)

    async def move_mobile(self, character, direction):
        room = self.room_registry.get_room_by_id(character.room_id)
        destination = AreaUtil.is_valid_direction(direction, room)
        player_id = self.character_registry[character.id]['player_id']
        if destination is not None:
            destination_room = self.room_registry.get_room_by_id(destination)
            character.room_id = destination
            await self.print_room(player_id, destination_room)
        else:
            await self.message_bus.send_to_character(player_id, Message(type=MessageType.GAME, data={'text': "You can't go that direction!\r\n"}))

    async def print_room(self, player_id, room: Room):
        if room is None:
            self.logger.error(f"Attempted to print room to player {player_id} but room is None")
            return
        await self.message_bus.send_to_character(player_id, self.format_room_description(room.name, room.description, self.format_exits(room)))

    def get_in_room(self, character):
        loiterers = []
        for registered_characters in self.character_registry.registry.values():
            current_character = registered_characters.get("current_character")
            if current_character is None or current_character.name == character.name:
                continue
            if current_character.room_id == character.room_id:
                loiterers.append(current_character.id)
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

        loiterers = self._get_loiterers(in_room)
        await self.message_bus.send_to_room(character.room_id, Message(type=MessageType.GAME, data={"text": message}), loiterers)

    def _get_loiterers(self, in_room: list):
        loiterers = []
        for pc in self.character_registry.registry.values():
            character = pc.get("current_character")
            if character is None or character.id in in_room:
                continue
            loiterers.append(character.id)
        return loiterers

    @staticmethod
    def format_exits(room) -> str:
        return AreaUtil.cardinal_direction(room)

    @staticmethod
    def format_room_description(room_name: str, description: str, exits: str) -> Message:
        text = f"[{room_name}]\r\n{description}\r\n[Exits: {exits}]"

        return Message(type=MessageType.GAME, data={'text': text})