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

from tests.test_character_api_immortal import CharacterApi as RealCharacterApi


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


class _PlayerActBits(IntEnum):
    PLR_KILLER = 1
    PLR_THIEF = 2


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
    # Use the real membership helper with this module's isolated API stubs.
    is_clan = staticmethod(RealCharacterApi.is_clan)
    GameParameters = RealCharacterApi.GameParameters

    @staticmethod
    def set_act_flags(entity, bit):
        entity.status_flags.act |= int(bit)

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
        if left is None or right is None:
            return False
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
_stub_package("combat")
_stub_module("combat.CombatEvent", CombatEvent=object)
_stub_package("game")
_stub_module("game", GameData=object, __path__=[str(SRC / "game")])
_stub_module("game.EnumProvider", EnumProvider=object)
_stub_module("game.RegistryService", RegistryService=object)
_stub_module("game.WizHandler", WizHandler=object)
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
_stub_module("player.CharacterService", CharacterService=object)
_stub_package("server")
_stub_module("server.LoggerFactory", LoggerFactory=_LoggerFactory)
_stub_package("server.messaging")
_stub_module("server.messaging.MessageBus", MessageBus=object)
_stub_package("util")
_stub_module("util.InterpUtil", InterpUtil=SimpleNamespace())
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

FightHandler = _load_module("combat.FightHandler", "combat/CombatHandler.py").FightHandler


class TestFightHandlerAggression(unittest.TestCase):
    def test_one_hit_weapon_effects_require_damage_and_continued_combat(self):
        for roll, applied, fighting, expected in ((0, 10, True, False), (19, 0, True, False),
                                                  (19, 10, False, False), (19, 10, True, True)):
            with self.subTest(roll=roll, applied=applied, fighting=fighting):
                attacker, victim, handler = self._killer_pair()
                attacker.equipped = SimpleNamespace(wielded=SimpleNamespace(
                    name="blade", item_type="weapon", value0=1, value3="stab"))
                room = self._safety_room(attacker, victim)
                room.id = "room-1"
                handler.room_registry.get = Mock(return_value=room)
                handler._thac0 = Mock(return_value=0)
                handler._victim_ac_for_damage_type = Mock(return_value=0)
                handler._to_hit_roll = Mock(return_value=roll)
                handler._attack_damage = Mock(return_value=10)
                attacker.fighting = victim if fighting else None
                handler.damage = Mock(return_value={"to_char": "hit", "damage_applied": applied,
                                                    "xp_gain": 0, "killed": not fighting})
                handler.weapon_hit_handler = SimpleNamespace(apply=Mock(return_value={
                    "to_char": "proc", "xp_gain": 3, "killed": True, "level_up_messages": "level"}))
                result = handler.one_hit(attacker, victim)
                self.assertEqual(expected, handler.weapon_hit_handler.apply.called)
                if expected:
                    self.assertEqual("hitproc", result["to_char"])
                    self.assertEqual(3, result["xp_gain"])
                    self.assertEqual("level", result["level_up_messages"])
                    self.assertTrue(result["killed"])

    def _killer_pair(self):
        attacker, victim = self._player("attacker"), self._player("victim")
        attacker.name, victim.name = "Attacker", "Victim"
        return attacker, victim, self._handler(self._safety_room(attacker, victim))

    def _charm(self, entity, master=None):
        entity.status_flags.affected_by = int(_AffectBits.AFF_CHARM)
        entity.master = master
        def set_affected(_bits, _name, enabled):
            if not enabled:
                entity.status_flags.affected_by &= ~int(_AffectBits.AFF_CHARM)
        entity.set_affected = set_affected

    def test_check_killer_marks_saves_and_returns_notices_once(self):
        attacker, victim, handler = self._killer_pair()
        attacker.status_flags.act = 8
        def save(character):
            self.assertIs(character, attacker)
            self.assertTrue(character.status_flags.act & int(_PlayerActBits.PLR_KILLER))
            self.assertIsNone(character.fighting)
            return True
        handler.character_service.save_character.side_effect = save
        payload = handler.check_killer(attacker, victim)
        self.assertEqual(9, attacker.status_flags.act)
        self.assertEqual("*** You are now a KILLER!! ***\r\n", payload["to_char"])
        self.assertEqual("Attacker is attempting to murder Victim", payload["to_wiznet"])
        self.assertEqual("WIZ_FLAGS", payload["wiznet_flag"])
        self.assertIs(attacker, payload["wiznet_actor"])
        self.assertEqual({}, handler.check_killer(attacker, victim))
        handler.character_service.save_character.assert_called_once_with(attacker)

    def test_check_killer_exemptions_do_not_mark_or_save(self):
        for case in ("npc_victim", "killer_victim", "thief_victim", "npc_attacker", "self",
                     "immortal", "unclanned", "already_killer", "already_fighting"):
            with self.subTest(case=case):
                attacker, victim, handler = self._killer_pair()
                if case == "npc_victim":
                    victim = self._mob("victim")
                elif case == "killer_victim":
                    victim.status_flags.act = int(_PlayerActBits.PLR_KILLER)
                elif case == "thief_victim":
                    victim.status_flags.act = int(_PlayerActBits.PLR_THIEF)
                elif case == "npc_attacker":
                    attacker = self._mob("attacker")
                elif case == "self":
                    victim = attacker
                elif case == "immortal":
                    attacker.level = _CharacterApi.GameParameters.LEVEL_IMMORTAL.value
                elif case == "unclanned":
                    attacker.guild = ""
                elif case == "already_killer":
                    attacker.status_flags.act = int(_PlayerActBits.PLR_KILLER)
                else:
                    attacker.fighting = victim
                before = attacker.status_flags.act
                self.assertEqual({}, handler.check_killer(attacker, victim))
                self.assertEqual(before, attacker.status_flags.act)
                handler.character_service.save_character.assert_not_called()

    def test_check_killer_follows_nested_charm_owner_and_owner_flags(self):
        for owner_flags in (0, _PlayerActBits.PLR_KILLER, _PlayerActBits.PLR_THIEF):
            with self.subTest(flags=owner_flags):
                attacker, owner, handler = self._killer_pair()
                first, second = self._mob("first"), self._mob("second")
                self._charm(first, second)
                self._charm(second, owner)
                owner.status_flags.act = int(owner_flags)
                payload = handler.check_killer(attacker, first)
                self.assertEqual(not bool(owner_flags), bool(payload))
                if payload:
                    self.assertIn("Victim", payload["to_wiznet"])
                    handler.character_service.save_character.assert_called_once_with(attacker)
                else:
                    handler.character_service.save_character.assert_not_called()

    def test_check_killer_breaks_charmed_attacker_follower_and_pet_links(self):
        attacker, victim, handler = self._killer_pair()
        master = self._player("master")
        master.name = "Master"
        master.pet = attacker
        attacker.leader = master
        self._charm(attacker, master)
        payload = handler.check_killer(attacker, victim)
        self.assertIsNone(attacker.master)
        self.assertIsNone(attacker.leader)
        self.assertIsNone(master.pet)
        self.assertFalse(attacker.status_flags.affected_by & int(_AffectBits.AFF_CHARM))
        handler.effect_handler.affect_strip.assert_called_once_with(attacker, "spell.charm_person")
        self.assertEqual("You stop following Master.\r\n", payload["to_char"])
        self.assertEqual("Attacker stops following you.\r\n", payload["global_message"])
        self.assertEqual([master], payload["global_targets"])
        self.assertEqual(0, master.status_flags.act)
        handler.character_service.save_character.assert_not_called()

    def test_check_killer_repairs_orphaned_charm_without_marking(self):
        attacker, victim, handler = self._killer_pair()
        handler.logger = Mock()
        self._charm(attacker)
        self.assertEqual({}, handler.check_killer(attacker, victim))
        self.assertEqual(0, attacker.status_flags.affected_by)
        handler.effect_handler.affect_strip.assert_called_once_with(attacker, "spell.charm_person")
        handler.logger.error.assert_called_once()
        handler.character_service.save_character.assert_not_called()

    def test_check_killer_exempt_victim_does_not_break_attacker_charm(self):
        attacker, victim, handler = self._killer_pair()
        master = self._player("master")
        self._charm(attacker, master)
        victim.status_flags.act = int(_PlayerActBits.PLR_KILLER)
        self.assertEqual({}, handler.check_killer(attacker, victim))
        self.assertIs(attacker.master, master)
        handler.effect_handler.affect_strip.assert_not_called()

    def test_damage_marks_on_zero_damage_and_preserves_wiznet_in_round_payload(self):
        attacker, victim, handler = self._killer_pair()
        victim.hit = 20
        handler._apply_damage = Mock(return_value={"to_char": "Miss.\r\n", "killed": False,
                                                   "xp_gain": 0, "level_up_messages": ""})
        result = handler.damage(attacker, victim, 0)
        self.assertEqual("*** You are now a KILLER!! ***\r\nMiss.\r\n", result["to_char"])
        room = self._safety_room(attacker, victim)
        room.player_targets = lambda _actor: []
        payload = handler.build_round_payload(attacker, victim, room, result)
        self.assertEqual(result["to_wiznet"], payload["to_wiznet"])
        handler.character_service.save_character.assert_called_once_with(attacker)

    def test_round_emitter_routes_wiznet_through_existing_handler(self):
        attacker, victim, handler = self._killer_pair()
        watcher = self._player("watcher")
        payload = handler.check_killer(attacker, victim)
        handler.wiz_handler.wiznet_targets.return_value = [watcher]
        handler.wiz_handler.decorate_wiznet_text = Mock(return_value="Wiznet notice")
        handler.message_bus = SimpleNamespace(text_to_message=lambda text: text,
                                              send_to_character=AsyncMock(), send_to_room=AsyncMock())
        asyncio.run(handler.emit_round_payload(attacker, payload))
        handler.wiz_handler.wiznet_targets.assert_called_once_with(attacker, flag_name="WIZ_FLAGS")
        handler.message_bus.send_to_character.assert_any_await(watcher.id, "Wiznet notice")

    @staticmethod
    def _spell_api_class():
        # Load the real area-spell caller with only unrelated dependencies stubbed.
        replacements = {
            "api.InterpApi": SimpleNamespace(InterpApi=object),
            "item.Effect": SimpleNamespace(Effect=object),
            "util.EffectUtil": SimpleNamespace(EffectUtil=object),
            "util.PlayerUtil": SimpleNamespace(PlayerUtil=object),
            "skill.SpellContext": SimpleNamespace(SpellContext=object),
            "skill.SpellSpeech": SimpleNamespace(SpellSpeech=object),
        }
        with unittest.mock.patch.dict(sys.modules, replacements):
            spec = importlib.util.spec_from_file_location("_test_area_spell_api", SRC / "api/SpellApi.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        return module.SpellApi

    def test_spell_damage_preserves_killer_and_follower_notice_channels(self):
        SpellApi = self._spell_api_class()
        spell_api = SpellApi(effect_handler=Mock(), interp_api=Mock())
        spell_api.send = Mock()
        ctx = SimpleNamespace(queue_payload=Mock())
        victim = self._player("victim")
        notice = {"to_wiznet": "alert", "wiznet_flag": "WIZ_FLAGS", "global_message": "stopped",
                  "global_targets": [victim]}
        spell_api._queue_damage_payload(ctx, {"to_char": "killer", **notice}, victim)
        spell_api.send.assert_called_once_with(ctx, to_char="killer", to_room="", to_victim="", victim=victim)
        ctx.queue_payload.assert_called_once_with(notice)

    def test_offensive_spell_without_damage_checks_killer_before_starting_combat(self):
        SpellApi = self._spell_api_class()
        attacker, victim, handler = self._killer_pair()
        room = self._safety_room(attacker, victim)
        room.id = "room-1"
        ctx = SimpleNamespace(actor=attacker, victim=victim, room=room, queue_payload=Mock(),
                              spell=SimpleNamespace(target="CHAR_OFFENSIVE"))
        spell_api = SpellApi(effect_handler=Mock(), interp_api=Mock())
        spell_api._fight_handler = Mock(return_value=handler)
        spell_api.start_offensive_combat(ctx)
        self.assertTrue(attacker.status_flags.act & int(_PlayerActBits.PLR_KILLER))
        handler.character_service.save_character.assert_called_once_with(attacker)
        self.assertIs(attacker.fighting, victim)
        self.assertEqual("WIZ_FLAGS", ctx.queue_payload.call_args.args[0]["wiznet_flag"])

    def test_melee_executor_checks_killer_before_preparing_fight(self):
        replacements = {
            "area.RoomRegistry": SimpleNamespace(RoomRegistry=object),
            "combat.CombatHandler": SimpleNamespace(FightHandler=FightHandler),
            "combat.CombatView": SimpleNamespace(FightView=object),
            "game.action": SimpleNamespace(ActionGuard=object, ActionDefinition=object, ActionPlan=object, MessageRef=object),
            "api.SkillApi": SimpleNamespace(SkillApi=object),
            "skill.SkillRegistry": SimpleNamespace(SkillRegistry=object),
            "util.PlayerUtil": SimpleNamespace(PlayerUtil=object),
        }
        with unittest.mock.patch.dict(sys.modules, replacements):
            spec = importlib.util.spec_from_file_location("_test_killer_fight_api", SRC / "api/FightApi.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        attacker, victim, handler = self._killer_pair()
        room = self._safety_room(attacker, victim)
        room.id = "room-1"
        api = module.FightApi.__new__(module.FightApi)
        api.fight_handler = handler
        handler.multi_hit = Mock(return_value={"to_char": "hit", "killed": False, "xp_gain": 0})
        handler.build_round_payload = Mock(side_effect=lambda _a, _v, _r, result, _ids: result)
        view = SimpleNamespace(actor=attacker, victim=victim, room=room)
        commands = SimpleNamespace(_pre_corpse_ids=Mock(return_value=set()))
        result = api.execute_fight_plan(None, commands, view, SimpleNamespace(operation="multi_hit", data={}))
        self.assertTrue(attacker.status_flags.act & int(_PlayerActBits.PLR_KILLER))
        self.assertIs(attacker.fighting, victim)
        self.assertTrue(result["to_char"].startswith("*** You are now a KILLER!! ***"))
        handler.character_service.save_character.assert_called_once_with(attacker)

    def test_failed_disarm_still_checks_killer_and_returns_notices(self):
        replacements = {name: SimpleNamespace(**{attr: object}) for name, attr in (
            ("api.FightApi", "FightApi"), ("api.MovementApi", "MovementApi"),
            ("game.WeatherHandler", "WeatherHandler"), ("interp.Context", "Context"),
            ("item.Effect", "Effect"), ("api.InterpApi", "InterpApi"),
            ("api.SkillApi", "SkillApi"), ("api.SpellApi", "SpellApi"),
            ("skill.SpellContext", "SpellContext"), ("util.MovementUtil", "MovementUtil"),
            ("util.PayloadUtil", "PayloadUtil"), ("util.PlayerUtil", "PlayerUtil"))}
        replacements["combat.CombatHandler"] = SimpleNamespace(FightHandler=FightHandler)
        with unittest.mock.patch.dict(sys.modules, replacements):
            spec = importlib.util.spec_from_file_location("_test_killer_fight_commands", SRC / "interp/commands/Fight.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        attacker, victim, handler = self._killer_pair()
        room = self._safety_room(attacker, victim)
        victim.equipped = SimpleNamespace(wielded=object())
        commands = module.Fight.__new__(module.Fight)
        commands.fight_handler = handler
        commands.skill_api = SimpleNamespace(get_rating=Mock(return_value=0))
        commands.skill_registry = SimpleNamespace(get=Mock())
        view = SimpleNamespace(skill=object(), actor=attacker, victim=victim, room=room, extra={})
        commands.fight_api = SimpleNamespace(build_fight_view=Mock(return_value=view),
                                            evaluate_guards_only_view=Mock(return_value=None))
        commands._combat_skill_chance = Mock(return_value=0)
        commands._set_wait = Mock()
        commands._skill_beats = Mock(return_value=12)
        commands._check_improve = Mock()
        commands._command_payload = Mock(return_value={"to_char": "failed"})
        commands._room_targets = Mock(return_value=[])
        result = commands.do_disarm(attacker, SimpleNamespace(finish=Mock()))
        self.assertEqual("WIZ_FLAGS", result["payloads"][0]["wiznet_flag"])
        handler.character_service.save_character.assert_called_once_with(attacker)

    def test_notice_merge_preserves_damage_rewards_without_duplication(self):
        merged = FightHandler._merge_attack_payloads(
            {"to_char": "notice", "to_wiznet": "alert"},
            {"to_char": "hit", "to_victim": "hurt", "xp_gain": 5, "killed": True, "level_up_messages": "level"})
        self.assertEqual("noticehit", merged["to_char"])
        self.assertEqual("hurt", merged["to_victim"])
        self.assertEqual(5, merged["xp_gain"])
        self.assertEqual("level", merged["level_up_messages"])
        self.assertEqual("alert", merged["to_wiznet"])

    def test_area_spell_caller_skips_protected_targets_before_damage(self):
        SpellApi = self._spell_api_class()

        attacker, allowed = self._player("attacker"), self._mob("allowed")
        charmed, immortal = self._mob("charmed"), self._player("immortal")
        charmed.master = attacker
        charmed.status_flags.affected_by = int(_AffectBits.AFF_CHARM)
        immortal.is_immortal = True
        immortal.level = _CharacterApi.GameParameters.LEVEL_IMMORTAL.value + 1
        room = self._safety_room(attacker, allowed, charmed, immortal)
        handler = self._handler(room)
        handler.damage = Mock(return_value={"killed": False})
        spell_api = SpellApi(effect_handler=Mock(), interp_api=Mock())
        spell_api._fight_handler = Mock(return_value=handler)
        spell_api._room_entities = Mock(return_value=[attacker, allowed, charmed, immortal])
        spell_api.eval_int = Mock(return_value=10)
        spell_api._queue_damage_payload = Mock()
        ctx = SimpleNamespace(actor=attacker, room=room, spell=SimpleNamespace(name="earthquake"),
                              mark_performed=Mock(return_value=True))

        self.assertTrue(spell_api.damage_room_expr(ctx, "10", save_half=False))

        handler.damage.assert_called_once_with(attacker, allowed, 10, dt="earthquake", dam_type="DAM_NONE")
        spell_api._queue_damage_payload.assert_called_once_with(ctx, {"killed": False}, allowed)
        ctx.mark_performed.assert_called_once_with()

    def test_spell_safety_self_and_retaliation_precede_area_protections(self):
        attacker, victim = self._player("attacker"), self._mob("victim")
        attacker.guild = ""
        victim.fighting = attacker
        room = self._safety_room(attacker, victim)
        room.room_flags = int(_RoomFlags.ROOM_SAFE)
        handler = self._handler(room)
        self.assertTrue(handler.is_safe_spell(attacker, attacker, area=True))
        self.assertFalse(handler.is_safe_spell(attacker, attacker))
        for area in (False, True):
            self.assertFalse(handler.is_safe_spell(attacker, victim, area=area))

    def test_spell_safety_immortal_override_is_single_target_only(self):
        threshold = _CharacterApi.GameParameters.LEVEL_IMMORTAL.value
        for level, immortal in ((threshold, True), (threshold + 1, True), (threshold + 1, False)):
            for area in (False, True):
                with self.subTest(level=level, immortal=immortal, area=area):
                    attacker, victim = self._player("attacker"), self._mob("victim")
                    attacker.level, attacker.is_immortal = level, immortal
                    room = self._safety_room(attacker, victim)
                    room.room_flags = int(_RoomFlags.ROOM_SAFE)
                    self.assertEqual(not (immortal and level > threshold and not area),
                                     self._handler(room).is_safe_spell(attacker, victim, area=area))

    def test_spell_safety_protects_high_immortals_from_area_but_retaliation_wins(self):
        threshold = _CharacterApi.GameParameters.LEVEL_IMMORTAL.value
        attacker, victim = self._player("attacker"), self._player("victim")
        victim.is_immortal = True
        room = self._safety_room(attacker, victim)
        handler = self._handler(room)
        victim.level = threshold
        self.assertFalse(handler.is_safe_spell(attacker, victim, area=True))
        victim.level += 1
        self.assertTrue(handler.is_safe_spell(attacker, victim, area=True))
        self.assertFalse(handler.is_safe_spell(attacker, victim))
        victim.fighting = attacker
        self.assertFalse(handler.is_safe_spell(attacker, victim, area=True))

    def test_spell_safety_charmed_victims_exclude_owner_area_spells(self):
        for owner, area in ((True, False), (True, True), (False, False), (False, True)):
            with self.subTest(owner=owner, area=area):
                attacker, victim = self._player("attacker"), self._mob("victim")
                victim.status_flags.affected_by = int(_AffectBits.AFF_CHARM)
                victim.master = attacker if owner else self._player("owner")
                handler = self._handler(self._safety_room(attacker, victim))
                self.assertEqual(area or not owner, handler.is_safe_spell(attacker, victim, area=area))

    def test_spell_safety_player_cannot_hit_npc_fighting_another_group(self):
        for grouped in (False, True):
            for area in (False, True):
                with self.subTest(grouped=grouped, area=area):
                    attacker, ally, victim = self._player("attacker"), self._player("ally"), self._mob("victim")
                    ally.leader = attacker if grouped else None
                    victim.fighting = ally
                    handler = self._handler(self._safety_room(attacker, ally, victim))
                    self.assertEqual(not grouped, handler.is_safe_spell(attacker, victim, area=area))
                    self.assertEqual((False, ""), handler.is_safe(attacker, victim))

    def test_spell_safety_npc_area_targets_only_opponent_group_mobs(self):
        for fighting, grouped, area in ((False, False, True), (True, False, True),
                                        (True, True, True), (True, False, False)):
            with self.subTest(fighting=fighting, grouped=grouped, area=area):
                attacker, opponent, victim = self._mob("attacker"), self._player("opponent"), self._mob("victim")
                attacker.fighting = opponent if fighting else None
                victim.leader = opponent if grouped else None
                handler = self._handler(self._safety_room(attacker, opponent, victim))
                self.assertEqual(area and not grouped, handler.is_safe_spell(attacker, victim, area=area))

    def test_spell_safety_npc_player_targets_require_opponent_group_for_all_spells(self):
        for fighting, grouped in ((False, False), (True, False), (True, True)):
            for area in (False, True):
                with self.subTest(fighting=fighting, grouped=grouped, area=area):
                    attacker, opponent, victim = self._mob("attacker"), self._player("opponent"), self._player("victim")
                    attacker.fighting = opponent if fighting else None
                    victim.leader = opponent if grouped else None
                    handler = self._handler(self._safety_room(attacker, opponent, victim))
                    self.assertEqual(fighting and not grouped, handler.is_safe_spell(attacker, victim, area=area))

    def test_spell_safety_preserves_npc_protections(self):
        for protection in ("safe_room", "shop", "ACT_TRAIN", "ACT_PRACTICE", "ACT_IS_HEALER", "ACT_IS_CHANGER", "ACT_PET"):
            for area in (False, True):
                with self.subTest(protection=protection, area=area):
                    attacker, victim = self._player("attacker"), self._mob("victim")
                    room = self._safety_room(attacker, victim)
                    handler = self._handler(room)
                    if protection == "safe_room":
                        room.room_flags = int(_RoomFlags.ROOM_SAFE)
                    elif protection == "shop":
                        handler.shop_registry.find_by_keeper_vnum.return_value = object()
                    else:
                        handler.ActBits = SimpleNamespace(**{protection: 4})
                        victim.status_flags.act = 4
                    self.assertTrue(handler.is_safe_spell(attacker, victim, area=area))

    def test_spell_safety_preserves_player_clan_and_criminal_exceptions(self):
        for attacker_guild, victim_guild, level, flags, blocked in (
                ("", "rom", 5, 0, True), ("", "", 50, _PlayerActBits.PLR_KILLER, True),
                ("rom", "", 5, 0, True), ("rom", "rom", 13, 0, False),
                ("rom", "rom", 14, 0, True), ("rom", "", 50, _PlayerActBits.PLR_KILLER, False),
                ("rom", "", 50, _PlayerActBits.PLR_THIEF, False)):
            for area in (False, True):
                with self.subTest(attacker_guild=attacker_guild, victim_guild=victim_guild, level=level, flags=flags, area=area):
                    attacker, victim = self._player("attacker"), self._player("victim")
                    attacker.guild, victim.guild = attacker_guild, victim_guild
                    attacker.level = level
                    victim.status_flags.act = int(flags)
                    handler = self._handler(self._safety_room(attacker, victim))
                    self.assertEqual(blocked, handler.is_safe_spell(attacker, victim, area=area))

    def test_spell_safety_preserves_charmed_npc_and_safe_room_player_protection(self):
        attacker, victim, master = self._mob("attacker"), self._player("victim"), self._player("master")
        attacker.status_flags.affected_by = int(_AffectBits.AFF_CHARM)
        attacker.master = master
        room = self._safety_room(attacker, victim, master)
        handler = self._handler(room)
        for area in (False, True):
            master.fighting = None
            self.assertTrue(handler.is_safe_spell(attacker, victim, area=area))
            master.fighting = victim
            self.assertFalse(handler.is_safe_spell(attacker, victim, area=area))
            room.room_flags = int(_RoomFlags.ROOM_SAFE)
            self.assertTrue(handler.is_safe_spell(attacker, victim, area=area))
            room.room_flags = 0

    def test_spell_safety_rejects_missing_dead_or_absent_targets(self):
        attacker, victim = self._player("attacker"), self._mob("victim")
        handler = self._handler(self._safety_room(attacker, victim))
        self.assertTrue(handler.is_safe_spell(None, victim))
        self.assertTrue(handler.is_safe_spell(attacker, None))
        victim.character_attributes.position = _Positions.POS_DEAD
        self.assertTrue(handler.is_safe_spell(attacker, victim))
        victim.character_attributes.position = _Positions.POS_STANDING
        victim.room_id = "elsewhere"
        self.assertTrue(handler.is_safe_spell(attacker, victim))
        victim.room_id = attacker.room_id
        handler._find_room_for_entity = Mock(return_value=None)
        self.assertTrue(handler.is_safe_spell(attacker, victim))

    def test_is_safe_allows_self_in_safe_room_before_protections(self):
        for entity in (self._player("player"), self._mob("mob")):
            with self.subTest(npc=entity.is_npc):
                entity.guild = ""
                room = self._safety_room(entity)
                room.room_flags = int(_RoomFlags.ROOM_SAFE)
                handler = self._handler(room)
                handler.shop_registry.find_by_keeper_vnum.return_value = object()
                self.assertEqual((False, ""), handler.is_safe(entity, entity))
                handler.shop_registry.find_by_keeper_vnum.assert_not_called()

    def test_is_safe_allows_retaliation_before_room_npc_and_clan_protections(self):
        for npc_target in (True, False):
            with self.subTest(npc=npc_target):
                attacker = self._player("attacker")
                attacker.guild = ""
                victim = self._mob("victim") if npc_target else self._player("victim")
                victim.fighting = attacker
                room = self._safety_room(attacker, victim)
                room.room_flags = int(_RoomFlags.ROOM_SAFE)
                handler = self._handler(room)
                handler.shop_registry.find_by_keeper_vnum.return_value = object()
                self.assertEqual((False, ""), handler.is_safe(attacker, victim))
                handler.shop_registry.find_by_keeper_vnum.assert_not_called()

    def test_is_safe_immortal_override_requires_actual_level_above_threshold(self):
        threshold = _CharacterApi.GameParameters.LEVEL_IMMORTAL.value
        for level, immortal, blocked in ((threshold - 1, True, True),
                                           (threshold, True, True),
                                           (threshold + 1, True, False),
                                           (threshold + 1, False, True)):
            with self.subTest(level=level, immortal=immortal):
                attacker, victim = self._player("attacker"), self._mob("victim")
                attacker.level, attacker.is_immortal = level, immortal
                room = self._safety_room(attacker, victim)
                room.room_flags = int(_RoomFlags.ROOM_SAFE)
                handler = self._handler(room)
                safe, message = handler.is_safe(attacker, victim)
                self.assertEqual(blocked, safe)
                self.assertEqual("Not in this room.\r\n" if blocked else "", message)

    def test_is_safe_player_vs_player_uses_clan_rules_in_safe_room(self):
        attacker, victim = self._player("attacker"), self._player("victim")
        room = self._safety_room(attacker, victim)
        room.room_flags = int(_RoomFlags.ROOM_SAFE)
        handler = self._handler(room)
        self.assertEqual((False, ""), handler.is_safe(attacker, victim))
        attacker.guild = ""
        self.assertEqual((True, "Join a clan if you want to kill players.\r\n"),
                         handler.is_safe(attacker, victim))

    def test_is_safe_room_still_protects_players_from_npc_attackers(self):
        attacker, victim = self._mob("attacker"), self._player("victim")
        room = self._safety_room(attacker, victim)
        room.room_flags = int(_RoomFlags.ROOM_SAFE)
        self.assertEqual((True, "Not in this room.\r\n"), self._handler(room).is_safe(attacker, victim))

    def test_is_safe_does_not_enforce_command_kill_stealing_policy(self):
        for npc_target in (True, False):
            for ignore in (True, False):
                with self.subTest(npc=npc_target, ignore=ignore):
                    attacker, opponent = self._player("attacker"), self._player("opponent")
                    victim = self._mob("victim") if npc_target else self._player("victim")
                    victim.fighting = opponent
                    room = self._safety_room(attacker, victim, opponent)
                    self.assertEqual((False, ""), self._handler(room).is_safe(
                        attacker, victim, ignore_target_fighting=ignore))

    def test_is_safe_exceptions_do_not_bypass_missing_room_or_dead_target(self):
        attacker, victim = self._player("attacker"), self._mob("victim")
        attacker.is_immortal = True
        attacker.level = _CharacterApi.GameParameters.LEVEL_IMMORTAL.value + 1
        victim.fighting = attacker
        room = self._safety_room(attacker, victim)
        handler = self._handler(room)
        handler._find_room_for_entity = Mock(return_value=None)
        self.assertEqual((True, "They aren't here.\r\n"), handler.is_safe(attacker, victim))
        handler._find_room_for_entity = Mock(return_value=room)
        victim.character_attributes.position = _Positions.POS_DEAD
        self.assertEqual((True, "They are already dead.\r\n"), handler.is_safe(attacker, victim))

    def test_damage_allows_retaliation_in_safe_room_through_final_safety_check(self):
        attacker, victim = self._player("attacker"), self._mob("victim")
        victim.fighting = attacker
        victim.hit = 20
        room = self._safety_room(attacker, victim)
        room.room_flags = int(_RoomFlags.ROOM_SAFE)
        handler = self._damage_handler(room)

        result = handler.damage(attacker, victim, 1)

        self.assertEqual(19, victim.hit)
        self.assertFalse(result["killed"])
        handler.check_killer.assert_called_once_with(attacker, victim)
        handler._set_fighting.assert_called_once_with(attacker, victim)

    def _safety_room(self, *entities):
        return SimpleNamespace(
            room_flags=0,
            characters={entity.id: entity for entity in entities if not entity.is_npc},
            mobiles={entity.id: entity for entity in entities if entity.is_npc},
        )

    def test_is_safe_player_killing_membership_flags_and_level_boundary(self):
        cases = (
            # Attacker membership is required even against a flagged victim.
            ("", "rom", 5, 5, 0, "Join a clan"),
            ("", "", 50, 5, _PlayerActBits.PLR_KILLER, "Join a clan"),
            ("rom", "", 5, 5, 0, "They aren't in a clan"),
            ("rom", "rom", 13, 5, 0, ""),
            ("rom", "rom", 14, 5, 0, "Pick on someone your own size"),
            ("rom", "rom", 5, 50, 0, ""),
            ("rom", "", 50, 5, _PlayerActBits.PLR_KILLER, ""),
            ("rom", "", 50, 5, _PlayerActBits.PLR_THIEF, ""),
            ("loner", "independent", 5, 5, 0, ""),
        )
        for guild, target_guild, level, target_level, flags, reason in cases:
            with self.subTest(guild=guild, target_guild=target_guild, level=level,
                              target_level=target_level, flags=flags):
                attacker, victim = self._player("attacker"), self._player("victim")
                attacker.guild, victim.guild = guild, target_guild
                attacker.level, victim.level = level, target_level
                victim.status_flags.act = int(flags)
                room = self._safety_room(attacker, victim)
                safe, message = self._handler(room).is_safe(attacker, victim)
                self.assertEqual(bool(reason), safe)
                self.assertTrue(message.startswith(reason))
                if not safe:
                    self.assertEqual("", message)

    def test_is_safe_protects_shopkeepers_from_players_and_npcs(self):
        for attacker in (self._player("player"), self._mob("mob")):
            with self.subTest(npc=attacker.is_npc):
                victim = self._mob("keeper")
                victim.vnum = "3000"
                room = self._safety_room(attacker, victim)
                handler = self._handler(room)
                handler.shop_registry.find_by_keeper_vnum.return_value = object()
                self.assertEqual((True, "The shopkeeper wouldn't like that.\r\n"),
                                 handler.is_safe(attacker, victim))
                handler.shop_registry.find_by_keeper_vnum.assert_called_once_with("3000")

    def test_is_safe_charmed_npc_victim_requires_player_owner(self):
        for npc_attacker, charmed, owns_victim, blocked in (
                (False, True, False, True), (False, True, True, False),
                (True, True, False, False), (False, False, False, False)):
            with self.subTest(npc=npc_attacker, charmed=charmed, owner=owns_victim):
                attacker = self._mob("attacker") if npc_attacker else self._player("attacker")
                victim = self._mob("victim")
                victim.status_flags.affected_by = int(_AffectBits.AFF_CHARM) if charmed else 0
                victim.master = attacker if owns_victim else self._player("owner")
                room = self._safety_room(attacker, victim)
                self.assertEqual((blocked, "You don't own that monster.\r\n" if blocked else ""),
                                 self._handler(room).is_safe(attacker, victim))

    def test_is_safe_charmed_npc_attacker_requires_master_fighting_player(self):
        for charmed, has_master, master_attacking, blocked in (
                (True, True, False, True), (True, True, True, False),
                (True, False, False, False), (False, True, False, False)):
            with self.subTest(charmed=charmed, has_master=has_master, master_attacking=master_attacking):
                attacker, victim = self._mob("attacker"), self._player("victim")
                attacker.status_flags.affected_by = int(_AffectBits.AFF_CHARM) if charmed else 0
                master = self._player("owner")
                master.fighting = victim if master_attacking else self._mob("other opponent")
                attacker.master = master if has_master else None
                room = self._safety_room(attacker, victim)
                self.assertEqual((blocked, "Players are your friends!\r\n" if blocked else ""),
                                 self._handler(room).is_safe(attacker, victim))

    def test_damage_enforces_player_killing_rules_without_command_guards(self):
        attacker, victim = self._player("attacker"), self._player("victim")
        attacker.guild = ""
        victim.hit = 20
        handler = self._damage_handler(self._safety_room(attacker, victim))
        result = handler.damage(attacker, victim, 100)
        self.assertEqual("Join a clan if you want to kill players.\r\n", result["to_char"])
        self.assertEqual(20, victim.hit)
        handler.check_killer.assert_not_called()
        handler._set_fighting.assert_not_called()
        handler.raw_kill.assert_not_called()

    def _damage_handler(self, room):
        handler = self._handler(room)
        handler.check_killer = Mock(return_value={})
        handler._set_fighting = Mock()
        handler._check_immunity = Mock(return_value="IS_NORMAL")
        handler.dam_message = Mock(return_value={"to_char": "hit", "to_victim": "hit", "to_room": "hit"})
        handler.raw_kill = Mock()
        handler.xp_compute = Mock()
        return handler

    def test_damage_rejects_missing_or_dead_victim_before_side_effects(self):
        attacker = self._player("attacker")
        dead = self._mob("dead")
        dead.character_attributes.position = _Positions.POS_DEAD
        dead.hit = -20
        for victim in (None, dead):
            with self.subTest(victim=victim):
                handler = self._damage_handler(SimpleNamespace())
                handler.is_safe = Mock()
                self.assertEqual(handler._error_payload(), handler.damage(attacker, victim, 100))
                handler.is_safe.assert_not_called()
                handler.check_killer.assert_not_called()
                handler._set_fighting.assert_not_called()
                handler._check_immunity.assert_not_called()
                handler.dam_message.assert_not_called()
                handler.raw_kill.assert_not_called()
                handler.xp_compute.assert_not_called()
                self.assertEqual(-20, dead.hit)

    def test_damage_enforces_safe_room_even_for_misses_and_hidden_damage(self):
        for dam in (0, 100):
            for show in (False, True):
                with self.subTest(dam=dam, show=show):
                    attacker = self._player("attacker")
                    victim = self._mob("victim")
                    victim.hit = 20
                    room = SimpleNamespace(room_flags=int(_RoomFlags.ROOM_SAFE),
                                           characters={attacker.id: attacker}, mobiles={victim.id: victim})
                    handler = self._damage_handler(room)
                    result = handler.damage(attacker, victim, dam, show=show)
                    self.assertEqual("Not in this room.\r\n", result["to_char"])
                    self.assertFalse(result["killed"])
                    self.assertEqual("", result["to_victim"])
                    self.assertEqual("", result["to_room"])
                    self.assertEqual(20, victim.hit)
                    self.assertIsNone(attacker.fighting)
                    self.assertIsNone(victim.fighting)
                    handler.check_killer.assert_not_called()
                    handler._set_fighting.assert_not_called()
                    handler._check_immunity.assert_not_called()
                    handler.dam_message.assert_not_called()
                    handler.raw_kill.assert_not_called()
                    handler.xp_compute.assert_not_called()

    def test_damage_enforces_protected_npc_safety(self):
        attacker = self._player("attacker")
        victim = self._mob("trainer")
        victim.status_flags.act = 4
        victim.hit = 20
        room = SimpleNamespace(room_flags=0, characters={attacker.id: attacker}, mobiles={victim.id: victim})
        handler = self._damage_handler(room)
        handler.ActBits = SimpleNamespace(ACT_TRAIN=4)

        result = handler.damage(attacker, victim, 100)

        self.assertEqual("I don't think Mota would approve.\r\n", result["to_char"])
        self.assertEqual(20, victim.hit)
        handler.check_killer.assert_not_called()
        handler._set_fighting.assert_not_called()
        handler.raw_kill.assert_not_called()

    def test_allowed_damage_checks_killer_before_combat_even_for_zero_damage(self):
        for dam in (0, 1):
            with self.subTest(dam=dam):
                attacker = self._player("attacker")
                victim = self._mob("victim")
                victim.hit = 20
                room = SimpleNamespace(room_flags=0, characters={attacker.id: attacker},
                                       mobiles={victim.id: victim})
                handler = self._damage_handler(room)
                events = Mock()
                events.attach_mock(handler.check_killer, "killer")
                events.attach_mock(handler._set_fighting, "fight")
                result = handler.damage(attacker, victim, dam)
                self.assertEqual([unittest.mock.call.killer(attacker, victim),
                                  unittest.mock.call.fight(attacker, victim)], events.mock_calls)
                self.assertEqual(20 - dam, victim.hit)
                self.assertFalse(result["killed"])
                handler.raw_kill.assert_not_called()

    def test_self_damage_bypasses_hostile_checks_in_safe_room(self):
        victim = self._mob("victim")
        victim.hit = 20
        room = SimpleNamespace(room_flags=int(_RoomFlags.ROOM_SAFE), mobiles={victim.id: victim})
        handler = self._damage_handler(room)
        handler.is_safe = Mock(return_value=(True, "blocked"))
        result = handler.damage(victim, victim, 1)
        handler.is_safe.assert_not_called()
        handler.check_killer.assert_not_called()
        self.assertEqual(19, victim.hit)
        self.assertFalse(result["killed"])

    def test_refresh_combat_registry_retains_only_fights_in_the_room(self):
        attacker = self._mob("mob-1")
        victim = self._player("char-1")
        absent = self._mob("mob-2")
        attacker.fighting = victim
        victim.fighting = absent
        room = SimpleNamespace(id="room-1", people=lambda: [attacker, victim],
                               find_entity_in_room=lambda entity_id: {victim.id: victim, attacker.id: attacker}.get(entity_id))
        handler = self._handler(room)
        handler.room_registry.all_rooms = lambda: [room]
        handler.combat_registry.retain_keys = Mock()
        handler.stop_fighting = Mock()

        handler.refresh_combat_registry_from_world()

        handler.combat_registry.upsert.assert_called_once_with(attacker.id, victim.id, room.id)
        handler.combat_registry.retain_keys.assert_called_once_with({(attacker.id, victim.id, room.id)})
        handler.stop_fighting.assert_called_once_with(victim, both=False)

    def test_violence_update_attacks_npcs_first_and_prompts_message_recipients(self):
        attacker = self._mob("mob-1")
        victim = self._player("char-1")
        attacker.fighting = victim
        victim.fighting = attacker
        room = SimpleNamespace(id="room-1", area_id="area-1", characters={victim.id: victim},
                               find_entity_in_room=lambda entity_id: {victim.id: victim, attacker.id: attacker}.get(entity_id))
        handler = self._handler(room)
        handler.area_registry.get_or_none = lambda **_kwargs: SimpleNamespace(id="area-1")
        handler.combat_registry.all_events = lambda: [
            SimpleNamespace(id="player-event", room_id=room.id, attacker_id=victim.id, defender_id=attacker.id),
            SimpleNamespace(id="npc-event", room_id=room.id, attacker_id=attacker.id, defender_id=victim.id),
        ]
        handler.multi_hit = Mock(return_value={"to_char": "Your attack.\r\n", "to_victim": "Their attack.\r\n"})
        handler._append_condition_line = lambda text, _target: text
        handler.check_assist = Mock()
        handler.message_bus = SimpleNamespace(text_to_message=lambda text: text,
                                              send_to_character=AsyncMock(), send_to_room=AsyncMock(),
                                              send_prompt=AsyncMock())
        with unittest.mock.patch.object(_SkillUtil, "take_improve_messages", return_value="", create=True):
            asyncio.run(handler.violence_update())

        self.assertEqual([(attacker, victim), (victim, attacker)],
                         [call.args for call in handler.multi_hit.call_args_list])
        self.assertEqual([("char-1", "Their attack.\r\n"), ("char-1", "Your attack.\r\n")],
                         [call.args for call in handler.message_bus.send_to_character.await_args_list])
        self.assertEqual(2, handler.check_assist.call_count)
        handler.message_bus.send_prompt.assert_awaited_once()

    def test_aggression_update_emits_opening_round_and_prompt(self):
        victim = self._player("char-1")
        attacker = self._mob("mob-1")
        room = SimpleNamespace(id="room-1", area_id="area-1")
        handler = self._handler(room)
        handler.room_registry.all_rooms = lambda: [room]
        handler.area_registry.get_or_none = lambda **_kwargs: SimpleNamespace(id="area-1")
        handler.aggressive_room_rounds = Mock(return_value=[
            (attacker, {"victim": victim, "to_victim": "The mob hits you.\r\n"})])
        handler.message_bus = SimpleNamespace(text_to_message=lambda text: text,
                                              send_to_character=AsyncMock(), send_prompt=AsyncMock())

        asyncio.run(handler.aggression_update())

        handler.message_bus.send_to_character.assert_awaited_once_with("char-1", "The mob hits you.\r\n")
        handler.message_bus.send_prompt.assert_awaited_once()

    def _handler(self, room):
        handler = FightHandler.__new__(FightHandler)
        handler.logger = _Logger()
        handler.area_registry = SimpleNamespace(get_or_none=lambda **_kwargs: None)
        handler.combat_registry = SimpleNamespace(upsert=Mock())
        handler.room_registry = SimpleNamespace(get=lambda **_kwargs: room, get_or_none=lambda **_kwargs: room)
        handler.PositionsEnum = _Positions
        handler.ActBits = _ActBits
        handler.RoomFlags = _RoomFlags
        handler.PlayerActBits = _PlayerActBits
        handler.shop_registry = SimpleNamespace(find_by_keeper_vnum=Mock(return_value=None))
        handler.character_service = SimpleNamespace(save_character=Mock(return_value=True))
        handler.effect_handler = SimpleNamespace(affect_strip=Mock())
        handler.wiz_handler = SimpleNamespace(wiznet_targets=Mock(return_value=[]))
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
            guild="rom",
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

    def test_aggressive_entry_rounds_attacks_immediately(self):
        victim = self._player("char-1")
        aggressor = self._mob("mob-1")
        room = SimpleNamespace(id="room-1", area_id="area-1", room_flags=0, mobiles={"mob-1": aggressor}, characters={"char-1": victim})
        handler = self._handler(room)
        handler.multi_hit = Mock(return_value={"to_victim": "The mob hits you.\r\n"})

        rounds = handler.aggressive_entry_rounds(victim, room)

        handler.multi_hit.assert_called_once_with(aggressor, victim, dt="TYPE_UNDEFINED")
        self.assertEqual([(aggressor, {"to_char": "", "to_room": "", "targets": [],
                                     "victim": victim, "to_victim": "The mob hits you.\r\n"})], rounds)
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
        def attack(attacker, target, dt):
            self.assertIs(attacker.fighting, target)
            target.hit -= 7
            return {"to_victim": "The mob hits you.\r\n", "to_room": "The mob attacks.\r\n"}

        victim.hit = 20
        handler.multi_hit = Mock(side_effect=attack)
        handler._select_aggressive_victim = Mock(return_value=victim)
        handler._should_aggress = Mock(return_value=True)

        rounds = handler.aggressive_room_rounds(room)

        handler.multi_hit.assert_called_once_with(aggressor, victim, dt="TYPE_UNDEFINED")
        self.assertEqual(13, victim.hit)
        self.assertEqual([(aggressor, {"to_char": "", "to_room": "The mob attacks.\r\n",
                                     "targets": [witness], "victim": victim,
                                     "to_victim": "The mob hits you.\r\n"})], rounds)
        self.assertEqual(1, handler._select_aggressive_victim.call_count)
        self.assertEqual(1, handler._should_aggress.call_count)
        self.assertIs(aggressor.fighting, victim)
        self.assertIs(victim.fighting, aggressor)

        self.assertEqual([], handler.aggressive_room_rounds(room))
        handler.multi_hit.assert_called_once_with(aggressor, victim, dt="TYPE_UNDEFINED")

    def test_aggression_does_not_attack_without_a_valid_start(self):
        for entry in (False, True):
            for reason in ("no victim", "failed guard", "already fighting", "empty area"):
                with self.subTest(entry=entry, reason=reason):
                    victim = self._player("char-1")
                    aggressor = self._mob("mob-1")
                    room = SimpleNamespace(id="room-1", area_id="area-1", room_flags=0,
                                           mobiles={aggressor.id: aggressor}, characters={victim.id: victim})
                    handler = self._handler(room)
                    handler.multi_hit = Mock()
                    handler._select_aggressive_victim = Mock(
                        return_value=None if reason == "no victim" else victim)
                    handler._should_aggress = Mock(return_value=reason != "failed guard")
                    if reason == "already fighting":
                        aggressor.fighting = victim
                    if reason == "empty area":
                        handler.area_registry.get_or_none = lambda **_kwargs: SimpleNamespace(empty=True)

                    rounds = (handler.aggressive_entry_rounds(victim, room) if entry
                              else handler.aggressive_room_rounds(room))

                    self.assertEqual([], rounds)
                    handler.multi_hit.assert_not_called()

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

    def test_damage_uses_skill_payload_for_successful_dodge(self):
        attacker = self._player("char-1")
        attacker.name = "Tester"
        victim = self._player("char-2")
        victim.name = "Target"
        room = SimpleNamespace(id="room-1", area_id="area-1", room_flags=0, mobiles={}, characters={"char-1": attacker, "char-2": victim})
        handler = self._handler(room)

        messages = {
            ("to_char", "success"): "{t} dodges your attack.",
            ("to_victim", "success"): "You dodge {c}'s attack.",
        }
        dodge = SimpleNamespace(message=lambda channel, key, **tokens: messages.get((channel, key), "").format_map(tokens))
        handler.skill_registry = SimpleNamespace(get_or_none=lambda **kwargs: dodge if kwargs.get("name") == "dodge" else None)

        with unittest.mock.patch.object(handler, "check_parry", return_value=False), \
                unittest.mock.patch.object(handler, "check_dodge", return_value=True), \
                unittest.mock.patch.object(handler, "check_shield_block", return_value=False):
            result = handler.damage(attacker, victim, 0, dt="slash", weapon_hit=True)

        self.assertEqual("*** You are now a KILLER!! ***\r\nTarget dodges your attack.\r\n", result["to_char"])
        self.assertEqual("You dodge Tester's attack.\r\n", result["to_victim"])
        self.assertEqual("", result["to_room"])
        self.assertFalse(result["killed"])

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

        with unittest.mock.patch.object(sys.modules["combat.FightHandler"].GameApi, "is_set", return_value=False, create=True), \
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

    def test_is_safe_can_ignore_existing_fight_for_direct_offensive_spell(self):
        owner = self._player("char-1")
        caster = self._player("char-2")
        victim = self._mob("mob-1")
        victim.fighting = owner
        room = SimpleNamespace(
            id="room-1",
            area_id="area-1",
            room_flags=0,
            mobiles={"mob-1": victim},
            characters={"char-1": owner, "char-2": caster},
        )
        handler = self._handler(room)

        safe, message = handler.is_safe(caster, victim, room=room, ignore_target_fighting=True)

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
