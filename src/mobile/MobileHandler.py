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

    async def look_mobile_target(self, character: Character, player_handler):
        if player_handler.look_done(character):
            return

        ctx = player_handler.look_context(character)
        arg1 = ctx.get("arg1", "")
        if not arg1 or arg1 in {"i", "in", "on"}:
            return

        room = self.room_registry.get(id=character.room_id)
        if room is None:
            return

        target = None
        for mob in room.mobiles or []:
            mob_name = (mob.name or "").lower()
            short_name = (mob.short_description or "").lower()
            if mob_name == arg1 or mob_name.startswith(arg1) or short_name.startswith(arg1):
                target = mob
                break

        if target is None:
            return

        header = target.short_description or target.name or "Someone"
        desc = (target.description or "").strip() or "You see nothing special."
        text = f"{header}\r\n{desc}\r\n"
        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))
        player_handler.look_mark_done(character)