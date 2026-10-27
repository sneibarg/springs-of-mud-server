from typing import Optional
from injector import inject
from mobile.Mobile import Mobile
from mobile.MobileFactory import MobileFactory
from server.FetchAndRegisterMixin import FetchAndRegisterMixin
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig
from combat.CombatHandler import FightHandler
from game.GameData import GameData
from area.AreaRegistry import AreaRegistry
from mobile.MobileRegistry import MobileRegistry
from area.SpecialRegistry import SpecialRegistry


class MobileService(FetchAndRegisterMixin):
    @inject
    def __init__(self, config: ServiceConfig, area_registry: AreaRegistry, mobile_registry: MobileRegistry, fight_handler: FightHandler, game_data: GameData, special_registry: SpecialRegistry):
        self.__name__ = "MobileService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.mobile_registry = mobile_registry
        self.special_registry = special_registry
        self.game_data = game_data
        self.enums = self.game_data.enums
        self.mobiles_endpoint = config.mobiles_endpoint
        self.area_registry = area_registry
        self.fight_handler = fight_handler
        self.load_mobiles()

    def reload_mobiles(self) -> bool:
        return self._reload_collection(self.mobiles_endpoint, "mobiles", self.mobile_registry)

    def load_mobiles(self):
        self._fetch_and_register(self.mobiles_endpoint, "all mobiles")

    def load_mobile(self, mobile_name: str):
        url = f"{self.mobiles_endpoint}/name/{mobile_name}"
        return self._fetch_and_register(url, f"mobile '{mobile_name}'")

    def _build_fetch_item(self, raw_mobile) -> Optional[Mobile]:
        mobile = MobileFactory.from_data(raw_mobile, self.game_data.races)
        if mobile is None:
            self.logger.error(f"Failed to build mobile for {raw_mobile}")
        else:
            special = self.special_registry.for_mobile(mobile.area_id, mobile.vnum)
            if special is not None:
                mobile.special_name = special.name
                mobile.special_function = list(special.special_function)
        return mobile

    def _register_fetch_item(self, mobile: Mobile) -> None:
        self.mobile_registry.register(mobile)
