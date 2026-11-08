"""Regressions derived from the October 31 ROM24 review's five findings."""
import unittest
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock, patch

from tests import test_speech_text_parity as speech
from tests.test_movement_rules_parity import MovementFixture, item
from api.CharacterApi import CharacterApi
from api.SpellApi import SpellApi
from game.EntityUpdateHandler import EntityUpdateHandler
from interp.commands.Info import Info
from util.InterpUtil import InterpUtil
from mobile.MobileFactory import MobileFactory
from mobile.Dice import Dice
from skill.SpellContext import SpellContext
from skill.SpellSpeech import SpellSpeech


class PublicInputTests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        speech.SpeechTextTests.setUpClass()

    def setUp(self):
        self.fixture = f = speech.SpeechTextTests()
        f.setUp()
        self.addCleanup(f.doCleanups)
        commands = {name: f.command(name) for name in f.documents}
        registry = NS(get_or_none=lambda **kw: commands.get(kw.get('name')),
                      all_commands=lambda: list(commands.values()))
        f.registries.interp_registry = registry
        f.interpreter.interp_registry = registry
        f.interpreter.social_registry = NS(get_or_none=lambda **kw: None)
        f.interpreter.command_not_found_message = f.bus.text_to_message('Huh?\r\n')
        f.interpreter.logger, f.interpreter.command_audit = Mock(), None

    async def test_spacing_survives_public_interpreter_and_real_delivery(self):
        f = self.fixture
        await f.interpreter.handle_command(f.actor, '  SAY\thello   brave\tworld')
        self.assertEqual(["Alice says 'hello   brave\tworld'\r\n"], f.messages(f.bob))

    async def test_punctuation_without_space_and_with_space(self):
        f = self.fixture
        for token in ("'", '.'):
            for separator in ('', ' '):
                with self.subTest(token=token, separator=separator):
                    for connection in f.connections.values():
                        connection.send_message.reset_mock()
                    await f.interpreter.handle_command(f.actor, token + separator + 'hello   world')
                    self.assertTrue(f.messages(f.bob))
                    self.assertIn('hello   world', f.messages(f.bob)[0])
                    self.assertNotIn('Huh?', ''.join(f.messages(f.actor)))

    def test_other_punctuation_routes_preserve_body(self):
        for token in (',', ';'):
            command, body = InterpUtil.extract_parameters(self.fixture.interpreter.interp_registry,
                                                          token + 'hello   world')
            self.assertEqual(token, command.name)
            self.assertEqual('hello   world', body)

    async def test_alias_and_prefix_keep_interior_body_spacing(self):
        f = self.fixture
        f.actor.aliases = {'chat': 'say'}
        await f.interpreter.handle_command(f.actor, 'chat hello   world')
        self.assertIn('hello   world', f.messages(f.bob)[0])
        f.actor.context['prefix'] = 'say'
        await f.interpreter.handle_command(f.actor, 'hello   again')
        self.assertIn('hello   again', f.messages(f.bob)[-1])

    async def test_stored_description_keeps_spacing(self):
        f = self.fixture
        handler = f.interpreter.handler_service.get_handler('ph')
        handler.info_commands = Info.__new__(Info)
        await f.interpreter.handle_command(f.actor, 'description Two   spaces remain.')
        self.assertEqual('Two   spaces remain.\r\n', f.actor.description)


    async def test_description_removes_only_the_last_line(self):
        f = self.fixture
        handler = f.interpreter.handler_service.get_handler('ph')
        handler.info_commands = Info.__new__(Info)
        f.actor.description = 'First line.\r\n\r\nLast line.\r\n'
        await f.interpreter.handle_command(f.actor, 'description -')
        self.assertEqual('First line.\r\n\r\n', f.actor.description)
        await f.interpreter.handle_command(f.actor, 'description -')
        self.assertEqual('First line.\r\n', f.actor.description)


class RuntimeParityTests(MovementFixture, unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        super().setUp()
        self.actor.name = 'Alice'
        self.bob, self.cara = self.follower('Bob'), self.follower('Cara')
        self.actor.character_class.name = self.bob.character_class.name = 'mage'
        self.cara.character_class.name = 'cleric'

    def announcements(self, target=None, name='armor'):
        api = SpellApi.__new__(SpellApi)
        ctx = SpellContext(actor=self.actor, spell=NS(name=name), handler=NS(), room=self.room,
                           target=target or self.actor, target_kind='char')
        api.queue_cast_announcement(ctx)
        output = {}
        for payload in ctx.payloads:
            if 'to_victim' in payload:
                output.setdefault(payload['victim'].id, []).append(payload['to_victim'])
            for observer in payload.get('targets', []):
                output.setdefault(observer.id, []).append(payload['to_room'])
        return ctx, output

    def test_invisible_caster_names_and_translation_are_recipient_specific(self):
        self.flag(self.actor, 'AFF_INVISIBLE')
        self.flag(self.cara, 'AFF_DETECT_INVIS')
        self.assertFalse(CharacterApi.can_see(self.bob, self.actor, self.room))
        _, output = self.announcements()
        self.assertEqual(["Someone utters the words, 'armor'.\r\n"], output[self.bob.id])
        self.assertEqual([SpellSpeech.utterance('armor', 'Alice', translated=True)], output[self.cara.id])

    def test_direct_victim_sees_only_visible_name_and_gets_one_notice(self):
        self.flag(self.actor, 'AFF_INVISIBLE')
        _, output = self.announcements(target=self.bob)
        self.assertEqual(["Someone utters the words, 'armor'.\r\n"], output[self.bob.id])
        self.assertEqual(1, len(output[self.cara.id]))
        self.flag(self.bob, 'AFF_DETECT_INVIS')
        _, output = self.announcements(target=self.bob)
        self.assertEqual(["Alice utters the words, 'armor'.\r\n"], output[self.bob.id])

    def test_wizinvis_and_sleeping_observers(self):
        self.actor.status_flags.invis_level = 60
        self.assertFalse(CharacterApi.can_see(self.bob, self.actor, self.room))
        _, output = self.announcements()
        self.assertIn('Someone utters', output[self.bob.id][0])
        self.bob.set_position(CharacterApi.pos_value('POS_SLEEPING'))
        self.cara.set_position(CharacterApi.pos_value('POS_SLEEPING'))
        _, output = self.announcements(target=self.bob)
        self.assertEqual({}, output)

    def test_ventriloquate_does_not_announce(self):
        context, output = self.announcements(name='ventriloquate')
        self.assertEqual([], context.payloads)
        self.assertEqual({}, output)

    def test_fallback_attack_selector_reaches_each_rom_attack(self):
        for roll, expected in ((0, 3), (1, 7), (2, 11)):
            with self.subTest(roll=roll), patch('mobile.MobileFactory.rng.number_range', return_value=roll) as rng:
                self.assertEqual(expected, MobileFactory._random_dam_type())
                rng.assert_called_once_with(0, 2)

    def test_spawn_uses_fallback_only_without_an_authored_attack(self):
        prototype = self.npc()
        prototype.hit_dice = prototype.mana_dice = prototype.damage_dice = Dice(1, 4, 0)
        prototype.origin_area_id = 'runtime-origin'
        for attack, expected in (('', 7), ('none', 7), ('slash', 'slash')):
            with self.subTest(attack=attack), patch.object(MobileFactory, '_random_dam_type', return_value=7) as fallback:
                prototype.dam_type = attack
                mobile = MobileFactory.create(prototype, self.enums)
                self.assertEqual(expected, mobile.dam_type)
                self.assertEqual(not bool(attack) or attack == 'none', fallback.called)
                # Only resets establish an origin, as with ROM's zone pointer.
                self.assertEqual('', mobile.origin_area_id)

    def test_movement_changes_current_area_without_replacing_reset_origin(self):
        mobile = self.npc()
        mobile.origin_area_id = self.room.area_id
        self.room.add_mobile_to_room(mobile)
        self.movement.travel(mobile, 'north', self.room)
        self.assertEqual(self.destination.id, mobile.room_id)
        self.assertEqual(self.destination.area_id, mobile.area_id)
        self.assertEqual(self.room.area_id, mobile.origin_area_id)

    def ticker(self, mobile):
        self.room.add_mobile_to_room(mobile)
        self.registries.character_registry = NS(all_characters=lambda: [mobile, self.actor, self.bob, self.cara],
                                                unregister=Mock())
        fight = NS(stop_fighting=Mock(), effect_handler=self.effects)
        effects = NS(tick_effects=AsyncMock(), tick_status_effects=AsyncMock())
        bus = NS(send_to_character=AsyncMock(), text_to_message=lambda text: text)
        wiz = NS(current_session=Mock(return_value=None))
        ticker = EntityUpdateHandler(self.registries, self.enums, fight, effects, bus, wiz)
        ticker.rng = Mock(number_percent=Mock(return_value=1))
        mobile.regenerate = Mock()
        return ticker

    async def test_displaced_npc_extraction_precedes_notice_and_skips_rest_of_tick(self):
        mobile = self.npc()
        mobile.origin_area_id = 'home'
        possession = item('keepsake')
        mobile.add_item(possession)
        self.bob.master = self.bob.leader = mobile
        self.bob.context = {'reply_to': mobile.id}
        self.flag(mobile, 'AFF_INVISIBLE')
        self.flag(self.cara, 'AFF_DETECT_INVIS')
        ticker = self.ticker(mobile)

        async def notice(recipient, text):
            self.assertNotIn(mobile.id, self.room.mobiles)
            self.assertEqual('', mobile.room_id)
        ticker.message_bus.send_to_character.side_effect = notice
        await ticker.tick(mobile, self.room)
        self.assertEqual([], mobile.owned_items())
        self.assertIsNone(self.bob.master)
        self.assertIsNone(self.bob.leader)
        self.assertNotIn('reply_to', self.bob.context)
        self.assertEqual({}, self.room.contents)  # No corpse, loot drop or death reward.
        ticker.entity_extractor.registries.character_registry.unregister.assert_called_once_with(item=mobile)
        mobile.regenerate.assert_not_called()
        ticker.effect_update_handler.tick_effects.assert_not_awaited()
        ticker.effect_update_handler.tick_status_effects.assert_not_awaited()
        messages = dict(call.args for call in ticker.message_bus.send_to_character.await_args_list)
        self.assertEqual('Someone wanders on home.\r\n', messages[self.bob.id])
        self.assertEqual('Npc wanders on home.\r\n', messages[self.cara.id])

    async def test_home_roll_has_strict_four_percent_success_boundary(self):
        for roll, removed in ((1, True), (4, True), (5, False), (100, False)):
            with self.subTest(roll=roll):
                mobile = self.npc()
                mobile.origin_area_id = 'home'
                if roll == 4:
                    mobile.set_position(CharacterApi.pos_value('POS_STUNNED'))
                ticker = self.ticker(mobile)
                ticker.rng.number_percent.return_value = roll
                await ticker.tick(mobile, self.room)
                self.assertEqual(removed, mobile.id not in self.room.mobiles)
                self.assertEqual(not removed, mobile.regenerate.called)
                ticker.rng.number_percent.assert_called_once_with()

    async def test_ineligible_npcs_never_roll_for_home_cleanup(self):
        for reason in ('no_origin', 'home', 'controlled', 'fighting', 'charmed', 'incapacitated'):
            with self.subTest(reason=reason):
                mobile = self.npc()
                mobile.origin_area_id = 'home'
                ticker = self.ticker(mobile)
                if reason == 'no_origin':
                    mobile.origin_area_id = ''
                elif reason == 'home':
                    mobile.origin_area_id = self.room.area_id
                elif reason == 'controlled':
                    ticker.wiz_handler.current_session.return_value = NS()
                elif reason == 'fighting':
                    mobile.fighting = self.actor
                elif reason == 'charmed':
                    self.flag(mobile, 'AFF_CHARM')
                else:
                    mobile.set_position(CharacterApi.pos_value('POS_INCAP'))
                await ticker.tick(mobile, self.room)
                self.assertIn(mobile.id, self.room.mobiles)
                ticker.rng.number_percent.assert_not_called()
                ticker.effect_update_handler.tick_effects.assert_awaited_once_with(mobile)


if __name__ == '__main__':
    unittest.main()
