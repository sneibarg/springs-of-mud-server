from typing import Any

import requests

from injector import inject

from game.GamePayload import GamePayload
from interp.Command import Command
from interp.InterpRegistry import InterpRegistry
from interp.HelpRegistry import HelpRegistry
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class InterpService:
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

    def reload_commands(self) -> None:
        self.logger.info("Reloading all commands...")
        self.interp_registry.reset()
        self.load_commands()
        self.logger.info("Commands reload completed.")

    def load_commands(self):
        self.interp_registry.reset()
        self._build_help_indexes()
        self._fetch_and_register(self.commands_endpoint, "all commands")
        self.interp_registry.register(self._build_summary_command())

    def load_command(self, command_name: str):
        url = f"{self.commands_endpoint}/name/{command_name}"
        return self._fetch_and_register(url, f"command '{command_name}'")

    def _fetch_and_register(self, url: str, description: str) -> int:
        from util.GenericUtil import GenericUtil
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        try:
            if isinstance(data, list):
                for command_data in data:
                    command = Command.from_json(command_data)
                    command.payload = GamePayload.from_json(GenericUtil.camel_to_snake_case(command_data.get("payload")))
                    self._assign_help_to_command(command)
                    self.interp_registry.register(command)
                self.logger.info(f"Loaded {len(self.interp_registry.all_commands())} {description}.")
                return None
            else:
                command = Command.from_json(data)
                self.interp_registry.register(command)
                self.logger.info(f"Loaded {description}.")
                return command
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {description} from {url}: {e}")
            return 0
        except Exception as e:
            self.logger.error(f"Unexpected error processing {description}: {e}", exc_info=True)
            return 0

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
        command.help = None
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
