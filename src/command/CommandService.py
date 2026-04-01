import requests

from injector import inject
from registry.CommandRegistry import CommandRegistry
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class CommandService:
    @inject
    def __init__(self, config: ServiceConfig, command_registry: CommandRegistry):
        self.__name__ = "CommandService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.command_registry = command_registry
        self.commands_endpoint = config.commands_endpoint
        self.load_command_list()
        self.logger.info(f"Initialized CommandService instance with a total of {len(self.command_registry.registry.values())} commands.")

    def load_command_list(self):
        response = requests.get(self.commands_endpoint)
        if response.status_code == 200:
            commands = response.json()
            for command in commands:
                self.command_registry.register_command(command)
            return
        raise ValueError('Failed to retrieve commands from MongoDB')

    def load_command_by_id(self, command_id):
        url = self.commands_endpoint + "/" + command_id
        command = requests.get(url).json()
        self.command_registry.register_command(command)

    def load_command_by_name(self, command_name):
        url = self.commands_endpoint + "/name/" + command_name
        if url:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    command = response.json()
                    if command:
                        self.command_registry.register_command(command)
            except Exception as e:
                self.logger.error(f"Failed to fetch command '{command_name}': {e}")
        return None

