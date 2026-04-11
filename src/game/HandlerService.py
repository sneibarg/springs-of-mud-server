from injector import inject

from area.RoomHandler import RoomHandler
from mobile.MobileHandler import MobileHandler
from object.ItemHandler import ItemHandler
from player.PlayerHandler import PlayerHandler
from server.LoggerFactory import LoggerFactory


class HandlerService:
    @inject
    def __init__(self, player_handler: PlayerHandler, room_handler: RoomHandler, mobile_handler: MobileHandler, item_handler: ItemHandler):
        self.__name__ = "HandlerService"
        self.logger = LoggerFactory.get_logger(__name__)
        self.player_handler = player_handler
        self.room_handler = room_handler
        self.mobile_handler = mobile_handler
        self.item_handler = item_handler
