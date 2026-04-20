from typing import List
from injector import inject

from area.AreaUtil import AreaUtil
from area.Exit import Exit
from area.Room import Room
from area.RoomHelper import RoomHelper
from game.RegistryService import RegistryService
from interp.Context import Context
from object.ItemUtil import ItemUtil
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

    @staticmethod
    async def print_in_room(context: Context):
        character = context.character
        player_handler = context.player_handler()
        mobile_handler = context.mobile_handler()

        await player_handler.print_players_in_room(character)
        await mobile_handler.print_mobiles_in_room(character)

        context.finish()

    async def move_player(self, character: Character, direction: str):
        room = self.room_registry.get_or_none(id=character.room_id)
        destination_id = AreaUtil.is_valid_direction(direction, room)
        destination_room = self.room_registry.get_or_none(id=destination_id)
        if room is not None and destination_room is not None:
            character.room_id = destination_id
            room.remove_player_from_room(character)
            destination_room.add_player_to_room(character)
            await self.print_room(character.id, destination_room)
        else:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(f"You can't go that direction!\r\n"))

    async def print_exits(self, character: Character):
        room = self.room_registry.get(id=character.room_id)
        if room is None:
            return
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
            if self.room_helper.can_see_room_vnum(character):
                line = AreaUtil.align_exits(direction.direction, destination_room.name, destination_room.vnum, width=6)
                lines.append(line)
            else:
                line = AreaUtil.align_exits(direction.direction, destination_room.name, None, width=6)
                lines.append(line)

        text = "\n".join(lines) + "\n"
        message = self.message_bus.text_to_message(text)
        await self.message_bus.send_to_character(character.id, message)

    async def print_room(self, character_id, room: Room):
        if room is None:
            self.logger.error(f"Attempted to print room to character {character_id} but room is None")
            return
        character = self.character_registry.get_or_none(id=character_id)
        show_description = True
        if character is not None:
            comm_flags = self.room_helper.character_macros.enums.get("commFlags")
            if hasattr(comm_flags, "COMM_BRIEF"):
                comm = int(self.room_helper.character_macros.convert_flags(getattr(character.character_flags, "comm", "0") or "0"))
                if self.room_helper.character_macros.is_set(comm, comm_flags.COMM_BRIEF.value):
                    show_description = False

        if show_description:
            await self.message_bus.send_to_character(character_id, self.room_helper.format_room_description(room.name, room.description))
        else:
            await self.message_bus.send_to_character(character_id, self.message_bus.text_to_message(f"[{room.name}]\r\n"))
        lines = ItemUtil.room_items(room)
        if lines:
            await self.message_bus.send_to_character(character_id, self.message_bus.text_to_message("\r\n".join(lines) + "\r\n"))

    async def look_direction(self, character: Character, context: Context):
        token = (context.parameters[0] if context.parameters and len(context.parameters) > 0 else "").strip()
        direction_map = {"n": 0, "north": 0, "e": 1, "east": 1, "s": 2, "south": 2, "w": 3, "west": 3, "u": 4, "up": 4, "d": 5, "down": 5}
        door = direction_map.get((token or "").strip().lower())
        if door is None:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("You do not see that here.\r\n"))
            context.finish()
            return

        room = self.room_registry.get(id=character.room_id)
        if room is None:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("Nothing special there.\r\n"))
            context.finish()
            return

        pexit = None
        for ex in room.exits:
            if ex.direction == door:
                pexit = ex
                break

        if pexit is None:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("Nothing special there.\r\n"))
            context.finish()
            return

        desc = (pexit.description or "").strip()
        if desc:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(desc + "\r\n"))
        else:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("Nothing special there.\r\n"))

        keyword = (pexit.keyword or "").strip()
        if keyword and not keyword.startswith(" "):
            flags = int(getattr(pexit, "exit_flags", 0) or 0)
            if flags & 2:  # CLOSED
                await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(f"The {keyword} is closed.\r\n"))
            elif flags & 1:  # IS_DOOR
                await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(f"The {keyword} is open.\r\n"))
        context.finish()
