from injector import inject
from api.CharacterApi import CharacterApi
from game.EnumProvider import EnumProvider
from game.RegistryService import RegistryService
from item.Item import Item
from item.ItemOwnership import ItemOwnership
from item.EffectUpdateHandler import EffectUpdateHandler
from mobile.Mobile import Mobile
from player.Character import Character
from server.messaging.MessageBus import MessageBus
from util.DisplayUtil import DisplayUtil, RecipientText
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
        # The socket loop owns all live mutations. Finish this phase without
        # yielding, so pickup/transfer/quit cannot invalidate selected ownership.
        notices = []
        for item, _, location in list(self._ownership().walk_world_items()):
            owner = location['parent']
            if isinstance(owner, Character) and owner.world_retired:
                continue
            for message in self.effect_update_handler.expired_messages(item, "msg_obj"):
                current = self._locate_item(item)
                if current is not None:
                    notices.append((message, item, current, False, False))
            if Item.tick_timer(item):
                notice = self._expire_item(item)
                if notice is not None:
                    notices.append((*notice, True))
        for text, item, location, is_float, decay in notices:
            await self._emit_item_message(text, item, location['kind'], location['parent'],
                                          location.get('room'), is_float=is_float, decay=decay)

    async def tick_effects(self, item):
        for message in self.effect_update_handler.expired_messages(item, "msg_obj"):
            await self._emit_obj_effect_message(item, message)

    def _ownership(self):
        return ItemOwnership(self.effect_update_handler.effect_handler, self.room_registry)

    def _locate_item(self, target):
        return self._ownership().find_location(target)

    def _expire_item(self, item):
        """Complete decay synchronously; return its notice for async delivery."""
        is_pc_corpse = Item.is_pc_corpse(item)
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
            notice = None
        else:
            message = Item.decay_message(item, self.WearFlags)
            notice = (message, item, location, is_float)

        contents = list(getattr(item, "contains", []) or [])
        if (is_pc_corpse or is_float) and contents:
            for child in contents:
                self._move_child_from_expiring_item(child, parent_kind, parent, container, room, is_float)
            item.contains = []

        self._remove_item_at_location(item, parent_kind, parent, container)
        return notice

    def _move_child_from_expiring_item(self, child, parent_kind: str, parent, container, room, is_float: bool):
        if parent_kind == "item_contains":
            container.append(child)
        elif parent_kind == "room" or is_float:
            if room is not None:
                room.contents[getattr(child, "id", None) or GenericUtil.generate_mongo_id()] = child
        elif parent_kind in ("char_loot", "char_equipped"):
            parent.loot.append(child)
        elif parent_kind in ("mob_inventory", "mob_equipped"):
            parent.inventory.append(child)

    def _remove_item_at_location(self, item, parent_kind: str, parent, container):
        self._ownership().detach(item, {"kind": parent_kind, "parent": parent, "container": container})

    async def _emit_obj_effect_message(self, item, message: str):
        location = self._locate_item(item)
        if location is not None:
            await self._emit_item_message(message, item, location["kind"], location["parent"], location.get("room"))

    async def _emit_item_message(self, text: str, item, parent_kind: str, parent, room, *, is_float: bool = False, decay: bool = False):
        """Only direct carriers and directly exposed room objects receive notices."""
        if not text or parent_kind == "item_contains":
            return

        def render(observer):
            if not decay:
                return Item.format_message(item, text) + "\r\n"
            name = DisplayUtil.visible_tokens({"item": item}, observer, room)["item"]
            rendered = text.replace("$p", name)
            return rendered[:1].upper() + rendered[1:] + "\r\n"

        resting = CharacterApi.pos_value("POS_RESTING") if decay else None
        controlled = decay and (getattr(parent, "context", None) or {}).get("controller_original")
        if parent_kind in ("char_loot", "char_equipped") or controlled:
            if not decay or CharacterApi.position_value(parent) >= resting:
                await self.message_bus.send_to_character(parent.id, self.message_bus.text_to_message(render(parent)))
        if room is not None and (parent_kind == "room" or is_float):
            if decay:
                listeners = DisplayUtil.room_listeners(None if parent_kind == "room" else parent, room)
            else:
                listeners = [player for player in room.players_in_room() if player is not parent]
            if listeners:
                if decay:
                    fallback = render(None)
                    text = RecipientText(fallback, {str(observer.id): render(observer) for observer in listeners}, fallback)
                else:
                    text = render(None)
                await self.message_bus.send_to_room(self.message_bus.text_to_message(text), listeners)
