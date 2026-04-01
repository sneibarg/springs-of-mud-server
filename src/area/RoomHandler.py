from typing import List

from injector import inject
from area.AreaUtil import AreaUtil
from area.Room import Room
from player.Character import Character
from registry import RoomRegistry, CharacterRegistry
from server.LoggerFactory import LoggerFactory
from server.messaging import MessageBus
from server.protocol import Message, MessageType
from server.session.SessionHandler import SessionHandler


class RoomHandler:
    @inject
    def __init__(self, message_bus: MessageBus, room_registry: RoomRegistry, character_registry: CharacterRegistry, session_handler: SessionHandler):
        self.__name__ = "RoomHandler"
        self.message_bus = message_bus
        self.room_registry = room_registry
        self.character_registry = character_registry
        self.session_handler = session_handler
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
        if destination is not None:
            destination_room = self.room_registry.get_room_by_id(destination)
            character.room_id = destination
            await self.print_room(character.id, destination_room)
        else:
            await self.message_bus.send_to_character(character.id, Message(type=MessageType.GAME, data={'text': "You can't go that direction!\r\n"}))

    async def print_room(self, character_id, room: Room):
        if room is None:
            self.logger.error(f"Attempted to print room to character {character_id} but room is None")
            return
        await self.message_bus.send_to_character(character_id, self.format_room_description(room.name, room.description, self.format_exits(room)))

    async def print_in_room(self, character_id):
        character = self.character_registry.get_character_by_id(character_id)
        in_room = self.get_in_room(character)
        characters_in_room: List[Character] = [self.character_registry.get_character_by_id(char_id) for char_id in in_room]
        message = ""
        for char_in_room in characters_in_room:
            name = char_in_room.name if not char_in_room.cloaked else "Someone"
            message = message + f"{name} is here.\r\n"
        await self.message_bus.send_to_character(character_id, Message(type=MessageType.GAME, data={"text": message}))

    def get_in_room(self, character: Character):
        loiterers = []
        for session in self.session_handler.get_playing_sessions():
            char: Character = session.character
            if char.id == character.id:
                continue
            if char.room_id == character.room_id:
                loiterers.append(char.id)
        return loiterers

    async def to_room(self, character, message, pattern):
        in_room = self.get_in_room(character)
        cloaked_name = "Someone"
        if pattern is not None:
            pattern = pattern.replace('%p', cloaked_name if character.cloaked else character.name)
            pattern = pattern.replace('%m', message)
            message = pattern + "\r\n"
        else:
            message = message + "\r\n"

        exclude = self._get_exclude_ids(in_room)
        await self.message_bus.send_to_room(character.room_id, Message(type=MessageType.GAME, data={"text": message}), exclude)

    def _get_exclude_ids(self, in_room: list):
        exclude = []
        for session in self.session_handler.get_playing_sessions():
            char = session.character
            if char.id not in in_room:
                exclude.append(char.id)
        return exclude

    @staticmethod
    def format_exits(room) -> str:
        return AreaUtil.cardinal_direction(room)

    @staticmethod
    def format_room_description(room_name: str, description: str, exits: str) -> Message:
        text = f"[{room_name}]\r\n{description}\r\n[Exits: {exits}]"

        return Message(type=MessageType.GAME, data={'text': text})
