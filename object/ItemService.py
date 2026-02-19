import requests

from server.LoggerFactory import LoggerFactory


class ItemService:
    def __init__(self, injector, config):
        self.__name__ = "ItemService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.injector = injector
        self.config = config['endpoints']
        self.all_items = {}
        self.total_items = 0
        self.load_items()
        self.logger.info("Initialized ObjectService instance with a total of "+str(self.total_items)+" in memory.")

    def return_item_by_id(self, item_id):
        return self.all_items[item_id]

    def get_item_by_id(self, item_id):
        url = self.config['items_endpoint'] + "/" + item_id
        try:
            return requests.get(url).json()
        except Exception as e:
            self.logger.error("Failed to get item data: "+str(e))
        return None

    def load_items(self):
        try:
            for item in requests.get(self.config['items_endpoint']).json():
                self.all_items[item['id']] = item
                self.total_items = self.total_items + 1
        except Exception as e:
            self.logger.error("Failed to get items: "+str(e))
        return None
