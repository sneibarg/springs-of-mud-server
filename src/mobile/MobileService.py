import requests

from typing import Optional
from injector import inject
from mobile.Mobile import Mobile
from mobile.MobileUtil import MobileUtil
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig
from fight.FightHandler import FightHandler
from game.GameData import GameData
from area.AreaRegistry import AreaRegistry
from mobile.MobileRegistry import MobileRegistry


class MobileService:
    @inject
    def __init__(self, config: ServiceConfig,
                 area_registry: AreaRegistry,
                 mobile_registry: MobileRegistry,
                 fight_handler: FightHandler,
                 game_data: GameData):
        self.__name__ = "MobileService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.mobile_registry = mobile_registry
        self.game_data = game_data
        self.enums = self.game_data.enums
        self.mobiles_endpoint = config.mobiles_endpoint
        self.area_registry = area_registry
        self.fight_handler = fight_handler
        self.kill_table: dict[int, int] = {}

    def start(self):
        self.load_mobiles()

    def reload_mobiles(self) -> None:
        self.logger.info("Reloading all socials...")
        self.mobile_registry.reset()
        self.load_mobiles()
        self.logger.info("Socials reload completed.")

    def load_mobiles(self):
        self._fetch_and_register(self.mobiles_endpoint, "all mobiles")

    def load_mobile(self, mobile_name: str):
        url = f"{self.mobiles_endpoint}/name/{mobile_name}"
        return self._fetch_and_register(url, f"social '{mobile_name}'")

    def _fetch_and_register(self, url: str, description: str) -> Optional[Mobile]:
        kill_table: dict[int, int] = {}
        npc_flag = MobileUtil.resolve_npc_flag(self.game_data)
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            from server.ServerUtil import ServerUtil
            if isinstance(data, list):
                count = 0
                for raw_mobile in data:
                    converted_mobile = ServerUtil.camel_to_snake_case(raw_mobile)
                    mobile_id = MobileUtil.resolve_mobile_id(converted_mobile, raw_mobile)
                    if mobile_id is None:
                        continue

                    mobile, level = MobileUtil.build_mobile(mobile_id, self.game_data.races, converted_mobile, npc_flag)
                    MobileUtil.increment_kill_table(kill_table, level)
                    self.mobile_registry.register(mobile)
                    count += 1
                self.kill_table = kill_table
                self.logger.info(f"Loaded {count} {description}.")
                return None
            else:
                social = Mobile.from_json(data)
                self.mobile_registry.register(social)
                self.logger.info(f"Loaded {description}.")
                return social

        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {description} from {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error processing {description}: {e}", exc_info=True)
            return None


