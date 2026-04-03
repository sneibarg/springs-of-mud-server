from typing import Optional

import requests
from injector import inject

from game.GameData import GameData
from object import Item
from object.ItemRegistry import ItemRegistry
from object.ItemUtil import ItemUtil
from object.ObjectMacros import ObjectMacros
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig
from skill.SkillRegistry import SkillRegistry


class ItemService:
    @inject
    def __init__(self, config: ServiceConfig, item_registry: ItemRegistry, skill_registry: SkillRegistry, game_data: GameData, object_macros: ObjectMacros):
        self.__name__ = "ItemService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.items_endpoint = config.items_endpoint
        self.game_data = game_data
        self.object_macros = object_macros
        self.enums = self.game_data.enums
        self.item_registry = item_registry
        self.skill_registry = skill_registry
        self.load_items()

    def reload_mobiles(self) -> None:
        self.logger.info("Reloading all mobiles...")
        self.item_registry.reset()
        self.load_items()
        self.logger.info("Mobiles reload completed.")

    def load_items(self):
        self._fetch_and_register(self.items_endpoint, "all items")

    def load_item(self, item_name: str):
        url = f"{self.items_endpoint}/name/{item_name}"
        return self._fetch_and_register(url, f"item '{item_name}'")

    def _fetch_and_register(self, url: str, description: str) -> Optional[Item]:
        liquids = self.game_data.liquids
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                count = 0
                for item_data in data:
                    item = ItemUtil.normalize_item_data(self.object_macros, item_data, liquids, self.skill_registry)
                    self.item_registry.register(item)
                    count += 1
                self.logger.info(f"Loaded {count} {description}.")
                return None
            else:
                item = ItemUtil.normalize_item_data(self.object_macros, data, liquids, self.skill_registry)
                self.item_registry.register(item)
                self.logger.info(f"Loaded {description}.")
                return item

        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {description} from {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error processing {description}: {e}", exc_info=True)
            return None


