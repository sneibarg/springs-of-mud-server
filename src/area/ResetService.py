from injector import inject
from area.Reset import Reset
from area.ResetRegistry import ResetRegistry
from server.FetchAndRegisterMixin import FetchAndRegisterMixin
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class ResetService(FetchAndRegisterMixin):
    log_fetch_list_count = False

    @inject
    def __init__(self, config: ServiceConfig, reset_registry: ResetRegistry):
        self.__name__ = "ResetService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.resets_endpoint = config.resets_endpoint
        self.reset_registry = reset_registry
        self.load_resets()

    def reload_resets(self) -> bool:
        return self._reload_collection(self.resets_endpoint, "resets", self.reset_registry)

    def load_resets(self):
        self._fetch_and_register(self.resets_endpoint, "resets")
        self.logger.info(f"Loaded {len(self.reset_registry.all_resets())} resets.")

    def load_reset(self, reset_name: str):
        url = f"{self.resets_endpoint}/name/{reset_name}"
        return self._fetch_and_register(url, f"reset '{reset_name}'")

    def _build_fetch_item(self, reset_data) -> Reset:
        return Reset.from_json(reset_data)

    def _register_fetch_item(self, reset: Reset) -> None:
        self.reset_registry.register(reset)
