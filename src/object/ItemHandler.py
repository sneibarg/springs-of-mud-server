from injector import inject
from game.RegistryService import RegistryService
from object.Item import Item
from object.ObjectHelper import ObjectHelper
from player.Character import Character
from server.messaging import MessageBus
from server.protocol import Message, MessageType


class ItemHandler:
    @inject
    def __init__(self, message_bus: MessageBus, registry_service: RegistryService, object_helper: ObjectHelper):
        self.message_bus = message_bus
        self.room_registry = registry_service.room_registry
        self.object_helper = object_helper
        self.object_macros = None

    def set_object_macros(self, object_macros):
        self.object_macros = object_macros
        self.ContainerState = object_macros.ContainerState

    def _room_items(self, character: Character):
        room = self.room_registry.get(id=character.room_id)
        if room is None:
            return []

        room_id = str(room.id)
        room_vnum = str(room.vnum)
        found = []
        for item in self.item_registry.all_items():
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

    async def _items_in_container(self, character: Character, obj: Item):
        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(f"{obj.name} holds:\r\n"))
        if len(obj.contains) > 0:
            for item in obj.contains:
                await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(f"\t{item.name}\r\n"))
        else:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("\tNothing.\r\n"))

    async def look_room_items(self, character: Character, player_handler):
        lines = []
        for item in self._room_items(character):
            line = (item.long_description or "").strip()
            if not line:
                line = item.short_description or item.name
            if line:
                lines.append(line)

        if lines:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("\r\n".join(lines) + "\r\n"))

    async def look_in_item(self, character: Character, player_handler, context: Context):
        arg2 = context.parameters[1] if len(context.parameters) > 1 else None
        if not arg2:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("Look in what?\r\n"))
            return

        obj = self._find_item_here(character, arg2)
        if obj is None:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("You do not see that here.\r\n"))
            return

        if self._is_drink_container(obj):
            text = ItemUtil.container_volume_description(obj)
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))
            return

        if self._is_container_like(obj):
            if self._container_closed(obj):
                await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("It is closed.\r\n"))
                return
            self._items_in_container(character, obj)
            return

        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("That is not a container.\r\n"))

    # to-do: match code needs to be re-added.
    async def look_item_or_extra(self, character: Character, player_handler, context: Context):
        token = context.parameters[1] if len(context.parameters) > 1 else ""
        for item in list(character.get_items()) + self._room_items(character):
            if not self.object_helper.can_see_object(character, item):
                continue

            extra = getattr(item, "extra_description", None)
            if extra and player_handler.look_keyword_matches(token, extra.keyword or ""):
                if player_handler.look_register_match(character):
                    await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message((extra.description or "") + "\r\n"))
                    return

            if player_handler.look_keyword_matches(token, item.name or ""):
                if player_handler.look_register_match(character):
                    text = (item.long_description or item.short_description or item.name or "You see nothing special.") + "\r\n"
                    await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))
                    return

    async def print_name(self, player_id: str, item):
        msg = "\t" + item.name + "\r\n"
        await self.message_bus.send_to_character(player_id, self.message_bus.text_to_message(msg))

    async def print_description(self, character_id: str, item):
        msg = "\r\n\n" + item.long_description + "\r\n\n"
        await self.message_bus.send_to_character(character_id, self.message_bus.text_to_message(msg))

    async def print_inventory(self, character: Character):
        items = character.get_items()
        msg = "\r\n\nYou are carrying:\r\n"
        for item in items:
            msg = msg + "\t" + item.name + "\r\n"
        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(msg))

    @staticmethod
    def _is_drink_container(item) -> bool:
        t = (item.item_type or "").strip().lower()
        return ("drink" in t) or ("fountain" in t)

    @staticmethod
    def _is_container_like(item) -> bool:
        t = (item.item_type or "").strip().lower()
        return ("container" in t) or ("corpse" in t)

    @staticmethod
    def _container_closed(item) -> bool:
        try:
            flags = int(item.value1)
            return self.is_set(flags, self.ContainerState.CONT_CLOSED.value)
        except (TypeError, ValueError):
            return False
