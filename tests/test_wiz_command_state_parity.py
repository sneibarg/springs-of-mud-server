import unittest
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock, patch

from tests.test_wiz_identity_targeting_parity import TargetingFixture
from tests.test_immortal_priority_parity import mobile_entity
from api.AliasApi import AliasApi
from api.CharacterApi import CharacterApi
from api.WizSetApi import WizSetApi
from interp.CommandAudit import CommandAudit
from interp.CommandExecutor import CommandExecutor
from interp.CommandAccess import CommandDenial
from item.Effect import Effect
from item.EffectHandler import EffectHandler
from mobile.MobileFactory import MobileFactory
from server.session.SessionState import SessionStatus
from util.WizDiagnostics import WizDiagnostics


class CommandStateTests(TargetingFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.registries.skill_registry = NS(all_skills=lambda: [])
        self.registries.spell_registry = NS(all_spells=lambda: [])
        self.registries.item_registry = NS(all_items=lambda: [])
        self.registries.mobile_registry = NS(all_mobiles=lambda: [])
        self.wiz.registry_service = self.registries
        self.diagnostics = WizDiagnostics(self.registries, self.wiz_handler)
        self.set_api = WizSetApi(self.registries, self.wiz_handler)

    def test_prefix_runs_before_alias_and_bypasses_prefix_controls(self):
        self.actor.context = {'prefix': 's', 'aliases': {'s': 'say'}}
        self.assertEqual(AliasApi.substitute_command(self.actor, 'hello').command, 'say hello')
        for control in ('prefix', 'pref', 'prefi'):
            self.assertEqual(AliasApi.substitute_command(self.actor, control).command, control)
            self.actor.context['prefix'] = 's'
            context = self.context('prefix', '')
            context.raw_command = control
            result = self.wiz.do_prefix(self.actor, context)
            if control != 'prefix':
                self.assertEqual(result['blocked_key'], 'abbreviated')
                self.assertEqual(self.actor.context['prefix'], 's')

    def test_prefix_overflow_keeps_original_input(self):
        self.actor.context = {'prefix': 'say ' + 'x' * AliasApi.MAX_INPUT_LENGTH}
        result = AliasApi.substitute_command(self.actor, 'look')
        self.assertEqual(result.command, 'look')
        self.assertEqual(result.message_key, 'overflow')
        self.assertEqual(self.command('prefix').render_message('to_char', result.message_key),
                         'Line too long, prefix not processed.')

    def test_prefix_applies_to_switched_body_without_alias_expansion(self):
        mob = mobile_entity('body', self.actor.status_flags)
        mob.context = {'prefix': 'say', 'aliases': {'say': 'yell'}}
        self.assertEqual(AliasApi.substitute_command(mob, 'hello').command, 'say hello')

    def test_switched_input_uses_original_players_prefix_and_aliases(self):
        mob = mobile_entity('body', self.actor.status_flags)
        self.actor.context = {'prefix': 's', 'aliases': {'s': 'say'}}
        mob.context = {'prefix': 'yell', 'controller_original': self.actor}
        self.assertEqual(AliasApi.substitute_command(mob, 'hello').command, 'say hello')

    def test_set_quoted_skill_and_abbreviated_fields(self):
        victim = self.player('bob')
        spell = NS(name='cure light')
        self.registries.spell_registry.all_spells = lambda: [spell]
        context = self.context('set', "skill bob 'cure light' 73")
        self.assertEqual(self.set_api.dispatch(self.actor, context), {'to_char': ''})
        self.assertEqual(victim.get_learned('cure light', collection_name='spells')['level'], 73)
        self.set_api.dispatch(self.actor, self.context('set', 'char bob ali -500'))
        self.assertEqual(victim.get_alignment(), -500)
        self.set_api.dispatch(self.actor, self.context('set', 'char bob alignmentjunk 500'))
        self.assertEqual(victim.get_alignment(), -500)

    def test_setting_permanent_stats_retains_spell_and_item_modifiers(self):
        victim = self.player('bob')
        handler = EffectHandler(self.enums)
        victim.character_attributes.strength = 15
        for source, modifier in (('spell', 3), ('item:bracelet', 2)):
            handler.affect_to_char(victim, Effect(type=source, location='APPLY_STR', modifier=modifier, source=source))
        self.assertEqual(victim.character_attributes.strength, 20)
        with patch.object(self.set_api, '_max_train_for', return_value=25):
            self.set_api.dispatch(self.actor, self.context('set', 'char bob str 20'))
        self.assertEqual(victim.character_attributes.strength, 25)
        for effect in list(victim.effects):
            handler.affect_remove(victim, effect)
        self.assertEqual(victim.character_attributes.strength, 20)

    def test_setting_sex_preserves_temporary_modifier_until_expiry(self):
        victim = self.player('bob')
        victim.sex = '1'
        handler = EffectHandler(self.enums)
        handler.affect_to_char(victim, Effect(type='change sex', location='APPLY_SEX', modifier=1))
        self.set_api.dispatch(self.actor, self.context('set', 'char bob sex 0'))
        self.assertEqual(int(victim.sex), 1)
        handler.affect_remove(victim, victim.effects[0])
        self.assertEqual(int(victim.sex), 0)

    def test_string_quoted_target_and_extra_description_keywords(self):
        item = self.item('item', 'royal silver sword')
        self.room.add_item_to_room(item)
        self.wiz.do_string(self.actor, self.context('string', "obj 'royal silver' sh a gleaming sword"))
        self.assertEqual(item.short_description, 'a gleaming sword')
        self.wiz.do_string(self.actor, self.context('string', "obj 'royal silver' ed 'runes blade' Ancient writing."))
        self.assertEqual(item.extra_description.keyword, 'runes blade')

    def test_clone_copies_live_resources_attributes_and_effects_independently(self):
        mob = mobile_entity('body', self.actor.status_flags)
        mob.hit, mob.max_hit, mob.mana, mob.max_mana = 7, 111, 9, 80
        from player.CharacterAttributes import CharacterAttributes
        mob.character_attributes = CharacterAttributes.default()
        mob.character_attributes.strength = 21
        mob.position = 5
        mob.effects = [Effect(type='poison', duration=4, location='APPLY_STR', modifier=-2)]
        gear = self.item('bracelet')
        mob.equip_item(gear, 'head')
        mob.effects.append(Effect(type='item', source=Effect.item_source(gear.id), location='APPLY_STR', modifier=3))
        fresh = mobile_entity('fresh', self.actor.status_flags)
        with patch.object(MobileFactory, 'create', return_value=fresh):
            clone = MobileFactory.copy_instance(mob, self.enums)
        self.assertEqual((clone.hit, clone.max_hit, clone.mana, clone.max_mana, clone.position), (7, 111, 9, 80, 5))
        self.assertEqual(clone.character_attributes.strength, 21)
        self.assertIsNot(clone.character_attributes, mob.character_attributes)
        self.assertIsNot(clone.effects[0], mob.effects[0])
        self.assertNotEqual(clone.equipped.head.id, gear.id)
        self.assertTrue(clone.effects[1].belongs_to_item(clone.equipped.head.id))
        EffectHandler(self.enums).affect_remove(clone, clone.effects[0])
        self.assertEqual((clone.character_attributes.strength, mob.character_attributes.strength), (23, 21))

    def test_stat_remote_room_generic_numeric_and_object_priority(self):
        self.remote.description = 'A remote chamber.'
        self.remote.heal_rate = 150
        for text in ('room 2', '2'):
            output = self.wiz.do_stat(self.actor, self.context('stat', text))['to_char']
            self.assertIn('Destination', output)
            self.assertIn('heal_rate: 150', output)
            self.assertIn('A remote chamber.', output)
        self.player('sword')
        item = self.item('sword')
        self.room.add_item_to_room(item)
        output = self.wiz.do_stat(self.actor, self.context('stat', 'sword'))['to_char']
        self.assertTrue(output.startswith('Obj ['))
        self.assertIn('value4:', output)
        with patch.object(self.wiz_handler, 'room_is_private_for_actor', return_value=True):
            self.assertIn('private', self.wiz.do_stat(self.actor, self.context('stat', 'room 2'))['to_char'])

    def test_filtered_clone_drops_excluded_equipment_modifiers(self):
        from player.CharacterAttributes import CharacterAttributes
        mob = mobile_entity('body', self.actor.status_flags)
        mob.character_attributes = CharacterAttributes.default()
        mob.character_attributes.strength = 18
        gear = self.item('bracelet')
        mob.equip_item(gear, 'head')
        handler = EffectHandler(self.enums)
        handler.affect_to_char(mob, Effect(type='item', source=Effect.item_source(gear.id),
                                           location='APPLY_STR', modifier=3))
        fresh = mobile_entity('fresh', self.actor.status_flags)
        with patch.object(MobileFactory, 'create', return_value=fresh):
            clone = MobileFactory.copy_instance(mob, self.enums, item_filter=lambda item: False,
                                                 effect_handler=handler)
        self.assertEqual(clone.character_attributes.strength, 18)
        self.assertEqual(clone.effects, [])
        self.assertEqual(mob.character_attributes.strength, 21)

    def test_character_stat_reports_resources_flags_attributes_and_effects(self):
        victim = self.player('bob')
        victim.effects = [Effect(type='poison', duration=3, modifier=-2, location='APPLY_STR')]
        output = self.diagnostics.stat(self.actor, 'char bob')['to_char']
        for field in ('Hit:', 'Mana:', 'Move:', 'Attributes:', 'Flags:', 'poison', 'duration: 3'):
            self.assertIn(field, output)

    def test_typed_vnum_and_ability_lookup(self):
        self.registries.mobile_registry.all_mobiles = lambda: [NS(vnum='12', name='royal guard', short_description='a guard')]
        self.registries.item_registry.all_items = lambda: [NS(vnum='13', name='guard sword', short_description='a sword')]
        self.registries.spell_registry.all_spells = lambda: [NS(id='cure-id', name='cure light', slot=16)]
        self.assertIn('M [12]', self.diagnostics.vnum('mob guard')['to_char'])
        self.assertNotIn('O [13]', self.diagnostics.vnum('mob guard')['to_char'])
        self.assertIn('O [13]', self.diagnostics.vnum('obj sword')['to_char'])
        self.assertIn('cure-id', self.diagnostics.vnum('skill cure light')['to_char'])
        self.assertIn('slot 16', self.diagnostics.vnum('spell all')['to_char'])

    def test_mwhere_players_named_and_connected_switched_body(self):
        player = self.player('bob')
        self.assertIn('bob', self.diagnostics.mwhere(self.actor, 'bob'))
        body = mobile_entity('body', self.actor.status_flags)
        body.room_id = self.remote.id
        self.remote.add_mobile_to_room(body)
        session = self.sessions.create_session('switched')
        session.status, session.character = SessionStatus.PLAYING, body
        session.metadata['switched_original'] = player
        output = self.diagnostics.mwhere(self.actor, '')
        self.assertIn('bob (in the body of body)', output)
        self.assertIn('Destination', output)

    def test_owhere_nested_carried_equipped_level_and_visibility(self):
        player = self.player('bob')
        bag, gem, helm = [self.item(name) for name in ('bag', 'gem', 'helm')]
        bag.contains.append(gem)
        player.add_item(bag)
        player.equip_item(helm, 'head')
        for name in ('gem', 'helm'):
            self.assertIn('carried by bob', self.diagnostics.owhere(self.actor, name))
        gem.level = 61
        self.assertIn('Nothing like', self.diagnostics.owhere(self.actor, 'gem'))
        gem.level = 1
        with patch('util.WizDiagnostics.LookupUtil.object_visible', return_value=False):
            self.assertIn('Nothing like', self.diagnostics.owhere(self.actor, 'gem'))
        with patch.object(CharacterApi, 'can_see', return_value=False):
            self.assertIn('somewhere', self.diagnostics.owhere(self.actor, 'gem'))

    def test_sockets_includes_active_character_sessions_and_filters_visibility(self):
        player = self.player('bob')
        session = self.sessions.create_session('login')
        session.character = player
        self.assertIn('bob@', self.wiz_handler.render_sockets(self.actor, 'bo'))
        with patch.object(CharacterApi, 'can_see', return_value=False):
            self.assertIn('No one', self.wiz_handler.render_sockets(self.actor, ''))


class CommandAuditTests(TargetingFixture, unittest.IsolatedAsyncioTestCase):
    async def test_logging_modes_global_player_secure_and_never_redaction(self):
        bus = NS(mirror_snoop_input=AsyncMock(), send_to_character=AsyncMock(), text_to_message=lambda value: value)
        handler = NS(current_session=lambda actor: 'session', log_all=False,
                     wiznet_targets=Mock(return_value=[self.actor]), decorate_wiznet_text=lambda recipient, text: text)
        audit = CommandAudit(handler, bus)
        audit.logger = Mock()
        for mode, global_log, player_log, expected in (
                ('LOG_NORMAL', False, False, False), ('LOG_NORMAL', True, False, True),
                ('LOG_NORMAL', False, True, True), ('LOG_ALWAYS', False, False, True),
                ('LOG_NEVER', True, False, True)):
            with self.subTest(mode=mode, global_log=global_log, player_log=player_log):
                handler.log_all = global_log
                audit.logger.reset_mock()
                bus.mirror_snoop_input.reset_mock()
                with patch.object(CharacterApi, 'has_player_flag', return_value=player_log):
                    await audit.record(self.actor, NS(log=mode), 'password secret')
                self.assertEqual(audit.logger.info.called, expected)
                text = bus.mirror_snoop_input.await_args.args[1]
                self.assertEqual(text, '' if mode == 'LOG_NEVER' else 'password secret')
                if expected:
                    handler.wiznet_targets.assert_called_with(self.actor, flag_name='WIZ_SECURE', min_level=60)
                    self.assertNotIn('secret', audit.logger.info.call_args.args[1] if mode == 'LOG_NEVER' else '')

    async def test_executor_logs_before_position_denial_but_not_freeze(self):
        for denial, count in ((CommandDenial('command_position_sleeping'), 1), (CommandDenial('command_frozen'), 0)):
            audit = NS(record=AsyncMock())
            context = self.context('log', 'all')
            context.raw_command = 'log all'
            await CommandExecutor.execute(context.command, context, authorization=lambda *args: denial,
                                          message_bus=NS(send_to_character=AsyncMock(), text_to_message=lambda value: value), audit=audit)
            self.assertEqual(audit.record.await_count, count)

    def test_log_invalid_input_uses_collection_guards(self):
        result = self.wiz.do_log(self.actor, self.context('log', 'missing'))
        self.assertEqual(result['blocked_key'], 'target_missing')


if __name__ == '__main__':
    unittest.main()
