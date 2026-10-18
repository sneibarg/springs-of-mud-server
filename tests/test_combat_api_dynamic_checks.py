import sys
import types
import importlib.util
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


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

    def debug(self, *_args, **_kwargs):
        return None

    def error(self, *_args, **_kwargs):
        return None


class _LoggerFactory:
    @staticmethod
    def get_logger(_name):
        return _Logger()


class _CharacterApi:
    @staticmethod
    def is_npc(_entity):
        return False

    @staticmethod
    def is_awake(_entity):
        return True

    @staticmethod
    def get_enum(_name):
        return SimpleNamespace(WEAPON_DAGGER=SimpleNamespace(value=1))

    @staticmethod
    def is_affected_by_name(_entity, _bits, _name):
        return False

    @staticmethod
    def position_value(entity):
        return int(getattr(entity, "position", 8))

    @staticmethod
    def pos_value(name: str):
        return 7 if name == "POS_FIGHTING" else 0


class _SkillUtil:
    @staticmethod
    def weapon_skill_name(weapon, _weapon_class_names=None):
        if weapon is None:
            return "hand to hand"
        return "dagger" if getattr(weapon, "value0", None) == 1 else ""

    @staticmethod
    def active_melee_skill_name(weapon, weapon_class_names=None):
        return _SkillUtil.weapon_skill_name(weapon, weapon_class_names) or "hand to hand"


_stub_module("injector", inject=lambda target: target)
_stub_package("server")
_stub_module("server.LoggerFactory", LoggerFactory=_LoggerFactory)
_stub_package("util")
_load_module("util.GenericUtil", "util/GenericUtil.py")
_load_module("util.FightUtil", "util/FightUtil.py")
_stub_module("util.PlayerUtil", PlayerUtil=SimpleNamespace(get_target=lambda *_args, **_kwargs: None))
_stub_module("util.SkillUtil", SkillUtil=_SkillUtil)
_stub_package("game")
_load_module("game.GamePayload", "game/GamePayload.py")
_load_module("game.action", "game/action/__init__.py")
_stub_package("area")
_stub_module("area.RoomRegistry", RoomRegistry=object)
_stub_package("combat")
_stub_module("combat.FightHandler", FightHandler=object)
_stub_package("interp")
_stub_module("interp.Context", Context=object)
FightView = _load_module("combat.FightView", "combat/CombatView.py").FightView
_stub_package("skill")
_stub_module("skill.SkillRegistry", SkillRegistry=object)
_stub_module("api.SkillApi", SkillApi=object)
_stub_package("player")
_stub_module("api.CharacterApi", CharacterApi=_CharacterApi)
Skill = _load_module("skill.Skill", "skill/Skill.py").Skill
FightApi = _load_module("api.FightApi", "api/FightApi.py").FightApi


class TestFightApiDynamicChecks(unittest.TestCase):
    def test_build_view_exposes_legacy_fight_check_fields(self):
        skill = Skill.from_json(
            {
                "_id": {"$oid": "skill-dagger"},
                "name": "dagger",
                "kind": "skill",
                "handlerId": "skill.none",
                "target": "IGNORE",
                "minPosition": "FIGHTING",
                "nounDamage": "",
                "msgOff": "",
                "msgObj": "",
                "levelByClass": {"warrior": 1},
                "ratingByClass": {"warrior": 2},
                "slot": 0,
                "minMana": 0,
                "beats": 0,
                "guards": [
                    {"predicate": "lambda v: not v.argument", "messageKey": "noArgument"},
                    {"predicate": "lambda v: v.current_fighting is not None and v.current_fighting is v.victim", "messageKey": "alreadyFighting"},
                ],
                "fightExecutor": "multi_hit",
                "fightPlan": {"dt": "TYPE_UNDEFINED"},
            }
        )

        room = SimpleNamespace(id="room-1", player_targets=lambda _character: [])
        room_registry = Mock()
        room_registry.get_or_none.return_value = room
        skill_registry = Mock()
        skill_registry.get_or_none.return_value = skill
        skill_api = Mock()
        skill_api.get_rating.return_value = 75
        fight_handler = Mock()
        fight_handler.is_safe.return_value = (False, "")
        fight_handler.WeaponClass = type(
            "WeaponClass",
            (),
            {
                "__members__": {"WEAPON_DAGGER": "dagger"},
                "__contains__": classmethod(lambda cls, value: value in cls.__members__),
                "__getitem__": classmethod(lambda cls, value: cls.__members__[value]),
            },
        )

        victim = SimpleNamespace(id="mob-1", name="goblin")
        actor = SimpleNamespace(
            name="Tester",
            room_id="room-1",
            fighting=victim,
            level=10,
            character_class=SimpleNamespace(name="warrior"),
            equipped=SimpleNamespace(wielded=SimpleNamespace(item_type="weapon", value0=1)),
        )
        context = SimpleNamespace(
            character=actor,
            command=SimpleNamespace(name="kill", payload=SimpleNamespace(render=lambda channel, key, fallback="", **_tokens: key)),
            room=room,
            result="goblin",
            parameters=[],
            finish=lambda: None,
        )

        api = FightApi(room_registry, skill_registry, skill_api, fight_handler)
        original_target = sys.modules["api.FightApi"].PlayerUtil.get_target
        sys.modules["api.FightApi"].PlayerUtil.get_target = lambda *_args, **_kwargs: victim
        try:
            view = api.build_fight_view(context)
            definition = api._fight_action_definition(view, "kill", require_executor=False)
        finally:
            sys.modules["api.FightApi"].PlayerUtil.get_target = original_target

        self.assertEqual("goblin", view.argument)
        self.assertIs(view.room, room)
        self.assertIs(view.current_fighting, victim)

    def test_blocked_check_renders_command_payload_key(self):
        skill = Skill.from_json(
            {
                "_id": {"$oid": "skill-backstab"},
                "name": "backstab",
                "kind": "skill",
                "handlerId": "skill.none",
                "target": "IGNORE",
                "minPosition": "STANDING",
                "nounDamage": "backstab",
                "msgOff": "",
                "msgObj": "",
                "levelByClass": {"thief": 1},
                "ratingByClass": {"thief": 5},
                "slot": 0,
                "minMana": 0,
                "beats": 24,
                "guards": [
                    {"predicate": "lambda v: v.victim is v.actor", "messageKey": "targetSelf"},
                ],
                "fightExecutor": "backstab",
                "fightPlan": {"dt": "backstab"},
            }
        )

        payload = SimpleNamespace(render=lambda channel, key, fallback="", **_tokens: "How can you sneak up on yourself?" if (channel, key) == ("to_char", "target_self") else fallback)
        actor = SimpleNamespace(name="Tester", fighting=None)
        context = SimpleNamespace(character=actor, command=SimpleNamespace(name="backstab", payload=payload), finish=lambda: None)
        view = FightView(
            context=context,
            payload=payload,
            victim=actor,
            skill=skill,
            spell=None,
            extra={"command_name": "backstab"},
        )

        api = FightApi(Mock(), Mock(), Mock(), Mock())
        rendered = api.evaluate_guards_only_view(view)

        self.assertEqual("How can you sneak up on yourself?\r\n", rendered["to_char"])


if __name__ == "__main__":
    unittest.main()
