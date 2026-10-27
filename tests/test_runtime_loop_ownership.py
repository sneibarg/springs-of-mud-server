import asyncio
import sys
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from game.GameService import GameService
from server.MudServer import MudServer
from server.session.SessionHandler import SessionHandler
from server.session.SessionState import SessionStatus


def scheduler(update):
    service = GameService.__new__(GameService)
    service.logger = Mock()
    service.update_handler = NS(handle_updates=update)
    service.enums = {'gameParameters': {'PULSE_PER_SECOND': 1000}}
    service._runtime_loop = None
    service._stop_requested = threading.Event()
    service._pending_update = None
    service._updates_suspended = False
    service._active_update_task = None
    return service


class RuntimeLoopOwnershipTests(unittest.IsolatedAsyncioTestCase):
    async def test_saved_shutdown_returns_from_server_start_and_stops_scheduler(self):
        from server.RuntimeControl import RuntimeControl
        updated = asyncio.Event()
        async def update():
            updated.set()
        service = scheduler(update)
        control = RuntimeControl(service, Mock(), NS(get_active_sessions=lambda: []), NS(close_all=AsyncMock()))
        server = MudServer.__new__(MudServer)
        server.logger = Mock()
        server.injector = Mock(get=lambda cls: service if cls is GameService else control)
        server.host, server.port = 'localhost', 0
        class Listener:
            def __init__(self):
                self.closed = False
            async def __aenter__(self):
                return self
            async def __aexit__(self, *args):
                self.closed = True
            def close(self):
                self.closed = True
            async def wait_closed(self):
                pass
        listener = Listener()
        with patch('server.MudServer.asyncio.start_server', new=AsyncMock(return_value=listener)):
            task = asyncio.create_task(server.start())
            await asyncio.wait_for(updated.wait(), 1)
            self.assertTrue(await control.shutdown('shutdown'))
            await asyncio.wait_for(task, 3)
        self.assertTrue(listener.closed)
        self.assertTrue(service._stop_requested.is_set())
        control.connection_manager.close_all.assert_awaited_once()

    async def test_pause_drains_current_update_then_skips_pulses_until_resumed(self):
        entered, release = asyncio.Event(), asyncio.Event()
        calls = []
        async def update():
            calls.append('update')
            entered.set()
            await release.wait()
        service = scheduler(update)
        active = asyncio.create_task(service._run_updates())
        await entered.wait()
        pause = asyncio.create_task(service.pause_updates())
        await asyncio.sleep(0)
        self.assertFalse(pause.done())
        release.set()
        await active
        await pause
        await service._run_updates()
        self.assertEqual(calls, ['update'])
        service.resume_updates()
        await service._run_updates()
        self.assertEqual(calls, ['update', 'update'])

    async def test_background_scheduler_runs_world_and_session_mutations_on_socket_loop(self):
        owner_loop = asyncio.get_running_loop()
        owner_thread = threading.get_ident()
        sessions = SessionHandler()
        entered, release = asyncio.Event(), asyncio.Event()
        observations = []

        async def update():
            observations.append((threading.get_ident(), asyncio.get_running_loop()))
            sessions.create_session('world').status = SessionStatus.PLAYING
            entered.set()
            await release.wait()
            self.assertEqual({'world', 'socket'}, {s.session_id for s in sessions.get_playing_sessions()})

        service = scheduler(update)
        service.set_runtime_loop(owner_loop)

        def run_pulse():
            thread_id = threading.get_ident()
            asyncio.run(service._run_updates())
            return thread_id

        task = asyncio.create_task(asyncio.to_thread(run_pulse))
        try:
            await asyncio.wait_for(entered.wait(), 1)
            sessions.create_session('socket').status = SessionStatus.PLAYING
        finally:
            release.set()
        scheduler_thread = await asyncio.wait_for(task, 1)
        self.assertNotEqual(owner_thread, scheduler_thread)
        self.assertEqual([(owner_thread, owner_loop)], observations)

    async def test_scheduler_waits_for_each_pulse_and_stops_without_overlap(self):
        entered = asyncio.Event()
        pulses, in_progress = [], 0

        async def update():
            nonlocal in_progress
            in_progress += 1
            self.assertEqual(1, in_progress)
            pulses.append(threading.get_ident())
            await asyncio.sleep(0)
            in_progress -= 1
            if len(pulses) == 3:
                service.stop()
                entered.set()

        service = scheduler(update)
        service.set_runtime_loop(asyncio.get_running_loop())
        task = asyncio.create_task(asyncio.to_thread(lambda: asyncio.run(service.start())))
        await asyncio.wait_for(entered.wait(), 1)
        await asyncio.wait_for(task, 1)
        self.assertEqual([threading.get_ident()] * 3, pulses)
        self.assertIsNone(service._pending_update)

    async def test_stopping_scheduler_cancels_pending_owner_update(self):
        entered, cancelled = asyncio.Event(), asyncio.Event()

        async def update():
            entered.set()
            try:
                await asyncio.Event().wait()
            finally:
                cancelled.set()

        service = scheduler(update)
        service.set_runtime_loop(asyncio.get_running_loop())
        task = asyncio.create_task(asyncio.to_thread(lambda: asyncio.run(service.start())))
        await asyncio.wait_for(entered.wait(), 1)
        service.stop()
        await asyncio.wait_for(task, 1)
        await asyncio.wait_for(cancelled.wait(), 1)
        self.assertIsNone(service._pending_update)

    async def test_owner_update_errors_propagate_to_scheduler(self):
        async def update():
            raise ValueError('failed pulse')
        service = scheduler(update)
        service.set_runtime_loop(asyncio.get_running_loop())
        with self.assertRaisesRegex(ValueError, 'failed pulse'):
            await asyncio.to_thread(lambda: asyncio.run(service._run_updates()))
        self.assertIsNone(service._pending_update)

    async def test_standalone_service_uses_current_loop(self):
        observed = []
        async def update():
            observed.append(asyncio.get_running_loop())
        service = scheduler(update)
        await service._run_updates()
        self.assertEqual([asyncio.get_running_loop()], observed)

    async def test_server_configures_owner_and_stops_background_scheduler_on_cancel(self):
        updated = asyncio.Event()
        async def update():
            self.assertIs(asyncio.get_running_loop(), owner)
            updated.set()
        owner = asyncio.get_running_loop()
        service = scheduler(update)
        server = MudServer.__new__(MudServer)
        server.logger = Mock()
        control = NS(bind_listener=Mock())
        async def wait_stopped():
            await asyncio.Event().wait()
        control.wait_stopped = wait_stopped
        server.injector = Mock(get=lambda cls: service if cls is GameService else control)
        server.host, server.port = 'localhost', 0

        class Listener:
            async def __aenter__(self):
                return self
            async def __aexit__(self, *args):
                self.closed = True
            async def serve_forever(self):
                await asyncio.Event().wait()
        listener = Listener()
        with patch('server.MudServer.asyncio.start_server', new=AsyncMock(return_value=listener)):
            task = asyncio.create_task(server.start())
            await asyncio.wait_for(updated.wait(), 1)
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await asyncio.wait_for(task, 3)
        self.assertTrue(listener.closed)
        self.assertTrue(service._stop_requested.is_set())
        self.assertIsNone(service._pending_update)
        server.logger.warning.assert_not_called()


class NoteRegistrySnapshotTests(unittest.TestCase):
    def test_note_filter_uses_snapshot_while_worker_publishes_a_note(self):
        from notes.NoteRegistry import NoteRegistry
        registry = NoteRegistry()
        entered, published = threading.Event(), threading.Event()
        class BlockingNote:
            id = 'existing'
            @property
            def type(self):
                entered.set()
                if not published.wait(1):
                    raise AssertionError('Writer could not publish while the snapshot was filtered')
                return 0
        existing = BlockingNote()
        registry.register_note(existing)
        def publish():
            if entered.wait(1):
                registry.register_note(NS(id='new', type=0))
                published.set()
        worker = threading.Thread(target=publish)
        worker.start()
        try:
            self.assertEqual([existing], registry.get_notes_by_type(0))
            self.assertEqual(2, len(registry.all_notes()))
        finally:
            worker.join(2)
        self.assertFalse(worker.is_alive())


if __name__ == '__main__':
    unittest.main()
