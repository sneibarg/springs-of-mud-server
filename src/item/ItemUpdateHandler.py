from injector import inject
from game.EnumProvider import EnumProvider
from game.RegistryService import RegistryService
from item.Item import Item
from item.ItemOwnership import ItemOwnership
from item.EffectUpdateHandler import EffectUpdateHandler
from mobile.Mobile import Mobile
from server.messaging.MessageBus import MessageBus
from util.GenericUtil import GenericUtil


class ItemUpdateHandler:
    """Coordinate item effects and expiration across world ownership locations."""

    @inject
    def __init__(self, registry_service: RegistryService, enum_provider: EnumProvider,
                 effect_update_handler: EffectUpdateHandler, message_bus: MessageBus):
        self.room_registry = registry_service.room_registry
        self.shop_registry = registry_service.shop_registry
        self.enum_provider = enum_provider
        self.effect_update_handler = effect_update_handler
        self.message_bus = message_bus
        self.ItemTypes = enum_provider.get("itemTypes")
        self.WearLocation = enum_provider.get("wearLocation")
        self.WearFlags = enum_provider.get("wearFlags")

    async def update(self):
        if self.ItemTypes is None:
            return
        items = [item for item, _, _ in self._ownership().walk_world_items()]
        for item in items:
            await self.tick_effects(item)
            if Item.tick_timer(item):
                await self.expire_item(item)

    async def tick_effects(self, item):
        for message in self.effect_update_handler.expired_messages(item, "msg_obj"):
            await self._emit_obj_effect_message(item, message)

    def _ownership(self):
        return ItemOwnership(self.effect_update_handler.effect_handler, self.room_registry)

    def _locate_item(self, target):
        return self._ownership().find_location(target)

    async def expire_item(self, item):
        item_type = str(getattr(item, "item_type", "") or "").upper()
        is_pc_corpse = self.ItemTypes is not None and item_type in [self.ItemTypes.ITEM_CORPSE_PC.name]
        is_float = (
            self.WearLocation is not None
            and GenericUtil.to_int(getattr(item, "wear_loc", -1), -1) in [self.WearLocation.WEAR_FLOAT.value]
        )

        location = self._locate_item(item)
        if location is None:
            return

        parent_kind = location["kind"]
        parent = location["parent"]
        container = location["container"]
        room = location.get("room")

        shop = (self.shop_registry.find_by_keeper_vnum(getattr(parent, "vnum", ""))
                if parent_kind in ("mob_inventory", "mob_equipped") else None)
        if shop is not None:
            Mobile.credit_expired_stock(parent, item)
        elif not (parent_kind == "item_contains" and Item.is_fixed_pit(
                parent, self.enum_provider.get("wellKnownObjectVnums"), self.WearFlags)):
            message = Item.decay_message(item, self.WearFlags)
            await self._emit_item_decay_message(message, item, parent_kind, parent, room, is_float)

        contents = list(getattr(item, "contains", []) or [])
        if (is_pc_corpse or is_float) and contents:
            for child in contents:
                self._move_child_from_expiring_item(child, parent_kind, parent, container, room)
            item.contains = []

        self._remove_item_at_location(item, parent_kind, parent, container)

    def _move_child_from_expiring_item(self, child, parent_kind: str, parent, container, room):
        if parent_kind == "room":
            parent.contents[getattr(child, "id", GenericUtil.generate_mongo_id())] = child
            return
        if parent_kind == "char_loot":
            parent.loot.append(child)
            return
        if parent_kind == "mob_inventory":
            parent.inventory.append(child)
            return
        if parent_kind == "item_contains":
            container.append(child)
            return
        if parent_kind == "char_equipped":
            holder = room or self.room_registry.get_or_none(id=getattr(parent, "room_id", ""))
            if holder is not None:
                holder.contents[getattr(child, "id", GenericUtil.generate_mongo_id())] = child
            return
        if parent_kind == "mob_equipped":
            holder = room
            if holder is not None:
                holder.contents[getattr(child, "id", GenericUtil.generate_mongo_id())] = child

    def _remove_item_at_location(self, item, parent_kind: str, parent, container):
        self._ownership().detach(item, {"kind": parent_kind, "parent": parent, "container": container})

    async def _emit_obj_effect_message(self, item, message: str):
        location = self._locate_item(item)
        if location is None:
            return

        parent_kind = location["kind"]
        parent = location["parent"]
        room = location.get("room")
        text = Item.format_message(item, message)
        if not text:
            return

        if parent_kind in ["char_loot", "char_equipped"]:
            await self.message_bus.send_to_character(parent.id, self.message_bus.text_to_message(text + "\r\n"))
            return
        if room is not None:
            in_room = room.players_in_room()
            message = self.message_bus.text_to_message(text + "\r\n")
            await self.message_bus.send_to_room(message, in_room)

    async def _emit_item_decay_message(self, message: str, item, parent_kind: str, parent, room, is_float: bool):
        text = Item.format_message(item, message)
        if not text:
            return

        message = self.message_bus.text_to_message(text + "\r\n")
        if parent_kind in ["char_loot", "char_equipped"]:
            await self.message_bus.send_to_character(parent.id, self.message_bus.text_to_message(text + "\r\n"))
            if is_float and room is not None:
                in_room = room.players_in_room()
                await self.message_bus.send_to_room(message, in_room)
            return
        if room is not None:
            in_room = room.players_in_room()
            await self.message_bus.send_to_room(message, in_room)

