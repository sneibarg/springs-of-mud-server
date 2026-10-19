import importlib.util
import sys
import unittest
from enum import IntEnum
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch, call

from tests import test_combat_handler_aggression as fixtures
from tests.test_combat_survival import Components

ROOT = Path(__file__).resolve().parents[1]
Runtime = sys.modules[fixtures.FightHandler.__module__]


def load_class(name, path, class_name):
    replacements = {
        "game.HandlerService": SimpleNamespace(HandlerService=object),
        "interp.Context": Components["interp.Context"],
        "interp.commands.Fight": SimpleNamespace(Fight=object),
        "skill": SimpleNamespace(Skill=object),
        "skill.SkillRegistry": SimpleNamespace(SkillRegistry=object),
    }
    with patch.dict(sys.modules, replacements):
        spec = importlib.util.spec_from_file_location(name, ROOT / "src" / path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return getattr(module, class_name)


CombatSkillHandler = load_class("_round_skill_handler", "combat/CombatSkillHandler.py", "CombatSkillHandler")
SkillApi = load_class("_round_skill_api", "api/SkillApi.py", "SkillApi")


class Bits(IntEnum):
    OFF_BASH = 1
    OFF_BERSERK = 2
    OFF_DISARM = 4
    OFF_KICK = 8
    OFF_KICK_DIRT = 16
    OFF_TRIP = 32
    OFF_BACKSTAB = 64
    ACT_WARRIOR = 128
    ACT_THIEF = 256
    AFF_BERSERK = 512
    AFF_HASTE = 1024
    AFF_SLOW = 2048


class TestCombatRoundSkills(unittest.TestCase):
    def setUp(self):
        self.fixtures = fixtures.TestFightHandlerAggression()
        self.actor, self.victim, self.combat = self.fixtures._killer_pair()
        self.combat.AffectBits = Bits

    def test_player_extra_attacks_improve_after_each_swing_even_if_combat_ends(self):
        for end_after, expected in ((1, []), (2, [("second attack", True, 5)]),
                                    (3, [("second attack", True, 5), ("third attack", True, 6)])):
            with self.subTest(end_after=end_after):
                self.actor.fighting = self.victim
                swings = []
                def hit(*args, **kwargs):
                    swings.append("hit")
                    if len(swings) == end_after:
                        self.actor.fighting = None
                    return {}
                self.combat.one_hit = Mock(side_effect=hit)
                self.combat._skill_percent = Mock(return_value=100)
                learned = []
                def improve(actor, name, success, multiplier):
                    self.assertEqual(2 if name == "second attack" else 3, len(swings))
                    learned.append((name, success, multiplier))
                with patch.object(Runtime.CharacterApi, "is_affected", return_value=False), \
                        patch.object(Runtime.random, "randint", return_value=1), \
                        patch.object(Runtime.Ability, "check_improve_by_name", side_effect=improve):
                    self.combat.multi_hit(self.actor, self.victim)
                self.assertEqual(expected, learned)

    def test_failed_extra_attack_rolls_do_not_improve(self):
        self.actor.fighting = self.victim
        self.combat.one_hit = Mock(return_value={})
        self.combat._skill_percent = Mock(return_value=100)
        with patch.object(Runtime.CharacterApi, "is_affected", return_value=False), \
                patch.object(Runtime.random, "randint", return_value=100), \
                patch.object(Runtime.Ability, "check_improve_by_name") as improve:
            self.combat.multi_hit(self.actor, self.victim)
            improve.assert_not_called()
            self.combat.one_hit.assert_called_once()

    def selector(self, number):
        self.actor = self.fixtures._mob("actor")
        self.actor.fighting = self.victim
        self.actor.status_flags.pulse_wait = 0
        self.actor.status_flags.off = sum(int(flag) for flag in Bits if flag.name.startswith("OFF_"))
        self.actor.status_flags.act = 0
        self.actor.equipped = None
        self.commands = SimpleNamespace(**{"do_" + name: Mock(return_value={"to_char": name})
                                          for name in ("bash", "berserk", "disarm", "kick", "dirt", "trip", "backstab")})
        self.room = object()
        registry = SimpleNamespace(room_registry=SimpleNamespace(get_or_none=Mock(return_value=self.room)),
                                   interp_registry=SimpleNamespace(get_or_none=Mock(side_effect=lambda **kw: SimpleNamespace(name=kw["name"]))))
        handler = CombatSkillHandler(self.commands, registry, object(), SimpleNamespace(get=lambda name: Bits))
        handler.rng = SimpleNamespace(number_range=Mock(side_effect=[0, number]))
        return handler

    def test_all_npc_choices_keep_noop_slots_and_command_context(self):
        for number, name in enumerate(("bash", "berserk", "disarm", "kick", "dirt", None, "trip", None, "backstab")):
            with self.subTest(number=number):
                handler = self.selector(number)
                result = handler.after_round(self.actor)
                self.assertEqual([call(0, 2), call(0, 8)], handler.rng.number_range.call_args_list)
                if name is None:
                    self.assertEqual([], result)
                else:
                    command = getattr(self.commands, "do_" + name)
                    command.assert_called_once()
                    context = command.call_args.args[1]
                    self.assertEqual(([], "", name), (context.parameters, context.result, context.command.name))
                    self.assertIs(self.room, context.room)
                    self.assertIs(self.actor, result[0]["actor"])
                    self.assertIs(context, result[0]["context"])

    def test_npc_flags_wait_and_existing_berserk_gate_selection(self):
        for kind in ("no_flag", "waiting", "not_fighting", "berserk"):
            with self.subTest(kind=kind):
                handler = self.selector(1)
                if kind == "no_flag":
                    self.actor.status_flags.off = 0
                elif kind == "waiting":
                    self.actor.status_flags.pulse_wait = 1
                elif kind == "not_fighting":
                    self.actor.fighting = None
                else:
                    self.actor.status_flags.affected_by = int(Bits.AFF_BERSERK)
                self.assertEqual([], handler.after_round(self.actor))
                if kind in ("waiting", "not_fighting"):
                    handler.rng.number_range.assert_not_called()
                self.commands.do_berserk.assert_not_called()

    def test_disarm_class_fallback_requires_wielded_item(self):
        for armed, class_flag, expected in ((True, Bits.ACT_WARRIOR, True), (True, Bits.ACT_THIEF, True),
                                           (False, Bits.ACT_WARRIOR, False), (True, 0, False)):
            handler = self.selector(2)
            self.actor.status_flags.off = 0
            self.actor.status_flags.act = int(class_flag)
            self.actor.equipped = SimpleNamespace(wielded=SimpleNamespace(item_type="weapon") if armed else None)
            self.assertEqual(expected, bool(handler.after_round(self.actor)))

    def test_mob_round_runs_selection_after_swings_and_preserves_payload(self):
        handler = self.selector(0)
        self.combat._find_room_for_entity = Mock(return_value=None)
        self.combat._mob_has_off = Mock(return_value=False)
        self.combat._skill_percent = Mock(return_value=100)
        self.combat.one_hit = Mock(return_value={"to_char": "swing"})
        self.combat.npc_skill_handler = handler
        with patch.object(Runtime.CharacterApi, "is_affected", return_value=False), \
                patch.object(Runtime.random, "randint", return_value=1), \
                patch.object(Runtime.Ability, "check_improve_by_name") as improve:
            result = self.combat.mob_hit(self.actor, self.victim)
        self.assertEqual(3, self.combat.one_hit.call_count)
        improve.assert_not_called()
        self.assertEqual("swingswingswing", result["to_char"])
        self.assertEqual("bash", result["post_damage_actions"][0]["context"].command.name)

    def test_npc_rating_reads_real_status_flag_fields(self):
        handler = self.selector(0)
        api = SkillApi.__new__(SkillApi)
        api.ActBits = api.OffBits = Bits
        self.actor.level = 20
        self.actor.status_flags.pulse_daze = 0
        self.assertEqual(70, api.get_rating(self.actor, SimpleNamespace(name="bash")))
        self.actor.status_flags.pulse_daze = 1
        self.assertEqual(46, api.get_rating(self.actor, SimpleNamespace(name="bash")))

    def test_selected_kick_uses_real_command_wait_rating_damage_and_payload(self):
        handler = self.selector(3)
        commands_module = Components["interp.commands.Fight"]
        commands = commands_module.Fight.__new__(commands_module.Fight)
        skill = SimpleNamespace(name="kick", beats=12)
        commands.fight_api = SimpleNamespace(
            build_fight_view=Mock(return_value=SimpleNamespace(skill=skill, room=self.room, victim=self.victim)),
            evaluate_guards_only_view=Mock(return_value=None))
        commands.skill_api = SkillApi.__new__(SkillApi)
        commands.skill_api.ActBits = commands.skill_api.OffBits = Bits
        commands.fight_handler = SimpleNamespace(damage=Mock(return_value={"to_room": "kick hits"}),
                                                 build_round_payload=Mock(return_value={"to_room": "kick hits"}))
        self.actor.level = 20
        self.actor.status_flags.pulse_daze = 0
        handler.fight_commands = commands
        with patch.object(commands_module.random, "randint", side_effect=[1, 7]):
            result = handler.after_round(self.actor)
        self.assertEqual(12, self.actor.status_flags.pulse_wait)
        commands.fight_handler.damage.assert_called_once_with(self.actor, self.victim, 7, dt="kick")
        self.assertEqual({"to_room": "kick hits"}, result[0]["payloads"][0])

    def test_mob_stopping_after_third_attack_skips_skill_selection(self):
        selector = self.selector(0)
        self.combat.npc_skill_handler = selector
        self.combat._find_room_for_entity = Mock(return_value=None)
        self.combat._mob_has_off = Mock(return_value=False)
        self.combat._skill_percent = Mock(return_value=100)
        hits = []
        def hit(*args, **kwargs):
            hits.append(1)
            if len(hits) == 3:
                self.actor.fighting = None
            return {}
        self.combat.one_hit = Mock(side_effect=hit)
        with patch.object(Runtime.CharacterApi, "is_affected", return_value=False), \
                patch.object(Runtime.random, "randint", return_value=1):
            self.combat.mob_hit(self.actor, self.victim)
        selector.rng.number_range.assert_not_called()


if __name__ == "__main__":
    unittest.main()
