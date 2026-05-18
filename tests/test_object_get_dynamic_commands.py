import importlib.util
import json
import os
import re
import sys
import types
import unittest
from copy import deepcopy
from types import SimpleNamespace


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


class _ItemApi:
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
    def is_nodrop(item, _item_flags) -> bool:
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
    def finish(self):
        self.done = True


for package_name in ("api", "game", "interp", "item", "player", "server", "util"):
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
_stub_module("util.EffectUtil", EffectUtil=SimpleNamespace())
_stub_module("util.ItemUtil", ItemUtil=_ItemUtil)
_stub_module("game.Equipped", Equipped=object)
_stub_module("game.RegistryService", RegistryService=object)
_stub_module("interp.Context", Context=_Context)
_stub_module("item.Item", Item=object)
_stub_module("player.Character", Character=object)

_load_module("util.GenericUtil", "util/GenericUtil.py")
GamePayload = _load_module("game.GamePayload", "game/GamePayload.py").GamePayload
_load_module("interp.HelpEntry", "interp/HelpEntry.py")
_load_module("interp.InterpView", "interp/InterpView.py")
_load_module("game.action", "game/action/__init__.py")
_load_module("util.InterpUtil", "util/InterpUtil.py")
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

    def player_targets(self, _character):
        return []


class _Container(SimpleNamespace):
    def remove_contained_item(self, item):
        self.contains.remove(item)


class TestObjectGetDynamicCommands(unittest.TestCase):
    def _commands(self, room, *, shop_registry=None, weather_handler=None):
        room_registry = SimpleNamespace(
            get_or_none=lambda **kwargs: room if kwargs.get("id") == room.id else None,
            get=lambda **kwargs: room if kwargs.get("id") == room.id else None,
        )
        registry_service = SimpleNamespace(room_registry=room_registry, mobile_registry=None, shop_registry=shop_registry)
        commands = Object(registry_service=registry_service, interp_api=InterpApi(), weather_handler=weather_handler)
        commands.item_flags = SimpleNamespace(
            ITEM_INVENTORY=SimpleNamespace(value=1),
            ITEM_HAD_TIMER=SimpleNamespace(value=2),
            ITEM_SELL_EXTRACT=SimpleNamespace(value=4),
        )
        commands.wear_flags = SimpleNamespace()
        return commands

    @staticmethod
    def _build_character(*items, is_immortal=False):
        inventory = list(items)
        character = SimpleNamespace(
            id="char-1",
            name="Tester",
            room_id="room-1",
            loot=inventory,
            gold=0,
            silver=0,
            is_immortal=is_immortal,
            character_attributes=SimpleNamespace(max_items=10, max_weight=100),
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

        character.find_inventory_item = _find_inventory_item
        character.add_item = _add_item
        character.remove_item = _remove_item
        character.equipped_slot_of = lambda _item: None
        character.unequip_item = lambda _slot: None
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
        shop = SimpleNamespace(
            keeper="100",
            open_hour=0,
            is_open_at=lambda _hour: True,
            buy_price=lambda _obj: 96,
            sell_price=lambda *_args, **_kwargs: 0,
        )
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
        shop = SimpleNamespace(
            keeper="100",
            open_hour=0,
            is_open_at=lambda _hour: True,
            buy_price=lambda _obj: 0,
            sell_price=lambda *_args, **_kwargs: 0,
        )
        shop_registry = SimpleNamespace(find_by_keeper_vnum=lambda keeper_vnum: shop if str(keeper_vnum) == "100" else None)
        character = self._build_character()

        payload = self._commands(room, shop_registry=shop_registry, weather_handler=SimpleNamespace(time_info=SimpleNamespace(hour=12))).do_buy(
            character,
            self._build_context("shield", room, character, "buy"),
        )

        self.assertEqual("I don't sell that -- try 'list'.\r\n", payload["to_char"])
        self.assertEqual("no_such_item", payload["blocked_key"])

    def test_sell_item_uses_payload_templates(self):
        blade = SimpleNamespace(id="obj-12", vnum="202", name="blade iron", short_description="an iron blade", level=5, cost=100, weight=1, extra_flags=0, timer=0)
        keeper = SimpleNamespace(id="mob-3", vnum="100", inventory=[], short_description="the shopkeeper", gold=1, silver=0)
        room = _Room(id="room-1", contents={}, mobiles={"keeper": keeper})
        shop = SimpleNamespace(
            keeper="100",
            open_hour=0,
            is_open_at=lambda _hour: True,
            buy_price=lambda _obj: 0,
            sell_price=lambda _obj, *_args, **_kwargs: 50,
        )
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
        shop = SimpleNamespace(
            keeper="100",
            open_hour=0,
            is_open_at=lambda _hour: True,
            buy_price=lambda _obj: 0,
            sell_price=lambda _obj, *_args, **_kwargs: 0,
        )
        shop_registry = SimpleNamespace(find_by_keeper_vnum=lambda keeper_vnum: shop if str(keeper_vnum) == "100" else None)
        character = self._build_character(junk)

        payload = self._commands(room, shop_registry=shop_registry, weather_handler=SimpleNamespace(time_info=SimpleNamespace(hour=12))).do_sell(
            character,
            self._build_context("junk", room, character, "sell"),
        )

        self.assertEqual("the shopkeeper looks uninterested in a brass trinket.\r\n", payload["to_char"])
        self.assertEqual("looks_uninterested", payload["blocked_key"])


if __name__ == "__main__":
    unittest.main()
