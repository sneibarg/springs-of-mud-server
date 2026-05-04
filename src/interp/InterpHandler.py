import inspect

from typing import List
from injector import inject, Injector

from game.HandlerService import HandlerService
from game.RegistryService import RegistryService
from interp.Command import Command
from interp.Context import Context
from util.InterpUtil import InterpUtil
from player.Character import Character
from server.LoggerFactory import LoggerFactory
from server.connection.ConnectionManager import ConnectionManager
from server.messaging import MessageBus


class InterpHandler:
    @inject
    def __init__(self, injector: Injector, message_bus: MessageBus, registry_service: RegistryService, handler_service: HandlerService):
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

    @staticmethod
    async def _execute_lambda(func, context) -> Context:
        result = func(context)
        if inspect.isawaitable(result):
            context.result = await result
        else:
            context.result = result
        return context

    async def _handle_pipeline(self, command: Command, context: Context):
        i = 0
        while i < len(command.lambdas):
            lambda_str = command.lambdas[i]
            if not isinstance(lambda_str, str):
                i += 1
                continue

            try:
                func = eval(lambda_str)
                if not callable(func):
                    i += 1
                    continue

                context = await self._execute_lambda(func, context)
                if context.done:
                    break

                if isinstance(context.next_index, int) and context.next_index >= 0:
                    i = context.next_index
                    context.next_index = None
                    continue
            except Exception as e:
                self.logger.error(f"Pipeline lambda failed at index {i}: {lambda_str} | {e}")
                raise
            i += 1

    async def _handle_sequence(self, command: Command, context: Context):
        for lambda_string in command.lambdas:
            func = eval(lambda_string)
            if not callable(func):
                continue
            await self._execute_lambda(func, context)

    async def _handle_lambdas(self, character: Character, command: Command, parameters: str):
        lambdas = getattr(command, "lambdas", None) or []
        has_executable_lambda = any(isinstance(value, str) and value.strip() for value in lambdas)
        if not has_executable_lambda:
            await self.message_bus.send_to_character(character.id, self.command_not_found_message)
            return None

        arguments = InterpUtil.build_arguments(command, parameters)
        connection = self.connection_manager.get_connection_by_character(character.id)
        room = self.room_registry.get_or_none(id=character.room_id)
        context = Context(character=character, handler_service=self.handler_service, conn=connection, command=command, parameters=arguments, result=parameters, room=room)
        if len(arguments) < command.max_arguments and command.usage != "":
            await self.handle_usage(command, context)
            return None

        if command.pipeline:
            await self._handle_pipeline(command, context)
        else:
            await self._handle_sequence(command, context)

        return context.result

    async def _call_lambda(self, character: Character, command_name: str, command_list: List[Command], parameters: str):
        command = self.interp_registry.get_or_none(name=command_name)
        if command is None:
            command_json = InterpUtil.find_command_by_name(command_name, command_list)
            if command_json is None:
                return await self.message_bus.send_to_character(character.id, self.command_not_found_message)

        try:
            await self._handle_lambdas(character=character, command=command, parameters=parameters)
        except TypeError as te:
            self.logger.error("TypeError: " + str(te))
            raise

    async def handle_command(self, player, character, command):
        if command is None or not str(command).strip():
            return None

        cmd, parameters = InterpUtil.extract_parameters(self.registry_service.interp_registry, command)
        if cmd is None:
            social = self.social_registry.get_or_none(name=command.lower())
            if social is not None:
                return await self.social_handler.handle_social(character, command, social)
            await self.message_bus.send_to_character(character.id, self.command_not_found_message)
            return None

        self.logger.debug(f"CMD: {cmd.name}, PARAMETERS: {parameters}, USAGE: {str(player.usage)}")
        return await self._call_lambda(character, cmd.name, self.interp_registry.all_commands(), parameters)

    async def handle_usage(self, cmd: Command, context: Context):
        usage = getattr(cmd, "usage", None)
        if isinstance(usage, str) and cmd.usage.strip():
            usage_function = eval(cmd.usage)
            if not callable(usage_function):
                self.logger.error("NOT_CALLABLE: " + str(usage_function))
                return None
            if not inspect.iscoroutinefunction(usage_function):
                self.logger.error("NOT_ASYNC: " + str(usage_function))
            await usage_function(context)
        return None
