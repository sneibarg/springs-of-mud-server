import inspect

from typing import List
from injector import inject, Injector
from game.HandlerService import HandlerService
from game.RegistryService import RegistryService
from interp.Command import Command
from interp.Context import Context
from interp.HelpEntry import HelpEntry
from interp.InterpUtil import InterpUtil
from player.Character import Character
from player.Player import Player
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
        self.interp_registry = registry_service.interp_registry
        self.social_registry = registry_service.social_registry
        self.handler_service = handler_service
        self.social_handler = self.handler_service.social_handler
        self.connection_manager = injector.get(ConnectionManager)
        self.command_not_found_message = self.message_bus.text_to_message("Huh?\r\n")

    def get_message(self, cmd):
        command = self.interp_registry.get_or_none(name=cmd.lower())
        if command is None or command.message is None:
            self.logger.error(f"Issue with command {cmd} in registry; message is {command.message if command else 'None'}")
            return None
        return command.message

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

                if context.next_index is not None:
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

    async def _handle_lambdas(self, player: Player, character: Character, command: Command, parameters: str):
        if not command.lambdas:
            return None

        arguments = InterpUtil.build_arguments(command, parameters)
        context = Context(player=player, character=character, handler_service=self.handler_service, parameters=arguments, result=parameters)

        if command.pipeline:
            await self._handle_pipeline(command, context)
        else:
            await self._handle_sequence(command, context)

        return context.result

    async def _call_lambda(self, player: Player, character: Character, command_name: str, command_list: List[Command], parameters: str):
        command = self.interp_registry.get_or_none(name=command_name)
        if command is None:
            command_json = InterpUtil.find_command_by_name(command_name, command_list)
            if command_json is None:
                return await self.message_bus.send_to_character(character.id, self.command_not_found_message)

        try:
            await self._handle_lambdas(self, player=player, character=character, command=command, parameters=parameters)
        except ValueError as ve:
            self.logger.error("ValueError: " + str(ve))
            raise
        except TypeError as te:
            self.logger.error("TypeError: " + str(te))
            raise

    async def handle_command(self, player, character, command):
        cmd, parameters = InterpUtil.extract_parameters(self.interp_registry, command)
        if cmd is None:
            social = self.social_registry.get_or_none(name=command.lower())
            if social is not None:
                return await self.social_handler.handle_social(character, command, social)
            await self.message_bus.send_to_character(character.id, self.command_not_found_message)
            return None

        player.usage = self.handle_usage(command)
        self.logger.info(f"CMD: {cmd.name}, PARAMETERS: {parameters}, USAGE: {str(player.usage)}")
        return await self._call_lambda(player, character, cmd.name, self.interp_registry.all_commands(), parameters)

    def handle_usage(self, cmd: Command):
        usage = cmd.usage
        if isinstance(usage, str) and usage.strip():
            usage_function = eval(usage)
            if not callable(usage_function):
                self.logger.error("NOT_CALLABLE: " + str(usage_function))
                return None
        return usage

    async def help_usage(self, character, argument: str = ""):
        arg_all = " ".join((argument or "").split()).lower()
        if not arg_all:
            arg_all = "summary"
        output_parts = []
        found = False
        for command in self.interp_registry.all_commands():
            help_entry: HelpEntry = command.help
            if help_entry is None or not help_entry.keyword:
                continue

            q_words = arg_all.split()
            k_words = help_entry.keyword.split()
            if (not q_words or not k_words) or not all(any(k.startswith(q) for k in k_words) for q in q_words):
                continue

            level_raw = getattr(help_entry, "level", 0)
            try:
                level = int(level_raw)
            except (TypeError, ValueError):
                level = 0

            if found:
                output_parts.append("\n\r============================================================\n\r\n\r")
            found = True

            if level >= 0 and arg_all != "imotd":
                output_parts.append(str(getattr(help_entry, "keyword", "")))
                output_parts.append("\n\r")

            text = str(getattr(help_entry, "text", "") or "")
            if text.startswith("."):
                text = text[1:]
            output_parts.append(text)

        message_text = "".join(output_parts) if len(output_parts) > 0 else "No help on that word.\n\r"
        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(message_text))
