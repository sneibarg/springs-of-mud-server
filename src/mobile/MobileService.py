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
from object.ObjectMacros import ObjectMacros


class MobileService:
    @inject
    def __init__(self, config: ServiceConfig, area_registry: AreaRegistry, mobile_registry: MobileRegistry, fight_handler: FightHandler, game_data: GameData, object_macros: ObjectMacros):
        self.__name__ = "MobileService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.mobile_registry = mobile_registry
        self.game_data = game_data
        self.enums = self.game_data.enums
        self.mobiles_endpoint = config.mobiles_endpoint
        self.area_registry = area_registry
        self.fight_handler = fight_handler
        self.object_macros = object_macros
        self.kill_table: dict[int, int] = {}
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
            if isinstance(data, list):
                count = 0
                for raw_mobile in data:
                    mobile = self._build_mobile(raw_mobile, npc_flag, kill_table)
                    if mobile is None:
                        self.logger.error(f"Failed to build mobile for {raw_mobile}")
                        continue
                    print(f"Mobile flags: {mobile.flags}")
                    self.mobile_registry.register(mobile)
                    count += 1
                self.kill_table = kill_table
                self.logger.info(f"Loaded {count} {description}.")
                return None
            else:
                mobile = self._build_mobile(data, npc_flag, kill_table)
                if mobile is None:
                    return None
                self.mobile_registry.register(mobile)
                self.logger.info(f"Loaded {description}.")
                return mobile

        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {description} from {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error processing {description}: {e}", exc_info=True)
            return None

    def _build_mobile(self, raw_mobile, npc_flag, kill_table) -> Optional[Mobile]:
        from server.ServerUtil import ServerUtil
        converted_mobile = ServerUtil.camel_to_snake_case(raw_mobile)
        converted_mobile['form'] = MobileUtil.convert_form(converted_mobile['race'], converted_mobile['form'], self.object_macros)
        converted_mobile['parts'] = MobileUtil.convert_parts(converted_mobile['race'], converted_mobile['parts'], self.object_macros)

        mobile_id = MobileUtil.resolve_mobile_id(converted_mobile, raw_mobile)
        if mobile_id is None:
            return None

        mobile, level = MobileUtil.build_mobile(mobile_id, self.game_data.races, converted_mobile, npc_flag, self.enums)
        MobileUtil.increment_kill_table(kill_table, level)
        return mobile
