import importlib.util
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch
from tests import test_bash_parity as bash
from tests import test_combat_handler_aggression as fixtures

Module = bash.Module


class TestFinalCombatParity(unittest.TestCase):
    def setUp(self):
        fixture = bash.TestBashParity()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.commands, self.actor, self.victim = fixture.commands, fixture.actor, fixture.victim
        self.room, self.context = fixture.room, fixture.context
        self.actor.hit, self.actor.max_hit, self.actor.mana, self.actor.movement = 10, 100, 100, 40
        self.actor.level = 24
        self.context.room = self.room
        self.commands._position = Mock(return_value=7)
        self.commands._pos = Mock(return_value=7)
        self.commands._check_improve = Mock()

    def test_berserk_uncapped_chance_fuzzy_duration_and_loaded_wait(self):
        self.commands.fight_handler.rng = SimpleNamespace(number_fuzzy=Mock(return_value=4))
        self.commands.effect_handler = SimpleNamespace(affect_to_char=Mock())
        self.room.player_targets = lambda actor: []
        with patch.object(Module.random, "randint", return_value=100), \
                patch.object(Module, "Effect", side_effect=lambda **kwargs: SimpleNamespace(**kwargs)):
            self.commands.do_berserk(self.actor, self.context)
        self.commands.fight_handler.rng.number_fuzzy.assert_called_once_with(3)
        self.assertEqual([4, 4, 4], [c.args[1].duration for c in self.commands.effect_handler.affect_to_char.call_args_list])
        self.assertEqual((10, 50, 20, 58), (self.actor.status_flags.pulse_wait, self.actor.mana, self.actor.movement, self.actor.hit))

    def test_berserk_exact_endpoint_fails_and_waits_three_pulses(self):
        self.commands.skill_api.get_rating.side_effect = None
        self.commands.skill_api.get_rating.return_value = 50
        # rating50 + fighting10 + hp modifier20 =80.
        with patch.object(Module.random, "randint", return_value=80):
            self.commands.do_berserk(self.actor, self.context)
        self.assertEqual((30, 75, 20), (self.actor.status_flags.pulse_wait, self.actor.mana, self.actor.movement))

    def flee_setup(self):
        self.actor.fighting = self.victim
        self.actor.room_id = "source"
        self.context.command = SimpleNamespace(name="flee")
        self.room.exits = [SimpleNamespace(direction=0)]
        self.room.player_targets = lambda actor: []
        self.room.remove_player_from_room = Mock()
        self.destination = SimpleNamespace(id="dest", area_id="area", player_targets=lambda actor: [], add_player_to_room=Mock())
        self.commands._flee_destination = Mock(return_value=self.destination)
        self.commands._movement_cost = Mock(return_value=2)
        self.commands.fight_handler.stop_fighting = Mock()
        self.commands.fight_handler.aggressive_entry_rounds = Mock(return_value=[])
        self.commands.interp_api = SimpleNamespace(evaluate_guards_only=Mock(side_effect=lambda ctx, name: {"blocked": True} if ctx.flee_to_room is None else None))

    def test_flee_samples_missing_directions_six_times_with_replacement(self):
        self.flee_setup()
        with patch.object(Module.random, "randint", return_value=1) as rolls:
            self.assertEqual({"blocked": True}, self.commands.do_flee(self.actor, self.context))
        self.assertEqual(6, rolls.call_count)
        self.commands._flee_destination.assert_not_called()
        self.assertEqual("source", self.actor.room_id)

    def test_thief_flee_xp_exception_has_strict_boundary(self):
        for roll, charged in ((35, False), (36, True)):
            self.flee_setup()
            self.actor.character_class = SimpleNamespace(name="thief")
            with patch.object(Module.random, "randint", side_effect=[0, roll]), \
                    patch.object(Module.CharacterAdvancement, "gain_experience") as gain:
                result = self.commands.do_flee(self.actor, self.context)
            self.assertEqual(charged, gain.called)
            self.assertEqual("lost_exp" if charged else "snuckAwaySafely", result["payloads"][1]["message_key"])

    def test_npc_flee_cannot_enter_no_mob_room(self):
        self.actor.is_npc = True
        destination = SimpleNamespace(room_flags=1)
        self.commands.room_registry = SimpleNamespace(get_or_none=Mock(return_value=destination))
        self.commands._current_daze = Mock(return_value=0)
        with patch.object(Module.CharacterApi, "get_enum", side_effect=lambda name: SimpleNamespace(ROOM_NO_MOB=SimpleNamespace(value=1))):
            self.assertIsNone(self.commands._flee_destination(self.actor, self.room, SimpleNamespace(exit_flags=0)))

    def test_backstab_strict_endpoint_zero_skill_and_sleep_exception(self):
        replacements = {name: SimpleNamespace(**attrs) for name, attrs in {
            "area.RoomRegistry": {"RoomRegistry": object}, "combat.CombatHandler": {"FightHandler": object},
            "combat.CombatView": {"FightView": object}, "game.action": dict.fromkeys(("ActionGuard", "ActionDefinition", "ActionPlan", "MessageRef"), object),
            "api.SkillApi": {"SkillApi": object}, "skill.SkillRegistry": {"SkillRegistry": object},
            "util.PlayerUtil": {"PlayerUtil": object}}.items()}
        with patch.dict(sys.modules, replacements):
            spec = importlib.util.spec_from_file_location("_final_fight_api", fixtures.SRC / "api/FightApi.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        api = module.FightApi.__new__(module.FightApi)
        api.fight_handler = SimpleNamespace(multi_hit=Mock(return_value={}), damage=Mock(return_value={}), build_round_payload=Mock())
        commands = SimpleNamespace(_set_wait=Mock(), _skill_beats=Mock(return_value=12), _pre_corpse_ids=Mock(return_value=set()), _check_improve=Mock())
        for rating, roll, awake, success in ((50, 50, True, False), (50, 49, True, True), (0, 1, True, False), (1, 100, False, False), (2, 100, False, True)):
            api.fight_handler.multi_hit.reset_mock()
            view = SimpleNamespace(actor=self.actor, victim=self.victim, room=self.room, skill=object(), extra={"skill_percent": rating})
            with patch.object(module.random, "randint", return_value=roll), patch.object(module.CharacterApi, "is_awake", return_value=awake):
                api.execute_fight_plan(self.context, commands, view, SimpleNamespace(operation="backstab", data={}))
            self.assertEqual(success, api.fight_handler.multi_hit.called)


if __name__ == "__main__":
    unittest.main()
