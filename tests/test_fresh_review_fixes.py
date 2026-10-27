import asyncio
import json
import unittest
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock, patch

from tests.test_review_application_fixes import RuntimeFixture
from api.CharacterApi import CharacterApi
from combat.CombatHandler import FightHandler
from devtools.collection_query import load_collections
from game.EntityUpdateHandler import EntityUpdateHandler
from game.Equipped import Equipped
from interp.Context import Context
from item.Effect import Effect
from item.EffectHandler import EffectHandler
from item.Item import Item
from item.ItemUpdateHandler import ItemUpdateHandler
from mobile.Mobile import Mobile
from notes.InGameNote import InGameNote
from notes.NoteHandler import NoteHandler
from player.Character import Character
from player.CharacterService import CharacterService
from player.PlayerHandler import PlayerHandler
from server.session.SessionHandler import SessionHandler
from server.session.SessionState import SessionStatus
from skill.Spell import Spell
from util.EffectUtil import EffectUtil
from item.ItemFactory import ItemFactory
from util.WizUtil import WizUtil



def item(identifier, **changes):
    data = dict(id=identifier, areaId='area', vnum='100', name=identifier,
                shortDescription=identifier, longDescription=identifier, material='cloth',
                itemType='container', extraFlags='0', wearFlags='1', value0='0', value1='0',
                value2='0', value3='0', value4='0', condition='G', level=1, weight=1,
                cost=1, affectData=[], contains=[])
    data.update(changes)
    return Item.from_json(data)


def restore(character):
    return Character.from_json(json.loads(json.dumps(CharacterService._serialize_character(character))))


class EquipmentEffectTests(RuntimeFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.effects = EffectHandler(self.enums)

    def ring(self, identifier, modifier=2):
        return item(identifier, effects=[dict(type='ring', where='TO_OBJECT', duration=-1,
                                             location='APPLY_STR', modifier=modifier)])

    def test_save_load_remove_and_reequip_preserve_exactly_one_item_contribution(self):
        for legacy in (False, True):
            with self.subTest(legacy_source=legacy):
                actor = self.character('wearer')
                ring = self.ring('ring')
                actor.equip_item(ring, 'finger1')
                self.effects.apply_item_effects(actor, ring)
                if legacy:
                    actor.effects[0].source += ':123456789'
                loaded = restore(actor)
                ring = loaded.equipped.finger1
                self.assertIs(loaded, ring._effect_wearer)
                self.assertEqual('item:ring', loaded.effects[0].source)
                self.assertEqual(15, loaded.character_attributes.strength)
                self.effects.remove_item_effects(loaded, ring)
                loaded.unequip_item('finger1')
                self.assertEqual(13, loaded.character_attributes.strength)
                self.assertFalse(loaded.effects)
                loaded.equip_item(ring, 'finger1')
                self.effects.apply_item_effects(loaded, ring)
                self.effects.apply_item_effects(loaded, ring)
                self.assertEqual(15, loaded.character_attributes.strength)
                self.assertEqual(1, len(loaded.effects))

    def test_similar_items_with_distinct_ids_keep_separate_ownership_after_reload(self):
        for slot, identifier, modifier in [('finger1', 'one', 2), ('finger2', 'two', 3)]:
            ring = self.ring(identifier, modifier)
            self.actor.equip_item(ring, slot)
            self.effects.apply_item_effects(self.actor, ring)
        loaded = restore(self.actor)
        self.effects.remove_item_effects(loaded, loaded.equipped.finger1)
        self.assertEqual(16, loaded.character_attributes.strength)
        self.assertEqual(['item:two'], [effect.source for effect in loaded.effects])

    def test_restored_wearer_refreshes_when_object_affect_expires(self):
        ring = self.ring('ring')
        ring.effects[0].duration = 0
        self.actor.equip_item(ring, 'finger1')
        self.effects.apply_item_effects(self.actor, ring)
        loaded = restore(self.actor)
        self.effects.tick_effects(loaded.equipped.finger1)
        self.assertEqual(13, loaded.character_attributes.strength)
        self.assertFalse(loaded.effects)

    def test_clone_and_nested_clone_effects_are_independent_during_ticks(self):
        original = self.ring('ring')
        original.effects[0].duration = 3
        container = item('bag', contains=[original])
        clone = ItemFactory.copy_instance(container)
        copied = clone.contains[0]
        self.assertIsNot(original.effects[0], copied.effects[0])
        self.effects.tick_effects(copied)
        copied.effects[0].modifier = 99
        self.assertEqual(3, original.effects[0].duration)
        self.assertEqual(2, original.effects[0].modifier)
        self.assertEqual(2, copied.effects[0].duration)


class CombatModifierTests(RuntimeFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.effects = EffectHandler(self.enums)

    def spell(self, name):
        documents = load_collections(Path(__file__).resolve().parents[1] / 'resources/collections', ['spells'])
        record = deepcopy(next(doc for doc in documents['spells'].documents if doc['name'] == name))
        record.setdefault('levelByClass', {})
        record.setdefault('ratingByClass', {})
        return Spell.from_json(record)

    def test_authored_bless_curse_frenzy_apply_persist_and_dispel_on_real_players(self):
        for name, expected in [('bless', (3, 0, -3)), ('curse', (-3, 0, 3)), ('frenzy', (4, 4, 0))]:
            with self.subTest(spell=name):
                actor = self.character(name)
                actor.level = 24
                spell = self.spell(name)
                self.effects.apply_spell_effects(actor, actor, spell)
                self.assertEqual(expected, (actor.hit_roll, actor.dam_roll, actor.saving_throw))
                loaded = restore(actor)
                self.assertEqual(expected, (loaded.hit_roll, loaded.dam_roll, loaded.saving_throw))
                combat = FightHandler.__new__(FightHandler)
                self.assertEqual(CharacterApi.get_hitroll(loaded), combat._current_hitroll(loaded))
                self.assertEqual(CharacterApi.get_damroll(loaded), combat._current_damroll(loaded))
                with patch.object(EffectUtil, 'saves_dispel', return_value=False):
                    self.effects.dispel_effects(24, loaded, spell.handler_id)
                self.assertEqual((0, 0, 0), (loaded.hit_roll, loaded.dam_roll, loaded.saving_throw))

    def test_saving_throw_affect_changes_the_actual_save_roll(self):
        self.actor.level = 24
        baseline = int(50 * (0.9 if self.actor.character_class.mana_gain else 1))
        with patch('util.EffectUtil.random.randint', return_value=baseline + 1):
            self.assertFalse(EffectUtil.saves_spell(24, self.actor))
            self.effects.apply_spell_effects(self.actor, self.actor, self.spell('bless'))
            self.assertTrue(EffectUtil.saves_spell(24, self.actor))

    def test_legacy_missing_counters_reconstruct_named_and_numeric_effects_once(self):
        self.actor.effects = [Effect(location='APPLY_HITROLL', modifier=3),
                              Effect(location=self.enums.get('applyTypes').APPLY_DAMROLL.value, modifier=4),
                              Effect(location='APPLY_SAVING_SPELL', modifier=-2)]
        document = CharacterService._serialize_character(self.actor)
        for name in ['hitRoll', 'damRoll', 'savingThrow']:
            document.pop(name)
        loaded = Character.from_json(document)
        self.assertEqual((3, 4, -2), (loaded.hit_roll, loaded.dam_roll, loaded.saving_throw))
        loaded = restore(loaded)
        self.assertEqual((3, 4, -2), (loaded.hit_roll, loaded.dam_roll, loaded.saving_throw))

    def test_equipment_modifiers_and_expiration_reverse_player_counters(self):
        ring = item('ring', effects=[dict(location='APPLY_HITROLL', modifier=5, duration=0)])
        self.actor.equip_item(ring, 'finger1')
        self.effects.apply_item_effects(self.actor, ring)
        self.assertEqual(5, self.actor.hit_roll)
        self.effects.tick_effects(self.actor)
        self.assertEqual(0, self.actor.hit_roll)


class WorldLookupTests(RuntimeFixture, unittest.TestCase):
    def test_live_traversal_covers_players_npcs_equipment_and_nested_room_items(self):
        player_item, worn, mob_item, mob_worn, nested = [item(name) for name in
                                                       ['player', 'worn', 'mobitem', 'mobworn', 'nested']]
        self.actor.add_item(player_item)
        self.actor.equip_item(worn, 'held')
        mobile = Mobile.__new__(Mobile)
        mobile.id, mobile.inventory, mobile.equipped = 'mobile', [mob_item], Equipped(held=mob_worn)
        self.room.add_mobile_to_room(mobile)
        bag = item('bag', contains=[nested])
        self.room.add_item_to_room(bag)
        # The account registry is deliberately not an authority for live objects.
        offline = NS(all_characters=Mock(side_effect=AssertionError('offline registry used')))
        for target in [player_item, worn, mob_item, mob_worn, nested]:
            self.assertIs(target, WizUtil.find_world_item(offline, self.rooms, target.name))
        bag.contains.append(bag)
        self.assertIsNone(WizUtil.find_world_item(offline, self.rooms, 'missing'))
        self.assertIsNone(WizUtil.find_world_item(offline, None, 'offline-only'))


class NestedSocialTests(RuntimeFixture, unittest.IsolatedAsyncioTestCase):
    async def test_at_force_and_order_resolve_only_social_verb_preserving_target_text(self):
        social = object()
        handler = PlayerHandler.__new__(PlayerHandler)
        handler.interp_registry = NS(get_or_none=lambda **kw: None, all_commands=lambda: [])
        handler.social_registry = NS(get_or_none=Mock(side_effect=lambda **kw: social if kw['name'] == 'smile' else None))
        handler.room_registry = self.rooms
        handler.interp_api = NS(render_message_key=lambda *args, **kwargs: {})
        handler.message_bus = NS(send_to_character=AsyncMock(), text_to_message=lambda text: text)
        socials = NS(handle_social=AsyncMock())
        context = self.context('force')
        context.handler_service = NS(get_handler=lambda key: socials)
        for command in ['SMILE\tTester', 'smile', 'smile self']:
            entry = {'victim': self.actor, 'command': command}
            await handler._handle_force_payload(self.actor, context, {'forced_commands': [entry]})
            await handler._handle_order_payload(self.actor, context, {'ordered_commands': [entry]})
            await handler._handle_at_payload(self.actor, context,
                                            {'interpret_at': command, 'at_original_room': self.room})
            self.assertEqual((self.actor, command, social), socials.handle_social.await_args.args)
        self.assertEqual(9, socials.handle_social.await_count)
        self.assertTrue(all(call.kwargs == {'name': 'smile'}
                            for call in handler.social_registry.get_or_none.call_args_list))


class NoteCursorTests(RuntimeFixture, unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        super().setUp()
        self.notes = [InGameNote(id='a', type=0, to_list='all', subject='FIRST', date_stamp=123),
                      InGameNote(id='b', type=0, to_list='all', subject='SECOND', date_stamp=123)]
        self.handler = NoteHandler(None, NS(get_notes_by_type=lambda kind: list(reversed(self.notes))), None, self.api)

    async def read(self, text=''):
        return (await self.handler.execute(self.actor, self.context('note', text)))['to_char']

    async def test_equal_timestamps_are_read_independently_across_save_load(self):
        self.assertIn('FIRST', await self.read())
        self.actor = restore(self.actor)
        self.assertIn('SECOND', await self.read())
        self.assertIn('no unread', await self.read())
        self.notes.append(InGameNote(id='c', to_list='all', subject='LATE', date_stamp=123))
        self.assertIn('LATE', await self.read())

    async def test_explicit_read_does_not_skip_its_unread_timestamp_peer(self):
        self.assertIn('SECOND', await self.read('read 2'))
        self.assertIn('FIRST', await self.read())
        self.assertIn('no unread', await self.read())

    async def test_catchup_marks_current_peers_but_not_a_later_post_in_same_second(self):
        await self.read('catchup')
        self.actor = restore(self.actor)
        self.assertIn('no unread', await self.read())
        self.notes.append(InGameNote(id='c', to_list='all', subject='LATER', date_stamp=123))
        self.assertIn('LATER', await self.read())

    async def test_legacy_timestamp_cursor_preserves_prior_read_semantics(self):
        self.actor.note_read_stamps = {'0': 123}
        self.actor.note_read_ids = {}
        self.assertIn('no unread', await self.read())
        self.notes.append(InGameNote(id='c', to_list='all', subject='NEW', date_stamp=124))
        self.assertIn('NEW', await self.read())

    async def test_empty_catchup_does_not_hide_a_new_note_at_the_boundary(self):
        self.notes.clear()
        with patch('notes.NoteHandler.time.time', return_value=123):
            await self.read('catchup')
        self.notes.append(InGameNote(id='new', to_list='all', subject='NEW', date_stamp=123))
        self.assertIn('NEW', await self.read())


class RetirementTests(RuntimeFixture, unittest.IsolatedAsyncioTestCase):
    async def test_save_exception_restores_world_update_eligibility(self):
        handler = self.quit_handler(AsyncMock(side_effect=RuntimeError('save failed')))
        with self.assertRaisesRegex(RuntimeError, 'save failed'):
            await handler.do_quit(self.actor, self.context('quit'))
        self.assertFalse(self.actor.world_retired)
        handler.character_registry.set_playing.assert_called_once_with(self.actor)
        self.assertIn(self.actor.id, self.room.characters)

    def quit_handler(self, save):
        handler = PlayerHandler.__new__(PlayerHandler)
        handler.info_commands = NS(do_quit=lambda ctx: {'to_char': 'Bye', 'to_room': 'Left'})
        handler.room_registry = self.rooms
        handler.character_registry = NS(remove_playing=Mock(), set_playing=Mock())
        handler.character_service = NS(save_character_async=save)
        sessions = SessionHandler()
        session = sessions.create_session('session')
        session.character, session.status = self.actor, SessionStatus.PLAYING
        handler.message_bus = NS(session_handler=sessions, send_to_character=AsyncMock(), text_to_message=lambda text: text)
        return handler

    def updater(self, send):
        return EntityUpdateHandler(NS(room_registry=self.rooms), self.enums, Mock(),
                                   NS(tick_effects=AsyncMock(), tick_status_effects=AsyncMock()),
                                   NS(send_to_character=send, text_to_message=lambda text: text))

    async def test_already_selected_player_cannot_tick_after_quit_snapshot(self):
        first = self.character('first')
        first.status_flags.hunger = 1
        self.room.add_player_to_room(first)
        last = self.character('last')
        self.room.add_player_to_room(last)
        entered, release, saved, finish = [asyncio.Event() for _ in range(4)]
        snapshots = []

        async def send(character_id, message):
            if character_id == first.id:
                entered.set()
                await release.wait()

        async def save(character):
            snapshots.append(deepcopy(CharacterService._serialize_character(character)))
            saved.set()
            await finish.wait()
            return True

        update = asyncio.create_task(self.updater(send).update([first, self.actor, last]))
        await asyncio.wait_for(entered.wait(), 1)
        handler = self.quit_handler(save)
        with patch.object(CharacterApi, 'can_see', return_value=True):
            quit_task = asyncio.create_task(handler.do_quit(self.actor, self.context('quit')))
            try:
                await asyncio.wait_for(saved.wait(), 1)
                release.set()
                await asyncio.wait_for(asyncio.shield(update), 1)
                self.assertFalse(quit_task.done())
                self.assertEqual(47, last.status_flags.thirst)
                self.assertEqual(48, self.actor.status_flags.thirst)
            finally:
                release.set()
                finish.set()
            await asyncio.wait_for(asyncio.gather(update, quit_task), 2)
        self.assertEqual(snapshots[0]['statusFlags']['thirst'], self.actor.status_flags.thirst)
        self.assertTrue(self.actor.world_retired)

    async def test_quit_waits_for_an_entity_tick_already_in_progress(self):
        self.actor.status_flags.hunger = 1
        entered, release = asyncio.Event(), asyncio.Event()
        snapshots = []

        async def send(*args):
            entered.set()
            await release.wait()

        async def save(character):
            snapshots.append(CharacterService._serialize_character(character))
            return True

        tick = asyncio.create_task(self.updater(send).tick(self.actor, self.room))
        await asyncio.wait_for(entered.wait(), 1)
        quit_task = asyncio.create_task(self.quit_handler(save).do_quit(self.actor, self.context('quit')))
        try:
            await asyncio.sleep(0)
            self.assertFalse(snapshots)
        finally:
            release.set()
        await asyncio.wait_for(asyncio.gather(tick, quit_task), 2)
        self.assertEqual(47, snapshots[0]['statusFlags']['thirst'])

    def item_updater(self, messages=None):
        effects = EffectHandler(self.enums)
        return ItemUpdateHandler(
            NS(room_registry=self.rooms, shop_registry=NS(find_by_keeper_vnum=lambda vnum: None)),
            self.enums, NS(effect_handler=effects, expired_messages=Mock(side_effect=messages or (lambda obj, key: []))),
            NS(text_to_message=lambda text: text, send_to_character=AsyncMock(), send_to_room=AsyncMock()))

    async def test_owned_item_state_finishes_before_output_and_final_save(self):
        carried = item('carried', timer=3)
        self.actor.add_item(carried)
        entered, release = asyncio.Event(), asyncio.Event()
        updater = self.item_updater(lambda obj, key: ['Glow fades.'])

        async def send(*args, **kwargs):
            entered.set()
            await release.wait()

        updater._emit_item_message = send
        snapshots = []

        async def save(character):
            snapshots.append(CharacterService._serialize_character(character))
            return True

        update = asyncio.create_task(updater.update())
        await asyncio.wait_for(entered.wait(), 1)
        quit_task = asyncio.create_task(self.quit_handler(save).do_quit(self.actor, self.context('quit')))
        try:
            await asyncio.wait_for(asyncio.shield(quit_task), 1)
            self.assertEqual(2, carried.timer)
            self.assertEqual(2, snapshots[0]['inventory'][0]['timer'])
        finally:
            release.set()
        await asyncio.wait_for(asyncio.gather(update, quit_task), 2)
        self.assertEqual(2, snapshots[0]['inventory'][0]['timer'])

    async def test_pickup_or_transfer_during_output_cannot_change_saved_item_state(self):
        for transferred, nested in ((False, False), (True, False), (False, True), (True, True)):
            with self.subTest(transferred=transferred, nested=nested):
                self.actor.world_retired = False
                self.actor.loot.clear()
                self.room.add_player_to_room(self.actor)
                first = item('first', timer=3)
                target = item('target', timer=3)
                root = item('bag', contains=[target], timer=0) if nested else target
                self.room.contents = {first.id: first}
                donor = self.character('donor')
                self.room.add_player_to_room(donor)
                if transferred:
                    donor.add_item(root)
                else:
                    self.room.add_item_to_room(root)
                entered, release = asyncio.Event(), asyncio.Event()
                updater = self.item_updater(lambda obj, key: ['Glow fades.'] if obj is first else [])

                async def send(*args, **kwargs):
                    entered.set()
                    await release.wait()

                updater._emit_item_message = send
                update = asyncio.create_task(updater.update())
                await asyncio.wait_for(entered.wait(), 1)
                snapshots = []

                async def save(character):
                    snapshots.append(CharacterService._serialize_character(character))
                    return True

                try:
                    if transferred:
                        donor.loot.remove(root)
                    else:
                        self.room.remove_item_from_room(root)
                    self.actor.add_item(root)
                    with patch.object(CharacterApi, 'can_see', return_value=True):
                        await self.quit_handler(save).do_quit(self.actor, self.context('quit'))
                finally:
                    release.set()
                    await asyncio.wait_for(update, 1)
                saved = snapshots[0]['inventory'][0]
                self.assertEqual(2, saved['contains'][0]['timer'] if nested else saved['timer'])
                self.assertEqual(2, target.timer)
                self.assertEqual(1, sum(call.args[0] is target for call in updater.effect_update_handler.expired_messages.call_args_list))
                self.room.remove_player_from_room(donor)

    async def test_expiration_removes_item_before_any_notice_can_yield(self):
        first, target = item('first', timer=3), item('target', timer=1)
        self.room.contents = {first.id: first, target.id: target}
        entered, release = asyncio.Event(), asyncio.Event()
        updater = self.item_updater(lambda obj, key: ['Glow fades.'] if obj is first else [])

        async def send(*args, **kwargs):
            entered.set()
            await release.wait()

        updater._emit_item_message = send
        update = asyncio.create_task(updater.update())
        await asyncio.wait_for(entered.wait(), 1)
        try:
            self.assertNotIn(target.id, self.room.contents)
            self.assertEqual(0, target.timer)
        finally:
            release.set()
            await asyncio.wait_for(update, 1)

    async def test_item_update_finishes_while_retired_owner_save_is_pending(self):
        carried, exposed = item('carried', timer=3), item('room', timer=3)
        self.actor.add_item(carried)
        self.room.add_item_to_room(exposed)
        saving, finish = asyncio.Event(), asyncio.Event()

        async def save(character):
            saving.set()
            await finish.wait()
            return True

        quit_task = asyncio.create_task(self.quit_handler(save).do_quit(self.actor, self.context('quit')))
        await asyncio.wait_for(saving.wait(), 1)
        try:
            await asyncio.wait_for(self.item_updater().update(), 1)
            self.assertEqual(3, carried.timer)
            self.assertEqual(2, exposed.timer)
            self.assertFalse(quit_task.done())
        finally:
            finish.set()
            await asyncio.wait_for(quit_task, 1)


if __name__ == '__main__':
    unittest.main()
