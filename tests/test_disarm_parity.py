import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from tests import test_bash_parity as bash

Module = bash.Module


class TestDisarmParity(unittest.TestCase):
    def setUp(self):
        fixture = bash.TestBashParity()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.commands, self.actor, self.victim = fixture.commands, fixture.actor, fixture.victim
        self.skill, self.room, self.context = fixture.skill, fixture.room, fixture.context
        self.actor.character_attributes.dexterity = 20
        self.victim.character_attributes.strength = 15
        self.weapon, self.other = object(), object()
        self.actor.equipped = SimpleNamespace(wielded=self.weapon)
        self.victim.equipped = SimpleNamespace(wielded=self.other)
        self.commands.skill_api.get_rating.side_effect = None
        self.commands.skill_api.get_rating.return_value = 80
        self.commands._check_improve = Mock()
        self.commands.fight_api.build_fight_view.return_value.extra = {}

    def test_three_weapon_proficiencies_and_signed_contest_rounding(self):
        self.commands.fight_handler._weapon_skill_total = Mock(side_effect=[80, 70, 91])
        # 80*60/100 + trunc((50/2-71)/2) +20-30 = 15.
        self.assertEqual(15, self.commands._disarm_chance(self.actor, self.victim, self.skill,
                                                        self.weapon, self.other, 100))
        self.assertEqual([(self.actor, self.weapon), (self.actor, self.other), (self.victim, self.other)],
                         [c.args for c in self.commands.fight_handler._weapon_skill_total.call_args_list])

    def test_unarmed_scaling_precedes_weapon_contest_stats_and_level(self):
        self.commands.fight_handler._weapon_skill_total = Mock(side_effect=[70, 90])
        self.actor.level += 3
        self.assertEqual(6, self.commands._disarm_chance(self.actor, self.victim, self.skill, None, self.other, 60))

    def test_exact_chance_fails_and_success_uses_existing_transition(self):
        self.commands._disarm_chance = Mock(return_value=30)
        self.commands.fight_handler.check_killer = Mock(return_value={})
        self.commands._disarm_payload = Mock(return_value={"success": True})
        with patch.object(Module.random, "randint", return_value=30):
            self.commands.do_disarm(self.actor, self.context)
        self.commands._disarm_payload.assert_not_called()
        self.assertEqual(13, self.actor.status_flags.pulse_wait)
        with patch.object(Module.random, "randint", return_value=29):
            self.commands.do_disarm(self.actor, self.context)
        self.commands._disarm_payload.assert_called_once_with(self.actor, self.victim, self.room, self.other)

    def transfer_setup(self, *, npc=True, flags=0, wait=0):
        self.victim.is_npc = npc
        self.victim.name = "Defender"
        self.victim.status_flags.pulse_wait = wait
        self.item = SimpleNamespace(name="blade", short_description="a blade", extra_flags=flags)
        self.inventory, self.floor = [], []
        self.victim.equipped.wielded = self.item
        self.victim.unequip_item = Mock(side_effect=lambda slot: setattr(self.victim.equipped, slot, None))
        self.victim.remove_item = Mock(side_effect=lambda item: self.inventory.remove(item) if item in self.inventory else None)
        self.victim.add_item = Mock(side_effect=lambda item: self.inventory.append(item))
        self.room.add_item_to_room = Mock(side_effect=lambda item: self.floor.append(item))
        self.room.remove_item_from_room = Mock(side_effect=lambda item: self.floor.remove(item))
        self.room.player_targets = lambda actor: [self.actor]
        self.commands.effect_handler = SimpleNamespace(remove_item_effects=Mock())
        self.commands.registry_service = SimpleNamespace(interp_registry=SimpleNamespace(
            get_or_none=Mock(return_value=SimpleNamespace(name="get"))))
        flags_enum = SimpleNamespace(ITEM_NOREMOVE=SimpleNamespace(value=1), ITEM_NODROP=SimpleNamespace(value=2),
                                     ITEM_INVENTORY=SimpleNamespace(value=4))
        patchers = [patch.object(Module.CharacterApi, "get_enum", return_value=flags_enum),
                    patch.object(Module.GameApi, "is_set", side_effect=lambda value, bit: bool(value & bit), create=True),
                    patch.object(Module.ItemApi, "can_see_object", return_value=True, create=True),
                    patch.object(Module.ItemApi, "item_takeable", return_value=True, create=True)]
        for patcher in patchers:
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_npc_recovers_dropped_visible_weapon_without_equipping(self):
        self.transfer_setup()
        payload = self.commands._disarm_payload(self.actor, self.victim, self.room, self.item)
        self.assertIsNone(self.victim.equipped.wielded)
        self.assertEqual([self.item], self.inventory)
        self.assertEqual([], self.floor)
        self.commands.effect_handler.remove_item_effects.assert_called_once_with(self.victim, self.item)
        action = payload["payloads"][1]
        self.assertIs(self.victim, action["actor"])
        self.assertEqual("get", action["context"].command.name)
        self.assertEqual("default", action["payloads"][0]["message_key"])

    def test_player_and_waiting_npc_do_not_retrieve(self):
        for npc, wait in ((False, 0), (True, 1)):
            self.transfer_setup(npc=npc, wait=wait)
            self.commands._disarm_payload(self.actor, self.victim, self.room, self.item)
            self.assertEqual([self.item], self.floor)
            self.assertEqual([], self.inventory)

    def test_no_remove_and_retained_inventory_flags(self):
        for flag in (1, 2, 4):
            self.transfer_setup(flags=flag)
            self.commands._disarm_payload(self.actor, self.victim, self.room, self.item)
            self.assertEqual([], self.floor)
            if flag == 1:
                self.assertIs(self.item, self.victim.equipped.wielded)
                self.commands.effect_handler.remove_item_effects.assert_not_called()
            else:
                self.assertEqual([self.item], self.inventory)
                self.assertIsNone(self.victim.equipped.wielded)

    def test_unseen_or_untakeable_weapon_stays_on_floor(self):
        for visible, takeable in ((False, True), (True, False)):
            self.transfer_setup()
            with patch.object(Module.ItemApi, "can_see_object", return_value=visible), \
                    patch.object(Module.ItemApi, "item_takeable", return_value=takeable):
                self.commands._disarm_payload(self.actor, self.victim, self.room, self.item)
            self.assertEqual([self.item], self.floor)
            self.assertEqual([], self.inventory)


if __name__ == "__main__":
    unittest.main()
