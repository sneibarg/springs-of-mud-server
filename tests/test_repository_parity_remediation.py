"""Regressions derived from the October 31 ROM24 review's five findings."""
import unittest
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock, patch

from tests import test_speech_text_parity as speech
from tests.test_movement_rules_parity import MovementFixture, item
from api.CharacterApi import CharacterApi
from api.AliasApi import AliasApi
from api.SpellApi import SpellApi
from area.Area import Area
from area.AreaRegistry import AreaRegistry
from area.RoomHandler import RoomHandler
from combat.CombatEscapeHandler import CombatEscapeHandler
from combat.CombatHandler import FightHandler
from combat.CombatRegistry import CombatRegistry
from game.EntityUpdateHandler import EntityUpdateHandler
from interp.commands.Fight import Fight
from interp.commands.Info import Info
from interp.commands.Wiz import Wiz
from player.Character import Character
from player.CharacterService import CharacterService
from server.handlers.ConnectionHandler import ConnectionHandler
from server.protocol.MessageCodec import MessageCodec
from server.session.SessionHandler import SessionHandler
from server.session.SessionState import SessionStatus
from util.InterpUtil import InterpUtil
from mobile.MobileFactory import MobileFactory
from mobile.Dice import Dice
from player.CharacterAttributes import CharacterAttributes
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

    def setup_information_commands(self):
        f = self.fixture
        f.registries.help_registry = f.registries.area_registry = None
        sessions = SessionHandler()
        for character in (f.actor, f.bob, f.cara):
            session = sessions.create_session(character.id)
            session.character, session.status = character, SessionStatus.PLAYING
        player = f.interpreter.handler_service.get_handler('ph')
        player.info_commands = Info(f.registries, sessions, f.weather, f.enums, f.api)
        player.interp_api = f.api
        return sessions

    async def test_titles_use_rom_spacing_in_roster_score_and_standing_room_lines(self):
        f = self.fixture
        self.setup_information_commands()
        f.actor.set_position(f.enums.get('positions').POS_STANDING)
        brief = f.enums.get('commFlags').COMM_BRIEF
        f.bob.status_flags.unset_flag('comm', brief)
        await f.interpreter.handle_command(f.actor, 'title the explorer')
        self.assertEqual(' the explorer', f.actor.title)
        await f.interpreter.handle_command(f.bob, 'who')
        self.assertIn('Alice the explorer\r\n', f.messages(f.bob)[-1])
        self.assertIn('Alice the explorer is here.', f.room.get_players_in_room(f.bob))
        f.bob.status_flags.set_flag('comm', brief)
        self.assertNotIn('the explorer', f.room.get_players_in_room(f.bob))
        f.bob.status_flags.unset_flag('comm', brief)
        f.bob.on = item('bench')
        self.assertNotIn('the explorer', f.room.get_players_in_room(f.bob))
        f.bob.on = None
        f.actor.set_position(f.enums.get('positions').POS_RESTING)
        self.assertNotIn('the explorer', f.room.get_players_in_room(f.bob))

        await f.interpreter.handle_command(f.actor, 'title , the explorer')
        await f.interpreter.handle_command(f.bob, 'whois Alice')
        self.assertIn('Alice, the explorer\r\n', f.messages(f.bob)[-1])
        await f.interpreter.handle_command(f.actor, 'score')
        self.assertIn('You are Alice, the explorer, level', f.messages(f.actor)[-1])
        f.actor.title = 'the explorer'  # Bare titles stored by older records and advancement.
        await f.interpreter.handle_command(f.bob, 'whois Alice')
        self.assertIn('Alice the explorer\r\n', f.messages(f.bob)[-1])

    async def test_title_truncates_before_tilde_rewrite_and_supports_staff_override(self):
        f = self.fixture
        self.setup_information_commands()
        await f.interpreter.handle_command(f.actor, 'title ' + 'x' * 44 + '~Z')
        self.assertEqual(' ' + 'x' * 44 + '-', f.actor.title)

        f.actor.level, f.actor.role = f.enums.get('gameParameters').MAX_LEVEL.value, 'admin'
        player = f.interpreter.handler_service.get_handler('ph')
        player.wiz_commands = Wiz.__new__(Wiz)
        player.wiz_commands.room_registry = f.rooms
        player.wiz_commands.character_registry = player.character_registry
        await f.interpreter.handle_command(f.actor, 'string cha Bob ti ' + 'z' * 60 + '~')
        self.assertEqual(' ' + 'z' * 60 + '-', f.bob.title)

    async def test_count_uses_visible_bodies_and_roster_uses_switched_player(self):
        f = self.fixture
        sessions = self.setup_information_commands()
        body = f.npc()
        body.room_id = f.actor.room_id
        session = sessions.get_session(f.bob.id)
        session.character = body
        session.metadata['switched_original'] = f.bob
        body.context = {'controller_original': f.bob}
        f.bob.title = ', the explorer'
        sessions.get_session(f.cara.id).status = SessionStatus.IDLING

        await f.interpreter.handle_command(f.actor, 'whois Bob')
        self.assertIn('Bob, the explorer\r\n', f.messages(f.actor)[-1])
        f.bob.status_flags.invis_level = 100
        await f.interpreter.handle_command(f.actor, 'who')
        self.assertNotIn('Bob, the explorer', f.messages(f.actor)[-1])
        await f.interpreter.handle_command(f.actor, 'count')
        self.assertEqual('There are 3 characters on, the most so far today.\r\n', f.messages(f.actor)[-1])

        f.bob.status_flags.invis_level = 0
        body.status_flags.invis_level = 100
        await f.interpreter.handle_command(f.cara, 'who')
        self.assertNotIn('Bob, the explorer', f.messages(f.cara)[-1])
        await f.interpreter.handle_command(f.cara, 'count')
        self.assertEqual('There are 2 characters on, the most on today was 3.\r\n', f.messages(f.cara)[-1])

        f.flag(f.cara, 'AFF_BLIND')
        await f.interpreter.handle_command(f.cara, 'count')
        self.assertEqual('There are 1 characters on, the most on today was 3.\r\n', f.messages(f.cara)[-1])

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

    async def test_alias_management_and_expansion_use_rom_rules_while_switched(self):
        f = self.fixture
        body = f.npc()
        body.context = {'controller_original': f.actor}
        body.room_id = f.actor.room_id
        f.connections[body.id] = f.connections[f.actor.id]

        await f.interpreter.handle_command(body, 'alias w~ say hi~')
        self.assertEqual({'w-': 'say hi-'}, f.actor.aliases)
        await f.interpreter.handle_command(body, 'alias w~')
        self.assertIn("w- aliases to 'say hi-'.", f.messages(body)[-1])
        await f.interpreter.handle_command(body, 'alias x del')
        self.assertNotIn('x', f.actor.aliases)
        await f.interpreter.handle_command(body, 'alias x delete now')
        self.assertEqual('delete now', f.actor.aliases['x'])
        raw = MessageCodec.decode_text(b'  w- again\r\n').get('text')
        self.assertEqual('  w- again', AliasApi.substitute_command(body, raw).command)
        self.assertEqual('"w-" again', AliasApi.substitute_command(body, '"w-" again').command)
        self.assertEqual('say hi- again', AliasApi.substitute_command(body, 'w- again').command)
        await f.interpreter.handle_command(body, 'alias aliasfoo say hi')
        self.assertEqual('aliasfoo', AliasApi.substitute_command(body, 'aliasfoo').command)
        overflow = AliasApi.substitute_command(body, 'w- ' + 'x' * 255)
        self.assertEqual(255, len(overflow.command))
        self.assertFalse(overflow.message)
        await f.interpreter.handle_command(body, 'una w-')
        self.assertNotIn('w-', f.actor.aliases)

    async def test_scroll_command_preserves_preference_and_matches_rom_argument_rules(self):
        f = self.fixture
        self.setup_information_commands()
        for command, expected in (
            ('scroll', 'You currently display 24 lines per page.'),
            ('scr +20 trailing', 'Scroll set to 20 lines.'),
            ('scroll --10', 'You must provide a number.'),
            ('scroll', 'You currently display 20 lines per page.'),
            ('scroll "10"', 'Scroll set to 10 lines.'),
            ('scroll 0', 'Paging disabled.'),
            ('scroll', 'You do not page long messages.'),
        ):
            with self.subTest(command=command):
                await f.interpreter.handle_command(f.actor, command)
                self.assertEqual(expected + '\r\n', f.messages(f.actor)[-1])
        restored = Character.from_json(CharacterService._serialize_character(f.actor))
        self.assertEqual(0, CharacterApi.scroll_line_limit(restored))

    async def test_pager_continues_and_mirrors_then_dismisses_on_a_command(self):
        f = self.fixture
        sessions = self.setup_information_commands()
        f.bus.session_handler = sessions
        session = sessions.get_session(f.actor.id)
        session.metadata['snoop_by_session_id'] = f.bob.id
        f.bus.connection_manager.get_connection = f.connections.get
        f.actor.scroll_lines = 2
        text = 'one\r\ntwo\r\nthree\r\nfour\r\nfive\r\nsix\r\n   \r\n'
        await f.bus.send_to_character(f.actor.id, f.bus.text_to_message(text))
        self.assertEqual(text, f.messages(f.actor)[-1])
        self.assertFalse(session.metadata.get('paging_active', False))
        await f.bus.send_to_character(f.actor.id, f.bus.text_to_message(text), paginate=True)
        self.assertEqual(['three\r\nfour\r\n', 'five\r\nsix\r\n'], session.metadata['paging_queue'])

        handler = ConnectionHandler.__new__(ConnectionHandler)
        handler.session_handler, handler.message_bus = sessions, f.bus
        handler.command_handler = NS(handle_command=AsyncMock())
        handler.logger = Mock()
        handler._get_area_and_room = lambda _: (None, f.room)
        handler._wait_for_message = AsyncMock(side_effect=[
            MessageCodec.decode_text(b'\r\n'), MessageCodec.decode_text(b'look\r\n'),
            MessageCodec.decode_text(b'count\r\n'), None,
        ])
        await handler._game_loop(f.connections[f.actor.id], session, None, f.actor)
        handler.command_handler.handle_command.assert_awaited_once_with(f.actor, 'count')
        self.assertFalse(session.metadata['paging_active'])
        self.assertIn('three\r\nfour', f.messages(f.bob)[-1])
        self.assertNotIn('five', f.messages(f.actor)[-1])

    async def test_auto_commands_use_rom_shortcuts_and_ignore_switched_mobiles(self):
        f = self.fixture
        self.setup_information_commands()
        await f.interpreter.handle_command(f.actor, 'auto')
        self.assertIn('autoassist', f.messages(f.actor)[-1])
        previous = CharacterApi.has_player_flag(f.actor, 'PLR_AUTOEXIT')
        await f.interpreter.handle_command(f.actor, 'autoex')
        self.assertEqual(not previous, CharacterApi.has_player_flag(f.actor, 'PLR_AUTOEXIT'))

        body = f.npc()
        body.context = {'controller_original': f.actor}
        body.room_id = f.actor.room_id
        f.connections[body.id] = f.connections[f.actor.id]
        f.connections[body.id].send_message.reset_mock()
        act_flags = body.status_flags.act, f.actor.status_flags.act
        for command in ('autolist', 'autoassist', 'autoexit', 'autogold', 'autoloot', 'autosac', 'autosplit'):
            await f.interpreter.handle_command(body, command)
        self.assertEqual([], f.messages(body))
        self.assertEqual(act_flags, (body.status_flags.act, f.actor.status_flags.act))

        player = f.interpreter.handler_service.get_handler('ph')
        room_handler = NS(print_room=AsyncMock(return_value=True), print_exits=AsyncMock(),
                          print_in_room=RoomHandler.print_in_room)
        mobile_handler = NS(print_mobiles_in_room=AsyncMock())
        f.rooms.get = f.rooms.get_or_none
        handlers = {'ph': player, 'rh': room_handler, 'mh': mobile_handler}
        f.interpreter.handler_service = NS(get_handler=handlers.get)
        body.status_flags.set_flag('act', f.enums.get('playerActBits').PLR_AUTOEXIT)
        f.actor.status_flags.set_flag('act', f.enums.get('playerActBits').PLR_AUTOEXIT)
        await f.interpreter.handle_command(body, 'look')
        await player._show_room_to_character(
            body, f.room, NS(room_handler=lambda: room_handler, mobile_handler=lambda: mobile_handler)
        )
        self.assertEqual(2, room_handler.print_room.await_count)
        room_handler.print_exits.assert_not_awaited()

    async def test_stored_description_keeps_spacing(self):
        f = self.fixture
        handler = f.interpreter.handler_service.get_handler('ph')
        handler.info_commands = Info.__new__(Info)
        await f.interpreter.handle_command(f.actor, 'description Two   spaces remain.')
        self.assertEqual('Two   spaces remain.\r\n', f.actor.description)

    async def test_areas_preserves_load_order_and_full_credits_without_paging(self):
        f = self.fixture
        area_registry = AreaRegistry()
        area_documents = (
            ('Zeta', 'Diku', 'All'),
            ('Amber Gate and the Forgotten Court of the First Kings', 'Builder', '5-50'),
            ('Crystal Woods', '', '10 20'),
        )
        for vnum, (name, author, levels) in enumerate(area_documents):
            area_registry.register(Area.from_json({
                'id': str(vnum), 'vnum': str(vnum), 'name': name,
                'author': author, 'suggestedLevelRange': levels,
            }))
        first, second, _ = area_registry.areas_in_load_order()
        self.assertEqual((1, 50), first.vnum_range)
        self.assertEqual((5, 50), second.vnum_range)

        info = Info.__new__(Info)
        info.interp_api, info.area_registry = f.api, area_registry
        f.interpreter.handler_service.get_handler('ph').info_commands = info
        f.actor.context = {'scroll_lines': 1}
        session = NS(character=f.actor, metadata={})
        f.bus.session_handler.get_session_by_character = lambda _: session

        await f.interpreter.handle_command(f.actor, 'areas')
        expected_left = '{ All } Diku    Zeta'
        expected_right = '{10 20} Crystal Woods'
        long_credit = '{ 5-50} Builder Amber Gate and the Forgotten Court of the First Kings'
        expected = f'{expected_left:<39}{expected_right:<39}\r\n{long_credit}{" " * 39}\r\n'
        self.assertEqual([expected], f.messages(f.actor))
        self.assertFalse(session.metadata.get('paging_active', False))

    async def test_wimpy_parses_rom_arguments_and_sets_automatic_flee_threshold(self):
        f = self.fixture
        info = Info.__new__(Info)
        info.interp_api = f.api
        f.interpreter.handler_service.get_handler('ph').info_commands = info
        f.actor.max_hit, f.actor.hit = 103, 18
        escape = CombatEscapeHandler.__new__(CombatEscapeHandler)
        escape.game_parameters = f.enums.get('gameParameters')
        escape._connected = Mock(return_value=True)
        escape._perform = Mock(return_value=['flee'])

        for argument, threshold in (
            ('', 20), ('+20', 20), ('20 trailing', 20), ('"20"', 20), ('20hp', 20),
            ('0', 0), ('abc', 0), ('--20', 0), ('51', 51),
        ):
            with self.subTest(argument=argument):
                f.actor.character_attributes.wimpy = 10
                await f.interpreter.handle_command(f.actor, f'wimpy {argument}')
                self.assertEqual(threshold, f.actor.character_attributes.wimpy)
                self.assertEqual(f'Wimpy set to {threshold} hit points.\r\n', f.messages(f.actor)[-1])
                self.assertEqual(threshold >= 18, bool(escape.after_damage(f.bob, f.actor, 1)))

        for argument, message in (
            ('-1', 'Your courage exceeds your wisdom.\r\n'),
            ('52', 'Such cowardice ill becomes you.\r\n'),
        ):
            with self.subTest(argument=argument):
                await f.interpreter.handle_command(f.actor, f'wimpy {argument}')
                self.assertEqual(51, f.actor.character_attributes.wimpy)
                self.assertEqual(message, f.messages(f.actor)[-1])

    async def test_wimpy_sets_the_switched_body_threshold(self):
        from tests.test_immortal_priority_parity import mobile_entity

        f = self.fixture
        info = Info.__new__(Info)
        info.interp_api = f.api
        f.interpreter.handler_service.get_handler('ph').info_commands = info
        f.actor.character_attributes.wimpy = 20
        body = mobile_entity('body', f.actor.status_flags)
        body.character_attributes = CharacterAttributes.default()
        body.set_position(f.enums.get('positions').POS_STANDING)
        body.max_hit = 103
        body.room_id = f.actor.room_id
        body.context = {'controller_original': f.actor}
        f.connections[body.id] = f.connections[f.actor.id]

        await f.interpreter.handle_command(body, 'wimpy 12')
        self.assertEqual(12, body.character_attributes.wimpy)
        self.assertEqual(20, f.actor.character_attributes.wimpy)
        self.assertEqual(['Wimpy set to 12 hit points.\r\n'], f.messages(body))

    async def test_wimpy_damage_moves_player_and_delivers_arrival_and_flee_messages(self):
        f = self.fixture
        player = f.interpreter.handler_service.get_handler('ph')
        player.interp_api = f.api
        player.info_commands = Info.__new__(Info)
        player.info_commands.interp_api = f.api
        player.info_commands.PlayerActBits = f.enums.get('playerActBits')
        f.rooms.get = f.rooms.get_or_none
        room_handler = RoomHandler(f.bus, f.bus.session_handler, f.registries)
        mobile_handler = NS(print_mobiles_in_room=AsyncMock())
        handlers = {'ph': player, 'rh': room_handler, 'mh': mobile_handler}
        handler_service = NS(player_handler=player, get_handler=handlers.get)
        f.interpreter.handler_service = handler_service
        f.bus.session_handler.get_session_by_character = lambda _: NS(character=f.actor, metadata={})

        combat = FightHandler.__new__(FightHandler)
        combat.message_bus = f.bus
        combat.room_registry = f.rooms
        combat.combat_registry = CombatRegistry()
        combat.PositionsEnum = f.enums.get('positions')
        combat.AffectBits = f.enums.get('affectedBy')
        combat.PlayerActBits = f.enums.get('playerActBits')
        combat.logger = Mock()
        combat.death_handler = None
        combat.aggressive_entry_rounds = Mock(return_value=[])
        player.fight_handler = f.movement.fight_handler = combat
        flee = Fight.__new__(Fight)
        flee.registry_service, flee.room_registry, flee.interp_api = f.registries, f.rooms, f.api
        flee.fight_handler, flee.movement_commands = combat, f.movement
        combat.set_escape_handler(CombatEscapeHandler(
            flee, f.movement, f.registries, handler_service, f.bus.session_handler,
            f.bus.connection_manager, f.enums,
        ))

        f.destination.name = 'North of the guard'
        f.actor.max_hit, f.actor.hit = 100, 36
        await f.interpreter.handle_command(f.actor, 'wimpy 20')
        combat.set_fighting(f.actor, f.bob, f.room.id)
        combat.set_fighting(f.bob, f.actor, f.room.id)
        with patch('interp.commands.Fight.random.randint', return_value=0):
            result = combat.damage(f.bob, f.actor, 16, show=False)
        payload = combat.build_round_payload(f.bob, f.actor, f.room, result)
        await combat.emit_round_payload(f.bob, payload)

        self.assertEqual(20, f.actor.hit)
        self.assertEqual(f.destination.id, f.actor.room_id)
        self.assertIsNone(f.actor.fighting)
        self.assertIsNone(f.bob.fighting)
        output = ''.join(f.messages(f.actor))
        self.assertIn(f.destination.name, output)
        self.assertIn(f.command('flee').render_message('to_char', 'flee'), output)


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
