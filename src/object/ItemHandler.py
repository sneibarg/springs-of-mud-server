from injector import inject

from game.RegistryService import RegistryService
from interp.Context import Context
from interp.InterpUtil import InterpUtil
from object.ItemUtil import ItemUtil
from object.ObjectHelper import ObjectHelper
from player.Character import Character
from server.messaging import MessageBus


class ItemHandler:
    @inject
    def __init__(self, message_bus: MessageBus, registry_service: RegistryService, object_helper: ObjectHelper):
        self.message_bus = message_bus
        self.room_registry = registry_service.room_registry
        self.item_registry = registry_service.item_registry
        self.object_helper = object_helper
        self.object_macros = None
        self.ContainerState = None

    def set_object_macros(self, object_macros):
        self.object_macros = object_macros
        self.ContainerState = object_macros.ContainerState

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

        room = self.room_registry.get(id=character.room_id)
        arg2 = (context.parameters[1] if context.parameters and len(context.parameters) > 1 else "").strip().lower()
        if not arg2:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("Look in what?\r\n"))
            context.finish()
            return

        obj = ItemUtil.find_item(character, room, arg2)
        if obj is None:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("You do not see that here.\r\n"))
            context.finish()
            return

        if ItemUtil.is_drink_container(obj):
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(
                ItemUtil.container_volume_description(obj)))
            context.finish()
            return

        if ItemUtil.is_container_like(obj):
            if self.object_macros.is_container_closed(obj):
                await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("It is closed.\r\n"))
                context.finish()
                return
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(ItemUtil.items_in_container(obj)))
            context.finish()
            return

        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("That is not a container.\r\n"))
        context.finish()

    async def look_item_or_extra(self, character: Character, context: Context):
        room = self.room_registry.get(id=character.room_id)
        if room is None:
            context.finish()
            return

        arg1 = (context.parameters[0] if context.parameters and len(context.parameters) > 0 else "").strip().lower()
        number, arg3 = InterpUtil.number_argument(arg1)
        context.number = max(1, number)
        context.count = 0
        token = (arg3 or "").strip().lower()

        for item in list(character.get_items()) + list(room.contents.values()):
            if not self.object_helper.can_see_object(character, item):
                continue

            extra = getattr(item, "extra_description", None)
            if extra and context.look_keyword_matches(token, extra.keyword or ""):
                if context.look_register_match():
                    await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message((extra.description or "") + "\r\n"))
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
