from typing import List
from injector import inject
from area.AreaUtil import AreaUtil
from area.Exit import Exit
from area.Room import Room
from area.RoomRegistry import RoomRegistry
from area.RoomHelper import RoomHelper
from game.RegistryService import RegistryService
from player.Character import Character
from player.CharacterRegistry import CharacterRegistry
from server.LoggerFactory import LoggerFactory
from server.messaging import MessageBus
from server.protocol import Message
from server.session.SessionHandler import SessionHandler


class RoomHandler:
    @inject
    def __init__(self, message_bus: MessageBus, session_handler: SessionHandler, registry_service: RegistryService, room_helper: RoomHelper):
        self.__name__ = "RoomHandler"
        self.message_bus = message_bus
        self.registry_service = registry_service
        self.character_registry = registry_service.character_registry
        self.session_handler = session_handler
        self.room_helper = room_helper
        self.logger = LoggerFactory.get_logger(__name__)

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
        lines = [f"Obvious exits from room {room.vnum}:"]
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

    async def print_in_room(self, character_id, mobile_handler):
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
        await mobile_handler.print_mobiles_in_room(character_id)

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

    async def look_room_header(self, character: Character, player_handler):
        if player_handler.look_done(character):
            return
        ctx = player_handler.look_context(character)
        if ctx.get("branch") != "default":
            return

        room = self.room_registry.get(id=character.room_id)
        if room is None:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("You are nowhere.\r\n"))
            return

        await self.print_room(character.id, room)

    async def look_room_extra(self, character: Character, player_handler):
        if player_handler.look_done(character):
            return

        ctx = player_handler.look_context(character)
        token = (ctx.get("arg3", "") or "").strip().lower()
        if not token:
            return

        room = self.room_registry.get(id=character.room_id)
        if room is None:
            return

        extra = getattr(room, "extra_description", None)
        if extra and player_handler.look_keyword_matches(token, extra.keyword or ""):
            if player_handler.look_register_match(character):
                await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(
                    (extra.description or "") + "\r\n"))

    async def look_direction(self, character: Character, player_handler):
        if player_handler.look_done(character):
            return

        ctx = player_handler.look_context(character)
        arg1 = ctx.get("arg1", "")

        direction_map = {
            "n": 0, "north": 0,
            "e": 1, "east": 1,
            "s": 2, "south": 2,
            "w": 3, "west": 3,
            "u": 4, "up": 4,
            "d": 5, "down": 5,
        }
        if arg1 not in direction_map:
            return

        room = self.room_registry.get(id=character.room_id)
        if room is None:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("Nothing special there.\r\n"))
            return

        door = direction_map[arg1]
        exits = list(room.exits or [])
        pexit = None
        for ex in exits:
            if ex.direction == door:
                pexit = ex
                break

        if pexit is None:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("Nothing special there.\r\n"))
            return

        text = (pexit.description or "").strip()
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text + "\r\n"))
        else:
            await self.message_bus.send_to_character(character.id,
                                                     self.message_bus.text_to_message("Nothing special there.\r\n"))

        # ROM-compatible defaults (customizers can change these bits)
        EXIT_IS_DOOR_BIT = 1
        EXIT_CLOSED_BIT = 2
        try:
            flags = int(pexit.exit_flags)
        except (TypeError, ValueError):
            flags = 0

        keyword = (pexit.keyword or "").strip()
        if keyword:
            if (flags & EXIT_CLOSED_BIT) != 0:
                await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(
                    f"The {keyword} is closed.\r\n"))
            elif (flags & EXIT_IS_DOOR_BIT) != 0:
                await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(
                    f"The {keyword} is open.\r\n"))

    def _get_exclude_ids(self, in_room: list):
        exclude = []
        for session in self.session_handler.get_playing_sessions():
            char = session.character
            if char.id not in in_room:
                exclude.append(char.id)
        return exclude