import requests
from injector import inject

from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig


class ItemService:
    @inject
    def __init__(self, config: ServiceConfig):
        self.__name__ = "ItemService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.items_endpoint = config.items_endpoint
        self.all_items = {}
        self.total_items = 0
        self.load_items()
        self.logger.info("Initialized ObjectService instance with a total of "+str(self.total_items)+" in memory.")

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
            for item in requests.get(self.items_endpoint).json():
                self.all_items[item['id']] = item
                self.total_items = self.total_items + 1
        except Exception as e:
            self.logger.error("Failed to get items: "+str(e))
        return None
