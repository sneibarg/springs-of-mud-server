import json
import unittest
from dataclasses import fields
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock, patch

from tests.test_update_handler_active_players import Character, build_character_data
from api.AliasApi import AliasApi
from api.CharacterApi import CharacterApi
from area.Room import Room
from interp.InterpHandler import InterpHandler
from interp.PromptFormat import PromptFormat, build_prompt_map
from interp.Social import Social
from interp.SocialHandler import SocialHandler
from player.CharacterService import CharacterService
from server.session.SessionState import SessionStatus


class AliasPromptRegressions(unittest.TestCase):
    def test_alias_keys_survive_json_save_reload_without_collision(self):
        actor = Character.from_json(build_character_data())
        aliases = {'go_home': 'recall', 'gohome': 'north', 'two__words': 'south'}
        for name, replacement in aliases.items():
            AliasApi.set_alias(actor, name, replacement)
        saved = json.loads(json.dumps(CharacterService._serialize_character(actor)))
        self.assertEqual(aliases, saved['aliases'])
        restored = Character.from_json(saved)
        for name, replacement in aliases.items():
            self.assertEqual(replacement + ' now', AliasApi.substitute_command(restored, name + ' now').command)

    def test_all_prompt_options_survive_save_and_render_on_real_character(self):
        actor = Character.from_json(build_character_data())
        actor.set_alignment(-900)
        room = Room(name='Hall', vnum='42')
        area = NS(name='Town')
        for option in fields(PromptFormat):
            with self.subTest(option=option.name):
                actor.prompt_format = PromptFormat(**{option.name: True})
                restored = Character.from_json(json.loads(json.dumps(CharacterService._serialize_character(actor))))
                self.assertTrue(getattr(restored.prompt_format, option.name))
                with patch.object(CharacterApi, 'is_immortal', return_value=True):
                    message = restored.prompt_format.render_prompt(SessionStatus.PLAYING, restored, room, area)
                    expected = {'%h': 25, '%H': 30, '%m': 15, '%M': 20, '%v': 18, '%V': 20,
                                '%x': 100, '%X': 100, '%g': 10, '%s': 5, '%a': -900,
                                '%r': 'Hall', '%e': 'none', '%R': '42', '%z': 'Town', '%c': '\n'}
                    for token, renderer in build_prompt_map().items():
                        self.assertEqual(expected[token], PromptFormat._call_prompt_lambda(renderer, restored, room, area))
                self.assertIn('text', message.data)
                if option.name == 'alignment':
                    self.assertIn('-900', message.data['text'])


class SocialInterpreterRegressions(unittest.IsolatedAsyncioTestCase):
    def setup_interpreter(self):
        from enum import IntEnum
        self.enterContext(patch.object(CharacterApi, 'get_enum', return_value=IntEnum('Affects', {'AFF_HIDE': 1})))
        self.actor = Character.from_json(build_character_data('actor-id'))
        self.target = Character.from_json(build_character_data('target-id'))
        self.target.name = 'Tester'
        self.actor.name = 'Actor'
        self.viewer = Character.from_json(build_character_data('viewer-id'))
        self.viewer.name = 'Viewer'
        self.npc = NS(id='npc-id', name='city guard')
        self.room = Room(id=self.actor.room_id,
                         characters={p.id: p for p in (self.actor, self.target, self.viewer)},
                         mobiles={self.npc.id: self.npc})
        social = Social('smile-id', 'smile', 'You smile.', '$n smiles.',
                        'You smile at $N.', '$n smiles at $N.', '$n smiles at you.',
                        'Nobody here.', 'You smile at yourself.', '$n smiles at themself.')
        bus = Mock(send_to_character=AsyncMock(), send_to_room=AsyncMock(), text_to_message=lambda text: text)
        registry = Mock(get_or_none=Mock(side_effect=lambda **kw: social if kw['name'] == 'smile' else None))
        rooms = Mock(get=Mock(return_value=self.room))
        handler = SocialHandler(bus, registry, Mock(), rooms)
        interp = InterpHandler.__new__(InterpHandler)
        interp.social_registry = registry
        interp.social_handler = handler
        interp.interp_registry = Mock(get_or_none=Mock(return_value=None), all_commands=Mock(return_value=[]))
        interp.registry_service = NS(interp_registry=interp.interp_registry)
        interp.message_bus = bus
        interp.command_not_found_message = 'Huh?'
        return interp, bus

    async def test_social_fallback_resolves_room_names_and_excludes_direct_recipients(self):
        for argument, expected, victim in (
                ('', 'You smile.', None), ('Tester', 'You smile at Tester.', 'player'),
                ('guard', 'You smile at city guard.', 'npc'), ('self', 'You smile at yourself.', 'self'),
                ('Actor', 'You smile at yourself.', 'self'),
                ('missing', 'Nobody here.', 'missing'), ('\tTester', 'You smile at Tester.', 'player')):
            with self.subTest(argument=argument):
                interp, bus = self.setup_interpreter()
                with patch.object(CharacterApi, 'can_see', return_value=True):
                    await interp.handle_command(None, self.actor, 'SMILE ' + argument)
                interp.social_registry.get_or_none.assert_called_once_with(name='smile')
                self.assertEqual((self.actor.id, expected + '\r\n'), bus.send_to_character.call_args_list[0].args)
                if victim == 'missing':
                    bus.send_to_room.assert_not_called()
                else:
                    recipients = bus.send_to_room.call_args.args[1]
                    self.assertNotIn(self.actor.id, [p.id for p in recipients])
                    if victim == 'player':
                        self.assertNotIn(self.target.id, [p.id for p in recipients])
                        self.assertEqual(self.target.id, bus.send_to_character.call_args_list[1].args[0])

    async def test_invisible_target_is_not_resolved(self):
        interp, bus = self.setup_interpreter()
        self.target.status_flags.invis_level = 1000
        await interp.handle_command(None, self.actor, 'smile Tester')
        bus.send_to_character.assert_awaited_once_with(self.actor.id, 'Nobody here.\r\n')
        bus.send_to_room.assert_not_called()


if __name__ == '__main__':
    unittest.main()
