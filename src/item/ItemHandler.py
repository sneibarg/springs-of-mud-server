from injector import inject

from game.RegistryService import RegistryService
from interp.Context import Context
from util.InterpUtil import InterpUtil
from util.ItemUtil import ItemUtil
from api.ItemApi import ItemApi
from player.Character import Character
from server.messaging import MessageBus


class ItemHandler:
    @inject
    def __init__(self, message_bus: MessageBus, registry_service: RegistryService):
        self.message_bus = message_bus
        self.room_registry = registry_service.room_registry
        self.item_registry = registry_service.item_registry

    async def look_room_items(self, character: Character):
        room = self.room_registry.get(id=character.room_id)
        if room is None:
            return
        lines = ItemUtil.room_items(room)
        if lines:
            message = self.message_bus.text_to_message("\r\n".join(lines) + "\r\n")
            await self.message_bus.send_to_character(character.id, message)

    async def look_in_item(self, character: Character, context: Context):
        arg1 = (context.parameters[0] if context.parameters and len(context.parameters) > 0 else "").strip().lower()
        if arg1 not in ("i", "in", "on"):
            return

        room = context.room if context.room is not None else self.room_registry.get(id=character.room_id)
        arg2 = (context.parameters[1] if context.parameters and len(context.parameters) > 1 else "").strip().lower()
        obj = ItemUtil.find_item(character, room, arg2)

        if ItemUtil.is_drink_container(obj):
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(ItemUtil.container_volume_description(obj)))
            context.finish()
            return

        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(ItemUtil.items_in_container(obj)))
        context.finish()

    async def look_item_or_extra(self, character: Character, context: Context):
        room = context.room if context.room is not None else self.room_registry.get(id=character.room_id)
        if room is None:
            context.finish()
            return

        arg1 = (context.parameters[0] if context.parameters and len(context.parameters) > 0 else "").strip().lower()
        number, arg3 = InterpUtil.number_argument(arg1)
        context.number = max(1, number)
        context.count = 0
        token = (arg3 or "").strip().lower()

        for item in list(character.get_items()) + list(room.contents.values()):
            if not ItemUtil.can_see_object(room, character, item):
                continue

            extra = getattr(item, "extra_description", None)
            extra_keyword = getattr(extra, "keyword", None) if extra is not None else None
            extra_description = getattr(extra, "description", None) if extra is not None else None
            if isinstance(extra, dict):
                extra_keyword = extra.get("keyword")
                extra_description = extra.get("description")
            if extra and context.look_keyword_matches(token, extra_keyword or ""):
                if context.look_register_match():
                    await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message((extra_description or "") + "\r\n"))
                    context.finish()
                    return

            if context.look_keyword_matches(token, item.name or ""):
                if context.look_register_match():
                    text = (item.long_description or item.short_description or item.name or "You see nothing special.") + "\r\n"
                    await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))
                    context.finish()
                    return

        room_extra = getattr(room, "extra_description", None)
        if room_extra and context.look_keyword_matches(token, room_extra.keyword or ""):
            if context.look_register_match():
                await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(
                    (room_extra.description or "") + "\r\n"))
                context.finish()
                return

        if context.count > 0 and context.count != context.number:
            if context.count == 1:
                text = f"You only see one {token} here.\r\n"
            else:
                text = f"You only see {context.count} of those here.\r\n"
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))
            context.finish()
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
