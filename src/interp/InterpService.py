import requests

from injector import inject
from interp.InterpRegistry import InterpRegistry
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class InterpService:
    @inject
    def __init__(self, config: ServiceConfig, interp_registry: InterpRegistry):
        self.__name__ = "CommandService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.interp_registry = interp_registry
        self.commands_endpoint = config.commands_endpoint
        self.helps_endpoint = config.helps_endpoint
        self.load_help_list()
        self.load_command_list()

    def load_help_list(self):
        response = requests.get(self.helps_endpoint)
        if response.status_code != 200:
            raise ValueError("Failed to retrieve help")
        help_json = response.json()
        for help_data in help_json:
            self.interp_registry.register_help(help_data)

    def load_command_list(self):
        response = requests.get(self.commands_endpoint)
        if response.status_code != 200:
            raise ValueError("Failed to retrieve commands")

        commands = response.json()
        for command in commands:
            self.interp_registry.register_command(command)
        self._assign_help_to_commands()

    def _assign_help_to_commands(self):
        for command in self.interp_registry.registry.values():
            if not command.get('help'):
                help_entry = self.interp_registry.get_help_by_keyword(command.get('name', ''))
                if help_entry:
                    command['help'] = help_entry
        summary_entry = self.interp_registry.get_help_by_keyword('summary')
        if summary_entry:
            self.interp_registry.registry['summary'] = {'name': 'summary', 'help': summary_entry}
