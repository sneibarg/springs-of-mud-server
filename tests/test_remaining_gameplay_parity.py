import unittest
from itertools import product
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch

from tests.test_movement_rules_parity import MovementFixture, item
from api.CharacterApi import CharacterApi
from api.FightApi import FightApi
from api.MobileApi import MobileApi
from api.SpellApi import SpellApi
from combat.CombatHandler import FightHandler
from devtools.collection_query import load_collections
from interp.commands.Fight import Fight
from item.Effect import Effect
from mobile.MobileContext import MobileContext
from mobile.MobileHandler import MobileHandler
from skill.Spell import Spell
from skill.SpellContext import SpellContext
from util.EffectUtil import EffectUtil


class RemainingGameplayTests(MovementFixture, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from tests.test_review_application_fixes import ROOT
        data = load_collections(ROOT / 'resources/collections', ['spells', 'specials'])
        cls.spell_documents = {d['name']: d for d in data['spells'].documents}
        cls.nasty_steps = next(d['specialFunction'] for d in data['specials'].documents
                              if d['name'] == 'spec_nasty')

    def setUp(self):
        super().setUp()
        self.spell_api = SpellApi(self.effects, self.api)
        self.spell_handler = NS(spell_api=self.spell_api, room_registry=self.rooms,
                                registry_service=self.registries)
        self.combat = FightHandler.__new__(FightHandler)
        self.combat.ActBits = self.enums.get('actBits')
        self.combat.MobImmunity = self.enums.get('mobImmunity')
        self.combat.MobResistance = self.enums.get('mobResistance')
        self.combat.MobVulnerability = self.enums.get('mobVulnerability')
        self.combat._current_hitroll = lambda entity: 0

    def test_permanent_dispel_adds_five_levels_and_preserves_roll_boundaries(self):
        for duration, boundary in ((-1, 75), (5, 50)):
            for roll in (boundary - 1, boundary):
                with self.subTest(duration=duration, roll=roll), \
                        patch('util.EffectUtil.random.randint', return_value=roll):
                    self.assertEqual(roll < boundary, EffectUtil.saves_dispel(20, 20, duration))

    def test_dispel_bounds_still_clamp(self):
        for caster, spell, boundary in ((100, 1, 5), (1, 100, 95)):
            for roll in (boundary - 1, boundary):
                with self.subTest(caster=caster, roll=roll), \
                        patch('util.EffectUtil.random.randint', return_value=roll):
                    self.assertEqual(roll < boundary, EffectUtil.saves_dispel(caster, spell, -1))

    def test_permanent_sanctuary_resists_then_weakens_then_dispels(self):
        effect = self.effects.affect_to_char(self.actor, Effect(type='spell.sanctuary',
            level=20, duration=-1, bitvector='AFF_SANCTUARY'))
        with patch('util.EffectUtil.random.randint', return_value=60):
            self.assertFalse(self.effects.check_dispel(20, self.actor, 'spell.sanctuary'))
        self.assertEqual(19, effect.level)
        self.assertTrue(CharacterApi.is_affected(self.actor, self.enums.get('affectedBy').AFF_SANCTUARY))
        with patch('util.EffectUtil.random.randint', return_value=70):
            self.assertTrue(self.effects.check_dispel(20, self.actor, 'spell.sanctuary'))
        self.assertFalse(CharacterApi.is_affected(self.actor, self.enums.get('affectedBy').AFF_SANCTUARY))

    def test_permanent_sanctuary_raw_flag_uses_same_resistance_bonus(self):
        self.flag(self.actor, 'AFF_SANCTUARY')
        ctx = self.spell_context('dispel magic')
        ctx.set_target(self.actor)
        with patch('util.EffectUtil.random.randint', return_value=60):
            self.assertFalse(self.spell_api.dispel_flag(ctx, 'AFF_SANCTUARY', 'spell.sanctuary'))
        with patch('util.EffectUtil.random.randint', return_value=75):
            self.assertTrue(self.spell_api.dispel_flag(ctx, 'AFF_SANCTUARY', 'spell.sanctuary'))

    def test_npc_backstab_hit_proficiency_matches_activation_with_daze_and_clamp(self):
        mob = self.npc()
        mob.status_flags.set_flag('act', self.combat.ActBits.ACT_THIEF)
        for level, daze, expected in ((1, 0, 22), (20, 0, 60), (20, 1, 40), (50, 0, 100), (50, 1, 80)):
            with self.subTest(level=level, daze=daze):
                mob.level, mob.status_flags.pulse_daze = level, daze
                normal = self.combat._thac0(mob, 'TYPE_HIT', 100)
                self.assertEqual(expected, self.skill_api.get_rating(mob, self.skills['backstab']))
                self.assertEqual(normal - 10 * (100 - expected), self.combat._thac0(mob, 'backstab', 100))

    def test_non_thief_npc_backstab_still_has_zero_proficiency(self):
        mob = self.npc()
        self.assertEqual(0, self.combat._skill_percent(mob, 'backstab'))

    def test_specific_defense_precedence_for_all_flag_combinations(self):
        mob = self.npc()
        for imm, res, vuln in product((False, True), repeat=3):
            with self.subTest(immune=imm, resistant=res, vulnerable=vuln):
                mob.status_flags.assign_bitfield('imm', int(self.combat.MobImmunity.IMM_FIRE) if imm else 0)
                mob.status_flags.assign_bitfield('res', int(self.combat.MobResistance.RES_FIRE) if res else 0)
                mob.status_flags.assign_bitfield('vuln', int(self.combat.MobVulnerability.VULN_FIRE) if vuln else 0)
                expected = 'IS_IMMUNE' if imm else 'IS_RESISTANT' if res else 'IS_VULNERABLE' if vuln else 'IS_NORMAL'
                self.assertEqual(expected, self.combat._check_immunity(mob, 'DAM_FIRE'))

    def test_specific_flags_override_general_defenses_but_none_damage_is_normal(self):
        mob = self.npc()
        mob.status_flags.set_flag('imm', self.combat.MobImmunity.IMM_MAGIC)
        self.assertEqual('IS_IMMUNE', self.combat._check_immunity(mob, 'DAM_FIRE'))
        mob.status_flags.set_flag('vuln', self.combat.MobVulnerability.VULN_FIRE)
        self.assertEqual('IS_VULNERABLE', self.combat._check_immunity(mob, 'DAM_FIRE'))
        self.assertEqual('IS_NORMAL', self.combat._check_immunity(mob, 'DAM_NONE'))

    def test_spell_saves_respect_immunity_and_resistance_over_vulnerability(self):
        mob = self.npc()
        mob.level = 20
        mob.status_flags.set_flag('vuln', self.combat.MobVulnerability.VULN_FIRE)
        mob.status_flags.set_flag('imm', self.combat.MobImmunity.IMM_FIRE)
        self.assertTrue(EffectUtil.saves_spell(20, mob, 'DAM_FIRE',
            immunity=self.combat._check_immunity, roll=lambda: 99))
        mob.status_flags.unset_flag('imm', self.combat.MobImmunity.IMM_FIRE)
        mob.status_flags.set_flag('res', self.combat.MobResistance.RES_FIRE)
        self.assertTrue(EffectUtil.saves_spell(20, mob, 'DAM_FIRE',
            immunity=self.combat._check_immunity, roll=lambda: 50))

    def world_member(self, name, room, identifier):
        mob = self.npc()
        mob.id, mob.name, mob.room_id, mob.level = identifier, name, room.id, 1
        room.add_mobile_to_room(mob)
        return mob

    def spell_context(self, name='summon', target='guard'):
        return SpellContext(actor=self.actor, spell=Spell.from_json(self.spell_documents[name]),
                            handler=self.spell_handler, room=self.room, target_name=target)

    def test_world_lookup_prefers_local_match_and_supports_self(self):
        remote = self.world_member('guard', self.destination, 'remote')
        local = self.world_member('guard', self.room, 'local')
        self.world = [self.destination, self.room, self.temple]
        self.assertIs(local, self.spell_api.find_world_target(self.spell_context()))
        self.assertIs(self.actor, self.spell_api.find_world_target(self.spell_context(target='self')))

    def test_world_lookup_counts_ordinals_across_rooms(self):
        self.world_member('guard', self.destination, 'first')
        second = self.world_member('guard', self.temple, 'second')
        self.assertIs(second, self.spell_api.find_world_target(self.spell_context(target='2.guard')))

    def test_world_lookup_skips_invisible_and_retired_targets(self):
        hidden = self.world_member('guard', self.destination, 'hidden')
        self.flag(hidden, 'AFF_INVISIBLE')
        retired = self.character('guard')
        retired.id, retired.room_id, retired.world_retired = 'retired', self.destination.id, True
        self.destination.add_player_to_room(retired)
        visible = self.world_member('guard', self.temple, 'visible')
        self.assertIs(visible, self.spell_api.find_world_target(self.spell_context()))
        self.assertIsNone(self.spell_api.find_world_target(self.spell_context(target='missing')))

    def test_actual_world_spell_documents_reach_their_operations(self):
        self.world_member('guard', self.destination, 'guard')
        self.actor.trust = int(self.enums.get('gameParameters').LEVEL_IMMORTAL)
        for name in ('summon', 'gate', 'portal', 'nexus'):
            with self.subTest(spell=name), patch.object(self.spell_api, 'saves_spell', return_value=False), \
                    patch.object(self.spell_api, 'move_to', return_value=True) as move, \
                    patch.object(self.spell_api, 'create_portals', return_value=True) as portals:
                ctx = self.spell_context(name)
                self.spell_api.execute_lambdas(ctx)
                self.assertFalse(ctx.failed)
                (portals if name in ('portal', 'nexus') else move).assert_called_once()

    def test_world_spell_missing_target_fails_normally(self):
        ctx = self.spell_context(target='missing')
        self.spell_api.execute_lambdas(ctx)
        self.assertTrue(ctx.done)
        self.assertNotIn('fizzles', str(ctx.payloads))

    def test_world_spells_relocate_and_create_portals_with_real_operations(self):
        self.actor.trust = int(self.enums.get('gameParameters').LEVEL_IMMORTAL)
        self.registries.item_registry = NS(get_or_none=lambda **kw: item('portal', itemType='portal'))
        for name in ('summon', 'gate', 'portal', 'nexus'):
            with self.subTest(spell=name):
                self.room.characters.clear()
                self.destination.characters.clear()
                self.room.mobiles.clear()
                self.destination.mobiles.clear()
                self.actor.room_id = self.room.id
                self.room.add_player_to_room(self.actor)
                target = self.world_member('guard', self.destination, 'guard')
                self.room.contents.clear()
                self.destination.contents.clear()
                ctx = self.spell_context(name)
                with patch.object(self.spell_api, 'saves_spell', return_value=False):
                    self.assertTrue(self.spell_api.execute_lambdas(ctx))
                self.assertFalse(ctx.failed)
                if name == 'summon':
                    self.assertIs(target, self.room.mobiles['guard'])
                    self.assertNotIn('guard', self.destination.mobiles)
                elif name == 'gate':
                    self.assertIs(self.actor, self.destination.characters[self.actor.id])
                    self.assertNotIn(self.actor.id, self.room.characters)
                else:
                    portal = next(iter(self.room.contents.values()))
                    self.assertEqual(self.destination.vnum, portal.value3)
                    self.assertGreater(portal.timer, 0)
                    if name == 'nexus':
                        self.assertEqual(self.room.vnum, next(iter(self.destination.contents.values())).value3)

    def test_trusted_mortal_conditions_and_lamp_keep_ticking(self):
        self.actor.trust = int(self.enums.get('gameParameters').LEVEL_IMMORTAL)
        self.actor.status_flags.hunger = self.actor.status_flags.thirst = 10
        self.actor.status_flags.drunk = 12
        lamp = item('lamp', itemType='light', value2='3')
        self.actor.equip_item(lamp, 'light')
        self.actor.tick_conditions()
        self.actor.tick_light_source(self.room)
        self.assertEqual((9, 9, 11, 2), (self.actor.status_flags.hunger,
            self.actor.status_flags.thirst, self.actor.status_flags.drunk, int(lamp.value2)))
        self.actor.gain_condition('hunger', -2)
        self.assertEqual(7, self.actor.status_flags.hunger)

    def test_actual_immortal_tick_exemption_uses_level_even_with_low_trust(self):
        self.actor.level = int(self.enums.get('gameParameters').LEVEL_IMMORTAL)
        self.actor.trust = 1
        self.actor.status_flags.hunger = 10
        lamp = item('lamp', itemType='light', value2='3')
        self.actor.equip_item(lamp, 'light')
        self.actor.tick_conditions()
        self.actor.tick_light_source(self.room)
        self.actor.gain_condition('hunger', -2)
        self.assertEqual((10, 3), (self.actor.status_flags.hunger, int(lamp.value2)))

    def setup_nasty(self):
        self.mob = self.world_member('thief', self.room, 'thief')
        self.mob.level = 10
        self.mob.status_flags.set_flag('act', self.enums.get('actBits').ACT_THIEF)
        self.actor.level = 15
        self.actor.hit = self.actor.max_hit
        self.mob.equip_item(item('dagger', itemType='weapon', value0='2', value1='1', value2='4'), 'wielded')
        def begin(actor, victim, *args, **kwargs):
            actor.fighting, victim.fighting = victim, actor
            CharacterApi.set_position(actor, 'POS_FIGHTING')
            CharacterApi.set_position(victim, 'POS_FIGHTING')
            return {}
        def stop(actor, both):
            victim = actor.fighting
            actor.fighting = None
            if both and victim is not None:
                victim.fighting = None
        self.fight = NS(is_safe=Mock(return_value=(False, '')), check_killer=Mock(return_value={}),
            multi_hit=Mock(side_effect=begin), damage=Mock(side_effect=begin), set_fighting=Mock(side_effect=begin),
            stop_fighting=Mock(side_effect=stop), aggressive_entry_rounds=lambda *args: [],
            _merge_attack_payloads=lambda notice, result: result,
            build_round_payload=lambda actor, victim, room, result, *args: result)
        self.fight.WeaponClass = self.enums.get('weaponClass')
        self.movement.fight_handler = self.fight
        self.commands = Fight.__new__(Fight)
        self.commands.fight_handler, self.commands.interp_api = self.fight, self.api
        self.commands.fight_api = FightApi(self.rooms, self.skill_registry, self.skill_api, self.fight)
        self.commands.room_registry, self.commands.skill_registry = self.rooms, self.skill_registry
        self.commands.movement_commands = self.movement
        self.commands.AffectBits = self.enums.get('affectedBy')
        self.handler = MobileHandler.__new__(MobileHandler)
        self.handler.registry_service, self.handler.fight_commands = self.registries, self.commands
        self.ctx_nasty = MobileContext(self.mob, self.room, self.handler)

    def test_nasty_uses_backstab_command_and_does_not_take_combat_turn_same_pulse(self):
        self.setup_nasty()
        with patch('api.FightApi.random.randint', return_value=1), \
                patch.object(MobileApi, 'choose_weighted') as choose:
            for source in self.nasty_steps:
                eval(source)(self.ctx_nasty)
                if self.ctx_nasty.done:
                    break
        self.fight.multi_hit.assert_called_once_with(self.mob, self.actor, dt='backstab')
        self.assertGreater(self.mob.status_flags.pulse_wait, 0)
        self.assertEqual('backstab', self.ctx_nasty.payloads[0]['context'].command.name)
        choose.assert_not_called()

    def test_nasty_falls_back_to_murder_when_backstab_prerequisite_fails(self):
        self.setup_nasty()
        self.mob.unequip_item('wielded')
        MobileApi.nasty_opening_attack(self.ctx_nasty, (1, 9), ['backstab', 'murder'])
        self.assertEqual(['backstab', 'murder'], [p['context'].command.name for p in self.ctx_nasty.payloads])
        self.fight.multi_hit.assert_called_once_with(self.mob, self.actor, dt='TYPE_UNDEFINED')

    def test_nasty_keeps_combat_after_missed_backstab_without_murder_fallback(self):
        self.setup_nasty()
        with patch('api.FightApi.random.randint', return_value=100):
            MobileApi.nasty_opening_attack(self.ctx_nasty, (1, 9), ['backstab', 'murder'])
        self.fight.damage.assert_called_once_with(self.mob, self.actor, 0, dt='backstab')
        self.assertEqual(1, len(self.ctx_nasty.payloads))
        self.fight.multi_hit.assert_not_called()

    def test_nasty_flee_moves_and_stops_both_combat_links(self):
        self.setup_nasty()
        self.fight.multi_hit(self.mob, self.actor)
        with patch.object(MobileApi, 'choose_weighted', return_value='flee'), \
                patch('interp.commands.Fight.random.randint', return_value=0):
            MobileApi.nasty_combat_turn(self.ctx_nasty)
        self.assertEqual(self.destination.id, self.mob.room_id)
        self.assertIsNone(self.mob.fighting)
        self.assertIsNone(self.actor.fighting)
        self.fight.stop_fighting.assert_called_once_with(self.mob, both=True)
        self.assertEqual('flee', self.ctx_nasty.payloads[0]['context'].command.name)

    def test_nasty_failed_flee_preserves_combat(self):
        self.setup_nasty()
        self.fight.multi_hit(self.mob, self.actor)
        self.room.exits = []
        with patch.object(MobileApi, 'choose_weighted', return_value='flee'):
            MobileApi.nasty_combat_turn(self.ctx_nasty)
        self.assertEqual(self.room.id, self.mob.room_id)
        self.assertIs(self.actor, self.mob.fighting)
        self.fight.stop_fighting.assert_not_called()

    def test_nasty_purse_and_idle_preserve_their_existing_behavior(self):
        self.setup_nasty()
        self.fight.multi_hit(self.mob, self.actor)
        self.actor.gold, self.mob.gold = 100, 0
        with patch.object(MobileApi, 'choose_weighted', return_value='purse'):
            self.assertTrue(MobileApi.nasty_combat_turn(self.ctx_nasty))
        self.assertEqual((90, 10), (self.actor.gold, self.mob.gold))
        with patch.object(MobileApi, 'choose_weighted', return_value='idle'):
            self.assertFalse(MobileApi.nasty_combat_turn(self.ctx_nasty))
        self.fight.stop_fighting.assert_not_called()


if __name__ == '__main__':
    unittest.main()
