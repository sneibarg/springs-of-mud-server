import unittest
from types import SimpleNamespace as NS
from unittest.mock import Mock

from tests.test_movement_rules_parity import MovementFixture
from api.CharacterApi import CharacterApi
from combat.CombatHandler import FightHandler
from interp.commands.Info import Info
from util.PlayerUtil import PlayerUtil


class RoomDisplayConsiderTests(MovementFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.target = self.follower('Target')
        self.combat = FightHandler.__new__(FightHandler)
        for name, key in (('PositionsEnum', 'positions'), ('RoomFlags', 'roomFlags'),
                          ('ActBits', 'actBits'), ('AffectBits', 'affectedBy'),
                          ('PlayerActBits', 'playerActBits')):
            setattr(self.combat, name, self.enums.get(key))
        self.combat.shop_registry = NS(find_by_keeper_vnum=lambda vnum: None)
        self.info = Info.__new__(Info)
        self.info.room_registry = self.rooms
        self.info.interp_api = self.api

    def consider(self, selector):
        context = self.ctx('consider', selector)
        context.handler_service = NS(get_handler=lambda name: NS(fight_handler=self.combat))
        return self.info.do_consider(self.actor, context)

    def test_room_markers_use_act_and_ignore_afk_and_other_comm_bits(self):
        bits = self.enums.get('playerActBits')
        self.target.status_flags.assign_bitfield('comm', 0)
        self.target.status_flags.assign_bitfield('act', int(bits.PLR_KILLER) | int(bits.PLR_THIEF))
        line = self.room.get_players_in_room(self.actor)
        self.assertIn('(KILLER)', line)
        self.assertIn('(THIEF)', line)
        self.target.status_flags.assign_bitfield('act', 0)
        self.target.status_flags.assign_bitfield('comm', int(bits.PLR_KILLER) | int(bits.PLR_THIEF))
        line = self.room.get_players_in_room(self.actor)
        self.assertNotIn('(KILLER)', line)
        self.assertNotIn('(THIEF)', line)
        npc = self.npc()
        npc.status_flags.assign_bitfield('act', int(bits.PLR_KILLER) | int(bits.PLR_THIEF))
        self.assertNotIn('(KILLER)', PlayerUtil.format_visible_character_line(self.actor, npc))
        self.assertNotIn('(THIEF)', PlayerUtil.format_visible_character_line(self.actor, npc))

    def test_fighting_room_line_conceals_unseen_opponent(self):
        hidden = self.character('SecretImmortal')
        hidden.room_id = self.room.id
        hidden.status_flags.invis_level = 60
        self.target.fighting = hidden
        CharacterApi.set_position(self.target, 'POS_FIGHTING')
        self.assertFalse(CharacterApi.can_see(self.actor, hidden, self.room))
        line = self.room.get_players_in_room(self.actor)
        self.assertIn('fighting someone.', line)
        self.assertNotIn(hidden.name, line)

    def test_fighting_line_uses_npc_short_description_and_special_branches(self):
        npc = self.npc()
        npc.room_id = self.room.id
        npc.name = 'guard city sentinel'
        npc.short_description = 'a city guard'
        CharacterApi.set_position(self.target, 'POS_FIGHTING')
        for opponent, expected in ((npc, 'fighting a city guard.'),
                                   (self.actor, 'fighting YOU!'), (None, 'fighting thin air??')):
            self.target.fighting = opponent
            self.assertIn(expected, self.room.get_players_in_room(self.actor))
        npc.room_id = self.destination.id
        self.target.fighting = npc
        self.assertIn('someone who left??', self.room.get_players_in_room(self.actor))

    def test_consider_rejects_safe_room_and_protected_npcs(self):
        npc = self.npc()
        npc.name = 'guard'
        npc.level = 1
        self.room.add_mobile_to_room(npc)
        for protection in ('safe', 'shop', 'ACT_TRAIN', 'ACT_PRACTICE', 'ACT_IS_HEALER', 'ACT_IS_CHANGER'):
            with self.subTest(protection=protection):
                self.room.room_flags = int(self.enums.get('roomFlags').ROOM_SAFE) if protection == 'safe' else 0
                self.combat.shop_registry.find_by_keeper_vnum = lambda vnum: object() if protection == 'shop' else None
                npc.status_flags.assign_bitfield('act', int(getattr(self.enums.get('actBits'), protection))
                                                   if protection.startswith('ACT_') else 0)
                output = self.consider('guard')
                self.assertIn("Don't even think about it.", output)
                self.assertNotIn('naked and weaponless', output)
        self.room.room_flags = 0
        npc.status_flags.assign_bitfield('act', 0)
        self.assertIn('naked and weaponless', self.consider('guard'))

    def test_consider_preserves_safety_exceptions(self):
        npc = self.npc()
        npc.name = 'guard'
        npc.level = 1
        self.room.add_mobile_to_room(npc)
        self.room.room_flags = int(self.enums.get('roomFlags').ROOM_SAFE)
        npc.fighting = self.actor
        self.assertIn('naked and weaponless', self.consider('guard'))
        npc.fighting = None
        self.actor.level = int(self.enums.get('gameParameters').LEVEL_IMMORTAL) + 1
        self.assertIn('naked and weaponless', self.consider('guard'))

    def test_consider_guards_run_before_safety_lookup(self):
        self.combat.is_safe = Mock(side_effect=AssertionError('must not run'))
        self.assertIn('Consider killing whom?', self.consider(''))
        self.assertIn("They're not here.", self.consider('missing'))
        self.combat.is_safe.assert_not_called()
