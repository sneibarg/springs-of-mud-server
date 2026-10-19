import asyncio
import json
import sys
import unittest
from enum import IntEnum
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from tests import test_combat_handler_aggression as fixtures

Runtime = sys.modules[fixtures.FightHandler.__module__]
ROOT = Path(__file__).resolve().parents[1]


class Bits(IntEnum):
    AFF_SLEEP = 1
    AFF_INVISIBLE = 2
    AFF_SANCTUARY = 4
    AFF_PROTECT_EVIL = 8
    AFF_PROTECT_GOOD = 16


class TestCombatStateEffects(unittest.TestCase):
    def setUp(self):
        self.fixtures = fixtures.TestFightHandlerAggression()
        self.actor, self.victim, self.handler = self.fixtures._killer_pair()
        self.room = self.fixtures._safety_room(self.actor, self.victim)
        self.room.id = "room-1"
        self.room.player_targets = lambda actor: [self.victim] if actor is self.actor else [self.actor]
        self.handler.room_registry.get_or_none = Mock(return_value=self.room)
        self.handler.room_registry.get = Mock(return_value=self.room)
        self.handler._find_room_for_entity = Mock(return_value=self.room)
        self.handler.AffectBits = Bits

    def test_entering_combat_strips_sleep_once_before_setting_fighting(self):
        self.actor.status_flags.affected_by = int(Bits.AFF_SLEEP)
        def strip(entity, kind):
            self.assertIsNone(entity.fighting)
            self.assertEqual("spell.sleep", kind)
            entity.status_flags.affected_by &= ~int(Bits.AFF_SLEEP)
        self.handler.effect_handler.affect_strip.side_effect = strip
        self.handler.set_fighting(self.actor, self.victim, self.room.id)
        self.handler.set_fighting(self.actor, self.victim, self.room.id)
        self.handler.effect_handler.affect_strip.assert_called_once_with(self.actor, "spell.sleep")
        self.assertIs(self.actor.fighting, self.victim)
        self.assertEqual(fixtures._Positions.POS_FIGHTING, self.actor.character_attributes.position)

    def reveal_setup(self):
        document = next(doc for doc in json.loads((ROOT / "resources/collections/SOMDB.Spells.json").read_text())
                        if doc["name"] == "invisibility")
        self.assertEqual("spell.invis", document["handlerId"])
        payload = Runtime.GamePayload.from_json(document["payload"])
        self.handler.spell_registry = SimpleNamespace(get_or_none=Mock(return_value=SimpleNamespace(payload=payload)))
        self.actor.name = "Attacker"
        self.actor.status_flags.affected_by = int(Bits.AFF_INVISIBLE) | 128
        self.handler.is_safe = Mock(return_value=(False, ""))
        self.handler.check_killer = Mock(return_value={})
        self.handler._set_fighting = Mock()
        self.handler._apply_damage = Mock(return_value={"to_char": "hit", "killed": False})

    def test_zero_and_self_damage_reveal_before_damage_and_clear_raw_flag(self):
        for self_damage in (False, True):
            self.reveal_setup()
            self.handler.effect_handler.affect_strip.reset_mock()
            self.handler._apply_damage.side_effect = lambda *args: self.assertFalse(
                self.actor.status_flags.affected_by & int(Bits.AFF_INVISIBLE)) or {"to_char": "hit"}
            result = self.handler.damage(self.actor, self.actor if self_damage else self.victim, 0)
            self.assertEqual(128, self.actor.status_flags.affected_by)
            self.assertEqual(["spell.invis", "spell.mass_invis"],
                             [c.args[1] for c in self.handler.effect_handler.affect_strip.call_args_list])
            self.assertEqual("Attacker fades into existence.\r\n", result["pre_damage_payloads"][0]["to_room"])
            self.assertEqual([self.victim], result["pre_damage_payloads"][0]["targets"])

    def test_safety_rejection_does_not_reveal(self):
        self.reveal_setup()
        self.handler.is_safe.return_value = (True, "safe")
        self.handler.damage(self.actor, self.victim, 10)
        self.assertTrue(self.actor.status_flags.affected_by & int(Bits.AFF_INVISIBLE))
        self.handler.effect_handler.affect_strip.assert_not_called()

    def test_reveal_emits_before_hit_and_reaches_victim(self):
        self.reveal_setup()
        result = self.handler.damage(self.actor, self.victim, 0)
        self.handler._append_condition_line = lambda text, target: text
        payload = self.handler.build_round_payload(self.actor, self.victim, self.room, result)
        delivered = []
        self.handler.message_bus = SimpleNamespace(text_to_message=lambda text: text,
            send_to_room=AsyncMock(side_effect=lambda text, targets: delivered.append((text, targets))),
            send_to_character=AsyncMock(side_effect=lambda id, text: delivered.append((id, text))))
        asyncio.run(self.handler.emit_round_payload(self.actor, payload))
        self.assertEqual(("Attacker fades into existence.\r\n", [self.victim]), delivered[0])
        self.assertEqual((self.actor.id, "hit"), delivered[1])

    def test_unconscious_damage_stops_only_victims_outgoing_combat_before_escape(self):
        for hp, expected in ((0, fixtures._Positions.POS_STUNNED), (-3, fixtures._Positions.POS_INCAP),
                              (-6, fixtures._Positions.POS_MORTAL)):
            with self.subTest(hp=hp):
                self.actor.fighting, self.victim.fighting = self.victim, self.actor
                self.victim.level, self.victim.hit = 10, hp + 1
                self.victim.status_flags.drunk = 0
                self.handler.is_safe = Mock(return_value=(False, ""))
                self.handler.check_killer = Mock(return_value={})
                self.handler._set_fighting = Mock()
                self.handler._check_immunity = Mock(return_value="IS_NORMAL")
                self.handler.dam_message = Mock(return_value={})
                incoming = SimpleNamespace(id="incoming", attacker_id=self.actor.id)
                outgoing = SimpleNamespace(id="outgoing", attacker_id=self.victim.id)
                self.handler.combat_registry.get_by_combatant.return_value = [incoming, outgoing]
                self.handler.combat_registry.remove_by_id.reset_mock()
                def escape(*args):
                    self.assertIsNone(self.victim.fighting)
                    return []
                self.handler.escape_handler = SimpleNamespace(after_damage=Mock(side_effect=escape))
                with patch.object(Runtime.CharacterApi, "is_awake", side_effect=lambda e: e.character_attributes.position > 4):
                    self.handler.damage(self.actor, self.victim, 1)
                self.assertIsNone(self.victim.fighting)
                self.assertIs(self.actor.fighting, self.victim)
                self.assertEqual(expected, self.victim.character_attributes.position)
                self.handler.combat_registry.remove_by_id.assert_called_once_with("outgoing")

    def test_recovery_to_positive_hp_stands_even_with_stale_fighting_pointer(self):
        self.victim.hit = 1
        self.victim.fighting = self.actor
        self.victim.character_attributes.position = fixtures._Positions.POS_STUNNED
        self.handler.update_pos(self.victim)
        self.assertEqual(fixtures._Positions.POS_STANDING, self.victim.character_attributes.position)

    def test_reveal_notices_survive_attack_merges_and_precede_spell_hit(self):
        from tests.test_weapon_hit_effects import WeaponHitHandler
        first, second = {"to_room": "reveal1"}, {"to_room": "reveal2"}
        for merge in (Runtime.FightHandler._merge_attack_payloads, WeaponHitHandler._merge):
            result = merge({"pre_damage_payloads": [first]}, {"pre_damage_payloads": [second]})
            self.assertEqual([first, second], result["pre_damage_payloads"])
        api = self.fixtures._spell_api_class()(effect_handler=Mock(), interp_api=Mock())
        order = []
        api.send = Mock(side_effect=lambda *args, **kwargs: order.append("hit"))
        context = SimpleNamespace(queue_payload=lambda payload: order.append(payload))
        api._queue_damage_payload(context, {"pre_damage_payloads": [first]}, self.victim)
        self.assertEqual([first, "hit"], order)


if __name__ == "__main__":
    unittest.main()
