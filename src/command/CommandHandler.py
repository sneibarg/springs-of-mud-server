import re

from typing import Union, Any
from command.CommandService import CommandService
from server.LoggerFactory import LoggerFactory


class CommandHandler:
    def __init__(self, injector):
        self.__name__ = "CommandHandler"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.injector = injector
        self.command_list = self.injector.get(CommandService).command_list
        self.logger.info("Initialized CommandHandler instance.")

    def handle_command(self, player, command):
        usage = None
        cmd, parameters = self.extract_parameters(command)
        if cmd is None:
            player.writer().write(b'Huh?\r\n')
            return

        if cmd is not None and "usage" in cmd:
            usage = cmd['usage']

        self.logger.info("CMD: "+cmd['name'] + ", PARAMETERS: "+parameters)
        self.logger.info("USAGE: "+str(usage))
        if usage is not None:
            usage_function = eval(usage)
            if not callable(usage_function):
                self.logger.info("NOT_CALLABLE: "+str(usage_function))
            else:
                player.set_usage(usage_function)

        return self.injector.get(CommandService).call_lambda(player, cmd['name'], self.command_list, parameters)

    def extract_parameters(self, command: str) -> Union[tuple[Any, str], tuple[None, None]]:
        for cmd in self.command_list:
            json = self.command_list[cmd]
            if command in json['shortcuts'] or command.startswith(json['name']):
                return json, ' '.join(re.split(' ', command)[1:]).strip()
        return None, None
