from typing import Any

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
        self._help_exact_by_keyword: dict[str, Any] = {}
        self._help_token_index: dict[str, Any] = {}
        self._build_help_indexes()
        self.load_commands()

    def reload_commands(self) -> bool:
        self._build_help_indexes()
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

    def _build_help_indexes(self) -> None:
        self._help_exact_by_keyword = {}
        self._help_token_index = {}
        for help_entry in self.help_registry.all_helps():
            keyword = str(getattr(help_entry, "keyword", "") or "").strip().lower()
            if not keyword:
                continue
            self._help_exact_by_keyword[keyword] = help_entry
            for token in keyword.split():
                normalized = self._normalize_help_token(token)
                if normalized and normalized not in self._help_token_index:
                    self._help_token_index[normalized] = help_entry

    def _assign_help_to_command(self, command: Command) -> None:
        if command.help is not None:
            return
        command_name = str(getattr(command, "name", "") or "").strip().lower()
        if not command_name:
            return
        exact = self._help_exact_by_keyword.get(command_name)
        if exact is not None:
            command.help = exact
            return
        token_match = self._help_token_index.get(command_name)
        if token_match is not None:
            command.help = token_match

    @staticmethod
    def _normalize_help_token(value: str) -> str:
        token = str(value or "").strip().lower()
        token = token.strip("~`'\".,;:!?()[]{}<>")
        return token

    def _build_summary_command(self) -> Command:
        from util.GenericUtil import GenericUtil
        summary_id = GenericUtil.generate_mongo_id()
        summary_cmd = Command(_id=summary_id, id=summary_id, max_arguments=0, level=0, name='summary', shortcuts="", message="", skill_id="", position="", usage="", role="", enabled=True, lambdas=[], function=[], help=self.help_registry.get(keyword='summary'))
        return summary_cmd
