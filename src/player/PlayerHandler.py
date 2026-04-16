from typing import Any
from injector import inject

from game.RegistryService import RegistryService
from interp.Context import Context
from interp.commands.InfoCommands import InfoCommands
from player.Character import Character
from player.PlayerHelper import PlayerHelper
from server.messaging import MessageBus
from server.LoggerFactory import LoggerFactory


class PlayerHandler:
    @inject
    def __init__(self, message_bus: MessageBus,
                 registry_service: RegistryService,
                 player_helper: PlayerHelper,
                 info_commands: InfoCommands):
        self.__name__ = "PlayerHandler"
        self.message_bus = message_bus
        self.character_registry = registry_service.character_registry
        self.room_registry = registry_service.room_registry
        self.player_helper = player_helper
        self.info_commands = info_commands
        self.logger = LoggerFactory.get_logger(__name__)

    async def do_quit(self, character: Character, context: Context):
        payload = self.info_commands.do_quit(character)
        await self.message_bus.send_to_character(
            character.id,
            self.message_bus.text_to_message(payload["to_char"])
        )
        if len(payload["in_room"]) > 0:
            await self.message_bus.send_to_room(
                self.message_bus.text_to_message(payload["to_room"]),
                payload["in_room"]
            )
        await context.disconnect()

    async def do_who(self, character):
        await self.message_bus.send_to_character(
            character.id,
            self.message_bus.text_to_message(self.info_commands.do_who(character))
        )

    async def do_help(self, character: Character, context: Context):
        argument = context.result if isinstance(context.result, str) else " ".join(context.parameters or [])
        await self.message_bus.send_to_character(
            character.id,
            self.message_bus.text_to_message(self.info_commands.do_help(argument))
        )
        context.finish()

    async def do_look(self, character: Character, context: Context):
        text = await self.info_commands.do_look(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_scroll(self, character: Character, context: Context):
        text = self.info_commands.do_scroll(character, context)
        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_wimpy(self, character: Character, context: Context):
        text = self.info_commands.do_wimpy(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_score(self, character: Character, context: Context):
        text = self.info_commands.do_score(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_time(self, character: Character, context: Context):
        text = self.info_commands.do_time(context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_weather(self, character: Character, context: Context):
        text = self.info_commands.do_weather(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_where(self, character: Character, context: Context):
        text = self.info_commands.do_where(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_consider(self, character: Character, context: Context):
        text = self.info_commands.do_consider(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def print_players_in_room(self, character: Character):
        message = self.player_helper.get_players_in_room(character)
        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(message))

    async def to_player(self, character_id, msg: str):
        text = msg + "\r\n"
        message = self.message_bus.text_to_message(text)
        await self.message_bus.send_to_character(character_id, message)

    async def to_target(self, context: Context):
        target = self.character_registry.get_or_none(name=context.parameters[0])
        if target is None:
            await self.message_bus.send_to_character(context.character.id,
                                                     self.message_bus.text_to_message("They aren't here.\r\n"))
            return
        text = context.parameters[1] + "\r\n"
        message = self.message_bus.text_to_message(text)
        await self.message_bus.send_to_character(target.id, message)

    async def to_room(self, character: Character, msg: str):
        room = self.room_registry.get(id=character.room_id)
        text = msg.replace("%c", character.name).replace("%m", msg)
        message = self.message_bus.text_to_message(text)
        in_room = self.player_helper.players_in_room(character, room)
        await self.message_bus.send_to_room(message, in_room)

    async def look_target(self, character: Any, context: Context):
        text = self.info_commands.look_target(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))
