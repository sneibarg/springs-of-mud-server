import importlib.util
import sys
import types
import unittest
from enum import IntEnum
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
    assert spec.loader is not None
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


class _ActBits(IntEnum):
    ACT_AGGRESSIVE = 1
    ACT_WIMPY = 2


class _RoomFlags(IntEnum):
    ROOM_SAFE = 1


class _AffectBits(IntEnum):
    AFF_CALM = 1


class _Positions(IntEnum):
    POS_DEAD = 0
    POS_STUNNED = 3
    POS_FIGHTING = 7


class _CharacterApi:
    @staticmethod
    def is_npc(entity):
        return bool(getattr(entity, "is_npc", False))

    @staticmethod
    def is_immortal(entity):
        return bool(getattr(entity, "is_immortal", False))

    @staticmethod
    def is_set(flags, bit):
        return (int(flags) & int(bit)) != 0 if bit else False

    @staticmethod
    def enum_bit(enum_obj, name):
        member = getattr(enum_obj, str(name), None)
        return int(getattr(member, "value", member or 0))

    @staticmethod
    def is_affected(_entity, _bit):
        return False

    @staticmethod
    def is_awake(_entity):
        return True

    @staticmethod
    def can_see(_aggressor, _witness, _room):
        return True

    @staticmethod
    def get_enum(name):
        if name == "actBits":
            return _ActBits
        return SimpleNamespace()


class _MobileApi:
    @staticmethod
    def mobile_is_charmed(_entity):
        return False


class _RandomNumberGenerator:
    def number_bits(self, _width):
        return 1

    def number_range(self, _start, _end):
        return 0


_stub_module("injector", inject=lambda target: target)
_stub_package("api")
_stub_module("api.GameApi", GameApi=SimpleNamespace())
_stub_module("api.ItemApi", ItemApi=SimpleNamespace())
_stub_module("api.CharacterApi", CharacterApi=_CharacterApi)
_stub_module("api.MobileApi", MobileApi=_MobileApi)
_stub_package("fight")
_stub_module("fight.CombatEvent", CombatEvent=object)
_stub_package("game")
_stub_module("game", GameData=object)
_stub_module("game.EnumProvider", EnumProvider=object)
_stub_module("game.RegistryService", RegistryService=object)
_stub_module("game.RandomNumberGenerator", RandomNumberGenerator=_RandomNumberGenerator)
_stub_package("item")
_stub_module("item.EffectHandler", EffectHandler=object)
_stub_module("item.BodyForm", BodyForm=object)
_stub_module("item.BodyParts", BodyParts=object)
_stub_module("item.Item", Item=object)
_stub_package("player")
_stub_module("player.Character", Character=object)
_stub_module("player.CharacterAdvancement", CharacterAdvancement=object)
_stub_package("server")
_stub_module("server.LoggerFactory", LoggerFactory=_LoggerFactory)
_stub_package("server.messaging")
_stub_module("server.messaging.MessageBus", MessageBus=object)
_stub_package("util")
_load_module("util.GenericUtil", "util/GenericUtil.py")
_load_module("util.FightUtil", "util/FightUtil.py")
_stub_module("util.InfoUtil", InfoUtil=SimpleNamespace())
_stub_module("util.ItemUtil", ItemUtil=SimpleNamespace())
_stub_module("util.SkillUtil", SkillUtil=SimpleNamespace(learned_level=lambda *_args, **_kwargs: 0, find_learned_entry=lambda *_args, **_kwargs: None, check_improve=lambda *_args, **_kwargs: None))

FightHandler = _load_module("fight.FightHandler", "fight/FightHandler.py").FightHandler


class TestFightHandlerAggression(unittest.TestCase):
    def _handler(self, room):
        handler = FightHandler.__new__(FightHandler)
        handler.area_registry = SimpleNamespace(get_or_none=lambda **_kwargs: None)
        handler.combat_registry = SimpleNamespace(upsert=Mock())
        handler.PositionsEnum = _Positions
        handler.ActBits = _ActBits
        handler.RoomFlags = _RoomFlags
        handler.AffectBits = _AffectBits
        handler.rng = _RandomNumberGenerator()
        handler.attacks = {
            "none": {"message": "hit", "damage_type": -1},
            "slice": {"message": "slice", "damage_type": "DAM_SLASH"},
            "stab": {"message": "stab", "damage_type": "DAM_PIERCE"},
            "slash": {"message": "slash", "damage_type": "DAM_SLASH"},
            "punch": {"message": "punch", "damage_type": "DAM_BASH"},
        }
        handler._find_room_for_entity = lambda _entity: room
        return handler

    @staticmethod
    def _mob(mob_id: str):
        return SimpleNamespace(
            id=mob_id,
            is_npc=True,
            is_immortal=False,
            level=10,
            fighting=None,
            status_flags=SimpleNamespace(act=int(_ActBits.ACT_AGGRESSIVE), off=0),
            character_attributes=SimpleNamespace(position=8),
        )

    @staticmethod
    def _player(player_id: str):
        return SimpleNamespace(
            id=player_id,
            is_npc=False,
            is_immortal=False,
            level=5,
            fighting=None,
            character_attributes=SimpleNamespace(position=8),
        )

    def test_aggressive_entry_rounds_only_sets_fighting(self):
        victim = self._player("char-1")
        aggressor = self._mob("mob-1")
        room = SimpleNamespace(id="room-1", area_id="area-1", room_flags=0, mobiles={"mob-1": aggressor}, characters={"char-1": victim})
        handler = self._handler(room)
        handler.multi_hit = Mock(side_effect=AssertionError("aggression should not execute a combat round"))

        rounds = handler.aggressive_entry_rounds(victim, room)

        self.assertEqual([], rounds)
        self.assertIs(aggressor.fighting, victim)
        self.assertIs(victim.fighting, aggressor)
        self.assertEqual(2, handler.combat_registry.upsert.call_count)

    def test_aggressive_room_rounds_evaluates_each_aggressor_once(self):
        victim = self._player("char-1")
        witness = self._player("char-2")
        aggressor = self._mob("mob-1")
        room = SimpleNamespace(
            id="room-1",
            area_id="area-1",
            room_flags=0,
            mobiles={"mob-1": aggressor},
            characters={"char-1": victim, "char-2": witness},
        )
        handler = self._handler(room)
        handler.multi_hit = Mock(side_effect=AssertionError("aggression should not execute a combat round"))
        handler._select_aggressive_victim = Mock(return_value=victim)
        handler._should_aggress = Mock(return_value=True)

        rounds = handler.aggressive_room_rounds(room)

        self.assertEqual([], rounds)
        self.assertEqual(1, handler._select_aggressive_victim.call_count)
        self.assertEqual(1, handler._should_aggress.call_count)
        self.assertIs(aggressor.fighting, victim)
        self.assertIs(victim.fighting, aggressor)

    def test_should_aggress_false_when_already_fighting(self):
        victim = self._player("char-1")
        aggressor = self._mob("mob-1")
        aggressor.fighting = victim
        room = SimpleNamespace(id="room-1", area_id="area-1", room_flags=0, mobiles={"mob-1": aggressor}, characters={"char-1": victim})
        handler = self._handler(room)

        self.assertFalse(handler._should_aggress(aggressor, victim, room))

    def test_attack_damage_type_handles_none_attack_entry(self):
        handler = self._handler(SimpleNamespace())
        handler._is_backstab_attack = Mock(return_value=False)
        attacker = SimpleNamespace(dam_type="none")

        damage_type = handler._attack_damage_type(attacker, "TYPE_UNDEFINED", "")

        self.assertEqual("DAM_NONE", damage_type)

    def test_attack_damage_type_defaults_unknown_attack_to_bash(self):
        handler = self._handler(SimpleNamespace())
        handler._is_backstab_attack = Mock(return_value=False)
        attacker = SimpleNamespace(dam_type="foreman_special")

        damage_type = handler._attack_damage_type(attacker, "TYPE_UNDEFINED", "")

        self.assertEqual("DAM_BASH", damage_type)

    def test_attack_verb_resolves_numeric_mobile_dam_type(self):
        handler = self._handler(SimpleNamespace())
        attacker = SimpleNamespace(dam_type="3", equipped=None)

        attack_verb = handler._attack_verb(attacker, "TYPE_UNDEFINED")

        self.assertEqual("slash", attack_verb)

    def test_attack_damage_type_resolves_numeric_mobile_dam_type(self):
        handler = self._handler(SimpleNamespace())
        handler._is_backstab_attack = Mock(return_value=False)
        attacker = SimpleNamespace(dam_type="3")

        damage_type = handler._attack_damage_type(attacker, "TYPE_UNDEFINED", "")

        self.assertEqual("DAM_SLASH", damage_type)


if __name__ == "__main__":
    unittest.main()
