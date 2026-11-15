import unittest
from copy import deepcopy
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock, patch

from tests import test_review_application_fixes as fixtures
from tests.test_immortal_priority_parity import mobile_entity
from tests import test_runtime_factories as item_fixtures
from api.AreaApi import AreaApi
from api.CharacterApi import CharacterApi
from api.CommunicationsApi import CommunicationsApi
from api.GameApi import GameApi
from api.SkillApi import SkillApi
from api.SpellApi import SpellApi
from api.WizApi import WizApi
from area.Room import Room
from combat.CombatHandler import FightHandler
from combat.CombatRegistry import CombatRegistry
from devtools.collection_query import load_collections
from game.WizHandler import WizHandler
from interp.CommandAccess import CommandAccess
from interp.InterpHandler import InterpHandler
from interp.commands.Communications import Communications
from interp.commands.Info import Info
from interp.commands.Movement import Movement
from interp.commands.Object import Object
from interp.commands.Wiz import Wiz
from item.Effect import Effect
from item.EffectHandler import EffectHandler
from mobile.Dice import Dice
from mobile.ArmorClass import ArmorClass
from mobile.MobileFactory import MobileFactory
from mobile.MobileHandler import MobileHandler
from mobile.PetSnapshot import restore_pet, snapshot_pet
from player.CharacterRegistry import CharacterRegistry
from player.PlayerHandler import PlayerHandler
from server.connection.ConnectionManager import ConnectionManager
from server.handlers.ConnectionHandler import ConnectionHandler
from server.protocol.Message import Message, MessageType
from server.session.SessionHandler import SessionHandler
from server.session.SessionState import SessionStatus
from skill.Skill import Skill
from skill.Spell import Spell
from skill.SpellContext import SpellContext
from util.WizUtil import WizUtil


class TargetingFixture(fixtures.RuntimeFixture):
    def setUp(self):
        super().setUp()
        self.actor.level = self.actor.trust = 60
        self.actor.role = 'immortal'
        CharacterApi.set_act_flags(self.actor, self.enums.get('playerActBits').PLR_HOLYLIGHT)
        self.room.vnum, self.room.name, self.room.light = '1', 'Origin', 1
        self.remote = Room(id='remote', area_id='other', vnum='2', name='Destination', light=1)
        self.room_list = [self.room, self.remote]
        self.rooms = NS(all_rooms=lambda: self.room_list, get_or_none=self.room_lookup)
        self.registry = CharacterRegistry()
        self.registry.register(self.actor)
        self.sessions, self.manager = SessionHandler(), ConnectionManager()
        self.registries = NS(character_registry=self.registry, room_registry=self.rooms)
        self.wiz_handler = WizHandler(self.registries, self.sessions, self.manager)
        self.wiz = Wiz.__new__(Wiz)
        self.wiz.character_registry = self.registry
        self.wiz.room_registry = self.rooms
        self.wiz.interp_api = self.api
        self.wiz.wiz_handler = self.wiz_handler
        self.wiz.CommFlagsEnum = self.enums.get('commFlags')
        self.wiz.PlayerActBitsEnum = self.enums.get('playerActBits')
        self.wiz.character_service = NS(queue_save_character=Mock())

    def room_lookup(self, **kwargs):
        return next((room for room in self.room_list if all(str(getattr(room, name)) == str(value)
                                                          for name, value in kwargs.items())), None)

    def player(self, identifier, name=None, room=None, live=True):
        player = self.character(identifier)
        player.name = name or identifier
        player.room_id = (room or self.remote).id
        self.registry.register(player)
        if live:
            (room or self.remote).add_player_to_room(player)
        return player

    def context(self, name, text=''):
        context = super().context(name, text)
        ph = NS(character_registry=self.registry, room_registry=self.rooms)
        context.handler_service = NS(get_handler=lambda key: self.wiz_handler if key == 'wh' else ph)
        return context

    def lookup(self, selector, **kwargs):
        return WizUtil.find_world_entity(self.registry, self.rooms, selector, observer=self.actor, **kwargs)

    def item(self, identifier, name=None):
        item = item_fixtures.RuntimeFactoryTests().item(identifier)
        item.name = name or identifier
        return item


class WorldTargetingTests(TargetingFixture, unittest.TestCase):
    def test_loaded_mobile_receives_live_room_and_area_identity(self):
        mob = mobile_entity('loaded', self.actor.status_flags)
        mob.room_id, mob.area_id = '', 'prototype-area'
        self.wiz.mobile_registry = NS(get_or_none=lambda **kw: mob)
        with patch('interp.commands.Wiz.MobileFactory.create', return_value=mob):
            self.wiz.do_load(self.actor, self.context('load', 'mob 1'))
        self.assertEqual((mob.room_id, mob.area_id), (self.room.id, self.room.area_id))
        self.assertIs(self.lookup('loaded'), mob)

    def test_cached_offline_retired_and_stale_membership_are_not_world_targets(self):
        self.player('offline', live=False)
        retired = self.player('retired')
        retired.world_retired = True
        stale = self.player('stale')
        stale.room_id = 'missing'
        for name in ('offline', 'retired', 'stale'):
            self.assertIsNone(self.lookup(name))
        self.assertIsNone(WizUtil.find_world_entity(self.registry, None, 'offline'))

    def test_local_priority_visible_ordinals_and_world_fallback(self):
        first = self.player('first', 'royal elite guard', self.room)
        second = self.player('second', 'royal elite guard', self.room)
        remote = self.player('third', 'royal elite guard')
        self.assertIs(self.lookup('roy el'), first)
        self.assertIs(self.lookup('2.guard'), second)
        self.assertIs(self.lookup('3.guard'), remote)
        first.status_flags.invis_level = 61
        self.assertIs(self.lookup('guard'), second)
        self.assertIs(self.lookup('2.guard'), remote)
        self.assertIsNone(self.lookup('0.guard'))

    def test_self_and_role_filters_use_the_actual_observer(self):
        mob = mobile_entity('guard', self.actor.status_flags)
        mob.room_id = self.room.id
        self.room.add_mobile_to_room(mob)
        self.assertIs(self.lookup('guard'), mob)
        self.assertIsNone(self.lookup('guard', include_mobiles=False))
        self.assertIs(self.lookup('self'), self.actor)
        self.assertIsNone(self.lookup('self', include_players=False))

    def test_guards_and_handler_apply_to_same_visible_ordinal(self):
        first = self.player('one', 'guard', self.room)
        second = self.player('two', 'guard', self.room)
        result = self.wiz.do_freeze(self.actor, self.context('freeze', '2.guard'))
        bit = self.enums.get('playerActBits').PLR_FREEZE
        self.assertIs(result['victim'], second)
        self.assertFalse(CharacterApi.is_set(first.status_flags.act, bit))
        self.assertTrue(CharacterApi.is_set(second.status_flags.act, bit))

    def test_hidden_and_offline_targets_are_rejected_before_side_effects(self):
        session = self.sessions.create_session('actor')
        session.character = self.actor
        hidden = self.player('hidden')
        hidden.status_flags.invis_level = 61
        offline = self.player('offline', live=False)
        for command in ('freeze', 'restore', 'deny', 'switch', 'snoop'):
            for name in ('hidden', 'offline'):
                with self.subTest(command=command, target=name):
                    result = self.wiz.execute(self.actor, self.context(command, name))
                    self.assertIn("aren't", result['to_char'])
        self.wiz.character_service.queue_save_character.assert_not_called()
        self.assertFalse(hidden.world_retired)
        self.assertFalse(offline.world_retired)

    def test_force_groups_use_live_pcs_but_preserve_rom_bulk_visibility_rule(self):
        mortal = self.player('mortal')
        hidden_hero = self.player('hero')
        hidden_hero.level = 51
        hidden_hero.status_flags.invis_level = 61
        self.player('offline', live=False)
        mob = mobile_entity('mob', self.actor.status_flags)
        mob.room_id = self.remote.id
        self.remote.add_mobile_to_room(mob)
        for group, expected in (('all', {mortal.id, hidden_hero.id}), ('players', {mortal.id}), ('gods', {hidden_hero.id})):
            view = self.api.build_interp_view(self.context('force', group + ' smile'))
            self.assertEqual({v.id for v in WizApi.force_targets(view)}, expected)

    def test_floor_inventory_worn_then_world_item_search(self):
        floor = self.item('floor', 'gem jewel')
        inventory = self.item('inventory', 'gem jewel')
        worn = self.item('worn', 'gem jewel')
        remote = self.item('remote', 'gem jewel')
        self.room.add_item_to_room(floor)
        self.actor.add_item(inventory)
        self.actor.equip_item(worn, 'head')
        self.remote.add_item_to_room(remote)
        find = lambda token: WizUtil.find_world_item(self.registry, self.rooms, token, observer=self.actor)
        self.assertIs(find('gem'), floor)
        self.room.remove_item_from_room(floor)
        self.assertIs(find('gem'), inventory)
        self.actor.loot.remove(inventory)
        self.assertIs(find('gem'), worn)
        self.actor.unequip_item('head')
        self.actor.loot.clear()
        self.assertIs(find('gem'), remote)

    def test_nested_and_carried_items_are_live_but_offline_inventory_is_not(self):
        carrier = self.player('carrier')
        bag = self.item('bag')
        gem = self.item('gem')
        bag.contains = [gem]
        carrier.add_item(bag)
        offline = self.player('offline', live=False)
        offline.add_item(self.item('lost'))
        self.assertIs(WizUtil.find_world_item(self.registry, self.rooms, 'gem', observer=self.actor), gem)
        self.assertIsNone(WizUtil.find_world_item(self.registry, self.rooms, 'lost', observer=self.actor))

    def test_invisible_items_are_excluded_before_ordinal_counting(self):
        CharacterApi.unset_act_flags(self.actor, self.enums.get('playerActBits').PLR_HOLYLIGHT)
        hidden = self.item('hidden', 'gem')
        hidden.extra_flags = int(self.enums.get('itemFlags').ITEM_INVIS)
        visible = self.item('visible', 'gem')
        self.remote.add_item_to_room(hidden)
        self.remote.add_item_to_room(visible)
        self.assertIs(WizUtil.find_world_item(self.registry, self.rooms, 'gem', observer=self.actor), visible)
        self.assertIsNone(WizUtil.find_world_item(self.registry, self.rooms, '2.gem', observer=self.actor))

    def test_location_adapters_use_visible_live_targets_and_floor_objects(self):
        hidden = self.player('hidden')
        hidden.status_flags.invis_level = 61
        self.player('offline', live=False)
        floor = self.item('obelisk')
        self.remote.add_item_to_room(floor)
        for name, expected in (('hidden', None), ('offline', None), ('obelisk', self.remote), ('2', self.remote)):
            view = self.api.build_interp_view(self.context('goto', name))
            self.assertIs(WizApi.location(view), expected)
        self.remote.remove_item_from_room(floor)
        self.actor.add_item(floor)
        self.assertIsNone(WizApi.location(self.api.build_interp_view(self.context('goto', 'obelisk'))))


class SwitchedIdentityTests(TargetingFixture, unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        super().setUp()
        self.body = mobile_entity('body', self.actor.status_flags)
        self.body.room_id = self.room.id
        self.room.add_mobile_to_room(self.body)
        self.registry.register(self.body)
        session = self.sessions.create_session('controller')
        session.character = self.actor
        session.status = SessionStatus.PLAYING
        self.manager.add_connection(NS(session_id=session.session_id, is_closed=lambda: False))
        self.manager.bind_character(self.actor.id, session.session_id)
        self.session = session

    def handler(self):
        handler = PlayerHandler.__new__(PlayerHandler)
        handler.command_audit = None
        handler.interp_api = self.api
        handler.wiz_handler = self.wiz_handler
        handler.message_bus = NS(connection_manager=self.manager, send_to_character=AsyncMock(), send_to_room=AsyncMock(),
                                 text_to_message=lambda text: text)
        handler._send_prompt = AsyncMock()
        return handler

    async def test_switch_acknowledgment_and_diagnostics_reach_controlled_body(self):
        handler = self.handler()
        context = self.context('switch', 'body')
        payload = self.wiz.do_switch(self.actor, context)
        self.assertIs(context.character, self.body)
        await handler._emit_standard_payload(self.body, payload, context)
        self.assertEqual(handler.message_bus.send_to_character.await_args_list[0].args, (self.body.id, 'Ok.\r\n'))
        await handler._emit_standard_payload(self.body, {'to_char': 'diagnostic\r\n'}, context)
        handler.message_bus.send_to_character.assert_awaited_with(self.body.id, 'diagnostic\r\n')

    async def test_controller_trust_is_shared_by_access_guards_visibility_and_clone_checks(self):
        self.wiz_handler.switch_character(self.actor, self.body)
        self.assertEqual(CharacterApi.get_trust(self.body), 60)
        self.assertIsNone(CommandAccess.check(self.body, self.command('force')))
        context = self.context('force', 'all smile')
        context.character = self.body
        self.assertFalse(WizApi.force_insufficient_level(self.api.build_interp_view(context)))
        self.assertTrue(WizUtil.can_clone_object(self.body, NS(level=60, cost=99999)))
        target = self.player('invisible')
        target.status_flags.invis_level = 59
        self.assertIs(WizUtil.find_world_entity(self.registry, self.rooms, 'invisible', observer=self.body), target)
        self.wiz_handler.return_character(self.body)
        self.assertEqual(CharacterApi.get_trust(self.body), self.body.level)
        self.assertIs(self.session.character, self.actor)
        self.assertIsNone(self.manager.get_connection_by_character(self.body.id))

    async def test_uncontrolled_npc_does_not_receive_player_output(self):
        handler = self.handler()
        await handler._emit_standard_payload(self.body, {'to_char': 'unbound'}, self.context('stat'))
        handler.message_bus.send_to_character.assert_not_awaited()

    async def test_ordered_wear_all_and_score_keep_connection_open(self):
        fight, *_ = self.death_fixture()
        self.actor.level = self.actor.trust = 20
        self.actor.role = 'player'
        self.body.level = 25
        self.body.mana = self.body.max_mana = 20
        self.body.armor_class = ArmorClass(pierce=100, bash=100, slash=100, exotic=100)
        self.body.master = self.actor
        self.body.status_flags.set_flag('affected_by', fight.AffectBits.AFF_CHARM)
        ring = self.item('ring')
        ring.wear_flags = str(self.enums.get('wearFlags').ITEM_WEAR_FINGER.value)
        self.body.add_item(ring)

        commands = {name: self.command(name) for name in ('order', 'wear', 'score')}
        self.registries.interp_registry = NS(
            all_commands=lambda: list(commands.values()), get_or_none=lambda *, name: commands.get(name))
        self.registries.social_registry = None
        player = self.handler()
        player.room_registry, player.interp_registry = self.rooms, self.registries.interp_registry
        player.communications_commands = Communications.__new__(Communications)
        player.communications_commands.communications_api = CommunicationsApi
        player.communications_commands.interp_api = self.api
        player.info_commands = Info.__new__(Info)
        player.object_commands = Object.__new__(Object)
        player.object_commands.room_registry, player.object_commands.interp_api = self.rooms, self.api
        player.object_commands.item_flags = self.enums.get('itemFlags')
        player.object_commands.wear_flags = self.enums.get('wearFlags')
        player.object_commands.effect_handler = fight.effect_handler
        interpreter = InterpHandler(
            NS(get=lambda _: self.manager), player.message_bus, self.registries,
            NS(social_handler=None, get_handler={'ph': player, 'wh': self.wiz_handler}.get))
        connection_handler = ConnectionHandler.__new__(ConnectionHandler)
        connection_handler.command_handler = interpreter
        connection_handler.session_handler = self.sessions
        connection_handler.message_bus = player.message_bus
        player.message_bus.send_prompt = AsyncMock()
        connection_handler.logger = Mock()
        connection_handler._get_area_and_room = lambda _: (None, self.room)
        connection_handler._wait_for_action_ready = AsyncMock(return_value=True)
        connection_handler._wait_for_message = AsyncMock(side_effect=[
            *(Message(MessageType.GAME, {'text': command}) for command in
              ('order body wear all', 'order body score', 'score')),
            None,
        ])
        connection = self.manager.get_connection_by_character(self.actor.id)
        await connection_handler._game_loop(connection, self.session, None, self.actor)
        self.assertEqual(4, connection_handler._wait_for_message.await_count)
        connection_handler.logger.error.assert_not_called()
        self.assertIsNotNone(self.body.equipped_slot_of(ring))

        self.actor.level = self.actor.trust = 60
        self.actor.role = 'immortal'
        self.wiz_handler.switch_character(self.actor, self.body)
        await interpreter.handle_command(self.body, 'score')
        score = player.message_bus.send_to_character.await_args.args
        self.assertEqual(self.body.id, score[0])
        self.assertIn('Class: mobile', score[1])
        self.assertIn('Armor: pierce:', score[1])

    async def test_spawned_shopkeeper_replenishes_configured_wealth(self):
        standing = CharacterApi.pos_value('POS_STANDING')
        prototype = MobileFactory.from_data({
            'vnum': '3070', 'name': 'potion-brewer', 'level': 32, 'size': 'medium', 'gold': 5000,
            'startPos': standing, 'armorClass': '{"bash": 0, "pierce": 0, "slash": 0, "exotic": 0}',
        }, {})
        keeper = MobileFactory.create(prototype, self.enums)
        self.room.add_mobile_to_room(keeper)
        keeper.gold = keeper.silver = 0
        handler = MobileHandler.__new__(MobileHandler)
        handler.room_registry, handler.logger = self.rooms, Mock()
        handler.act_bits = self.enums.get('actBits')
        handler.area_registry = NS(get_or_none=lambda **_: NS(empty=False))
        handler.shop_registry = NS(find_by_keeper_vnum=lambda vnum: object() if vnum == '3070' else None)
        handler.execute_special_function = AsyncMock(return_value=False)
        handler._execute_generic_special = AsyncMock()
        handler.rng = Mock(number_range=Mock(return_value=20))

        await handler.mobile_update()
        self.assertEqual((0, 2), (keeper.gold, keeper.silver))
        self.assertEqual(2, handler.rng.number_range.call_count)
        keeper.gold = 50
        keeper.silver = 0
        await handler.mobile_update()
        self.assertEqual((50, 0), (keeper.gold, keeper.silver))
        self.assertEqual(2, handler.rng.number_range.call_count)

    async def test_victim_reply_prompts_reach_switched_body(self):
        self.wiz_handler.switch_character(self.actor, self.body)
        handler = self.handler()
        await handler._emit_standard_payload(self.actor, {'to_victim': 'reply', 'victim': self.body}, self.context('pecho'))
        handler.message_bus.send_to_character.assert_awaited_once_with(self.body.id, 'reply')
        handler._send_prompt.assert_awaited_once()

    async def test_violence_update_delivers_direct_messages_and_prompt_to_switched_body(self):
        fight, player, *_ = self.death_fixture()
        self.wiz_handler.switch_character(self.actor, self.body)
        fight.message_bus = self.handler().message_bus
        fight.message_bus.send_prompt = AsyncMock()
        area = NS(id=self.room.area_id)
        fight.area_registry = NS(get_or_none=lambda **_: area)
        fight.multi_hit = Mock(side_effect=lambda attacker, victim, **_: fight.dam_message(attacker, victim, 9))
        fight.check_assist = Mock(return_value=[])

        for attacker, victim, controller_channel in [(self.body, player, 'to_char'), (player, self.body, 'to_victim')]:
            with self.subTest(controller_channel=controller_channel):
                fight.set_fighting(attacker, victim, self.room.id)
                await fight.violence_update()
                expected = fight.dam_message(attacker, victim, 9)[controller_channel]
                fight.message_bus.send_to_character.assert_any_await(self.body.id, expected)
                fight.message_bus.send_prompt.assert_any_await(self.body, area, self.room)
                fight.stop_fighting(attacker, both=False)
                fight.message_bus.send_to_character.reset_mock()
                fight.message_bus.send_prompt.reset_mock()

        self.wiz_handler.return_character(self.body)
        fight.set_fighting(self.body, player, self.room.id)
        fight.set_fighting(player, self.body, self.room.id)
        await fight.violence_update()
        self.assertEqual({player.id}, {call.args[0] for call in fight.message_bus.send_to_character.await_args_list})
        fight.message_bus.send_prompt.assert_any_await(player, area, self.room)
        self.assertNotIn(self.body, [call.args[0] for call in fight.message_bus.send_prompt.await_args_list])

    async def test_standard_fight_payload_retains_switched_victim(self):
        fight, attacker, *_ = self.death_fixture()
        self.wiz_handler.switch_character(self.actor, self.body)
        handler = self.handler()
        fight.message_bus = handler.message_bus
        result = fight.dam_message(attacker, self.body, 9)
        payload = fight.build_round_payload(attacker, self.body, self.room, result)
        await handler._handle_fight_payload(attacker, self.context('kill'), payload)
        handler.message_bus.send_to_character.assert_any_await(self.body.id, result['to_victim'])
        handler._send_prompt.assert_awaited_once()

    async def test_magic_missile_delivers_direct_hit_to_switched_victim(self):
        fight, attacker, *_ = self.death_fixture()
        player_handler = self.handler()
        mobile_handler = MobileHandler.__new__(MobileHandler)
        mobile_handler.message_bus = player_handler.message_bus
        fight.is_safe = Mock(return_value=(False, ''))
        fight.check_killer = Mock(return_value={})
        fight._check_immunity = Mock(return_value='IS_NORMAL')
        self.body.hit = self.body.max_hit = 50
        spell_api = SpellApi(fight.effect_handler, self.api, connection_manager=self.manager)
        spells = load_collections(fixtures.ROOT / 'resources/collections', ['spells'])['spells']
        spell = Spell.from_json(deepcopy(next(doc for doc in spells.documents if doc['name'] == 'magic missile')))
        self.wiz_handler.switch_character(self.actor, self.body)

        for switched in (True, False):
            if not switched:
                self.wiz_handler.return_character(self.body)
            with self.subTest(switched=switched):
                context = SpellContext(actor=attacker, spell=spell, room=self.room, target=self.body,
                                       target_kind='char', source='player', cast_level=15,
                                       handler=NS(fight_handler=fight, spell_api=spell_api))
                with patch.object(spell_api, 'saves_spell', return_value=False), \
                        patch('api.SpellApi.random.randint', side_effect=lambda low, high: low):
                    spell_api.execute_lambdas(context)
                self.assertEqual(self.body.hit, 47 if switched else 44)
                victim_lines = [entry['to_victim'] for entry in context.payloads if entry.get('victim') is self.body]
                if switched:
                    self.assertEqual(len(victim_lines), 1)
                    self.assertIn('magic missile', victim_lines[0])
                    await player_handler._emit_standard_payloads(attacker, context.payloads, self.context('cast'))
                    player_handler.message_bus.send_to_character.assert_any_await(self.body.id, victim_lines[0])
                    player_handler._send_prompt.assert_awaited_once()
                    mobile_handler.message_bus.send_to_character.reset_mock()
                    for entry in context.payloads:
                        await mobile_handler._handle_payload(entry)
                    mobile_handler.message_bus.send_to_character.assert_awaited_once_with(self.body.id, victim_lines[0])
                else:
                    self.assertEqual(victim_lines, [])

    def death_fixture(self):
        self.body.hit = self.body.max_hit = 1
        self.body.character_attributes = deepcopy(self.actor.character_attributes)
        self.body.default_pos = CharacterApi.pos_value('POS_STANDING')
        CharacterApi.set_position(self.body, 'POS_STANDING')
        self.actor.status_flags.pulse_wait = 0
        killer = self.player('killer', room=self.room)
        killer.level = killer.trust = self.actor.level
        loot = self.item('carried')
        self.body.add_item(loot)
        prototype = NS(killed=0)
        fight = FightHandler.__new__(FightHandler)
        fight.logger = Mock()
        fight.registry_service = self.registries
        fight.room_registry = self.rooms
        fight.combat_registry = CombatRegistry()
        fight.wiz_handler = self.wiz_handler
        fight.effect_handler = EffectHandler(self.enums)
        fight.PositionsEnum = self.enums.get('positions')
        fight.AffectBits = self.enums.get('affectedBy')
        fight.ActBits = self.enums.get('actBits')
        fight.RoomFlags = self.enums.get('roomFlags')
        fight.shop_registry = NS(find_by_keeper_vnum=lambda _: None)
        fight.PlayerActBits = self.enums.get('playerActBits')
        fight.WellKnownObjectVnums = self.enums.get('wellKnownObjectVnums')
        fight.item_registry = NS(get=lambda **_: self.item('corpse', 'corpse'))
        fight.mobile_registry = NS(get_or_none=lambda **_: prototype)
        fight.mobile_handler = NS(record_mobile_kill=Mock())
        fight.death_handler = None
        fight.death_cry = Mock(return_value=[])
        fight.escape_handler = None
        fight.group_gain = Mock(return_value={'xp_gain': 0})
        self.wiz.fight_handler = fight
        return fight, killer, loot, prototype

    async def assert_return_after_death(self, fight, loot, prototype):
        self.assertIs(self.session.character, self.actor)
        self.assertTrue(self.manager.owns_character(self.actor.id, self.session.session_id))
        self.assertIsNone(self.manager.get_connection_by_character(self.body.id))
        self.assertNotIn('switched_original', self.session.metadata)
        self.assertNotIn('switched_original_id', self.session.metadata)
        self.assertNotIn('controller_original', self.body.context)
        self.assertNotIn('controller_original_id', self.body.context)
        self.assertNotIn(self.body.id, self.room.mobiles)
        self.assertIsNone(self.registry.get_or_none(id=self.body.id))
        corpse, = self.room.contents.values()
        self.assertEqual([loot], corpse.contains)
        self.assertEqual(1, prototype.killed)
        fight.mobile_handler.record_mobile_kill.assert_called_once_with(self.body)

        connection_handler = ConnectionHandler.__new__(ConnectionHandler)
        connection_handler.session_handler = self.sessions
        connection_handler.command_handler = NS(handle_command=AsyncMock())
        connection_handler.message_bus = NS(send_prompt=AsyncMock())
        connection_handler.logger = Mock()
        connection_handler._get_area_and_room = lambda _: (None, self.room)
        connection_handler._wait_for_message = AsyncMock(side_effect=[
            Message(MessageType.GAME, {'text': 'look'}), None,
        ])
        connection = self.manager.get_connection_by_character(self.actor.id)
        connection.is_closed = lambda: False
        await connection_handler._game_loop(connection, self.session, None, self.body)
        connection_handler.command_handler.handle_command.assert_awaited_once_with(self.actor, 'look')

    async def test_lethal_damage_returns_controller_to_original_body(self):
        fight, killer, loot, prototype = self.death_fixture()
        self.wiz_handler.switch_character(self.actor, self.body)
        result = fight.damage(killer, self.body, 1, show=False)
        self.assertTrue(result['killed'])
        await self.assert_return_after_death(fight, loot, prototype)

    def area_attack_fixture(self):
        fight, *_ = self.death_fixture()
        self.remote.vnum = '3001'
        fight.OffenseTypes = self.enums.get('offenseTypes')
        fight.npc_skill_handler = None
        fight._skill_percent = Mock(return_value=0)
        self.body.status_flags.set_flag('off', fight.OffenseTypes.OFF_AREA_ATTACK)
        self.body.status_flags.set_flag('affected_by', fight.AffectBits.AFF_HASTE)
        primary = self.player('primary', room=self.room)
        secondary = self.player('secondary', room=self.room)
        fight.set_fighting(self.body, primary, self.room.id)
        fight.set_fighting(primary, self.body, self.room.id)
        fight.set_fighting(secondary, self.body, self.room.id)
        fight.dam_message = lambda _actor, victim, *_args, **_kwargs: {
            'to_char': '', 'to_room': '', 'to_victim': f'hit for {victim.name}',
        }
        return fight, primary, secondary

    async def test_lethal_area_hit_delivers_to_secondary_between_primary_swings(self):
        fight, primary, secondary = self.area_attack_fixture()
        secondary.hit = 1
        fight.one_hit = lambda actor, victim, dt: fight.damage(actor, victim, 12 if victim is secondary else 1)
        fight.death_cry.return_value = [{'victim': secondary, 'to_victim': 'death aftermath'}]
        fight.message_bus = self.handler().message_bus

        result = fight.mob_hit(self.body, primary)
        self.assertFalse(result['killed'])
        self.assertIn(primary.id, self.room.characters)
        self.assertIn(secondary.id, self.remote.characters)
        await fight.emit_round_payload(self.body, fight.build_round_payload(self.body, primary, self.room, result))
        self.assertEqual(
            [(primary.id, 'hit for primary'), (secondary.id, 'hit for secondary'),
             (secondary.id, 'death aftermath'), (primary.id, 'hit for primary')],
            [call.args for call in fight.message_bus.send_to_character.await_args_list],
        )

    def test_lethal_primary_hit_ends_round_before_area_sweep(self):
        fight, primary, secondary = self.area_attack_fixture()
        primary.hit = 1
        fight.one_hit = Mock(side_effect=lambda actor, victim, dt: fight.damage(actor, victim, 12))
        result = fight.mob_hit(self.body, primary)
        self.assertTrue(result['killed'])
        self.assertIn(primary.id, self.remote.characters)
        self.assertIn(secondary.id, self.room.characters)
        fight.one_hit.assert_called_once_with(self.body, primary, dt='TYPE_HIT')

    def test_mobile_bonus_follows_posture_and_scales_with_proficiency(self):
        fight, victim, *_ = self.death_fixture()
        prototype = MobileFactory.from_data({
            'id': '3700', 'name': 'acolyte', 'level': 30, 'size': 'medium',
            'armorClass': '{"bash": 0, "pierce": 0, "slash": 0, "exotic": 0}',
            'damageDice': {'number': 2, 'type': 4, 'bonus': 30},
        }, {})
        attacker = MobileFactory.create(prototype, self.enums)
        self.assertEqual(Dice(2, 4, 30), attacker.damage_dice)
        self.assertEqual(30, attacker.dam_roll)
        fight.rng = Mock(dice=Mock(return_value=8))
        fight.WeaponTypes = self.enums.get('weaponType')
        fight._skill_percent = Mock(return_value=0)
        fight._strength_combat_bonus = Mock(return_value=6)
        weapon = NS(value1=2, value2=4, value4=0)

        CharacterApi.set_position(victim, 'POS_RESTING')
        self.assertEqual(48, fight._attack_damage(attacker, victim, skill=100))
        self.assertEqual(30, fight._attack_damage(attacker, victim, skill=50))
        CharacterApi.set_position(victim, 'POS_STANDING')
        self.assertEqual(44, fight._attack_damage(attacker, victim, weapon=weapon, skill=100))

        attacker.dam_roll += 4
        snapshot = snapshot_pet(attacker, CharacterApi.pos_value('POS_FIGHTING'), CharacterApi.pos_value('POS_STANDING'))
        self.assertEqual(34, restore_pet(snapshot, victim).dam_roll)
        snapshot.pop('damageBonusInDamRoll')
        snapshot['damRoll'] = 4
        self.assertEqual(34, restore_pet(snapshot, victim).dam_roll)

    def test_authored_mobile_hit_roll_survives_spawn_equipment_clone_and_pet_restore(self):
        fight, owner, *_ = self.death_fixture()
        for fields, hit_roll in [
            ({'hitroll': 10}, 10),
            ({'hitroll': '-5'}, -5),
            ({'hitRoll': 0, 'hitroll': 10}, 0),
        ]:
            with self.subTest(fields=fields):
                prototype = MobileFactory.from_data({
                    'vnum': '3700', 'name': 'acolyte', 'level': 30, 'size': 'medium',
                    'armorClass': '{"bash": 0, "pierce": 0, "slash": 0, "exotic": 0}',
                    **fields,
                }, {})
                mob = MobileFactory.create(prototype, self.enums)
                self.assertEqual(hit_roll, prototype.hit_roll)
                self.assertEqual(hit_roll, mob.hit_roll)
                with patch.object(fight, '_strength_combat_bonus', return_value=0):
                    self.assertEqual(hit_roll, fight._current_hitroll(mob))
                    before = fight._thac0(mob, 'TYPE_HIT', 100)
                    ring = self.item('accuracy-ring')
                    ring.effects = [Effect(where='TO_OBJECT', location='APPLY_HITROLL', modifier=3, duration=-1)]
                    mob.equip_item(ring, 'finger1')
                    fight.effect_handler.apply_item_effects(mob, ring)
                    self.assertEqual(hit_roll + 3, fight._current_hitroll(mob))
                    self.assertEqual(before - 3, fight._thac0(mob, 'TYPE_HIT', 100))

                clone = MobileFactory.copy_instance(mob, self.enums)
                self.assertEqual(hit_roll + 3, clone.hit_roll)
                fight.effect_handler.remove_item_effects(mob, ring)
                mob.unequip_item('finger1')
                mob.remove_item(ring)
                self.assertEqual(hit_roll, mob.hit_roll)
                fight.effect_handler.apply_effect(mob, Effect(
                    type='spell.bless', where='TO_AFFECTS', location='APPLY_HITROLL', modifier=2, duration=3))
                snapshot = snapshot_pet(mob, CharacterApi.pos_value('POS_FIGHTING'),
                                        CharacterApi.pos_value('POS_STANDING'))
                restored = restore_pet(snapshot, owner)
                self.assertEqual(hit_roll + 2, restored.hit_roll)
                fight.effect_handler.affect_strip(restored, 'spell.bless')
                self.assertEqual(hit_roll, restored.hit_roll)

    def test_melee_and_score_omit_dexterity_armor_below_resting(self):
        fight, attacker, *_ = self.death_fixture()
        victim = self.player('defender', room=self.room)
        victim.level = victim.trust = 25
        victim.character_attributes.dexterity = 25
        victim.armor_class.bashing = 130
        armor = self.item('body-armor')
        armor.item_type, armor.value1 = 'armor', '10'
        victim.equip_item(armor, 'torso')
        fight.room_registry = NS(get=self.room_lookup)
        fight.WeaponClass = self.enums.get('weaponClass')
        fight._attack_damage_type = Mock(return_value='DAM_BASH')
        fight._weapon_skill_total = Mock(return_value=100)
        fight._thac0 = Mock(return_value=20)
        fight._to_hit_roll = Mock(return_value=5)
        fight._attack_damage = Mock(return_value=10)
        fight.damage = Mock(return_value={})

        cases = [('POS_STANDING', 10, 0), ('POS_RESTING', 10, 0),
                 ('POS_SLEEPING', 100, 10), ('POS_STUNNED', 100, 10)]
        with patch('combat.CombatHandler.Ability.check_improve_by_name'):
            for position, raw_armor, damage in cases:
                with self.subTest(position=position):
                    CharacterApi.set_position(victim, position)
                    self.assertEqual(raw_armor, victim.armor_class.get_ac(victim, 1))
                    self.assertEqual(raw_armor // 10, fight._victim_ac_for_damage_type(victim, 'DAM_BASH'))
                    fight.one_hit(attacker, victim)
                    self.assertEqual(damage, fight.damage.call_args.args[2])

    def test_followup_damage_restores_fighting_posture_without_replacing_opponent(self):
        fight, attacker, *_ = self.death_fixture()
        victim = self.player('victim', room=self.room)
        fight.set_fighting(victim, self.body, self.room.id)
        fight.rng = Mock(dice=Mock(return_value=8))
        fight._skill_percent = Mock(return_value=0)
        fight._strength_combat_bonus = Mock(return_value=0)
        self.body.damage_dice = Dice(2, 4, 0)
        CharacterApi.set_position(victim, 'POS_RESTING')

        self.assertEqual(12, fight._attack_damage(self.body, victim, skill=100))
        fight.damage(attacker, victim, 1)
        self.assertIs(victim.fighting, self.body)
        self.assertEqual(CharacterApi.pos_value('POS_FIGHTING'), CharacterApi.position_value(victim))
        self.assertEqual(8, fight._attack_damage(self.body, victim, skill=100))

        victim.hit = 0
        CharacterApi.set_position(victim, 'POS_STUNNED')
        fight.damage(attacker, victim, 0)
        self.assertEqual(CharacterApi.pos_value('POS_STUNNED'), CharacterApi.position_value(victim))

    async def test_slay_returns_controller_to_original_body(self):
        fight, killer, loot, prototype = self.death_fixture()
        self.wiz_handler.switch_character(self.actor, self.body)
        self.wiz.do_slay(killer, self.context('slay', 'body'))
        await self.assert_return_after_death(fight, loot, prototype)

    def test_player_death_extracts_pet_and_preserves_ordinary_followers(self):
        fight, _, pet_loot, prototype = self.death_fixture()
        self.remote.vnum = '3001'
        self.actor.pet = self.body
        self.body.master = self.body.leader = self.actor
        follower = self.player('follower', room=self.room)
        follower.master = follower.leader = self.actor
        owner_loot = self.item('owner loot')
        self.actor.add_item(owner_loot)

        fight.raw_kill(self.actor)

        self.assertIsNone(self.actor.pet)
        self.assertNotIn(self.body.id, self.room.mobiles)
        self.assertIsNone(self.registry.get_or_none(id=self.body.id))
        self.assertNotIn(pet_loot, self.body.owned_items())
        corpse, = self.room.contents.values()
        self.assertEqual([owner_loot], corpse.contains)
        self.assertIn(self.actor.id, self.remote.characters)
        self.assertIs(self.session.character, self.actor)
        self.assertIs(follower.master, self.actor)
        self.assertIs(follower.leader, self.actor)
        self.assertEqual(0, prototype.killed)
        fight.mobile_handler.record_mobile_kill.assert_not_called()

    def test_pet_death_allows_owner_to_buy_replacement(self):
        fight, _, loot, prototype = self.death_fixture()
        self.actor.pet = self.body
        self.body.master = self.body.leader = self.actor
        stock = mobile_entity('kitten', self.actor.status_flags)
        act_bits = self.enums.get('actBits')
        CharacterApi.set_act_flags(stock, act_bits.ACT_PET)
        self.remote.add_mobile_to_room(stock)
        room_flags = self.enums.get('roomFlags')
        self.room.room_flags = room_flags.ROOM_PET_SHOP.value
        replacement = mobile_entity('kitten', self.actor.status_flags)
        objects = Object.__new__(Object)
        objects.room_registry = self.rooms
        objects.registry_service = self.registries
        objects.interp_api = self.api
        objects.room_flags = room_flags
        objects.act_bits = act_bits
        objects.affected_bits = self.enums.get('affectedBy')
        objects.comm_flags = self.enums.get('commFlags')
        objects._haggle_transaction = Mock(return_value='')
        blocked = objects.do_buy(self.actor, self.context('buy', 'kitten'))
        self.assertEqual('has_pet', blocked['blocked_key'])

        fight.raw_kill(self.body)

        self.assertIsNone(self.actor.pet)
        self.assertIsNone(self.body.master)
        self.assertIsNone(self.body.leader)
        self.assertIsNone(self.registry.get_or_none(id=self.body.id))
        corpse, = self.room.contents.values()
        self.assertEqual([loot], corpse.contains)
        self.assertEqual(1, prototype.killed)
        with patch('area.Shop.MobileFactory.create', return_value=replacement):
            objects.do_buy(self.actor, self.context('buy', 'kitten'))
        self.assertIs(self.actor.pet, replacement)
        self.assertIs(replacement.master, self.actor)
        self.assertIs(replacement.leader, self.actor)
        self.assertIs(self.registry.get_or_none(id=replacement.id), replacement)

    def test_npc_death_releases_charmed_followers_and_group_members(self):
        fight, _, _, _ = self.death_fixture()
        follower = self.player('follower', room=self.remote)
        group_member = self.player('group member', room=self.room)
        other_leader = self.player('other leader', room=self.remote)
        follower.master = self.body
        follower.leader = other_leader
        group_member.leader = self.body
        charm = Effect(type='spell.charm_person', where='TO_AFFECTS', bitvector='AFF_CHARM', duration=5)
        fight.effect_handler.affect_to_char(follower, charm)

        fight.raw_kill(self.body)

        self.assertIsNone(follower.master)
        self.assertIsNone(follower.leader)
        self.assertIsNone(group_member.leader)
        self.assertFalse(CharacterApi.is_affected_by_name(follower, fight.AffectBits, 'AFF_CHARM'))
        self.assertEqual([], follower.effects)
        self.assertIn(follower.id, self.remote.characters)
        self.assertIn(group_member.id, self.room.characters)

    def assert_attack_breaks_charm(self, damage):
        fight, killer, _, _ = self.death_fixture()
        self.body.hit = 10
        self.body.master = self.body.leader = killer
        charm = Effect(type='spell.charm_person', where='TO_AFFECTS', bitvector='AFF_CHARM', duration=5)
        fight.effect_handler.affect_to_char(self.body, charm)

        result = fight.damage(killer, self.body, damage, show=False)

        self.assertFalse(result['killed'])
        self.assertEqual(10 - damage, self.body.hit)
        self.assertIs(self.body.fighting, killer)
        self.assertIsNone(self.body.master)
        self.assertIsNone(self.body.leader)
        self.assertFalse(CharacterApi.is_affected_by_name(self.body, fight.AffectBits, 'AFF_CHARM'))
        self.assertNotIn(charm, self.body.effects)

    def test_missed_attack_breaks_own_followers_charm(self):
        self.assert_attack_breaks_charm(0)

    def test_damaging_attack_breaks_own_followers_charm(self):
        self.assert_attack_breaks_charm(2)

    def test_rejected_attack_and_other_attackers_preserve_charm(self):
        fight, killer, _, _ = self.death_fixture()
        self.actor.level = killer.level = 20
        self.body.hit = 10
        self.body.master = self.body.leader = self.actor
        charm = Effect(type='spell.charm_person', where='TO_AFFECTS', bitvector='AFF_CHARM', duration=5)
        fight.effect_handler.affect_to_char(self.body, charm)

        self.room.room_flags = fight.RoomFlags.ROOM_SAFE.value
        denied = fight.damage(self.actor, self.body, 2, show=False)
        self.assertIn('Not in this room', denied['to_char'])
        self.assertIsNone(self.body.fighting)
        self.room.room_flags = 0
        denied = fight.damage(killer, self.body, 2, show=False)
        self.assertIn("don't own", denied['to_char'])
        self.assertIsNone(self.body.fighting)
        killer.level = CharacterApi.GameParameters.IMPLEMENTOR.value
        fight.damage(killer, self.body, 2, show=False)

        self.assertEqual(8, self.body.hit)
        self.assertIs(self.body.master, self.actor)
        self.assertIs(self.body.leader, self.actor)
        self.assertTrue(CharacterApi.is_affected_by_name(self.body, fight.AffectBits, 'AFF_CHARM'))
        self.assertIn(charm, self.body.effects)

    def test_player_death_uses_shipped_and_custom_clan_halls(self):
        fight, _, _, _ = self.death_fixture()
        self.remote.vnum = '3001'
        altar = Room(id='altar', vnum='3054', area_id='altar-area')
        hall = Room(id='hall', vnum='4000', area_id='hall-area')
        self.room_list.extend((altar, hall))
        clans = {**GameApi.clans_map(), 'custom': {'name': 'custom', 'hall': '4000'},
                 'missing': {'name': 'missing', 'hall': '9999'},
                 'unset': {'name': 'unset'}}
        with patch.object(GameApi, 'clans_map', return_value=clans):
            for index, (guild, destination) in enumerate((
                    ('', altar), ('none', altar), ('loner', altar), ('rom', altar), (' Custom ', hall),
                    ('missing', self.remote), ('unset', self.remote), ('cus', self.remote))):
                with self.subTest(guild=guild):
                    victim = self.player(f'victim-{index}', room=self.room)
                    victim.guild = guild
                    victim.gold = victim.silver = 0
                    victim.hit = -11
                    fight.raw_kill(victim)
                    self.assertNotIn(victim.id, self.room.characters)
                    self.assertIs(destination.characters[victim.id], victim)
                    self.assertEqual((destination.id, destination.area_id), (victim.room_id, victim.area_id))
                    self.assertEqual(1, victim.hit)
                    self.assertEqual(CharacterApi.pos_value('POS_RESTING'), CharacterApi.position_value(victim))

    def test_player_death_clears_hide_and_restores_innate_affects(self):
        fight, witness, *_ = self.death_fixture()
        self.remote.vnum = '3001'
        skills = load_collections(fixtures.ROOT / 'resources/collections', ['skills'])['skills']
        hide = Skill.from_json(deepcopy(next(doc for doc in skills.documents if doc['name'] == 'hide')))
        movement = Movement.__new__(Movement)
        movement.skill_registry = NS(get=lambda **_: hide)
        movement.skill_api = SkillApi(movement.skill_registry, self.enums)
        movement.skill_api.rng = Mock(number_percent=Mock(return_value=1))
        movement.effect_handler = fight.effect_handler
        affected = self.enums.get('affectedBy')

        for race, innate in (('human', 0), ('elf', affected.AFF_INFRARED.value)):
            with self.subTest(race=race):
                victim = self.player(race, room=self.room)
                victim.race = race
                victim.level = 30
                victim.character_class.name = 'warrior'
                victim.set_learned('hide', 90, collection_name='skills', create=True)
                movement.do_hide(victim, self.context('hide'))
                self.assertEqual(victim.status_flags.affected_by, affected.AFF_HIDE.value)
                self.assertFalse(fight.effect_handler.ensure_effects(victim))
                self.assertFalse(CharacterApi.can_see(witness, victim, self.room))

                victim.hit = -11
                fight.raw_kill(victim)

                self.assertIs(self.remote.characters[victim.id], victim)
                self.assertEqual(victim.status_flags.affected_by, innate)
                self.assertTrue(CharacterApi.can_see(witness, victim, self.remote))

    async def test_cyclic_controller_identity_fails_closed(self):
        self.body.context = {'controller_original': self.actor}
        self.actor.context = {'controller_original': self.body}
        self.assertEqual(CharacterApi.get_trust(self.body), 0)
