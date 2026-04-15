from injector import inject
from area.RoomHelper import RoomHelper
from area.RoomRegistry import RoomRegistry
from mobile.MobileHelper import MobileHelper
from player.Character import Character
from server.messaging import MessageBus


class MobileHandler:
    @inject
    def __init__(self, message_bus: MessageBus, room_registry: RoomRegistry, room_helper: RoomHelper, mobile_helper: MobileHelper):
        self.message_bus = message_bus
        self.room_registry = room_registry
        self.room_helper = room_helper
        self.mobile_helper = mobile_helper

    async def print_mobiles_in_room(self, character: Character):
        message = self.mobile_helper.get_mobiles_in_room(character)
        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(message))
