import asyncio
import unittest
from enum import IntEnum
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from tests import test_command_authorization as authorization_fixtures
from api.CharacterApi import CharacterApi
from interp.CommandAccess import CommandDenial
from interp.CommandExecutor import CommandExecutor
from interp.Context import Context
from interp.InterpHandler import InterpHandler
from player.PlayerHandler import PlayerHandler


class CommandExecutorTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.actor = SimpleNamespace(id='victim', name='Victim', level=10, role='player', position=8,
                                     room_id='victim-room', context={})
        self.command = SimpleNamespace(name='probe', lambdas=[], pipeline=True, max_arguments=3,
                                       enabled=True, level=0, role='player', position='POS_STANDING')
        parameters = IntEnum('Parameters', {'MAX_LEVEL': 60, 'LEVEL_IMMORTAL': 55})
        positions = IntEnum('Positions', {'POS_STANDING': 8})
        self.enterContext(patch.object(CharacterApi, 'get_enum', side_effect=lambda name: {
            'gameParameters': parameters, 'positions': positions}[name]))
        self.enterContext(patch.object(CharacterApi, 'get_trust', side_effect=lambda actor: actor.level))
        self.enterContext(patch.object(CharacterApi, 'position_value', side_effect=lambda actor: actor.position))
        self.connection = object()
        self.room = object()
        self.bus = SimpleNamespace(text_to_message=lambda text: text, send_to_character=AsyncMock(),
                                   connection_manager=SimpleNamespace(get_connection_by_character=Mock(return_value=self.connection)))
        self.services = SimpleNamespace()
        self.normal = InterpHandler.__new__(InterpHandler)
        self.normal.message_bus = self.bus
        self.normal.connection_manager = self.bus.connection_manager
        self.normal.room_registry = SimpleNamespace(get_or_none=Mock(return_value=self.room))
        self.normal.handler_service = self.services
        self.nested = PlayerHandler.__new__(PlayerHandler)
        self.nested.message_bus = self.bus
        self.nested.room_registry = self.normal.room_registry
        self.nested.interp_registry = SimpleNamespace(get_or_none=lambda **kw: self.command)
        self.nested.interp_api = SimpleNamespace(render_message_key=lambda *args, **kw: {})

    async def run_path(self, path):
        if path == 'normal':
            return await self.normal._handle_lambdas(self.actor, self.command, 'hello world')
        context = Context(character=self.actor, command=self.command, handler_service=self.services,
                          result='hello world', parameters=['hello', 'world'], room=self.room, conn=self.connection)
        return await self.nested._execute_nested_lambdas(self.command, context)

    async def test_direct_and_nested_paths_share_command_auditing(self):
        for path, handler in (('normal', self.normal), ('nested', self.nested)):
            with self.subTest(path=path):
                handler.command_audit = SimpleNamespace(record=AsyncMock())
                self.command.log = 'LOG_NEVER'
                self.command.lambdas = ['lambda ctx: "ok"']
                self.assertEqual(await self.run_path(path), 'ok')
                handler.command_audit.record.assert_awaited_once_with(self.actor, self.command, f'{self.command.name} hello world')

    async def test_sync_and_async_results_execute_in_order_in_both_paths(self):
        for path in ('normal', 'nested'):
            with self.subTest(path=path):
                events = []
                def first(ctx):
                    events.append(ctx.result)
                    return 'sync'
                async def second(ctx):
                    await asyncio.sleep(0)
                    events.append(ctx.result)
                    return 'async'
                self.services.first, self.services.second = first, second
                self.command.pipeline = False
                self.command.lambdas = ['lambda ctx: ctx.handler_service.first(ctx)',
                                        'lambda ctx: ctx.handler_service.second(ctx)', 'lambda ctx: ctx.result + " result"']
                self.assertEqual(await self.run_path(path), 'async result')
                self.assertEqual(events, ['hello world', 'sync'])

    async def test_pipeline_forward_backward_jumps_and_completion_in_both_paths(self):
        for path in ('normal', 'nested'):
            with self.subTest(path=path):
                events = []
                def step(ctx):
                    events.append('step')
                    self.assertIsNone(ctx.next_index)
                    ctx.jump_to(0 if len(events) == 1 else 3)
                    return len(events)
                self.services.step = step
                self.command.lambdas = ['lambda ctx: ctx.jump_to(2)',
                                        'lambda ctx: 1 / 0',
                                        'lambda ctx: ctx.handler_service.step(ctx)',
                                        'lambda ctx: (ctx.jump_to(0), ctx.finish(), "done")[-1]',
                                        'lambda ctx: 1 / 0']
                self.assertEqual(await self.run_path(path), 'done')
                self.assertEqual(events, ['step', 'step'])

    async def test_legacy_sequence_continues_after_pipeline_control_flags(self):
        for path in ('normal', 'nested'):
            with self.subTest(path=path):
                self.command.pipeline = False
                self.command.lambdas = ['lambda ctx: (ctx.finish(), ctx.jump_to(100))', 'lambda ctx: "last"']
                self.assertEqual(await self.run_path(path), 'last')

    async def test_blank_nonstring_and_noncallable_entries_are_skipped(self):
        for pipeline in (False, True):
            for path in ('normal', 'nested'):
                with self.subTest(pipeline=pipeline, path=path):
                    self.command.pipeline = pipeline
                    self.command.lambdas = [None, '', '  ', 42, '42', 'lambda ctx: "executed"']
                    self.assertEqual(await self.run_path(path), 'executed')

    async def test_awaited_exceptions_propagate_and_stop_following_lambdas(self):
        for path in ('normal', 'nested'):
            with self.subTest(path=path):
                self.services.fail = AsyncMock(side_effect=ValueError('failed command'))
                self.services.after = Mock()
                self.command.lambdas = ['lambda ctx: ctx.handler_service.fail()', 'lambda ctx: ctx.handler_service.after()']
                with patch('interp.CommandExecutor.LoggerFactory.get_logger', return_value=Mock()):
                    with self.assertRaisesRegex(ValueError, 'failed command'):
                        await self.run_path(path)
                self.services.fail.assert_awaited_once()
                self.services.after.assert_not_called()

    async def test_cancellation_propagates_without_running_later_steps(self):
        for path in ('normal', 'nested'):
            self.services.fail = AsyncMock(side_effect=asyncio.CancelledError())
            self.services.after = Mock()
            self.command.lambdas = ['lambda ctx: ctx.handler_service.fail()', 'lambda ctx: ctx.handler_service.after()']
            with self.assertRaises(asyncio.CancelledError):
                await self.run_path(path)
            self.services.after.assert_not_called()

    async def test_future_results_are_awaited_in_both_paths(self):
        for path in ('normal', 'nested'):
            future = asyncio.get_running_loop().create_future()
            asyncio.get_running_loop().call_soon(future.set_result, 'future result')
            self.services.future = lambda: future
            self.command.lambdas = ['lambda ctx: ctx.handler_service.future()']
            self.assertEqual(await self.run_path(path), 'future result')

    async def test_out_of_range_jump_ends_pipeline(self):
        for path in ('normal', 'nested'):
            self.command.lambdas = ['lambda ctx: (ctx.jump_to(100), "jumped")[-1]', 'lambda ctx: 1 / 0']
            self.assertEqual(await self.run_path(path), 'jumped')

    async def test_awaited_completion_stops_pipeline_in_both_paths(self):
        async def finish(ctx):
            await asyncio.sleep(0)
            ctx.finish()
            return 'finished'
        self.services.finish = finish
        self.command.lambdas = ['lambda ctx: ctx.handler_service.finish(ctx)', 'lambda ctx: 1 / 0']
        for path in ('normal', 'nested'):
            self.assertEqual(await self.run_path(path), 'finished')

    async def test_remote_command_restores_location_after_awaited_failure(self):
        from area.Room import Room

        original = Room(id='original', area_id='home')
        remote = Room(id=self.actor.room_id, area_id='remote')
        remote.add_player_to_room(self.actor)
        self.nested.room_registry = SimpleNamespace(get_or_none=lambda **kw: remote,
                                                    all_rooms=lambda: [original, remote])
        self.services.fail = AsyncMock(side_effect=ValueError('remote failure'))
        self.command.lambdas = ['lambda ctx: ctx.handler_service.fail()']
        context = Context(character=self.actor, handler_service=self.services)
        seat = object()
        original.contents['seat'] = seat
        with patch('interp.CommandExecutor.LoggerFactory.get_logger', return_value=Mock()), \
                patch.object(CharacterApi, 'is_npc', return_value=False):
            with self.assertRaisesRegex(ValueError, 'remote failure'):
                await self.nested._handle_at_payload(self.actor, context, {
                    'interpret_at': 'probe', 'at_original_room': original, 'at_on': seat})
        self.assertIs(original.characters[self.actor.id], self.actor)
        self.assertNotIn(self.actor.id, remote.characters)
        self.assertEqual((self.actor.room_id, self.actor.area_id), ('original', 'home'))
        self.assertIs(self.actor.on, seat)

    async def test_authorization_is_explicit_and_precedes_evaluation(self):
        self.command.lambdas = ['invalid syntax']
        context = Context(character=self.actor)
        policy = Mock(return_value=CommandDenial('command_not_allowed'))
        await CommandExecutor.execute(self.command, context, authorization=policy, message_bus=self.bus)
        policy.assert_called_once_with(self.actor, self.command)
        self.assertTrue(context.done)
        self.bus.send_to_character.assert_awaited_once_with('victim', 'Huh?\r\n')
        with self.assertRaises(TypeError):
            await CommandExecutor.execute(self.command, context, message_bus=self.bus)

    async def test_empty_commands_report_unavailable_in_both_paths(self):
        for path in ('normal', 'nested'):
            self.assertIsNone(await self.run_path(path))
        self.assertEqual(self.bus.send_to_character.await_count, 2)

    async def test_force_preserves_victim_identity_connection_room_and_arguments(self):
        observed = []
        async def capture(ctx):
            observed.append((ctx, ctx.argument, ctx.result))
        self.services.capture = capture
        self.command.lambdas = ['lambda ctx: ctx.handler_service.capture(ctx)']
        admin = SimpleNamespace(id='admin', name='Admin', level=60)
        outer = Context(character=admin, command=object(), handler_service=self.services, conn=object())
        await self.nested._handle_force_payload(admin, outer, {
            'forced_commands': [{'victim': self.actor, 'command': 'probe Hello World'}]})
        self.assertEqual(len(observed), 1)
        context, argument, raw_result = observed[0]
        self.assertIs(context.character, self.actor)
        self.assertIs(context.conn, self.connection)
        self.assertIs(context.room, self.room)
        self.assertIs(context.command, self.command)
        self.assertEqual(context.parameters, ['hello', 'world'])
        self.assertEqual((argument, raw_result), ('Hello World', 'Hello World'))
        self.assertIs(outer.character, admin)

    async def test_force_cannot_borrow_admin_authority(self):
        self.command.level = 55
        self.services.capture = Mock()
        self.command.lambdas = ['lambda ctx: ctx.handler_service.capture(ctx)']
        admin = SimpleNamespace(id='admin', name='Admin', level=60)
        await self.nested._handle_force_payload(admin, Context(character=admin, handler_service=self.services), {
            'forced_commands': [{'victim': self.actor, 'command': 'probe'}]})
        self.services.capture.assert_not_called()
        self.bus.send_to_character.assert_awaited_once_with(self.actor.id, 'Huh?\r\n')


if __name__ == '__main__':
    unittest.main()
