import importlib.util
import sys
import types
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
OBJECT_PATH = SRC / "interp" / "commands" / "Object.py"


def _stub_package(name: str):
    if name in sys.modules:
        return sys.modules[name]
    module = types.ModuleType(name)
    module.__path__ = [str(SRC / name)]
    sys.modules[name] = module
    return module


def _stub_module(name: str, **attrs):
    module = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    sys.modules[name] = module
    return module


for package_name in ("api", "area", "fight", "game", "interp", "item", "player", "server", "skill", "util"):
    _stub_package(package_name)
_stub_package("interp.commands")

_stub_module("injector", inject=lambda target: target)


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


class _GenericUtil:
    @staticmethod
    def to_int(value, default=0):
        try:
            return int(value)
        except (TypeError, ValueError):
            return default


class _ItemUtil:
    @staticmethod
    def parse_raw_arguments(result, parameters):
        raw = str(result or "").strip()
        if not raw and parameters:
            raw = " ".join(parameters).strip()
        parts = raw.split(maxsplit=1)
        if not parts:
            return "", ""
        if len(parts) == 1:
            return parts[0], ""
        return parts[0], parts[1]

    @staticmethod
    def find_room_item(room, wanted):
        if room is None:
            return None
        query = str(wanted or "").strip().lower()
        for item in room.contents.values():
            name = str(getattr(item, "name", "") or "").lower()
            if name == query or name.startswith(query):
                return item
        return None

    @staticmethod
    def find_container(character, room, wanted):
        query = str(wanted or "").strip().lower()
        if hasattr(character, "find_inventory_item"):
            found = character.find_inventory_item(query)
            if found is not None:
                return found
        return _ItemUtil.find_room_item(room, query)

    @staticmethod
    def first_fountain(room):
        if room is None:
            return None
        for item in room.contents.values():
            if _ItemUtil.is_fountain(item):
                return item
        return None

    @staticmethod
    def is_drink_container(item):
        item_type = str(getattr(item, "item_type", "") or "").strip().lower()
        return ("drink" in item_type) or ("fountain" in item_type)

    @staticmethod
    def is_fountain(item):
        item_type = str(getattr(item, "item_type", "") or "").strip().lower()
        return "fountain" in item_type

    @staticmethod
    def is_edible(item):
        item_type = str(getattr(item, "item_type", "") or "").strip().lower()
        return ("food" in item_type) or ("pill" in item_type)

    @staticmethod
    def short(item):
        return getattr(item, "short_description", getattr(item, "name", "it"))


class _CharacterApi:
    @staticmethod
    def is_npc(_character):
        return False

    @staticmethod
    def is_immortal(_character):
        return False


class _InterpApi:
    def evaluate_guards_only(self, context, _action_name):
        name = str(getattr(getattr(context, "command", None), "name", "") or "").lower()
        if name == "drink":
            item = getattr(context, "drink_item", None)
            if (not getattr(context, "drink_arg1", "")) and item is None:
                return {"to_char": context.command.render_message("to_char", "no_argument") + "\r\n"}
            if getattr(context, "drink_arg1", "") and item is None:
                return {"to_char": context.command.render_message("to_char", "item_missing") + "\r\n"}
            if item is not None and not _ItemUtil.is_drink_container(item):
                return {"to_char": context.command.render_message("to_char", "item_not_container") + "\r\n"}
            if item is not None and (not _ItemUtil.is_fountain(item)) and _GenericUtil.to_int(getattr(item, "value1", 0), 0) <= 0:
                return {"to_char": context.command.render_message("to_char", "container_empty") + "\r\n"}
            if item is not None and _GenericUtil.to_int(getattr(getattr(context.character, "status_flags", None), "hunger", 0), 0) > 45:
                return {"to_char": context.command.render_message("to_char", "too_full") + "\r\n"}
        if name == "eat":
            item = getattr(context, "eat_item", None)
            if not getattr(context, "eat_arg1", ""):
                return {"to_char": context.command.render_message("to_char", "no_argument") + "\r\n"}
            if item is None:
                return {"to_char": context.command.render_message("to_char", "item_missing") + "\r\n"}
            if not _ItemUtil.is_edible(item):
                return {"to_char": context.command.render_message("to_char", "not_edible") + "\r\n"}
            if _GenericUtil.to_int(getattr(getattr(context.character, "status_flags", None), "hunger", 0), 0) > 40:
                return {"to_char": context.command.render_message("to_char", "too_full") + "\r\n"}
        if name == "fill":
            dest = getattr(context, "fill_dest", None)
            src = getattr(context, "fill_src", None)
            if not getattr(context, "fill_arg1", ""):
                return {"to_char": context.command.render_message("to_char", "no_argument") + "\r\n"}
            if dest is None:
                return {"to_char": context.command.render_message("to_char", "item_missing") + "\r\n"}
            if (not _ItemUtil.is_drink_container(dest)) or (src is not None and not _ItemUtil.is_drink_container(src)):
                return {"to_char": context.command.render_message("to_char", "not_container") + "\r\n"}
            cap = _GenericUtil.to_int(getattr(dest, "value0", 0), 0)
            cur = _GenericUtil.to_int(getattr(dest, "value1", 0), 0)
            if cap > 0 and cur >= cap:
                return {"to_char": context.command.render_message("to_char", "container_full") + "\r\n"}
        return None

    def render_message_key(self, context, message_key: str, channel: str = "", fallback: str = "", **tokens):
        payload = {}
        channels = [channel] if channel else ["to_char", "to_room", "to_victim"]
        for name in channels:
            text = context.command.render_message(name, message_key, fallback=fallback, **tokens)
            if text:
                payload[name] = text + ("\r\n" if not text.endswith("\r\n") else "")
        return payload


class _Command:
    def __init__(self, name, payload):
        self.name = name
        self._payload = payload

    def render_message(self, channel, key, fallback="", **tokens):
        table = self._payload.get(channel, {})
        template = table.get(key, fallback)
        text = str(template or "")
        for marker, value in {
            "%c": tokens.get("c", ""),
            "%p": tokens.get("p", ""),
            "%l": tokens.get("l", ""),
            "%t": tokens.get("t", ""),
            "%s": tokens.get("s", ""),
            "%T": tokens.get("T", ""),
        }.items():
            text = text.replace(marker, str(value or ""))
        return text


class _SpellApi:
    def __init__(self, *_args, **_kwargs):
        return None


class _Item:
    @staticmethod
    def first_fountain(room):
        return _ItemUtil.first_fountain(room)

    @staticmethod
    def inspect_fill(destination, source):
        from types import SimpleNamespace

        if source is None:
            return SimpleNamespace(blocked_key="sourceMissing", liquid_name="")
        if _ItemUtil.is_fountain(destination) or not _ItemUtil.is_drink_container(destination) or not _ItemUtil.is_drink_container(source):
            return SimpleNamespace(blocked_key="notContainer", liquid_name="")

        dest_capacity = _GenericUtil.to_int(getattr(destination, "value0", 0), 0)
        dest_amount = _GenericUtil.to_int(getattr(destination, "value1", 0), 0)
        if dest_capacity > 0 and dest_amount >= dest_capacity:
            return SimpleNamespace(blocked_key="containerFull", liquid_name="")

        source_liquid = str(getattr(source, "value2", "") or "")
        dest_liquid = str(getattr(destination, "value2", "") or "")
        if dest_amount > 0 and source_liquid and dest_liquid != source_liquid:
            return SimpleNamespace(blocked_key="differentLiquid", liquid_name="")

        if not _ItemUtil.is_fountain(source) and _GenericUtil.to_int(getattr(source, "value1", 0), 0) <= 0:
            return SimpleNamespace(blocked_key="sourceEmpty", liquid_name="")
        return SimpleNamespace(blocked_key="", liquid_name=source_liquid)

    @staticmethod
    def fill_from_source(destination, source):
        result = _Item.inspect_fill(destination, source)
        if result.blocked_key:
            return result
        destination.value2 = result.liquid_name
        destination.value1 = str(_GenericUtil.to_int(getattr(destination, "value0", 0), 0))
        return result


_stub_module("server.LoggerFactory", LoggerFactory=_LoggerFactory)
_stub_module("area.Shop", Shop=SimpleNamespace())
_stub_module("game.Equipped", Equipped=object)
_stub_module("item.Item", Item=_Item)
_stub_module("game.RegistryService", RegistryService=object)
_stub_module("interp.Context", Context=object)
_stub_module("util.GenericUtil", GenericUtil=_GenericUtil)
_stub_module("util.InterpUtil", InterpUtil=SimpleNamespace())
_stub_module("util.MobileUtil", MobileUtil=SimpleNamespace())
_stub_module("util.EffectUtil", EffectUtil=SimpleNamespace(handler=lambda: SimpleNamespace()))
_stub_module("util.ItemUtil", ItemUtil=_ItemUtil)
_stub_module("util.PlayerUtil", PlayerUtil=SimpleNamespace(get_target=lambda *_args, **_kwargs: None))
_stub_module("util.SkillUtil", SkillUtil=SimpleNamespace(check_improve=lambda *_args, **_kwargs: None))
_stub_module("skill.Ability", Ability=SimpleNamespace(check_improve=lambda *_args, **_kwargs: None))
_stub_module("api.ItemApi", ItemApi=SimpleNamespace(is_container_closed=lambda _obj: False))
_stub_module("api.InterpApi", InterpApi=_InterpApi)
_stub_module("api.SpellApi", SpellApi=_SpellApi)
_stub_module("player.Character", Character=object)
_stub_module("api.CharacterApi", CharacterApi=_CharacterApi)
_stub_module("fight.FightHandler", FightHandler=object)
_stub_module("skill.SpellContext", SpellContext=object)


spec = importlib.util.spec_from_file_location("test_object_module", OBJECT_PATH)
object_module = importlib.util.module_from_spec(spec)
sys.modules["test_object_module"] = object_module
spec.loader.exec_module(object_module)
Object = object_module.Object


class TestObjectFountainCommands(unittest.TestCase):
    @staticmethod
    def _build_commands(room):
        room_registry = Mock()
        room_registry.get_or_none.return_value = room
        registry_service = SimpleNamespace(
            room_registry=room_registry,
            mobile_registry=None,
            shop_registry=None,
        )
        enum_provider = SimpleNamespace(get=lambda _name: SimpleNamespace())
        commands = Object(registry_service=registry_service, enum_provider=enum_provider)
        commands.item_flags = SimpleNamespace()
        commands.wear_flags = SimpleNamespace()
        return commands

    @staticmethod
    def _build_character(*items):
        inventory = list(items)
        character = SimpleNamespace(
            id="char1",
            name="Tester",
            room_id="room1",
            loot=inventory,
            status_flags=SimpleNamespace(hunger=0, thirst=0, drunk=0),
        )

        def find_inventory_item(wanted):
            query = str(wanted or "").strip().lower()
            for item in inventory:
                name = str(getattr(item, "name", "") or "").lower()
                if name == query or name.startswith(query):
                    return item
            return None

        character.find_inventory_item = find_inventory_item
        character.equipped_slot_of = lambda _item: None
        character.unequip_item = lambda _slot: None
        character.remove_item = lambda item: inventory.remove(item)
        return character

    @staticmethod
    def _build_room(*items):
        return SimpleNamespace(
            id="room1",
            contents={str(index): item for index, item in enumerate(items, start=1)},
            player_targets=lambda _character: [],
        )

    @staticmethod
    def _build_context(command_name, raw, character=None):
        payloads = {
            "drink": {
                "to_char": {
                    "no_argument": "Drink what?",
                    "item_missing": "You can't find it.",
                "item_not_container": "You can't drink from that.",
                "container_empty": "It is already empty.",
                "too_full": "You're too full to drink more.",
                "full": "You are full.",
                "quenched": "Your thirst is quenched.",
                "alcohol": "You feel drunk.",
                "default": "You drink %l from %p.",
                },
                "to_room": {
                    "default": "%c drinks %l from %p.",
                },
            },
            "eat": {
                "to_char": {
                    "no_argument": "Eat what?",
                    "item_missing": "You do not have that item.",
                    "not_edible": "That's not edible.",
                    "too_full": "You are too full to eat more.",
                    "satiated": "You are no longer hungry.",
                    "full": "You are full.",
                    "default": "You eat %p.",
                },
                "to_room": {
                    "default": "%c eats %p.",
                },
            },
            "fill": {
                "to_char": {
                    "no_argument": "Fill what?",
                    "item_missing": "You do not have that item.",
                    "not_container": "You can't fill that.",
                    "container_full": "It is already full.",
                    "default": "You fill %t with %s from %T.",
                },
                "to_room": {
                    "default": "%c fills %t with %s from %T.",
                },
            },
        }
        return SimpleNamespace(
            character=character,
            result=raw,
            parameters=[],
            room=None,
            finish=Mock(),
            command=_Command(command_name, payloads[command_name]),
        )

    def test_drink_from_fountain_does_not_require_current_amount(self):
        fountain = SimpleNamespace(
            id="obj1",
            name="fountain water",
            short_description="a fountain",
            item_type="fountain",
            value0="0",
            value1="0",
            value2="water",
        )
        room = self._build_room(fountain)
        character = self._build_character()

        payload = self._build_commands(room).do_drink(character, self._build_context("drink", "fountain", character))

        self.assertEqual("You drink water from a fountain.\r\n", payload["to_char"])
        self.assertEqual("0", fountain.value1)

    def test_fill_from_fountain_ignores_empty_current_amount(self):
        fountain = SimpleNamespace(
            id="obj1",
            name="fountain water",
            short_description="a fountain",
            item_type="fountain",
            value0="0",
            value1="0",
            value2="water",
        )
        skin = SimpleNamespace(
            id="obj2",
            name="waterskin skin",
            short_description="a waterskin",
            item_type="drinkcon",
            value0="5",
            value1="0",
            value2="",
        )
        room = self._build_room(fountain)
        character = self._build_character(skin)

        payload = self._build_commands(room).do_fill(character, self._build_context("fill", "waterskin", character))

        self.assertEqual("You fill a waterskin with water from a fountain.\r\n", payload["to_char"])
        self.assertEqual("5", skin.value1)
        self.assertEqual("water", skin.value2)

    def test_drink_updates_existing_hunger_and_thirst_conditions(self):
        drink = SimpleNamespace(
            id="obj1",
            name="waterskin water",
            short_description="a waterskin",
            item_type="drinkcon",
            value0="10",
            value1="10",
            value2="water",
            liquid_affect_data=[0, 1, 10, 0, 10],
        )
        room = self._build_room()
        character = self._build_character(drink)

        payload = self._build_commands(room).do_drink(character, self._build_context("drink", "waterskin", character))

        self.assertEqual("You drink water from a waterskin.\r\n", payload["to_char"])
        self.assertEqual(2, character.status_flags.hunger)
        self.assertEqual(10, character.status_flags.thirst)
        self.assertEqual("0", drink.value1)

    def test_drink_buffalo_skin_matches_rom_water_math(self):
        drink = SimpleNamespace(
            id="obj1",
            name="skin water buffalo",
            short_description="a buffalo water skin",
            item_type="drinkcon",
            value0="64",
            value1="64",
            value2="water",
            liquid_affect_data=[0, 1, 10, 0, 16],
        )
        room = self._build_room()
        character = self._build_character(drink)

        payload = self._build_commands(room).do_drink(character, self._build_context("drink", "skin", character))

        self.assertEqual("You drink water from a buffalo water skin.\r\n", payload["to_char"])
        self.assertEqual(4, character.status_flags.hunger)
        self.assertEqual(16, character.status_flags.thirst)
        self.assertEqual(0, character.status_flags.drunk)
        self.assertEqual("48", drink.value1)

    def test_drink_refuses_when_hunger_meter_is_already_full(self):
        fountain = SimpleNamespace(
            id="obj1",
            name="fountain water",
            short_description="a fountain",
            item_type="fountain",
            value0="0",
            value1="0",
            value2="water",
            liquid_affect_data=[0, 1, 10, 0, 16],
        )
        room = self._build_room(fountain)
        character = self._build_character()
        character.status_flags.hunger = 46

        payload = self._build_commands(room).do_drink(character, self._build_context("drink", "fountain", character))

        self.assertEqual("You're too full to drink more.\r\n", payload["to_char"])

    def test_eat_updates_hunger_and_stops_when_sated(self):
        food = SimpleNamespace(
            id="obj1",
            name="bread loaf",
            short_description="a loaf of bread",
            item_type="food",
            value0="5",
            value1="8",
            value3="0",
        )
        room = self._build_room()
        character = self._build_character(food)
        character.status_flags.hunger = 0

        payload = self._build_commands(room).do_eat(character, self._build_context("eat", "bread", character))

        self.assertEqual("You eat a loaf of bread.\r\nYou are no longer hungry.\r\n", payload["to_char"])
        self.assertEqual(13, character.status_flags.hunger)
        self.assertNotIn(food, character.loot)


if __name__ == "__main__":
    unittest.main()
