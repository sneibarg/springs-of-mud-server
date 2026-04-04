from typing import List
from injector import inject
from area.AreaUtil import AreaUtil
from area.Exits import Exits
from area.Room import Room
from area.RoomRegistry import RoomRegistry
from player.Character import Character
from player.CharacterRegistry import CharacterRegistry
from server.LoggerFactory import LoggerFactory
from server.messaging import MessageBus
from server.protocol import Message
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

    async def move_mobile(self, character, direction):
        room = self.room_registry.get_room_by_id(character.room_id)
        destination_id = AreaUtil.is_valid_direction(direction, room)
        if destination_id is not None:
            destination_room = self.room_registry.get_room_by_id(destination_id)
            character.room_id = destination_id
            await self.print_room(character.id, destination_room)
        else:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(f"You can't go that direction!\r\n"))

    async def print_exits(self, character: Character, room: Room):
        lines = [f"Obvious exits from room {room.vnum}:"]
        exits: Exits = room.exits
        destination_rooms = exits.get_exits()
        for direction in destination_rooms:
            destination = destination_rooms[direction]
            if destination is None:
                continue
            destination_room: Room = self.room_registry.get_room_by_id(destination)
            line = AreaUtil.align_exits(direction.capitalize(), destination_room.name, destination_room.vnum, width=6)
            lines.append(line)

        text = "\n".join(lines) + "\n"
        message = self.message_bus.text_to_message(text)
        await self.message_bus.send_to_character(character.id, message)

    async def print_room(self, character_id, room: Room):
        if room is None:
            self.logger.error(f"Attempted to print room to character {character_id} but room is None")
            return
        await self.message_bus.send_to_character(character_id, self.format_room_description(room.name, room.description))

    async def print_in_room(self, character_id):
        character = self.character_registry.get(id=character_id)
        in_room = self.get_in_room(character)
        characters_in_room: List[Character] = [self.character_registry.get(id=char_id) for char_id in in_room]
        text = ""
        for char_in_room in characters_in_room:
            if char_in_room.cloaked:
                continue
            name = char_in_room.name
            text = text + f"{name} {char_in_room.title} is here.\r\n"
        message = self.message_bus.text_to_message(text)
        await self.message_bus.send_to_character(character_id, message)

    async def to_room(self, character, message, pattern):
        in_room = self.get_in_room(character)
        cloaked_name = "Someone"
        if pattern is not None:
            pattern = pattern.replace('%p', cloaked_name if character.cloaked else character.name)
            pattern = pattern.replace('%m', message)
            message = pattern + "\r\n"
        else:
            message = message + "\r\n"

        await self.message_bus.send_to_room(character.room_id, self.message_bus.text_to_message(message), self._get_exclude_ids(in_room))

    def get_room(self, room_id) -> Room | None:
        if room_id is None:
            self.logger.debug("get_room: room_id is None")
            return None
        if room_id not in self.room_registry:
            self.logger.debug("get_room: room_id="+str(room_id)+" not in registry.")
            return None
        return self.room_registry.get_room_by_id(room_id)

    def get_in_room(self, character: Character):
        loiterers = []
        for session in self.session_handler.get_playing_sessions():
            char: Character = session.character
            if char.id == character.id:
                continue
            if char.room_id == character.room_id:
                loiterers.append(char.id)
        return loiterers

    def format_room_description(self, room_name: str, description: str) -> Message:
        return self.message_bus.text_to_message(f"[{room_name}]\r\n{description}\r\n")

    def _get_exclude_ids(self, in_room: list):
        exclude = []
        for session in self.session_handler.get_playing_sessions():
            char = session.character
            if char.id not in in_room:
                exclude.append(char.id)
        return exclude
