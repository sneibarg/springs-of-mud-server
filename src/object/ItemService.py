import requests

from injector import inject
from game import GameData
from object.Item import Item
from server.LoggerFactory import LoggerFactory
from server.ServerUtil import ServerUtil
from server.ServiceConfig import ServiceConfig


class ItemService:
    @inject
    def __init__(self, config: ServiceConfig, game_data: GameData):
        self.__name__ = "ItemService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.items_endpoint = config.items_endpoint
        self.game_data = game_data
        self.item_types = ServerUtil.build_enum("ITEM", "ItemType", self.game_data.enums["itemType"])
        self.enum_lookup = ServerUtil.build_enum_lookup(self.game_data.enums)
        self.all_items = {}
        self.load_items()
        self.logger.info("Initialized ObjectService instance with a total of "+str(len(self.all_items))+" in memory.")

    def return_item_by_id(self, item_id):
        return self.all_items[item_id]

    def get_item_by_id(self, item_id):
        url = self.items_endpoint + "/" + item_id
        try:
            return requests.get(url).json()
        except Exception as e:
            self.logger.error("Failed to get item data: "+str(e))
        return None

    def load_items(self):
        try:
            all_items = requests.get(self.items_endpoint).json()
            for item_data in all_items:
                item_id = item_data['id']
                item = self._normalize_item_data(item_data)
                self.all_items[item_id] = item
        except Exception as e:
            self.logger.error("Failed to get items: "+str(e))
        return None

    def _normalize_item_data(self, item_data) -> Item:
        self._update_item_type(item_data)
        self._update_condition(item_data)
        return Item.from_json(item_data)

    def _update_item_type(self, item_data):
        item_type = item_data.get("itemType")
        if item_type == self.item_types.ITEM_WEAPON:
            self._weapon_type(item_data)
        elif item_type == self.item_types.ITEM_CONTAINER:
            self._update_container()
        elif item_type == self.item_types.ITEM_FOUNTAIN:
            self._update_fountain()
        elif item_type == self.item_types.ITEM_STAFF:
            self._update_staff()
        elif item_type == self.item_types.ITEM_SCROLL:
            self._update_scroll()
        else:
            pass

    def _update_container(self):
        pass

    def _update_fountain(self):
        pass

    def _update_staff(self):
        pass

    def _update_scroll(self):
        pass

    def _weapon_type(self, item_data):
        pass

    def _attack_lookup(self):
        pass

    def _attack_type(self):
        pass

    def _liq_lookup(self):
        pass

    def _skill_lookup(self):
        pass

    def _update_condition(self, item_data):
        pass

    def _update_affect_data(self):
        pass

    def _update_extra_descr(self):
        pass
