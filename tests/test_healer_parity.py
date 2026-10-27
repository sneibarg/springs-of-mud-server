import asyncio
import unittest
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch

from tests.test_review_application_fixes import RuntimeFixture
from api.CharacterApi import CharacterApi
from api.SpellApi import SpellApi
from devtools.collection_query import load_collections
from interp.commands.Object import Object
from item.EffectHandler import EffectHandler
from item.Effect import Effect
from mobile.Mobile import Mobile
from server.handlers.ConnectionHandler import ConnectionHandler
from skill.Spell import Spell


class HealerParityTests(RuntimeFixture, unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        super().setUp()
        visible = patch.object(CharacterApi, 'can_see', return_value=True)
        visible.start()
        self.addCleanup(visible.stop)
        self.healer = Mobile.__new__(Mobile)
        self.healer.id, self.healer.name = 'healer', 'Sera'
        self.healer.short_description = 'the healer Sera'
        self.healer.sex = 'female'
        self.healer.level, self.healer.gold, self.healer.silver = 30, 0, 150
        self.healer.status_flags = NS(act=self.enums.get('actBits').ACT_IS_HEALER.value)
        self.room.mobiles[self.healer.id] = self.healer
        self.actor.gold, self.actor.silver = 100, 0
        self.actor.mana, self.actor.max_mana = 0, 100
        self.actor.character_attributes.position = self.enums.get('positions').POS_STANDING.value
        self.commands = Object.__new__(Object)
        self.commands.room_registry = self.rooms
        self.commands.act_bits = self.enums.get('actBits')
        self.commands.GameParameters = self.enums.get('gameParameters')
        self.commands.interp_api = self.api
        self.commands.fight_handler = NS(update_pos=Mock())
        self.commands.spell_api = SpellApi(EffectHandler(self.enums), self.api)
        docs = load_collections(Path(__file__).resolve().parents[1] / 'resources/collections', ['spells'])
        names = ('cure light', 'cure serious', 'cure critical', 'heal', 'refresh',
                 'cure blindness', 'cure disease', 'cure poison', 'remove curse')
        spells = []
        for record in docs['spells'].documents:
            if record['name'] in names:
                data = deepcopy(record)
                data.setdefault('levelByClass', {})
                data.setdefault('ratingByClass', {})
                spells.append(Spell.from_json(data))
        self.commands.spell_registry = NS(all_spells=lambda: spells)

    def buy(self, text):
        return self.commands.do_heal(self.actor, self.context('heal', text))

    def test_rom_service_precedence_and_prefixes(self):
        branches = [('light',), ('serious',), ('critical',), ('heal',), ('blindness',),
                    ('disease',), ('poison',), ('uncurse', 'curse'), ('mana', 'energize'), ('refresh', 'moves')]
        costs = [1000, 1600, 2500, 5000, 2000, 1500, 2500, 5000, 1000, 500]
        for aliases in branches:
            for alias in aliases:
                for size in range(1, len(alias) + 1):
                    query = alias[:size]
                    expected = next(i for i, names in enumerate(branches) if any(n.startswith(query) for n in names))
                    service = self.commands._healer_service(query)
                    self.assertEqual(costs[expected], service['cost'], query)
                    self.assertEqual(expected == 8, service.get('kind') == 'mana', query)
        for invalid in ('lightning', 'manafoo', 'criticalextra', 'movesmore'):
            self.assertIsNone(self.commands._healer_service(invalid))

    async def test_purchase_applies_configured_wait_and_input_gate(self):
        self.buy('m')
        pulses = self.enums.get('gameParameters').PULSE_VIOLENCE.value
        self.assertEqual(pulses, self.actor.status_flags.pulse_wait)
        connection = NS(is_closed=lambda: False)
        session = NS(character=self.actor, is_playing=lambda: True, is_idle=lambda: False)
        handler = ConnectionHandler.__new__(ConnectionHandler)
        task = asyncio.create_task(handler._wait_for_action_ready(connection, session))
        try:
            await asyncio.sleep(0)
            self.assertFalse(task.done())
            self.actor.status_flags.pulse_wait = 0
            self.assertTrue(await asyncio.wait_for(task, 1))
        finally:
            if not task.done():
                task.cancel()
                await asyncio.gather(task, return_exceptions=True)
        self.actor.status_flags.pulse_wait = pulses + 5
        self.buy('mana')
        self.assertEqual(pulses + 5, self.actor.status_flags.pulse_wait)
        self.commands.GameParameters = NS(PULSE_VIOLENCE=NS(value=7))
        self.actor.status_flags.pulse_wait = 0
        self.buy('mana')
        self.assertEqual(7, self.actor.status_flags.pulse_wait)

    def test_payment_preserves_denominations_and_breaks_only_needed_gold(self):
        for initial, expected in [((0, 2100), (0, 1100)), ((20, 50), (10, 50)),
                                  ((10, 1), (0, 1)), ((100, 1001), (100, 1))]:
            self.actor.gold, self.actor.silver = initial
            self.healer.gold, self.healer.silver = 0, 150
            self.buy('mana')
            self.assertEqual(expected, (self.actor.gold, self.actor.silver))
            self.assertEqual((10, 150), (self.healer.gold, self.healer.silver))

    def test_rejected_purchases_and_listing_never_charge_or_wait(self):
        for text in ('manafoo', ''):
            before = (self.actor.gold, self.actor.silver, self.healer.gold, self.healer.silver)
            response = self.buy(text)
            self.assertIn('healer Sera', response['to_char'])
            self.assertEqual(before, (self.actor.gold, self.actor.silver, self.healer.gold, self.healer.silver))
            self.assertEqual(0, self.actor.status_flags.pulse_wait)
        self.actor.gold, self.actor.silver = 0, 999
        response = self.buy('mana')
        self.assertEqual("The healer Sera says 'You do not have enough gold for my services.'\r\n", response['to_char'])
        self.assertEqual((0, 999), (self.actor.gold, self.actor.silver))
        self.assertEqual(0, self.actor.status_flags.pulse_wait)
        self.room.mobiles.clear()
        self.assertEqual("You can't do that here.\r\n", self.buy('mana')['to_char'])

    def test_incantation_includes_buyer_and_only_resting_or_higher_observers(self):
        observer, sleeper = self.character('observer'), self.character('sleeper')
        observer.character_attributes.position = self.enums.get('positions').POS_RESTING.value
        sleeper.character_attributes.position = self.enums.get('positions').POS_SLEEPING.value
        self.room.add_player_to_room(observer)
        self.room.add_player_to_room(sleeper)
        with patch.object(CharacterApi, 'can_see', side_effect=lambda viewer, target, room: viewer is self.actor):
            notice = self.buy('mana')['payloads'][0]
        self.assertEqual({self.actor.id, observer.id}, {target.id for target in notice['targets']})
        self.assertEqual("The healer Sera utters the words 'energizer'.\r\n", notice['to_room'].for_recipient(self.actor.id))
        self.assertEqual("Someone utters the words 'energizer'.\r\n", notice['to_room'].for_recipient(observer.id))

    def test_lone_buyer_gets_chant_and_visibility_applies_to_list_and_refusals(self):
        self.assertEqual([self.actor], self.buy('mana')['payloads'][0]['targets'])
        with patch.object(CharacterApi, 'can_see', return_value=False):
            listing = self.buy('')['to_char']
            self.assertTrue(listing.startswith("Someone says 'I offer the following spells:'\r\n"))
            self.assertIn('serious: cure serious wounds  15 gold', listing)
            self.assertIn('healing spell\t      50 gold', listing)
            self.assertEqual("Someone says 'Type 'heal' for a list of spells.'\r\n", self.buy('nonsense')['to_char'])

    def test_legacy_act_utterance_renders_for_visible_and_unseen_recipients(self):
        observer = self.character('observer')
        self.room.add_player_to_room(observer)
        context = self.context('heal', 'mana')
        context.command.payload.to_room['utters_words'] = "$n utters the words '$T'."
        with patch.object(CharacterApi, 'can_see', side_effect=lambda viewer, target, room: viewer is self.actor):
            notice = self.commands.do_heal(self.actor, context)['payloads'][0]
        self.assertEqual("The healer Sera utters the words 'energizer'.\r\n",
                         notice['to_room'].for_recipient(self.actor.id))
        self.assertEqual("Someone utters the words 'energizer'.\r\n",
                         notice['to_room'].for_recipient(observer.id))
        self.assertNotIn('$', str(notice['to_room']))

    def test_older_live_payload_still_lists_services_and_reports_mana_restoration(self):
        context = self.context('heal')
        context.command.payload.to_char.pop('services')
        context.command.payload.to_char.pop('warm_glow')
        result = self.commands.do_heal(self.actor, context)
        self.assertTrue(result['to_char'].startswith("The healer Sera says 'I offer the following spells:'\r\n"))
        for service in ('light:', 'serious:', 'critic:', 'heal:', 'blind:', 'disease:',
                        'poison:', 'uncurse:', 'refresh:', 'mana:'):
            self.assertIn(service, result['to_char'])
        self.assertIn('Type heal <type> to be healed.', result['to_char'])
        self.assertEqual(100, self.actor.gold)
        self.assertEqual(0, self.actor.status_flags.pulse_wait)
        context.result = 'mana'
        response = self.commands.do_heal(self.actor, context)
        self.assertEqual('A warm glow passes through you.\r\n', response['payloads'][0]['to_char'])

    def test_live_service_list_overrides_bundled_default(self):
        context = self.context('heal')
        context.command.payload.to_char['services'] = '{healer} offers custom services.'
        with patch('interp.CommandDefaults.bundled_payload', side_effect=AssertionError('unexpected fallback')):
            response = self.commands.do_heal(self.actor, context)
        self.assertEqual('The healer Sera offers custom services.\r\n', response['to_char'])

    def test_authored_restoration_spells_keep_c_values_caps_and_healer_level(self):
        for service, hit, move, mana, cost in [('light', 24, 10, 0, 10), ('serious', 33, 10, 0, 16),
                                             ('critical', 46, 10, 0, 25), ('heal', 110, 10, 0, 50),
                                             ('refresh', 10, 40, 0, 5), ('mana', 10, 10, 18, 10)]:
            self.actor.gold, self.actor.silver = 100, 0
            self.actor.hit, self.actor.max_hit = 10, 200
            self.actor.movement, self.actor.max_movement = 10, 100
            self.actor.mana = 0
            with patch('api.SpellApi.random.randint', return_value=4):
                response = self.buy(service)
            self.assertEqual((hit, move, mana), (self.actor.hit, self.actor.movement, self.actor.mana), service)
            self.assertEqual(100 - cost, self.actor.gold)
            self.assertEqual(12, self.actor.status_flags.pulse_wait)
            self.assertTrue(response['payloads'])
            if service != 'mana':
                self.assertIs(self.actor, response['payloads'][1]['victim'])
                self.assertTrue(response['payloads'][1]['to_victim'])
        self.actor.mana = 99
        self.buy('mana')
        self.assertEqual(100, self.actor.mana)

    def test_missing_spell_has_no_invented_restoration_message(self):
        self.commands.spell_registry = NS(all_spells=lambda: [])
        response = self.buy('light')
        self.assertEqual(1, len(response['payloads']))
        self.assertNotIn('to_char', response['payloads'][0])
        self.assertEqual(90, self.actor.gold)

    def test_condition_services_use_real_authored_dispels(self):
        for service, effect_name, flag in [('blind', 'blindness', 'AFF_BLIND'),
                                          ('disease', 'plague', 'AFF_PLAGUE'),
                                          ('poison', 'poison', 'AFF_POISON'),
                                          ('uncurse', 'curse', 'AFF_CURSE')]:
            with self.subTest(service=service):
                self.actor.gold = 100
                effects = self.commands.spell_api.effect_handler
                effects.affect_to_char(self.actor, Effect(where='TO_AFFECTS', type='spell.' + effect_name,
                                                        level=30, duration=5, location='APPLY_NONE',
                                                        modifier=0, bitvector=flag))
                with patch('util.EffectUtil.EffectUtil.saves_dispel', return_value=False):
                    response = self.buy(service)
                self.assertFalse(any(effect.type == 'spell.' + effect_name for effect in self.actor.effects))
                self.assertTrue(any(payload.get('to_victim') for payload in response['payloads']))


if __name__ == '__main__':
    unittest.main()
