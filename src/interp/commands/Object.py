from __future__ import annotations

from injector import inject

from game.Equipped import Equipped
from item.Item import Item
from util.GenericUtil import GenericUtil
from game.RegistryService import RegistryService
from interp.Context import Context
from util.InterpUtil import InterpUtil
from util.MobileUtil import MobileUtil
from util.EffectUtil import EffectUtil
from util.ItemUtil import ItemUtil
from api.ItemApi import ItemApi
from api.InterpApi import InterpApi
from player.Character import Character
from api.CharacterApi import CharacterApi
from server.LoggerFactory import LoggerFactory


class Object:
    @inject
    def __init__(self, registry_service: RegistryService, weather_handler=None, interp_api=None):
        self.__name__ = "Object"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry_service = registry_service
        self.room_registry = getattr(registry_service, "room_registry", None)
        self.mobile_registry = getattr(registry_service, "mobile_registry", None)
        self.shop_registry = getattr(registry_service, "shop_registry", None)
        self.weather_handler = weather_handler
        self.interp_api = interp_api or InterpApi()
        self.item_types = None
        self.item_flags = None
        self.wear_flags = None
        self.room_flags = None
        self.act_bits = None
        self.affected_bits = None
        self.comm_flags = None

    def lazy_load(self):
        self.item_types = CharacterApi.get_enum("itemTypes")
        self.item_flags = CharacterApi.get_enum("itemFlags")
        self.wear_flags = CharacterApi.get_enum("wearFlags")
        self.room_flags = CharacterApi.get_enum("roomFlags")
        self.act_bits = CharacterApi.get_enum("actBits")
        self.affected_bits = CharacterApi.get_enum("affectedBy")
        self.comm_flags = CharacterApi.get_enum("commFlags")
        if self.item_types is None or self.item_flags is None or self.wear_flags is None:
            raise ValueError("Failed to load shop and item enums")

    def execute(self, character: Character, context: Context):
        name = (getattr(context.command, "name", "") or "").strip().lower()
        handlers = {
            "get": self.do_get,
            "put": self.do_put,
            "drop": self.do_drop,
            "junk": self.do_junk,
            "sacrifice": self.do_sacrifice,
            "give": self.do_give,
            "wear": self.do_wear,
            "wield": self.do_wield,
            "hold": self.do_hold,
            "grab": self.do_hold,
            "remove": self.do_remove,
            "buy": self.do_buy,
            "list": self.do_list,
            "sell": self.do_sell,
            "value": self.do_value,
            "drink": self.do_drink,
            "eat": self.do_eat,
            "fill": self.do_fill,
            "pour": self.do_pour,
            "quaff": self.do_quaff,
            "recite": self.do_recite,
            "brandish": self.do_brandish,
            "zap": self.do_zap,
        }
        fn = handlers.get(name)
        if fn is None:
            print(f"Executing function {fn}")
            context.finish()
            return {"to_char": f"{name} is not implemented yet.\r\n"}
        return fn(character, context)

    def do_buy(self, character: Character, context: Context):
        room = self.room_registry.get_or_none(id=character.room_id)
        raw = (context.result if isinstance(context.result, str) else "").strip()
        if not raw and context.parameters:
            raw = " ".join(context.parameters).strip()
        if not raw:
            context.finish()
            return {"to_char": "Buy what?\r\n"}
        if room is None:
            context.finish()
            return {"to_char": "You can't do that here.\r\n"}

        if self._is_pet_shop(room):
            payload = self._buy_pet(character, room, raw)
            context.finish()
            return payload

        keeper, shop, error = self._find_keeper(character, room)
        if error:
            context.finish()
            return {"to_char": error}

        quantity, selector = self._mult_argument(raw)
        if quantity < 1 or quantity > 99:
            context.finish()
            return {"to_char": "Get real!\r\n"}

        obj = self._get_keeper_stock_item(character, keeper, selector)
        cost = 0 if obj is None else shop.buy_price(obj)
        if obj is None or cost <= 0 or not ItemUtil.can_see_object(room, character, obj):
            context.finish()
            return {"to_char": "I don't sell that -- try 'list'.\r\n"}

        if not self._is_inventory_item(obj):
            available = self._available_stock_quantity(keeper, obj)
            if available < quantity:
                context.finish()
                return {"to_char": "I don't have that many in stock.\r\n"}

        total_cost = cost * quantity
        if not self._can_afford(character, total_cost):
            context.finish()
            if quantity > 1:
                return {"to_char": "You can't afford to buy that many.\r\n"}
            return {"to_char": f"You can't afford to buy {ItemUtil.short(obj)}.\r\n"}

        if GenericUtil.to_int(getattr(obj, "level", 0), 0) > GenericUtil.to_int(getattr(character, "level", 0), 0):
            context.finish()
            return {"to_char": f"You can't use {ItemUtil.short(obj)} yet.\r\n"}

        if self._carry_count(character) + quantity > self._max_items(character):
            context.finish()
            return {"to_char": "You can't carry that many items.\r\n"}

        if self._carry_weight(character) + (quantity * GenericUtil.to_int(getattr(obj, "weight", 0), 0)) > self._max_weight(character):
            context.finish()
            return {"to_char": "You can't carry that much weight.\r\n"}

        purchased = []
        current_obj = obj
        for _ in range(quantity):
            if self._is_inventory_item(current_obj):
                item = ItemUtil.create_object(current_obj)
            else:
                item = current_obj
                self._remove_keeper_item(keeper, item)
                current_obj = self._find_matching_stock_item(keeper, item)

            self._normalize_purchased_item(item, cost)
            character.add_item(item)
            purchased.append(item)

        self._deduct_money(character, total_cost)
        self._add_money(keeper, total_cost)
        context.finish()

        item_label = ItemUtil.short(obj)
        if quantity > 1:
            return {
                "to_char": f"You buy {item_label}[{quantity}] for {total_cost} silver.\r\n",
                "to_room": f"{character.name} buys {item_label}[{quantity}].\r\n",
                "targets": room.player_targets(character),
            }
        return {
            "to_char": f"You buy {item_label} for {cost} silver.\r\n",
            "to_room": f"{character.name} buys {item_label}.\r\n",
            "targets": room.player_targets(character),
        }

    def do_list(self, character: Character, context: Context):
        room = self.room_registry.get_or_none(id=character.room_id)
        raw = (context.result if isinstance(context.result, str) else "").strip().lower()
        if not raw and context.parameters:
            raw = " ".join(context.parameters).strip().lower()
        if room is None:
            context.finish()
            return {"to_char": "You can't do that here.\r\n"}

        if self._is_pet_shop(room):
            payload = self._list_pets(room)
            context.finish()
            return payload

        keeper, shop, error = self._find_keeper(character, room)
        if error:
            context.finish()
            return {"to_char": error}

        lines = []
        stock = self._keeper_visible_stock(character, keeper)
        index = 0
        while index < len(stock):
            obj = stock[index]
            cost = shop.buy_price(obj)
            if cost > 0 and (not raw or self._matches_name(obj, raw)):
                if not lines:
                    lines.append("[Lv Price Qty] Item\r\n")
                if self._is_inventory_item(obj):
                    lines.append(
                        f"[{GenericUtil.to_int(getattr(obj, 'level', 0), 0):>2} "
                        f"{cost:>5} -- ] {ItemUtil.short(obj)}\r\n"
                    )
                    index += 1
                    continue

                count = 1
                while index + count < len(stock) and self._same_stock_item(obj, stock[index + count]):
                    count += 1
                lines.append(
                    f"[{GenericUtil.to_int(getattr(obj, 'level', 0), 0):>2} "
                    f"{cost:>5} {count:>2} ] {ItemUtil.short(obj)}\r\n"
                )
                index += count
                continue
            index += 1

        context.finish()
        if not lines:
            return {"to_char": "You can't buy anything here.\r\n"}
        return {"to_char": "".join(lines)}

    def do_sell(self, character: Character, context: Context):
        room = self.room_registry.get_or_none(id=character.room_id)
        raw = (context.result if isinstance(context.result, str) else "").strip()
        if not raw and context.parameters:
            raw = " ".join(context.parameters).strip()
        if not raw:
            context.finish()
            return {"to_char": "Sell what?\r\n"}
        if room is None:
            context.finish()
            return {"to_char": "You can't do that here.\r\n"}

        keeper, shop, error = self._find_keeper(character, room)
        if error:
            context.finish()
            return {"to_char": error}

        obj = CharacterApi.find_owned_item(character, raw)
        if obj is None:
            context.finish()
            return {"to_char": "You don't have that item.\r\n"}
        if ItemUtil.is_nodrop(obj, self.item_flags):
            context.finish()
            return {"to_char": "You can't let go of it.\r\n"}

        cost = shop.sell_price(obj, getattr(keeper, "inventory", []) or [], self.item_types, self.item_flags)
        if cost <= 0:
            context.finish()
            return {"to_char": f"{getattr(keeper, 'short_description', 'The shopkeeper')} looks uninterested in {ItemUtil.short(obj)}.\r\n"}
        if self._money_value(keeper) < cost:
            context.finish()
            return {"to_char": f"I'm afraid I don't have enough wealth to buy {ItemUtil.short(obj)}.\r\n"}

        slot = character.equipped_slot_of(obj)
        if slot:
            EffectUtil.remove_item_effects(character, obj)
            character.unequip_item(slot)
        character.remove_item(obj)

        self._add_money(character, cost)
        self._deduct_money(keeper, cost)
        if self._is_trash_item(obj) or self._is_sell_extract_item(obj):
            context.finish()
            return {
                "to_char": self._sell_message(obj, cost),
                "to_room": f"{character.name} sells {ItemUtil.short(obj)}.\r\n",
                "targets": room.player_targets(character),
            }

        self._prepare_sold_item(obj)
        self._add_item_to_keeper(keeper, obj)
        context.finish()
        return {
            "to_char": self._sell_message(obj, cost),
            "to_room": f"{character.name} sells {ItemUtil.short(obj)}.\r\n",
            "targets": room.player_targets(character),
        }

    def do_value(self, character: Character, context: Context):
        room = self.room_registry.get_or_none(id=character.room_id)
        raw = (context.result if isinstance(context.result, str) else "").strip()
        if not raw and context.parameters:
            raw = " ".join(context.parameters).strip()
        if not raw:
            context.finish()
            return {"to_char": "Value what?\r\n"}
        if room is None:
            context.finish()
            return {"to_char": "You can't do that here.\r\n"}

        keeper, shop, error = self._find_keeper(character, room)
        if error:
            context.finish()
            return {"to_char": error}

        obj = CharacterApi.find_owned_item(character, raw)
        if obj is None:
            context.finish()
            return {"to_char": "You don't have that item.\r\n"}
        if ItemUtil.is_nodrop(obj, self.item_flags):
            context.finish()
            return {"to_char": "You can't let go of it.\r\n"}

        cost = shop.sell_price(obj, getattr(keeper, "inventory", []) or [], self.item_types, self.item_flags)
        context.finish()
        if cost <= 0:
            return {"to_char": f"{getattr(keeper, 'short_description', 'The shopkeeper')} looks uninterested in {ItemUtil.short(obj)}.\r\n"}

        silver = cost - (cost // 100) * 100
        gold = cost // 100
        return {"to_char": f"I'll give you {silver} silver and {gold} gold coins for {ItemUtil.short(obj)}.\r\n"}

    def do_get(self, character: Character, context: Context):
        arg1, rem = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = self.room_registry.get_or_none(id=character.room_id)
        if not arg1:
            context.finish()
            return {"to_char": "Get what?\r\n"}
        if room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}

        container = None
        if rem:
            container = ItemUtil.find_container(character, room, rem.split()[0])
            if container is None:
                context.finish()
                return {"to_char": "I see no container here.\r\n"}
            if not ItemUtil.is_container_like(container):
                context.finish()
                return {"to_char": "That's not a container.\r\n"}
            if ItemApi.is_container_closed(container):
                context.finish()
                return {"to_char": "It is closed.\r\n"}
            if arg1 == "all" or arg1.startswith("all."):
                payload = self._get_all_from_container(character, room, container, arg1)
                context.finish()
                return payload
            target_item = container.find_contained_item(arg1)
        else:
            target_item = ItemUtil.find_room_item(room, arg1)

        if target_item is None:
            context.finish()
            if container is not None:
                return {"to_char": f"I see nothing like that in {ItemUtil.short(container)}.\r\n"}
            return {"to_char": "I see nothing like that here.\r\n"}

        if not ItemUtil.item_takeable(target_item, self.wear_flags):
            context.finish()
            return {"to_char": "You can't take that.\r\n"}

        if container is not None:
            container.remove_contained_item(target_item)
        else:
            room.remove_item_from_room(target_item)
        character.add_item(target_item)
        context.finish()
        return {
            "to_char": f"You get {ItemUtil.short(target_item)}.\r\n",
            "to_room": f"{character.name} gets {ItemUtil.short(target_item)}.\r\n",
            "targets": room.player_targets(character),
        }

    def _get_all_from_container(self, character: Character, room, container, arg1: str):
        wanted = ""
        if arg1.startswith("all."):
            wanted = arg1[4:].strip().lower()

        picked = []
        for obj in list(getattr(container, "contains", []) or []):
            name = str(getattr(obj, "name", "") or "").strip().lower()
            if wanted and wanted not in name.split() and not name.startswith(wanted):
                continue
            if not ItemUtil.item_takeable(obj, self.wear_flags):
                continue
            container.remove_contained_item(obj)
            character.add_item(obj)
            picked.append(obj)

        if not picked:
            if wanted:
                return {"to_char": f"I see nothing like that in {ItemUtil.short(container)}.\r\n"}
            return {"to_char": f"I see nothing in {ItemUtil.short(container)}.\r\n"}

        return {
            "to_char": "".join(f"You get {ItemUtil.short(obj)} from {ItemUtil.short(container)}.\r\n" for obj in picked),
            "to_room": "".join(f"{character.name} gets {ItemUtil.short(obj)} from {ItemUtil.short(container)}.\r\n" for obj in picked),
            "targets": room.player_targets(character),
        }

    def do_put(self, character: Character, context: Context):
        arg1, rem = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = self.room_registry.get_or_none(id=character.room_id)
        if not arg1 or not rem:
            context.finish()
            return {"to_char": "Put what in what?\r\n"}
        if room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}

        obj = character.find_inventory_item(arg1)
        if obj is None:
            context.finish()
            return {"to_char": "You do not have that item.\r\n"}
        container = ItemUtil.find_container(character, room, rem.split()[0])
        if container is None:
            context.finish()
            return {"to_char": "I see no container here.\r\n"}
        if not ItemUtil.is_container(container):
            context.finish()
            return {"to_char": "That's not a container.\r\n"}
        if ItemApi.is_container_closed(container):
            context.finish()
            return {"to_char": "It is closed.\r\n"}
        if obj is container:
            context.finish()
            return {"to_char": "You can't fold it into itself.\r\n"}

        character.remove_item(obj)
        container.add_contained_item(obj)
        context.finish()
        return {
            "to_char": f"You put {ItemUtil.short(obj)} in {ItemUtil.short(container)}.\r\n",
            "to_room": f"{character.name} puts {ItemUtil.short(obj)} in {ItemUtil.short(container)}.\r\n",
            "targets": room.player_targets(character),
        }

    def do_drop(self, character: Character, context: Context):
        arg1, _ = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = self.room_registry.get_or_none(id=character.room_id)
        if not arg1:
            context.finish()
            return {"to_char": "Drop what?\r\n"}
        if room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}
        if arg1 == "all" or arg1.startswith("all."):
            payload = self._drop_all(character, room, arg1)
            context.finish()
            return payload
        item = character.find_inventory_item(arg1)
        if item is None:
            context.finish()
            return {"to_char": "You do not have that item.\r\n"}
        if ItemUtil.is_nodrop(item, self.item_flags):
            context.finish()
            return {"to_char": "You can't let go of it.\r\n"}

        payload = self._drop_one(character, room, item)
        context.finish()
        return payload

    def _drop_all(self, character: Character, room, arg1: str):
        wanted = arg1[4:].strip().lower() if arg1.startswith("all.") else ""
        dropped = []
        room_lines = []
        char_lines = []

        for item in list(getattr(character, "loot", []) or []):
            if character.equipped_slot_of(item):
                continue
            if ItemUtil.is_nodrop(item, self.item_flags):
                continue
            name = str(getattr(item, "name", "") or "").strip().lower()
            if wanted and wanted not in name.split() and not name.startswith(wanted):
                continue
            payload = self._drop_one(character, room, item)
            dropped.append(item)
            char_lines.append(payload.get("to_char", ""))
            room_lines.append(payload.get("to_room", ""))

        if not dropped:
            if wanted:
                return {"to_char": f"You are not carrying any {wanted}.\r\n"}
            return {"to_char": "You are not carrying anything.\r\n"}

        return {
            "to_char": "".join(char_lines),
            "to_room": "".join(room_lines),
            "targets": room.player_targets(character),
        }

    def _drop_one(self, character: Character, room, item):
        slot = character.equipped_slot_of(item)
        if slot:
            EffectUtil.remove_item_effects(character, item)
            character.unequip_item(slot)
        character.remove_item(item)

        if self._melts_on_drop(item):
            return {
                "to_char": f"You drop {ItemUtil.short(item)}.\r\n{ItemUtil.short(item)} dissolves into smoke.\r\n",
                "to_room": f"{character.name} drops {ItemUtil.short(item)}.\r\n{ItemUtil.short(item)} dissolves into smoke.\r\n",
            }

        room.add_item_to_room(item)
        return {
            "to_char": f"You drop {ItemUtil.short(item)}.\r\n",
            "to_room": f"{character.name} drops {ItemUtil.short(item)}.\r\n",
        }

    def _melts_on_drop(self, item) -> bool:
        if not hasattr(self.item_flags, "ITEM_MELT_DROP"):
            return False
        return ItemUtil.has_flag(getattr(item, "extra_flags", 0), self.item_flags.ITEM_MELT_DROP.value)

    def do_junk(self, character: Character, context: Context):
        return self.destroy_carried(character, context, "Junk what?\r\n")

    def do_sacrifice(self, character: Character, context: Context):
        arg1, _ = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = self.room_registry.get_or_none(id=character.room_id)
        if not arg1 or arg1.lower() == str(getattr(character, "name", "") or "").strip().lower():
            context.finish()
            return {
                "to_char": "Mota appreciates your offer and may accept it later.\r\n",
                "to_room": f"{character.name} offers themselves to Mota, who graciously declines.\r\n",
                "targets": room.player_targets(character),
            }

        item = ItemUtil.find_room_item(room, arg1) if room is not None else None
        if item is None:
            context.finish()
            return {"to_char": "You can't find it.\r\n"}
        if ItemUtil.is_pc_corpse(item) and list(getattr(item, "contains", []) or []):
            context.finish()
            return {"to_char": "Mota wouldn't like that.\r\n"}
        if not ItemUtil.item_takeable(item, self.wear_flags) or ItemUtil.is_nosac(item, self.item_flags):
            context.finish()
            return {"to_char": f"{ItemUtil.short(item)} is not an acceptable sacrifice.\r\n"}

        for occupant in list(getattr(room, "characters", {}).values()) + list(getattr(room, "mobiles", {}).values()) if room is not None else []:
            if getattr(occupant, "on", None) is item:
                name = getattr(occupant, "short_description", None) or getattr(occupant, "name", "Someone")
                context.finish()
                return {"to_char": f"{name} appears to be using {ItemUtil.short(item)}.\r\n"}

        silver = ItemUtil.sacrifice_silver_value(item)
        room.remove_item_from_room(item)
        character.silver = int(getattr(character, "silver", 0) or 0) + silver
        context.finish()
        return {
            "to_char": ItemUtil.sacrifice_reward_message(silver),
            "to_room": f"{character.name} sacrifices {ItemUtil.short(item)} to Mota.\r\n",
            "targets": room.player_targets(character),
        }

    def destroy_carried(self, character: Character, context: Context, empty_msg: str, success_msg: str = "Ok.\r\n"):
        arg1, _ = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        if not arg1:
            context.finish()
            return {"to_char": empty_msg}
        item = character.find_inventory_item(arg1)
        if item is None:
            context.finish()
            return {"to_char": "You do not have that item.\r\n"}
        if ItemUtil.is_nodrop(item, self.item_flags):
            context.finish()
            return {"to_char": "You can't let go of it.\r\n"}
        slot = character.equipped_slot_of(item)
        if slot:
            EffectUtil.remove_item_effects(character, item)
            character.unequip_item(slot)
        character.remove_item(item)
        context.finish()
        return {"to_char": success_msg}

    def do_give(self, character: Character, context: Context):
        arg1, rem = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = self.room_registry.get_or_none(id=character.room_id)
        if not arg1 or not rem:
            context.finish()
            return {"to_char": "Give what to whom?\r\n"}
        if room is None:
            context.finish()
            return {"to_char": "They aren't here.\r\n"}
        victim = room.find_character_in_room(rem.split()[0], Context.look_keyword_matches)
        if victim is None:
            context.finish()
            return {"to_char": "They aren't here.\r\n"}
        item = character.find_inventory_item(arg1)
        if item is None:
            context.finish()
            return {"to_char": "You do not have that item.\r\n"}
        if ItemUtil.is_nodrop(item, self.item_flags):
            context.finish()
            return {"to_char": "You can't let go of it.\r\n"}

        slot = character.equipped_slot_of(item)
        if slot:
            EffectUtil.remove_item_effects(character, item)
            character.unequip_item(slot)
        character.remove_item(item)
        victim.add_item(item)
        context.finish()
        return {
            "to_char": f"You give {ItemUtil.short(item)} to {victim.name}.\r\n",
            "to_victim": f"{character.name} gives you {ItemUtil.short(item)}.\r\n",
            "victim": victim,
            "to_room": f"{character.name} gives {ItemUtil.short(item)} to {victim.name}.\r\n",
            "targets": room.player_targets(character),
        }

    def do_wear(self, character: Character, context: Context):
        arg1, rem = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = self.room_registry.get_or_none(id=character.room_id)
        if not arg1:
            context.finish()
            return {"to_char": "Wear, wield, or hold what?\r\n"}
        if arg1 == "all":
            payload = self._wear_all(character, room)
            context.finish()
            return payload
        item = character.find_inventory_item(arg1)
        if item is None:
            context.finish()
            return {"to_char": "You do not have that item.\r\n"}
        forced_slot = rem.split()[0] if rem else ""
        invalid_msg = "You can't wear that there.\r\n" if forced_slot else "You can't wear, wield, or hold that.\r\n"
        payload = self._wear_item(character, item, room, replace=True, forced_slot=forced_slot, invalid_msg=invalid_msg)
        context.finish()
        return payload

    def do_wield(self, character: Character, context: Context):
        return self.equip_to_slot(character, context, "wielded", "Wield what?\r\n", "You can't wield that.\r\n")

    def do_hold(self, character: Character, context: Context):
        return self.equip_to_slot(character, context, "held", "Hold what?\r\n", "You can't hold that.\r\n")

    def equip_to_slot(self, character: Character, context: Context, slot: str, empty_msg: str, invalid_msg: str):
        arg1, _ = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = self.room_registry.get_or_none(id=character.room_id)
        if not arg1:
            context.finish()
            return {"to_char": empty_msg}
        item = character.find_inventory_item(arg1)
        if item is None:
            context.finish()
            return {"to_char": "You do not have that item.\r\n"}
        payload = self._wear_item(character, item, room, replace=True, preferred_slot=slot, invalid_msg=invalid_msg)
        context.finish()
        return payload

    def do_remove(self, character: Character, context: Context):
        arg1, _ = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        if not arg1:
            context.finish()
            return {"to_char": "Remove what?\r\n"}
        equipped = character.ensure_equipped()

        # Match by slot name first, then item name.
        if hasattr(equipped, arg1):
            item = character.unequip_item(arg1)
            if item is None:
                context.finish()
                return {"to_char": "You aren't wearing that.\r\n"}
            EffectUtil.remove_item_effects(character, item)
            context.finish()
            return {"to_char": f"You stop using {ItemUtil.short(item)}.\r\n"}

        for slot, item in equipped.__dict__.items():
            if item is None:
                continue
            name = (getattr(item, "name", "") or "").lower()
            if name == arg1 or name.startswith(arg1):
                EffectUtil.remove_item_effects(character, item)
                character.unequip_item(slot)
                context.finish()
                return {"to_char": f"You stop using {ItemUtil.short(item)}.\r\n"}
        context.finish()
        return {"to_char": "You aren't wearing that.\r\n"}

    def _wear_all(self, character: Character, room):
        char_lines = []
        room_lines = []

        for item in list(getattr(character, "loot", []) or []):
            payload = self._wear_item(character, item, room, replace=False)
            if not isinstance(payload, dict):
                continue
            if payload.get("to_char"):
                char_lines.append(payload["to_char"])
            if payload.get("to_room"):
                room_lines.append(payload["to_room"])

        result = {"to_char": "".join(char_lines)}
        if room_lines and room is not None:
            result["to_room"] = "".join(room_lines)
            result["targets"] = room.player_targets(character)
        return result

    def _wear_item(self, character: Character, item, room, *, replace: bool, preferred_slot: str = "",
                   forced_slot: str = "", invalid_msg: str = "You can't wear, wield, or hold that.\r\n") -> dict:
        level = GenericUtil.to_int(getattr(character, "level", 0), 0)
        item_level = GenericUtil.to_int(getattr(item, "level", 0), 0)
        if level < item_level:
            return Equipped.build_wear_payload(character, room,
                                               to_char=f"You must be level {item_level} to use this object.\r\n",
                                               to_room=f"{character.name} tries to use {ItemUtil.short(item)}, but is too inexperienced.\r\n")

        equipped = character.ensure_equipped()
        slot_groups = equipped.wear_slot_groups_for_item(item, self.wear_flags, preferred_slot=preferred_slot, forced_slot=forced_slot)
        if not slot_groups:
            return {"to_char": invalid_msg if replace else ""}

        char_lines = []
        room_lines = []
        slots = slot_groups[0]
        selected_slot, removed_payload = equipped.resolve_wear_slot(character, slots, replace, can_remove_item=self._can_remove_worn_item, remove_item=self._remove_worn_item)
        if removed_payload:
            if removed_payload.get("to_char"):
                char_lines.append(removed_payload["to_char"])
            if removed_payload.get("to_room"):
                room_lines.append(removed_payload["to_room"])
        if selected_slot is None:
            return Equipped.build_wear_payload(character, room, "".join(char_lines), "".join(room_lines) if room_lines else "")

        if selected_slot == "shield":
            weapon = getattr(getattr(character, "equipped", None), "wielded", None)
            if weapon is not None and self._character_size(character) < self._large_size_value() and item.is_two_handed_weapon():
                char_lines.append("Your hands are tied up with your weapon!\r\n")
                return Equipped.build_wear_payload(character, room, "".join(char_lines), "".join(room_lines))

        if selected_slot == "wielded":
            if item.weapon_too_heavy(character):
                char_lines.append("It is too heavy for you to wield.\r\n")
                return Equipped.build_wear_payload(character, room, "".join(char_lines), "".join(room_lines))

            shield = getattr(getattr(character, "equipped", None), "shield", None)
            if shield is not None and self._character_size(character) < self._large_size_value() and item.is_two_handed_weapon():
                char_lines.append("You need two hands free for that weapon.\r\n")
                return Equipped.build_wear_payload(character, room, "".join(char_lines), "".join(room_lines))

        character.equip_item(item, selected_slot)
        EffectUtil.apply_item_effects(character, item)
        equip_payload = equipped.slot_wear_payload(character, room, item, selected_slot)
        char_lines.append(equip_payload.get("to_char", ""))
        room_lines.append(equip_payload.get("to_room", ""))
        if selected_slot == "wielded":
            skill_feedback = self._weapon_skill_feedback(character, item)
            if skill_feedback:
                char_lines.append(skill_feedback)
        return Equipped.build_wear_payload(character, room, "".join(char_lines), "".join(room_lines))

    def _can_remove_worn_item(self, item) -> bool:
        if not hasattr(self.item_flags, "ITEM_NOREMOVE"):
            return True
        return not ItemUtil.has_flag(getattr(item, "extra_flags", 0), self.item_flags.ITEM_NOREMOVE.value)

    @staticmethod
    def _remove_worn_item(character: Character, slot: str, item) -> None:
        EffectUtil.remove_item_effects(character, item)
        character.unequip_item(slot)

    def _character_size(self, character: Character) -> int:
        direct_size = GenericUtil.to_int(getattr(character, "size", None), None)
        if direct_size is not None:
            return direct_size

        race_name = str(getattr(character, "race", "") or "").strip().lower()
        try:
            race_data = CharacterApi._pc_races_map().get(race_name, {})
        except RuntimeError:
            race_data = {}
        raw_size = race_data.get("size")
        try:
            size_enum = CharacterApi.get_enum("size")
        except RuntimeError:
            size_enum = None
        if isinstance(raw_size, str) and size_enum is not None and hasattr(size_enum, raw_size):
            return int(getattr(size_enum, raw_size).value)
        size_value = GenericUtil.to_int(raw_size, None)
        if size_value is not None:
            return size_value
        return self._large_size_value() - 1

    @staticmethod
    def _large_size_value() -> int:
        try:
            size_enum = CharacterApi.get_enum("size")
        except RuntimeError:
            size_enum = None
        if size_enum is not None and hasattr(size_enum, "SIZE_LARGE"):
            return int(size_enum.SIZE_LARGE.value)
        return 3

    @staticmethod
    def _weapon_skill_feedback(character: Character, item) -> str:
        if CharacterApi.is_npc(character):
            return ""

        try:
            weapon_class = CharacterApi.get_enum("weaponClass")
        except RuntimeError:
            weapon_class = None
        if weapon_class is None:
            return ""

        skill_map = {
            getattr(weapon_class, "WEAPON_SWORD", None): "sword",
            getattr(weapon_class, "WEAPON_DAGGER", None): "dagger",
            getattr(weapon_class, "WEAPON_SPEAR", None): "spear",
            getattr(weapon_class, "WEAPON_MACE", None): "mace",
            getattr(weapon_class, "WEAPON_AXE", None): "axe",
            getattr(weapon_class, "WEAPON_FLAIL", None): "flail",
            getattr(weapon_class, "WEAPON_WHIP", None): "whip",
            getattr(weapon_class, "WEAPON_POLEARM", None): "polearm",
        }
        class_value = GenericUtil.to_int(getattr(item, "value0", 0), 0)
        skill_name = ""
        for enum_member, name in skill_map.items():
            if enum_member is not None and class_value == int(enum_member.value):
                skill_name = name
                break
        if not skill_name:
            return ""

        skill = 0
        for entry in list(getattr(character, "skills", []) or []):
            if isinstance(entry, dict):
                entry_name = str(entry.get("name", "")).strip().lower()
                entry_level = entry.get("level", 0)
            else:
                entry_name = str(getattr(entry, "name", "")).strip().lower()
                entry_level = getattr(entry, "level", 0)
            if entry_name == skill_name:
                skill = max(0, min(100, GenericUtil.to_int(entry_level, 0)))
                break

        short = ItemUtil.short(item)
        if skill >= 100:
            return f"{short} feels like a part of you!\r\n"
        if skill > 85:
            return f"You feel quite confident with {short}.\r\n"
        if skill > 70:
            return f"You are skilled with {short}.\r\n"
        if skill > 50:
            return f"Your skill with {short} is adequate.\r\n"
        if skill > 25:
            return f"{short} feels a little clumsy in your hands.\r\n"
        if skill > 1:
            return f"You fumble and almost drop {short}.\r\n"
        return f"You don't even know which end is up on {short}.\r\n"

    @staticmethod
    def _ensure_message_break(text: str) -> str:
        rendered = str(text or "")
        if rendered and not rendered.endswith("\r\n"):
            rendered += "\r\n"
        return rendered

    @staticmethod
    def _render_command_message(context: Context, key: str, channel: str = "to_char", **tokens) -> str:
        command = getattr(context, "command", None)
        if command is None:
            return ""
        text = command.render_message(channel, key, **tokens)
        return Object._ensure_message_break(text)

    @staticmethod
    def _condition_value(character: Character, name: str) -> int:
        status_flags = getattr(character, "status_flags", None)
        if status_flags is None or not hasattr(status_flags, name):
            return -1
        return GenericUtil.to_int(getattr(status_flags, name, -1), -1)

    @staticmethod
    def _gain_condition(character: Character, name: str, amount: int) -> int:
        status_flags = getattr(character, "status_flags", None)
        if status_flags is None or not hasattr(status_flags, name):
            return -1
        current = GenericUtil.to_int(getattr(status_flags, name, -1), -1)
        if current == -1:
            return -1
        updated = max(0, min(48, current + int(amount)))
        setattr(status_flags, name, updated)
        return updated

    def do_drink(self, character: Character, context: Context):
        arg1, _ = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = getattr(context, "room", None)
        if room is None:
            room = self.room_registry.get_or_none(id=character.room_id)
        item = character.find_inventory_item(arg1) if arg1 else None
        if item is None:
            item = ItemUtil.find_room_item(room, arg1) if arg1 else None
        if item is None and not arg1:
            item = ItemUtil.first_fountain(room)
        context.drink_arg1 = arg1
        context.drink_item = item
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked

        liquid_name = str(getattr(item, "value2", "") or "")
        liquid_affect = list(getattr(item, "liquid_affect_data", []) or [])
        serving_size = GenericUtil.to_int(liquid_affect[4], 0) if len(liquid_affect) > 4 else 0
        if ItemUtil.is_fountain(item):
            amount = max(1, serving_size * 3)
        else:
            value1 = GenericUtil.to_int(getattr(item, "value1", 0), 0)
            amount = min(max(1, serving_size), value1)
            if GenericUtil.to_int(getattr(item, "value0", 0), 0) > 0:
                item.value1 = str(max(0, value1 - amount))

        tokens = {
            "c": character.name,
            "p": ItemUtil.short(item),
            "l": liquid_name,
        }
        payload = {
            "to_char": self._render_command_message(context, "default", "to_char", **tokens),
        }
        if room is not None:
            payload["to_room"] = self._render_command_message(context, "default", "to_room", **tokens)
            payload["targets"] = room.player_targets(character)

        if not CharacterApi.is_npc(character) and not CharacterApi.is_immortal(character):
            drunk_gain = (amount * GenericUtil.to_int(liquid_affect[0], 0)) // 36 if len(liquid_affect) > 0 else 0
            full_gain = (amount * GenericUtil.to_int(liquid_affect[1], 0)) // 4 if len(liquid_affect) > 1 else 0
            thirst_gain = (amount * GenericUtil.to_int(liquid_affect[2], 0)) // 10 if len(liquid_affect) > 2 else 0
            hunger_gain = (amount * GenericUtil.to_int(liquid_affect[3], 0)) // 2 if len(liquid_affect) > 3 else 0

            drunk = self._gain_condition(character, "drunk", drunk_gain)
            full = self._gain_condition(character, "hunger", full_gain)
            if hunger_gain != 0:
                full = self._gain_condition(character, "hunger", hunger_gain)
            thirst = self._gain_condition(character, "thirst", thirst_gain)

            if drunk > 10:
                payload["to_char"] += self._render_command_message(context, "alcohol")
            if full > 40:
                payload["to_char"] += self._render_command_message(context, "full")
            if thirst > 40:
                payload["to_char"] += self._render_command_message(context, "quenched")
        context.finish()
        return payload

    def do_eat(self, character: Character, context: Context):
        arg1, _ = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        item = character.find_inventory_item(arg1)
        context.eat_arg1 = arg1
        context.eat_item = item
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked

        item_type = (getattr(item, "item_type", "") or "").upper()
        payload = {
            "to_char": self._render_command_message(context, "default", "to_char", p=ItemUtil.short(item)),
        }
        room = self.room_registry.get_or_none(id=character.room_id)
        if room is not None:
            payload["to_room"] = self._render_command_message(context, "default", "to_room", c=character.name, p=ItemUtil.short(item))
            payload["targets"] = room.player_targets(character)

        if "FOOD" in item_type and not CharacterApi.is_npc(character):
            hunger_before = self._condition_value(character, "hunger")
            hunger_after = self._gain_condition(character, "hunger", GenericUtil.to_int(getattr(item, "value1", 0), 0))
            self._gain_condition(character, "hunger", GenericUtil.to_int(getattr(item, "value0", 0), 0))
            if hunger_before == 0 and hunger_after > 0:
                payload["to_char"] += self._render_command_message(context, "satiated")
            elif self._condition_value(character, "hunger") > 40:
                payload["to_char"] += self._render_command_message(context, "full")

        slot = character.equipped_slot_of(item)
        if slot:
            EffectUtil.remove_item_effects(character, item)
            character.unequip_item(slot)
        character.remove_item(item)
        context.finish()
        return payload

    def do_fill(self, character: Character, context: Context):
        arg1, rem = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = self.room_registry.get_or_none(id=character.room_id)
        dest = character.find_inventory_item(arg1)
        src_name = rem.split()[0] if rem else ""
        src = ItemUtil.find_container(character, room, src_name) if src_name else None
        if src is None:
            # fallback to first fountain in room
            src = ItemUtil.first_fountain(room)
        context.fill_arg1 = arg1
        context.fill_dest = dest
        context.fill_src = src
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked

        if src is None:
            context.finish()
            return {"to_char": "There is no source of liquid here.\r\n"}
        if ItemUtil.is_fountain(dest) or not ItemUtil.is_drink_container(dest) or not ItemUtil.is_drink_container(src):
            context.finish()
            return {"to_char": "You can't fill that.\r\n"}

        dest_cap = GenericUtil.to_int(getattr(dest, "value0", 0), 0)
        dest_amt = GenericUtil.to_int(getattr(dest, "value1", 0), 0)
        if dest_cap > 0 and dest_amt >= dest_cap:
            context.finish()
            return {"to_char": "Your container is full.\r\n"}

        src_liquid = str(getattr(src, "value2", "") or "")
        if dest_amt > 0 and src_liquid and str(getattr(dest, "value2", "") or "") != src_liquid:
            context.finish()
            return {"to_char": "There is already another liquid in it.\r\n"}

        if not ItemUtil.is_fountain(src):
            src_amt = GenericUtil.to_int(getattr(src, "value1", 0), 0)
            if src_amt <= 0:
                context.finish()
                return {"to_char": "It is empty.\r\n"}

        if src_liquid:
            dest.value2 = src_liquid
        dest.value1 = str(dest_cap if dest_cap > 0 else GenericUtil.to_int(getattr(src, "value1", 0), 0))
        context.finish()
        payload = {
            "to_char": self._render_command_message(
                context,
                "default",
                "to_char",
                t=ItemUtil.short(dest),
                s=src_liquid,
                T=ItemUtil.short(src),
            ),
        }
        if room is not None:
            payload["to_room"] = self._render_command_message(
                context,
                "default",
                "to_room",
                c=character.name,
                t=ItemUtil.short(dest),
                s=src_liquid,
                T=ItemUtil.short(src),
            )
            payload["targets"] = room.player_targets(character)
        return payload

    def do_pour(self, character: Character, context: Context):
        context.finish()
        return {"to_char": "Pour is not implemented yet.\r\n"}

    def do_quaff(self, character: Character, context: Context):
        context.finish()
        return {"to_char": "Quaff is not implemented yet.\r\n"}

    def do_recite(self, character: Character, context: Context):
        context.finish()
        return {"to_char": "Recite is not implemented yet.\r\n"}

    def do_brandish(self, character: Character, context: Context):
        context.finish()
        return {"to_char": "Brandish is not implemented yet.\r\n"}

    def do_zap(self, character: Character, context: Context):
        context.finish()
        return {"to_char": "Zap is not implemented yet.\r\n"}

    def _find_keeper(self, character: Character, room):
        if self.shop_registry is None:
            return None, None, "You can't do that here.\r\n"
        for mob in room.mobiles.values():
            shop = self.shop_registry.find_by_keeper_vnum(getattr(mob, "vnum", ""))
            if shop is None:
                continue
            hour = GenericUtil.to_int(getattr(getattr(self.weather_handler, "time_info", None), "hour", -1), -1)
            if not shop.is_open_at(hour):
                if hour < GenericUtil.to_int(shop.open_hour, 0):
                    return None, None, "Sorry, I am closed. Come back later.\r\n"
                return None, None, "Sorry, I am closed. Come back tomorrow.\r\n"
            if not CharacterApi.can_see(mob, character, room):
                return None, None, "I don't trade with folks I can't see.\r\n"
            return mob, shop, ""
        return None, None, "You can't do that here.\r\n"

    def _is_pet_shop(self, room) -> bool:
        if room is None or self.room_flags is None or not hasattr(self.room_flags, "ROOM_PET_SHOP"):
            return False
        return ItemUtil.has_flag(getattr(room, "room_flags", 0), self.room_flags.ROOM_PET_SHOP.value)

    def _list_pets(self, room):
        stock_room = self._pet_stock_room(room)
        if stock_room is None:
            return {"to_char": "You can't do that here.\r\n"}

        pet_bit = CharacterApi.enum_bit(self.act_bits, "ACT_PET")
        lines = []
        for pet in stock_room.mobiles.values():
            if pet_bit and not CharacterApi.is_set(GenericUtil.to_int(getattr(getattr(pet, "status_flags", None), "act", 0), 0), pet_bit):
                continue
            level = GenericUtil.to_int(getattr(pet, "level", 0), 0)
            cost = 10 * level * level
            if not lines:
                lines.append("Pets for sale:\r\n")
            lines.append(f"[{level:>2}] {cost:>8} - {getattr(pet, 'short_description', 'a pet')}\r\n")

        if not lines:
            return {"to_char": "Sorry, we're out of pets right now.\r\n"}
        return {"to_char": "".join(lines)}

    def _buy_pet(self, character: Character, room, raw: str):
        if CharacterApi.is_npc(character):
            return {"to_char": "You can't do that here.\r\n"}

        selector, pet_name = InterpUtil.one_argument(raw)
        stock_room = self._pet_stock_room(room)
        if stock_room is None:
            return {"to_char": "Sorry, you can't buy that here.\r\n"}

        pet_proto = self._find_pet(stock_room, selector)
        if pet_proto is None:
            return {"to_char": "Sorry, you can't buy that here.\r\n"}
        if getattr(character, "pet", None) is not None:
            return {"to_char": "You already own a pet.\r\n"}

        cost = 10 * GenericUtil.to_int(getattr(pet_proto, "level", 0), 0) ** 2
        if not self._can_afford(character, cost):
            return {"to_char": "You can't afford it.\r\n"}
        if GenericUtil.to_int(getattr(character, "level", 0), 0) < GenericUtil.to_int(getattr(pet_proto, "level", 0), 0):
            return {"to_char": "You're not powerful enough to master this pet.\r\n"}

        pet = MobileUtil.create_mobile(pet_proto, CharacterApi._enums_map())
        pet_bit = CharacterApi.enum_bit(self.act_bits, "ACT_PET")
        charm_bit = CharacterApi.enum_bit(self.affected_bits, "AFF_CHARM")
        if pet_bit:
            pet.status_flags.act = CharacterApi.set_bit(GenericUtil.to_int(getattr(pet.status_flags, "act", 0), 0), pet_bit)
        if charm_bit:
            pet.status_flags.affected_by = CharacterApi.set_bit(GenericUtil.to_int(getattr(pet.status_flags, "affected_by", 0), 0), charm_bit)

        for comm_name in ("COMM_NOTELL", "COMM_NOSHOUT", "COMM_NOCHANNELS"):
            bit = CharacterApi.enum_bit(self.comm_flags, comm_name)
            if bit:
                pet.status_flags.comm = CharacterApi.set_bit(GenericUtil.to_int(getattr(pet.status_flags, "comm", 0), 0), bit)

        if pet_name:
            pet.name = f"{pet.name} {pet_name}".strip()
        pet.description = f"{getattr(pet, 'description', '')}A neck tag says 'I belong to {character.name}'.\r\n"
        room.add_mobile_to_room(pet)
        pet.leader = character
        character.pet = pet
        self._deduct_money(character, cost)
        return {
            "to_char": "Enjoy your pet.\r\n",
            "to_room": f"{character.name} bought {getattr(pet, 'short_description', 'a pet')} as a pet.\r\n",
            "targets": room.player_targets(character),
        }

    def _pet_stock_room(self, room):
        current_vnum = GenericUtil.to_int(getattr(room, "vnum", 0), 0)
        next_vnum = 9706 if current_vnum == 9621 else current_vnum + 1
        return self.room_registry.get_or_none(vnum=str(next_vnum))

    def _find_pet(self, stock_room, selector: str):
        number, keyword = InterpUtil.number_argument(selector)
        pet_bit = CharacterApi.enum_bit(self.act_bits, "ACT_PET")
        count = 0
        for pet in stock_room.mobiles.values():
            if pet_bit and not CharacterApi.is_set(GenericUtil.to_int(getattr(getattr(pet, "status_flags", None), "act", 0), 0), pet_bit):
                continue
            if not self._matches_name(pet, keyword):
                continue
            count += 1
            if count == number:
                return pet
        return None

    def _mult_argument(self, argument: str) -> tuple[int, str]:
        text = str(argument or "").strip()
        if "*" not in text:
            return 1, text
        count_text, remainder = text.split("*", 1)
        count = GenericUtil.to_int(count_text, 1)
        return max(1, count), remainder.strip()

    def _keeper_visible_stock(self, character: Character, keeper) -> list:
        stock = []
        room = self.room_registry.get(id=character.room_id)
        for item in list(getattr(keeper, "inventory", []) or []):
            if self._is_item_worn(item):
                continue
            if not ItemUtil.can_see_object(room, character, item):
                continue
            stock.append(item)
        return stock

    def _get_keeper_stock_item(self, character: Character, keeper, selector: str) -> Item:
        number, keyword = InterpUtil.number_argument(selector)
        count = 0
        stock = self._keeper_visible_stock(character, keeper)
        index = 0
        while index < len(stock):
            item = stock[index]
            if self._matches_name(item, keyword):
                count += 1
                if count == number:
                    return item
                while index + 1 < len(stock) and self._same_stock_item(item, stock[index + 1]):
                    index += 1
            index += 1
        return None

    def _available_stock_quantity(self, keeper, item) -> int:
        count = 0
        matched = False
        for stocked in list(getattr(keeper, "inventory", []) or []):
            if self._is_item_worn(stocked):
                continue
            if not matched:
                matched = stocked is item
            if not matched:
                continue
            if not self._same_stock_item(item, stocked):
                break
            count += 1
        return count

    def _find_matching_stock_item(self, keeper, wanted):
        for stocked in list(getattr(keeper, "inventory", []) or []):
            if self._is_item_worn(stocked):
                continue
            if self._same_stock_item(wanted, stocked):
                return stocked
        return wanted

    def _remove_keeper_item(self, keeper, item):
        inventory = getattr(keeper, "inventory", None)
        if inventory is None:
            return
        try:
            inventory.remove(item)
        except ValueError:
            return

    def _add_item_to_keeper(self, keeper, item):
        inventory = getattr(keeper, "inventory", None)
        if inventory is None:
            keeper.inventory = []
            inventory = keeper.inventory

        for index, stocked in enumerate(list(inventory)):
            if not self._same_stock_item(item, stocked):
                continue
            if self._is_inventory_item(stocked):
                return None
            item.cost = GenericUtil.to_int(getattr(stocked, "cost", getattr(item, "cost", 0)), 0)
            inventory.insert(index + 1, item)
            return item
        inventory.insert(0, item)
        return item

    def _normalize_purchased_item(self, item, cost: int):
        if GenericUtil.to_int(getattr(item, "timer", 0), 0) > 0 and not self._had_timer(item):
            item.timer = 0
        item.extra_flags = CharacterApi.unset_bit(GenericUtil.to_int(getattr(item, "extra_flags", 0), 0), CharacterApi.enum_bit(self.item_flags, "ITEM_HAD_TIMER"))
        if GenericUtil.to_int(getattr(item, "cost", 0), 0) > cost:
            item.cost = cost
        if hasattr(item, "wear_loc"):
            item.wear_loc = -1

    def _prepare_sold_item(self, item):
        if GenericUtil.to_int(getattr(item, "timer", 0), 0) > 0:
            had_timer = CharacterApi.enum_bit(self.item_flags, "ITEM_HAD_TIMER")
            item.extra_flags = CharacterApi.set_bit(GenericUtil.to_int(getattr(item, "extra_flags", 0), 0), had_timer)
        else:
            item.timer = self._timer_roll()
        if hasattr(item, "wear_loc"):
            item.wear_loc = -1

    def _timer_roll(self) -> int:
        from game.RandomNumberGenerator import RandomNumberGenerator
        return RandomNumberGenerator().number_range(50, 100)

    def _had_timer(self, item) -> bool:
        bit = CharacterApi.enum_bit(self.item_flags, "ITEM_HAD_TIMER")
        return bit != 0 and ItemUtil.has_flag(getattr(item, "extra_flags", 0), bit)

    def _is_inventory_item(self, item) -> bool:
        bit = CharacterApi.enum_bit(self.item_flags, "ITEM_INVENTORY")
        return bit != 0 and ItemUtil.has_flag(getattr(item, "extra_flags", 0), bit)

    def _is_sell_extract_item(self, item) -> bool:
        bit = CharacterApi.enum_bit(self.item_flags, "ITEM_SELL_EXTRACT")
        return bit != 0 and ItemUtil.has_flag(getattr(item, "extra_flags", 0), bit)

    @staticmethod
    def _is_trash_item(item) -> bool:
        return str(getattr(item, "item_type", "") or "").strip().upper() == "ITEM_TRASH"

    @staticmethod
    def _is_item_worn(item) -> bool:
        wear_loc = GenericUtil.to_int(getattr(item, "wear_loc", -1), -1)
        return wear_loc >= 0

    @staticmethod
    def _same_stock_item(left, right) -> bool:
        return (
            left is not None
            and right is not None
            and str(getattr(left, "vnum", "") or "") == str(getattr(right, "vnum", "") or "")
            and str(getattr(left, "short_description", "") or "") == str(getattr(right, "short_description", "") or "")
        )

    @staticmethod
    def _matches_name(entity, wanted: str) -> bool:
        query = str(wanted or "").strip().lower()
        if not query:
            return True
        name = str(getattr(entity, "name", "") or "").strip().lower()
        words = [word for word in name.split() if word]
        return name == query or name.startswith(query) or query in words or any(word.startswith(query) for word in words)

    @staticmethod
    def _money_value(entity) -> int:
        return (GenericUtil.to_int(getattr(entity, "gold", 0), 0) * 100) + GenericUtil.to_int(getattr(entity, "silver", 0), 0)

    def _can_afford(self, entity, amount: int) -> bool:
        return self._money_value(entity) >= GenericUtil.to_int(amount, 0)

    @staticmethod
    def _add_money(entity, amount: int):
        total = (GenericUtil.to_int(getattr(entity, "gold", 0), 0) * 100) + GenericUtil.to_int(getattr(entity, "silver", 0), 0)
        total += GenericUtil.to_int(amount, 0)
        entity.gold = total // 100
        entity.silver = total - (entity.gold * 100)

    @staticmethod
    def _deduct_money(entity, amount: int):
        total = (GenericUtil.to_int(getattr(entity, "gold", 0), 0) * 100) + GenericUtil.to_int(getattr(entity, "silver", 0), 0)
        total = max(0, total - GenericUtil.to_int(amount, 0))
        entity.gold = total // 100
        entity.silver = total - (entity.gold * 100)

    @staticmethod
    def _carry_count(character: Character) -> int:
        return len(CharacterApi.owned_items(character))

    @staticmethod
    def _carry_weight(character: Character) -> int:
        item_weight = sum(GenericUtil.to_int(getattr(item, "weight", 0), 0) for item in CharacterApi.owned_items(character))
        coin_weight = int((GenericUtil.to_int(character.silver, 0) / 10) + (GenericUtil.to_int(character.gold, 0) * 2 / 5))
        return item_weight + coin_weight

    @staticmethod
    def _max_items(character: Character) -> int:
        return GenericUtil.to_int(getattr(getattr(character, "character_attributes", None), "max_items", 0), 0)

    @staticmethod
    def _max_weight(character: Character) -> int:
        return GenericUtil.to_int(getattr(getattr(character, "character_attributes", None), "max_weight", 0), 0)

    @staticmethod
    def _sell_message(item, cost: int) -> str:
        silver = cost - (cost // 100) * 100
        gold = cost // 100
        suffix = "" if cost == 1 else "s"
        return f"You sell {ItemUtil.short(item)} for {silver} silver and {gold} gold piece{suffix}.\r\n"
