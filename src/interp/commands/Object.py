from __future__ import annotations

import random

from injector import inject

from api.GameApi import GameApi
from area.Shop import Shop
from fight.FightHandler import FightHandler
from game.EnumProvider import EnumProvider
from game.Equipped import Equipped
from item.EffectHandler import EffectHandler
from util.GenericUtil import GenericUtil
from game.RegistryService import RegistryService
from interp.Context import Context
from util.InfoUtil import InfoUtil
from util.InterpUtil import InterpUtil
from util.EffectUtil import EffectUtil
from util.ItemUtil import ItemUtil
from api.InterpApi import InterpApi
from api.ItemApi import ItemApi
from api.SpellApi import SpellApi
from player.Character import Character
from item.Item import Item
from api.CharacterApi import CharacterApi
from server.LoggerFactory import LoggerFactory
from skill.Ability import Ability
from skill.SpellContext import SpellContext
from util.FightUtil import FightUtil
from util.CommunicationsUtil import CommunicationsUtil
from util.PlayerUtil import PlayerUtil


class Object:
    @inject
    def __init__(self, registry_service: RegistryService,
                 enum_provider: EnumProvider,
                 weather_handler=None,
                 interp_api=None,
                 spell_api=None,
                 fight_handler: FightHandler = None,
                 effect_handler: EffectHandler = None):
        self.__name__ = "Object"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry_service = registry_service
        self.room_registry = getattr(registry_service, "room_registry", None)
        self.mobile_registry = getattr(registry_service, "mobile_registry", None)
        self.shop_registry = getattr(registry_service, "shop_registry", None)
        self.skill_registry = getattr(registry_service, "skill_registry", None)
        self.spell_registry = getattr(registry_service, "spell_registry", None)
        self.weather_handler = weather_handler
        self.interp_api = interp_api or InterpApi()
        self.effect_handler = effect_handler or EffectUtil.handler()
        self.spell_api = spell_api or SpellApi(effect_handler=self.effect_handler)
        self.fight_handler = fight_handler
        self.item_types = enum_provider.get("itemTypes")
        self.item_flags = enum_provider.get("itemFlags")
        self.wear_flags = enum_provider.get("wearFlags")
        self.room_flags = enum_provider.get("roomFlags")
        self.act_bits = enum_provider.get("actBits")
        self.affected_bits = enum_provider.get("affectedBy")
        self.comm_flags = enum_provider.get("commFlags")

    def execute(self, character: Character, context: Context):
        name = (getattr(context.command, "name", "") or "").strip().lower()
        handlers = {
            "get": self.do_get,
            "take": self.do_get,
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
        room = self._prepare_buy_context(character, context)
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            context.finish()
            return blocked

        if context.buy_is_pet_shop:
            payload = self._finish_buy_pet(character, room, context)
        else:
            payload = self._finish_buy_item(character, room, context)

        context.finish()
        return payload

    def do_list(self, character: Character, context: Context):
        room = self._prepare_list_context(character, context)
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            context.finish()
            return blocked

        if context.list_is_pet_shop:
            payload = Shop.list_pets(room, self.room_registry, self.act_bits)
            context.finish()
            return payload

        payload = context.list_shop.list_inventory(
            context.list_keeper,
            room,
            character,
            item_flags=self.item_flags,
            wanted=context.list_filter,
        )
        context.finish()
        return payload

    def _prepare_list_context(self, character: Character, context: Context):
        room = context.room if context.room is not None else self.room_registry.get_or_none(id=character.room_id)
        raw = (context.result if isinstance(context.result, str) else "").strip().lower()
        if not raw and context.parameters:
            raw = " ".join(context.parameters).strip().lower()

        context.room = room
        context.list_filter = raw
        context.list_is_pet_shop = Shop.is_pet_shop(room, self.room_flags)
        context.list_keeper = None
        context.list_shop = None
        context.list_keeper_error = ""
        if room is not None and not context.list_is_pet_shop:
            context.list_keeper, context.list_shop, context.list_keeper_error = self._find_keeper(character, room)
        return room

    def do_sell(self, character: Character, context: Context):
        room = self._prepare_sell_context(character, context)
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            context.finish()
            return blocked

        context.sell_shop.complete_sale(character, context.sell_keeper, context.sell_obj, context.sell_cost, self.item_flags, effect_handler=self.effect_handler)

        payload = self._sell_success_payload(character, room, context)
        context.finish()
        return payload

    def do_value(self, character: Character, context: Context):
        self._prepare_value_context(character, context)
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            context.finish()
            return blocked

        context.finish()
        return self.interp_api.render_message_key(
            context,
            "default",
            q=context.value_silver,
            g=context.value_gold,
            t=context.value_item_short,
        )

    def do_get(self, character: Character, context: Context):
        room = self._prepare_get_context(character, context)
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            context.finish()
            return blocked

        if context.get_all:
            payload = self._get_many(character, room, context, context.get_candidates, context.container)
        else:
            payload = self._get_one(character, room, context, context.target_item, context.container)

        context.finish()
        return payload

    def _prepare_get_context(self, character: Character, context: Context):
        arg1, rem = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = getattr(context, "room", None)
        if room is None:
            room = self.room_registry.get_or_none(id=character.room_id)

        context.room = room
        context.arg1 = arg1
        context.rem = rem
        context.container_name = rem.split()[0] if rem else ""
        context.get_all = self._is_get_all_selector(arg1)
        context.get_filter_name = self._get_selector_filter(arg1)
        context.get_all_from_container = bool(context.get_all and context.container_name)
        context.container = character.find_inventory_item(context.container_name) or (None if room is None else room.find_room_item(context.container_name)) if context.container_name else None
        context.target_item = None
        context.get_candidates = []
        context.get_item_takeable = False

        if context.container is not None:
            if context.get_all:
                context.get_candidates = self._get_matching_container_items(character, room, context.container, context.get_filter_name)
            else:
                context.target_item = context.container.find_contained_item(arg1) if hasattr(context.container, "find_contained_item") else None
        elif not context.container_name:
            if context.get_all:
                context.get_candidates = self._get_matching_room_items(character, room, context.get_filter_name)
            else:
                context.target_item = room.find_room_item(arg1)

        if context.target_item is not None:
            context.get_item_takeable = ItemApi.item_takeable(context.target_item, self.wear_flags)
        return room

    def _get_matching_room_items(self, character: Character, room, wanted: str) -> list:
        if room is None:
            return []
        matches = []
        for obj in list(getattr(room, "contents", {}).values()):
            if not self._matches_name(obj, wanted):
                continue
            if not ItemUtil.can_see_object(room, character, obj):
                continue
            matches.append(obj)
        return matches

    def _get_matching_container_items(self, character: Character, room, container, wanted: str) -> list:
        matches = []
        for obj in list(getattr(container, "contains", []) or []):
            if not self._matches_name(obj, wanted):
                continue
            if room is not None and not ItemUtil.can_see_object(room, character, obj):
                continue
            matches.append(obj)
        return matches

    def _get_many(self, character: Character, room, context: Context, items: list, container=None):
        char_lines = []
        room_lines = []
        moved_any = False

        for obj in list(items or []):
            payload = self._get_one(character, room, context, obj, container)
            if payload.get("to_char"):
                char_lines.append(payload["to_char"])
            if payload.get("to_room"):
                room_lines.append(payload["to_room"])
                moved_any = True

        result = {"to_char": "".join(char_lines)}
        if moved_any and room is not None:
            result["to_room"] = "".join(room_lines)
            result["targets"] = room.player_targets(character)
        return result

    def _get_one(self, character: Character, room, context: Context, item, container=None):
        error = self._get_item_error(character, context, item)
        if error:
            return {"to_char": error}

        item_short = Item.short(item)
        if container is not None:
            container.remove_contained_item(item)
            container_short = Item.short(container)
            to_char = self._render_command_message(context, "from_container", t=item_short, T=container_short)
            to_room = self._render_command_message(context, "from_container", channel="to_room", c=character.name, t=item_short, T=container_short)
        else:
            if room is not None:
                room.remove_item_from_room(item)
            to_char = self._render_command_message(context, "default", t=item_short)
            to_room = self._render_command_message(context, "default", channel="to_room", c=character.name, t=item_short)

        character.add_item(item)
        payload = {"to_char": to_char}
        if room is not None:
            payload["to_room"] = to_room
            payload["targets"] = room.player_targets(character)
        return payload

    def _get_item_error(self, character: Character, context: Context, item) -> str:
        if item is None:
            return ""
        item_short = Item.short(item)
        if not ItemApi.item_takeable(item, self.wear_flags):
            return self._render_command_message(context, "cannot_take", t=item_short)

        max_items = character.max_items()
        if max_items > 0 and character.carry_count() + 1 > max_items:
            return self._render_command_message(context, "carry_items", t=item_short)

        max_weight = character.max_weight()
        item_weight = GenericUtil.to_int(getattr(item, "weight", 0), 0)
        if max_weight > 0 and character.carry_weight() + item_weight > max_weight:
            return self._render_command_message(context, "carry_weight", t=item_short)
        return ""

    @staticmethod
    def _is_get_all_selector(arg1: str) -> bool:
        selector = str(arg1 or "").strip().lower()
        return selector == "all" or selector.startswith("all.")

    @staticmethod
    def _get_selector_filter(arg1: str) -> str:
        selector = str(arg1 or "").strip().lower()
        if selector.startswith("all."):
            return selector[4:].strip()
        return ""

    def do_put(self, character: Character, context: Context):
        room = self._prepare_put_context(character, context)
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            context.finish()
            return blocked

        error = self._put_item_error(context.put_obj, context)
        if error:
            context.finish()
            return {"to_char": error}

        character.remove_item(context.put_obj)
        context.put_container.add_contained_item(context.put_obj)
        context.finish()
        key = "on" if context.put_relation == "on" else "in"
        return {
            "to_char": self._render_command_message(
                context,
                key,
                t=Item.short(context.put_obj),
                T=Item.short(context.put_container),
            ),
            "to_room": self._render_command_message(
                context,
                key,
                channel="to_room",
                c=character.name,
                t=Item.short(context.put_obj),
                T=Item.short(context.put_container),
            ),
            "targets": room.player_targets(character),
        }

    def _prepare_put_context(self, character: Character, context: Context):
        arg1, rem = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = getattr(context, "room", None)
        if room is None:
            room = self.room_registry.get_or_none(id=character.room_id)

        context.room = room
        context.put_room = room
        context.put_arg1 = arg1
        context.put_rem = rem
        context.put_relation = self._put_relation(context)
        context.put_container_name = rem.split()[0] if rem else ""
        context.put_obj = character.find_inventory_item(arg1) if arg1 else None
        context.put_container = character.find_inventory_item(context.put_container_name) or (None if room is None else room.find_room_item(context.put_container_name)) if context.put_container_name else None
        return room

    def _put_item_error(self, item, context: Context) -> str:
        if item is None:
            return ""
        if ItemApi.has_item_flag(item, self.item_flags, "ITEM_NODROP"):
            return self._render_command_message(context, "target_no_drop", t=Item.short(item))
        return ""

    @staticmethod
    def _put_relation(context: Context) -> str:
        raw = (context.result if isinstance(context.result, str) else "").strip()
        if not raw:
            raw = " ".join(getattr(context, "parameters", []) or []).strip()
        _arg1, rest = InterpUtil.one_argument(raw)
        prep, _tail = InterpUtil.one_argument(rest)
        return "on" if prep.strip().lower() == "on" else "in"

    def do_drop(self, character: Character, context: Context):
        room = self._prepare_drop_context(character, context)
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            context.finish()
            return blocked

        if context.drop_all:
            payload = self._drop_all(character, room, context, context.arg1)
        else:
            payload = self._drop_one(character, room, context, context.drop_item)
        context.finish()
        return payload

    def _prepare_drop_context(self, character: Character, context: Context):
        arg1, _ = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = getattr(context, "room", None)
        if room is None:
            room = self.room_registry.get_or_none(id=character.room_id)

        context.arg1 = arg1
        context.drop_room = room
        context.drop_all = arg1 == "all" or arg1.startswith("all.")
        context.drop_item = None if context.drop_all or not arg1 else character.find_inventory_item(arg1)
        context.drop_no_drop = bool(context.drop_item is not None and ItemApi.has_item_flag(context.drop_item, self.item_flags, "ITEM_NODROP"))
        return room

    def _drop_all(self, character: Character, room, context: Context, arg1: str):
        wanted = arg1[4:].strip().lower() if arg1.startswith("all.") else ""
        dropped = []
        room_lines = []
        char_lines = []

        for item in list(getattr(character, "loot", []) or []):
            if character.equipped_slot_of(item):
                continue
            if ItemApi.has_item_flag(item, self.item_flags, "ITEM_NODROP"):
                continue
            name = str(getattr(item, "name", "") or "").strip().lower()
            if wanted and wanted not in name.split() and not name.startswith(wanted):
                continue
            payload = self._drop_one(character, room, context, item)
            dropped.append(item)
            char_lines.append(payload.get("to_char", ""))
            room_lines.append(payload.get("to_room", ""))

        if not dropped:
            if wanted:
                return {"to_char": self._render_command_message(context, "target_not_found", t=wanted)}
            return {"to_char": self._render_command_message(context, "no_inventory")}

        return {
            "to_char": "".join(char_lines),
            "to_room": "".join(room_lines),
            "targets": room.player_targets(character),
        }

    def _drop_one(self, character: Character, room, context: Context, item):
        slot = character.equipped_slot_of(item)
        if slot:
            self.effect_handler.remove_item_effects(character, item)
            ItemUtil.unequip_item(character, slot)
        character.remove_item(item)

        item_short = Item.short(item)
        if self._melts_on_drop(item):
            return {
                "to_char": self._render_command_message(context, "default", t=item_short)
                + self._render_command_message(context, "dissolved", t=item_short),
                "to_room": self._render_command_message(context, "default", channel="to_room", c=character.name, t=item_short)
                + self._render_command_message(context, "dissolved", channel="to_room", t=item_short),
            }

        room.add_item_to_room(item)
        return {
            "to_char": self._render_command_message(context, "default", t=item_short),
            "to_room": self._render_command_message(context, "default", channel="to_room", c=character.name, t=item_short),
        }

    def _melts_on_drop(self, item) -> bool:
        if not hasattr(self.item_flags, "ITEM_MELT_DROP"):
            return False
        return GameApi.is_set(getattr(item, "extra_flags", 0), self.item_flags.ITEM_MELT_DROP.value)

    def _prepare_buy_context(self, character: Character, context: Context):
        raw = (context.result if isinstance(context.result, str) else "").strip()
        if not raw and context.parameters:
            raw = " ".join(context.parameters).strip()
        room = getattr(context, "room", None)
        if room is None:
            room = self.room_registry.get_or_none(id=character.room_id)

        context.room = room
        context.buy_raw = raw
        context.buy_room = room
        context.buy_is_pet_shop = Shop.is_pet_shop(room, self.room_flags)
        context.buy_keeper = None
        context.buy_shop = None
        context.buy_keeper_error = ""
        context.buy_quantity = 1
        context.buy_selector = ""
        context.buy_item = None
        context.buy_item_short = ""
        context.buy_cost = 0
        context.buy_total_cost = 0
        context.buy_available = 0
        context.buy_stock_limited = False
        context.buy_pet_name = ""
        context.buy_pet_proto = None

        if not raw or room is None:
            return room

        if context.buy_is_pet_shop:
            selector, pet_name = InterpUtil.one_argument(raw)
            stock_room = Shop.pet_stock_room(room, self.room_registry)
            pet_proto = Shop.find_pet(stock_room, selector, self.act_bits)
            context.buy_selector = selector
            context.buy_pet_name = pet_name
            context.buy_pet_proto = pet_proto
            context.buy_item = pet_proto
            context.buy_item_short = getattr(pet_proto, "short_description", "a pet") if pet_proto is not None else ""
            context.buy_cost = Shop.pet_price(pet_proto)
            context.buy_total_cost = context.buy_cost
            return room

        keeper, shop, error = self._find_keeper(character, room)
        context.buy_keeper = keeper
        context.buy_shop = shop
        context.buy_keeper_error = error
        quantity, selector = self._mult_argument(raw)
        context.buy_quantity = quantity
        context.buy_selector = selector
        if keeper is None or shop is None:
            return room

        obj = shop.get_keeper_stock_item(keeper, room, character, selector)
        cost = 0 if obj is None else shop.buy_price(obj)
        context.buy_item = obj
        context.buy_item_short = "" if obj is None else Item.short(obj)
        context.buy_cost = cost
        context.buy_total_cost = cost * max(0, quantity)
        context.buy_stock_limited = bool(obj is not None and not shop.is_inventory_item(obj, self.item_flags))
        if context.buy_stock_limited:
            context.buy_available = shop.available_stock_quantity(keeper, obj)
        return room

    def _finish_buy_item(self, character: Character, room, context: Context):
        context.buy_shop.complete_purchase(
            character,
            context.buy_keeper,
            context.buy_item,
            context.buy_quantity,
            context.buy_cost,
            self.item_flags,
        )
        if context.buy_quantity > 1:
            return {
                "to_char": self._render_command_message(context, "bulk_purchased", t=context.buy_item_short, d=context.buy_quantity, q=context.buy_total_cost),
                "to_room": self._render_command_message(context, "bulk_purchased", channel="to_room", c=character.name, t=context.buy_item_short, d=context.buy_quantity),
                "targets": room.player_targets(character),
            }
        return {
            "to_char": self._render_command_message(context, "default", t=context.buy_item_short, q=context.buy_cost),
            "to_room": self._render_command_message(context, "item_purchased", channel="to_room", c=character.name, t=context.buy_item_short),
            "targets": room.player_targets(character),
        }

    def _finish_buy_pet(self, character: Character, room, context: Context):
        pet = Shop.complete_pet_purchase(
            character,
            room,
            context.buy_pet_proto,
            context.buy_pet_name,
            context.buy_cost,
            self.act_bits,
            self.affected_bits,
            self.comm_flags,
        )
        return {
            "to_char": self._render_command_message(context, "pet_purchased"),
            "to_room": self._render_command_message(context, "pet_purchased", channel="to_room", c=character.name, t=getattr(pet, "short_description", "a pet")),
            "targets": room.player_targets(character),
        }

    def _prepare_sell_context(self, character: Character, context: Context):
        raw = (context.result if isinstance(context.result, str) else "").strip()
        if not raw and context.parameters:
            raw = " ".join(context.parameters).strip()
        room = getattr(context, "room", None)
        if room is None:
            room = self.room_registry.get_or_none(id=character.room_id)

        context.room = room
        context.sell_raw = raw
        context.sell_room = room
        context.sell_keeper = None
        context.sell_shop = None
        context.sell_keeper_error = ""
        context.sell_obj = None
        context.sell_item_short = ""
        context.sell_keeper_short = ""
        context.sell_cost = 0
        context.sell_gold = 0
        context.sell_silver = 0
        context.sell_suffix = "s"
        context.sell_no_drop = False

        if not raw or room is None:
            return room

        keeper, shop, error = self._find_keeper(character, room)
        context.sell_keeper = keeper
        context.sell_shop = shop
        context.sell_keeper_error = error
        if keeper is None or shop is None:
            return room

        obj = character.find_owned_item(raw)
        context.sell_obj = obj
        if obj is None:
            return room

        context.sell_no_drop = ItemApi.has_item_flag(obj, self.item_flags, "ITEM_NODROP")
        context.sell_item_short = Item.short(obj)
        context.sell_keeper_short = getattr(keeper, "short_description", "The shopkeeper")
        context.sell_cost = shop.sell_price(obj, getattr(keeper, "inventory", []) or [], self.item_types, self.item_flags)
        context.sell_gold = context.sell_cost // 100
        context.sell_silver = context.sell_cost - (context.sell_gold * 100)
        context.sell_suffix = "" if context.sell_cost == 1 else "s"
        return room

    def _sell_success_payload(self, character: Character, room, context: Context):
        return {
            "to_char": self._render_command_message(context, "default", t=context.sell_item_short, q=context.sell_silver, g=context.sell_gold, sfx=context.sell_suffix),
            "to_room": self._render_command_message(context, "sells", channel="to_room", c=character.name, t=context.sell_item_short),
            "targets": room.player_targets(character),
        }

    def _prepare_value_context(self, character: Character, context: Context):
        raw = (context.result if isinstance(context.result, str) else "").strip()
        if not raw and context.parameters:
            raw = " ".join(context.parameters).strip()
        room = getattr(context, "room", None)
        if room is None:
            room = self.room_registry.get_or_none(id=character.room_id)

        context.room = room
        context.value_raw = raw
        context.value_room = room
        context.value_keeper = None
        context.value_shop = None
        context.value_keeper_error = ""
        context.value_keeper_name = "The shopkeeper"
        context.value_item = None
        context.value_item_short = ""
        context.value_no_drop = False
        context.value_cost = 0
        context.value_gold = 0
        context.value_silver = 0

        if not raw or room is None:
            return room

        keeper, shop, error = self._find_keeper(character, room)
        context.value_keeper = keeper
        context.value_shop = shop
        context.value_keeper_error = error
        if keeper is not None:
            context.value_keeper_name = getattr(keeper, "short_description", "The shopkeeper")
        if keeper is None or shop is None:
            return room

        obj = character.find_owned_item(raw)
        context.value_item = obj
        if obj is None:
            return room

        context.value_no_drop = ItemApi.has_item_flag(obj, self.item_flags, "ITEM_NODROP")
        context.value_item_short = Item.short(obj)
        quote = shop.quote_value(obj, keeper, self.item_types, self.item_flags)
        context.value_cost = quote.cost
        context.value_gold = quote.gold
        context.value_silver = quote.silver
        return room

    def do_junk(self, character: Character, context: Context):
        return self.destroy_carried(character, context, "Junk what?\r\n")

    def do_sacrifice(self, character: Character, context: Context):
        context.arg1, _ = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = context.room if context.room is not None else self.room_registry.get_or_none(id=character.room_id)
        context.item = room.find_room_item(context.arg1) if room is not None else None
        context.item_name = Item.short(context.item) if context.item is not None else None
        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get('blocked'):
            context.finish()
            return payload

        silver = ItemUtil.sacrifice_silver_value(context.item)
        room.remove_item_from_room(context.item)
        character.silver = int(getattr(character, "silver", 0) or 0) + silver
        context.finish()
        return {
            "to_char": context.command.payload.to_char.get('one_silver') if silver == 1 else context.command.payload.to_char.get('multiple_silver').replace("%d", str(silver)),
            "to_room": context.command.payload.to_room["default"],
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
        if ItemApi.has_item_flag(item, self.item_flags, "ITEM_NODROP"):
            context.finish()
            return {"to_char": "You can't let go of it.\r\n"}
        slot = character.equipped_slot_of(item)
        if slot:
            self.effect_handler.remove_item_effects(character, item)
            character.unequip_item(slot)
        character.remove_item(item)
        context.finish()
        return {"to_char": success_msg}

    def do_give(self, character: Character, context: Context):
        room = self._prepare_give_context(character, context)
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            context.finish()
            return blocked

        if context.give_is_money:
            payload = self._finish_give_money(character, room, context)
        else:
            payload = self._finish_give_item(character, room, context)

        context.finish()
        return payload

    def _prepare_give_context(self, character: Character, context: Context):
        raw = (context.result if isinstance(context.result, str) else "").strip()
        if not raw and context.parameters:
            raw = " ".join(context.parameters).strip()
        arg1, rem = ItemUtil.parse_raw_arguments(raw, context.parameters)
        room = getattr(context, "room", None)
        if room is None:
            room = self.room_registry.get_or_none(id=character.room_id)

        context.room = room
        context.give_raw = raw
        context.arg1 = arg1
        context.rem = rem
        context.give_is_money = str(arg1 or "").strip().isdigit()
        context.give_amount = GenericUtil.to_int(arg1, 0) if context.give_is_money else 0
        context.give_currency_token = ""
        context.give_currency = ""
        context.give_victim_name = ""
        context.victim = None
        context.item = None
        context.give_item = None
        context.give_item_short = ""
        context.give_item_worn = False
        context.give_target_is_keeper = False
        context.give_no_drop = False
        context.give_target_hands_full = False
        context.give_target_encumbered = False
        context.give_target_cannot_see = False
        context.give_insufficient_funds = False
        context.give_invalid_money = False
        context.give_money_changer = False
        context.give_change_total = 0
        context.give_change_gold = 0
        context.give_change_silver = 0
        context.interp_tokens = {}

        if not arg1 or not rem:
            return room

        if context.give_is_money:
            currency_token, victim_name = InterpUtil.one_argument(rem)
            context.give_currency_token = str(currency_token or "").strip().lower()
            context.give_currency = self._give_currency_name(context.give_currency_token)
            context.give_victim_name = victim_name
            context.give_invalid_money = context.give_amount <= 0 or not context.give_currency
            if context.give_invalid_money or not victim_name:
                return room

            victim = self._find_give_target(room, victim_name)
            context.victim = victim
            if victim is None:
                return room

            context.interp_tokens = {"t": getattr(victim, "name", "")}
            context.give_insufficient_funds = (
                GenericUtil.to_int(getattr(character, context.give_currency, 0), 0) < context.give_amount
            )
            context.give_money_changer = self._is_money_changer(victim)
            if context.give_money_changer:
                if context.give_currency == "silver":
                    context.give_change_total = (95 * context.give_amount) // 100
                else:
                    context.give_change_total = 95 * context.give_amount
                context.give_change_gold = context.give_change_total // 100
                context.give_change_silver = context.give_change_total - (context.give_change_gold * 100)
            return room

        victim_name, _ = InterpUtil.one_argument(rem)
        item = character.find_inventory_item(arg1) if arg1 else None
        victim = self._find_give_target(room, victim_name)
        item_short = Item.short(item) if item is not None else ""

        context.give_victim_name = victim_name
        context.victim = victim
        context.item = item
        context.give_item = item
        context.give_item_short = item_short
        context.give_item_worn = bool(item is not None and character.equipped_slot_of(item))
        context.give_target_is_keeper = self._is_shopkeeper(victim)
        context.give_no_drop = bool(item is not None and ItemApi.has_item_flag(item, self.item_flags, "ITEM_NODROP"))
        context.interp_tokens = {
            "t": getattr(victim, "name", ""),
            "s": self._possessive_name(victim),
        }

        if victim is None or item is None:
            return room

        max_items = victim.max_items()
        if max_items > 0 and victim.carry_count() + 1 > max_items:
            context.give_target_hands_full = True

        max_weight = victim.max_weight()
        item_weight = GenericUtil.to_int(getattr(item, "weight", 0), 0)
        if max_weight > 0 and victim.carry_weight() + item_weight > max_weight:
            context.give_target_encumbered = True

        if room is not None:
            context.give_target_cannot_see = not ItemUtil.can_see_object(room, victim, item)
        return room

    def _finish_give_item(self, character: Character, room, context: Context):
        item = context.give_item
        victim = context.victim
        item_short = context.give_item_short
        character.remove_item(item)
        victim.add_item(item)

        payload = {
            "to_char": self._render_command_message(context, "item_received", t=item_short, T=getattr(victim, "name", "")),
        }
        if room is not None:
            payload["to_room"] = self._render_command_message(
                context,
                "item_received",
                channel="to_room",
                c=character.name,
                t=item_short,
                T=getattr(victim, "name", ""),
            )
            payload["targets"] = room.to_not_victim(victim)
        if not CharacterApi.is_npc(victim):
            payload["to_victim"] = self._render_command_message(
                context,
                "item_received",
                channel="to_victim",
                c=character.name,
                t=item_short,
                T=getattr(victim, "name", ""),
            )
            payload["victim"] = victim
        return payload

    def _finish_give_money(self, character: Character, room, context: Context):
        victim = context.victim
        currency = context.give_currency
        amount = context.give_amount
        self._deduct_money(character, amount if currency == "silver" else amount * 100)
        self._add_money(victim, amount if currency == "silver" else amount * 100)

        payload = {
            "to_char": self._render_command_message(
                context,
                "funds_received",
                t=getattr(victim, "name", ""),
                q=amount,
                s=currency,
            ),
        }
        if room is not None:
            payload["to_room"] = self._render_command_message(
                context,
                "funds_received",
                channel="to_room",
                c=character.name,
                t=getattr(victim, "name", ""),
                q=amount,
                s=currency,
            )
            payload["targets"] = [
                viewer for viewer in room.player_targets(character)
                if getattr(viewer, "id", "") != getattr(victim, "id", "")
            ]
        if not CharacterApi.is_npc(victim):
            payload["to_victim"] = self._render_command_message(
                context,
                "funds_received",
                channel="to_victim",
                c=character.name,
                q=amount,
                s=currency,
            )
            payload["victim"] = victim

        if context.give_money_changer and CharacterApi.can_see(victim, character, room):
            self._append_money_changer_payload(character, room, context, payload)

        return payload

    def _append_money_changer_payload(self, character: Character, room, context: Context, payload: dict):
        victim = context.victim
        amount_total = context.give_amount if context.give_currency == "silver" else context.give_amount * 100
        if context.give_change_total < 1:
            payload["to_char"] += self._render_command_message(
                context,
                "money_changer_insufficient_funds",
                t=getattr(victim, "name", ""),
            )
            self._deduct_money(victim, amount_total)
            self._add_money(character, amount_total)
            payload["to_char"] += self._render_command_message(
                context,
                "funds_received",
                channel="to_victim",
                c=getattr(victim, "name", ""),
                q=context.give_amount,
                s=context.give_currency,
            )
            if room is not None:
                payload["to_room"] = payload.get("to_room", "") + self._render_command_message(
                    context,
                    "funds_received",
                    channel="to_room",
                    c=getattr(victim, "name", ""),
                    t=character.name,
                )
            return

        self._deduct_money(victim, context.give_change_total)
        self._add_money(character, context.give_change_total)
        if context.give_change_gold > 0:
            payload["to_char"] += self._render_command_message(
                context,
                "funds_received",
                channel="to_victim",
                c=getattr(victim, "name", ""),
                q=context.give_change_gold,
                s="gold",
            )
            if room is not None:
                payload["to_room"] = payload.get("to_room", "") + self._render_command_message(
                    context,
                    "funds_received",
                    channel="to_room",
                    c=getattr(victim, "name", ""),
                    t=character.name,
                )
        if context.give_change_silver > 0:
            payload["to_char"] += self._render_command_message(
                context,
                "funds_received",
                channel="to_victim",
                c=getattr(victim, "name", ""),
                q=context.give_change_silver,
                s="silver",
            )
            if room is not None:
                payload["to_room"] = payload.get("to_room", "") + self._render_command_message(
                    context,
                    "funds_received",
                    channel="to_room",
                    c=getattr(victim, "name", ""),
                    t=character.name,
                )
        payload["to_char"] += self._render_command_message(
            context,
            "money_changer_funds_received",
            t=getattr(victim, "name", ""),
        )

    def _find_give_target(self, room, wanted: str):
        query = str(wanted or "").strip()
        if room is None or not query:
            return None
        for collection_name in ("characters", "mobiles"):
            collection = getattr(room, collection_name, {}) or {}
            for entity in collection.values():
                if InfoUtil.look_keyword_matches(query, getattr(entity, "name", "")):
                    return entity
        return None

    def _is_shopkeeper(self, victim) -> bool:
        if victim is None or self.shop_registry is None:
            return False
        return self.shop_registry.find_by_keeper_vnum(getattr(victim, "vnum", "")) is not None

    def _is_money_changer(self, victim) -> bool:
        if victim is None:
            return False
        bit = CharacterApi.enum_bit(self.act_bits, "ACT_IS_CHANGER")
        if bit <= 0:
            return False
        raw = GenericUtil.to_int(getattr(getattr(victim, "status_flags", None), "act", getattr(victim, "act", 0)), 0)
        if hasattr(CharacterApi, "is_set"):
            return CharacterApi.is_set(raw, bit)
        return (raw & bit) != 0

    @staticmethod
    def _give_currency_name(token: str) -> str:
        wanted = str(token or "").strip().lower()
        if wanted == "gold":
            return "gold"
        if wanted in {"silver", "coin", "coins"}:
            return "silver"
        return ""

    @staticmethod
    def _possessive_name(victim) -> str:
        if victim is None:
            return "their"
        sex = str(getattr(victim, "sex", "") or "").strip().lower()
        if sex in {"m", "male", "1"}:
            return "his"
        if sex in {"f", "female", "2"}:
            return "her"
        if sex in {"n", "neutral", "0", "it"}:
            return "its"
        return "their"

    def do_wear(self, character: Character, context: Context):
        room = self._prepare_equipment_context(character, context)
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            context.finish()
            return blocked

        if context.wear_all:
            result = Equipped.wear_all(character, self.wear_flags, self.item_flags, effect_handler=self.effect_handler)
        else:
            result = Equipped.wear_item(
                character,
                context.wear_item,
                self.wear_flags,
                self.item_flags,
                replace=True,
                forced_slot=context.wear_forced_slot,
                effect_handler=self.effect_handler,
            )
        payload = self._equipment_result_payload(character, room, context, result)
        context.finish()
        return payload

    def do_wield(self, character: Character, context: Context):
        return self.equip_to_slot(character, context, "wielded")

    def do_hold(self, character: Character, context: Context):
        return self.equip_to_slot(character, context, "held")

    def equip_to_slot(self, character: Character, context: Context, slot: str):
        room = self._prepare_equipment_context(character, context, preferred_slot=slot)
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            context.finish()
            return blocked

        result = Equipped.wear_item(
            character,
            context.equip_item,
            self.wear_flags,
            self.item_flags,
            replace=True,
            preferred_slot=slot,
            effect_handler=self.effect_handler,
        )
        payload = self._equipment_result_payload(character, room, context, result)
        context.finish()
        return payload

    def _prepare_equipment_context(self, character: Character, context: Context, preferred_slot: str = ""):
        arg1, rem = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = self.room_registry.get_or_none(id=character.room_id)
        item = None if arg1 == "all" else character.find_inventory_item(arg1)

        context.room = room
        context.wear_arg1 = arg1
        context.wear_all = (not preferred_slot) and arg1 == "all"
        context.wear_item = item
        context.wear_forced_slot = "" if preferred_slot else (rem.split()[0] if rem else "")
        context.wear_invalid_target = False
        context.wear_invalid_message_key = "invalidTarget"
        context.wear_item_short = "" if item is None else Item.short(item)
        context.wear_item_level = 0 if item is None else GenericUtil.to_int(getattr(item, "level", 0), 0)

        context.equip_arg1 = arg1
        context.equip_item = item

        if item is not None and not context.wear_all:
            slot_groups = Equipped.wear_slot_groups_for_item(
                item,
                self.wear_flags,
                preferred_slot=preferred_slot,
                forced_slot=context.wear_forced_slot,
            )
            context.wear_invalid_target = not bool(slot_groups)
            context.wear_invalid_message_key = "invalidTargetThere" if context.wear_forced_slot else "invalidTarget"
        return room

    def _equipment_result_payload(self, character: Character, room, context: Context, result) -> dict:
        payload: dict[str, str | list] = {}

        def _append(rendered: dict):
            text = str(rendered.get("to_char", "") or "")
            if text:
                payload["to_char"] = f"{payload.get('to_char', '')}{text}"
            room_text = str(rendered.get("to_room", "") or "")
            if room_text:
                payload["to_room"] = f"{payload.get('to_room', '')}{room_text}"

        if getattr(result, "blocked_key", ""):
            payload["blocked_key"] = result.blocked_key
            _append(self.interp_api.render_message_key(context, result.blocked_key, **dict(getattr(result, "blocked_tokens", {}) or {})))
        for key, tokens in list(getattr(result, "shared_messages", []) or []):
            _append(self.interp_api.render_message_key(context, key, **dict(tokens or {})))
        for key, tokens in list(getattr(result, "char_messages", []) or []):
            _append(self.interp_api.render_message_key(context, key, channel="to_char", **dict(tokens or {})))

        if payload.get("to_room") and room is not None:
            payload["targets"] = room.player_targets(character)
        return payload

    def do_remove(self, character: Character, context: Context):
        room = self._prepare_remove_context(character, context)
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            context.finish()
            return blocked

        result = Equipped.remove_item(character, context.remove_slot, context.remove_item, self.item_flags, effect_handler=self.effect_handler)
        payload = self._equipment_result_payload(character, room, context, result)
        context.finish()
        return payload

    def _prepare_remove_context(self, character: Character, context: Context):
        arg1, _ = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = getattr(context, "room", None)
        if room is None:
            room = self.room_registry.get_or_none(id=character.room_id)

        equipped = character.ensure_equipped()
        slot, item = equipped.find_remove_target(arg1)

        context.room = room
        context.remove_arg1 = arg1
        context.remove_slot = slot
        context.remove_item = item
        context.remove_item_short = "" if item is None else Item.short(item)
        context.remove_no_remove = bool(item is not None and not getattr(item, "can_remove", lambda _item_flags: True)(self.item_flags))
        return room

    @staticmethod
    def _render_command_message(context: Context, key: str, channel: str = "to_char", **tokens) -> str:
        command = getattr(context, "command", None)
        if command is None:
            return ""
        text = command.render_message(channel, key, **tokens)
        return CommunicationsUtil.ensure_message_break(text)

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
        room = context.room if context.room is not None else self.room_registry.get_or_none(id=character.room_id)
        item = character.find_inventory_item(arg1) if arg1 else None
        if item is None:
            item = room.find_room_item(arg1) if room is not None and arg1 else None
        if item is None and not arg1:
            item = Item.first_fountain(room)
        context.drink_arg1 = arg1
        context.drink_item = item
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked

        liquid_name = str(getattr(item, "value2", "") or "")
        liquid_affect = list(getattr(item, "liquid_affect_data", []) or [])
        serving_size = GenericUtil.to_int(liquid_affect[4], 0) if len(liquid_affect) > 4 else 0
        if Item.is_fountain(item):
            amount = max(1, serving_size * 3)
        else:
            value1 = GenericUtil.to_int(getattr(item, "value1", 0), 0)
            amount = min(max(1, serving_size), value1)
            if GenericUtil.to_int(getattr(item, "value0", 0), 0) > 0:
                item.value1 = str(max(0, value1 - amount))

        tokens = {
            "c": character.name,
            "p": Item.short(item),
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
            self.logger.debug(f"Drunk: {drunk}, Full: {full}, Thirst: {thirst}")
            self.logger.debug(f"drunk_gain: {drunk_gain}; thirst_gain: {thirst_gain}; full_gain: {full_gain}; hunger_gain: {hunger_gain}")
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
            "to_char": self._render_command_message(context, "default", "to_char", p=Item.short(item)),
        }
        room = self.room_registry.get_or_none(id=character.room_id)
        if room is not None:
            payload["to_room"] = self._render_command_message(context, "default", "to_room", c=character.name, p=Item.short(item))
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
            self.effect_handler.remove_item_effects(character, item)
            character.unequip_item(slot)
        character.remove_item(item)
        context.finish()
        return payload

    def do_fill(self, character: Character, context: Context):
        room = self._prepare_fill_context(character, context)
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            context.finish()
            return blocked

        result = Item.fill_from_source(context.fill_dest, context.fill_src)
        context.finish()
        payload = self.interp_api.render_message_key(
            context,
            "default",
            t=context.fill_dest_short,
            s=result.liquid_name,
            T=context.fill_src_short,
        )
        if room is not None and payload.get("to_room"):
            payload["targets"] = room.player_targets(character)
        return payload

    def _prepare_fill_context(self, character: Character, context: Context):
        arg1, rem = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = getattr(context, "room", None)
        if room is None:
            room = self.room_registry.get_or_none(id=character.room_id)

        dest = character.find_inventory_item(arg1) if arg1 else None
        src_name = rem.split()[0] if rem else ""
        src = character.find_inventory_item(src_name) or (None if room is None else room.find_room_item(src_name)) if src_name else None
        if src is None:
            src = Item.first_fountain(room)

        context.room = room
        context.fill_arg1 = arg1
        context.fill_rem = rem
        context.fill_dest = dest
        context.fill_src = src
        context.fill_dest_short = "" if dest is None else Item.short(dest)
        context.fill_src_short = "" if src is None else Item.short(src)
        context.fill_blocked_key = ""
        if dest is not None:
            preview = Item.inspect_fill(dest, src)
            context.fill_blocked_key = preview.blocked_key
        return room

    def do_pour(self, character: Character, context: Context):
        room = self._prepare_pour_context(character, context)
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            context.finish()
            return blocked

        result = Item.pour(context.pour_source, context.pour_target_container, pour_out=context.pour_is_out)
        context.finish()
        if context.pour_is_out:
            payload = self.interp_api.render_message_key(
                context,
                "spill_out",
                t=Item.short(context.pour_source),
                s=result.liquid_name,
                c=character.name,
            )
        elif context.pour_target_character is not None:
            payload = self.interp_api.render_message_key(
                context,
                "for_victim",
                t=getattr(context.pour_target_character, "name", ""),
                s=result.liquid_name,
                c=character.name,
            )
            payload["to_victim"] = self._render_command_message(
                context,
                "default",
                channel="to_victim",
                c=character.name,
                s=result.liquid_name,
            )
            payload["victim"] = context.pour_target_character
            if room is not None and payload.get("to_room"):
                payload["targets"] = [
                    viewer for viewer in room.player_targets(character)
                    if getattr(viewer, "id", "") != getattr(context.pour_target_character, "id", "")
                ]
        else:
            payload = self.interp_api.render_message_key(
                context,
                "to_container",
                s=result.liquid_name,
                t=Item.short(context.pour_source),
                T=Item.short(context.pour_target_container),
                c=character.name,
            )

        if room is not None and payload.get("to_room") and "targets" not in payload:
            payload["targets"] = room.player_targets(character)
        return payload

    def _prepare_pour_context(self, character: Character, context: Context):
        arg1, rem = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = context.room if context.room is not None else self.room_registry.get_or_none(id=character.room_id)
        target_arg = str(rem or "").strip()
        source = character.find_inventory_item(arg1) if arg1 else None
        target_item = None
        target_character = None
        target_container = None
        preview = None

        if target_arg and target_arg.lower() != "out":
            target_item = character.find_inventory_item(target_arg) or (None if room is None else room.find_room_item(target_arg))
            if target_item is None:
                target_character = PlayerUtil.get_target(character, target_arg, room)
                if target_character is not None:
                    equipped = target_character.ensure_equipped() if hasattr(target_character, "ensure_equipped") else getattr(target_character, "equipped", None)
                    target_container = getattr(equipped, "held", None) if equipped is not None else None
            else:
                target_container = target_item

        if source is not None:
            preview = Item.inspect_pour(source, target_container, pour_out=target_arg.lower() == "out")

        context.room = room
        context.pour_arg1 = arg1
        context.pour_target_arg = target_arg
        context.pour_is_out = target_arg.lower() == "out"
        context.pour_source = source
        context.pour_target_item = target_item
        context.pour_target_character = target_character
        context.pour_target_container = target_container
        context.pour_liquid_name = "" if preview is None else preview.liquid_name
        context.pour_blocked_key = "" if preview is None else preview.blocked_key
        return room

    def do_quaff(self, character: Character, context: Context):
        arg1, _ = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = context.room if context.room is not None else self.room_registry.get_or_none(id=character.room_id)
        item = character.find_inventory_item(arg1) if arg1 else None
        context.room = room
        context.quaff_arg1 = arg1
        context.quaff_item = item
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked

        payloads = [{
            "to_char": self._render_command_message(context, "quaff", t=Item.short(item)),
            "to_room": self._render_command_message(context, "quaffs", channel="to_room", c=character.name, t=Item.short(item)),
            "targets": room.player_targets(character) if room is not None else [],
        }]
        for spell_ref in Item.spell_refs(item, 1, 2, 3):
            payloads.extend(self._cast_item_spell(character, room, item, spell_ref, target=character, target_name=character.name, target_kind="char"))

        self._destroy_item(character, item)
        context.finish()
        return {"payloads": payloads}

    def do_recite(self, character: Character, context: Context):
        arg1, rem = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = context.room if context.room is not None else self.room_registry.get_or_none(id=character.room_id)
        scroll = character.find_inventory_item(arg1) if arg1 else None
        target_name = rem.split()[0] if rem else ""
        target = character if not target_name else PlayerUtil.get_target(character, target_name, room)
        if target is None and target_name:
            target = character.find_inventory_item(target_name) or (None if room is None else room.find_room_item(target_name))

        context.room = room
        context.recite_arg1 = arg1
        context.recite_target_name = target_name
        context.recite_scroll = scroll
        context.recite_target = target
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked

        payloads = [{
            "to_char": self._render_command_message(context, "recite", t=Item.short(scroll)),
            "to_room": self._render_command_message(context, "recites", channel="to_room", c=character.name, t=Item.short(scroll)),
            "targets": room.player_targets(character) if room is not None else [],
        }]
        if not self._item_skill_check(character, "scrolls"):
            self._improve_item_skill(character, "scrolls", False)
            payloads.append({"to_char": self._render_command_message(context, "failed")})
        else:
            target_kind = "obj" if target is not None and hasattr(target, "item_type") else "char"
            for spell_ref in Item.spell_refs(scroll, 1, 2, 3):
                payloads.extend(self._cast_item_spell(character, room, scroll, spell_ref, target=target, target_name=target_name, target_kind=target_kind))
            self._improve_item_skill(character, "scrolls", True)

        self._destroy_item(character, scroll)
        context.finish()
        return {"payloads": payloads}

    def do_brandish(self, character: Character, context: Context):
        room = context.room if context.room is not None else self.room_registry.get_or_none(id=character.room_id)
        staff = getattr(character.ensure_equipped(), "held", None)
        context.room = room
        context.brandish_item = staff
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked

        skill_ref = Item.spell_refs(staff, 3)
        spell = skill_ref[0] if skill_ref and hasattr(skill_ref[0], "handler_id") else None
        if spell is None and skill_ref:
            spell = FightUtil.find_spell(self.spell_registry, skill_ref[0])
        if spell is None:
            context.finish()
            return None

        CharacterApi.wait_state(character, 24)
        payloads: list[dict] = []
        if Item.charges(staff) > 0:
            payloads.append({
                "to_char": self._render_command_message(context, "default", t=Item.short(staff)),
                "to_room": self._render_command_message(context, "default", channel="to_room", c=character.name, t=Item.short(staff)),
                "targets": room.player_targets(character) if room is not None else [],
            })
            if int(getattr(character, "level", 0) or 0) < int(getattr(staff, "level", 0) or 0) or not self._item_skill_check(character, "staves"):
                self._improve_item_skill(character, "staves", False)
                failure = self.interp_api.render_message_key(context, "failure", t=Item.short(staff))
                if room is not None and failure.get("to_room"):
                    failure["targets"] = room.player_targets(character)
                payloads.append(failure)
            else:
                people = list(getattr(room, "characters", {}).values()) + list(getattr(room, "mobiles", {}).values()) if room is not None else []
                if character not in people:
                    people.insert(0, character)
                target_type = str(getattr(spell, "target", "") or "").upper()
                for victim in people:
                    if target_type == "IGNORE" and victim is not character:
                        continue
                    if target_type == "CHAR_SELF" and victim is not character:
                        continue
                    if target_type == "CHAR_OFFENSIVE" and CharacterApi.is_npc(character) == CharacterApi.is_npc(victim):
                        continue
                    if target_type == "CHAR_DEFENSIVE" and CharacterApi.is_npc(character) != CharacterApi.is_npc(victim):
                        continue
                    payloads.extend(self._cast_item_spell(character, room, staff, spell, target=victim, target_name=getattr(victim, "name", ""), target_kind="char"))
                self._improve_item_skill(character, "staves", True)

        if Item.spend_charge(staff) <= 0:
            broken = self.interp_api.render_message_key(context, "item_broken", t=Item.short(staff), c=character.name)
            if room is not None and broken.get("to_room"):
                broken["targets"] = room.player_targets(character)
            payloads.append(broken)
            self._destroy_item(character, staff)

        context.finish()
        return {"payloads": payloads}

    def do_zap(self, character: Character, context: Context):
        arg1, _ = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = context.room if context.room is not None else self.room_registry.get_or_none(id=character.room_id)
        wand = getattr(character.ensure_equipped(), "held", None)
        victim = getattr(character, "fighting", None) if not arg1 else PlayerUtil.get_target(character, arg1, room)
        obj = None if victim is not None else ((character.find_inventory_item(arg1) if arg1 else None) or (None if room is None else room.find_room_item(arg1)))

        context.room = room
        context.zap_arg1 = arg1
        context.zap_item = wand
        context.zap_victim = victim
        context.zap_obj = obj
        context.zap_target = victim or obj
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked

        CharacterApi.wait_state(character, 24)
        payloads: list[dict] = []
        if Item.charges(wand) > 0:
            if victim is not None:
                room_targets = room.player_targets(character) if room is not None else []
                room_targets = [viewer for viewer in room_targets if getattr(viewer, "id", "") != getattr(victim, "id", "")]
                payloads.append({
                    "to_char": self._render_command_message(context, "default", t=getattr(victim, "name", ""), T=Item.short(wand)),
                    "to_room": self._render_command_message(context, "default", channel="to_room", c=character.name, t=getattr(victim, "name", ""), T=Item.short(wand)),
                    "to_victim": self._render_command_message(context, "zaps_with", channel="to_victim", c=character.name, t=Item.short(wand)),
                    "victim": victim,
                    "targets": room_targets,
                })
            else:
                payloads.append({
                    "to_char": self._render_command_message(context, "default", t=Item.short(obj), T=Item.short(wand)),
                    "to_room": self._render_command_message(context, "default", channel="to_room", c=character.name, t=Item.short(obj), T=Item.short(wand)),
                    "targets": room.player_targets(character) if room is not None else [],
                })

            if int(getattr(character, "level", 0) or 0) < int(getattr(wand, "level", 0) or 0) or not self._item_skill_check(character, "wands"):
                self._improve_item_skill(character, "wands", False)
                failure = self.interp_api.render_message_key(context, "failed", t=Item.short(wand), c=character.name)
                if room is not None and failure.get("to_room"):
                    failure["targets"] = room.player_targets(character)
                payloads.append(failure)
            else:
                spell_refs = Item.spell_refs(wand, 3)
                payloads.extend(
                    self._cast_item_spell(
                        character,
                        room,
                        wand,
                        spell_refs[0] if spell_refs else None,
                        target=victim or obj,
                        target_name=arg1,
                        target_kind="obj" if obj is not None else "char",
                    )
                )
                self._improve_item_skill(character, "wands", True)

        if Item.spend_charge(wand) <= 0:
            broken = self.interp_api.render_message_key(context, "item_broken", t=Item.short(wand), c=character.name)
            if room is not None and broken.get("to_room"):
                broken["targets"] = room.player_targets(character)
            payloads.append(broken)
            self._destroy_item(character, wand)

        context.finish()
        return {"payloads": payloads}

    def _item_skill_check(self, character: Character, skill_name: str) -> bool:
        skill_percent = 1
        if CharacterApi.is_npc(character):
            skill_percent = max(1, min(100, 40 + (2 * int(getattr(character, "level", 0) or 0))))
        elif hasattr(character, "skill_level"):
            skill_percent = max(1, min(100, GenericUtil.to_int(character.skill_level(skill_name), 1)))
        threshold = 20 + (skill_percent * 4) // 5
        return random.randint(1, 100) < threshold

    def _improve_item_skill(self, character: Character, skill_name: str, success: bool):
        if self.skill_registry is None or not hasattr(self.skill_registry, "get_or_none"):
            return
        skill = self.skill_registry.get_or_none(name=skill_name)
        if skill is None:
            return
        Ability.check_improve(character, getattr(skill, "id", ""), success, 2)

    def _cast_item_spell(self, character: Character, room, item, spell_ref, *, target=None, target_name: str = "", target_kind: str = "") -> list[dict]:
        spell = spell_ref
        if spell is None or not hasattr(spell, "handler_id"):
            spell = FightUtil.find_spell(self.spell_registry, getattr(spell_ref, "name", spell_ref))
        if spell is None:
            return []

        context = SpellContext(
            actor=character,
            spell=spell,
            handler=self,
            room=room,
            target=target,
            target_name=target_name,
            target_kind=target_kind,
            cast_level=Item.spell_level(item),
            source="player",
        )
        self.spell_api.execute_lambdas(context)
        if context.performed:
            self.spell_api.start_offensive_combat(context)
        return list(context.payloads)

    @staticmethod
    def _destroy_item(character: Character, item) -> None:
        if item is None:
            return
        slot = character.equipped_slot_of(item) if hasattr(character, "equipped_slot_of") else None
        if slot:
            character.unequip_item(slot)
        character.remove_item(item)

    def _find_keeper(self, character: Character, room):
        if self.shop_registry is None:
            return None, None, "shop_unavailable"
        for mob in room.mobiles.values():
            shop = self.shop_registry.find_by_keeper_vnum(getattr(mob, "vnum", ""))
            if shop is None:
                continue
            hour = GenericUtil.to_int(getattr(getattr(self.weather_handler, "time_info", None), "hour", -1), -1)
            error = shop.keeper_error(mob, character, room, hour)
            if error:
                return None, None, error
            return mob, shop, ""
        return None, None, "shop_unavailable"

    def _keeper_error_payload(self, error_key: str) -> dict:
        messages = {
            "shop_unavailable": "You can't do that here.\r\n",
            "shop_closed_later": "Sorry, I am closed. Come back later.\r\n",
            "shop_closed_tomorrow": "Sorry, I am closed. Come back tomorrow.\r\n",
            "keeper_cannot_see": "I don't trade with folks I can't see.\r\n",
        }
        return {"to_char": messages.get(error_key, "You can't do that here.\r\n")}

    def _mult_argument(self, argument: str) -> tuple[int, str]:
        text = str(argument or "").strip()
        if "*" not in text:
            return 1, text
        count_text, remainder = text.split("*", 1)
        count = GenericUtil.to_int(count_text, 1)
        return max(1, count), remainder.strip()

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
