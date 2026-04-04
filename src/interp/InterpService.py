import json
from pathlib import Path
from typing import Any, Optional

import requests

from injector import inject
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
        self.help_keyword_list = [help_entry.keyword.lower() for help_entry in self.help_registry.all_helps()]
        self.load_commands()

    def reload_commands(self) -> None:
        self.logger.info("Reloading all commands...")
        self.social_registry.reset()
        self.load_socials()
        self.logger.info("Commands reload completed.")

    def load_commands(self):
        self.interp_registry.reset()
        self._fetch_and_register(self.commands_endpoint, "all commands")
        self.interp_registry.register(self._build_summary_command())

    def load_command(self, command_name: str):
        url = f"{self.commands_endpoint}/name/{command_name}"
        return self._fetch_and_register(url, f"command '{command_name}'")

    def _fetch_and_register(self, url: str, description: str) -> int:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        try:
            if isinstance(data, list):
                count = 0
                for command_data in data:
                    command = Command.from_json(command_data)
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

    def _assign_help_to_command(self, command: Command) -> None:
        for help_entry in self.help_registry.all_helps():
            if command.name.lower() in self.help_keyword_list:
                command.help = self.help_registry.get(keyword=command.name.lower())
                continue
            if command.name.lower() in help_entry.keyword.lower():
                command.help= help_entry

    def _build_summary_command(self) -> Command:
        from server.ServerUtil import ServerUtil
        summary_id = ServerUtil.generate_mongo_id()
        summary_cmd = Command(_id=summary_id, id=summary_id, name='summary', shortcuts="", message="", skill_id="", position="", usage="", role="", enabled=True, lambdas=[], function=[], help=self.help_registry.get(keyword='summary'))
        return summary_cmd
