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

    async def do_title(self, character: Character, context: Context):
        text = self.info_commands.do_title(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_description(self, character: Character, context: Context):
        text = self.info_commands.do_description(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_report(self, character: Character, context: Context):
        payload = self.info_commands.do_report(character)
        await self.message_bus.send_to_character(
            character.id,
            self.message_bus.text_to_message(payload["to_char"])
        )
        if len(payload["in_room"]) > 0:
            await self.message_bus.send_to_room(
                self.message_bus.text_to_message(payload["to_room"]),
                payload["in_room"]
            )

    async def do_autolist(self, character: Character, context: Context):
        text = self.info_commands.do_autolist(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_autoassist(self, character: Character, context: Context):
        text = self.info_commands.do_autoassist(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_autoexit(self, character: Character, context: Context):
        text = self.info_commands.do_autoexit(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_autogold(self, character: Character, context: Context):
        text = self.info_commands.do_autogold(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_autoloot(self, character: Character, context: Context):
        text = self.info_commands.do_autoloot(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_autosac(self, character: Character, context: Context):
        text = self.info_commands.do_autosac(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_autosplit(self, character: Character, context: Context):
        text = self.info_commands.do_autosplit(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_worth(self, character: Character, context: Context):
        text = self.info_commands.do_worth(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_affects(self, character: Character, context: Context):
        text = self.info_commands.do_affects(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_brief(self, character: Character, context: Context):
        text = self.info_commands.do_brief(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_compact(self, character: Character, context: Context):
        text = self.info_commands.do_compact(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_combine(self, character: Character, context: Context):
        text = self.info_commands.do_combine(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_noloot(self, character: Character, context: Context):
        text = self.info_commands.do_noloot(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_nofollow(self, character: Character, context: Context):
        text = self.info_commands.do_nofollow(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_nosummon(self, character: Character, context: Context):
        text = self.info_commands.do_nosummon(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_read(self, character: Character, context: Context):
        payload = self.info_commands.do_read(character, context)
        if payload.get("look"):
            text = await self.info_commands.do_look(character, context)
            if text:
                await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))
            if not context.done:
                await context.room_handler().print_in_room(context)
            return

        if payload.get("error"):
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(payload["error"]))
            return

        context.parameters = [payload["argument"]]
        await context.item_handler().look_item_or_extra(character, context)
        if not context.done:
            context.finish()
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("You do not see that here.\r\n"))

    async def do_examine(self, character: Character, context: Context):
        payload = self.info_commands.do_examine(character, context)
        if payload.get("error"):
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(payload["error"]))
            return

        context.parameters = [payload["argument"]]
        await context.item_handler().look_item_or_extra(character, context)
        if not context.done:
            context.finish()
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("You do not see that here.\r\n"))
            return

        if payload.get("look_in"):
            context.done = False
            context.parameters = ["in", payload["argument"]]
            await context.item_handler().look_in_item(character, context)

    async def do_whois(self, character: Character, context: Context):
        text = self.info_commands.do_whois(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_count(self, character: Character, context: Context):
        text = self.info_commands.do_count(context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_show(self, character: Character, context: Context):
        text = self.info_commands.do_show(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_practice(self, character: Character, context: Context):
        text = self.info_commands.do_practice(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_prompt(self, character: Character, context: Context):
        text = self.info_commands.do_prompt(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_equipment(self, character: Character, context: Context):
        text = self.info_commands.do_equipment(character, context)
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def do_compare(self, character: Character, context: Context):
        text = self.info_commands.do_compare(character, context)
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
