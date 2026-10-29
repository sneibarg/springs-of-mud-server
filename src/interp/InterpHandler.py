from typing import List
from injector import inject, Injector

from api.AliasApi import AliasApi
from game.HandlerService import HandlerService
from game.RegistryService import RegistryService
from interp.Command import Command
from interp.CommandAccess import CommandAccess
from interp.CommandExecutor import CommandExecutor
from interp.CommandAudit import CommandAudit
from interp.Context import Context
from util.InterpUtil import InterpUtil
from player.Character import Character
from server.LoggerFactory import LoggerFactory
from server.connection.ConnectionManager import ConnectionManager
from server.messaging import MessageBus


class InterpHandler:
    @inject
    def __init__(self, injector: Injector, message_bus: MessageBus, registry_service: RegistryService, handler_service: HandlerService,
                 command_audit: CommandAudit = None):
        self.__name__ = "InterpHandler"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.injector = injector
        self.message_bus = message_bus
        self.registry_service = registry_service
        self.handler_service = handler_service
        self.social_registry = registry_service.social_registry
        self.interp_registry = registry_service.interp_registry
        self.room_registry = registry_service.room_registry
        self.social_handler = self.handler_service.social_handler
        self.connection_manager = injector.get(ConnectionManager)
        self.command_not_found_message = self.message_bus.text_to_message("Huh?\r\n")
        self.command_audit = command_audit

    async def _handle_lambdas(self, character: Character, command: Command, parameters: str, raw_command=None):
        arguments = InterpUtil.build_arguments(command, parameters)
        connection = self.connection_manager.get_connection_by_character(character.id)
        room = self.room_registry.get_or_none(id=character.room_id)
        context = Context(character=character, handler_service=self.handler_service, conn=connection, command=command,
                          parameters=arguments, result=parameters, room=room, raw_command=raw_command)

        return await CommandExecutor.execute(command, context, authorization=CommandAccess.check,
                                             message_bus=self.message_bus, audit=getattr(self, 'command_audit', None))

    async def _call_lambda(self, character: Character, command_name: str, command_list: List[Command], parameters: str, raw_command=None):
        command = self.interp_registry.get_or_none(name=command_name)
        if command is None:
            command_json = InterpUtil.find_command_by_name(command_name, command_list)
            if command_json is None:
                return await self.message_bus.send_to_character(character.id, self.command_not_found_message)

        try:
            await self._handle_lambdas(character=character, command=command, parameters=parameters, raw_command=raw_command)
        except TypeError as te:
            self.logger.error("TypeError: " + str(te))
            raise

    async def _send_alias_substitution_message(self, character: Character, alias_result):
        text = str(getattr(alias_result, "message", "") or "")
        message_key = str(getattr(alias_result, "message_key", "") or "")
        if message_key:
            alias_command = self.interp_registry.get_or_none(name=getattr(alias_result, 'message_command', 'alias'))
            if alias_command is not None:
                rendered = alias_command.render_message("to_char", message_key, fallback=text)
                if rendered:
                    text = rendered if rendered.endswith("\r\n") else f"{rendered}\r\n"
        if text:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))

    async def handle_command(self, player, character, command):
        if not InterpUtil.begin_input(character, command):
            return None

        alias_result = AliasApi.substitute_command(character, command)
        if alias_result.message:
            await self._send_alias_substitution_message(character, alias_result)
        command = alias_result.command

        cmd, parameters = InterpUtil.extract_parameters(self.registry_service.interp_registry, command)
        if cmd is None:
            denial = CommandAccess.check_actor(character)
            if denial is not None:
                await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(denial.render(None)))
                return None
            if getattr(self, 'command_audit', None) is not None:
                await self.command_audit.record(character, None, command)
            social = self.social_registry.get_or_none(name=InterpUtil.one_argument(command)[0])
            if social is not None:
                return await self.social_handler.handle_social(character, command, social)
            await self.message_bus.send_to_character(character.id, self.command_not_found_message)
            return None

        self.logger.debug("CMD: %s", cmd.name)
        return await self._call_lambda(character, cmd.name, self.interp_registry.all_commands(), parameters, raw_command=command)
