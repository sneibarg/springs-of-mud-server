import importlib.util
import json
import os
import re
import sys
import types
import unittest
from copy import deepcopy
from types import SimpleNamespace
from unittest.mock import patch


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
COMMANDS_PATH = os.path.join(ROOT, "resources", "collections", "SOMDB.Commands.json")

if SRC not in sys.path:
    sys.path.insert(0, SRC)


def _stub_package(name: str):
    if name in sys.modules:
        return sys.modules[name]
    module = types.ModuleType(name)
    module.__path__ = [os.path.join(SRC, *name.split("."))]
    sys.modules[name] = module
    return module


def _stub_module(name: str, **attrs):
    module = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    sys.modules[name] = module
    return module


def _load_module(name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(name, os.path.join(SRC, relative_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class _Logger:
    def info(self, *_args, **_kwargs):
        return None

    def debug(self, *_args, **_kwargs):
        return None

    def warning(self, *_args, **_kwargs):
        return None

    def warn(self, *_args, **_kwargs):
        return None

    def error(self, *_args, **_kwargs):
        return None


class _LoggerFactory:
    @staticmethod
    def get_logger(_name):
        return _Logger()


class _CharacterApi:
    @staticmethod
    def get_enum(name: str):
        if name == "wellKnownObjectVnums":
            return SimpleNamespace(OBJ_VNUM_PIT=SimpleNamespace(value="999"))
        if name == "wearFlags":
            return SimpleNamespace(ITEM_TAKE=SimpleNamespace(value=1))
        if name == "itemFlags":
            return SimpleNamespace(
                ITEM_INVENTORY=SimpleNamespace(value=1),
                ITEM_HAD_TIMER=SimpleNamespace(value=2),
                ITEM_SELL_EXTRACT=SimpleNamespace(value=4),
            )
        if name == "actBits":
            return SimpleNamespace(ACT_IS_CHANGER=SimpleNamespace(value=1))
        return SimpleNamespace()

    @staticmethod
    def is_immortal(character) -> bool:
        return bool(getattr(character, "is_immortal", False))

    @staticmethod
    def is_npc(character) -> bool:
        return bool(getattr(character, "is_npc", False))

    @staticmethod
    def owned_items(character):
        return list(getattr(character, "loot", []) or [])

    @staticmethod
    def find_owned_item(character, wanted):
        return character.find_inventory_item(wanted)

    @staticmethod
    def can_see(_actor, _target, _room) -> bool:
        return True

    @staticmethod
    def is_set(value: int, bit: int) -> bool:
        return (int(value or 0) & int(bit or 0)) != 0

    @staticmethod
    def enum_bit(enum_obj, name: str) -> int:
        member = getattr(enum_obj, name, None)
        return int(getattr(member, "value", 0) or 0) if member is not None else 0

    @staticmethod
    def unset_bit(value: int, bit: int) -> int:
        return int(value or 0) & ~int(bit or 0)

    @staticmethod
    def set_bit(value: int, bit: int) -> int:
        return int(value or 0) | int(bit or 0)

    @staticmethod
    def _enums_map():
        return {}

    @staticmethod
    def wait_state(character, pulses: int):
        character.wait = int(pulses)
        return character.wait


class _ItemApi:
    @staticmethod
    def flags_to_int(raw) -> int:
        return int(raw or 0)

    @staticmethod
    def is_container_closed(item) -> bool:
        return bool(getattr(item, "closed", False))


class _CommunicationsUtil:
    @staticmethod
    def ensure_message_break(text: str) -> str:
        rendered = str(text or "")
        if rendered and not rendered.endswith("\r\n"):
            rendered += "\r\n"
        return rendered

    @staticmethod
    def split_first(text: str):
        raw = str(text or "").strip()
        if not raw:
            return "", ""
        parts = raw.split(maxsplit=1)
        if len(parts) == 1:
            return parts[0], ""
        return parts[0], parts[1]


class _ItemUtil:
    @staticmethod
    def parse_raw_arguments(result, parameters):
        text = (result if isinstance(result, str) else "").strip()
        if not text:
            text = " ".join(parameters or []).strip()
        words = text.split()
        if not words:
            return "", ""
        arg1 = words[0]
        remaining = words[1:]
        if remaining and remaining[0].lower() in {"from", "in", "on"}:
            remaining = remaining[1:]
        return arg1, " ".join(remaining)

    @staticmethod
    def find_room_item(room, wanted):
        if room is None:
            return None
        query = str(wanted or "").strip().lower()
        if not query:
            return None
        for item in room.contents.values():
            name = str(getattr(item, "name", "") or "").lower()
            if name == query or name.startswith(query):
                return item
        return None

    @staticmethod
    def find_container(character, room, wanted):
        query = str(wanted or "").strip().lower()
        found = character.find_inventory_item(query) if hasattr(character, "find_inventory_item") else None
        if found is not None:
            return found
        return _ItemUtil.find_room_item(room, query)

    @staticmethod
    def find_item(character, room, wanted):
        return character.find_inventory_item(wanted) if hasattr(character, "find_inventory_item") and character.find_inventory_item(wanted) is not None else _ItemUtil.find_room_item(room, wanted)

    @staticmethod
    def find_in_contains(container, wanted):
        query = str(wanted or "").strip().lower()
        for item in list(getattr(container, "contains", []) or []):
            name = str(getattr(item, "name", "") or "").lower()
            if name == query or name.startswith(query):
                return item
        return None

    @staticmethod
    def add_to_inventory(character, item):
        character.add_item(item)

    @staticmethod
    def remove_from_contains(container, item):
        container.remove_contained_item(item)

    @staticmethod
    def equipped_slot_of(character, item):
        return character.equipped_slot_of(item)

    @staticmethod
    def unequip_item(character, slot_name: str):
        return character.unequip_item(slot_name)

    @staticmethod
    def item_takeable(item) -> bool:
        return bool(getattr(item, "takeable", True))

    @staticmethod
    def is_nodrop(item, _item_flags=None) -> bool:
        return bool(getattr(item, "nodrop", False))

    @staticmethod
    def can_see_object(_room, _character, _item) -> bool:
        return True

    @staticmethod
    def is_newbie_pit(item) -> bool:
        return item is not None and str(getattr(item, "vnum", "") or "") == "999"

    @staticmethod
    def is_container_like(item) -> bool:
        item_type = str(getattr(item, "item_type", "") or "").lower()
        return "container" in item_type or "corpse" in item_type

    @staticmethod
    def is_container(item) -> bool:
        item_type = str(getattr(item, "item_type", "") or "").lower()
        return "container" in item_type

    @staticmethod
    def is_closed_container(item) -> bool:
        return _ItemApi.is_container_closed(item)

    @staticmethod
    def has_flag(raw_flags, bit_value: int) -> bool:
        return (int(raw_flags or 0) & int(bit_value or 0)) != 0

    @staticmethod
    def create_object(item):
        clone = SimpleNamespace(**getattr(item, "__dict__", {}).copy())
        clone.id = f"clone-{getattr(item, 'id', 'item')}"
        return clone

    @staticmethod
    def short(item) -> str:
        return str(getattr(item, "short_description", getattr(item, "name", "it")) or "it")


class _Context(SimpleNamespace):
    @staticmethod
    def look_keyword_matches(token: str, keyword: str) -> bool:
        q = str(token or "").strip().lower()
        words = [word for word in str(keyword or "").strip().lower().split() if word]
        return any(word == q or word.startswith(q) for word in words)

    def finish(self):
        self.done = True


for package_name in ("api", "area", "fight", "game", "interp", "item", "player", "server", "skill", "util"):
    _stub_package(package_name)
_stub_package("interp.commands")

_stub_module("injector", inject=lambda target: target)
_stub_module("server.LoggerFactory", LoggerFactory=_LoggerFactory)
_stub_module("api.CharacterApi", CharacterApi=_CharacterApi)
_stub_module("api.ItemApi", ItemApi=_ItemApi)
_stub_module("api.MovementApi", MovementApi=SimpleNamespace())
_stub_module("util.CommunicationsUtil", CommunicationsUtil=_CommunicationsUtil)
_stub_module("util.AreaUtil", AreaUtil=SimpleNamespace())
_stub_module("util.FightUtil", FightUtil=SimpleNamespace())
_stub_module("util.MovementUtil", MovementUtil=SimpleNamespace())
_stub_module("util.MobileUtil", MobileUtil=SimpleNamespace())
_stub_module("util.EffectUtil", EffectUtil=SimpleNamespace(apply_item_effects=lambda *_args, **_kwargs: None, remove_item_effects=lambda *_args, **_kwargs: None))
_stub_module("util.ItemUtil", ItemUtil=_ItemUtil)
_stub_module(
    "util.PlayerUtil",
    PlayerUtil=SimpleNamespace(
        get_target=lambda _character, wanted, room: next(
            (
                entity
                for entity in list(getattr(room, "characters", {}).values()) + list(getattr(room, "mobiles", {}).values())
                if str(getattr(entity, "name", "") or "").lower().startswith(str(wanted or "").strip().lower())
            ),
            None,
        )
        if room is not None and str(wanted or "").strip()
        else None
    ),
)
_stub_module("util.SkillUtil", SkillUtil=SimpleNamespace(check_improve=lambda *_args, **_kwargs: None))
_stub_module("game.RegistryService", RegistryService=object)
_stub_module("interp.Context", Context=_Context)
_stub_module("item.Item", Item=object)
_stub_module("player.Character", Character=object)
_stub_module("fight.FightHandler", FightHandler=object)
_stub_module("skill.SpellContext", SpellContext=object)
_stub_module("api.SpellApi", SpellApi=object)

_load_module("util.GenericUtil", "util/GenericUtil.py")
GamePayload = _load_module("game.GamePayload", "game/GamePayload.py").GamePayload
_load_module("interp.HelpEntry", "interp/HelpEntry.py")
_load_module("interp.InterpView", "interp/InterpView.py")
_load_module("game.action", "game/action/__init__.py")
Item = _load_module("item.Item", "item/Item.py").Item
Equipped = _load_module("game.Equipped", "game/Equipped.py").Equipped
_load_module("skill.SpellContext", "skill/SpellContext.py")
_load_module("util.InterpUtil", "util/InterpUtil.py")
Shop = _load_module("area.Shop", "area/Shop.py").Shop
InterpApi = _load_module("api.InterpApi", "api/InterpApi.py").InterpApi
Object = _load_module("interp.commands.Object", "interp/commands/Object.py").Object


def _snake(text: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", str(text or "")).lower()


class _Command:
    def __init__(self, payload: dict):
        self.name = payload["name"]
        self.payload = GamePayload(
            to_char={_snake(key): value for key, value in (payload.get("payload", {}).get("toChar", {}) or {}).items()},
            to_room={_snake(key): value for key, value in (payload.get("payload", {}).get("toRoom", {}) or {}).items()},
            to_victim={_snake(key): value for key, value in (payload.get("payload", {}).get("toVictim", {}) or {}).items()},
        )
        self.guards = []
        for entry in list(payload.get("guards", []) or []):
            self.guards.append(
                {
                    "predicate": entry["predicate"],
                    "channel": str(entry.get("channel", "") or "").strip(),
                    "message_key": _snake(entry.get("messageKey", "")),
                    "fallback": str(entry.get("fallback", "") or ""),
                    "token_factory": str(entry.get("tokenFactory", "") or "").strip(),
                }
            )

    def render_message(self, channel: str, key: str, fallback: str = "", **values) -> str:
        return self.payload.render(channel, key, fallback=fallback, **values)


def _load_command(name: str):
    with open(COMMANDS_PATH, "r", encoding="utf-8") as handle:
        commands = json.load(handle)
    for entry in commands:
        if entry.get("name") == name:
            payload = deepcopy(entry)
            return _Command(payload)
    raise KeyError(name)


class _Room(SimpleNamespace):
    def add_item_to_room(self, item):
        self.contents[item.id] = item

    def remove_item_from_room(self, item):
        self.contents.pop(item.id, None)

    def player_targets(self, character):
        return [ch for ch in list(getattr(self, "characters", {}).values()) if getattr(ch, "id", None) != getattr(character, "id", None)]


class _Container(SimpleNamespace):
    def remove_contained_item(self, item):
        self.contains.remove(item)


class TestObjectGetDynamicCommands(unittest.TestCase):
    def _commands(self, room, *, shop_registry=None, weather_handler=None, skill_registry=None, spell_registry=None, spell_api=None, fight_handler=None):
        room_registry = SimpleNamespace(
            get_or_none=lambda **kwargs: room if kwargs.get("id") == room.id else None,
            get=lambda **kwargs: room if kwargs.get("id") == room.id else None,
        )
        registry_service = SimpleNamespace(
            room_registry=room_registry,
            mobile_registry=None,
            shop_registry=shop_registry,
            skill_registry=skill_registry,
            spell_registry=spell_registry,
        )
        commands = Object(
            registry_service=registry_service,
            interp_api=InterpApi(),
            weather_handler=weather_handler,
            spell_api=spell_api,
            fight_handler=fight_handler,
        )
        commands.item_types = SimpleNamespace(ITEM_WEAPON=SimpleNamespace(value=5))
        commands.item_flags = SimpleNamespace(
            ITEM_INVENTORY=SimpleNamespace(value=1),
            ITEM_HAD_TIMER=SimpleNamespace(value=2),
            ITEM_SELL_EXTRACT=SimpleNamespace(value=4),
            ITEM_NOREMOVE=SimpleNamespace(value=8),
        )
        commands.act_bits = SimpleNamespace(ACT_IS_CHANGER=SimpleNamespace(value=1))
        commands.wear_flags = SimpleNamespace(
            ITEM_WEAR_BODY=SimpleNamespace(value=1 << 0),
            ITEM_WIELD=SimpleNamespace(value=1 << 1),
            ITEM_HOLD=SimpleNamespace(value=1 << 2),
            ITEM_WEAR_SHIELD=SimpleNamespace(value=1 << 3),
        )
        return commands

    @staticmethod
    def _build_shop(*, keeper="100", profit_buy=120, profit_sell=50):
        return Shop(
            id=f"shop-{keeper}",
            area_id="area-1",
            comment="",
            keeper=int(keeper),
            buy_type0=5,
            buy_type1=0,
            buy_type2=0,
            buy_type3=0,
            buy_type4=0,
            profit_buy=profit_buy,
            profit_sell=profit_sell,
            open_hour=0,
            close_hour=23,
        )

    @staticmethod
    def _build_character(*items, is_immortal=False, is_npc=False, name="Tester", level=10, max_items=10, max_weight=100, sex="male", act=0, skills=None, fighting=None):
        inventory = list(items)
        character = SimpleNamespace(
            id=f"{name.lower()}-id",
            name=name,
            room_id="room-1",
            loot=inventory,
            gold=0,
            silver=0,
            level=level,
            is_immortal=is_immortal,
            is_npc=is_npc,
            sex=sex,
            status_flags=SimpleNamespace(act=act),
            character_attributes=SimpleNamespace(max_items=max_items, max_weight=max_weight),
            equipped=Equipped(),
            skills=list(skills or []),
            fighting=fighting,
        )

        def _find_inventory_item(wanted):
            query = str(wanted or "").strip().lower()
            for item in inventory:
                name = str(getattr(item, "name", "") or "").lower()
                if name == query or name.startswith(query):
                    return item
            return None

        def _add_item(item):
            inventory.append(item)

        def _remove_item(item):
            inventory.remove(item)

        def _carry_count():
            return len(inventory)

        def _carry_weight():
            item_weight = sum(int(getattr(item, "weight", 0) or 0) for item in inventory)
            coin_weight = int((int(getattr(character, "silver", 0) or 0) / 10) + (int(getattr(character, "gold", 0) or 0) * 2 / 5))
            return item_weight + coin_weight

        def _max_items():
            return int(getattr(character.character_attributes, "max_items", 0) or 0)

        def _max_weight():
            return int(getattr(character.character_attributes, "max_weight", 0) or 0)

        character.find_inventory_item = _find_inventory_item
        character.add_item = _add_item
        character.remove_item = _remove_item
        character.carry_count = _carry_count
        character.carry_weight = _carry_weight
        character.max_items = _max_items
        character.max_weight = _max_weight
        character.skill_level = lambda wanted: next((entry.get("level", 1) for entry in character.skills if entry.get("name") == wanted), 1)
        character.size_value = lambda: 2
        character.large_size_value = lambda: 3
        character.ensure_equipped = lambda: character.equipped
        character.equip_item = lambda item, slot: Equipped.equip_item(character, item, slot)
        character.equipped_slot_of = lambda item: character.equipped.slot_of(item)
        character.unequip_item = lambda slot: Equipped.unequip_item(character, slot)
        return character

    @staticmethod
    def _build_context(raw, room, character, command_name="get"):
        return _Context(
            character=character,
            result=raw,
            parameters=raw.split(),
            room=room,
            command=_load_command(command_name),
            done=False,
        )

    def test_get_single_room_item_returns_pickup_payload(self):
        apple = SimpleNamespace(id="obj-1", name="apple red", short_description="a red apple", takeable=True, weight=1)
        room = _Room(id="room-1", contents={apple.id: apple})
        character = self._build_character()

        payload = self._commands(room).do_get(character, self._build_context("apple", room, character))

        self.assertEqual("You get a red apple.\r\n", payload["to_char"])
        self.assertEqual("Tester gets a red apple.\r\n", payload["to_room"])
        self.assertIn(apple, character.loot)
        self.assertNotIn(apple.id, room.contents)

    def test_get_from_container_uses_container_payload(self):
        gem = SimpleNamespace(id="obj-2", name="gem ruby", short_description="a ruby", takeable=True, weight=1)
        bag = _Container(
            id="obj-3",
            name="bag sack",
            short_description="a leather bag",
            item_type="container",
            contains=[gem],
            closed=False,
        )
        room = _Room(id="room-1", contents={bag.id: bag})
        character = self._build_character()

        payload = self._commands(room).do_get(character, self._build_context("gem from bag", room, character))

        self.assertEqual("You get a ruby from a leather bag.\r\n", payload["to_char"])
        self.assertEqual("Tester gets a ruby from a leather bag.\r\n", payload["to_room"])
        self.assertIn(gem, character.loot)
        self.assertNotIn(gem, bag.contains)

    def test_get_missing_container_uses_guard_payload_token(self):
        room = _Room(id="room-1", contents={})
        character = self._build_character()

        payload = self._commands(room).do_get(character, self._build_context("gem from chest", room, character))

        self.assertEqual("I see no chest here.\r\n", payload["to_char"])
        self.assertEqual("target_not_visible", payload["blocked_key"])

    def test_get_all_from_newbie_pit_uses_guard_payload(self):
        coin = SimpleNamespace(id="obj-4", name="coin gold", short_description="a gold coin", takeable=True, weight=1)
        pit = _Container(
            id="obj-5",
            vnum="999",
            name="pit donation",
            short_description="a donation pit",
            item_type="container",
            contains=[coin],
            closed=False,
        )
        room = _Room(id="room-1", contents={pit.id: pit})
        character = self._build_character()

        payload = self._commands(room).do_get(character, self._build_context("all from pit", room, character))

        self.assertEqual("Don't be so greedy!\r\n", payload["to_char"])
        self.assertEqual("is_newbie_pit", payload["blocked_key"])
        self.assertNotIn(coin, character.loot)
        self.assertIn(coin, pit.contains)

    def test_put_into_container_uses_payload_templates(self):
        gem = SimpleNamespace(id="obj-6", name="gem ruby", short_description="a ruby", takeable=True, weight=1)
        bag = _Container(
            id="obj-7",
            name="bag sack",
            short_description="a leather bag",
            item_type="container",
            contains=[],
            closed=False,
            add_contained_item=lambda item: bag.contains.append(item),
        )
        room = _Room(id="room-1", contents={bag.id: bag})
        character = self._build_character(gem)

        payload = self._commands(room).do_put(character, self._build_context("gem in bag", room, character, "put"))

        self.assertEqual("You put a ruby in a leather bag.\r\n", payload["to_char"])
        self.assertEqual("Tester puts a ruby in a leather bag.\r\n", payload["to_room"])
        self.assertNotIn(gem, character.loot)
        self.assertIn(gem, bag.contains)

    def test_put_missing_container_uses_guard_payload_token(self):
        gem = SimpleNamespace(id="obj-8", name="gem ruby", short_description="a ruby", takeable=True, weight=1)
        room = _Room(id="room-1", contents={})
        character = self._build_character(gem)

        payload = self._commands(room).do_put(character, self._build_context("gem in chest", room, character, "put"))

        self.assertEqual("I see no chest here.\r\n", payload["to_char"])
        self.assertEqual("null_container", payload["blocked_key"])

    def test_drop_single_item_uses_payload_templates(self):
        gem = SimpleNamespace(id="obj-9", name="gem ruby", short_description="a ruby", takeable=True, weight=1)
        room = _Room(id="room-1", contents={})
        character = self._build_character(gem)

        payload = self._commands(room).do_drop(character, self._build_context("gem", room, character, "drop"))

        self.assertEqual("You drop a ruby.\r\n", payload["to_char"])
        self.assertEqual("Tester drops a ruby.\r\n", payload["to_room"])
        self.assertNotIn(gem, character.loot)
        self.assertIn(gem.id, room.contents)

    def test_drop_all_with_no_matching_items_uses_payload_token(self):
        sword = SimpleNamespace(id="obj-10", name="sword steel", short_description="a steel sword", takeable=True, weight=1, nodrop=True)
        room = _Room(id="room-1", contents={})
        character = self._build_character(sword)

        payload = self._commands(room).do_drop(character, self._build_context("all.gem", room, character, "drop"))

        self.assertEqual("You are not carrying any gem.\r\n", payload["to_char"])

    def test_buy_single_item_uses_payload_templates(self):
        sword = SimpleNamespace(id="obj-11", vnum="201", name="sword steel", short_description="a steel sword", level=5, cost=80, weight=1, extra_flags=0, timer=0)
        keeper = SimpleNamespace(id="mob-1", vnum="100", inventory=[sword], short_description="the shopkeeper", gold=0, silver=0)
        room = _Room(id="room-1", contents={}, mobiles={"keeper": keeper})
        shop = self._build_shop()
        shop_registry = SimpleNamespace(find_by_keeper_vnum=lambda keeper_vnum: shop if str(keeper_vnum) == "100" else None)
        character = self._build_character()
        character.gold = 1
        character.level = 10

        payload = self._commands(room, shop_registry=shop_registry, weather_handler=SimpleNamespace(time_info=SimpleNamespace(hour=12))).do_buy(
            character,
            self._build_context("sword", room, character, "buy"),
        )

        self.assertEqual("You buy a steel sword for 96 silver.\r\n", payload["to_char"])
        self.assertEqual("Tester buys a steel sword.\r\n", payload["to_room"])
        self.assertEqual([], keeper.inventory)
        self.assertEqual(0, character.gold)
        self.assertEqual(4, character.silver)

    def test_buy_missing_item_uses_guard_payload(self):
        keeper = SimpleNamespace(id="mob-2", vnum="100", inventory=[], short_description="the shopkeeper", gold=0, silver=0)
        room = _Room(id="room-1", contents={}, mobiles={"keeper": keeper})
        shop = self._build_shop()
        shop_registry = SimpleNamespace(find_by_keeper_vnum=lambda keeper_vnum: shop if str(keeper_vnum) == "100" else None)
        character = self._build_character()

        payload = self._commands(room, shop_registry=shop_registry, weather_handler=SimpleNamespace(time_info=SimpleNamespace(hour=12))).do_buy(
            character,
            self._build_context("shield", room, character, "buy"),
        )

        self.assertEqual("I don't sell that -- try 'list'.\r\n", payload["to_char"])
        self.assertEqual("no_such_item", payload["blocked_key"])

    def test_sell_item_uses_payload_templates(self):
        blade = SimpleNamespace(id="obj-12", vnum="202", name="blade iron", short_description="an iron blade", item_type="ITEM_WEAPON", level=5, cost=100, weight=1, extra_flags=0, timer=0)
        keeper = SimpleNamespace(id="mob-3", vnum="100", inventory=[], short_description="the shopkeeper", gold=1, silver=0)
        room = _Room(id="room-1", contents={}, mobiles={"keeper": keeper})
        shop = self._build_shop()
        shop_registry = SimpleNamespace(find_by_keeper_vnum=lambda keeper_vnum: shop if str(keeper_vnum) == "100" else None)
        character = self._build_character(blade)

        payload = self._commands(room, shop_registry=shop_registry, weather_handler=SimpleNamespace(time_info=SimpleNamespace(hour=12))).do_sell(
            character,
            self._build_context("blade", room, character, "sell"),
        )

        self.assertEqual("You sell an iron blade for 50 silver and 0 gold pieces.\r\n", payload["to_char"])
        self.assertEqual("Tester sells an iron blade.\r\n", payload["to_room"])
        self.assertEqual([], character.loot)
        self.assertEqual([blade], keeper.inventory)

    def test_sell_uninterested_uses_guard_payload(self):
        junk = SimpleNamespace(id="obj-13", vnum="203", name="junk brass", short_description="a brass trinket", level=1, cost=10, weight=1, extra_flags=0, timer=0)
        keeper = SimpleNamespace(id="mob-4", vnum="100", inventory=[], short_description="the shopkeeper", gold=1, silver=0)
        room = _Room(id="room-1", contents={}, mobiles={"keeper": keeper})
        shop = self._build_shop()
        shop_registry = SimpleNamespace(find_by_keeper_vnum=lambda keeper_vnum: shop if str(keeper_vnum) == "100" else None)
        character = self._build_character(junk)

        payload = self._commands(room, shop_registry=shop_registry, weather_handler=SimpleNamespace(time_info=SimpleNamespace(hour=12))).do_sell(
            character,
            self._build_context("junk", room, character, "sell"),
        )

        self.assertEqual("the shopkeeper looks uninterested in a brass trinket.\r\n", payload["to_char"])
        self.assertEqual("looks_uninterested", payload["blocked_key"])

    def test_wear_item_uses_payload_templates(self):
        vest = SimpleNamespace(
            id="obj-wear-1",
            name="vest leather",
            short_description="a leather vest",
            item_type="armor",
            wear_flags=1 << 0,
            level=5,
            weight=2,
            extra_flags=0,
            weapon_too_heavy=lambda _character: False,
            is_two_handed_weapon=lambda: False,
            weapon_skill_feedback_key=lambda _character: "",
            can_remove=lambda _item_flags: True,
        )
        room = _Room(id="room-1", contents={}, mobiles={})
        character = self._build_character(vest)
        character.level = 10

        payload = self._commands(room).do_wear(character, self._build_context("vest", room, character, "wear"))

        self.assertEqual("You wear a leather vest on your torso.\r\n", payload["to_char"])
        self.assertEqual("Tester wears a leather vest on their torso.\r\n", payload["to_room"])
        self.assertIs(character.equipped.torso, vest)
        self.assertNotIn(vest, character.loot)

    def test_wear_invalid_forced_slot_uses_guard_payload(self):
        vest = SimpleNamespace(
            id="obj-wear-2",
            name="vest leather",
            short_description="a leather vest",
            item_type="armor",
            wear_flags=1 << 0,
            level=5,
            weight=2,
            extra_flags=0,
            weapon_too_heavy=lambda _character: False,
            is_two_handed_weapon=lambda: False,
            weapon_skill_feedback_key=lambda _character: "",
            can_remove=lambda _item_flags: True,
        )
        room = _Room(id="room-1", contents={}, mobiles={})
        character = self._build_character(vest)
        character.level = 10

        payload = self._commands(room).do_wear(character, self._build_context("vest head", room, character, "wear"))

        self.assertEqual("You can't wear that there.\r\n", payload["to_char"])
        self.assertEqual("invalid_target_there", payload["blocked_key"])
        self.assertIsNone(character.equipped.torso)
        self.assertIn(vest, character.loot)

    def test_wear_item_with_insufficient_level_uses_guard_payload(self):
        vest = SimpleNamespace(
            id="obj-wear-3",
            name="vest leather",
            short_description="a leather vest",
            item_type="armor",
            wear_flags=1 << 0,
            level=15,
            weight=2,
            extra_flags=0,
            weapon_too_heavy=lambda _character: False,
            is_two_handed_weapon=lambda: False,
            weapon_skill_feedback_key=lambda _character: "",
            can_remove=lambda _item_flags: True,
        )
        room = _Room(id="room-1", contents={}, mobiles={})
        character = self._build_character(vest)
        character.level = 10

        payload = self._commands(room).do_wear(character, self._build_context("vest", room, character, "wear"))

        self.assertEqual("You must be level 15 to use this object.\r\n", payload["to_char"])
        self.assertEqual("Tester tries to use a leather vest, but is too inexperienced.\r\n", payload["to_room"])
        self.assertEqual("insufficient_level", payload["blocked_key"])
        self.assertIsNone(character.equipped.torso)

    def test_value_item_uses_payload_templates(self):
        blade = SimpleNamespace(id="obj-value-1", vnum="301", name="blade iron", short_description="an iron blade", item_type="ITEM_WEAPON", level=5, cost=100, weight=1, extra_flags=0, timer=0)
        keeper = SimpleNamespace(id="mob-value-1", vnum="100", inventory=[], short_description="the shopkeeper", gold=1, silver=0)
        room = _Room(id="room-1", contents={}, mobiles={"keeper": keeper})
        shop = self._build_shop()
        shop_registry = SimpleNamespace(find_by_keeper_vnum=lambda keeper_vnum: shop if str(keeper_vnum) == "100" else None)
        character = self._build_character(blade)

        payload = self._commands(room, shop_registry=shop_registry, weather_handler=SimpleNamespace(time_info=SimpleNamespace(hour=12))).do_value(
            character,
            self._build_context("blade", room, character, "value"),
        )

        self.assertEqual("I'll give you 50 silver and 0 gold coins for an iron blade.\r\n", payload["to_char"])

    def test_value_uninterested_uses_guard_payload(self):
        junk = SimpleNamespace(id="obj-value-2", vnum="302", name="junk brass", short_description="a brass trinket", item_type="ITEM_TRASH", level=1, cost=10, weight=1, extra_flags=0, timer=0)
        keeper = SimpleNamespace(id="mob-value-2", vnum="100", inventory=[], short_description="the shopkeeper", gold=1, silver=0)
        room = _Room(id="room-1", contents={}, mobiles={"keeper": keeper})
        shop = self._build_shop()
        shop_registry = SimpleNamespace(find_by_keeper_vnum=lambda keeper_vnum: shop if str(keeper_vnum) == "100" else None)
        character = self._build_character(junk)

        payload = self._commands(room, shop_registry=shop_registry, weather_handler=SimpleNamespace(time_info=SimpleNamespace(hour=12))).do_value(
            character,
            self._build_context("junk", room, character, "value"),
        )

        self.assertEqual("the shopkeeper looks uninterested in a brass trinket.\r\n", payload["to_char"])
        self.assertEqual("looks_uninterested", payload["blocked_key"])

    def test_list_shop_inventory_uses_existing_stock_format(self):
        sword = SimpleNamespace(id="obj-list-1", vnum="301", name="sword iron", short_description="an iron sword", item_type="ITEM_WEAPON", level=5, cost=100, weight=1, extra_flags=1)
        shield = SimpleNamespace(id="obj-list-2", vnum="302", name="shield oak", short_description="an oak shield", item_type="ITEM_ARMOR", level=3, cost=80, weight=1, extra_flags=0)
        shield2 = SimpleNamespace(id="obj-list-3", vnum="302", name="shield oak", short_description="an oak shield", item_type="ITEM_ARMOR", level=3, cost=80, weight=1, extra_flags=0)
        keeper = SimpleNamespace(id="mob-list-1", vnum="100", inventory=[sword, shield, shield2], short_description="the shopkeeper", gold=0, silver=0)
        room = _Room(id="room-1", contents={}, mobiles={"keeper": keeper})
        shop = self._build_shop()
        shop_registry = SimpleNamespace(find_by_keeper_vnum=lambda keeper_vnum: shop if str(keeper_vnum) == "100" else None)
        character = self._build_character()

        payload = self._commands(room, shop_registry=shop_registry, weather_handler=SimpleNamespace(time_info=SimpleNamespace(hour=12))).do_list(
            character,
            self._build_context("shield", room, character, "list"),
        )

        self.assertEqual("[Lv Price Qty] Item\r\n[ 3    96  2 ] an oak shield\r\n", payload["to_char"])

    def test_list_without_keeper_uses_guard_payload(self):
        room = _Room(id="room-1", contents={}, mobiles={})
        character = self._build_character()

        payload = self._commands(room).do_list(character, self._build_context("", room, character, "list"))

        self.assertEqual("You can't do that here.\r\n", payload["to_char"])
        self.assertEqual("shop_unavailable", payload["blocked_key"])

    def test_remove_item_uses_payload_templates(self):
        vest = SimpleNamespace(
            id="obj-remove-1",
            name="vest leather",
            short_description="a leather vest",
            can_remove=lambda _item_flags: True,
        )
        room = _Room(id="room-1", contents={}, mobiles={})
        character = self._build_character()
        character.add_item(vest)
        Equipped.equip_item(character, vest, "torso")

        payload = self._commands(room).do_remove(character, self._build_context("vest", room, character, "remove"))

        self.assertEqual("You stop using a leather vest.\r\n", payload["to_char"])
        self.assertEqual("Tester stops using a leather vest.\r\n", payload["to_room"])
        self.assertIsNone(character.equipped.torso)
        self.assertIn(vest, character.loot)

    def test_remove_no_remove_uses_guard_payload(self):
        ring = SimpleNamespace(
            id="obj-remove-2",
            name="ring cursed",
            short_description="a cursed ring",
            can_remove=lambda _item_flags: False,
        )
        room = _Room(id="room-1", contents={}, mobiles={})
        character = self._build_character()
        character.add_item(ring)
        Equipped.equip_item(character, ring, "finger1")

        payload = self._commands(room).do_remove(character, self._build_context("ring", room, character, "remove"))

        self.assertEqual("You can't remove a cursed ring.\r\n", payload["to_char"])
        self.assertEqual("no_remove", payload["blocked_key"])
        self.assertIs(character.equipped.finger1, ring)
        self.assertNotIn(ring, character.loot)

    def test_fill_uses_payload_templates(self):
        bottle = SimpleNamespace(id="obj-fill-1", name="bottle glass", short_description="a glass bottle", item_type="drink container", value0="10", value1="0", value2="")
        fountain = SimpleNamespace(id="obj-fill-2", name="fountain stone", short_description="a stone fountain", item_type="fountain", value0="100", value1="100", value2="water")
        room = _Room(id="room-1", contents={fountain.id: fountain}, mobiles={})
        character = self._build_character(bottle)

        payload = self._commands(room).do_fill(character, self._build_context("bottle fountain", room, character, "fill"))

        self.assertEqual("You fill a glass bottle with water from a stone fountain.\r\n", payload["to_char"])
        self.assertEqual("Tester fills a glass bottle with water from a stone fountain.\r\n", payload["to_room"])
        self.assertEqual("10", bottle.value1)
        self.assertEqual("water", bottle.value2)

    def test_fill_empty_source_uses_guard_payload(self):
        bottle = SimpleNamespace(id="obj-fill-3", name="bottle glass", short_description="a glass bottle", item_type="drink container", value0="10", value1="0", value2="")
        skin = SimpleNamespace(id="obj-fill-4", name="skin leather", short_description="a leather skin", item_type="drink container", value0="10", value1="0", value2="water")
        room = _Room(id="room-1", contents={}, mobiles={})
        character = self._build_character(bottle, skin)

        payload = self._commands(room).do_fill(character, self._build_context("bottle skin", room, character, "fill"))

        self.assertEqual("It is empty.\r\n", payload["to_char"])
        self.assertEqual("source_empty", payload["blocked_key"])
        self.assertEqual("0", bottle.value1)

    def test_pour_out_uses_payload_templates_and_clears_container(self):
        waterskin = SimpleNamespace(
            id="obj-pour-1",
            name="waterskin leather",
            short_description="a leather waterskin",
            item_type="drink container",
            value0="10",
            value1="7",
            value2="water",
            value3="1",
        )
        room = _Room(id="room-1", contents={}, mobiles={})
        character = self._build_character(waterskin)

        payload = self._commands(room).do_pour(character, self._build_context("waterskin out", room, character, "pour"))

        self.assertEqual("You invert a leather waterskin, spilling water all over the ground.\r\n", payload["to_char"])
        self.assertEqual("Tester inverts a leather waterskin, spilling water all over the ground.\r\n", payload["to_room"])
        self.assertEqual("0", waterskin.value1)
        self.assertEqual("0", waterskin.value3)

    def test_pour_into_container_transfers_amount(self):
        source = SimpleNamespace(
            id="obj-pour-2",
            name="waterskin leather",
            short_description="a leather waterskin",
            item_type="drink container",
            value0="10",
            value1="8",
            value2="water",
            value3="0",
        )
        target = SimpleNamespace(
            id="obj-pour-3",
            name="bottle glass",
            short_description="a glass bottle",
            item_type="drink container",
            value0="5",
            value1="1",
            value2="water",
            value3="0",
        )
        room = _Room(id="room-1", contents={target.id: target}, mobiles={})
        character = self._build_character(source)

        payload = self._commands(room).do_pour(character, self._build_context("waterskin bottle", room, character, "pour"))

        self.assertEqual("You pour water from a leather waterskin into a glass bottle.\r\n", payload["to_char"])
        self.assertEqual("Tester pours water from a leather waterskin into a glass bottle.\r\n", payload["to_room"])
        self.assertEqual("4", source.value1)
        self.assertEqual("5", target.value1)

    def test_pour_for_victim_uses_held_container_messages(self):
        source = SimpleNamespace(
            id="obj-pour-4",
            name="waterskin leather",
            short_description="a leather waterskin",
            item_type="drink container",
            value0="10",
            value1="8",
            value2="water",
            value3="0",
        )
        cup = SimpleNamespace(
            id="obj-pour-5",
            name="cup tin",
            short_description="a tin cup",
            item_type="drink container",
            value0="4",
            value1="0",
            value2="",
            value3="0",
        )
        victim = self._build_character(name="Receiver")
        victim.add_item(cup)
        Equipped.equip_item(victim, cup, "held")
        room = _Room(id="room-1", contents={}, mobiles={}, characters={victim.id: victim})
        character = self._build_character(source)

        payload = self._commands(room).do_pour(character, self._build_context("waterskin receiver", room, character, "pour"))

        self.assertEqual("You pour some water for Receiver.\r\n", payload["to_char"])
        self.assertEqual("Tester pours you some water.\r\n", payload["to_victim"])
        self.assertEqual("Tester pours some water for Receiver.\r\n", payload["to_room"])
        self.assertIs(payload["victim"], victim)
        self.assertEqual("4", cup.value1)
        self.assertEqual("4", source.value1)

    def test_pour_missing_victim_container_uses_guard_payload(self):
        source = SimpleNamespace(
            id="obj-pour-6",
            name="waterskin leather",
            short_description="a leather waterskin",
            item_type="drink container",
            value0="10",
            value1="8",
            value2="water",
            value3="0",
        )
        victim = self._build_character(name="Receiver")
        room = _Room(id="room-1", contents={}, mobiles={}, characters={victim.id: victim})
        character = self._build_character(source)

        payload = self._commands(room).do_pour(character, self._build_context("waterskin receiver", room, character, "pour"))

        self.assertEqual("They aren't holding anything.\r\n", payload["to_char"])
        self.assertEqual("target_container_missing", payload["blocked_key"])

    def test_give_item_uses_payload_templates(self):
        gem = SimpleNamespace(id="obj-14", name="gem ruby", short_description="a ruby", weight=1)
        victim = self._build_character(name="Receiver")
        room = _Room(id="room-1", contents={}, mobiles={}, characters={victim.id: victim})
        character = self._build_character(gem)

        payload = self._commands(room).do_give(character, self._build_context("gem receiver", room, character, "give"))

        self.assertEqual("You give a ruby to Receiver.\r\n", payload["to_char"])
        self.assertEqual("Tester gives a ruby to Receiver.\r\n", payload["to_room"])
        self.assertEqual("Tester gives you a ruby.\r\n", payload["to_victim"])
        self.assertIn(gem, victim.loot)
        self.assertNotIn(gem, character.loot)

    def test_give_to_keeper_uses_guard_payload(self):
        gem = SimpleNamespace(id="obj-15", name="gem ruby", short_description="a ruby", weight=1)
        keeper = self._build_character(is_npc=True, name="Keeper")
        keeper.vnum = "100"
        room = _Room(id="room-1", contents={}, mobiles={"keeper": keeper}, characters={})
        shop = SimpleNamespace(keeper="100")
        shop_registry = SimpleNamespace(find_by_keeper_vnum=lambda keeper_vnum: shop if str(keeper_vnum) == "100" else None)
        character = self._build_character(gem)

        payload = self._commands(room, shop_registry=shop_registry).do_give(
            character,
            self._build_context("gem keeper", room, character, "give"),
        )

        self.assertEqual("Keeper tells you 'Sorry, you'll have to sell that.'\r\n", payload["to_char"])
        self.assertEqual("target_keeper", payload["blocked_key"])
        self.assertIn(gem, character.loot)

    def test_give_funds_uses_payload_templates(self):
        victim = self._build_character(name="Receiver")
        room = _Room(id="room-1", contents={}, mobiles={}, characters={victim.id: victim})
        character = self._build_character()
        character.silver = 75

        payload = self._commands(room).do_give(character, self._build_context("25 silver receiver", room, character, "give"))

        self.assertEqual("You give 25 silver to Receiver.\r\n", payload["to_char"])
        self.assertEqual("Tester gives Receiver some coins.\r\n", payload["to_room"])
        self.assertEqual("Tester gives you 25 silver.\r\n", payload["to_victim"])
        self.assertEqual(50, character.silver)
        self.assertEqual(25, victim.silver)

    def test_give_funds_insufficient_uses_guard_payload(self):
        victim = self._build_character(name="Receiver")
        room = _Room(id="room-1", contents={}, mobiles={}, characters={victim.id: victim})
        character = self._build_character()
        character.gold = 1

        payload = self._commands(room).do_give(character, self._build_context("2 gold receiver", room, character, "give"))

        self.assertEqual("You haven't got that much.\r\n", payload["to_char"])
        self.assertEqual("insufficient_funds", payload["blocked_key"])

    def test_give_silver_to_money_changer_returns_changed_funds(self):
        changer = self._build_character(is_npc=True, name="Changer", act=1)
        room = _Room(id="room-1", contents={}, mobiles={"changer": changer}, characters={})
        character = self._build_character()
        character.silver = 200

        payload = self._commands(room).do_give(character, self._build_context("200 silver changer", room, character, "give"))

        self.assertEqual(
            "You give 200 silver to Changer.\r\nChanger gives you 1 gold.\r\nChanger gives you 90 silver.\r\nChanger tells you 'Thank you, come again.'\r\n",
            payload["to_char"],
        )
        self.assertEqual(1, character.gold)
        self.assertEqual(90, character.silver)
        self.assertEqual(0, changer.gold)
        self.assertEqual(10, changer.silver)

    def test_give_silver_to_money_changer_with_too_little_returns_original_amount(self):
        changer = self._build_character(is_npc=True, name="Changer", act=1)
        room = _Room(id="room-1", contents={}, mobiles={"changer": changer}, characters={})
        character = self._build_character()
        character.silver = 50

        payload = self._commands(room).do_give(character, self._build_context("1 silver changer", room, character, "give"))

        self.assertEqual(
            "You give 1 silver to Changer.\r\nChanger tells you 'I'm sorry, you did not give me enough to change.'\r\nChanger gives you 1 silver.\r\n",
            payload["to_char"],
        )
        self.assertEqual(0, character.gold)
        self.assertEqual(50, character.silver)
        self.assertEqual(0, changer.gold)
        self.assertEqual(0, changer.silver)

    def test_quaff_uses_guards_and_casts_item_spells(self):
        class _SpellApiDouble:
            def __init__(self):
                self.calls = []

            def execute_lambdas(self, ctx):
                self.calls.append((ctx.spell.name, ctx.level, ctx.target))
                ctx.queue_payload({"to_char": f"{ctx.spell.name} fires.\r\n"})
                ctx.mark_performed()

            def start_offensive_combat(self, _ctx):
                return None

        room = _Room(id="room-1", contents={}, mobiles={}, characters={})
        potion = SimpleNamespace(
            id="obj-potion",
            name="potion bubbling",
            short_description="a bubbling potion",
            item_type="potion",
            value0="17",
            value1=SimpleNamespace(name="heal", handler_id="spell.heal", target="CHAR_DEFENSIVE"),
            value2="",
            value3="",
            level=10,
            weight=1,
        )
        character = self._build_character(potion, level=20)
        spell_api = _SpellApiDouble()

        payload = self._commands(room, spell_api=spell_api).do_quaff(character, self._build_context("potion", room, character, "quaff"))

        self.assertEqual("You quaff a bubbling potion.\r\n", payload["payloads"][0]["to_char"])
        self.assertEqual(("heal", 17, character), spell_api.calls[0])
        self.assertEqual("heal fires.\r\n", payload["payloads"][1]["to_char"])
        self.assertNotIn(potion, character.loot)

    def test_recite_missing_target_uses_command_guard(self):
        room = _Room(id="room-1", contents={}, mobiles={}, characters={})
        scroll = SimpleNamespace(
            id="obj-scroll",
            name="scroll vellum",
            short_description="a vellum scroll",
            item_type="scroll",
            value0="15",
            value1=SimpleNamespace(name="heal", handler_id="spell.heal", target="CHAR_DEFENSIVE"),
            value2="",
            value3="",
            level=5,
            weight=1,
        )
        character = self._build_character(scroll, level=20)

        payload = self._commands(room).do_recite(character, self._build_context("scroll goblin", room, character, "recite"))

        self.assertEqual("You can't find it.\r\n", payload["to_char"])
        self.assertEqual("target_missing", payload["blocked_key"])
        self.assertIn(scroll, character.loot)

    def test_brandish_filters_targets_by_spell_target_and_breaks_staff(self):
        class _SpellApiDouble:
            def __init__(self):
                self.targets = []

            def execute_lambdas(self, ctx):
                self.targets.append(getattr(ctx.target, "name", ""))
                ctx.queue_payload({"to_char": f"spell hits {getattr(ctx.target, 'name', '')}.\r\n"})
                ctx.mark_performed()

            def start_offensive_combat(self, _ctx):
                return None

        actor = self._build_character(
            level=30,
            skills=[{"name": "staves", "level": 100}],
        )
        ally = self._build_character(name="Ally", level=30)
        enemy = self._build_character(name="Goblin", is_npc=True, level=20)
        room = _Room(id="room-1", contents={}, mobiles={enemy.id: enemy}, characters={ally.id: ally})
        staff = SimpleNamespace(
            id="obj-staff",
            name="staff oak",
            short_description="an oak staff",
            item_type="staff",
            value0="20",
            value2="1",
            value3=SimpleNamespace(name="fireball", handler_id="spell.fireball", target="CHAR_OFFENSIVE"),
            level=10,
            weight=1,
        )
        actor.add_item(staff)
        Equipped.equip_item(actor, staff, "held")
        spell_api = _SpellApiDouble()
        skill_registry = SimpleNamespace(get_or_none=lambda **kwargs: SimpleNamespace(id=f"skill-{kwargs.get('name')}", name=kwargs.get("name")))

        with patch.object(sys.modules["interp.commands.Object"].random, "randint", return_value=1):
            payload = self._commands(room, skill_registry=skill_registry, spell_api=spell_api).do_brandish(
                actor,
                self._build_context("", room, actor, "brandish"),
            )

        self.assertEqual(["Goblin"], spell_api.targets)
        self.assertEqual(24, actor.wait)
        self.assertEqual("You brandish an oak staff.\r\n", payload["payloads"][0]["to_char"])
        self.assertEqual("Your an oak staff blazes bright and is gone.\r\n", payload["payloads"][-1]["to_char"])
        self.assertIsNone(actor.equipped.held)
        self.assertNotIn(staff, actor.loot)

    def test_zap_without_target_uses_no_argument_guard_before_item_checks(self):
        actor = self._build_character(level=20)
        wand = SimpleNamespace(
            id="obj-wand",
            name="wand crystal",
            short_description="a crystal wand",
            item_type="wand",
            value0="20",
            value2="1",
            value3=SimpleNamespace(name="magic missile", handler_id="spell.magic_missile", target="CHAR_OFFENSIVE"),
            level=10,
            weight=1,
        )
        actor.add_item(wand)
        Equipped.equip_item(actor, wand, "held")
        room = _Room(id="room-1", contents={}, mobiles={}, characters={})

        payload = self._commands(room).do_zap(actor, self._build_context("", room, actor, "zap"))

        self.assertEqual("Zap whom or what?\r\n", payload["to_char"])
        self.assertEqual("no_argument", payload["blocked_key"])

    def test_zap_casts_on_victim_and_breaks_wand(self):
        class _SpellApiDouble:
            def __init__(self):
                self.targets = []
                self.started = []

            def execute_lambdas(self, ctx):
                self.targets.append(getattr(ctx.target, "name", ""))
                ctx.queue_payload({"to_char": f"spell zaps {getattr(ctx.target, 'name', '')}.\r\n"})
                ctx.mark_performed()

            def start_offensive_combat(self, ctx):
                self.started.append(getattr(ctx.target, "name", ""))

        victim = self._build_character(name="Receiver", level=20)
        room = _Room(id="room-1", contents={}, mobiles={}, characters={victim.id: victim})
        actor = self._build_character(level=30, skills=[{"name": "wands", "level": 100}])
        wand = SimpleNamespace(
            id="obj-wand-2",
            name="wand crystal",
            short_description="a crystal wand",
            item_type="wand",
            value0="22",
            value2="1",
            value3=SimpleNamespace(name="magic missile", handler_id="spell.magic_missile", target="CHAR_OFFENSIVE"),
            level=10,
            weight=1,
        )
        actor.add_item(wand)
        Equipped.equip_item(actor, wand, "held")
        spell_api = _SpellApiDouble()
        skill_registry = SimpleNamespace(get_or_none=lambda **kwargs: SimpleNamespace(id=f"skill-{kwargs.get('name')}", name=kwargs.get("name")))

        with patch.object(sys.modules["interp.commands.Object"].random, "randint", return_value=1):
            payload = self._commands(room, skill_registry=skill_registry, spell_api=spell_api).do_zap(
                actor,
                self._build_context("receiver", room, actor, "zap"),
            )

        self.assertEqual(["Receiver"], spell_api.targets)
        self.assertEqual(["Receiver"], spell_api.started)
        self.assertEqual("You zap Receiver with a crystal wand.\r\n", payload["payloads"][0]["to_char"])
        self.assertEqual("Tester zaps you with a crystal wand.\r\n", payload["payloads"][0]["to_victim"])
        self.assertEqual("Your a crystal wand explodes into fragments.\r\n", payload["payloads"][-1]["to_char"])
        self.assertIsNone(actor.equipped.held)
        self.assertNotIn(wand, actor.loot)


if __name__ == "__main__":
    unittest.main()
