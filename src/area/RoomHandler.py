from typing import List
from injector import inject

from util.AreaUtil import AreaUtil
from area.Exit import Exit
from area.Room import Room
from game.RegistryService import RegistryService
from interp.Context import Context
from util.ItemUtil import ItemUtil
from player.Character import Character
from api.CharacterApi import CharacterApi
from server.LoggerFactory import LoggerFactory
from server.messaging import MessageBus
from server.session.SessionHandler import SessionHandler


class RoomHandler:
    @inject
    def __init__(self, message_bus: MessageBus, session_handler: SessionHandler, registry_service: RegistryService):
        self.__name__ = "RoomHandler"
        self.message_bus = message_bus
        self.registry_service = registry_service
        self.room_registry = registry_service.room_registry
        self.character_registry = registry_service.character_registry
        self.session_handler = session_handler
        self.logger = LoggerFactory.get_logger(__name__)

    @staticmethod
    async def print_in_room(context: Context):
        player_handler = context.player_handler()
        mobile_handler = context.mobile_handler()

        await player_handler.print_players_in_room(context.character)
        await mobile_handler.print_mobiles_in_room(context.character)

        context.finish()

    async def move_player(self, character: Character, direction: str):
        room = self.room_registry.get_or_none(id=character.room_id)
        destination_id = room.destination_id_for_direction(direction) if room is not None and hasattr(room, "destination_id_for_direction") else AreaUtil.is_valid_direction(direction, room)
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
        if room.can_see_room_vnum(character):
            lines = [f"Obvious exits from room {room.vnum}:"]
        else:
            lines = [f"Obvious exits:"]
        exits: List[Exit] = room.exits
        for direction in exits:
            destination = direction.to_room_id
            if destination is None:
                continue
            destination_room: Room = self.room_registry.get(id=destination)
            if destination_room.can_see_room_vnum(character):
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
        character: Character = self.character_registry.get(id=character_id)
        show_description = True
        if character is not None:
            comm_flags = CharacterApi.get_enum("commFlags")
            if CharacterApi.is_set(character.status_flags.comm, comm_flags.COMM_BRIEF.value):
                show_description = False

        if show_description:
            message = self.message_bus.text_to_message(room.format_room_description())
            await self.message_bus.send_to_character(character_id, message)
        else:
            await self.message_bus.send_to_character(character_id, self.message_bus.text_to_message(f"[{room.name}]\r\n"))
        lines = ItemUtil.room_items(room)
        if lines:
            await self.message_bus.send_to_character(character_id, self.message_bus.text_to_message("\r\n".join(lines) + "\r\n"))

    async def look_direction(self, character: Character, context: Context):
        arg1 = (context.parameters[0] if context.parameters and len(context.parameters) > 0 else "").strip()
        room = context.room if context.room is not None else self.room_registry.get(id=character.room_id)
        door = room.direction_index(arg1)
        pexit = room.get_exit(door) if hasattr(room, "get_exit") else AreaUtil.get_exit_by_direction(room, door)
        desc = (pexit.description or "").strip()

        if desc:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(desc + "\r\n"))
            context.finish()
            return

        keyword = (pexit.keyword or "").strip()
        if keyword and not keyword.startswith(" "):
            flags = int(getattr(pexit, "exit_flags", 0) or 0)
            if flags & 2:  # CLOSED
                await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(f"The {keyword} is closed.\r\n"))
            elif flags & 1:  # IS_DOOR
                await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(f"The {keyword} is open.\r\n"))
        context.finish()
