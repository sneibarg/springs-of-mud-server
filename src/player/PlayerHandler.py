from typing import Any
from injector import inject

from area.RoomHelper import RoomHelper
from game.RegistryService import RegistryService
from interp.CommandHelper import CommandHelper
from interp.Context import Context
from player.Character import Character
from player.CharacterMacros import CharacterMacros
from player.PlayerUtil import PlayerUtil
from player.PlayerHelper import PlayerHelper
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
                 player_helper: PlayerHelper,
                 character_macros: CharacterMacros):
        self.__name__ = "PlayerHandler"
        self.message_bus = message_bus
        self.character_registry = registry_service.character_registry
        self.room_registry = registry_service.room_registry
        self.session_handler = session_handler
        self.command_helper = command_helper
        self.room_helper = room_helper
        self.player_helper = player_helper
        self.character_macros = character_macros
        self.PlayerActBits = character_macros.enums.get('playerActBits')
        self.logger = LoggerFactory.get_logger(__name__)

    async def do_quit(self, character: Character, context: Context):
        room = self.room_registry.get(id=character.room_id)
        in_room = self.player_helper.players_in_room(character, room)
        message = self.message_bus.text_to_message(f"{character.name} has left the game.\r\n")
        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(f"Alas, all good things must come to an end.\r\n"))
        if len(in_room) > 0:
            await self.message_bus.send_to_room(message, in_room)
        self.session_handler.remove_session(character.id)
        await context.disconnect()

    async def print_players_in_room(self, character: Character):
        message = self.player_helper.get_players_in_room(character)
        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(message))

    async def do_who(self, character):
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

        arg1 = (context.parameters[0] if context.parameters and len(context.parameters) > 0 else "").strip().lower()
        if arg1 in ("", "auto", "i", "in", "on"):
            return

        target = PlayerUtil.get_target(character, arg1, room, self.character_macros, self.room_helper)
        if target is None:
            context.jump_to(4)
            return

        header = target.name or "Someone"
        desc = (target.description or "").strip() or "You see nothing special."
        text = f"{header}\r\n{desc}\r\n"
        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))
        context.finish()

    async def do_look(self, character: Character, context: Context):
        direction_map = {"n": 0, "north": 0, "e": 1, "east": 1, "s": 2, "south": 2, "w": 3, "west": 3, "u": 4, "up": 4, "d": 5, "down": 5}
        if not self.command_helper.check_position(character):
            context.finish()
            return

        if not self.room_helper.check_blind(character):
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("You can't see a thing!\n\r"))
            context.finish()
            return

        arg1 = (context.parameters[0] if context.parameters and len(context.parameters) > 0 else "").strip().lower()
        if (not self.character_macros.is_npc(character)
                and not self.character_macros.has_holy_light(character)
                and self.room_helper.is_room_dark(character.room_id)):
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("It is pitch black ...\n\r"))
            context.jump_to(1)  # show chars/mobs only
            return

        room = self.room_registry.get(id=character.room_id)
        if room is None:
            context.finish()
            return

        print(f"arg1 is {arg1}")
        if arg1 == "" or arg1 == "auto":
            await context.room_handler().print_room(character.id, room)
            if self.character_macros.is_set(int(self.character_macros.convert_flags(character.character_flags.act)), self.PlayerActBits.PLR_AUTOEXIT.value):
                await context.room_handler().print_exits(character, room)

            await context.item_handler().look_room_items(character)
            context.jump_to(1)  # players + mobiles
            return

        if arg1 in ("i", "in", "on"):
            context.jump_to(2)
            return

        if arg1 in direction_map:
            print(f"Looking in direction {arg1}")
            context.jump_to(5)

        context.jump_to(3)
