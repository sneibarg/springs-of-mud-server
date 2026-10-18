import os
import sys
import unittest
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import types
from unittest.mock import Mock, patch


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

if "registries" not in sys.modules:
    registries = types.ModuleType("registries")

    class _Registry:
        @classmethod
        def __class_getitem__(cls, _item):
            return cls

    registries.Registry = _Registry
    sys.modules["registries"] = registries

if "injector" not in sys.modules:
    injector = types.ModuleType("injector")
    injector.inject = lambda target: target
    sys.modules["injector"] = injector


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


def _load_module(name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(name, SRC / relative_path)
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


class _LoggerFactory:
    @staticmethod
    def get_logger(_name):
        return _Logger()


class _RoomRegistry:
    pass


class _FightHandler:
    WEAPON_SKILL_NAMES = {
        "WEAPON_SWORD": "sword",
        "WEAPON_DAGGER": "dagger",
        "WEAPON_SPEAR": "spear",
        "WEAPON_MACE": "mace",
        "WEAPON_AXE": "axe",
        "WEAPON_FLAIL": "flail",
        "WEAPON_WHIP": "whip",
        "WEAPON_POLEARM": "polearm",
    }


class _SkillApi:
    pass


class _SkillRegistry:
    pass


class _CharacterMacros:
    @staticmethod
    def is_npc(_entity):
        return False

    @staticmethod
    def is_awake(_entity):
        return True

    @staticmethod
    def get_enum(_name):
        return SimpleNamespace()


class _PlayerUtil:
    @staticmethod
    def get_target(_actor, _argument, _room):
        return None


_stub_package("server")
_stub_module("server.LoggerFactory", LoggerFactory=_LoggerFactory)
_stub_package("util")
_load_module("util.GenericUtil", "util/GenericUtil.py")
_load_module("util.FightUtil", "util/FightUtil.py")
_stub_module("util.PlayerUtil", PlayerUtil=_PlayerUtil)
_stub_package("game")
_load_module("game.GamePayload", "game/GamePayload.py")
_stub_package("area")
_stub_module("area.RoomRegistry", RoomRegistry=_RoomRegistry)
_stub_package("combat")
_load_module("combat.FightCheck", "combat/CombatCheck.py")
_load_module("combat.FightView", "combat/CombatView.py")
_load_module("combat.FightPlan", "combat/CombatPlan.py")
_load_module("combat.FightActionDefinition", "combat/CombatActionDefinition.py")
_stub_module("combat.FightHandler", FightHandler=_FightHandler)
_stub_package("skill")
_stub_module("skill.SkillApi", SkillApi=_SkillApi)
_stub_module("skill.SkillRegistry", SkillRegistry=_SkillRegistry)
_stub_package("player")
_stub_module("player.CharacterApi", CharacterMacros=_CharacterMacros)

GamePayload = _load_module("game.GamePayload", "game/GamePayload.py").GamePayload
Skill = _load_module("skill.Skill", "skill/Skill.py").Skill
FightView = sys.modules["combat.FightView"].FightView
fight_api_module = _load_module("combat.FightApi", "combat/FightApi.py")
FightApi = fight_api_module.FightApi


class TestFightApiData(unittest.TestCase):
    def test_skill_from_json_normalizes_fight_metadata(self):
        skill = Skill.from_json(
            {
                "_id": {"$oid": "skill-1"},
                "name": "dagger",
                "kind": "skill",
                "handlerId": "skill.none",
                "target": "IGNORE",
                "minPosition": "FIGHTING",
                "nounDamage": "",
                "msgOff": "!Dagger!",
                "msgObj": "",
                "levelByClass": {"warrior": 1},
                "ratingByClass": {"warrior": 2},
                "slot": 0,
                "minMana": 0,
                "beats": 0,
                "payload": {"toChar": {"noArgument": "Kill whom?"}},
                "guards": [
                    {
                        "predicate": "lambda v: not v.argument",
                        "messageKey": "noArgument",
                        "tokenFactory": "lambda v: victim_name_tokens(v)",
                    }
                ],
                "fightExecutor": "multi_hit",
                "fightPlan": {"dt": "TYPE_UNDEFINED"},
            }
        )

        self.assertEqual("skill-1", skill.id)
        self.assertIsInstance(skill.payload, GamePayload)
        self.assertEqual("Kill whom?", skill.payload.to_char["no_argument"])
        self.assertEqual("no_argument", skill.guards[0]["message_key"])
        self.assertEqual("lambda v: victim_name_tokens(v)", skill.guards[0]["token_factory"])
        self.assertEqual("multi_hit", skill.fight_executor)
        self.assertEqual({"dt": "TYPE_UNDEFINED"}, skill.fight_plan)

    def test_kill_uses_active_melee_skill_data(self):
        dagger_skill = Skill.from_json(
            {
                "_id": {"$oid": "skill-2"},
                "name": "dagger",
                "kind": "skill",
                "handlerId": "skill.none",
                "target": "IGNORE",
                "minPosition": "FIGHTING",
                "nounDamage": "",
                "msgOff": "!Dagger!",
                "msgObj": "",
                "levelByClass": {"warrior": 1},
                "ratingByClass": {"warrior": 2},
                "slot": 0,
                "minMana": 0,
                "beats": 0,
                "guards": [
                    {"predicate": "lambda v: not v.argument", "messageKey": "noArgument"},
                    {
                        "predicate": "lambda v: v.current_fighting is not None and v.current_fighting is v.victim",
                        "messageKey": "alreadyFighting",
                        "tokenFactory": "lambda v: victim_name_tokens(v)",
                    },
                ],
                "fightExecutor": "multi_hit",
                "fightPlan": {"dt": "TYPE_UNDEFINED"},
            }
        )

        room_registry = Mock()
        room_registry.get_or_none.return_value = SimpleNamespace(id="room-1")
        skill_registry = Mock()
        skill_registry.get_or_none.side_effect = lambda **kwargs: dagger_skill if kwargs.get("name") == "dagger" else None
        skill_api = Mock()
        skill_api.get_rating.return_value = 75
        fight_handler = Mock()
        fight_handler.is_safe.return_value = (False, "")

        api = FightApi(room_registry, skill_registry, skill_api, fight_handler)
        victim = SimpleNamespace(id="mob-1", name="goblin")
        character = SimpleNamespace(
            room_id="room-1",
            equipped=SimpleNamespace(wielded=SimpleNamespace(item_type="weapon", value0=1)),
            fighting=victim,
            level=10,
            character_class=SimpleNamespace(name="warrior"),
        )
        context = SimpleNamespace(
            command=SimpleNamespace(name="kill", payload=Mock()),
            room=room_registry.get_or_none.return_value,
            result="goblin",
            parameters=[],
        )

        weapon_class = SimpleNamespace(WEAPON_DAGGER=SimpleNamespace(value=1))
        with patch.object(fight_api_module.PlayerUtil, "get_target", return_value=victim), \
             patch.object(fight_api_module.CharacterMacros, "is_npc", return_value=False), \
             patch.object(fight_api_module.CharacterMacros, "get_enum", return_value=weapon_class):
            view = api.build_fight_view(character, context, "kill")
            definition = api._fight_action_definition(view, "kill")
            plan = api.evaluate_fight_action(view, definition)

        self.assertIs(view.skill, dagger_skill)
        self.assertEqual("multi_hit", definition.executor)
        self.assertEqual("already_fighting", plan.messages[0].key)
        self.assertEqual({"victim_name": "goblin"}, plan.messages[0].tokens)

    def test_backstab_uses_skill_checks_from_data(self):
        backstab_skill = Skill.from_json(
            {
                "_id": {"$oid": "skill-3"},
                "name": "backstab",
                "kind": "skill",
                "handlerId": "skill.none",
                "target": "IGNORE",
                "minPosition": "STANDING",
                "nounDamage": "backstab",
                "msgOff": "!Backstab!",
                "msgObj": "",
                "levelByClass": {"thief": 1},
                "ratingByClass": {"thief": 5},
                "slot": 0,
                "minMana": 0,
                "beats": 24,
                "guards": [
                    {
                        "predicate": "lambda v: not bool(v.extra.get('has_skill_access', False))",
                        "messageKey": "noAccess",
                    },
                    {
                        "predicate": "lambda v: not is_weapon_wielded(v)",
                        "messageKey": "requiresWeapon",
                    },
                ],
                "fightExecutor": "backstab",
                "fightPlan": {"dt": "backstab"},
            }
        )

        api = FightApi(Mock(), Mock(), Mock(), Mock())
        view = FightView(
            actor=SimpleNamespace(),
            command=SimpleNamespace(payload=Mock()),
            room=SimpleNamespace(id="room-1"),
            argument="victim",
            victim=SimpleNamespace(name="target", hit=20, max_hit=30),
            skill=backstab_skill,
            current_fighting=None,
            safe=False,
            safe_message="",
            extra={"command_name": "backstab", "has_skill_access": True, "weapon": None},
        )

        definition = api._fight_action_definition(view, "backstab")
        plan = api.evaluate_fight_action(view, definition)

        self.assertEqual("backstab", definition.executor)
        self.assertEqual("requires_weapon", plan.messages[0].key)


if __name__ == "__main__":
    unittest.main()
