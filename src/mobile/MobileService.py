from typing import Optional
from injector import inject
from mobile.Mobile import Mobile
from util.MobileUtil import MobileUtil
from server.FetchAndRegisterMixin import FetchAndRegisterMixin
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig
from combat.CombatHandler import FightHandler
from game.GameData import GameData
from area.AreaRegistry import AreaRegistry
from mobile.MobileRegistry import MobileRegistry


class MobileService(FetchAndRegisterMixin):
    @inject
    def __init__(self, config: ServiceConfig, area_registry: AreaRegistry, mobile_registry: MobileRegistry, fight_handler: FightHandler, game_data: GameData):
        self.__name__ = "MobileService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.mobile_registry = mobile_registry
        self.game_data = game_data
        self.enums = self.game_data.enums
        self.mobiles_endpoint = config.mobiles_endpoint
        self.area_registry = area_registry
        self.fight_handler = fight_handler
        self.load_mobiles()

    def reload_mobiles(self) -> None:
        self.logger.info("Reloading all mobiles...")
        self.mobile_registry.reset()
        self.load_mobiles()
        self.logger.info("Mobiles reload completed.")

    def load_mobiles(self):
        self._fetch_and_register(self.mobiles_endpoint, "all mobiles")

    def load_mobile(self, mobile_name: str):
        url = f"{self.mobiles_endpoint}/name/{mobile_name}"
        return self._fetch_and_register(url, f"mobile '{mobile_name}'")

    def _build_fetch_item(self, raw_mobile) -> Optional[Mobile]:
        mobile = self._build_mobile(raw_mobile)
        if mobile is None:
            self.logger.error(f"Failed to build mobile for {raw_mobile}")
        return mobile

    def _register_fetch_item(self, mobile: Mobile) -> None:
        self.mobile_registry.register(mobile)

    def _build_mobile(self, raw_mobile) -> Optional[Mobile]:
        from util.GenericUtil import GenericUtil

        converted_mobile = GenericUtil.camel_to_snake_case(raw_mobile)
        mobile_id = MobileUtil.resolve_mobile_id(converted_mobile, raw_mobile)
        if mobile_id is None:
            return None

        return MobileUtil.build_mobile(mobile_id, self.game_data.races, converted_mobile)
