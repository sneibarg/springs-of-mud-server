from injector import inject

from game.GamePayload import GamePayload
from interp.Command import Command
from interp.InterpRegistry import InterpRegistry
from interp.HelpRegistry import HelpRegistry
from server.FetchAndRegisterMixin import FetchAndRegisterMixin
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig
from util.GenericUtil import GenericUtil


class InterpService(FetchAndRegisterMixin):
    fetch_error_return = 0

    @inject
    def __init__(self, config: ServiceConfig, interp_registry: InterpRegistry, help_registry: HelpRegistry):
        self.__name__ = "InterpService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.commands_endpoint = config.commands_endpoint
        self.interp_registry = interp_registry
        self.help_registry = help_registry
        self.load_commands()

    def reload_commands(self) -> bool:
        return self._reload_collection(self.commands_endpoint, "commands", self.interp_registry)

    def _reload_extra_items(self):
        return (self._build_summary_command(),)

    def load_commands(self):
        return self.reload_commands()

    def load_command(self, command_name: str):
        url = f"{self.commands_endpoint}/name/{command_name}"
        return self._fetch_and_register(url, f"command '{command_name}'")

    def _build_fetch_item(self, command_data) -> Command:
        command = Command.from_json(command_data)
        command.payload = GamePayload.from_json(GenericUtil.camel_to_snake_case(command_data.get("payload")))
        self._assign_help_to_command(command)
        return command

    def _register_fetch_item(self, command: Command) -> None:
        self.interp_registry.register(command)

    def _assign_help_to_command(self, command: Command) -> None:
        if command.help is not None:
            return
        command_name = str(getattr(command, "name", "") or "").strip().lower()
        if not command_name:
            return
        command.help = self.help_registry.find_topic(command_name)

    def _build_summary_command(self) -> Command:
        from util.GenericUtil import GenericUtil
        summary_id = GenericUtil.generate_mongo_id()
        summary_cmd = Command(_id=summary_id, id=summary_id, max_arguments=0, level=0, name='summary', shortcuts="", message="", skill_id="", position="", usage="", role="", enabled=True, lambdas=[], function=[], help=self.help_registry.get(keyword='summary'))
        return summary_cmd
