import json
import os
import sys
import types
import unittest
from copy import deepcopy
from types import SimpleNamespace
from unittest.mock import Mock


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
COMMANDS_PATH = os.path.join(ROOT, "resources", "collections", "SOMDB.Commands.json")
SKILLS_PATH = os.path.join(ROOT, "resources", "collections", "SOMDB.Skills.json")
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


class _CharacterApi:
    _positions = {
        "POS_DEAD": 0,
        "POS_STUNNED": 3,
        "POS_RESTING": 6,
        "POS_FIGHTING": 7,
        "POS_STANDING": 8,
    }

    @staticmethod
    def get_enum(name: str):
        if name == "affectedBy":
            return SimpleNamespace(
                AFF_BLIND=SimpleNamespace(value=1),
                AFF_FLYING=SimpleNamespace(value=2),
                AFF_BERSERK=SimpleNamespace(value=4),
                AFF_CALM=SimpleNamespace(value=8),
                AFF_HASTE=SimpleNamespace(value=16),
                AFF_SLOW=SimpleNamespace(value=32),
            )
        if name == "weaponClass":
            return SimpleNamespace(WEAPON_DAGGER=SimpleNamespace(value=1))
        return SimpleNamespace()

    @staticmethod
    def is_npc(entity):
        return bool(getattr(entity, "is_npc", False))

    @staticmethod
    def is_awake(_entity):
        return True

    @classmethod
    def pos_value(cls, name: str) -> int:
        return int(cls._positions.get(name, -1))

    @classmethod
    def position_value(cls, entity) -> int:
        return int(getattr(entity, "position", cls._positions["POS_STANDING"]))

    @classmethod
    def set_position(cls, entity, name: str):
        entity.position = cls.pos_value(name)

    @staticmethod
    def is_affected_by_name(entity, _bits, name: str) -> bool:
        return str(name or "") in set(getattr(entity, "affects", set()) or set())

    @staticmethod
    def is_immortal(_entity):
        return False


class _PlayerUtil:
    @staticmethod
    def get_target(_character, arg, room):
        if room is None:
            return None
        wanted = str(arg or "").strip().lower()
        for key, value in getattr(room, "targets", {}).items():
            if str(key).lower() == wanted:
                return value
        return None


class _MovementUtil:
    @staticmethod
    def sector_cost(_sector):
        return 1

    @staticmethod
    def get_exit_flag(_flags, *_names):
        return 0


class _EffectUtil:
    @staticmethod
    def affect_to_char(_character, _effect):
        return None

    @staticmethod
    def remove_item_effects(_victim, _obj):
        return None


class _SkillUtil:
    @staticmethod
    def check_improve(_character, _skill_id, _success, _multiplier=1):
        return None


class _FightHandler:
    @staticmethod
    def _combat_target_name(target):
        return str(getattr(target, "name", "") or "")


class _StatusFlags(SimpleNamespace):
    pulse_wait: int = 0
    pulse_daze: int = 0


class _Context(SimpleNamespace):
    def finish(self):
        self.done = True


_stub_module("injector", inject=lambda target: target)
_stub_package("server")
_stub_module("server.LoggerFactory", LoggerFactory=_LoggerFactory)
_stub_package("util")
_load_module("util.GenericUtil", "util/GenericUtil.py")
_load_module("util.FightUtil", "util/FightUtil.py")
_load_module("util.InterpUtil", "util/InterpUtil.py")
_stub_module("util.PlayerUtil", PlayerUtil=_PlayerUtil)
_stub_module("util.MovementUtil", MovementUtil=_MovementUtil)
_stub_module("util.ItemUtil", ItemUtil=SimpleNamespace(find_inventory_item=lambda *_args, **_kwargs: None, find_room_item=lambda *_args, **_kwargs: None, has_flag=lambda *_args, **_kwargs: False))
_stub_module("util.EffectUtil", EffectUtil=_EffectUtil)
_stub_module("util.SkillUtil", SkillUtil=_SkillUtil)
_stub_module("util.CommunicationsUtil", CommunicationsUtil=SimpleNamespace(has_comm=lambda *_args, **_kwargs: False, split_first=lambda text: (text.split(maxsplit=1)[0], text.split(maxsplit=1)[1] if len(text.split(maxsplit=1)) > 1 else "") if text else ("", "")))
_stub_package("game")
_load_module("game.GamePayload", "game/GamePayload.py")
_load_module("game.action", "game/action/__init__.py")
_stub_module("game.RegistryService", RegistryService=object)
_stub_module("game.WeatherHandler", WeatherHandler=object)
_stub_package("area")
_stub_module("area.RoomRegistry", RoomRegistry=object)
_stub_package("interp")
_stub_module("interp.Context", Context=_Context)
_load_module("interp.HelpEntry", "interp/HelpEntry.py")
Command = _load_module("interp.Command", "interp/Command.py").Command
_load_module("interp.InterpView", "interp/InterpView.py")
_stub_module("api.CharacterApi", CharacterApi=_CharacterApi)
_stub_module("api.MovementApi", MovementApi=SimpleNamespace())
_stub_module("api.SkillApi", SkillApi=object)
InterpApi = _load_module("api.InterpApi", "api/InterpApi.py").InterpApi
_stub_package("fight")
_stub_module("fight.FightHandler", FightHandler=_FightHandler)
_load_module("fight.FightView", "fight/FightView.py")
_stub_package("skill")
_stub_module("skill.SkillRegistry", SkillRegistry=object)
FightApi = _load_module("api.FightApi", "api/FightApi.py").FightApi
_stub_package("item")
_stub_module("item.Effect", Effect=SimpleNamespace)
_stub_package("player")
_stub_module("player.Character", Character=object)
_stub_module("player.CharacterAdvancement", CharacterAdvancement=SimpleNamespace(gain_experience=lambda *_args, **_kwargs: None))
Skill = _load_module("skill.Skill", "skill/Skill.py").Skill
sys.modules["skill"].Skill = Skill
_stub_module("skill.SpellContext", SpellContext=SimpleNamespace)
_stub_module("api.SpellApi", SpellApi=lambda: SimpleNamespace(execute_lambdas=lambda *_args, **_kwargs: None, queue_cast_announcement=lambda *_args, **_kwargs: None, start_offensive_combat=lambda *_args, **_kwargs: None))
Fight = _load_module("interp.commands.Fight", "interp/commands/Fight.py").Fight


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


def _load_skill(name: str) -> Skill:
    with open(SKILLS_PATH, "r", encoding="utf-8") as handle:
        skills = json.load(handle)
    for entry in skills:
        if entry.get("name") == name:
            return Skill.from_json(deepcopy(entry))
    raise KeyError(name)


class _SkillRegistry:
    def __init__(self, skills):
        self._skills = dict(skills)

    def get(self, **kwargs):
        return self._skills[kwargs["name"]]

    def get_or_none(self, **kwargs):
        return self._skills.get(kwargs["name"])


class TestFightDynamicCommands(unittest.TestCase):
    def test_migrated_fight_metadata_has_check_lists(self):
        command_names = {"cast", "flee", "murder"}
        skill_names = {"bash", "berserk", "dirt kicking", "disarm", "kick", "rescue", "trip"}

        with open(COMMANDS_PATH, "r", encoding="utf-8") as handle:
            commands = {entry["name"]: entry for entry in json.load(handle)}
        with open(SKILLS_PATH, "r", encoding="utf-8") as handle:
            skills = {entry["name"]: entry for entry in json.load(handle)}

        for name in command_names:
            self.assertTrue(commands[name].get("checks"), name)
        for name in skill_names:
            self.assertTrue(skills[name].get("checks"), name)

    def test_do_flee_uses_command_check_and_stands_when_not_fighting(self):
        room = SimpleNamespace(id="room-1", exits=[], player_targets=lambda _character: [])
        registry_service = SimpleNamespace(
            room_registry=SimpleNamespace(get=lambda **_kwargs: room, get_or_none=lambda **_kwargs: room),
            skill_registry=_SkillRegistry({}),
            spell_registry=SimpleNamespace(all_spells=lambda: []),
        )
        fight_handler = Mock()
        fight_api = FightApi(registry_service.room_registry, registry_service.skill_registry, Mock(), fight_handler)
        commands = Fight(registry_service, Mock(), fight_api, InterpApi())

        character = SimpleNamespace(
            name="Hero",
            id="char-1",
            room_id="room-1",
            area_id="area-1",
            fighting=None,
            position=_CharacterApi.pos_value("POS_FIGHTING"),
            status_flags=_StatusFlags(pulse_wait=0, pulse_daze=0),
        )
        context = _Context(character=character, command=_load_command("flee"), room=room, result="", parameters=[], done=False)

        payload = commands.do_flee(character, context)

        self.assertTrue(payload["blocked"])
        self.assertEqual("not_fighting", payload["blocked_key"])
        self.assertEqual("You aren't fighting anyone.\r\n", payload["to_char"])
        self.assertEqual(_CharacterApi.pos_value("POS_STANDING"), character.position)

    def test_do_trip_uses_skill_check_for_self_target_and_sets_wait(self):
        trip_skill = _load_skill("trip")
        skill_registry = _SkillRegistry({"trip": trip_skill})
        room = SimpleNamespace(
            id="room-1",
            targets={"hero": None},
            player_targets=lambda _character: [SimpleNamespace(id="watcher-1")],
        )
        registry_service = SimpleNamespace(
            room_registry=SimpleNamespace(get=lambda **_kwargs: room, get_or_none=lambda **_kwargs: room),
            skill_registry=skill_registry,
            spell_registry=SimpleNamespace(all_spells=lambda: []),
        )
        skill_api = Mock()
        skill_api.get_rating.return_value = 75
        fight_handler = Mock()
        fight_handler.is_safe.return_value = (False, "")
        fight_api = FightApi(registry_service.room_registry, skill_registry, skill_api, fight_handler)
        commands = Fight(registry_service, skill_api, fight_api, InterpApi())

        character = SimpleNamespace(
            name="Hero",
            id="char-1",
            room_id="room-1",
            area_id="area-1",
            fighting=None,
            position=_CharacterApi.pos_value("POS_FIGHTING"),
            status_flags=_StatusFlags(pulse_wait=0, pulse_daze=0),
            level=20,
            character_class=SimpleNamespace(name="warrior"),
            affects=set(),
        )
        room.targets["hero"] = character
        context = _Context(character=character, command=_load_command("trip"), room=room, result="hero", parameters=[], done=False)

        payload = commands.do_trip(character, context)

        self.assertTrue(payload["blocked"])
        self.assertEqual("target_self", payload["blocked_key"])
        self.assertEqual("You fall flat on your face!\r\n", payload["to_char"])
        self.assertEqual("Hero trips over their own feet!\r\n", payload["to_room"])
        self.assertEqual(48, character.status_flags.pulse_wait)


if __name__ == "__main__":
    unittest.main()
