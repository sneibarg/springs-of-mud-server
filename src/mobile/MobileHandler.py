from injector import inject
from area.RoomRegistry import RoomRegistry
from player.Character import Character
from server.messaging import MessageBus


class MobileHandler:
    @inject
    def __init__(self, message_bus: MessageBus, room_registry: RoomRegistry):
        self.message_bus = message_bus
        self.room_registry = room_registry

    async def print_mobiles_in_room(self, character: Character):
        room = self.room_registry.get(id=character.room_id)
        if room is None:
            return

        lines = []
        for mob in room.mobiles or []:
            line = (mob.long_description or "").strip()
            if not line:
                line = f"{mob.short_description or mob.name} is here."
            lines.append(line)

        if lines:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("\r\n".join(lines) + "\r\n"))
