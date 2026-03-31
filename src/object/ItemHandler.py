from injector import inject
from server.messaging import MessageBus
from server.protocol import Message, MessageType
from object.Item import Item


class ItemHandler:
    @inject
    def __init__(self, message_bus: MessageBus):
        self.message_bus = message_bus

    def print_name(self, player_id: str, item: Item):
        msg = "\t" + item.name + "\r\n"
        self.message_bus.send_to_character(player_id, Message(type=MessageType.GAME, data={"text": msg}))

    def print_description(self, player_id: str, item: Item):
        msg = "\r\n\n" + item.long_description + "\r\n\n"
        self.message_bus.send_to_character(player_id, Message(type=MessageType.GAME, data={"text": msg}))
