from typing import Any
from injector import inject

from area.RoomHelper import RoomHelper
from game.RegistryService import RegistryService
from interp.CommandHelper import CommandHelper
from interp.Context import Context
from player.Character import Character
from player.CharacterMacros import CharacterMacros
from player.PlayerUtil import PlayerUtil
from server.messaging import MessageBus
from server.session.SessionHandler import SessionHandler
from server.LoggerFactory import LoggerFactory


class PlayerHandler:
    @inject
    def __init__(self, message_bus: MessageBus,
                 registry_service: RegistryService,
                 session_handler: SessionHandler,
                 command_helper: CommandHelper,
                 room_helper: RoomHelper,
                 character_macros: CharacterMacros):
        self.__name__ = "PlayerHandler"
        self.message_bus = message_bus
        self.character_registry = registry_service.character_registry
        self.room_registry = registry_service.room_registry
        self.session_handler = session_handler
        self.command_helper = command_helper
        self.room_helper = room_helper
        self.character_macros = character_macros
        self.PlayerActBits = character_macros.enums.get('playerActBits')
        self.logger = LoggerFactory.get_logger(__name__)

    async def print_visible(self, character):
        who_list = [character] + PlayerUtil.visible(character, self.session_handler)
        who_line = ""
        players_found = "Players found: " + str(len(who_list)) + "\r\n"
        for c in who_list:
            who_line = who_line + f"[{c.level}    {c.race}    {c.character_class.name}] {c.name} {c.title}\r\n"

        who_line = who_line + players_found
        message = self.message_bus.text_to_message(who_line)
        await self.message_bus.send_to_character(character.id, message)

    async def to_player(self, character_id, text):
        text += "\r\n"
        message = self.message_bus.text_to_message(text)
        await self.message_bus.send_to_character(character_id, message)

    async def look_target(self, character: Any, context: Context):
        room = self.room_registry.get(id=character.room_id)
        if room is None:
            return

        arg1 = context.parameters[0] if len(context.parameters) > 0 else ""
        target = PlayerUtil.get_target(character, arg1, room, self.room_helper)
        if target is None:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("You do not see them here.\r\n"))
            return

        header = target.name or "Someone"
        desc = (target.description or "").strip() or "You see nothing special."
        text = f"{header}\r\n{desc}\r\n"
        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_look(self, character: Character, context: Context):
        if not self.command_helper.check_position(character):
            return

        if self.room_helper.check_blind(character):
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("You can't see a thing!\n\r"))
            return

        if (not self.character_macros.is_npc(character)
                and not self.character_macros.has_holy_light(character)
                and self.room_helper.is_room_dark(character.room_id)):
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("It is pitch black ...\n\r"))
            await context.room_handler().print_in_room(character.id, context.mobile_handler())
            return

        arg1 = context.parameters[0]
        arg2 = context.parameters[1]
        if arg1 == "" or not arg1 == "auto":
            context.jump_to(context.next_index + 1)
        if arg1 == "i" or arg1 == "in" or arg1 == "on":
            context.jump_to(context.next_index + 2)
        if PlayerUtil.is_target_playing(arg2, self.session_handler):
            context.jump_to(context.next_index + 3)
