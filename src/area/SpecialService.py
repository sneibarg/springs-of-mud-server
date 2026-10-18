from injector import inject
from area.Special import Special
from area.SpecialRegistry import SpecialRegistry
from server.FetchAndRegisterMixin import FetchAndRegisterMixin
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class SpecialService(FetchAndRegisterMixin):
    log_fetch_list_count = False

    @inject
    def __init__(self, config: ServiceConfig, special_registry: SpecialRegistry):
        self.__name__ = "SpecialService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.specials_endpoint = config.specials_endpoint
        self.special_registry = special_registry
        self.load_specials()

    def reload_specials(self):
        self.logger.info("Reloading specials...")
        self.special_registry.reset()
        self.load_specials()
        self.logger.info("Specials reload completed.")

    def load_specials(self):
        self._fetch_and_register(self.specials_endpoint, "specials")
        self.logger.info(f"Loaded {len(self.special_registry.all_specials())} specials.")

    def load_special(self, special_name: str):
        url = f"{self.specials_endpoint}/name/{special_name}"
        return self._fetch_and_register(url, f"special '{special_name}'")

    def _build_fetch_item(self, special_data) -> Special:
        return Special.from_json(special_data)

    def _register_fetch_item(self, special: Special) -> None:
        self.special_registry.register(special)
