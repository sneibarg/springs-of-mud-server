from item.ExtraDescriptionData import ExtraDescriptionData
from util.LookupUtil import LookupUtil
from area.Room import Room
from api.ItemApi import ItemApi
from injector import inject

from api.CharacterApi import CharacterApi
from game.RegistryService import RegistryService
from interp.Context import Context
from item.Item import Item
from util.InterpUtil import InterpUtil
from util.InfoUtil import InfoUtil
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
        lines = Room.item_description_lines(room, character)
        if lines:
            message = self.message_bus.text_to_message("\r\n".join(lines) + "\r\n")
            await self.message_bus.send_to_character(character.id, message)

    async def look_in_item(self, character: Character, context: Context):
        arg1 = (context.parameters[0] if context.parameters and len(context.parameters) > 0 else "").strip().lower()
        if arg1 not in ("i", "in", "on"):
            return

        room = context.room if context.room is not None else self.room_registry.get(id=character.room_id)
        arg2 = (context.parameters[1] if context.parameters and len(context.parameters) > 1 else "").strip().lower()
        obj = LookupUtil.here(character, room, arg2,
                              visible=lambda item: ItemApi.can_see_object(room, character, item))

        if Item.is_drink_container(obj):
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(Item.container_volume_description(obj)))
            context.finish()
            return

        text = f"{obj.short() if obj is not None else ''} holds\r\n"
        text += '\r\n'.join(InfoUtil.visible_item_lines([] if obj is None else obj.contains, character, room)) + '\r\n'
        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))
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
            if not ItemApi.can_see_object(room, character, item):
                continue

            for extra in ExtraDescriptionData.entries(getattr(item, 'extra_description', None)):
                if LookupUtil.keyword_matches(token, extra.keyword or ''):
                    if context.register_match():
                        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message((extra.description or '') + "\r\n"))
                        context.finish()
                        return
                    # Each object contributes at most one matching description.
                    break

            if LookupUtil.keyword_matches(token, item.name or ""):
                if context.register_match():
                    text = (item.long_description or item.short_description or item.name or "You see nothing special.") + "\r\n"
                    await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))
                    context.finish()
                    return

        room_extra = getattr(room, "extra_description", None)
        if room_extra and LookupUtil.keyword_matches(token, room_extra.keyword or ""):
            if context.register_match():
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
        room = self.room_registry.get(id=character.room_id)
        msg = "\r\n\nYou are carrying:\r\n"
        msg += '\r\n'.join(InfoUtil.visible_inventory_lines(character, character, room)) + '\r\n'
        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(msg))
