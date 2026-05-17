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
    def item_takeable(item) -> bool:
        return bool(getattr(item, "takeable", True))

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
    def is_closed_container(item) -> bool:
        return _ItemApi.is_container_closed(item)

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
    def remove_item_from_room(self, item):
        self.contents.pop(item.id, None)

    def player_targets(self, _character):
        return []


class _Container(SimpleNamespace):
    def remove_contained_item(self, item):
        self.contains.remove(item)


class TestObjectGetDynamicCommands(unittest.TestCase):
    def _commands(self, room):
        room_registry = SimpleNamespace(
            get_or_none=lambda **kwargs: room if kwargs.get("id") == room.id else None,
        )
        registry_service = SimpleNamespace(room_registry=room_registry, mobile_registry=None, shop_registry=None)
        commands = Object(registry_service=registry_service, interp_api=InterpApi())
        commands.item_flags = SimpleNamespace()
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

        character.find_inventory_item = _find_inventory_item
        character.add_item = _add_item
        return character

    @staticmethod
    def _build_context(raw, room, character):
        return _Context(
            character=character,
            result=raw,
            parameters=raw.split(),
            room=room,
            command=_load_command("get"),
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


if __name__ == "__main__":
    unittest.main()
