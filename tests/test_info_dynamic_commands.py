import json
import os
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
    module.__path__ = [os.path.join(SRC, name)]
    sys.modules[name] = module
    return module


def _stub_module(name: str, **attrs):
    module = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    sys.modules[name] = module
    return module


def _load_module(name: str, relative_path: str):
    import importlib.util

    spec = importlib.util.spec_from_file_location(name, os.path.join(SRC, relative_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class _Logger:
    def info(self, *_args, **_kwargs):
        return None

    def error(self, *_args, **_kwargs):
        return None

    def warn(self, *_args, **_kwargs):
        return None

    def debug(self, *_args, **_kwargs):
        return None


class _LoggerFactory:
    @staticmethod
    def get_logger(_name):
        return _Logger()


class _StatusFlags:
    def __init__(self, act: int = 0, comm: int = 0):
        self.act = act
        self.comm = comm

    def assign_bitfield(self, name: str, value: int):
        setattr(self, name, value)


class _CharacterMacros:
    @staticmethod
    def get_enum(name: str):
        if name == "playerActBits":
            return SimpleNamespace(
                PLR_AUTOASSIST=SimpleNamespace(value=1),
                PLR_AUTOEXIT=SimpleNamespace(value=2),
                PLR_AUTOGOLD=SimpleNamespace(value=4),
                PLR_AUTOLOOT=SimpleNamespace(value=8),
                PLR_AUTOSAC=SimpleNamespace(value=16),
                PLR_AUTOSPLIT=SimpleNamespace(value=32),
                PLR_CANLOOT=SimpleNamespace(value=64),
                PLR_NOFOLLOW=SimpleNamespace(value=128),
                PLR_NOSUMMON=SimpleNamespace(value=256),
            )
        if name == "commFlags":
            return SimpleNamespace(
                COMM_BRIEF=SimpleNamespace(value=1),
                COMM_COMPACT=SimpleNamespace(value=2),
                COMM_COMBINE=SimpleNamespace(value=4),
                COMM_PROMPT=SimpleNamespace(value=8),
                COMM_SHOW_AFFECTS=SimpleNamespace(value=16),
            )
        if name == "actBits":
            return SimpleNamespace(ACT_PRACTICE=SimpleNamespace(value=1))
        if name == "itemFlags":
            return SimpleNamespace()
        return SimpleNamespace()

    @staticmethod
    def is_set(value: int, bit: int) -> bool:
        return (int(value) & int(bit)) != 0

    @classmethod
    def set_act_flags(cls, character, bit: int):
        character.status_flags.assign_bitfield("act", int(character.status_flags.act) | int(bit))

    @classmethod
    def unset_act_flags(cls, character, bit: int):
        character.status_flags.assign_bitfield("act", int(character.status_flags.act) & ~int(bit))

    @classmethod
    def set_comm_flags(cls, character, bit: int):
        character.status_flags.assign_bitfield("comm", int(character.status_flags.comm) | int(bit))

    @classmethod
    def unset_comm_flags(cls, character, bit: int):
        character.status_flags.assign_bitfield("comm", int(character.status_flags.comm) & ~int(bit))

    @classmethod
    def toggle_player_act(cls, character, bit_name: str, off_text: str, on_text: str):
        bit = getattr(cls.get_enum("playerActBits"), bit_name).value
        if cls.is_set(character.status_flags.act, bit):
            cls.unset_act_flags(character, bit)
            return off_text
        cls.set_act_flags(character, bit)
        return on_text

    @classmethod
    def toggle_comm(cls, character, bit_name: str, off_text: str, on_text: str):
        bit = getattr(cls.get_enum("commFlags"), bit_name).value
        if cls.is_set(character.status_flags.comm, bit):
            cls.unset_comm_flags(character, bit)
            return off_text
        cls.set_comm_flags(character, bit)
        return on_text

    @staticmethod
    def is_npc(_character) -> bool:
        return False

    @staticmethod
    def is_awake(_character) -> bool:
        return True

    @staticmethod
    def is_outside(character) -> bool:
        return bool(getattr(character, "is_outside", False))

    @staticmethod
    def who_line(_viewer, target) -> str:
        return str(getattr(target, "name", ""))

    @staticmethod
    def find_owned_item(character, wanted: str):
        for item in getattr(character, "inventory", []):
            if str(getattr(item, "name", "")).lower() == str(wanted or "").lower():
                return item
        return None

    @staticmethod
    def target_equipment_lines(_character, _labels):
        return []


class _SkillUtil:
    @staticmethod
    def _entry_name(entry) -> str:
        return str(entry.get("name", "") or "").strip() if isinstance(entry, dict) else str(getattr(entry, "name", "") or "").strip()

    @staticmethod
    def _entry_level(entry) -> int:
        return int(entry.get("level", 0)) if isinstance(entry, dict) else int(getattr(entry, "level", 0))

    @staticmethod
    def is_practice_trainer(mob, practice_bit: int) -> bool:
        flags = int(getattr(getattr(mob, "mobile_flags", None), "act", 0))
        return (flags & practice_bit) != 0 or "practice" in str(getattr(mob, "long_description", "") or "").lower()

    @staticmethod
    def find_character_skill(entries, raw: str):
        wanted = str(raw or "").strip().lower()
        prefix_match = None
        for entry in entries:
            name = _SkillUtil._entry_name(entry).lower()
            if name == wanted:
                return entry
            if prefix_match is None and name.startswith(wanted):
                prefix_match = entry
        return prefix_match

    @staticmethod
    def learned_entry_name(entry) -> str:
        return _SkillUtil._entry_name(entry)

    @staticmethod
    def learned_level(entry) -> int:
        return _SkillUtil._entry_level(entry)

    @staticmethod
    def practice_meta(_ability_name: str):
        return None

    @staticmethod
    def practice_visible(character, meta_or_name) -> bool:
        meta = meta_or_name
        if isinstance(meta_or_name, str):
            meta = _SkillUtil.practice_meta(meta_or_name)
        if meta is None:
            return True
        level_map = getattr(meta, "level_by_class", {}) or {}
        class_name = str(getattr(getattr(character, "character_class", None), "name", "") or "").strip().lower()
        required = int(level_map.get(class_name, level_map.get("mage", 99)))
        return int(getattr(character, "level", 0)) >= required

    @staticmethod
    def practice_rating(character, meta_or_name) -> int:
        meta = meta_or_name
        if isinstance(meta_or_name, str):
            meta = _SkillUtil.practice_meta(meta_or_name)
        if meta is None:
            return 1
        rating_map = getattr(meta, "rating_by_class", {}) or {}
        class_name = str(getattr(getattr(character, "character_class", None), "name", "") or "").strip().lower()
        return int(rating_map.get(class_name, rating_map.get("mage", 0)))

    @staticmethod
    def visible_learned_entries(character):
        entries = []
        for entry in list(getattr(character, "skills", []) or []) + list(getattr(character, "spells", []) or []):
            if _SkillUtil._entry_level(entry) < 1:
                continue
            if not _SkillUtil.practice_visible(character, _SkillUtil._entry_name(entry)):
                continue
            entries.append(entry)
        return entries

    @staticmethod
    def find_learned_entry(character, raw: str):
        return _SkillUtil.find_character_skill(_SkillUtil.visible_learned_entries(character), raw)

    @staticmethod
    def practice_adept(character) -> int:
        return int(getattr(getattr(character, "character_class", None), "skill_adept", 75))

    @staticmethod
    def practice_gain(_character, _rating: int) -> int:
        return 5


class _ItemMacros:
    @staticmethod
    def find_comparable_equipped_item(_character, obj1):
        return None if obj1 is None else SimpleNamespace(name="equipped", item_type=getattr(obj1, "item_type", ""), compare_value=10)

    @staticmethod
    def compare_value(obj):
        return getattr(obj, "compare_value", None) if obj is not None else None


class _ItemUtil:
    @staticmethod
    def format_obj_to_char(obj, **_kwargs):
        return getattr(obj, "name", "")

    @staticmethod
    def find_item(_character, room, arg):
        if room is None:
            return None
        return room.items.get(arg)

    @staticmethod
    def is_container_like(obj):
        return bool(getattr(obj, "container_like", False))

    @staticmethod
    def is_drink_container(obj):
        return bool(getattr(obj, "drink_container", False))


class _PlayerUtil:
    @staticmethod
    def visible(_character, session_handler):
        return [session.character for session in session_handler.get_playing_sessions()]

    @staticmethod
    def get_target(_character, arg, room):
        if room is None:
            return None
        return room.targets.get(arg)


class _InterpUtil:
    @staticmethod
    def one_argument(text: str):
        parts = str(text or "").split(maxsplit=1)
        if not parts:
            return "", ""
        if len(parts) == 1:
            return parts[0], ""
        return parts[0], parts[1]


class _Context(SimpleNamespace):
    def finish(self):
        self.done = True

    def player_handler(self):
        return getattr(self, "player_handler_value", None)


_stub_module("injector", inject=lambda target: target)
_stub_package("server")
_stub_module("server.LoggerFactory", LoggerFactory=_LoggerFactory)
_stub_package("util")
_load_module("util.GenericUtil", "util/GenericUtil.py")
_stub_module("util.InfoUtil", InfoUtil=SimpleNamespace())
_stub_module("util.InterpUtil", InterpUtil=_InterpUtil)
_stub_module("util.ItemUtil", ItemUtil=_ItemUtil)
_stub_module("util.PlayerUtil", PlayerUtil=_PlayerUtil)
_stub_module("util.SkillUtil", SkillUtil=_SkillUtil)
_stub_package("game")
_load_module("game.GamePayload", "game/GamePayload.py")
_stub_module("game.RegistryService", RegistryService=object)
_stub_module("game.WeatherHandler", WeatherHandler=object)
_stub_package("item")
_stub_module("item.ItemApi", ItemMacros=_ItemMacros)
_stub_package("player")
_stub_module("player.Character", Character=object)
_stub_module("player.CharacterApi", CharacterMacros=_CharacterMacros)
_stub_package("server.session")
_stub_module("server.session.SessionHandler", SessionHandler=object)
_stub_package("interp")
_stub_module("interp.Context", Context=_Context)
_stub_module("interp.HelpEntry", HelpEntry=object)

Command = _load_module("interp.Command", "interp/Command.py").Command
_load_module("interp.InterpView", "interp/InterpView.py")
_load_module("interp.InterpCheck", "interp/InterpCheck.py")
_load_module("interp.InterpActionDefinition", "interp/InterpActionDefinition.py")
_load_module("interp.InterpPlan", "interp/InterpPlan.py")
_load_module("interp.InterpApi", "api/InterpApi.py")
Info = _load_module("interp.commands.Info", "interp/commands/Info.py").Info


def _load_command(name: str) -> Command:
    with open(COMMANDS_PATH, "r", encoding="utf-8") as handle:
        commands = json.load(handle)
    for entry in commands:
        if entry.get("name") == name:
            payload = deepcopy(entry)
            payload.setdefault("shortcuts", "")
            payload.setdefault("function", [])
            payload.setdefault("usage", "")
            return Command.from_json(payload)
    raise KeyError(name)


class TestInfoDynamicCommands(unittest.TestCase):
    def _commands(self):
        room_registry = SimpleNamespace(get_or_none=lambda **_kwargs: None)
        registry_service = SimpleNamespace(
            interp_registry=SimpleNamespace(all_commands=lambda: []),
            room_registry=room_registry,
            skill_registry=SimpleNamespace(all_skills=lambda: []),
            spell_registry=SimpleNamespace(all_spells=lambda: []),
        )
        session_handler = SimpleNamespace(get_playing_sessions=lambda: [])
        weather_handler = SimpleNamespace(time_info=None, weather_info=None)
        enum_provider = SimpleNamespace(get=_CharacterMacros.get_enum)
        commands = Info(registry_service, session_handler, weather_handler, enum_provider)
        commands.PlayerActBits = _CharacterMacros.get_enum("playerActBits")
        return commands, room_registry, registry_service, session_handler, weather_handler

    def test_scroll_invalid_number_uses_command_check(self):
        commands, _room_registry, _registry_service, _session_handler, _weather_handler = self._commands()
        character = SimpleNamespace(context={}, status_flags=_StatusFlags(), prompt_format=None)
        context = _Context(character=character, command=_load_command("scroll"), result="abc", parameters=[], done=False)

        text = commands.do_scroll(character, context)

        self.assertEqual("You must provide a number.\r\n", text)

    def test_scroll_default_renders_payload_tokens(self):
        commands, _room_registry, _registry_service, _session_handler, _weather_handler = self._commands()
        character = SimpleNamespace(context={"scroll_lines": 18}, status_flags=_StatusFlags(), prompt_format=None)
        context = _Context(character=character, command=_load_command("scroll"), result="", parameters=[], done=False)

        text = commands.do_scroll(character, context)

        self.assertEqual("You currently display 20 lines per page.\r\n", text)

    def test_practice_no_sessions_uses_command_check(self):
        commands, room_registry, registry_service, _session_handler, _weather_handler = self._commands()
        registry_service.skill_registry = SimpleNamespace(
            all_skills=lambda: [SimpleNamespace(name="dagger", level_by_class={"thief": 1}, rating_by_class={"thief": 4})]
        )
        commands.skill_registry = registry_service.skill_registry
        character = SimpleNamespace(
            room_id="room-1",
            status_flags=_StatusFlags(),
            skills=[{"name": "dagger", "level": 10}],
            spells=[],
            level=10,
            character_class=SimpleNamespace(name="thief", skill_adept=75),
            character_attributes=SimpleNamespace(practices=0),
        )
        trainer = SimpleNamespace(mobile_flags=SimpleNamespace(act=1), long_description="")
        room = SimpleNamespace(mobiles={"trainer": trainer}, player_targets=lambda _character: [])
        room_registry.get_or_none = lambda **_kwargs: room
        commands.room_registry = room_registry
        context = _Context(character=character, command=_load_command("practice"), result="dagger", parameters=[], done=False)

        text = commands.do_practice(character, context)

        self.assertEqual("You have no practice sessions left.\r\n", text)

    def test_compare_incompatible_items_uses_command_check(self):
        commands, _room_registry, _registry_service, _session_handler, _weather_handler = self._commands()
        character = SimpleNamespace(
            inventory=[
                SimpleNamespace(name="sword", item_type="weapon", compare_value=10),
                SimpleNamespace(name="vest", item_type="armor", compare_value=8),
            ],
            status_flags=_StatusFlags(),
        )
        context = _Context(character=character, command=_load_command("compare"), result="sword vest", parameters=[], done=False)

        text = commands.do_compare(character, context)

        self.assertEqual("You can't compare those items.\r\n", text)

    def test_weather_indoors_uses_command_check(self):
        commands, _room_registry, _registry_service, _session_handler, weather_handler = self._commands()
        weather_handler.weather_info = SimpleNamespace(sky=0, change=0)
        commands.weather_handler = weather_handler
        character = SimpleNamespace(is_outside=False, status_flags=_StatusFlags())
        context = _Context(character=character, command=_load_command("weather"), result="", parameters=[], done=False)

        text = commands.do_weather(character, context)

        self.assertEqual("You can't see the weather indoors.\r\n", text)

    def test_show_toggle_renders_command_payload(self):
        commands, _room_registry, _registry_service, _session_handler, _weather_handler = self._commands()
        character = SimpleNamespace(status_flags=_StatusFlags(comm=0))
        context = _Context(character=character, command=_load_command("show"), result="", parameters=[], done=False)

        text = commands.do_show(character, context)

        self.assertEqual("Affects will now be shown in score.\r\n", text)


if __name__ == "__main__":
    unittest.main()
