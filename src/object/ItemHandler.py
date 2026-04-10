from injector import inject

from game.RegistryService import RegistryService
from player.Character import Character
from server.messaging import MessageBus
from server.protocol import Message, MessageType


CONTAINER_CLOSED_BIT = 1


class ItemHandler:
    @inject
    def __init__(self, message_bus: MessageBus, registry_service: RegistryService):
        self.message_bus = message_bus
        self.registry_service = registry_service

    async def print_name(self, player_id: str, item):
        msg = "\t" + item.name + "\r\n"
        await self.message_bus.send_to_character(player_id, Message(type=MessageType.GAME, data={"text": msg}))

    async def print_description(self, character_id: str, item):
        msg = "\r\n\n" + item.long_description + "\r\n\n"
        await self.message_bus.send_to_character(character_id, Message(type=MessageType.GAME, data={"text": msg}))

    async def print_inventory(self, character: Character):
        items = character.get_items()
        msg = "\r\n\nYou are carrying:\r\n"
        for item in items:
            msg = msg + "\t" + item.name + "\r\n"
        await self.message_bus.send_to_character(character.id, Message(type=MessageType.GAME, data={"text": msg}))

    def _room_items(self, character: Character):
        room = self.registry_service.room_registry.get(id=character.room_id)
        if room is None:
            return []

        room_id = str(room.id)
        room_vnum = str(room.vnum)
        found = []
        for item in self.registry_service.item_registry.all_items():
            rid = None
            if isinstance(item.room_index_data, dict):
                rid = item.room_index_data.get("id") or item.room_index_data.get("room_id") or item.room_index_data.get("vnum")
            if rid is None:
                continue
            rid = str(rid)
            if rid == room_id or rid == room_vnum:
                found.append(item)
        return found

    def _find_item_here(self, character: Character, name: str):
        wanted = (name or "").strip().lower()
        if not wanted:
            return None
        for item in character.get_items():
            nm = (item.name or "").lower()
            if nm == wanted or nm.startswith(wanted):
                return item
        for item in self._room_items(character):
            nm = (item.name or "").lower()
            if nm == wanted or nm.startswith(wanted):
                return item
        return None

    def _is_drink_container(self, item) -> bool:
        t = (item.item_type or "").strip().lower()
        return ("drink" in t) or ("fountain" in t)

    def _is_container_like(self, item) -> bool:
        t = (item.item_type or "").strip().lower()
        return ("container" in t) or ("corpse" in t)

    def _container_closed(self, item) -> bool:
        try:
            flags = int(item.value1)
        except (TypeError, ValueError):
            return False
        return (flags & CONTAINER_CLOSED_BIT) != 0

    async def look_room_items(self, character: Character, player_handler):
        if player_handler.look_done(character):
            return
        ctx = player_handler.look_context(character)
        if ctx.get("branch") != "default":
            return

        lines = []
        for item in self._room_items(character):
            line = (item.long_description or "").strip()
            if not line:
                line = item.short_description or item.name
            if line:
                lines.append(line)

        if lines:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("\r\n".join(lines) + "\r\n"))

    async def look_in_item(self, character: Character, player_handler):
        if player_handler.look_done(character):
            return

        ctx = player_handler.look_context(character)
        arg1 = ctx.get("arg1", "")
        arg2 = ctx.get("arg2", "")

        if arg1 not in {"i", "in", "on"}:
            return

        if not arg2:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("Look in what?\r\n"))
            player_handler.look_mark_done(character)
            return

        obj = self._find_item_here(character, arg2)
        if obj is None:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("You do not see that here.\r\n"))
            player_handler.look_mark_done(character)
            return

        if self._is_drink_container(obj):
            try:
                cap = max(0, int(obj.value0))
                cur = max(0, int(obj.value1))
            except (TypeError, ValueError):
                cap = 0
                cur = 0

            if cur <= 0:
                text = "It is empty.\r\n"
            else:
                if cap <= 0:
                    fill = "partly "
                elif cur < cap / 4:
                    fill = "less than half-"
                elif cur < (3 * cap) / 4:
                    fill = "about half-"
                else:
                    fill = "more than half-"
                color = getattr(obj, "liquid_color", None) or "unknown"
                text = f"It's {fill}filled with a {color} liquid.\r\n"

            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))
            player_handler.look_mark_done(character)
            return

        if self._is_container_like(obj):
            if self._container_closed(obj):
                await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("It is closed.\r\n"))
                player_handler.look_mark_done(character)
                return

            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(f"{obj.name} holds:\r\nNothing.\r\n"))
            player_handler.look_mark_done(character)
            return

        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("That is not a container.\r\n"))
        player_handler.look_mark_done(character)

    async def look_item_or_extra(self, character: Character, player_handler):
        if player_handler.look_done(character):
            return

        ctx = player_handler.look_context(character)
        token = (ctx.get("arg3", "") or "").strip().lower()
        if not token:
            return

        for item in list(character.get_items()) + self._room_items(character):
            extra = getattr(item, "extra_description", None)
            if extra and player_handler.look_keyword_matches(token, extra.keyword or ""):
                if player_handler.look_register_match(character):
                    await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message((extra.description or "") + "\r\n"))
                    player_handler.look_mark_done(character)
                    return

            if player_handler.look_keyword_matches(token, item.name or ""):
                if player_handler.look_register_match(character):
                    text = (item.long_description or item.short_description or item.name or "You see nothing special.") + "\r\n"
                    await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))
                    player_handler.look_mark_done(character)
                    return