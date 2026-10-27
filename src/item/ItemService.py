from injector import inject

from game.GameData import GameData
from item.Item import Item
from item.ItemRegistry import ItemRegistry
from item.ItemFactory import ItemFactory
from server.FetchAndRegisterMixin import FetchAndRegisterMixin
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig
from skill.SkillRegistry import SkillRegistry
from skill.SpellRegistry import SpellRegistry


class ItemService(FetchAndRegisterMixin):
    @inject
    def __init__(self, config: ServiceConfig, item_registry: ItemRegistry, skill_registry: SkillRegistry, spell_registry: SpellRegistry, game_data: GameData):
        self.__name__ = "ItemService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.items_endpoint = config.items_endpoint
        self.game_data = game_data
        self.item_registry = item_registry
        self.skill_registry = skill_registry
        self.spell_registry = spell_registry
        self.load_items()

    def reload_items(self) -> bool:
        return self._reload_collection(self.items_endpoint, "items", self.item_registry)

    def load_items(self):
        self._fetch_and_register(self.items_endpoint, "all items")

    def load_item(self, item_name: str):
        url = f"{self.items_endpoint}/name/{item_name}"
        return self._fetch_and_register(url, f"item '{item_name}'")

    def _build_fetch_item(self, item_data) -> Item:
        liquids = self.game_data.liquids
        return ItemFactory.from_data(item_data, liquids, (self.spell_registry, self.skill_registry))

    def _register_fetch_item(self, item: Item) -> None:
        self.item_registry.register(item)

