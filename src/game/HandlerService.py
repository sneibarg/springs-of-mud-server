from injector import inject

from area.RoomHandler import RoomHandler
from interp.SocialHandler import SocialHandler
from mobile.MobileHandler import MobileHandler
from item.ItemHandler import ItemHandler
from player.PlayerHandler import PlayerHandler
from server.LoggerFactory import LoggerFactory


class HandlerService:
    @inject
    def __init__(self, player_handler: PlayerHandler,
                 room_handler: RoomHandler,
                 mobile_handler: MobileHandler,
                 item_handler: ItemHandler,
                 social_handler: SocialHandler):
        self.__name__ = "HandlerService"
        self.logger = LoggerFactory.get_logger(__name__)
        self.player_handler = player_handler
        self.room_handler = room_handler
        self.mobile_handler = mobile_handler
        self.item_handler = item_handler
        self.social_handler = social_handler
        self.safe_handlers = {
            'ph': self.player_handler,
            'rh': self.room_handler,
            'mh': self.mobile_handler,
            'ih': self.item_handler,
            'sh': self.social_handler,
        }

    def get_handler(self, key: str):
        return self.safe_handlers.get(key)
