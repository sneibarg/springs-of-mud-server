from injector import inject
from interp.HelpRegistry import HelpRegistry
from interp.HelpEntry import HelpEntry
from server.FetchAndRegisterMixin import FetchAndRegisterMixin
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class HelpService(FetchAndRegisterMixin):
    @inject
    def __init__(self, config: ServiceConfig, help_registry: HelpRegistry):
        self.__name__ = "HelpService"
        self.helps_endpoint = config.helps_endpoint
        self.help_registry = help_registry
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.load_helps()

    def reload_helps(self) -> bool:
        return self._reload_collection(self.helps_endpoint, "helps", self.help_registry)

    def load_helps(self):
        self._fetch_and_register(self.helps_endpoint, "helps")

    def _build_fetch_item(self, help_data) -> HelpEntry:
        return HelpEntry.from_json(help_data)

    def _register_fetch_item(self, help_entry: HelpEntry) -> None:
        self.help_registry.register(help_entry)
