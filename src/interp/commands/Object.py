from __future__ import annotations

import random

from injector import inject

from api.GameApi import GameApi
from api.CommunicationsApi import CommunicationsApi
from area.Shop import Shop
from combat.CombatHandler import FightHandler
from game.EnumProvider import EnumProvider
from game.Equipped import Equipped
from game.WeatherHandler import WeatherHandler
from game.RandomNumberGenerator import RandomNumberGenerator
from item.Effect import Effect
from item.EffectHandler import EffectHandler
from util.EnumUtil import EnumUtil
from util.GenericUtil import GenericUtil
from game.RegistryService import RegistryService
from interp.Context import Context
from util.InfoUtil import InfoUtil
from util.LookupUtil import LookupUtil
from util.InterpUtil import InterpUtil
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
                 weather_handler: WeatherHandler,
                 interp_api: InterpApi,
                 spell_api: SpellApi,
                 fight_handler: FightHandler,
                 effect_handler: EffectHandler):
        self.__name__ = "Object"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry_service = registry_service
        self.room_registry = registry_service.room_registry
        self.item_registry = getattr(registry_service, "item_registry", None)
        self.mobile_registry = registry_service.mobile_registry
        self.shop_registry = registry_service.shop_registry
        self.skill_registry = registry_service.skill_registry
        self.spell_registry = registry_service.spell_registry
        self.weather_handler = weather_handler
        self.interp_api = interp_api
        self.effect_handler = effect_handler
        self.spell_api = spell_api
        self.fight_handler = fight_handler
        self.item_types = enum_provider.get("itemTypes")
        self.container_state = enum_provider.get("containerState")
        self.item_flags = enum_provider.get("itemFlags")
        self.wear_flags = enum_provider.get("wearFlags")
        self.weapon_type = enum_provider.get("weaponType")
        self.room_flags = enum_provider.get("roomFlags")
        self.act_bits = enum_provider.get("actBits")
        self.PlayerActBits = enum_provider.get("playerActBits")
        self.GameParameters = enum_provider.get("gameParameters")
        self.affected_bits = enum_provider.get("affectedBy")
        self.comm_flags = enum_provider.get("commFlags")
        self.well_known_object_vnums = enum_provider.get("wellKnownObjectVnums")

    def execute(self, character: Character, context: Context):
        context.handler = self
        name = (context.command.name or "").strip().lower()
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
            "heal": self.do_heal,
            "envenom": self.do_envenom,
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
            "steal": self.do_steal,
            "outfit": self.do_outfit,
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

    def do_heal(self, character: Character, context: Context):
        room = context.room if context.room is not None else self.room_registry.get_or_none(id=character.room_id)
        service_key, _rest = InterpUtil.one_argument((context.result if isinstance(context.result, str) else "") or " ".join(context.parameters or []))
        healer = self._find_healer(room)

        context.heal_room = room
        context.heal_healer = healer
        context.heal_service_key = service_key
        context.heal_service = self._healer_service(service_key)
        context.heal_cost = 0 if context.heal_service is None else context.heal_service["cost"]

        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            context.finish()
            return blocked

        if not service_key:
            context.finish()
            return {"to_char": self._healer_service_list(healer)}

        payloads = self._buy_healer_service(character, room, healer, context.heal_service)
        context.finish()
        return {"payloads": payloads}

    def _buy_healer_service(self, character: Character, room, healer, service: dict):
        cost = GenericUtil.to_int(service.get("cost"), 0)
        self._deduct_money(character, cost)
        self._add_money(healer, cost)
        CharacterApi.wait_state(character, 24)

        payload: dict = {
            "to_room": f"{getattr(healer, 'short_description', '') or getattr(healer, 'name', 'The healer')} utters the words '{service.get('words', '')}'.\r\n",
            "targets": room.player_targets(character) if room is not None and hasattr(room, "player_targets") else [],
        }

        if service.get("kind") == "mana":
            amount = random.randint(1, 8) + random.randint(1, 8) + (GenericUtil.to_int(getattr(healer, "level", 0), 0) // 3)
            current = GenericUtil.to_int(getattr(character, "mana", 0), 0)
            maximum = GenericUtil.to_int(getattr(character, "max_mana", current), current)
            character.mana = min(maximum, current + amount)
            payload["to_char"] = "A warm glow passes through you.\r\n"
            return [payload]

        spell = FightUtil.find_spell(self.spell_registry, str(service.get("spell", "") or ""))
        if spell is None:
            payload["to_char"] = "You feel momentarily better.\r\n"
            return [payload]

        spell_context = SpellContext(
            actor=healer,
            spell=spell,
            handler=self,
            room=room,
            target=character,
            target_name=str(getattr(character, "name", "") or ""),
            target_kind="char",
            cast_level=GenericUtil.to_int(getattr(healer, "level", 0), 0),
            source="mobile",
            command_context=None,
        )
        self.spell_api.execute_lambdas(spell_context)
        return [payload] + list(spell_context.payloads)

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

        haggle = self._haggle_transaction(character, context, "sell")
        context.sell_shop.complete_sale(character, context.sell_keeper, context.sell_obj, context.sell_cost, self.item_flags, effect_handler=self.effect_handler)

        payload = self._sell_success_payload(character, room, context)
        if haggle:
            payload = {"payloads": [
                {"to_room": payload["to_room"], "targets": payload["targets"]},
                {"to_char": haggle + payload["to_char"]},
            ]}
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

    def do_outfit(self, character: Character, context: Context):
        if GenericUtil.to_int(getattr(character, "level", 0), 0) > 5 and not CharacterApi.is_immortal(character):
            context.finish()
            return self.interp_api.render_message_key(context, "graduate", channel="to_char")

        for vnum in self._outfit_vnums(character):
            item = self._create_outfit_item(vnum)
            if item is None:
                continue
            character.add_item(item)
            result = Equipped.wear_item(
                character,
                item,
                self.wear_flags,
                self.item_flags,
                replace=False,
                effect_handler=self.effect_handler,
            )
            if character.equipped_slot_of(item) is None or getattr(result, "blocked_key", ""):
                try:
                    character.remove_item(item)
                except ValueError:
                    pass

        context.finish()
        return self.interp_api.render_message_key(context, "default", channel="to_char")

    def _outfit_vnums(self, character: Character) -> list[str]:
        return [
            self._well_known_outfit_vnum("OBJ_VNUM_SCHOOL_BANNER", 3716),
            self._outfit_weapon_vnum(character),
            self._well_known_outfit_vnum("OBJ_VNUM_SCHOOL_HELMET", 3706),
            self._well_known_outfit_vnum("OBJ_VNUM_SCHOOL_SHIELD", 3704),
            self._well_known_outfit_vnum("OBJ_VNUM_SCHOOL_VEST", 3703),
        ]

    def _outfit_weapon_vnum(self, character: Character) -> str:
        class_weapon = getattr(getattr(character, "character_class", None), "weapon", None)
        if not class_weapon:
            try:
                class_name = str(getattr(getattr(character, "character_class", None), "name", "") or "")
                class_weapon = CharacterApi.class_data(class_name).get("weapon", "")
            except (AttributeError, RuntimeError):
                class_weapon = ""
        return self._resolve_outfit_vnum(class_weapon) or self._well_known_outfit_vnum("OBJ_VNUM_SCHOOL_DAGGER", 3701)

    def _well_known_outfit_vnum(self, name: str, fallback: int) -> str:
        return self._resolve_outfit_vnum(name) or str(fallback)

    def _resolve_outfit_vnum(self, value) -> str:
        if value is None:
            return ""
        if isinstance(value, int):
            return str(value)
        text = str(getattr(value, "value", value) or "").strip()
        if not text:
            return ""
        if text.lstrip("-").isdigit():
            return text
        enum_obj = self.well_known_object_vnums
        member = None
        try:
            member = enum_obj[text]
        except (TypeError, KeyError, AttributeError):
            member = getattr(enum_obj, text, None)
        return str(getattr(member, "value", "") or "")

    def _create_outfit_item(self, vnum: str):
        proto = self._outfit_prototype(vnum)
        if proto is None:
            return None
        try:
            return ItemUtil.create_object(proto)
        except ValueError:
            return None

    def _outfit_prototype(self, vnum: str):
        registry = self.item_registry
        if registry is None:
            return None
        target = str(vnum or "").strip()
        if not target:
            return None
        for method_name in ("get_or_none", "get"):
            method = getattr(registry, method_name, None)
            if method is None:
                continue
            for current in (target, GenericUtil.to_int(target, target)):
                try:
                    proto = method(vnum=current)
                except Exception:
                    proto = None
                if proto is not None:
                    return proto
        for proto in list(getattr(registry, "all_items", lambda: [])() or []):
            if str(getattr(proto, "vnum", "") or "") == target:
                return proto
        return None

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
        context.container = self._here_item(character, room, context.container_name) if context.container_name else None
        context.get_container_loot_allowed = (
            context.container is None or not Item.is_pc_corpse(context.container)
            or self.can_loot(character, context.container, room)
        )
        context.target_item = None
        context.get_candidates = []
        context.get_item_takeable = False

        if context.container is not None:
            if context.get_all:
                context.get_candidates = self._get_matching_container_items(character, room, context.container, context.get_filter_name)
            else:
                context.target_item = LookupUtil.find(list(getattr(context.container, "contains", []) or []), arg1, visible=lambda obj: ItemUtil.can_see_object(room, character, obj))
        elif not context.container_name:
            if context.get_all:
                context.get_candidates = self._get_matching_room_items(character, room, context.get_filter_name)
            else:
                context.target_item = self._room_item(character, room, arg1)

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
        payloads = []

        for obj in list(items or []):
            payload = self._get_one(character, room, context, obj, container)
            payloads.append(payload)
            if payload.get("to_char"):
                char_lines.append(payload["to_char"])
            if payload.get("to_room"):
                room_lines.append(payload["to_room"])
                moved_any = True

        if any("payloads" in payload for payload in payloads):
            return {"payloads": payloads}
        result = {"to_char": "".join(char_lines)}
        if moved_any and room is not None:
            result["to_room"] = "".join(room_lines)
            result["targets"] = room.player_targets(character)
        return result

    def _get_one(self, character: Character, room, context: Context, item, container=None):
        if (getattr(container, "owner", None) and Item.is_pc_corpse(container)
                and not self.can_loot(character, container, room)):
            return {"to_char": self._render_command_message(context, "cannot")}
        error = self._get_item_error(character, context, item, container)
        if error:
            return {"to_char": error}

        item_short = Item.short(item)
        if container is not None:
            if self._is_donation_pit(container):
                if CharacterApi.get_trust(character) < GenericUtil.to_int(getattr(item, "level", 0), 0):
                    return {"to_char": self._render_command_message(context, "pit_level")}
                if (not ItemApi.item_takeable(container, self.wear_flags)
                        and not ItemApi.has_item_flag(item, self.item_flags, "ITEM_HAD_TIMER")):
                    item.timer = 0
            item.extra_flags = GameApi.unset_bit(
                GameApi.flags_to_int(getattr(item, "extra_flags", 0)),
                CharacterApi.enum_bit(self.item_flags, "ITEM_HAD_TIMER"),
            )
            container.remove_contained_item(item)
            container_short = Item.short(container)
            to_char = self._render_command_message(context, "from_container", t=item_short, T=container_short)
            to_room = self._render_command_message(context, "from_container", channel="to_room", c=character.name, t=item_short, T=container_short)
        else:
            if room is not None:
                room.remove_item_from_room(item)
            to_char = self._render_command_message(context, "default", t=item_short)
            to_room = self._render_command_message(context, "default", channel="to_room", c=character.name, t=item_short)

        if str(getattr(item, "item_type", "")).lower() == "money":
            character.silver = GenericUtil.to_int(getattr(character, "silver", 0), 0) + GenericUtil.to_int(item.value0, 0)
            character.gold = GenericUtil.to_int(getattr(character, "gold", 0), 0) + GenericUtil.to_int(item.value1, 0)
        else:
            character.add_item(item)
        payload = {"to_char": to_char}
        if room is not None:
            payload["to_room"] = to_room
            payload["targets"] = room.player_targets(character)
        if str(getattr(item, "item_type", "")).lower() == "money":
            split = self._autosplit(character, room, context, int(item.value0), int(item.value1))
            if split is not None:
                return {"payloads": [payload, split]}
        return payload

    def _autosplit(self, character, room, context, silver, gold=0, *, sacrifice=False):
        bit = CharacterApi.enum_bit(self.PlayerActBits, "PLR_AUTOSPLIT")
        flags = getattr(getattr(character, "status_flags", None), "act", 0)
        if room is None or not bit or not CharacterApi.is_set(flags, bit):
            return None
        if silver <= 1 and (sacrifice or gold <= 0):
            return None
        argument = str(silver) if sacrifice else f"{silver} {gold}"
        split_context = Context(character=character, room=room,
                                handler_service=getattr(context, "handler_service", None),
                                command=self.registry_service.interp_registry.get(name="split"),
                                result=argument, parameters=argument.split())
        view = self.interp_api.build_interp_view(split_context)
        members = [person for person in CommunicationsApi.room_people(view)
                   if CharacterApi.is_same_group(person, character)
                   and (sacrifice or not CommunicationsApi.is_charmed(person))]
        if len(members) <= 1:
            return None
        payload = CommunicationsApi.split_money(split_context, self.interp_api)
        return {"actor": character, "context": split_context, "payloads": [payload]}

    def _get_item_error(self, character: Character, context: Context, item, container=None) -> str:
        if item is None:
            return ""
        item_short = Item.short(item)
        if not ItemApi.item_takeable(item, self.wear_flags):
            return self._render_command_message(context, "cannot_take", t=item_short)

        max_items = character.max_items()
        if max_items > 0 and character.carry_count() + Item.object_number(item) > max_items:
            return self._render_command_message(context, "carry_items", t=item_short)

        max_weight = character.max_weight()
        item_weight = Item.object_weight(item)
        carried_container = container is not None and any(obj is container for obj in character.owned_items())
        if not carried_container and max_weight > 0 and character.carry_weight() + item_weight > max_weight:
            return self._render_command_message(context, "carry_weight", t=item_short)
        if not self.can_loot(character, item, getattr(context, "room", None)):
            return self._render_command_message(context, "loot_not_permitted")
        return ""

    def can_loot(self, character, item, room=None) -> bool:
        # Registries contain persisted players and NPC prototypes too. Only room
        # occupants and playing characters correspond to ROM's live char_list.
        if not getattr(item, "owner", None):
            return True

        def owners():
            registry = getattr(self.registry_service, "character_registry", None)
            yield from list(getattr(registry, "playing", {}).values())
            all_rooms = getattr(self.room_registry, "all_rooms", None)
            rooms = all_rooms() if callable(all_rooms) else ([room] if room is not None else [])
            for current_room in rooms:
                yield from list(getattr(current_room, "characters", {}).values())
                yield from list(getattr(current_room, "mobiles", {}).values())

        return ItemApi.can_loot(character, item, owners())

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

    def do_envenom(self, character: Character, context: Context):
        room = self._prepare_envenom_context(character, context)
        payload = self._envenom_blocked_payload(context)
        if payload is not None:
            context.finish()
            return payload

        item = context.envenom_item
        if context.envenom_kind == "food":
            payload = self._finish_envenom_food(character, room, context, item)
        elif context.envenom_kind == "weapon":
            payload = self._finish_envenom_weapon(character, room, context, item)
        else:
            payload = {"to_char": self._render_command_message(context, "target_invalid", t=Item.short(item))}
        context.finish()
        return payload

    def _prepare_envenom_context(self, character: Character, context: Context):
        arg1, _ = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = getattr(context, "room", None)
        if room is None:
            room = self.room_registry.get_or_none(id=character.room_id)
        item = self._inventory_item(character, room, arg1) if arg1 else None

        context.room = room
        context.envenom_arg1 = arg1
        context.envenom_item = item
        context.envenom_item_short = "" if item is None else Item.short(item)
        context.envenom_skill_percent = self._skill_percent(character, "envenom")
        context.envenom_kind = ""
        if item is not None:
            if self._is_poisonable_food_or_drink(item):
                context.envenom_kind = "food"
            elif self._is_weapon(item):
                context.envenom_kind = "weapon"
        return room

    def _envenom_blocked_payload(self, context: Context) -> dict | None:
        item = context.envenom_item
        if not context.envenom_arg1:
            return {"to_char": self._render_command_message(context, "no_argument")}
        if item is None:
            return {"to_char": self._render_command_message(context, "target_missing")}
        if context.envenom_skill_percent < 1:
            return {"to_char": self._render_command_message(context, "target_self")}
        if context.envenom_kind == "food" and self._has_item_flags(item, "ITEM_BLESS", "ITEM_BURN_PROOF"):
            return {"to_char": self._render_command_message(context, "food_fail", t=Item.short(item))}
        if context.envenom_kind == "weapon":
            if self._has_item_flags(item, "ITEM_BLESS", "ITEM_BURN_PROOF") or self._has_weapon_flags(item, "WEAPON_FLAMING", "WEAPON_FROST", "WEAPON_VAMPIRIC", "WEAPON_SHARP", "WEAPON_VORPAL", "WEAPON_SHOCKING"):
                return {"to_char": self._render_command_message(context, "enchanted", t=Item.short(item))}
            if not self._is_edged_weapon(item):
                return {"to_char": self._render_command_message(context, "invalid_weapon")}
            if self._has_weapon_flags(item, "WEAPON_POISON"):
                return {"to_char": self._render_command_message(context, "is_envenomed", t=Item.short(item))}
        return None

    def _finish_envenom_food(self, character: Character, room, context: Context, item) -> dict:
        success = random.randint(1, 100) < context.envenom_skill_percent
        self._set_wait(character, self._skill_beats("envenom", 24))
        if success:
            if GenericUtil.to_int(getattr(item, "value3", 0), 0) == 0:
                item.value3 = "1"
                self._improve_item_skill(character, "envenom", True, multiplier=4)
            return self._envenom_payload(character, room, context, "food", item)

        if GenericUtil.to_int(getattr(item, "value3", 0), 0) == 0:
            self._improve_item_skill(character, "envenom", False, multiplier=4)
        return {"to_char": self._render_command_message(context, "food_fail", t=Item.short(item))}

    def _finish_envenom_weapon(self, character: Character, room, context: Context, item) -> dict:
        percent = random.randint(1, 100)
        self._set_wait(character, self._skill_beats("envenom", 24))
        if percent < context.envenom_skill_percent:
            self._apply_weapon_poison(character, item, percent)
            self._improve_item_skill(character, "envenom", True, multiplier=3)
            return self._envenom_payload(character, room, context, "weapon", item)

        self._improve_item_skill(character, "envenom", False, multiplier=3)
        return {"to_char": self._render_command_message(context, "weapon_fail", t=Item.short(item))}

    def _envenom_payload(self, character: Character, room, context: Context, key: str, item) -> dict:
        payload = {
            "to_char": self._render_command_message(context, key, t=Item.short(item)),
        }
        if room is not None:
            payload["to_room"] = self._render_command_message(context, key, channel="to_room", c=character.name, t=Item.short(item))
            payload["targets"] = room.player_targets(character)
        return payload

    def _apply_weapon_poison(self, character: Character, item, percent: int) -> None:
        level = GenericUtil.to_int(getattr(character, "level", 0), 0)
        effect = Effect(
            where="TO_WEAPON",
            type="spell.poison",
            level=(level * percent) // 100,
            duration=((level // 2) * percent) // 100,
            location="0",
            modifier=0,
            bitvector="WEAPON_POISON",
        )
        applied = False
        affect_to_obj = getattr(self.effect_handler, "affect_to_obj", None)
        if callable(affect_to_obj):
            try:
                affect_to_obj(item, effect)
                applied = True
            except Exception:
                applied = False
        if not applied or not self._has_weapon_flags(item, "WEAPON_POISON"):
            self._set_weapon_flag(item, "WEAPON_POISON")

    def _skill_percent(self, character: Character, skill_name: str) -> int:
        if CharacterApi.is_npc(character):
            return max(1, min(100, 40 + (2 * GenericUtil.to_int(getattr(character, "level", 0), 0))))
        if hasattr(character, "skill_level"):
            return max(0, min(100, GenericUtil.to_int(character.skill_level(skill_name), 0)))
        return 0

    def _skill_beats(self, skill_name: str, default: int = 24) -> int:
        skill = self.skill_registry.get_or_none(name=skill_name) if self.skill_registry is not None else None
        return GenericUtil.to_int(getattr(skill, "beats", default), default) if skill is not None else default

    @staticmethod
    def _is_poisonable_food_or_drink(item) -> bool:
        item_type = str(getattr(item, "item_type", "") or "").strip().lower()
        return "food" in item_type or "drink" in item_type

    @staticmethod
    def _is_weapon(item) -> bool:
        return "weapon" in str(getattr(item, "item_type", "") or "").strip().lower()

    @staticmethod
    def _is_edged_weapon(item) -> bool:
        attack = str(getattr(item, "value3", "") or "").strip()
        if attack.lstrip("-").isdigit() and int(attack) < 0:
            return False
        raw_damage = getattr(item, "damage_type", None)
        damage = str(raw_damage if raw_damage is not None else attack).strip().lower()
        if damage.lstrip("-").isdigit():
            damage_types = CharacterApi.get_enum("damageTypes")
            return int(damage) >= 0 and int(damage) != int(damage_types.DAM_BASH.value)
        blunt_names = {"bash", "dam_bash", "blast", "pound", "crush", "suction", "beating", "charge", "slap", "punch", "peckb", "smash", "thwack"}
        return bool(damage) and damage not in blunt_names

    def _has_item_flags(self, item, *flag_names: str) -> bool:
        for flag_name in flag_names:
            if ItemApi.has_item_flag(item, self.item_flags, flag_name):
                return True
        return False

    def _has_weapon_flags(self, item, *flag_names: str) -> bool:
        raw = GameApi.flags_to_int(getattr(item, "value4", 0))
        return any((raw & self._enum_bit(self.weapon_type, flag_name)) != 0 for flag_name in flag_names)

    def _set_weapon_flag(self, item, flag_name: str) -> None:
        bit = self._enum_bit(self.weapon_type, flag_name)
        if bit:
            item.value4 = str(GameApi.flags_to_int(getattr(item, "value4", 0)) | bit)

    @staticmethod
    def _enum_bit(enum_obj, name: str) -> int:
        return EnumUtil.value(enum_obj, name)

    def do_put(self, character: Character, context: Context):
        room = self._prepare_put_context(character, context)
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            context.finish()
            return blocked

        if context.put_all:
            payload = self._put_many(character, room, context)
            context.finish()
            return payload

        error_key = self._put_item_error_key(context.put_obj, context)
        if error_key:
            context.finish()
            return {"to_char": self._render_command_message(context, error_key, t=Item.short(context.put_obj))}

        context.finish()
        return self._put_one(character, room, context, context.put_obj)

    def _is_donation_pit(self, container):
        pit = getattr(self.well_known_object_vnums, "OBJ_VNUM_PIT", None)
        return pit is not None and str(getattr(container, "vnum", "")) == str(pit.value)

    def _put_one(self, character, room, context, item):
        if (not context.put_all and self._is_donation_pit(context.put_container)
                and not ItemApi.item_takeable(context.put_container, self.wear_flags)):
            if GenericUtil.to_int(getattr(item, "timer", 0), 0):
                item.extra_flags = GameApi.set_bit(
                    GameApi.flags_to_int(getattr(item, "extra_flags", 0)),
                    CharacterApi.enum_bit(self.item_flags, "ITEM_HAD_TIMER"),
                )
            else:
                item.timer = RandomNumberGenerator().number_range(100, 200)
        character.remove_item(item)
        context.put_container.add_contained_item(item)
        put_on = CharacterApi.enum_bit(self.container_state, "CONT_PUT_ON")
        key = "on" if GameApi.is_set(getattr(context.put_container, "value1", 0), put_on) else "in"
        return {
            "to_char": self._render_command_message(
                context,
                key,
                t=Item.short(item),
                T=Item.short(context.put_container),
            ),
            "to_room": self._render_command_message(
                context,
                key,
                channel="to_room",
                c=character.name,
                t=Item.short(item),
                T=Item.short(context.put_container),
            ),
            "targets": room.player_targets(character),
        }

    def _put_many(self, character, room, context):
        container = context.put_container
        wanted = context.put_arg1[4:]
        payloads = []
        for item in list(character.owned_items()):
            if context.put_arg1 != "all" and (not wanted or not all(
                    InfoUtil.look_keyword_matches(word, getattr(item, "name", "")) for word in wanted.split())):
                continue
            if not ItemUtil.can_see_object(room, character, item):
                continue
            if (character.equipped_slot_of(item) is not None
                    or GenericUtil.to_int(getattr(item, "wear_loc", -1), -1) != -1
                    or item is container):
                continue
            if self._put_item_error_key(item, context, bulk=True):
                continue

            pit = getattr(self.well_known_object_vnums, "OBJ_VNUM_PIT", None)
            # Preserve this checkout's bulk-path predicate: the item's TAKE
            # flag controls the timer, unlike single put's container predicate.
            if (pit is not None and str(getattr(container, "vnum", "")) == str(pit.value)
                    and not ItemApi.item_takeable(item, self.wear_flags)):
                if GenericUtil.to_int(getattr(item, "timer", 0), 0):
                    item.extra_flags = GameApi.set_bit(
                        GameApi.flags_to_int(getattr(item, "extra_flags", 0)),
                        CharacterApi.enum_bit(self.item_flags, "ITEM_HAD_TIMER"),
                    )
                else:
                    item.timer = RandomNumberGenerator().number_range(100, 200)
            payloads.append(self._put_one(character, room, context, item))
        return {"payloads": payloads}

    def _prepare_put_context(self, character: Character, context: Context):
        arg1, rem = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = getattr(context, "room", None)
        if room is None:
            room = self.room_registry.get_or_none(id=character.room_id)

        context.room = room
        context.put_room = room
        context.put_arg1 = arg1.lower()
        context.put_rem = rem
        context.put_all = context.put_arg1 == "all" or context.put_arg1.startswith("all.")
        context.put_container_name = rem.split()[0] if rem else ""
        context.put_obj = self._inventory_item(character, room, arg1) if arg1 and not context.put_all else None
        context.put_container = self._here_item(character, room, context.put_container_name) if context.put_container_name else None
        return room

    def _put_item_error_key(self, item, context: Context, *, bulk: bool = False) -> str:
        if item is None:
            return ""
        if (ItemApi.has_item_flag(item, self.item_flags, "ITEM_NODROP")
                and not CharacterApi.is_immortal(context.character)):
            return "target_no_drop"
        if Item.weight_multiplier(item) != 100:
            return "weight_exceeds"
        container = context.put_container
        weight = Item.object_weight(item)
        item_limit = GenericUtil.to_int(container.value3, 0) * 10
        if (weight + Item.true_weight(container) > GenericUtil.to_int(container.value0, 0) * 10
                or (weight >= item_limit if bulk else weight > item_limit)):
            return "container_full"
        return ""

    def do_drop(self, character: Character, context: Context):
        room = self._prepare_drop_context(character, context)
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            context.finish()
            return blocked

        if context.drop_is_money:
            payload = self._drop_money(character, room, context)
        elif context.drop_all:
            payload = self._drop_all(character, room, context, context.arg1)
        else:
            payload = self._drop_one(character, room, context, context.drop_item)
        context.finish()
        return payload

    def _prepare_drop_context(self, character: Character, context: Context):
        arg1, remainder = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = getattr(context, "room", None)
        if room is None:
            room = self.room_registry.get_or_none(id=character.room_id)

        context.arg1 = arg1
        context.drop_room = room
        context.drop_all = arg1 == "all" or arg1.startswith("all.")
        context.drop_is_money = bool(arg1 and (arg1[1:] if arg1[:1] in ("+", "-") else arg1).isascii()
                                     and (arg1[1:] if arg1[:1] in ("+", "-") else arg1).isdigit())
        context.drop_amount = int(arg1) if context.drop_is_money else 0
        denomination, _ = ItemUtil.parse_raw_arguments(remainder, [])
        context.drop_currency = "silver" if denomination in ("coin", "coins", "silver") else denomination
        context.drop_invalid_money = context.drop_is_money and (context.drop_amount <= 0 or context.drop_currency not in ("silver", "gold"))
        context.drop_insufficient_money = (context.drop_is_money and not context.drop_invalid_money
                                           and int(getattr(character, context.drop_currency, 0) or 0) < context.drop_amount)
        context.drop_item = None if context.drop_is_money or context.drop_all or not arg1 else self._inventory_item(character, room, arg1)
        context.drop_no_drop = bool(context.drop_item is not None and ItemApi.has_item_flag(context.drop_item, self.item_flags, "ITEM_NODROP"))
        return room

    def _drop_money(self, character, room, context):
        silver = context.drop_amount if context.drop_currency == "silver" else 0
        gold = context.drop_amount if context.drop_currency == "gold" else 0
        enums = self.well_known_object_vnums
        piles = []
        for item in list(room.contents.values()):
            vnum = GenericUtil.to_int(getattr(item, "vnum", 0), 0)
            if vnum == enums.OBJ_VNUM_SILVER_ONE.value:
                silver += 1
            elif vnum == enums.OBJ_VNUM_GOLD_ONE.value:
                gold += 1
            elif vnum == enums.OBJ_VNUM_SILVER_SOME.value:
                silver += int(item.value0)
            elif vnum == enums.OBJ_VNUM_GOLD_SOME.value:
                gold += int(item.value1)
            elif vnum == enums.OBJ_VNUM_COINS.value:
                silver += int(item.value0)
                gold += int(item.value1)
            else:
                continue
            piles.append(item)
        money = ItemUtil.create_money(gold, silver, self.item_registry, enums)
        setattr(character, context.drop_currency, int(getattr(character, context.drop_currency, 0) or 0) - context.drop_amount)
        for item in piles:
            room.remove_item_from_room(item)
        room.add_item_to_room(money)
        return {"to_char": self._render_command_message(context, "coins"),
                "to_room": self._render_command_message(context, "coins", channel="to_room", c=character.name),
                "targets": room.player_targets(character)}

    def _drop_all(self, character: Character, room, context: Context, arg1: str):
        wanted = arg1[4:].strip().lower() if arg1.startswith("all.") else ""
        dropped = []
        room_lines = []
        char_lines = []

        for item in list(getattr(character, "loot", []) or []):
            if not ItemUtil.can_see_object(room, character, item):
                continue
            if character.equipped_slot_of(item):
                continue
            if ItemApi.has_item_flag(item, self.item_flags, "ITEM_NODROP"):
                continue
            name = str(getattr(item, "name", "") or "").strip().lower()
            if wanted and not LookupUtil.matches(wanted, name):
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

    def _haggle_skill_percent(self, character):
        if CharacterApi.is_npc(character):
            return 0
        skill = self.skill_registry.get_or_none(name="haggle")
        class_name = str(getattr(getattr(character, "character_class", None), "name", "") or "").lower()
        required = (getattr(skill, "level_by_class", {}) or {}).get(class_name, 0)
        if GenericUtil.to_int(getattr(character, "level", 0), 0) < GenericUtil.to_int(required, 0):
            return 0
        percent = self._skill_percent(character, "haggle")
        flags = getattr(character, "status_flags", None)
        if GenericUtil.to_int(getattr(flags, "pulse_daze", 0), 0) > 0:
            percent = 2 * percent // 3
        if GenericUtil.to_int(getattr(flags, "drunk", 0), 0) > 10:
            percent = 9 * percent // 10
        return percent

    def _haggle_transaction(self, character, context, transaction):
        # ROM consumes a roll even for unskilled actors and SELL_EXTRACT items.
        roll = RandomNumberGenerator().number_percent()
        item = None if transaction == "pet" else (context.sell_obj if transaction == "sell" else context.buy_item)
        if item is not None and ItemApi.has_item_flag(item, self.item_flags, "ITEM_SELL_EXTRACT"):
            return ""
        if roll >= self._haggle_skill_percent(character):
            return ""
        if transaction == "sell":
            context.sell_cost = context.sell_shop.haggle_sale_price(context.sell_cost, item, context.sell_keeper, roll)
            context.sell_gold, context.sell_silver = divmod(context.sell_cost, 100)
            context.sell_suffix = "" if context.sell_cost == 1 else "s"
            message = self._render_command_message(context, "haggle_success")
        else:
            base_cost = context.buy_cost if transaction == "pet" else GenericUtil.to_int(item.cost, 0)
            context.buy_cost = Shop.haggle_purchase_price(context.buy_cost, base_cost, roll)
            context.buy_total_cost = context.buy_cost * context.buy_quantity
            message = self._render_command_message(
                context, "haggle_pet" if transaction == "pet" else "haggle_success",
                q=context.buy_cost, t=getattr(context.buy_keeper, "short_description", ""))
        self._improve_item_skill(character, "haggle", True, multiplier=4)
        return message

    def _finish_buy_item(self, character: Character, room, context: Context):
        haggle = self._haggle_transaction(character, context, "buy")
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
                "to_char": haggle + self._render_command_message(context, "bulk_purchased", t=context.buy_item_short, d=context.buy_quantity, q=context.buy_total_cost),
                "to_room": self._render_command_message(context, "bulk_purchased", channel="to_room", c=character.name, t=context.buy_item_short, d=context.buy_quantity),
                "targets": room.player_targets(character),
            }
        return {
            "to_char": haggle + self._render_command_message(context, "default", t=context.buy_item_short, q=context.buy_cost),
            "to_room": self._render_command_message(context, "item_purchased", channel="to_room", c=character.name, t=context.buy_item_short),
            "targets": room.player_targets(character),
        }

    def _finish_buy_pet(self, character: Character, room, context: Context):
        haggle = self._haggle_transaction(character, context, "pet")
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
        character_registry = getattr(self.registry_service, "character_registry", None)
        if character_registry is not None:
            character_registry.register(pet)
        return {
            "to_char": haggle + self._render_command_message(context, "pet_purchased"),
            "to_room": self._render_command_message(context, "pet_purchased", channel="to_room", c=character.name, t=getattr(pet, "short_description", "a pet")),
            "targets": room.player_targets(character),
        }

    def _shop_carried_item(self, character, room, selector):
        return self._inventory_item(character, room, selector)

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
        context.sell_keeper_cannot_see_item = False

        if not raw or room is None:
            return room

        keeper, shop, error = self._find_keeper(character, room)
        context.sell_keeper = keeper
        context.sell_shop = shop
        context.sell_keeper_error = error
        if keeper is None or shop is None:
            return room

        obj = self._shop_carried_item(character, room, raw)
        context.sell_obj = obj
        if obj is None:
            return room

        context.sell_no_drop = ItemApi.has_item_flag(obj, self.item_flags, "ITEM_NODROP")
        context.sell_keeper_cannot_see_item = not ItemUtil.can_see_object(room, keeper, obj)
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
        context.value_keeper_cannot_see_item = False
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

        obj = self._shop_carried_item(character, room, raw)
        context.value_item = obj
        if obj is None:
            return room

        context.value_no_drop = ItemApi.has_item_flag(obj, self.item_flags, "ITEM_NODROP")
        context.value_keeper_cannot_see_item = not ItemUtil.can_see_object(room, keeper, obj)
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
        context.item = self._room_item(character, room, context.arg1) if room is not None else None
        context.item_name = Item.short(context.item) if context.item is not None else None
        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get('blocked'):
            context.finish()
            return payload

        silver = ItemUtil.sacrifice_silver_value(context.item)
        item_name = Item.short(context.item)
        room.remove_item_from_room(context.item)
        character.silver = int(getattr(character, "silver", 0) or 0) + silver
        context.finish()
        payload = self.interp_api.render_message_key(context, "default", c=character.name, t=item_name)
        reward = self.interp_api.render_message_key(
            context,
            "one_silver" if silver == 1 else "multiple_silver",
            channel="to_char",
            d=str(silver),
        )
        split = self._autosplit(character, room, context, silver, sacrifice=True)
        if split is None:
            payload.update(reward)
        if room is not None and payload.get("to_room"):
            payload["targets"] = room.player_targets(character)
        if split is not None:
            return {"payloads": [reward, split, payload]}
        return payload

    def destroy_carried(self, character: Character, context: Context, empty_msg: str, success_msg: str = "Ok.\r\n"):
        arg1, _ = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        if not arg1:
            context.finish()
            return {"to_char": empty_msg}
        room = context.room if context.room is not None else self.room_registry.get_or_none(id=character.room_id)
        item = self._inventory_item(character, room, arg1)
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

            victim = self._find_give_target(room, victim_name, character)
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
        item = self._inventory_item(character, room, arg1) if arg1 else None
        victim = self._find_give_target(room, victim_name, character)
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
        if max_items > 0 and victim.carry_count() + Item.object_number(item) > max_items:
            context.give_target_hands_full = True

        max_weight = victim.max_weight()
        item_weight = Item.object_weight(item)
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

    def _find_give_target(self, room, wanted: str, observer=None):
        return LookupUtil.character(room, observer, wanted,
                                    visible=lambda target: self._can_see(observer, target, room))

    def _is_shopkeeper(self, victim) -> bool:
        if victim is None:
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

    def do_steal(self, character: Character, context: Context):
        room = self._prepare_steal_context(character, context)
        payload = self._steal_blocked_payload(character, room, context)
        if payload is not None:
            context.finish()
            return payload

        self._set_wait(character, self._steal_beats())

        if not self._steal_succeeds(character, context.steal_victim, room):
            payload = self._finish_steal_failure(character, room, context)
            context.finish()
            return payload

        if context.steal_is_money:
            payload = self._finish_steal_money(character, context)
        else:
            self._prepare_steal_item_context(character, context)
            payload = self._steal_item_blocked_payload(context)
            if payload is not None:
                context.finish()
                return payload
            payload = self._finish_steal_item(character, context)
        context.finish()
        return payload

    def _prepare_steal_context(self, character: Character, context: Context):
        raw = (context.result if isinstance(context.result, str) else "").strip()
        if not raw and context.parameters:
            raw = " ".join(context.parameters).strip()
        arg1, rest = InterpUtil.one_argument(raw)
        arg2, _tail = InterpUtil.one_argument(rest)
        room = getattr(context, "room", None)
        if room is None:
            room = self.room_registry.get_or_none(id=character.room_id)

        victim = self._find_give_target(room, arg2, character)
        context.room = room
        context.steal_raw = raw
        context.steal_item_name = str(arg1 or "").strip().lower()
        context.steal_victim_name = arg2
        context.steal_victim = victim
        context.steal_is_money = str(arg1 or "").strip().lower() in {"coin", "coins", "gold", "silver"}
        context.steal_item = None
        context.steal_item_short = ""
        context.steal_no_drop = False
        context.steal_inventory_full = False
        context.steal_encumbered = False

        return room

    def _prepare_steal_item_context(self, character, context):
        victim = context.steal_victim
        if victim is not None:
            item = self._inventory_item(victim, context.room, context.steal_item_name, observer=character)
            context.steal_item = item
            context.steal_item_short = Item.short(item) if item is not None else ""
            if item is not None:
                context.steal_no_drop = bool(
                    (ItemApi.has_item_flag(item, self.item_flags, "ITEM_NODROP")
                     and not CharacterApi.is_immortal(character))
                    or ItemApi.has_item_flag(item, self.item_flags, "ITEM_INVENTORY")
                    or GenericUtil.to_int(getattr(item, "level", 0), 0) > GenericUtil.to_int(getattr(character, "level", 0), 0)
                )
                max_items = character.max_items() if hasattr(character, "max_items") else 0
                if max_items > 0 and character.carry_count() + Item.object_number(item) > max_items:
                    context.steal_inventory_full = True

                max_weight = character.max_weight() if hasattr(character, "max_weight") else 0
                item_weight = Item.object_weight(item)
                if max_weight > 0 and ItemApi.carried_weight(character, include_coins=False) + item_weight > max_weight:
                    context.steal_encumbered = True

    def _steal_blocked_payload(self, character: Character, room, context: Context) -> dict | None:
        if not context.steal_item_name or not context.steal_victim_name:
            return {"to_char": self._render_command_message(context, "no_argument")}

        victim = context.steal_victim
        if victim is None:
            return {"to_char": self._render_command_message(context, "target_missing")}
        if victim is character:
            return {"to_char": self._render_command_message(context, "target_self")}

        safe_payload = self._steal_safe_payload(character, victim, room)
        if safe_payload is not None:
            return safe_payload

        if CharacterApi.is_npc(victim) and getattr(victim, "fighting", None) is not None:
            return {"to_char": self._render_command_message(context, "no_kill_stealing")}
        return None

    def _steal_item_blocked_payload(self, context) -> dict | None:
        if context.steal_item is None:
            return {"to_char": self._render_command_message(context, "inventory_item_missing")}
        if context.steal_no_drop:
            return {"to_char": self._render_command_message(context, "no_drop")}
        if context.steal_inventory_full:
            return {"to_char": self._render_command_message(context, "inventory_full")}
        if context.steal_encumbered:
            return {"to_char": self._render_command_message(context, "encumbered")}
        return None

    def _steal_safe_payload(self, character: Character, victim, room) -> dict | None:
        checker = getattr(self.fight_handler, "is_safe", None)
        if not callable(checker):
            return None
        try:
            safe, message = checker(character, victim, room=room)
        except TypeError:
            safe, message = checker(character, victim)
        if not safe:
            return None
        return {"to_char": CommunicationsUtil.ensure_message_break(message or "You cannot do that here.")}

    def _steal_succeeds(self, character: Character, victim, room) -> bool:
        if CharacterApi.is_npc(character):
            return True

        percent = random.randint(1, 100)
        if not self._is_awake(victim):
            percent -= 10
        elif not self._can_see(victim, character, room):
            percent += 25
        else:
            percent += 50

        if not CharacterApi.is_npc(victim):
            level_delta = abs(GenericUtil.to_int(getattr(character, "level", 0), 0) - GenericUtil.to_int(getattr(victim, "level", 0), 0))
            if level_delta > 7:
                return False
        return percent <= self._steal_skill_percent(character) and CharacterApi.is_clan(character)

    def _finish_steal_failure(self, character: Character, room, context: Context) -> dict:
        victim = context.steal_victim
        self.effect_handler.affect_strip(character, "sneak")
        self.effect_handler.affect_strip(character, "skill.sneak")
        CharacterApi.set_affected_by_name(character, self.affected_bits, "AFF_SNEAK", False)
        payload = {
            "to_char": self._render_command_message(context, "failed"),
            "to_room": self._render_command_message(context, "failed", channel="to_room", c=character.name, t=getattr(victim, "name", "")),
            "targets": self._room_targets_except(room, character, victim),
        }
        if not CharacterApi.is_npc(victim):
            payload["to_victim"] = self._render_command_message(context, "failed", channel="to_victim", c=character.name)
            payload["victim"] = victim
        payloads = [payload]
        reaction = ("fail_message_one", "fail_message_two", "fail_message_robbed", "fail_message_three")[random.randint(0, 3)]
        text = self._render_command_message(context, reaction, channel="to_room", c=character.name).strip()
        player_handler = context.player_handler()
        if not self._is_awake(victim):
            stand_context = self._theft_reaction_context(context, victim, "stand", "")
            stand = player_handler.movement_commands.do_stand(victim, stand_context)
            payloads.append({"actor": victim, "context": stand_context, "payloads": [stand]})
        if self._is_awake(victim):
            yell_context = self._theft_reaction_context(context, victim, "yell", text)
            yell = player_handler.communications_commands.do_yell(yell_context)
            payloads.append({"actor": victim, "context": yell_context, "payloads": [yell]})
        if not CharacterApi.is_npc(character) and CharacterApi.is_npc(victim):
            self._improve_item_skill(character, "steal", False)
            result = self.fight_handler.multi_hit(victim, character, dt="TYPE_UNDEFINED")
            fight_payload = self.fight_handler.build_round_payload(victim, character, room, result)
            payloads.append({"actor": victim, "payloads": [fight_payload]})
        if not CharacterApi.is_npc(character) and not CharacterApi.is_npc(victim):
            payloads.append({"to_wiznet": self._render_command_message(
                context, "default", channel="to_wiznet", c=character.name, t=getattr(victim, "name", ""))})
            if self._mark_player_thief(character):
                payloads.append({"to_char": self._render_command_message(context, "thief")})
                self.fight_handler.character_service.queue_save_character(character)
        return {"payloads": payloads}

    def _theft_reaction_context(self, context, victim, name, argument):
        return Context(character=victim, command=self.registry_service.interp_registry.get(name=name),
                       handler_service=getattr(context, "handler_service", None), room=context.room,
                       parameters=argument.split(), result=argument)

    def _finish_steal_money(self, character: Character, context: Context) -> dict:
        victim = context.steal_victim
        level = max(1, GenericUtil.to_int(getattr(character, "level", 1), 1))
        max_level = self._max_level()
        gold = GenericUtil.to_int(getattr(victim, "gold", 0), 0) * random.randint(1, level) // max_level
        silver = GenericUtil.to_int(getattr(victim, "silver", 0), 0) * random.randint(1, level) // max_level
        if gold <= 0 and silver <= 0:
            return {"to_char": self._render_command_message(context, "failed_coins")}

        character.gold = GenericUtil.to_int(getattr(character, "gold", 0), 0) + gold
        character.silver = GenericUtil.to_int(getattr(character, "silver", 0), 0) + silver
        victim.gold = max(0, GenericUtil.to_int(getattr(victim, "gold", 0), 0) - gold)
        victim.silver = max(0, GenericUtil.to_int(getattr(victim, "silver", 0), 0) - silver)
        self._improve_item_skill(character, "steal", True)

        if silver <= 0:
            return {"to_char": self._render_command_message(context, "gold", d=gold)}
        if gold <= 0:
            return {"to_char": self._render_command_message(context, "silver", d=silver)}
        return {"to_char": self._render_command_message(context, "coins", d=silver, g=gold)}

    def _finish_steal_item(self, character: Character, context: Context) -> dict:
        item = context.steal_item
        context.steal_victim.remove_item(item)
        character.add_item(item)
        self._improve_item_skill(character, "steal", True)
        return {"to_char": self._render_command_message(context, "item", t=Item.short(item))}

    def _steal_skill_percent(self, character: Character) -> int:
        if hasattr(character, "skill_level"):
            return max(1, min(100, GenericUtil.to_int(character.skill_level("steal"), 1)))
        return max(1, min(100, 40 + (2 * GenericUtil.to_int(getattr(character, "level", 0), 0))))

    def _steal_beats(self) -> int:
        return self._skill_beats("steal", 24)

    @staticmethod
    def _set_wait(character: Character, pulses: int) -> None:
        status_flags = getattr(character, "status_flags", None)
        if status_flags is not None:
            status_flags.pulse_wait = max(GenericUtil.to_int(getattr(status_flags, "pulse_wait", 0), 0), GenericUtil.to_int(pulses, 0))

    @staticmethod
    def _can_see(viewer, target, room) -> bool:
        try:
            return CharacterApi.can_see(viewer, target, room)
        except TypeError:
            return CharacterApi.can_see(viewer, target)

    @staticmethod
    def _is_awake(entity) -> bool:
        checker = getattr(CharacterApi, "is_awake", None)
        if callable(checker):
            return checker(entity)
        return GenericUtil.to_int(getattr(entity, "position", 8), 8) > 4

    @staticmethod
    def _room_targets_except(room, character, victim) -> list:
        if room is None:
            return []
        excluded = {getattr(character, "id", ""), getattr(victim, "id", "")}
        return [target for target in room.player_targets(character) if getattr(target, "id", "") not in excluded]

    def _mark_player_thief(self, character: Character) -> bool:
        bit = CharacterApi.enum_bit(self.PlayerActBits, "PLR_THIEF")
        if bit <= 0 or getattr(character, "status_flags", None) is None:
            return False
        current = GenericUtil.to_int(getattr(character.status_flags, "act", 0), 0)
        if CharacterApi.is_set(current, bit):
            return False
        if hasattr(CharacterApi, "set_act_flags"):
            CharacterApi.set_act_flags(character, bit)
        else:
            character.status_flags.act = current | bit
        return True

    def _max_level(self) -> int:
        value = getattr(getattr(self, "GameParameters", None), "MAX_LEVEL", None)
        return max(1, GenericUtil.to_int(getattr(value, "value", value), 60))

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
            result = Equipped.wear_all(character, self.wear_flags, self.item_flags, effect_handler=self.effect_handler,
                                       visible=lambda item: ItemUtil.can_see_object(room, character, item))
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
        item = None if arg1 == "all" else self._inventory_item(character, room, arg1)

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

        def _render(key, **kwargs):
            normalized = next(iter(GenericUtil.camel_to_snake_case({key: ""})))
            return self.interp_api.render_message_key(context, normalized, **kwargs)

        def _append(rendered: dict):
            text = str(rendered.get("to_char", "") or "")
            if text:
                payload["to_char"] = f"{payload.get('to_char', '')}{text}"
            room_text = str(rendered.get("to_room", "") or "")
            if room_text:
                payload["to_room"] = f"{payload.get('to_room', '')}{room_text}"

        for key, tokens in list(getattr(result, "pre_messages", []) or []):
            _append(_render(key, channel="to_char", **dict(tokens or {})))
        if getattr(result, "blocked_key", ""):
            payload["blocked_key"] = result.blocked_key
            _append(_render(result.blocked_key, **dict(getattr(result, "blocked_tokens", {}) or {})))
        for key, tokens in list(getattr(result, "shared_messages", []) or []):
            _append(_render(key, **dict(tokens or {})))
        for key, tokens in list(getattr(result, "char_messages", []) or []):
            _append(_render(key, channel="to_char", **dict(tokens or {})))

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
        slot, item = equipped.find_remove_target(arg1, visible=lambda obj: ItemUtil.can_see_object(room, character, obj))

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
    def _gain_condition(character: Character, name: str, amount: int, messages=None) -> int:
        status_flags = getattr(character, "status_flags", None)
        if status_flags is None or not hasattr(status_flags, name):
            return -1
        current = GenericUtil.to_int(getattr(status_flags, name, -1), -1)
        if current == -1:
            return -1
        if amount == 0 or CharacterApi.is_npc(character) or CharacterApi.is_immortal(character):
            return current
        gain = getattr(character, "gain_condition", None)
        if callable(gain):
            message = gain(name, int(amount))
            if messages is not None and message:
                messages.append(message)
            return GenericUtil.to_int(getattr(status_flags, name, -1), -1)
        updated = max(0, min(48, current + int(amount)))
        setattr(status_flags, name, updated)
        return updated

    def do_drink(self, character: Character, context: Context):
        arg1, _ = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = context.room if context.room is not None else self.room_registry.get_or_none(id=character.room_id)
        context.room = room
        item = self._here_item(character, room, arg1) if arg1 else None
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

        if not CharacterApi.is_npc(character):
            def scaled_gain(index, divisor):
                numerator = amount * GenericUtil.to_int(liquid_affect[index], 0) if len(liquid_affect) > index else 0
                return (1 if numerator >= 0 else -1) * (abs(numerator) // divisor)

            drunk_gain = scaled_gain(0, 36)
            full_gain = scaled_gain(1, 4)
            thirst_gain = scaled_gain(2, 10)
            hunger_gain = scaled_gain(3, 2)

            condition_messages = []
            drunk = self._gain_condition(character, "drunk", drunk_gain, condition_messages)
            full = self._gain_condition(character, "fullness", full_gain, condition_messages)
            thirst = self._gain_condition(character, "thirst", thirst_gain, condition_messages)
            self._gain_condition(character, "hunger", hunger_gain, condition_messages)
            payload["to_char"] += "".join(condition_messages)
            self.logger.debug(f"Drunk: {drunk}, Full: {full}, Thirst: {thirst}")
            self.logger.debug(f"drunk_gain: {drunk_gain}; thirst_gain: {thirst_gain}; full_gain: {full_gain}; hunger_gain: {hunger_gain}")
            if drunk > 10:
                payload["to_char"] += self._render_command_message(context, "alcohol")
            if full > 40:
                payload["to_char"] += self._render_command_message(context, "full")
            if thirst > 40:
                payload["to_char"] += self._render_command_message(context, "quenched")
        if GenericUtil.to_int(getattr(item, "value3", 0), 0) != 0:
            self._apply_consumed_poison(character, context, payload, amount, 3 * amount)
        if GenericUtil.to_int(getattr(item, "value0", 0), 0) > 0:
            item.value1 = str(GenericUtil.to_int(getattr(item, "value1", 0), 0) - amount)
        context.finish()
        return payload

    def do_eat(self, character: Character, context: Context):
        room = context.room if context.room is not None else self.room_registry.get_or_none(id=character.room_id)
        arg1, _ = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        item = self._inventory_item(character, room, arg1)
        context.eat_arg1 = arg1
        context.eat_item = item
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked

        item_type = (getattr(item, "item_type", "") or "").upper()
        payload = {
            "to_char": self._render_command_message(context, "default", "to_char", p=Item.short(item)),
        }
        room = context.room if context.room is not None else self.room_registry.get_or_none(id=character.room_id)
        context.room = room
        if room is not None:
            payload["to_room"] = self._render_command_message(context, "default", "to_room", c=character.name, p=Item.short(item))
            payload["targets"] = room.player_targets(character)

        if "FOOD" in item_type and not CharacterApi.is_npc(character):
            hunger_before = self._condition_value(character, "hunger")
            condition_messages = []
            self._gain_condition(character, "fullness", GenericUtil.to_int(getattr(item, "value0", 0), 0), condition_messages)
            hunger_after = self._gain_condition(character, "hunger", GenericUtil.to_int(getattr(item, "value1", 0), 0), condition_messages)
            payload["to_char"] += "".join(condition_messages)
            if hunger_before == 0 and hunger_after > 0:
                payload["to_char"] += self._render_command_message(context, "satiated")
            elif self._condition_value(character, "fullness") > 40:
                payload["to_char"] += self._render_command_message(context, "full")

        spell_payloads = []
        if "FOOD" in item_type and GenericUtil.to_int(getattr(item, "value3", 0), 0) != 0:
            potency = GenericUtil.to_int(getattr(item, "value0", 0), 0)
            self._apply_consumed_poison(character, context, payload, potency, 2 * potency)
        elif "PILL" in item_type:
            for spell_ref in Item.spell_refs(item, 1, 2, 3):
                spell_payloads.extend(self._cast_item_spell(
                    character, room, item, spell_ref,
                    target=character, target_name=character.name, target_kind="char", command_context=context,
                ))

        slot = character.equipped_slot_of(item)
        if slot:
            self.effect_handler.remove_item_effects(character, item)
            character.unequip_item(slot)
        character.remove_item(item)
        context.finish()
        if "PILL" in item_type:
            return {"payloads": [payload, *spell_payloads]}
        return payload

    def _apply_consumed_poison(self, character, context, payload, potency: int, duration: int) -> None:
        """Food/drink poison joins existing poison without a saving throw."""
        effect = Effect(
            where="TO_AFFECTS",
            type="spell.poison",
            level=RandomNumberGenerator().number_fuzzy(potency),
            duration=duration,
            location="APPLY_NONE",
            modifier=0,
            bitvector="AFF_POISON",
            apply_to="char",
        )
        self.effect_handler.affect_join(character, effect)
        payload["to_char"] += self._render_command_message(context, "poison")
        if context.room is not None:
            payload["to_room"] = payload.get("to_room", "") + self._render_command_message(
                context, "poison", channel="to_room", c=character.name,
            )

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

        dest = self._inventory_item(character, room, arg1) if arg1 else None
        src_name = rem.split()[0] if rem else ""
        src = self._here_item(character, room, src_name) if src_name else None
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
        source = self._inventory_item(character, room, arg1) if arg1 else None
        target_item = None
        target_character = None
        target_container = None
        preview = None

        if target_arg and target_arg.lower() != "out":
            target_item = self._here_item(character, room, target_arg)
            if target_item is None:
                target_character = self._find_give_target(room, target_arg, character)
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
        item = self._inventory_item(character, room, arg1) if arg1 else None
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
            payloads.extend(self._cast_item_spell(character, room, item, spell_ref, target=character, target_name=character.name, target_kind="char", command_context=context))

        self._destroy_item(character, item)
        context.finish()
        return {"payloads": payloads}

    def do_recite(self, character: Character, context: Context):
        arg1, rem = ItemUtil.parse_raw_arguments(context.result, context.parameters)
        room = context.room if context.room is not None else self.room_registry.get_or_none(id=character.room_id)
        scroll = self._inventory_item(character, room, arg1) if arg1 else None
        target_name = rem.split()[0] if rem else ""
        target = character if not target_name else self._find_give_target(room, target_name, character)
        if target is None and target_name:
            target = self._here_item(character, room, target_name)

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
                payloads.extend(self._cast_item_spell(character, room, scroll, spell_ref, target=target, target_name=target_name, target_kind=target_kind, command_context=context))
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
                    payloads.extend(self._cast_item_spell(character, room, staff, spell, target=victim, target_name=getattr(victim, "name", ""), target_kind="char", command_context=context))
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
        victim = getattr(character, "fighting", None) if not arg1 else self._find_give_target(room, arg1, character)
        obj = None if victim is not None else self._here_item(character, room, arg1)

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
                        command_context=context,
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

    def _improve_item_skill(self, character: Character, skill_name: str, success: bool, multiplier: int = 2):
        skill = self.skill_registry.get_or_none(name=skill_name)
        if skill is None:
            return
        Ability.check_improve(character, getattr(skill, "id", ""), success, multiplier)

    def _cast_item_spell(self, character: Character, room, item, spell_ref, *, target=None, target_name: str = "", target_kind: str = "", command_context=None) -> list[dict]:
        spell = spell_ref
        if spell is None or not hasattr(spell, "handler_id"):
            spell = FightUtil.find_spell(self.spell_registry, getattr(spell_ref, "name", spell_ref))
        if spell is None:
            return []

        victim = target if target is not None and not hasattr(target, "item_type") else None
        obj = target if target is not None and hasattr(target, "item_type") else None
        target_type = str(getattr(spell, "target", "") or "").upper().removeprefix("TAR_")
        if target_type == "IGNORE":
            target, target_kind = None, ""
        elif target_type in ("CHAR_DEFENSIVE", "CHAR_SELF"):
            target, target_kind = victim if victim is not None else character, "char"
        elif target_type == "OBJ_INV":
            target, target_kind = obj, "obj"
        elif target_type == "CHAR_OFFENSIVE":
            target = victim if victim is not None else getattr(character, "fighting", None)
            target_kind = "char"
        elif target_type in ("OBJ_CHAR_OFF", "OBJ_CHAR_DEF"):
            target = victim if victim is not None else obj
            if target is None:
                target = getattr(character, "fighting", None) if target_type == "OBJ_CHAR_OFF" else character
            target_kind = "obj" if target is not None and hasattr(target, "item_type") else "char"
        else:
            self.logger.error(f"Item spell has invalid target type: {target_type}")
            return []

        if target is None and target_type != "IGNORE":
            return [{"to_char": self._render_command_message(command_context, "item_spell_target_missing")}]
        if target_kind == "char" and target is not character:
            safe, notice = False, ""
            if target_type == "CHAR_OFFENSIVE":
                safe, notice = self.fight_handler.is_safe(character, target, room=room)
            elif target_type == "OBJ_CHAR_OFF":
                safe = self.fight_handler.is_safe_spell(character, target, area=False)
            if safe:
                return [{"to_char": CommunicationsUtil.ensure_message_break(notice or "")
                         + self._render_command_message(command_context, "item_spell_unsafe")}]

        context = SpellContext(
            actor=character,
            spell=spell,
            handler=self,
            room=room,
            target=target,
            target_name="",
            target_kind=target_kind,
            cast_level=Item.spell_level(item),
            source="player",
            command_context=command_context,
        )
        self.spell_api.execute_lambdas(context)
        self._item_spell_retaliation(context, target_type)
        return list(context.payloads)

    def _item_spell_retaliation(self, context, target_type):
        victim, actor = context.victim, context.actor
        if (target_type not in ("CHAR_OFFENSIVE", "OBJ_CHAR_OFF") or victim is None
                or victim is actor or getattr(victim, "master", None) is actor
                or getattr(victim, "fighting", None) is not None):
            return
        room = context.room
        if room is not None and str(getattr(actor, "room_id", "")) != str(room.id):
            room = self.room_registry.get_or_none(id=actor.room_id)
        if room is None or not any(person is victim for person in LookupUtil.people(room)):
            return
        notice = self.fight_handler.check_killer(victim, actor)
        result = self.fight_handler.multi_hit(victim, actor, dt="TYPE_UNDEFINED")
        attack = self.fight_handler.build_round_payload(victim, actor, room, result)
        context.queue_payload({"actor": victim, "payloads": [*([notice] if notice else []), attack]})

    def _inventory_item(self, character, room, selector, *, observer=None):
        observer = character if observer is None else observer
        return LookupUtil.inventory(character, selector,
                                    visible=lambda item: ItemUtil.can_see_object(room, observer, item))

    def _room_item(self, character, room, selector):
        return LookupUtil.find(list(getattr(room, "contents", {}).values()), selector,
                               visible=lambda item: ItemUtil.can_see_object(room, character, item))

    def _here_item(self, character, room, selector):
        return LookupUtil.here(character, room, selector,
                               visible=lambda item: ItemUtil.can_see_object(room, character, item))

    @staticmethod
    def _destroy_item(character: Character, item) -> None:
        if item is None:
            return
        slot = character.equipped_slot_of(item) if hasattr(character, "equipped_slot_of") else None
        if slot:
            character.unequip_item(slot)
        character.remove_item(item)

    def _find_keeper(self, character: Character, room):
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

    def _find_healer(self, room):
        if room is None:
            return None
        healer_bit = CharacterApi.enum_bit(self.act_bits, "ACT_IS_HEALER")
        for mob in getattr(room, "mobiles", {}).values():
            act = GenericUtil.to_int(getattr(getattr(mob, "status_flags", None), "act", 0), 0)
            if healer_bit and CharacterApi.is_set(act, healer_bit):
                return mob
        return None

    @staticmethod
    def _healer_service(argument: str) -> dict | None:
        query = str(argument or "").strip().lower()
        if not query:
            return None
        services = [
            {"aliases": ("light",), "spell": "cure light", "cost": 1000, "words": "judicandus dies"},
            {"aliases": ("serious",), "spell": "cure serious", "cost": 1600, "words": "judicandus gzfuajg"},
            {"aliases": ("critical", "critic"), "spell": "cure critical", "cost": 2500, "words": "judicandus qfuhuqar"},
            {"aliases": ("heal",), "spell": "heal", "cost": 5000, "words": "pzar"},
            {"aliases": ("blindness", "blind"), "spell": "cure blindness", "cost": 2000, "words": "judicandus noselacri"},
            {"aliases": ("disease",), "spell": "cure disease", "cost": 1500, "words": "judicandus eugzagz"},
            {"aliases": ("poison",), "spell": "cure poison", "cost": 2500, "words": "judicandus sausabru"},
            {"aliases": ("uncurse", "curse"), "spell": "remove curse", "cost": 5000, "words": "candussido judifgz"},
            {"aliases": ("refresh", "moves"), "spell": "refresh", "cost": 500, "words": "candusima"},
            {"aliases": ("mana", "energize"), "kind": "mana", "cost": 1000, "words": "energizer"},
        ]
        for service in services:
            for alias in service["aliases"]:
                if alias.startswith(query) or query.startswith(alias):
                    return service
        return None

    @staticmethod
    def _healer_service_list(healer) -> str:
        name = getattr(healer, "short_description", "") or getattr(healer, "name", "The healer")
        return (
            f"{name} says 'I offer the following spells:'\r\n"
            "  light: cure light wounds      10 gold\r\n"
            "  serious: cure serious wounds  15 gold\r\n"
            "  critic: cure critical wounds  25 gold\r\n"
            "  heal: healing spell           50 gold\r\n"
            "  blind: cure blindness         20 gold\r\n"
            "  disease: cure disease         15 gold\r\n"
            "  poison: cure poison           25 gold\r\n"
            "  uncurse: remove curse         50 gold\r\n"
            "  refresh: restore movement      5 gold\r\n"
            "  mana: restore mana            10 gold\r\n"
            " Type heal <type> to be healed.\r\n"
        )

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
        return not str(wanted or "").strip() or LookupUtil.matches(wanted, getattr(entity, "name", ""))

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
