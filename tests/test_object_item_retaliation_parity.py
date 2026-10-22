"""ROM obj_cast_spell post-cast retaliation, including resisted item spells."""
import unittest
from types import SimpleNamespace as NS
from unittest.mock import Mock
from tests import test_object_container_shop_spell_parity as fixtures


class TestItemSpellRetaliationParity(unittest.TestCase):
    def setUp(self):
        self.base = fixtures.TestObjectContainerShopSpellParity()
        self.base.setUp()
        self.addCleanup(self.base.doCleanups)
        self.actor, self.room, self.commands = self.base.actor, self.base.room, self.base.commands
        self.victim = self.base.fixture._build_character(name="Victim")
        self.victim.id, self.victim.room_id = "victim", self.room.id
        self.actor.room_id = self.room.id
        self.room.characters = {self.actor.id: self.actor, self.victim.id: self.victim}
        self.commands.fight_handler = NS(is_safe=Mock(return_value=(False, "")),
            is_safe_spell=Mock(return_value=False), check_killer=Mock(return_value={"to_char": "killer"}),
            multi_hit=Mock(return_value={"hit": True}), build_round_payload=Mock(return_value={"to_char": "attack"}))
        self.fight = self.commands.fight_handler
        self.spell = self.base.base.spell("test")
        self.spell.target = "CHAR_OFFENSIVE"
        self.spell.lambdas = ["lambda ctx: False"]
        self.commands.spell_api.start_offensive_combat = Mock()

    def cast(self):
        return self.commands._cast_item_spell(self.actor, self.room, self.base.item(value0="15"),
            self.spell, target=self.victim, command_context=self.base.fixture._build_context("", self.room, self.actor, "zap"))

    def test_resisted_or_no_effect_spell_immediately_retaliates_without_cast_starter(self):
        payload = self.cast()
        self.fight.check_killer.assert_called_once_with(self.victim, self.actor)
        self.fight.multi_hit.assert_called_once_with(self.victim, self.actor, dt="TYPE_UNDEFINED")
        self.fight.build_round_payload.assert_called_once_with(self.victim, self.actor, self.room, {"hit": True})
        self.assertIs(self.victim, payload[-1]["actor"])
        self.assertEqual([{"to_char": "killer"}, {"to_char": "attack"}], payload[-1]["payloads"])
        self.commands.spell_api.start_offensive_combat.assert_not_called()

    def test_non_damage_offensive_effect_retaliates_after_spell_payload(self):
        self.spell.lambdas = ["lambda ctx: ctx.queue_payload({'to_char': 'spell'})", "lambda ctx: ctx.mark_performed()"]
        payload = self.cast()
        self.assertEqual({"to_char": "spell"}, payload[0])
        self.fight.multi_hit.assert_called_once()

    def test_departed_or_extracted_victim_does_not_retaliate(self):
        self.spell.lambdas = ["lambda ctx: ctx.room.characters.pop(ctx.target.id)"]
        self.cast()
        self.fight.check_killer.assert_not_called()
        self.fight.multi_hit.assert_not_called()

    def test_follower_self_busy_and_defensive_targets_do_not_retaliate(self):
        for reason in ("follower", "self", "busy", "defensive"):
            with self.subTest(reason=reason):
                self.victim.master = self.actor if reason == "follower" else None
                self.victim.fighting = self.actor if reason == "busy" else None
                self.spell.target = "CHAR_DEFENSIVE" if reason == "defensive" else "CHAR_OFFENSIVE"
                previous = self.victim
                if reason == "self":
                    self.victim = self.actor
                self.cast()
                self.victim = previous
                self.fight.multi_hit.assert_not_called()
                self.fight.check_killer.assert_not_called()

    def test_caster_departure_uses_current_room_instead_of_stale_cast_room(self):
        self.spell.lambdas = ["lambda ctx: setattr(ctx.actor, 'room_id', 'elsewhere')"]
        self.cast()
        self.fight.multi_hit.assert_not_called()

    def test_obj_char_off_retaliates_only_for_character_target(self):
        self.spell.target = "OBJ_CHAR_OFF"
        self.cast()
        self.fight.multi_hit.assert_called_once()
        self.fight.multi_hit.reset_mock()
        self.victim = self.base.item()
        self.cast()
        self.fight.multi_hit.assert_not_called()

    def test_retaliation_that_starts_fighting_prevents_repeat_attacks_from_later_item_spells(self):
        self.fight.multi_hit.side_effect = lambda victim, actor, **kwargs: setattr(victim, "fighting", actor) or {}
        self.cast()
        self.cast()
        self.fight.multi_hit.assert_called_once()
        self.fight.check_killer.assert_called_once()

    def test_unsafe_spell_never_executes_or_retaliates(self):
        self.fight.is_safe.return_value = (True, "safe")
        self.spell.lambdas = ["lambda ctx: ctx.queue_payload({'to_char': 'unexpected'})"]
        payload = self.cast()
        self.assertNotIn({"to_char": "unexpected"}, payload)
        self.fight.multi_hit.assert_not_called()


if __name__ == "__main__":
    unittest.main()
