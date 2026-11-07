from game.EnumProvider import EnumProvider
from injector import inject

from area.Room import Room
from area.Exit import Exit
from game.RegistryService import RegistryService
from interp.Context import Context
from player.Character import Character
from api.CharacterApi import CharacterApi
from server.LoggerFactory import LoggerFactory
from server.messaging import MessageBus
from server.session.SessionHandler import SessionHandler
from interp.CommandDefaults import bundled_payload, render_command_message


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

        if CharacterApi.room_view_block_reason(context.character, context.room) in ("", "dark"):
            await player_handler.print_players_in_room(context.character)
            await mobile_handler.print_mobiles_in_room(context.character)

        context.finish()

    async def move_player(self, character: Character, direction: str):
        room = self.room_registry.get_or_none(id=character.room_id)
        destination_id = room.destination_id_for_direction(direction) if room is not None else None
        destination_room = self.room_registry.get_or_none(id=destination_id)
        if room is not None and destination_room is not None:
            character.room_id = str(destination_id)
            room.remove_player_from_room(character)
            destination_room.add_player_to_room(character)
            await self.print_room(character.id, destination_room)
        else:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(f"You can't go that direction!\r\n"))

    async def print_exits(self, character: Character, *, automatic=False):
        room = self.room_registry.get(id=character.room_id)
        if room is None:
            return
        if CharacterApi.is_blind(character) and not CharacterApi.has_holy_light(character):
            command = self.registry_service.interp_registry.get_or_none(name="look")
            text = (render_command_message(command, "to_char", "blind") if command is not None
                    else bundled_payload("look").render("to_char", "blind"))
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))
            return
        if CharacterApi.is_immortal(character):
            lines = [f"Obvious exits from room {room.vnum}:"]
        else:
            lines = [f"Obvious exits:"]
        closed = EnumProvider.value(CharacterApi.get_enum("exitFlags"), "CLOSED", "EX_CLOSED")
        for direction in room.exits:
            if direction.to_room_id is None or CharacterApi.is_set(direction.exit_flags, closed):
                continue
            destination = self.room_registry.get_or_none(id=direction.to_room_id)
            if destination is None or not CharacterApi.can_see_room(character, destination):
                continue
            if automatic:
                lines.append(direction.direction_label(direction.direction).lower())
                continue
            name = "Too dark to tell" if destination.is_room_dark() else destination.name
            vnum = destination.vnum if CharacterApi.is_immortal(character) else None
            lines.append(direction.format_destination(name, vnum, width=6))
        if automatic:
            text = "[Exits: " + (" ".join(lines[1:]) or "none") + "]\r\n"
        else:
            if len(lines) == 1:
                lines.append("None.")
            text = "\n".join(lines) + "\n"
        message = self.message_bus.text_to_message(text)
        await self.message_bus.send_to_character(character.id, message)

    async def print_room(self, character_id, room: Room, *, automatic=True):
        if room is None:
            self.logger.error(f"Attempted to print room to character {character_id} but room is None")
            return None
        character: Character = self.character_registry.get(id=character_id)
        if character is None:
            return False
        blocked = CharacterApi.room_view_block_reason(character, room)
        if blocked:
            command = self.registry_service.interp_registry.get_or_none(name="look")
            text = (render_command_message(command, "to_char", blocked) if command is not None
                    else bundled_payload("look").render("to_char", blocked))
            await self.message_bus.send_to_character(character_id, self.message_bus.text_to_message(text))
            return False
        show_description = True
        if automatic:
            comm_flags = CharacterApi.get_enum("commFlags")
            if CharacterApi.is_set(character.status_flags.comm, comm_flags.COMM_BRIEF.value):
                show_description = False

        if show_description:
            message = self.message_bus.text_to_message(room.format_room_description())
            await self.message_bus.send_to_character(character_id, message)
        else:
            await self.message_bus.send_to_character(character_id, self.message_bus.text_to_message(f"[{room.name}]\r\n"))
        lines = Room.item_description_lines(room, character)
        if lines:
            await self.message_bus.send_to_character(character_id, self.message_bus.text_to_message("\r\n".join(lines) + "\r\n"))
        return True

    async def look_direction(self, character: Character, context: Context):
        arg1 = (context.parameters[0] if context.parameters and len(context.parameters) > 0 else "").strip()
        room = context.room if context.room is not None else self.room_registry.get(id=character.room_id)
        door = room.direction_index(arg1)
        pexit = room.get_exit(door)
        if pexit is None:
            context.finish()
            return
        command = context.command
        desc = (pexit.description or "").strip() or render_command_message(command, "to_char", "invalid_direction")
        lines = [desc]
        keyword = pexit.keyword or ""
        if keyword and not keyword.startswith(" "):
            exit_flags = CharacterApi.get_enum("exitFlags")
            flags = pexit.exit_flags
            if flags & EnumProvider.value(exit_flags, "EX_CLOSED"):
                lines.append(render_command_message(command, "to_char", "closed", t=Exit.door_name(keyword)))
            elif flags & EnumProvider.value(exit_flags, "EX_ISDOOR"):
                lines.append(render_command_message(command, "to_char", "open", t=Exit.door_name(keyword)))
        text = "".join(line.rstrip("\r\n") + "\r\n" for line in lines if line)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))
        context.finish()
