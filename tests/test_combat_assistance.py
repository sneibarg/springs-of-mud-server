import asyncio
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch, call

from tests import test_combat_handler_aggression as fixtures

Runtime = sys.modules[fixtures.FightHandler.__module__]


class TestCombatAssistance(unittest.TestCase):
    def setUp(self):
        self.fixtures = fixtures.TestFightHandlerAggression()
        self.attacker = self.fixtures._mob("attacker")
        self.victim = self.fixtures._player("victim")
        self.helper = self.fixtures._mob("helper")
        for entity in (self.attacker, self.helper):
            entity.race, entity.group, entity.vnum = "human", "0", "100"
        self.attacker.fighting, self.victim.fighting = self.victim, self.attacker
        self.people = [self.attacker, self.victim, self.helper]
        self.room = SimpleNamespace(id="room-1", area_id="area-1", contents={},
                                    characters={self.victim.id: self.victim},
                                    people=lambda: list(self.people), players_in_room=lambda: [self.victim],
                                    player_targets=lambda actor: [self.victim] if actor is not self.victim else [],
                                    find_entity_in_room=lambda id: next((e for e in self.people if e.id == id), None))
        self.handler = self.fixtures._handler(self.room)
        self.flags = set()
        self.handler._mob_has_off = lambda entity, flag: entity is self.helper and flag in self.flags
        self.handler.rng = SimpleNamespace(number_bits=Mock(return_value=1), number_range=Mock(return_value=0))
        self.handler.multi_hit = Mock(return_value={"to_victim": "assist hit", "to_room": "others see hit"})
        self.good = patch.object(Runtime.CharacterApi, "is_good", side_effect=lambda e: getattr(e, "alignment", 0) > 350, create=True)
        self.evil = patch.object(Runtime.CharacterApi, "is_evil", side_effect=lambda e: getattr(e, "alignment", 0) < -350, create=True)
        self.neutral = patch.object(Runtime.CharacterApi, "is_neutral", side_effect=lambda e: -350 <= getattr(e, "alignment", 0) <= 350, create=True)
        for patcher in (self.good, self.evil, self.neutral):
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_npc_assist_flags_and_group_membership(self):
        for flag in ("ASSIST_ALL", "ASSIST_RACE", "ASSIST_ALIGN", "ASSIST_VNUM", "group"):
            with self.subTest(flag=flag):
                self.handler.multi_hit.reset_mock()
                self.flags.clear()
                self.attacker.group = self.helper.group = "10" if flag == "group" else "0"
                if flag != "group":
                    self.flags.add(flag)
                result = self.handler.check_assist(self.attacker, self.victim)
                self.handler.multi_hit.assert_called_once_with(self.helper, self.victim, dt="TYPE_UNDEFINED")
                self.assertEqual(2, len(result))
                self.assertIn("screams and attacks!", result[0][1]["to_room"])
                self.assertEqual("assist hit", result[1][1]["to_victim"])

    def test_mismatched_npc_attributes_and_zero_group_do_not_assist(self):
        self.helper.race, self.helper.vnum, self.helper.alignment = "elf", "101", -1000
        self.attacker.alignment = 1000
        self.flags.update(("ASSIST_RACE", "ASSIST_VNUM", "ASSIST_ALIGN"))
        self.assertEqual([], self.handler.check_assist(self.attacker, self.victim))
        self.handler.rng.number_bits.assert_not_called()
        self.handler.multi_hit.assert_not_called()

    def test_npc_half_chance_gate_and_sleep_or_existing_fight(self):
        self.flags.add("ASSIST_ALL")
        self.handler.rng.number_bits.return_value = 0
        self.assertEqual([], self.handler.check_assist(self.attacker, self.victim))
        self.handler.rng.number_range.assert_not_called()
        self.helper.fighting = self.attacker
        self.handler.rng.number_bits.reset_mock()
        self.assertEqual([], self.handler.check_assist(self.attacker, self.victim))
        self.handler.rng.number_bits.assert_not_called()
        self.helper.fighting = None
        with patch.object(Runtime.CharacterApi, "is_awake", return_value=False):
            self.assertEqual([], self.handler.check_assist(self.attacker, self.victim))

    def test_target_selection_filters_sight_and_group_and_counts_replacements(self):
        self.flags.add("ASSIST_ALL")
        allies = [self.fixtures._player(str(i)) for i in range(4)]
        self.people.extend(allies)
        candidates = [self.victim, *allies[:3]]
        self.handler.rng.number_range.side_effect = [0, 1, 1, 0]
        with patch.object(Runtime.CharacterApi, "is_same_group", side_effect=lambda a, b: any(a is c for c in candidates)), \
                patch.object(Runtime.CharacterApi, "can_see", return_value=True):
            self.handler.check_assist(self.attacker, self.victim)
        self.assertEqual([call(0, 0), call(0, 1), call(0, 1), call(0, 1)],
                         self.handler.rng.number_range.call_args_list)
        self.handler.multi_hit.assert_called_once_with(self.helper, allies[2], dt="TYPE_UNDEFINED")
        self.handler.multi_hit.reset_mock()
        with patch.object(Runtime.CharacterApi, "can_see", return_value=False):
            self.assertEqual([], self.handler.check_assist(self.attacker, self.victim))
        self.handler.multi_hit.assert_not_called()

    def test_assist_players_level_boundary_ignores_npc_sampling_gate(self):
        player = self.fixtures._player("attacker-player")
        self.people[0] = player
        self.flags.add("ASSIST_PLAYERS")
        self.helper.level = 10
        for level, expected in ((15, True), (16, False)):
            self.victim.level = level
            self.handler.multi_hit.reset_mock()
            self.handler.check_assist(player, self.victim)
            self.assertEqual(expected, self.handler.multi_hit.called)
        self.handler.rng.number_bits.assert_not_called()

    def test_group_autoassist_obeys_safety_and_preserves_attack_payload(self):
        player = self.fixtures._player("attacker-player")
        helper = self.fixtures._player("helper-player")
        self.people = [player, self.victim, helper]
        with patch.object(Runtime.CharacterApi, "player_auto_assist", return_value=True), \
                patch.object(Runtime.CharacterApi, "is_same_group", return_value=True):
            self.handler.is_safe = Mock(return_value=(True, "safe"))
            self.assertEqual([], self.handler.check_assist(player, self.victim))
            self.handler.multi_hit.assert_not_called()
            self.handler.is_safe.return_value = (False, "")
            rounds = self.handler.check_assist(player, self.victim)
        self.handler.multi_hit.assert_called_once_with(helper, self.victim, dt="TYPE_UNDEFINED")
        self.assertEqual(1, len(rounds))
        self.assertIs(helper, rounds[0][0])
        self.assertEqual("assist hit", rounds[0][1]["to_victim"])

    def test_violence_emits_assist_notices_hits_and_one_prompt(self):
        self.flags.add("ASSIST_ALL")
        self.handler.combat_registry.all_events = lambda: [SimpleNamespace(
            id="event", room_id=self.room.id, attacker_id=self.attacker.id, defender_id=self.victim.id)]
        self.handler.area_registry.get_or_none = lambda **kw: object()
        self.handler.message_bus = SimpleNamespace(text_to_message=lambda t: t, send_to_character=AsyncMock(),
                                                    send_to_room=AsyncMock(), send_prompt=AsyncMock())
        with patch.object(Runtime.Ability, "take_improve_messages", return_value="", create=True):
            asyncio.run(self.handler.violence_update())
        self.assertEqual([("victim", "assist hit"), ("victim", "assist hit")],
                         [c.args for c in self.handler.message_bus.send_to_character.await_args_list])
        self.assertEqual(2, self.handler.multi_hit.call_count)
        self.assertTrue(any("screams and attacks!" in c.args[0]
                            for c in self.handler.message_bus.send_to_room.await_args_list))
        self.handler.message_bus.send_prompt.assert_awaited_once()

    def test_earlier_player_lethal_hit_cancels_later_npc_event(self):
        player, npc = self.victim, self.attacker
        self.handler.combat_registry.all_events = lambda: [
            SimpleNamespace(id="player", room_id=self.room.id, attacker_id=player.id, defender_id=npc.id),
            SimpleNamespace(id="npc", room_id=self.room.id, attacker_id=npc.id, defender_id=player.id)]
        self.handler.combat_registry.remove_by_id = Mock()
        def lethal(actor, target, **kw):
            actor.fighting = target.fighting = None
            return {}
        self.handler.multi_hit = Mock(side_effect=lethal)
        self.handler.build_round_payload = Mock(return_value={})
        self.handler.emit_round_payload = AsyncMock(return_value=[])
        asyncio.run(self.handler.violence_update())
        self.handler.multi_hit.assert_called_once_with(player, npc, dt="TYPE_UNDEFINED")
        self.handler.combat_registry.remove_by_id.assert_called_once_with("npc")


if __name__ == "__main__":
    unittest.main()
