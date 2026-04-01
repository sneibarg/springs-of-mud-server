from injector import inject

from player.Character import Character
from server.messaging import MessageBus
from server.protocol import Message, MessageType
from object.Item import Item


class ItemHandler:
    @inject
    def __init__(self, message_bus: MessageBus):
        self.message_bus = message_bus

    async def print_name(self, player_id: str, item: Item):
        msg = "\t" + item.name + "\r\n"
        await self.message_bus.send_to_character(player_id, Message(type=MessageType.GAME, data={"text": msg}))

    async def print_description(self, player_id: str, item: Item):
        msg = "\r\n\n" + item.long_description + "\r\n\n"
        await self.message_bus.send_to_character(player_id, Message(type=MessageType.GAME, data={"text": msg}))

    async def print_inventory(self, character: Character):
        items = character.get_items()
        msg = "\r\n\nYou are carrying:\r\n"
        for item in items:
            msg = msg + "\t" + item.name + "\r\n"
        await self.message_bus.send_to_character(character.id, Message(type=MessageType.GAME, data={"text": msg}))
