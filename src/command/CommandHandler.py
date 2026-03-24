import re
from injector import inject

from typing import Union, Any
from command.CommandService import CommandService
from server.LoggerFactory import LoggerFactory


class CommandHandler:
    @inject
    def __init__(self, command_service: CommandService):
        self.__name__ = "CommandHandler"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.command_service = command_service
        self.command_list = command_service.command_list
        self.logger.info("Initialized CommandHandler instance.")

    async def handle_command(self, player, command):
        usage = None
        cmd, parameters = self.extract_parameters(command)
        if cmd is None:
            player.writer().write(b'Huh?\r\n')
            return None

        if cmd is not None and "usage" in cmd:
            usage = cmd['usage']

        if usage is not None:
            usage_function = eval(usage)
            if not callable(usage_function):
                self.logger.info("NOT_CALLABLE: "+str(usage_function))
            else:
                player.set_usage(usage_function)

        self.logger.debug(f"CMD: {cmd['name']}, PARAMETERS: {parameters}, USAGE: {str(usage)}")
        return await self.command_service.call_lambda(player, cmd['name'], self.command_list, parameters)

    def extract_parameters(self, command: str) -> Union[tuple[Any, str], tuple[None, None]]:
        for cmd in self.command_list:
            json = self.command_list[cmd]
            shortcuts = json['shortcuts'].split(", ")
            if command in shortcuts or command.startswith(json['name']):
                return json, ' '.join(re.split(' ', command)[1:]).strip()
        return None, None
