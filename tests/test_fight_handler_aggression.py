import importlib.util
import asyncio
import sys
import types
import unittest
from enum import IntEnum
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock


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
    AFF_CHARM = 2


class _Positions(IntEnum):
    POS_DEAD = 0
    POS_MORTAL = 1
    POS_INCAP = 2
    POS_STUNNED = 3
    POS_STANDING = 8
    POS_RESTING = 6
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
    def is_affected(entity, bit):
        return (int(getattr(getattr(entity, "status_flags", None), "affected_by", 0) or 0) & int(bit or 0)) != 0

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
        if name == "weaponClass":
            return SimpleNamespace(WEAPON_DAGGER=SimpleNamespace(value=1))
        return SimpleNamespace()

    @staticmethod
    def get_attribute_bonus(attr_name, value):
        if attr_name == "strength" and str(value) == "14":
            return {"tohit": 0, "todam": 1}
        return {"tohit": 0, "todam": 0, "defensive": 0}

    @staticmethod
    def is_same_group(left, right):
        if getattr(left, "leader", None) is not None:
            left = left.leader
        if getattr(right, "leader", None) is not None:
            right = right.leader
        return left is right

    @staticmethod
    def player_auto_assist(entity):
        return bool(getattr(entity, "auto_assist", False))


class _MobileApi:
    @staticmethod
    def mobile_is_charmed(_entity):
        return False

    @staticmethod
    def mobile_will_assist(_entity):
        return False


class _RandomNumberGenerator:
    def number_bits(self, _width):
        return 1

    def number_range(self, _start, _end):
        return 0

    def dice(self, _num_dice, _num_sides):
        return 0


class _Character:
    @staticmethod
    def learned_entry_name(entry) -> str:
        return str(entry.get("name", "") or "").strip() if isinstance(entry, dict) else str(getattr(entry, "name", "") or "").strip()

    @staticmethod
    def learned_entry_level(entry) -> int:
        return int(entry.get("level", 0)) if isinstance(entry, dict) else int(getattr(entry, "level", 0))

    @staticmethod
    def get_learned(character, learned_name, *, visible_only: bool = False, collection_name: str = "", **_kwargs):
        wanted = str(learned_name or "").strip().lower()
        collections = [getattr(character, collection_name, [])] if collection_name else [getattr(character, "skills", []), getattr(character, "spells", [])]
        for collection in collections:
            for entry in list(collection or []):
                if visible_only and _Character.learned_entry_level(entry) < 1:
                    continue
                if _Character.learned_entry_name(entry).lower() == wanted:
                    return entry
        return None


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
_stub_package("mobile")
_stub_module("mobile.Mobile", Mobile=type("Mobile", (), {}))
_stub_package("player")
_stub_module("player.Character", Character=_Character)
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


class _SkillUtil:
    @staticmethod
    def practice_visible(_character, _meta_or_name) -> bool:
        return True

    @staticmethod
    def learned_level(*_args, **_kwargs):
        return 0

    @staticmethod
    def find_learned_entry(*_args, **_kwargs):
        return None

    @staticmethod
    def check_improve(*_args, **_kwargs):
        return None

    @staticmethod
    def check_improve_by_name(*_args, **_kwargs):
        return None

    @staticmethod
    def weapon_skill_name(weapon, _weapon_class_names=None):
        if weapon is None:
            return "hand to hand"
        return "dagger" if getattr(weapon, "value0", None) == 1 else ""

    @staticmethod
    def active_melee_skill_name(weapon, weapon_class_names=None):
        return _SkillUtil.weapon_skill_name(weapon, weapon_class_names) or "hand to hand"


_stub_module("util.SkillUtil", SkillUtil=_SkillUtil)
_stub_package("skill")
_stub_module("skill.Ability", Ability=_SkillUtil)

FightHandler = _load_module("fight.FightHandler", "fight/FightHandler.py").FightHandler


class TestFightHandlerAggression(unittest.TestCase):
    def _handler(self, room):
        handler = FightHandler.__new__(FightHandler)
        handler.logger = _Logger()
        handler.area_registry = SimpleNamespace(get_or_none=lambda **_kwargs: None)
        handler.combat_registry = SimpleNamespace(upsert=Mock())
        handler.room_registry = SimpleNamespace(get=lambda **_kwargs: room, get_or_none=lambda **_kwargs: room)
        handler.PositionsEnum = _Positions
        handler.ActBits = _ActBits
        handler.RoomFlags = _RoomFlags
        handler.AffectBits = _AffectBits
        handler.WeaponClass = type("WeaponClass", (), {"__members__": {"WEAPON_DAGGER": "dagger"}})
        handler.WeaponTypes = SimpleNamespace(WEAPON_SHARP=SimpleNamespace(value=1))
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
            room_id="room-1",
            fighting=None,
            status_flags=SimpleNamespace(act=int(_ActBits.ACT_AGGRESSIVE), affected_by=0, off=0),
            character_attributes=SimpleNamespace(position=8),
            leader=None,
            master=None,
        )

    @staticmethod
    def _player(player_id: str):
        return SimpleNamespace(
            id=player_id,
            is_npc=False,
            is_immortal=False,
            level=5,
            room_id="room-1",
            fighting=None,
            status_flags=SimpleNamespace(act=0, affected_by=0, comm=0),
            character_attributes=SimpleNamespace(position=8),
            leader=None,
            master=None,
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

    def test_one_hit_improves_weapon_skill_on_hit(self):
        victim = self._mob("mob-1")
        victim.room_id = "room-1"
        victim.hit = 20
        victim.max_hit = 20
        victim.position = 8
        victim.default_pos = 8
        victim.start_pos = 8
        attacker = self._player("char-1")
        attacker.name = "Tester"
        attacker.room_id = "room-1"
        attacker.equipped = SimpleNamespace(wielded=SimpleNamespace(item_type="weapon", value0=1, value3="stab"))
        room = SimpleNamespace(id="room-1", area_id="area-1", room_flags=0, mobiles={"mob-1": victim}, characters={"char-1": attacker})
        handler = self._handler(room)

        calls = []
        with unittest.mock.patch.object(
            _SkillUtil,
            "check_improve_by_name",
            side_effect=lambda *_args: calls.append(_args[1:]),
        ), unittest.mock.patch.object(handler, "_thac0", return_value=1), \
                unittest.mock.patch.object(handler, "_victim_ac_for_damage_type", return_value=0), \
                unittest.mock.patch.object(handler, "_attack_damage", return_value=7), \
                unittest.mock.patch.object(handler, "_to_hit_roll", return_value=19), \
                unittest.mock.patch.object(handler, "damage", return_value={"to_char": "", "to_victim": "", "to_room": "", "killed": False}):
            handler.one_hit(attacker, victim, dt="TYPE_HIT")

        self.assertEqual([("dagger", True, 5)], calls)

    def test_one_hit_improves_weapon_skill_on_miss(self):
        victim = self._mob("mob-1")
        victim.room_id = "room-1"
        victim.hit = 20
        victim.max_hit = 20
        victim.position = 8
        victim.default_pos = 8
        victim.start_pos = 8
        attacker = self._player("char-1")
        attacker.name = "Tester"
        attacker.room_id = "room-1"
        attacker.equipped = SimpleNamespace(wielded=SimpleNamespace(item_type="weapon", value0=1, value3="stab"))
        room = SimpleNamespace(id="room-1", area_id="area-1", room_flags=0, mobiles={"mob-1": victim}, characters={"char-1": attacker})
        handler = self._handler(room)

        calls = []
        with unittest.mock.patch.object(
            _SkillUtil,
            "check_improve_by_name",
            side_effect=lambda *_args: calls.append(_args[1:]),
        ), unittest.mock.patch.object(handler, "_thac0", return_value=20), \
                unittest.mock.patch.object(handler, "_victim_ac_for_damage_type", return_value=0), \
                unittest.mock.patch.object(handler, "_to_hit_roll", return_value=0), \
                unittest.mock.patch.object(handler, "damage", return_value={"to_char": "", "to_victim": "", "to_room": "", "killed": False}):
            handler.one_hit(attacker, victim, dt="TYPE_HIT")

        self.assertEqual([("dagger", False, 5)], calls)

    def test_update_pos_keeps_npc_alive_when_hit_points_remain(self):
        handler = self._handler(SimpleNamespace())
        victim = self._mob("mob-1")
        victim.hit = 34
        victim.fighting = self._player("char-1")

        handler.update_pos(victim)

        self.assertEqual(8, victim.character_attributes.position)

    def test_update_pos_kills_npc_only_when_zero_or_less_hit_points(self):
        handler = self._handler(SimpleNamespace())
        victim = self._mob("mob-1")
        victim.hit = 0

        handler.update_pos(victim)

        self.assertEqual(_Positions.POS_DEAD, victim.character_attributes.position)

    def test_attack_damage_adds_unscaled_damroll_for_players(self):
        handler = self._handler(SimpleNamespace())
        attacker = self._player("char-1")
        attacker.level = 6
        attacker.character_attributes = SimpleNamespace(position=8, strength=14)
        attacker.equipped = SimpleNamespace(
            wielded=SimpleNamespace(item_type="weapon", value0="sword", value1="1", value2="6", value3="slash", value4="0"),
            shield=SimpleNamespace(),
        )

        with unittest.mock.patch.object(sys.modules["fight.FightHandler"].GameApi, "is_set", return_value=False, create=True), \
                unittest.mock.patch.object(handler.rng, "dice", return_value=2):
            damage = handler._attack_damage(attacker, skill=60)

        self.assertEqual(2, damage)

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

    def test_is_safe_returns_safe_when_room_cannot_be_resolved(self):
        attacker = self._player("char-1")
        victim = self._mob("mob-1")
        handler = self._handler(SimpleNamespace())
        handler._find_room_for_entity = Mock(return_value=None)

        safe, message = handler.is_safe(attacker, victim)

        self.assertTrue(safe)
        self.assertEqual("They aren't here.\r\n", message)

    def test_check_assist_charmed_group_pet_autoattacks_owner_target(self):
        owner = self._player("char-1")
        victim = self._mob("mob-1")
        victim.fighting = owner
        pet = self._mob("pet-1")
        pet.status_flags.affected_by = int(_AffectBits.AFF_CHARM)
        pet.master = owner
        pet.leader = owner
        room = SimpleNamespace(
            id="room-1",
            area_id="area-1",
            room_flags=0,
            mobiles={"mob-1": victim, "pet-1": pet},
            characters={"char-1": owner},
            people=lambda: [owner, victim, pet],
        )
        handler = self._handler(room)
        handler.multi_hit = Mock()

        handler.check_assist(owner, victim)

        handler.multi_hit.assert_called_once_with(pet, victim, dt="TYPE_UNDEFINED")

    def test_check_assist_charmed_group_pet_defends_owner_from_npc_attacker(self):
        owner = self._player("char-1")
        attacker = self._mob("mob-1")
        attacker.fighting = owner
        owner.fighting = attacker
        pet = self._mob("pet-1")
        pet.status_flags.affected_by = int(_AffectBits.AFF_CHARM)
        pet.master = owner
        pet.leader = owner
        room = SimpleNamespace(
            id="room-1",
            area_id="area-1",
            room_flags=0,
            mobiles={"mob-1": attacker, "pet-1": pet},
            characters={"char-1": owner},
            people=lambda: [owner, attacker, pet],
        )
        handler = self._handler(room)
        handler.multi_hit = Mock()

        handler.check_assist(attacker, owner)

        handler.multi_hit.assert_called_once_with(pet, attacker, dt="TYPE_UNDEFINED")

    def test_is_safe_allows_group_member_to_join_existing_fight(self):
        owner = self._player("char-1")
        victim = self._mob("mob-1")
        victim.fighting = owner
        pet = self._mob("pet-1")
        pet.leader = owner
        room = SimpleNamespace(
            id="room-1",
            area_id="area-1",
            room_flags=0,
            mobiles={"mob-1": victim, "pet-1": pet},
            characters={"char-1": owner},
        )
        handler = self._handler(room)

        safe, message = handler.is_safe(pet, victim, room=room)

        self.assertFalse(safe)
        self.assertEqual("", message)

    def test_build_round_payload_uses_room_player_targets_for_observers(self):
        attacker = self._player("char-1")
        victim = self._player("char-2")
        watcher = self._player("char-3")
        room = SimpleNamespace(
            id="room-1",
            characters={"char-1": attacker, "char-2": victim, "char-3": watcher},
            player_targets=lambda character: [ch for ch in [attacker, victim, watcher] if ch.id != character.id],
        )
        handler = self._handler(room)

        payload = handler.build_round_payload(
            attacker,
            victim,
            room,
            {"to_char": "You hit.\r\n", "to_victim": "Tester hits you.\r\n", "to_room": "Tester hits Victim.\r\n"},
        )

        self.assertEqual([watcher], payload["targets"])

    def test_emit_round_payload_returns_room_observers_for_prompt(self):
        attacker = self._player("char-1")
        victim = self._mob("mob-1")
        watcher = self._player("char-2")
        handler = self._handler(SimpleNamespace())
        handler.message_bus = SimpleNamespace(
            text_to_message=lambda text: text,
            send_to_character=AsyncMock(),
            send_to_room=AsyncMock(),
        )

        prompted = asyncio.run(
            handler.emit_round_payload(
                attacker,
                {
                    "to_char": "You hit.\r\n",
                    "to_room": "Tester hits mob.\r\n",
                    "targets": [watcher],
                    "victim": victim,
                },
            )
        )

        self.assertEqual([attacker, watcher], prompted)
        handler.message_bus.send_to_room.assert_awaited_once_with("Tester hits mob.\r\n", [watcher])


if __name__ == "__main__":
    unittest.main()
