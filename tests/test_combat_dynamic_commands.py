from util.PayloadUtil import PayloadUtil
import json
import os
import sys
import types
import unittest
from copy import deepcopy
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, call


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


def _ensure_injector():
    current = sys.modules.get("injector")
    if current is not None and hasattr(current, "Injector"):
        return
    sys.modules.pop("injector", None)
    try:
        import injector  # noqa: F401
    except ImportError:
        _stub_module("injector", inject=lambda target: target, Injector=object, singleton=lambda target: target)


def _stub_module_if_missing(name: str, **attrs):
    if name not in sys.modules:
        _stub_module(name, **attrs)


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
    def handler():
        return SimpleNamespace()

    @staticmethod
    def affect_to_char(_character, _effect):
        return None

    @staticmethod
    def remove_item_effects(_victim, _obj):
        return None


class _SkillUtil:
    @staticmethod
    def take_improve_messages(_character):
        return ""

    @staticmethod
    def check_improve(_character, _skill_id, _success, _multiplier=1):
        return None

    @staticmethod
    def check_improve_by_name(_character, _skill_name, _success, _multiplier=1):
        return None

    @staticmethod
    def weapon_skill_name(weapon, _weapon_class_names=None):
        if weapon is None:
            return "hand to hand"
        return "dagger" if getattr(weapon, "value0", None) == 1 else ""

    @staticmethod
    def active_melee_skill_name(weapon, weapon_class_names=None):
        return _SkillUtil.weapon_skill_name(weapon, weapon_class_names) or "hand to hand"


class _FightHandler:
    @staticmethod
    def _combat_target_name(target):
        return str(getattr(target, "name", "") or "")


class _StatusFlags(SimpleNamespace):
    pulse_wait: int = 0
    pulse_daze: int = 0


class _Context(SimpleNamespace):
    def __init__(self, **kwargs):
        kwargs.setdefault("result", "")
        kwargs.setdefault("parameters", [])
        super().__init__(**kwargs)

    def finish(self):
        self.done = True


_ensure_injector()
_stub_package("server")
_stub_module("server.LoggerFactory", LoggerFactory=_LoggerFactory)
_stub_package("interp")
_stub_module("interp.Context", Context=_Context)
_stub_package("util")
_load_module("util.GenericUtil", "util/GenericUtil.py")
_load_module("util.FightUtil", "util/FightUtil.py")
_load_module("util.InterpUtil", "util/InterpUtil.py")
_stub_module("util.PlayerUtil", PlayerUtil=_PlayerUtil)
_stub_module("util.MovementUtil", MovementUtil=_MovementUtil)
_stub_module("util.ItemUtil", ItemUtil=SimpleNamespace(find_inventory_item=lambda *_args, **_kwargs: None, find_room_item=lambda *_args, **_kwargs: None, has_flag=lambda *_args, **_kwargs: False))
_stub_module("util.EffectUtil", EffectUtil=_EffectUtil)
_stub_module("util.SkillUtil", SkillUtil=_SkillUtil)
_stub_module("util.CommunicationsUtil", CommunicationsUtil=SimpleNamespace(has_comm=lambda *_args, **_kwargs: False, split_first=lambda text: (text.split(maxsplit=1)[0], text.split(maxsplit=1)[1] if len(text.split(maxsplit=1)) > 1 else "") if text else ("", ""), ensure_message_break=lambda text: text if not text or text.endswith("\r\n") else text + "\r\n"))
_stub_module("util.AreaUtil", AreaUtil=SimpleNamespace())
_stub_package("game")
_load_module("game.GamePayload", "game/GamePayload.py")
_load_module("game.action", "game/action/__init__.py")
_stub_module("game.RegistryService", RegistryService=object)
_stub_module("game.WeatherHandler", WeatherHandler=object)
_stub_package("area")
_stub_module("area.RoomRegistry", RoomRegistry=object)
_load_module("interp.HelpEntry", "interp/HelpEntry.py")
Command = _load_module("interp.Command", "interp/Command.py").Command
_load_module("interp.InterpView", "interp/InterpView.py")
_stub_module("api.CharacterApi", CharacterApi=_CharacterApi)
_stub_module_if_missing("api.MovementApi", MovementApi=SimpleNamespace())
_stub_module("api.ItemApi", ItemApi=SimpleNamespace())
_stub_module("api.SkillApi", SkillApi=object)
_stub_package("player")
_stub_module("player.Character", Character=object)
_stub_package("item")
_stub_module("item.Item", Item=SimpleNamespace)
InterpApi = _load_module("api.InterpApi", "api/InterpApi.py").InterpApi
_stub_package("combat")
_stub_module_if_missing("combat.CombatHandler", FightHandler=_FightHandler)
_stub_module_if_missing("combat.FightHandler", FightHandler=_FightHandler)
_load_module("combat.FightView", "combat/CombatView.py")
_stub_package("skill")
_stub_module("skill.SkillRegistry", SkillRegistry=object)
FightApi = _load_module("api.FightApi", "api/FightApi.py").FightApi
_stub_module("item.Effect", Effect=SimpleNamespace)
_stub_module("player.CharacterAdvancement", CharacterAdvancement=SimpleNamespace(gain_experience=lambda *_args, **_kwargs: None))
Skill = _load_module("skill.Skill", "skill/Skill.py").Skill
sys.modules["skill"].Skill = Skill
_stub_module("skill.SpellContext", SpellContext=lambda **kwargs: SimpleNamespace(payloads=[], performed=False, **kwargs))
_stub_module("api.SpellApi", SpellApi=lambda **_kwargs: SimpleNamespace(execute_lambdas=lambda *_args, **_kwargs: None, queue_cast_announcement=lambda *_args, **_kwargs: None, start_offensive_combat=lambda *_args, **_kwargs: None))
Fight = _load_module("interp.commands.Fight", "interp/commands/Fight.py").Fight
_stub_module_if_missing("interp.commands.Info", Info=object)
_stub_module_if_missing("interp.commands.Movement", Movement=object)
_stub_module_if_missing("interp.commands.Communications", Communications=object)
_stub_module_if_missing("interp.commands.Object", Object=object)
_stub_module_if_missing("interp.commands.Wiz", Wiz=object)
_stub_module_if_missing("server.messaging", MessageBus=object)
PlayerHandler = _load_module("player.PlayerHandler", "player/PlayerHandler.py").PlayerHandler


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
    def test_killer_notices_survive_late_guard_rejection_in_reference_order(self):
        for target_type in ("CHAR_OFFENSIVE", "OBJ_CHAR_OFF"):
            for reason in ("mana", "master"):
                with self.subTest(target_type=target_type, reason=reason):
                    victim = object()
                    actor = SimpleNamespace(name="Hero", level=20, mana=0 if reason == "mana" else 100,
                                            is_npc=False, master=victim if reason == "master" else None,
                                            affects={"AFF_CHARM"} if reason == "master" else set(),
                                            character_class=SimpleNamespace(name="mage"),
                                            get_learned=lambda *args, **kwargs: 100, learned_entry_level=lambda value: value)
                    spell = SimpleNamespace(name="curse", handler_id="spell.curse", target=target_type,
                                            min_position="FIGHTING", min_mana=5, level_by_class={"mage": 1})
                    commands = Fight.__new__(Fight)
                    commands.spell_registry = SimpleNamespace(all_spells=lambda: [spell])
                    commands.interp_api = InterpApi()
                    commands.spell_api = Mock()
                    commands.spell_api.check_offensive_cast.side_effect = lambda ctx: ctx.payloads.append({"to_wiznet": "notice"})
                    commands._resolve_spell_target = Mock(return_value=(victim, "char", ""))
                    ctx = _Context(character=actor, command=_load_command("cast"), room=SimpleNamespace(id="room"), result="curse")
                    result = commands.do_cast(actor, ctx)
                    if target_type == "OBJ_CHAR_OFF" and reason == "master":
                        commands.spell_api.check_offensive_cast.assert_not_called()
                        self.assertEqual("is_follower", result["blocked_key"])
                    else:
                        commands.spell_api.check_offensive_cast.assert_called_once()
                        self.assertEqual({"to_wiznet": "notice"}, result["payloads"][0])
                        self.assertEqual("insufficient_mana" if reason == "mana" else "is_follower",
                                         result["payloads"][1]["blocked_key"])
                    commands.spell_api.cast.assert_not_called()
                    commands.spell_api.start_offensive_combat.assert_not_called()

    def test_mixed_offensive_target_uses_spell_safety_even_for_implicit_opponent(self):
        victim = object()
        actor = SimpleNamespace(fighting=victim, is_npc=False)
        commands = Fight.__new__(Fight)
        commands.fight_handler = Mock()
        commands.fight_handler.is_safe_spell.return_value = True
        room = SimpleNamespace(targets={"target": victim})
        for argument in ("", "target"):
            with self.subTest(argument=argument):
                commands.fight_handler.reset_mock()
                result = commands._resolve_spell_target(actor, room, SimpleNamespace(target="OBJ_CHAR_OFF"), argument)
                self.assertEqual((None, "", "target_safe"), result)
                commands.fight_handler.is_safe_spell.assert_called_once_with(actor, victim, area=False)
                commands.fight_handler.is_safe.assert_not_called()
        actor.is_npc = True
        commands.fight_handler.reset_mock()
        self.assertEqual((victim, "char", ""), commands._resolve_spell_target(
            actor, room, SimpleNamespace(target="CHAR_OFFENSIVE"), "target"))
        commands.fight_handler.is_safe.assert_not_called()

    def test_spell_prefix_lookup_prefers_accessible_spells_in_stable_order(self):
        util = sys.modules["util.FightUtil"].FightUtil
        spells = [SimpleNamespace(name=name, handler_id="spell." + name.replace(" ", "_"),
                                  level_by_class={"mage": required})
                  for name, required in (("cure critical", 12), ("cure disease", 10), ("cure light", 1))]
        actor = SimpleNamespace(level=10, is_npc=False, character_class=SimpleNamespace(name="mage"),
                                get_learned=lambda name, **kwargs: 100,
                                learned_entry_level=lambda entry: entry)
        for ordered in (spells, list(reversed(spells))):
            registry = SimpleNamespace(all_spells=lambda: ordered)
            self.assertIs(spells[1], util.find_spell(registry, "cure", actor))
            self.assertIs(spells[2], util.find_spell(registry, "cure light", actor))
            self.assertIs(spells[2], util.find_spell(registry, "cure_light", actor))
            actor.get_learned = lambda name, **kwargs: 100 if name == "cure light" else 0
            self.assertIs(spells[2], util.find_spell(registry, "cure", actor))
            actor.get_learned = lambda *args, **kwargs: 0
            self.assertIs(spells[0], util.find_spell(registry, "cure", actor))
            actor.is_npc = True
            self.assertIs(spells[0], util.find_spell(registry, "cure", actor))
            actor.is_npc = False
            self.assertIsNone(util.find_spell(registry, "unknown", actor))
            self.assertIsNone(util.find_spell(registry, "", actor))
            self.assertIsNone(util.find_spell(registry, "cure"))
            self.assertIs(spells[2], util.find_spell(registry, "cure light"))
            actor.get_learned = lambda *args, **kwargs: 100

    def test_cast_checks_retaliation_after_no_effect_or_failed_concentration(self):
        spell = SimpleNamespace(name="blindness", handler_id="spell.blindness", min_position="FIGHTING",
                                min_mana=5, level_by_class={"mage": 1}, target="CHAR_OFFENSIVE")
        actor = SimpleNamespace(name="Hero", level=20, mana=100, is_npc=False,
                                character_class=SimpleNamespace(name="mage"),
                                get_learned=lambda *a, **kw: 100, learned_entry_level=lambda entry: entry)
        commands = Fight.__new__(Fight)
        commands.spell_registry = SimpleNamespace(all_spells=lambda: [spell])
        commands.interp_api = InterpApi()
        commands._resolve_spell_target = Mock(return_value=(object(), "char", ""))
        for success in (False, True):
            with self.subTest(concentration_success=success):
                commands.spell_api = Mock()
                def attempt(ctx, cost):
                    ctx.performed = False
                    ctx.payloads = []
                    return success
                commands.spell_api.cast.side_effect = attempt
                ctx = _Context(character=actor, command=_load_command("cast"), room=SimpleNamespace(id="room"), result="blind")
                commands.do_cast(actor, ctx)
                self.assertIs(spell, ctx.cast_spell)
                commands.spell_api.cast.assert_called_once()
                commands.spell_api.start_offensive_combat.assert_called_once()

    def test_charmed_caster_guard_blocks_attacking_master(self):
        for npc in (False, True):
            for target_type in ("CHAR_OFFENSIVE", "OBJ_CHAR_OFF"):
                with self.subTest(npc=npc, target_type=target_type):
                    master = object()
                    actor = SimpleNamespace(name="Follower", level=20, mana=100, is_npc=npc, master=master,
                                            affects={"AFF_CHARM"}, character_class=SimpleNamespace(name="mage"),
                                            get_learned=lambda *a, **kw: 100, learned_entry_level=lambda entry: entry)
                    spell = SimpleNamespace(name="curse", handler_id="spell.curse", target=target_type,
                                            min_position="FIGHTING", min_mana=5, level_by_class={"mage": 1})
                    commands = Fight.__new__(Fight)
                    commands.spell_registry = SimpleNamespace(all_spells=lambda: [spell])
                    commands.interp_api = InterpApi()
                    commands.spell_api = Mock()
                    commands._resolve_spell_target = Mock(return_value=(master, "char", ""))
                    ctx = _Context(character=actor, command=_load_command("cast"), room=SimpleNamespace(id="room"), result="curse")
                    result = commands.do_cast(actor, ctx)
                    self.assertEqual("is_follower", result["blocked_key"])
                    self.assertEqual(100, actor.mana)
                    commands.spell_api.cast.assert_not_called()
                    commands.spell_api.start_offensive_combat.assert_not_called()

    def test_cast_mana_cost_uses_class_level_and_integer_division(self):
        util = sys.modules["util.FightUtil"].FightUtil
        spell = SimpleNamespace(min_mana=15, level_by_class={"mage": 10, "warrior": 20})
        for level, class_name, expected in [(10, "mage", 50), (11, "mage", 33),
                                            (20, "mage", 15), (20, "warrior", 50),
                                            (18, "warrior", 50), (1, "mage", 15)]:
            with self.subTest(level=level, class_name=class_name):
                actor = SimpleNamespace(level=level, character_class=SimpleNamespace(name=class_name))
                self.assertEqual(expected, util.cast_mana_cost(actor, spell))

    def test_cast_position_target_and_mana_guards_do_not_start_attempt(self):
        for minimum, position, mana, target_error, expected in [
            ("STANDING", "POS_FIGHTING", 100, "", "minimum_position"),
            ("POS_STANDING", "POS_FIGHTING", 0, "", "minimum_position"),
            ("FIGHTING", "POS_FIGHTING", 0, "no_target", "no_target"),
            ("FIGHTING", "POS_FIGHTING", 49, "", "insufficient_mana"),
        ]:
            with self.subTest(minimum=minimum, mana=mana, target_error=target_error):
                actor = SimpleNamespace(name="Hero", level=10, mana=mana, is_npc=False,
                                        position=_CharacterApi.pos_value(position),
                                        character_class=SimpleNamespace(name="mage"),
                                        get_learned=Mock(return_value=100),
                                        learned_entry_level=Mock(return_value=100))
                spell = SimpleNamespace(name="armor", handler_id="spell.armor", min_position=minimum, target="CHAR_SELF",
                                        min_mana=5, level_by_class={"mage": 10})
                commands = Fight.__new__(Fight)
                commands.spell_registry = SimpleNamespace(all_spells=lambda: [spell])
                commands.interp_api = InterpApi()
                commands.spell_api = Mock()
                commands._resolve_spell_target = Mock(return_value=(actor, "char", target_error))
                context = _Context(character=actor, command=_load_command("cast"),
                                   room=SimpleNamespace(id="room-1"), result="armor", done=False)
                result = commands.do_cast(actor, context)
                self.assertEqual(expected, result["blocked_key"])
                commands.spell_api.cast.assert_not_called()
                self.assertEqual(mana, actor.mana)
                commands._resolve_spell_target.assert_called_once()

    def test_cast_access_guards_block_before_execution_and_mana_charge(self):
        # ROM magic.c do_cast rejects unlearned/under-level PCs, but exempts NPCs.
        cases = [
            ("missing learned spell", 10, "mage", None, False, 20, True),
            ("zero proficiency", 10, "mage", 0, False, 20, True),
            ("under class level", 9, "mage", 100, False, 20, True),
            ("access precedes mana", 9, "mage", 100, False, 0, True),
            ("at class level", 10, "mage", 1, False, 100, False),
            ("above class level", 11, "mage", 100, False, 100, False),
            ("different class requirement", 10, "warrior", 100, False, 20, True),
            ("NPC exemption", 1, "mage", None, True, 0, False),
        ]
        for label, level, class_name, learned, npc, mana, blocked in cases:
            with self.subTest(label=label):
                spell = SimpleNamespace(name="armor", handler_id="spell.armor",
                                        target="CHAR_SELF", min_mana=5, min_position="STANDING",
                                        level_by_class={"mage": 10, "warrior": 20})
                room = SimpleNamespace(id="room-1")
                character = SimpleNamespace(
                    name="Hero", level=level, mana=mana, is_npc=npc,
                    character_class=SimpleNamespace(name=class_name),
                    get_learned=Mock(return_value=learned),
                    learned_entry_level=Mock(return_value=learned or 0),
                )
                commands = Fight.__new__(Fight)
                commands.spell_registry = SimpleNamespace(all_spells=lambda: [spell])
                commands.interp_api = InterpApi()
                commands.spell_api = Mock()

                def perform(ctx, cost):
                    ctx.performed = True
                    ctx.payloads = []
                    ctx.actor.mana -= cost

                commands.spell_api.cast.side_effect = perform
                context = _Context(character=character, command=_load_command("cast"),
                                   room=room, result="armor", done=False)
                payload = commands.do_cast(character, context)

                self.assertTrue(context.done)
                if blocked:
                    self.assertEqual("spell_not_learned", payload["blocked_key"])
                    self.assertEqual("You don't know any spells of that name.\r\n", payload["to_char"])
                    self.assertEqual(mana, character.mana)
                    commands.spell_api.cast.assert_not_called()
                    commands.spell_api.execute_lambdas.assert_not_called()
                    commands.spell_api.queue_cast_announcement.assert_not_called()
                    commands.spell_api.start_offensive_combat.assert_not_called()
                else:
                    self.assertEqual(mana - sys.modules["util.FightUtil"].FightUtil.cast_mana_cost(character, spell), character.mana)
                    commands.spell_api.cast.assert_called_once()
                if npc or level < spell.level_by_class[class_name]:
                    character.get_learned.assert_not_called()
                else:
                    character.get_learned.assert_has_calls([call("armor", collection_name="spells")] * 2)

    def test_migrated_fight_metadata_has_check_lists(self):
        command_names = {"cast", "flee", "murder"}
        skill_names = {"bash", "berserk", "dirt kicking", "disarm", "kick", "rescue", "trip"}

        with open(COMMANDS_PATH, "r", encoding="utf-8") as handle:
            commands = {entry["name"]: entry for entry in json.load(handle)}
        with open(SKILLS_PATH, "r", encoding="utf-8") as handle:
            skills = {entry["name"]: entry for entry in json.load(handle)}

        for name in command_names:
            self.assertTrue(commands[name].get("guards"), name)
        for name in skill_names:
            self.assertTrue(skills[name].get("guards"), name)

    def test_defensive_skills_define_success_payloads(self):
        with open(SKILLS_PATH, "r", encoding="utf-8") as handle:
            skills = {entry["name"]: entry for entry in json.load(handle)}

        expected = {
            "dodge": ("{t} dodges your attack.", "You dodge {c}'s attack."),
            "parry": ("{t} parries your attack.", "You parry {c}'s attack."),
            "shield block": ("{t} blocks your attack with a shield.", "You block {c}'s attack with your shield."),
        }
        for skill_name, (to_char, to_victim) in expected.items():
            payload = skills[skill_name]["payload"]
            self.assertEqual(to_char, payload["toChar"]["success"])
            self.assertEqual(to_victim, payload["toVictim"]["success"])

    def test_do_flee_uses_command_check_and_stands_when_not_fighting(self):
        room = SimpleNamespace(id="room-1", exits=[], player_targets=lambda _character: [])
        registry_service = SimpleNamespace(
            room_registry=SimpleNamespace(get=lambda **_kwargs: room, get_or_none=lambda **_kwargs: room),
            skill_registry=_SkillRegistry({}),
            spell_registry=SimpleNamespace(all_spells=lambda: []),
        )
        fight_handler = Mock()
        fight_api = FightApi(registry_service.room_registry, registry_service.skill_registry, Mock(), fight_handler)
        commands = Fight(registry_service, Mock(), Mock(), fight_api, InterpApi(), Mock(), Mock(), Mock())

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
        commands = Fight(registry_service, Mock(), skill_api, fight_api, InterpApi(), Mock(), Mock(), Mock())

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
            equipped=None,
        )
        room.targets["hero"] = character
        context = _Context(character=character, command=_load_command("trip"), room=room, result="hero", parameters=[], done=False)

        payload = commands.do_trip(character, context)

        self.assertTrue(payload["blocked"])
        self.assertEqual("target_self", payload["blocked_key"])
        self.assertEqual("You fall flat on your face!\r\n", payload["to_char"])
        self.assertEqual("self_room", payload["payloads"][1]["message_key"])
        self.assertEqual("to_room", payload["payloads"][1]["channel"])
        self.assertEqual(48, character.status_flags.pulse_wait)

    def test_resolve_char_offensive_spell_allows_target_fighting_other_player(self):
        owner = SimpleNamespace(id="char-2", name="Owner", room_id="room-1", is_npc=False)
        victim = SimpleNamespace(id="mob-1", name="Goblin", room_id="room-1", is_npc=True, fighting=owner)
        room = SimpleNamespace(id="room-1", targets={"goblin": victim})
        registry_service = SimpleNamespace(
            room_registry=SimpleNamespace(get=lambda **_kwargs: room, get_or_none=lambda **_kwargs: room),
            skill_registry=_SkillRegistry({}),
            spell_registry=SimpleNamespace(all_spells=lambda: []),
        )
        fight_handler = Mock()
        fight_handler.is_safe.return_value = (False, "")
        fight_api = SimpleNamespace(fight_handler=fight_handler)
        enum_provider = SimpleNamespace(get=lambda _name: SimpleNamespace())
        commands = Fight(registry_service, enum_provider, Mock(), fight_api, InterpApi(), Mock(), Mock(), Mock())
        character = SimpleNamespace(id="char-1", name="Hero", room_id="room-1", is_npc=False, fighting=None)
        spell = SimpleNamespace(target="CHAR_OFFENSIVE")

        target, target_kind, target_error = commands._resolve_spell_target(character, room, spell, "goblin")

        self.assertIs(target, victim)
        self.assertEqual("char", target_kind)
        self.assertEqual("", target_error)
        fight_handler.is_safe.assert_called_once_with(character, victim, room=room, ignore_target_fighting=True)


class TestFightPayloadEmission(unittest.IsolatedAsyncioTestCase):
    async def test_emit_standard_payload_without_victim_skips_to_victim_render(self):
        delivered = []

        async def send_to_character(character_id, message):
            delivered.append((character_id, message))

        handler = PlayerHandler.__new__(PlayerHandler)
        handler.message_bus = SimpleNamespace(
            text_to_message=lambda text: text,
            send_to_character=send_to_character,
            send_to_room=AsyncMock(),
            broadcast=AsyncMock(),
            connection_manager=SimpleNamespace(get_connection=lambda *_args, **_kwargs: None),
        )
        handler.wiz_handler = SimpleNamespace(
            wiznet_targets=lambda *_args, **_kwargs: [],
            current_session=lambda *_args, **_kwargs: None,
        )
        handler.fight_handler = SimpleNamespace(emit_round_payload=AsyncMock())
        handler._show_room_to_character = AsyncMock()
        handler.interp_api = InterpApi()

        character = SimpleNamespace(id="char-1", name="Hero")
        context = _Context(character=character, command=_load_command("restore"), done=False)

        await handler._emit_standard_payload(character, {"message_key": "default", "tokens": {"t": "Hero"}}, context=context)

        self.assertEqual([("char-1", "Ok.\r\n")], delivered)

    async def test_emit_standard_payload_uses_interp_api_default_tokens(self):
        delivered = []

        async def send_to_character(character_id, message):
            delivered.append((character_id, message))

        handler = PlayerHandler.__new__(PlayerHandler)
        handler.message_bus = SimpleNamespace(
            text_to_message=lambda text: text,
            send_to_character=send_to_character,
            send_to_room=AsyncMock(),
            broadcast=AsyncMock(),
            connection_manager=SimpleNamespace(get_connection=lambda *_args, **_kwargs: None),
        )
        handler.wiz_handler = SimpleNamespace(
            wiznet_targets=lambda *_args, **_kwargs: [],
            current_session=lambda *_args, **_kwargs: None,
        )
        handler.fight_handler = SimpleNamespace(emit_round_payload=AsyncMock())
        handler._show_room_to_character = AsyncMock()
        handler.interp_api = InterpApi()

        character = SimpleNamespace(id="char-1", name="Hero")
        context = _Context(character=character, command=_load_command("restore"), done=False)

        await handler._emit_standard_payload(character, {"message_key": "default", "victim": character}, context=context)

        self.assertIn(("char-1", "Ok.\r\n"), delivered)
        self.assertIn(("char-1", "Hero has restored you.\r\n"), delivered)

    async def test_emit_standard_payloads_renders_command_message_keys(self):
        delivered = []

        async def send_to_character(character_id, message):
            delivered.append(("char", character_id, message))

        async def send_to_room(message, targets):
            delivered.append(("room", [target.id for target in targets], message))

        handler = PlayerHandler.__new__(PlayerHandler)
        handler.message_bus = SimpleNamespace(
            text_to_message=lambda text: text,
            send_to_character=send_to_character,
            send_to_room=send_to_room,
        )
        handler.interp_api = InterpApi()
        handler.fight_handler = SimpleNamespace(emit_round_payload=AsyncMock())
        handler._show_room_to_character = AsyncMock()

        character = SimpleNamespace(id="char-1", name="Hero")
        victim = SimpleNamespace(id="char-2", name="Rogue")
        watcher = SimpleNamespace(id="char-3")
        context = _Context(character=character, command=_load_command("rescue"), done=False)

        await handler._emit_standard_payloads(
            character,
            [PayloadUtil.command_payload("success", victim=victim, targets=[watcher], token_factory=Fight._actor_victim_tokens)],
            context=context,
        )

        self.assertIn(("char", "char-1", "You rescue Rogue!\r\n"), delivered)
        self.assertIn(("char", "char-2", "Hero rescues you!\r\n"), delivered)
        self.assertIn(("room", ["char-3"], "Hero rescues Rogue!\r\n"), delivered)


if __name__ == "__main__":
    unittest.main()
