from typing import List
from injector import inject

from area.AreaUtil import AreaUtil
from area.Exit import Exit
from area.Room import Room
from area.RoomHelper import RoomHelper
from game.RegistryService import RegistryService
from player.Character import Character
from server.LoggerFactory import LoggerFactory
from server.messaging import MessageBus
from server.session.SessionHandler import SessionHandler


class RoomHandler:
    @inject
    def __init__(self, message_bus: MessageBus, session_handler: SessionHandler, registry_service: RegistryService, room_helper: RoomHelper):
        self.__name__ = "RoomHandler"
        self.message_bus = message_bus
        self.registry_service = registry_service
        self.room_registry = registry_service.room_registry
        self.character_registry = registry_service.character_registry
        self.session_handler = session_handler
        self.room_helper = room_helper
        self.logger = LoggerFactory.get_logger(__name__)

    async def print_in_room(self, character_id, player_handler, mobile_handler):
        character = self.character_registry.get(id=character_id)
        await player_handler.print_players_in_room(character)
        await mobile_handler.print_mobiles_in_room(character_id)

    async def move_mobile(self, character, direction):
        room = self.room_registry.get(id=character.room_id)
        destination_id = AreaUtil.is_valid_direction(direction, room)
        if destination_id is not None:
            destination_room = self.room_registry.get(id=destination_id)
            character.room_id = destination_id
            await self.print_room(character.id, destination_room)
        else:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(f"You can't go that direction!\r\n"))

    async def print_exits(self, character: Character, room: Room):
        if self.room_helper.can_see_room_vnum(character):
            lines = [f"Obvious exits from room {room.vnum}:"]
        else:
            lines = [f"Obvious exits:"]
        exits: List[Exit] = room.exits
        for direction in exits:
            destination = direction.to_room_id
            if destination is None:
                continue
            destination_room: Room = self.room_registry.get(id=destination)
            line = AreaUtil.align_exits(direction.direction, destination_room.name, destination_room.vnum, width=6)
            lines.append(line)

        text = "\n".join(lines) + "\n"
        message = self.message_bus.text_to_message(text)
        await self.message_bus.send_to_character(character.id, message)

    async def print_room(self, character_id, room: Room):
        if room is None:
            self.logger.error(f"Attempted to print room to character {character_id} but room is None")
            return
        await self.message_bus.send_to_character(character_id, self.room_helper.format_room_description(room.name, room.description))
