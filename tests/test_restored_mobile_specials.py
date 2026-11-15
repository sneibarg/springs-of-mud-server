import unittest
from collections import Counter
from dataclasses import replace
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock, call, patch

from tests.test_movement_rules_parity import MovementFixture, item
from tests.test_review_application_fixes import ROOT
from api.CharacterApi import CharacterApi
from api.MobileApi import MobileApi
from api.SpellApi import SpellApi
from area.Special import Special
from area.SpecialRegistry import SpecialRegistry
from combat.CombatHandler import FightHandler
from combat.CombatRegistry import CombatRegistry
from devtools.collection_query import load_collections
from game.Equipped import Equipped
from interp.commands.Communications import Communications
from interp.commands.Fight import Fight
from item.Effect import Effect
from item.Item import Item
from mobile.MobileHandler import MobileHandler
from skill.Spell import Spell


class RestoredSpecialTests(MovementFixture, unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        collections = load_collections(ROOT / 'resources/collections', ['specials', 'spells', 'items'])
        cls.specials = [Special.from_json(document) for document in collections['specials'].documents]
        cls.spells = [Spell.from_json(document) for document in collections['spells'].documents]
        cls.brandy_document = next(document for document in collections['items'].documents if document['vnum'] == '3601')

    def setUp(self):
        super().setUp()
        self.room.light = 1
        self.handler = MobileHandler.__new__(MobileHandler)
        self.handler.logger = Mock()
        self.handler.room_registry = self.rooms
        self.handler.registry_service = self.registries
        self.handler.wear_flags = self.enums.get('wearFlags')
        self.registries.character_registry.playing = {}
        self.handler.handler_service = None
        self.handler.special_registry = SpecialRegistry()
        for special in self.specials:
            self.handler.special_registry.register(special)
        self.handler.rng = Mock(number_bits=Mock(return_value=0), number_range=Mock(return_value=0))
        self.handler.spell_registry = NS(all_spells=lambda: self.spells)
        self.handler.skill_registry = self.skill_registry
        self.handler.spell_api = SpellApi(self.effects, self.api)
        self.handler.spell_api.elemental_exposure = NS(expose=Mock(return_value={}))
        self.handler.fight_commands = Fight.__new__(Fight)
        self.combat = Mock(spec=FightHandler, is_safe=Mock(return_value=(False, '')),
                           is_safe_spell=Mock(return_value=False), damage=Mock(return_value={}),
                           _check_immunity=Mock(return_value='IS_NORMAL'), build_round_payload=Mock(return_value={}),
                           emit_round_payload=AsyncMock())
        self.handler.fight_handler = self.combat
        self.handler.effect_handler = self.effects
        self.handler.message_bus = Mock(text_to_message=lambda text: text,
                                        send_to_character=AsyncMock(), send_to_room=AsyncMock())

    def mobile(self, vnum, special_name='', group=''):
        mob = self.npc()
        mob.id = mob.vnum = vnum
        mob.short_description = f'mobile {vnum}'
        mob.group = group
        if special_name:
            special = next(special for special in self.specials
                           if special.name == special_name and special.mob_vnum == vnum)
            mob.special_name, mob.special_function = special.name, list(special.special_function)
        self.room.add_mobile_to_room(mob)
        return mob

    def test_all_restored_assignments_have_executable_scripts(self):
        expected = {'spec_breath_any': 19, 'spec_breath_acid': 11, 'spec_cast_adept': 6,
                    'spec_cast_judge': 7, 'spec_executioner': 1, 'spec_ogre_member': 4,
                    'spec_troll_member': 4, 'spec_patrolman': 1}
        assignments = [special for special in self.specials if special.name in expected]
        self.assertEqual(expected, Counter(special.name for special in assignments))
        for special in assignments:
            with self.subTest(special=special.name, mobile=special.mob_vnum):
                self.assertTrue(special.special_function)
                self.assertTrue(all(callable(eval(step)) for step in special.special_function))

    async def test_undead_spell_weights_match_each_eligible_rom_table(self):
        records = [special for special in self.specials if special.name == 'spec_cast_undead']
        self.assertEqual(39, len(records))
        self.assertEqual(1, len({tuple(special.special_function) for special in records}))
        undead = self.mobile(records[0].mob_vnum, 'spec_cast_undead')
        undead.fighting = self.actor
        self.actor.fighting = undead
        CharacterApi.set_position(undead, 'POS_FIGHTING')
        base = {'curse': 1, 'weaken': 1, 'chill touch': 1, 'blindness': 1,
                'poison': 1, 'energy drain': 1, 'harm': 8}
        for level, expected in ((18, base), (20, {**base, 'plague': 1}),
                                (21, {**base, 'plague': 1, 'teleport': 1})):
            with self.subTest(level=level):
                undead.level = level
                total = sum(expected.values())
                with patch('api.MobileApi.random.randint', side_effect=range(1, total + 1)) as roll, \
                        patch.object(MobileApi, 'cast_spell', side_effect=lambda ctx, *a, **kw: ctx.mark_performed()) as cast:
                    for _ in range(total):
                        self.assertTrue(await self.handler.execute_special_function(undead, self.room))
                self.assertEqual([call(1, total)] * total, roll.call_args_list)
                self.assertEqual(expected, Counter(entry.args[1] for entry in cast.call_args_list))

    async def test_bundled_thief_uses_integer_half_level_as_the_percentage_cap(self):
        thief = self.mobile('6608', 'spec_thief')
        gold_and_silver_rolls = [call(1, 20), call(1, 20)]
        for level, expected_stolen in ((1, 0), (2, 1)):
            with self.subTest(level=level):
                thief.level = level
                thief.gold = thief.silver = 0
                self.actor.gold = self.actor.silver = 100
                self.handler.rng.number_range.reset_mock()
                self.handler.rng.number_range.side_effect = [1, 20, 19]

                self.assertTrue(await self.handler.execute_special_function(thief, self.room))

                self.assertEqual((expected_stolen, expected_stolen), (thief.gold, thief.silver))
                self.assertEqual((100 - expected_stolen,) * 2, (self.actor.gold, self.actor.silver))
                self.assertEqual([call(0, level), *gold_and_silver_rolls],
                                 self.handler.rng.number_range.call_args_list)
        self.handler.logger.error.assert_not_called()

    async def test_bundled_nasty_requires_fighting_posture_before_choosing_a_combat_action(self):
        nasty = self.mobile('3163', 'spec_nasty')
        self.actor.level = nasty.level  # Outside the ambush window.
        self.actor.gold = 100
        nasty.fighting = self.actor
        CharacterApi.set_position(nasty, 'POS_RESTING')

        with patch.object(MobileApi, 'choose_weighted', return_value='purse') as choose:
            self.assertFalse(await self.handler.execute_special_function(nasty, self.room))
            choose.assert_not_called()
            self.assertEqual((100, 0), (self.actor.gold, nasty.gold))
            self.handler.message_bus.send_to_character.assert_not_awaited()
            self.handler.message_bus.send_to_room.assert_not_awaited()

            CharacterApi.set_position(nasty, 'POS_FIGHTING')
            self.assertTrue(await self.handler.execute_special_function(nasty, self.room))
            choose.assert_called_once()

        self.assertEqual((90, 10), (self.actor.gold, nasty.gold))
        self.handler.logger.error.assert_not_called()

    async def test_janitor_picks_up_takeable_drinks_trash_and_items_below_ten(self):
        janitor = self.mobile('3061', 'spec_janitor')
        brandy_data = {key: value for key, value in self.brandy_document.items() if key not in {'_id', '_class'}}
        brandy = Item.from_json({**brandy_data, 'id': self.brandy_document['_id']['$oid']})
        self.assertGreaterEqual(int(brandy.cost), 10)
        trash = item('expensive trash', itemType='trash', cost=100)
        cheap = item('cheap container', cost=9)
        ineligible = [item('fountain', itemType='fountain', cost=100), item('cost cutoff', cost=10),
                      item('fixed trash', itemType='trash', wearFlags='0', cost=1)]
        for obj in reversed([*ineligible, brandy, trash, cheap]):
            self.room.add_item_to_room(obj)

        for expected in (brandy, trash, cheap):
            self.assertTrue(await self.handler.execute_special_function(janitor, self.room))
            self.assertIs(expected, janitor.inventory[-1])
        self.assertFalse(await self.handler.execute_special_function(janitor, self.room))

        self.assertEqual([brandy, trash, cheap], janitor.inventory)
        self.assertEqual(list(reversed(ineligible)), list(self.room.contents.values()))
        notices = [entry.args[0].for_recipient(self.actor.id)
                   for entry in self.handler.message_bus.send_to_room.await_args_list]
        self.assertEqual(['Mobile 3061 picks up some trash.\r\n'] * 3, notices)
        self.handler.logger.error.assert_not_called()

    async def test_janitor_leaves_owned_trash_until_the_owner_allows_looting(self):
        janitor = self.mobile('3061', 'spec_janitor')
        owner = self.character('owner')
        self.destination.add_player_to_room(owner)
        trash = item('owned trash', itemType='trash', owner=owner.name, cost=1)
        self.room.add_item_to_room(trash)

        self.assertFalse(await self.handler.execute_special_function(janitor, self.room))
        self.assertIs(trash, self.room.contents[trash.id])
        self.assertEqual([], janitor.inventory)
        self.handler.message_bus.send_to_room.assert_not_awaited()

        owner.status_flags.set_flag('act', self.enums.get('playerActBits').PLR_CANLOOT)
        self.assertTrue(await self.handler.execute_special_function(janitor, self.room))
        self.assertNotIn(trash.id, self.room.contents)
        self.assertEqual([trash], janitor.inventory)
        self.handler.logger.error.assert_not_called()

    async def test_acid_and_judge_roll_only_against_reciprocal_opponents_then_cast(self):
        for vnum, name, bits, damage_type in (
                ('2222', 'spec_breath_acid', 3, 'DAM_ACID'),
                ('8011', 'spec_cast_judge', 2, 'DAM_PIERCE')):
            with self.subTest(name=name):
                mob = self.mobile(vnum, name)
                mob.hit = 120
                mob.fighting = self.mobile('other')
                self.actor.fighting = mob
                CharacterApi.set_position(mob, 'POS_FIGHTING')
                self.handler.rng.number_bits.reset_mock(side_effect=True)
                self.handler.rng.number_bits.side_effect = [1, 0]
                self.combat.damage.reset_mock()
                self.assertFalse(await self.handler.execute_special_function(mob, self.room))
                self.combat.damage.assert_not_called()
                self.assertTrue(await self.handler.execute_special_function(mob, self.room))
                self.assertEqual([call(bits), call(bits)], self.handler.rng.number_bits.call_args_list)
                self.combat.damage.assert_called_once()
                self.assertIs(self.combat.damage.call_args.args[1], self.actor)
                self.assertEqual(damage_type, self.combat.damage.call_args.kwargs['dam_type'])
                self.handler.logger.error.assert_not_called()

    async def test_breath_any_routes_all_eight_rolls_and_gas_skips_target_roll(self):
        mob = self.mobile('2016', 'spec_breath_any')
        mob.hit = 120
        CharacterApi.set_position(mob, 'POS_FIGHTING')
        self.actor.fighting = mob
        mob.fighting = self.actor
        real_cast = self.handler.spell_api.execute_lambdas
        with patch.object(self.handler.spell_api, 'execute_lambdas', wraps=real_cast) as cast:
            for roll, spell in enumerate(('fire', 'lightning', 'lightning', 'gas', 'acid', 'frost', 'frost', 'frost')):
                with self.subTest(roll=roll):
                    self.handler.rng.number_bits.reset_mock(side_effect=True)
                    self.handler.rng.number_bits.side_effect = [roll] if spell == 'gas' else [roll, 0]
                    self.assertTrue(await self.handler.execute_special_function(mob, self.room))
                    context = cast.call_args.args[0]
                    self.assertEqual(f'{spell} breath', context.spell.name)
                    if spell == 'gas':
                        self.assertEqual([call(3)], self.handler.rng.number_bits.call_args_list)
                        self.assertEqual('room', context.target_kind)
                        self.assertIsNone(context.target)
                    else:
                        self.assertIs(context.target, self.actor)
        self.handler.logger.error.assert_not_called()

    async def test_adept_rolls_before_level_filter_and_cure_disease_leaves_pulse_available(self):
        mob = self.mobile('3012', 'spec_cast_adept')
        eligible = self.follower('student')
        eligible.level = 10
        self.room.remove_player_from_room(self.actor)
        self.room.add_player_to_room(self.actor)
        plague = Effect(type='spell.plague', level=1, duration=3, bitvector='AFF_PLAGUE')
        self.effects.affect_to_char(eligible, plague)
        with patch('util.EffectUtil.random.randint', return_value=100):
            self.handler.rng.number_bits.side_effect = [0, 0, 6]
            self.assertFalse(await self.handler.execute_special_function(mob, self.room))
        self.assertEqual([call(1), call(1), call(4)], self.handler.rng.number_bits.call_args_list)
        self.assertNotIn(plague, eligible.effects)
        self.handler.rng.number_bits.side_effect = [0, 0, 15]
        self.assertFalse(await self.handler.execute_special_function(mob, self.room))
        self.handler.rng.number_bits.side_effect = [0, 0, 0]
        self.assertTrue(await self.handler.execute_special_function(mob, self.room))
        self.assertTrue(any(effect.type == 'spell.armor' for effect in eligible.effects))
        self.handler.logger.error.assert_not_called()

    async def test_saved_poison_bite_delivers_bite_and_resisted_notices(self):
        mob = self.mobile('8309', 'spec_poison')
        observer = self.follower('observer')
        mob.fighting = self.actor
        CharacterApi.set_position(mob, 'POS_FIGHTING')
        self.handler.rng.number_percent.return_value = 1
        self.combat._check_immunity.return_value = 'IS_IMMUNE'

        self.assertTrue(await self.handler.execute_special_function(mob, self.room))

        self.assertEqual([
            call(self.actor.id, 'mobile 8309 bites you!\r\n'),
            call(self.actor.id, 'You feel momentarily ill, but it passes.\r\n'),
        ], self.handler.message_bus.send_to_character.await_args_list)
        room_notices = self.handler.message_bus.send_to_room.await_args_list
        self.assertEqual([observer], room_notices[0].args[1])
        self.assertEqual('Mobile 8309 bites actor!\r\n', room_notices[0].args[0].for_recipient(observer.id))
        self.assertEqual(call('actor turns slightly green, but it passes.\r\n', [observer]), room_notices[1])
        self.assertEqual(2, len(room_notices))
        self.assertFalse(any(effect.type == 'spell.poison' for effect in self.actor.effects))
        self.handler.logger.error.assert_not_called()

    async def test_saved_bundled_mage_spell_skips_pulse_fallback(self):
        mage = self.mobile('1000', 'spec_cast_mage')
        mage.level = 1  # Only blindness is eligible in the bundled table.
        mage.fighting = self.actor
        self.actor.fighting = mage
        CharacterApi.set_position(mage, 'POS_FIGHTING')
        self.combat._check_immunity.return_value = 'IS_IMMUNE'
        self.handler.act_bits = self.enums.get('actBits')
        self.handler.area_registry = NS(get_or_none=lambda **_: None)
        self.handler._update_shop_money = Mock()
        self.handler._execute_generic_special = AsyncMock()

        await self.handler.mobile_update()

        self.combat._check_immunity.assert_called_once()
        self.assertFalse(any(effect.type == 'spell.blindness' for effect in self.actor.effects))
        self.handler._update_shop_money.assert_not_called()
        self.handler._execute_generic_special.assert_not_awaited()
        self.handler.logger.error.assert_not_called()

    async def test_missing_spell_target_and_script_error_leave_pulse_available(self):
        mob = self.mobile('1000', 'spec_cast_mage')
        mob.fighting = self.actor
        broken = replace(next(spell for spell in self.spells if spell.name == 'blindness'), name='broken spell', lambdas=[
            "lambda ctx: ctx.send(to_victim='incomplete cast')",
            'lambda ctx: ctx.mark_performed()',
            'lambda ctx: 1 / 0',
        ])
        self.handler.spell_registry = NS(all_spells=lambda: [broken])
        with patch.object(self.handler.spell_api, 'logger') as spell_logger:
            for step in (
                    "lambda ctx: ctx.cast_spell('missing spell', target=ctx.actor.fighting)",
                    "lambda ctx: ctx.cast_spell('broken spell')",
                    "lambda ctx: ctx.cast_spell('broken spell', target=ctx.actor.fighting)"):
                with self.subTest(step=step):
                    mob.special_function = [step]
                    self.assertFalse(await self.handler.execute_special_function(mob, self.room))
            spell_logger.error.assert_called_once()
        self.handler.message_bus.send_to_character.assert_not_awaited()
        self.handler.message_bus.send_to_room.assert_not_awaited()
        self.handler.logger.error.assert_not_called()

    async def test_executioner_uses_yell_rules_and_attacks_first_visible_criminal(self):
        mob = self.mobile('3011', 'spec_executioner')
        second = self.follower('killer')
        first = self.follower('thief')
        flags = self.enums.get('playerActBits')
        first.status_flags.set_flag('act', flags.PLR_THIEF)
        second.status_flags.set_flag('act', flags.PLR_KILLER)
        quiet = self.follower('quiet')
        sleeping = self.follower('sleeping')
        comm = self.enums.get('commFlags')
        mob.status_flags.set_flag('comm', comm.COMM_NOSHOUT)
        quiet.status_flags.set_flag('comm', comm.COMM_QUIET)
        CharacterApi.set_position(sleeping, 'POS_SLEEPING')
        yell = Communications.__new__(Communications)
        yell.interp_api, yell.room_registry, yell.comm_flags = self.api, self.rooms, comm
        yell.session_handler = NS(get_playing_sessions=lambda: [NS(character=entity) for entity in self.room.players_in_room()])
        self.handler.player_handler = NS(communications_commands=yell, _emit_standard_payload=AsyncMock())
        self.assertTrue(await self.handler.execute_special_function(mob, self.room))
        self.assertFalse(mob.status_flags.comm & comm.COMM_NOSHOUT)
        self.combat.multi_hit.assert_called_once_with(mob, first, dt='TYPE_UNDEFINED')
        self.combat.set_fighting.assert_not_called()
        payload = self.handler.player_handler._emit_standard_payload.await_args.args[1]['payloads'][0]
        self.assertNotIn(quiet, payload['global_targets'])
        self.assertNotIn(sleeping, payload['global_targets'])
        self.assertIn('yells', payload['global_message'].for_recipient(first.id))
        self.assertIn('thief is a THIEF!', payload['global_message'].for_recipient(first.id))
        self.handler.logger.error.assert_not_called()

    async def test_guard_criminal_branch_finishes_even_when_damage_is_blocked(self):
        guards = [special for special in self.specials if special.name == 'spec_guard']
        self.assertEqual(24, len(guards))
        self.assertEqual(1, len({tuple(special.special_function) for special in guards}))
        guard = self.mobile('3060', 'spec_guard')
        self.actor.status_flags.set_flag('act', self.enums.get('playerActBits').PLR_THIEF)
        fighter = self.follower('fighter')
        fighter.character_attributes.alignment = -500
        fighter.fighting = self.follower('opponent')
        self.handler.run_special_yell = Mock(return_value=False)
        self.combat.multi_hit.return_value = {'to_char': 'Not in this room.\r\n', 'damage_applied': 0}

        self.assertTrue(await self.handler.execute_special_function(guard, self.room))

        self.handler.run_special_yell.assert_called_once()
        self.combat.multi_hit.assert_called_once_with(guard, self.actor, dt='TYPE_UNDEFINED')
        self.combat.set_fighting.assert_not_called()
        self.handler.logger.error.assert_not_called()

    async def test_guard_fallback_requires_alignment_below_300_and_picks_lowest(self):
        guard = self.mobile('3060', 'spec_guard')
        self.actor.fighting = self.follower('opponent')
        self.actor.character_attributes.alignment = 300
        self.handler.run_special_yell = Mock()
        self.assertFalse(await self.handler.execute_special_function(guard, self.room))

        lowest = self.follower('lowest')
        lowest.character_attributes.alignment = -400
        lowest.fighting = self.actor.fighting
        other = self.follower('other')
        other.character_attributes.alignment = -100
        other.fighting = self.actor.fighting
        self.assertTrue(await self.handler.execute_special_function(guard, self.room))

        self.handler.run_special_yell.assert_not_called()
        self.combat.multi_hit.assert_called_once_with(guard, lowest, dt='TYPE_UNDEFINED')
        self.handler.logger.error.assert_not_called()

    async def test_guard_first_swing_uses_stunned_posture_without_linking_combat(self):
        guard = self.mobile('3060', 'spec_guard')
        victim = self.actor
        victim.status_flags.set_flag('act', self.enums.get('playerActBits').PLR_THIEF)
        victim.hit = 0
        CharacterApi.set_position(victim, 'POS_STUNNED')
        self.handler.run_special_yell = Mock(return_value=True)

        fight = FightHandler.__new__(FightHandler)
        fight.PositionsEnum = self.enums.get('positions')
        fight.WeaponClass = self.enums.get('weaponClass')
        fight.AffectBits = self.enums.get('affectedBy')
        fight.combat_registry = CombatRegistry()
        fight.effect_handler = self.effects
        fight.room_registry = NS(get=self.rooms.get_or_none, get_or_none=self.rooms.get_or_none)
        fight.logger = Mock()
        fight._wielded_weapon = Mock(return_value=None)
        fight._attack_verb = Mock(return_value='hit')
        fight._attack_damage_type = Mock(return_value='DAM_BASH')
        fight._weapon_skill_total = Mock(return_value=50)
        fight._thac0 = Mock(return_value=15)
        fight._victim_ac_for_damage_type = Mock(return_value=0)
        # Roll 10 hits with the stunned posture modifiers and misses at fighting posture.
        fight._to_hit_roll = Mock(return_value=10)
        fight._attack_damage = Mock(return_value=5)
        fight.is_safe = Mock(return_value=(False, ''))
        fight.check_killer = Mock(return_value={})
        fight._apply_damage = Mock(return_value={'damage_applied': 5})
        fight.build_round_payload = Mock(return_value={})
        fight.emit_round_payload = AsyncMock()
        self.handler.fight_handler = fight

        self.assertTrue(await self.handler.execute_special_function(guard, self.room))

        fight._apply_damage.assert_called_once()
        fight.is_safe.assert_called_once_with(guard, victim)
        self.assertEqual(5, fight._apply_damage.call_args.args[2])
        self.assertEqual(CharacterApi.pos_value('POS_STUNNED'), CharacterApi.position_value(victim))
        self.assertIsNone(guard.fighting)
        self.assertIsNone(victim.fighting)
        self.handler.logger.error.assert_not_called()

    async def test_gang_rivals_sample_eligible_targets_and_stop_for_patrolman(self):
        for vnum, name, group, rival_group in (
                ('2101', 'spec_troll_member', '2100', '2101'),
                ('2102', 'spec_ogre_member', '2101', '2100')):
            with self.subTest(name=name):
                mob = self.mobile(vnum, name, group)
                strong = self.mobile('strong', group=rival_group)
                strong.level = mob.level + 2
                rival = self.mobile('rival', group=rival_group)
                patrolman = self.mobile('2106')
                self.assertFalse(await self.handler.execute_special_function(mob, self.room))
                self.combat.multi_hit.assert_not_called()
                self.room.remove_mobile_from_room(patrolman)
                self.assertTrue(await self.handler.execute_special_function(mob, self.room))
                self.combat.multi_hit.assert_called_once_with(mob, rival, dt='TYPE_UNDEFINED')
                self.room.remove_mobile_from_room(mob)
                self.room.remove_mobile_from_room(rival)
                self.room.remove_mobile_from_room(strong)
                self.combat.multi_hit.reset_mock()
        self.handler.logger.error.assert_not_called()

    async def test_patrolman_targets_opponent_on_tie_and_announces_whistle_across_area(self):
        mob = self.mobile('2106', 'spec_patrolman')
        opponent = self.mobile('opponent')
        opponent.level = self.actor.level
        self.actor.fighting = opponent
        whistle = item('brass whistle', vnum='2116')
        mob.equipped = Equipped()
        mob.equip_item(whistle, 'neck2')
        remote_listener = self.character('remote')
        self.destination.area_id = self.room.area_id
        self.destination.add_player_to_room(remote_listener)

        opponent.special_name = 'spec_patrolman'
        self.assertFalse(await self.handler.execute_special_function(mob, self.room))
        self.handler.message_bus.send_to_room.assert_not_awaited()
        opponent.special_name = ''
        performed = await self.handler.execute_special_function(mob, self.room)
        self.handler.logger.error.assert_not_called()
        self.assertTrue(performed)
        self.combat.multi_hit.assert_called_once_with(mob, opponent, dt='TYPE_UNDEFINED')
        self.handler.message_bus.send_to_room.assert_any_await(
            'You hear a shrill whistling sound.\r\n', [remote_listener])

        mob.unequip_item('neck2')
        self.combat.multi_hit.reset_mock()
        self.handler.message_bus.send_to_room.reset_mock()
        self.assertTrue(await self.handler.execute_special_function(mob, self.room))
        self.combat.multi_hit.assert_called_once_with(mob, opponent, dt='TYPE_UNDEFINED')
        self.assertNotIn(call('You hear a shrill whistling sound.\r\n', [remote_listener]),
                         self.handler.message_bus.send_to_room.await_args_list)
        self.handler.logger.error.assert_not_called()
