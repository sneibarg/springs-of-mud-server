import json
import unittest
from copy import deepcopy
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock, patch

from tests.test_review_application_fixes import ROOT, RuntimeFixture
from tests.test_fresh_review_fixes import item
from api.CharacterApi import CharacterApi
from api.GameApi import GameApi
from api.ItemApi import ItemApi
from api.FightApi import FightApi
from api.SkillApi import SkillApi
from area.Room import Room
from area.RoomHandler import RoomHandler
from combat.CombatHandler import FightHandler
from devtools.collection_query import load_collections
from game.StatusFlags import StatusFlags
from interp.Context import Context
from interp.commands.Movement import Movement
from interp.commands.Info import Info
from item.Effect import Effect
from item.EffectHandler import EffectHandler
from item.ItemFactory import ItemFactory
from player.Character import Character
from player.CharacterService import CharacterService
from player.PlayerHandler import PlayerHandler
from mobile.Mobile import Mobile
from skill.Ability import Ability
from skill.Skill import Skill


class SharedFixture(RuntimeFixture):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        data = load_collections(ROOT / 'resources/collections', ['skills', 'items'])
        cls.skill_documents = {doc['name']: doc for doc in data['skills'].documents}
        cls.ring_document = next(doc for doc in data['items'].documents if doc['vnum'] == '6601')

    def setUp(self):
        super().setUp()
        Ability.configure_learning(None)
        self.addCleanup(Ability.configure_learning, None)
        self.skills = {name: Skill.from_json(deepcopy(doc)) for name, doc in self.skill_documents.items()}
        self.skill_registry = NS(get=lambda **kw: self.skills[kw['name']],
                                 get_or_none=lambda **kw: self.skills.get(kw.get('name')),
                                 all_skills=lambda: list(self.skills.values()))
        self.weather = NS(weather_info=NS(sunlight=self.enums.get('timeAndWeather').SUN_LIGHT))
        self.registries = NS(skill_registry=self.skill_registry, spell_registry=NS(all_spells=lambda: []),
                             room_registry=self.rooms,
                             character_registry=NS(get=lambda **kw: self.actor),
                             interp_registry=NS(get_or_none=lambda **kw: self.command(kw['name'])))
        CharacterApi.lazy_load(self.weather, self.registries)
        self.effects = EffectHandler(self.enums)
        self.skill_api = SkillApi(self.skill_registry, self.enums)
        self.actor.character_class.name = 'thief'
        self.actor.level = 20
        self.actor.character_attributes.position = self.enums.get('positions').POS_STANDING
        self.room.name = 'Visible room'
        self.room.description = 'Visible description'
        self.room.sector_type = self.enums.get('sectorTypes').SECT_FIELD
        self.victim = self.character('hidden target')
        self.victim.character_class.name = 'thief'
        self.victim.level = 20
        self.victim.room_id = self.room.id
        self.victim.character_attributes.position = self.enums.get('positions').POS_STANDING
        self.movement = Movement.__new__(Movement)
        self.movement.skill_registry = self.skill_registry
        self.movement.skill_api = self.skill_api
        self.movement.effect_handler = self.effects
        self.movement.affected_bits = self.enums.get('affectedBy')

    def flag(self, actor, name, enabled=True):
        CharacterApi.set_affected_by_name(actor, self.enums.get('affectedBy'), name, enabled)

    def npc(self):
        return Mobile(id='npc', area_id=self.room.area_id, room_id=self.room.id,
                      name='npc', sex='1', level=20, gold=0, silver=0, vnum='1',
                      short_description='npc', long_description='npc', description='',
                      race='human', flags='', alignment='0', group='', dam_type='bash',
                      size='medium', material='flesh', hit_roll=0,
                      character_attributes=deepcopy(self.actor.character_attributes),
                      status_flags=StatusFlags.default())


class ResourceAndDefenseParityTests(SharedFixture, unittest.TestCase):
    def test_resource_modifiers_reverse_without_changing_current_resources(self):
        for location, maximum, current in [('APPLY_HIT', 'max_hit', 'hit'),
                                            ('APPLY_MANA', 'max_mana', 'mana'),
                                            ('APPLY_MOVE', 'max_movement', 'movement')]:
            with self.subTest(location=location):
                base, filled = getattr(self.actor, maximum), getattr(self.actor, current)
                effect = self.effects.affect_to_char(self.actor, Effect(
                    where='TO_AFFECTS', type='resource', location=location, modifier=7))
                self.assertEqual(base + 7, getattr(self.actor, maximum))
                self.assertEqual(filled, getattr(self.actor, current))
                self.effects.remove_effect(self.actor, effect)
                self.assertEqual(base, getattr(self.actor, maximum))

    def test_bundled_ring_hp_bonus_survives_refresh_save_and_removal(self):
        document = deepcopy(self.ring_document)
        document['id'] = document.pop('_id')['$oid']
        document.pop('_class', None)
        ring = ItemFactory.from_data(document, {}, self.skill_registry)
        base = self.actor.max_hit
        self.actor.equip_item(ring, 'finger1')
        for _ in range(2):
            self.effects.apply_item_effects(self.actor, ring)
            self.assertEqual(base + 4, self.actor.max_hit)
        loaded = Character.from_json(json.loads(json.dumps(CharacterService._serialize_character(self.actor))))
        self.assertEqual(base + 4, loaded.max_hit)
        self.effects.remove_item_effects(loaded, loaded.equipped.finger1)
        self.assertEqual(base, loaded.max_hit)

    def test_defense_bits_apply_restore_overlapping_effects_and_remove(self):
        for where, field, name in [('TO_IMMUNE', 'imm', 'IMM_FIRE'),
                                    ('TO_RESIST', 'res', 'RES_FIRE'),
                                    ('TO_VULN', 'vuln', 'VULN_FIRE')]:
            with self.subTest(where=where):
                self.actor.status_flags.set_flag(field, 16)
                first = self.effects.affect_to_char(self.actor, Effect(where=where, type='first', bitvector=name))
                second = self.effects.affect_to_char(self.actor, Effect(where=where, type='second', bitvector=128))
                self.assertEqual(144, getattr(self.actor.status_flags, field))
                self.effects.remove_effect(self.actor, first)
                self.assertEqual(144, getattr(self.actor.status_flags, field))
                self.effects.remove_effect(self.actor, second)
                self.assertEqual(16, getattr(self.actor.status_flags, field))

    def test_worn_defense_reaches_actual_damage_immunity_resolver(self):
        ring = item('fire ring', effects=[dict(where='TO_RESIST', bitvector='RES_FIRE', duration=-1)])
        combat = FightHandler.__new__(FightHandler)
        combat.MobImmunity = self.enums.get('mobImmunity')
        combat.MobResistance = self.enums.get('mobResistance')
        combat.MobVulnerability = self.enums.get('mobVulnerability')
        self.effects.apply_item_effects(self.actor, ring)
        self.assertEqual('IS_RESISTANT', combat._check_immunity(self.actor, 'FIRE'))
        self.effects.remove_item_effects(self.actor, ring)
        self.assertEqual('IS_NORMAL', combat._check_immunity(self.actor, 'FIRE'))


class SkillProficiencyParityTests(SharedFixture, unittest.TestCase):
    def test_absent_zero_and_ineligible_skills_have_zero_rating(self):
        skill = self.skills['sneak']
        self.assertEqual(0, self.actor.skill_level('sneak'))
        for learned, level in [(0, 20), (90, 3)]:
            self.actor.level = level
            self.actor.set_learned('sneak', learned, create=True)
            self.assertEqual(0, self.skill_api.get_rating(self.actor, skill))

    def test_daze_drunk_order_and_final_clamping(self):
        self.actor.set_learned('sneak', 90, create=True)
        self.actor.status_flags.pulse_daze = 1
        self.actor.status_flags.drunk = 20
        self.assertEqual(54, self.skill_api.get_rating(self.actor, self.skills['sneak']))
        self.actor.status_flags.pulse_daze = 0
        self.actor.status_flags.drunk = 10
        self.assertEqual(90, self.skill_api.get_rating(self.actor, self.skills['sneak']))
        self.actor.set_learned('sneak', 150)
        self.assertEqual(100, self.skill_api.get_rating(self.actor, self.skills['sneak']))

    def test_unlearned_skill_is_denied_at_command_access_boundary(self):
        fight_api = FightApi.__new__(FightApi)
        fight_api.skill_api = self.skill_api
        self.assertFalse(fight_api._has_skill_access(self.actor, self.skills['sneak']))
        self.actor.set_learned('sneak', 1, create=True)
        self.assertTrue(fight_api._has_skill_access(self.actor, self.skills['sneak']))

    def test_npc_proficiency_keeps_level_formula_and_daze_penalty(self):
        npc = self.npc()
        npc.status_flags.pulse_daze = 1
        self.assertEqual(40, self.skill_api.get_rating(npc, self.skills['sneak']))

    def test_sneak_strict_roll_creates_content_defined_timed_affect(self):
        self.actor.set_learned('sneak', 60, create=True)
        with patch.object(self.skill_api.rng, 'number_percent', return_value=59), \
                patch.object(Ability, 'check_improve_by_name') as improve:
            self.movement.do_sneak(self.actor, self.context('sneak'))
        improve.assert_called_once_with(self.actor, 'sneak', True, 3)
        effect = self.actor.effects[0]
        self.assertEqual(('skill.sneak', 20, 20), (effect.type, effect.duration, effect.level))
        with patch.object(self.skill_api.rng, 'number_percent', return_value=60), \
                patch.object(Ability, 'check_improve_by_name') as improve:
            self.movement.do_sneak(self.actor, self.context('sneak'))
        improve.assert_called_once_with(self.actor, 'sneak', False, 3)
        self.assertEqual([], self.actor.effects)
        self.assertFalse(CharacterApi.is_affected_by_name(self.actor, self.enums.get('affectedBy'), 'AFF_SNEAK'))

    def test_sneak_does_not_roll_for_residual_innate_flag(self):
        self.flag(self.actor, 'AFF_SNEAK')
        with patch.object(self.skill_api.rng, 'number_percent') as roll, patch.object(Ability, 'check_improve_by_name') as improve:
            self.movement.do_sneak(self.actor, self.context('sneak'))
        roll.assert_not_called()
        improve.assert_not_called()

    def test_hide_clears_old_flag_before_failed_roll_and_can_succeed(self):
        self.actor.set_learned('hide', 50, create=True)
        self.flag(self.actor, 'AFF_HIDE')
        with patch.object(self.skill_api.rng, 'number_percent', return_value=50), patch.object(Ability, 'check_improve_by_name'):
            self.movement.do_hide(self.actor, self.context('hide'))
        self.assertFalse(CharacterApi.is_affected_by_name(self.actor, self.enums.get('affectedBy'), 'AFF_HIDE'))
        with patch.object(self.skill_api.rng, 'number_percent', return_value=49), patch.object(Ability, 'check_improve_by_name'):
            self.movement.do_hide(self.actor, self.context('hide'))
        self.assertTrue(CharacterApi.is_affected_by_name(self.actor, self.enums.get('affectedBy'), 'AFF_HIDE'))

    def test_sneak_expires_through_existing_effect_tick(self):
        self.actor.set_learned('sneak', 100, create=True)
        with patch.object(self.skill_api.rng, 'number_percent', return_value=1), patch.object(Ability, 'check_improve_by_name'):
            self.movement.do_sneak(self.actor, self.context('sneak'))
        self.actor.effects[0].duration = 0
        self.effects.tick_effects(self.actor)
        self.assertFalse(CharacterApi.is_affected_by_name(self.actor, self.enums.get('affectedBy'), 'AFF_SNEAK'))


class PerceptionParityTests(SharedFixture, unittest.TestCase):
    def test_hide_detect_hidden_and_fighting_exception(self):
        self.flag(self.victim, 'AFF_HIDE')
        self.assertFalse(CharacterApi.can_see(self.actor, self.victim, self.room))
        self.flag(self.actor, 'AFF_DETECT_HIDDEN')
        self.assertTrue(CharacterApi.can_see(self.actor, self.victim, self.room))
        self.flag(self.actor, 'AFF_DETECT_HIDDEN', False)
        self.victim.fighting = self.actor
        self.assertTrue(CharacterApi.can_see(self.actor, self.victim, self.room))

    def test_sneak_stat_level_formula_and_strict_endpoint(self):
        self.victim.set_learned('sneak', 60, create=True)
        self.flag(self.victim, 'AFF_SNEAK')
        self.victim.character_attributes.dexterity = 15
        self.actor.character_attributes.intelligence = 13
        # 60 + 15*3/2 - 13*2 - (20 - 20*3/2) = 66.
        with patch('api.CharacterApi.rng.number_percent', return_value=65) as roll:
            self.assertFalse(CharacterApi.can_see(self.actor, self.victim, self.room))
        roll.assert_called_once()
        with patch('api.CharacterApi.rng.number_percent', return_value=66):
            self.assertTrue(CharacterApi.can_see(self.actor, self.victim, self.room))

    def test_sneak_detect_hidden_skips_randomness(self):
        self.flag(self.victim, 'AFF_SNEAK')
        self.flag(self.actor, 'AFF_DETECT_HIDDEN')
        with patch('api.CharacterApi.rng.number_percent') as roll:
            self.assertTrue(CharacterApi.can_see(self.actor, self.victim, self.room))
        roll.assert_not_called()

    def test_outdoor_night_light_and_sector_exceptions(self):
        times = self.enums.get('timeAndWeather')
        for sunlight, expected in [(times.SUN_LIGHT, False), (times.SUN_RISE, False), (times.SUN_SET, True), (times.SUN_DARK, True)]:
            self.weather.weather_info.sunlight = sunlight
            self.assertEqual(expected, self.room.is_room_dark())
        self.room.light = 1
        self.assertFalse(self.room.is_room_dark())
        self.room.light = 0
        for sector in ['SECT_INSIDE', 'SECT_CITY']:
            self.room.sector_type = getattr(self.enums.get('sectorTypes'), sector)
            self.assertFalse(self.room.is_room_dark())
        self.room.room_flags = self.enums.get('roomFlags').ROOM_DARK
        self.assertTrue(self.room.is_room_dark())

    def test_night_character_and_object_vision_use_distinct_affects(self):
        self.weather.weather_info.sunlight = self.enums.get('timeAndWeather').SUN_DARK
        obj = item('gem')
        self.assertFalse(CharacterApi.can_see(self.actor, self.victim, self.room))
        self.assertFalse(ItemApi.can_see_object(self.room, self.actor, obj))
        self.flag(self.actor, 'AFF_INFRARED')
        self.assertTrue(CharacterApi.can_see(self.actor, self.victim, self.room))
        self.assertFalse(ItemApi.can_see_object(self.room, self.actor, obj))
        self.flag(self.actor, 'AFF_DARK_VISION')
        self.assertTrue(ItemApi.can_see_object(self.room, self.actor, obj))

    def test_room_lists_do_not_disclose_invisible_targets_or_objects(self):
        self.room.add_player_to_room(self.victim)
        self.flag(self.victim, 'AFF_INVISIBLE')
        invisible = item('hidden gem', extraFlags=str(self.enums.get('itemFlags').ITEM_INVIS))
        self.room.add_item_to_room(invisible)
        self.assertNotIn(self.victim.name, self.room.get_players_in_room(self.actor))
        self.assertEqual([], Room.item_description_lines(self.room, self.actor))
        self.flag(self.actor, 'AFF_DETECT_INVIS')
        self.assertIn(self.victim.name, self.room.get_players_in_room(self.actor))
        self.assertIn('hidden gem', ' '.join(Room.item_description_lines(self.room, self.actor)))

    def test_room_list_respects_wizinvis_even_for_holy_light(self):
        self.victim.status_flags.invis_level = 60
        self.room.add_player_to_room(self.victim)
        self.actor.status_flags.set_flag('act', self.enums.get('playerActBits').PLR_HOLYLIGHT)
        self.assertNotIn(self.victim.name, self.room.get_players_in_room(self.actor))

    def test_npc_observer_also_needs_infrared_in_darkness(self):
        npc = self.npc()
        self.weather.weather_info.sunlight = self.enums.get('timeAndWeather').SUN_DARK
        self.assertFalse(CharacterApi.can_see(npc, self.actor, self.room))
        self.flag(npc, 'AFF_INFRARED')
        self.assertTrue(CharacterApi.can_see(npc, self.actor, self.room))


class AutomaticRoomViewParityTests(SharedFixture, unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        super().setUp()
        self.bus = NS(send_to_character=AsyncMock(), text_to_message=lambda text: text)
        self.rooms_handler = RoomHandler(self.bus, NS(), self.registries)
        self.player_handler = PlayerHandler.__new__(PlayerHandler)
        self.player_handler.message_bus = self.bus
        self.player_handler.info_commands = NS(PlayerActBits=self.enums.get('playerActBits'))
        self.player_handler.print_players_in_room = AsyncMock()
        self.mobile_handler = NS(print_mobiles_in_room=AsyncMock())
        self.context = NS(room_handler=lambda: self.rooms_handler, mobile_handler=lambda: self.mobile_handler)

    async def test_automatic_view_blocks_blind_sleep_and_stun_without_room_disclosure(self):
        for reason in ['blind', 'sleeping', 'stunned']:
            with self.subTest(reason=reason):
                self.actor.status_flags.assign_bitfield('affected_by', 0)
                CharacterApi.set_position(self.actor, {'blind': 'POS_STANDING', 'sleeping': 'POS_SLEEPING', 'stunned': 'POS_STUNNED'}[reason])
                if reason == 'blind':
                    self.flag(self.actor, 'AFF_BLIND')
                self.bus.send_to_character.reset_mock()
                await self.player_handler._show_room_to_character(self.actor, self.room, self.context)
                self.assertEqual(self.command('look').render_message('to_char', reason), self.bus.send_to_character.call_args.args[1])
                self.player_handler.print_players_in_room.assert_not_called()

    async def test_dark_automatic_view_shows_only_character_perception_without_exits(self):
        self.weather.weather_info.sunlight = self.enums.get('timeAndWeather').SUN_DARK
        self.rooms_handler.print_exits = AsyncMock()
        await self.player_handler._show_room_to_character(self.actor, self.room, self.context)
        self.rooms_handler.print_exits.assert_not_called()
        self.player_handler.print_players_in_room.assert_awaited_once_with(self.actor)
        self.assertEqual(self.command('look').render_message('to_char', 'dark'), self.bus.send_to_character.call_args.args[1])

    async def test_holy_light_bypasses_blindness_and_darkness(self):
        self.flag(self.actor, 'AFF_BLIND')
        self.weather.weather_info.sunlight = self.enums.get('timeAndWeather').SUN_DARK
        self.actor.status_flags.set_flag('act', self.enums.get('playerActBits').PLR_HOLYLIGHT)
        self.assertTrue(await self.rooms_handler.print_room(self.actor.id, self.room))
        self.assertIn(self.room.name, self.bus.send_to_character.call_args.args[1])

    async def test_explicit_dark_look_still_shows_perceivable_characters(self):
        self.weather.weather_info.sunlight = self.enums.get('timeAndWeather').SUN_DARK
        info = Info.__new__(Info)
        info.room_registry = self.rooms
        info.interp_api = self.api
        self.player_handler.info_commands = info
        self.player_handler.room_registry = self.rooms
        context = self.context_for_look()
        await self.player_handler.do_look(self.actor, context)
        self.assertTrue(context.done)
        self.player_handler.print_players_in_room.assert_awaited_once_with(self.actor)
        self.mobile_handler.print_mobiles_in_room.assert_awaited_once_with(self.actor)

    async def test_explicit_look_autoexits_uses_room_handler_contract(self):
        info = Info.__new__(Info)
        info.room_registry = self.rooms
        info.interp_api = self.api
        info.PlayerActBits = self.enums.get('playerActBits')
        self.actor.status_flags.set_flag('act', info.PlayerActBits.PLR_AUTOEXIT)
        self.player_handler.info_commands = info
        self.player_handler.room_registry = self.rooms
        self.rooms_handler.print_exits = AsyncMock(spec=self.rooms_handler.print_exits)
        await self.player_handler.do_look(self.actor, self.context_for_look())
        self.rooms_handler.print_exits.assert_awaited_once_with(self.actor)

    def context_for_look(self):
        handlers = {'rh': self.rooms_handler, 'mh': self.mobile_handler}
        return Context(character=self.actor, command=self.command('look'), room=self.room,
                       result='', parameters=[], handler_service=NS(get_handler=handlers.get))


if __name__ == '__main__':
    unittest.main()
