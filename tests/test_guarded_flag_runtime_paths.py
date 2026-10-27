import sys
import unittest
from enum import IntEnum
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from api.CharacterApi import CharacterApi
from area.Room import Room
from combat.CombatHandler import FightHandler
from game.GamePayload import GamePayload
from game.StatusFlags import StatusFlags
from game.WizHandler import WizHandler
from interp.Context import Context
from interp.PromptFormat import PromptFormat
from interp.commands.Wiz import Wiz
from mobile.Mobile import Mobile
from player.Character import Character
from server.connection.ConnectionManager import ConnectionManager
from server.session.SessionHandler import SessionHandler


class Positions(IntEnum):
    POS_DEAD = 0
    POS_FIGHTING = 7
    POS_STANDING = 8


class TestGuardedFlagRuntimePaths(unittest.TestCase):
    @staticmethod
    def entity(entity_id, *, npc=False):
        entity = (Mobile if npc else Character).__new__(Mobile if npc else Character)
        entity.id = entity_id
        entity.name = entity_id
        entity.short_description = entity_id
        entity.room_id = "room"
        entity.status_flags = StatusFlags.default()
        entity.character_attributes = SimpleNamespace(position=Positions.POS_FIGHTING)
        entity.context = {}
        entity.fighting = None
        return entity

    def test_invisible_attack_clears_only_invisibility_before_applying_damage(self):
        actor, victim = self.entity("attacker"), self.entity("victim")
        actor.status_flags.assign_bitfield("affected_by", 2 | 128)
        room = Room(id="room")
        room.add_player_to_room(actor)
        room.add_player_to_room(victim)
        handler = FightHandler.__new__(FightHandler)
        handler.AffectBits = SimpleNamespace(AFF_INVISIBLE=SimpleNamespace(value=2))
        handler.PositionsEnum = Positions
        handler.effect_handler = Mock()
        handler.spell_registry = SimpleNamespace(get_or_none=lambda **_: SimpleNamespace(
            payload=GamePayload.from_json({"toRoom": {"reveal": "{victim} appears."}})))
        handler._find_room_for_entity = Mock(return_value=room)
        handler.is_safe = Mock(return_value=(False, ""))
        handler.check_killer = Mock(return_value={})
        handler._set_fighting = Mock()

        def apply_damage(*_):
            self.assertEqual(128, actor.status_flags.affected_by)
            return {"damage_applied": 1}

        handler._apply_damage = Mock(side_effect=apply_damage)
        result = handler.damage(actor, victim, 1)
        self.assertEqual(1, result["damage_applied"])
        self.assertEqual(["spell.invis", "spell.mass_invis"],
                         [call.args[1] for call in handler.effect_handler.affect_strip.call_args_list])
        self.assertEqual("attacker appears.\r\n", result["pre_damage_payloads"][0]["to_room"])
        self.assertEqual([victim], result["pre_damage_payloads"][0]["targets"])
        with self.assertRaises(AttributeError):
            actor.status_flags.affected_by = 2

    def test_switch_and_return_preserve_session_bindings_and_guarded_flags(self):
        original, target = self.entity("original"), self.entity("body", npc=True)
        original.status_flags.assign_bitfield("comm", 8192 | 2048)
        target.status_flags.assign_bitfield("comm", 1)
        target.status_flags.assign_bitfield("act", 4)
        original.prompt_format = PromptFormat.default()
        original.carriage_return = False
        sessions, connections = SessionHandler(), ConnectionManager()
        session = sessions.create_session("session")
        session.character = original
        connections.bind_character(original.id, session.session_id)
        handler = WizHandler(SimpleNamespace(room_registry=None), sessions, connections)

        self.assertIs(original, handler.switch_character(original, target))
        self.assertIs(target, session.character)
        self.assertTrue(connections.owns_character(target.id, session.session_id))
        self.assertFalse(connections.owns_character(original.id, session.session_id))
        self.assertIs(original, target.context["controller_original"])
        self.assertEqual(original.status_flags.comm, target.status_flags.comm)
        self.assertEqual(4, target.status_flags.act)
        self.assertEqual(original.prompt_format, target.prompt_format)
        self.assertIsNot(original.prompt_format, target.prompt_format)
        self.assertFalse(target.carriage_return)

        returned, body = handler.return_character(target)
        self.assertIs(original, returned)
        self.assertIs(target, body)
        self.assertIs(original, session.character)
        self.assertTrue(connections.owns_character(original.id, session.session_id))
        self.assertFalse(connections.owns_character(target.id, session.session_id))
        self.assertNotIn("controller_original", target.context)
        self.assertNotIn("switched_original", session.metadata)
        self.assertEqual(8192 | 2048, original.status_flags.comm)
        with self.assertRaises(AttributeError):
            target.status_flags.comm = 0

    def test_peace_stops_every_combatant_without_clearing_other_flags(self):
        actor = self.entity("immortal")
        mobiles = [self.entity("first", npc=True), self.entity("second", npc=True)]
        actor.status_flags.assign_bitfield("act", 2 | 4)
        room = Room(id="room")
        room.add_player_to_room(actor)
        for mobile in mobiles:
            mobile.status_flags.assign_bitfield("act", 2 | 4)
            mobile.fighting = actor
            room.add_mobile_to_room(mobile)
        actor.fighting = mobiles[0]
        commands = Wiz.__new__(Wiz)
        commands.room_registry = SimpleNamespace(get_or_none=lambda **_: room)
        commands.ActBitsEnum = SimpleNamespace(ACT_AGGRESSIVE=SimpleNamespace(value=2))
        context = Context(character=actor, room=room)
        with patch.object(CharacterApi, "positions", Positions, create=True):
            payload = commands.do_peace(actor, context)
        self.assertTrue(context.done)
        self.assertEqual("Ok.\r\n", payload["to_char"])
        for entity in [actor, *mobiles]:
            self.assertIsNone(entity.fighting)
            self.assertEqual(Positions.POS_STANDING, entity.character_attributes.position)
        self.assertEqual(2 | 4, actor.status_flags.act)
        for mobile in mobiles:
            self.assertEqual(4, mobile.status_flags.act)

    def test_mobile_flag_removals_support_all_existing_domain_aliases(self):
        domains = {"act": "act", "affect": "affected_by", "off": "off", "imm": "imm",
                   "res": "res", "vulnerability": "vuln", "form": "form", "parts": "parts"}
        for domain, field in domains.items():
            with self.subTest(domain=domain):
                flags = StatusFlags.default()
                flags.assign_bitfield(field, 2 | 4)
                flags.assign_bitfield("comm", 8)
                StatusFlags.apply_flag_removes(flags, [{"domain": domain.upper(), "vector": "2"},
                                                      {"domain": "unknown", "vector": "4"}])
                self.assertEqual(4, getattr(flags, field))
                self.assertEqual(8, flags.comm)
                with self.assertRaises(AttributeError):
                    setattr(flags, field, 0)


if __name__ == "__main__":
    unittest.main()
