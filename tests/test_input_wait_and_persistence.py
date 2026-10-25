import asyncio
import sys
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import requests
from game.UpdateHandler import UpdateHandler
from notes.InGameNote import InGameNote
from notes.NoteHandler import NoteHandler
from player.AdvancementHandler import AdvancementHandler
from player.CharacterService import CharacterService
from player.PlayerService import PlayerService
from game.GameService import GameService
from combat.CombatHandler import FightHandler
from player.Character import Character
from mobile.Mobile import Mobile
from server.handlers.ConnectionHandler import ConnectionHandler
from server.protocol.Message import Message, MessageType
from server.session.SessionState import SessionState, SessionStatus


class TestInputWait(unittest.IsolatedAsyncioTestCase):
    def setup_session(self, wait=0):
        character = NS(id="player", status_flags=NS(pulse_wait=wait, pulse_daze=3))
        session = SessionState("session", status=SessionStatus.PLAYING, character=character)
        sessions = NS(get_playing_sessions=lambda: [session], is_session_idle=lambda _: False)
        update = UpdateHandler.__new__(UpdateHandler)
        update.session_handler = sessions
        update.entity_update_handler = NS(room_registry=NS(all_rooms=lambda: []))
        handler = ConnectionHandler.__new__(ConnectionHandler)
        handler.session_handler = sessions
        handler.logger = Mock()
        return character, session, update, handler

    async def test_typed_commands_stay_ordered_until_world_pulses_release_wait(self):
        character, session, update, handler = self.setup_session()
        connection = Mock(is_closed=Mock(return_value=False))
        handler._wait_for_message = AsyncMock(side_effect=[
            Message(MessageType.GAME, {"text": "first"}),
            Message(MessageType.GAME, {"text": "second"}), None])
        handler._get_area_and_room = lambda _: (None, None)
        handler.message_bus = Mock(mirror_snoop_input=AsyncMock(), send_prompt=AsyncMock())
        first, second = asyncio.Event(), asyncio.Event()
        commands = []

        async def execute(player, actor, text):
            commands.append(text)
            if text == "first":
                actor.status_flags.pulse_wait = 2
                first.set()
            else:
                second.set()

        handler.command_handler = NS(handle_command=execute)
        task = asyncio.create_task(handler._game_loop(connection, session, None, character))
        try:
            await asyncio.wait_for(first.wait(), 1)
            update._advance_input_timers()
            await asyncio.sleep(0)
            self.assertEqual(["first"], commands)
            update._advance_input_timers()
            await asyncio.wait_for(second.wait(), 1)
            await asyncio.wait_for(task, 1)
            self.assertEqual(["first", "second"], commands)
        finally:
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)

    async def test_disconnect_abandons_waiting_command(self):
        _, session, _, handler = self.setup_session(wait=99)
        connection = Mock(is_closed=Mock(return_value=False))
        task = asyncio.create_task(handler._wait_for_action_ready(connection, session))
        await asyncio.sleep(0)
        connection.is_closed.return_value = True
        self.assertFalse(await asyncio.wait_for(task, 1))

    async def test_pulses_recover_outside_combat_and_do_not_double_count_original(self):
        original, session, update, _ = self.setup_session(wait=2)
        session.metadata["switched_original"] = original
        update._advance_input_timers()
        self.assertEqual(1, original.status_flags.pulse_wait)
        body = NS(status_flags=NS(pulse_wait=1, pulse_daze=1))
        session.character = body
        update._advance_input_timers()
        self.assertEqual(0, body.status_flags.pulse_wait)
        self.assertEqual(0, original.status_flags.pulse_wait)
        self.assertEqual(1, original.status_flags.pulse_daze)

    async def test_link_dead_players_recover_and_connected_players_are_not_counted_twice(self):
        character, _, update, _ = self.setup_session(wait=2)
        disconnected = NS(status_flags=NS(pulse_wait=1, pulse_daze=0))
        update.entity_update_handler.room_registry.all_rooms = lambda: [
            NS(characters={"connected": character, "disconnected": disconnected})]
        update._advance_input_timers()
        self.assertEqual(1, character.status_flags.pulse_wait)
        self.assertEqual(0, disconnected.status_flags.pulse_wait)

    async def test_combat_does_not_decrement_player_or_controlled_body_timers_again(self):
        player = Character.__new__(Character)
        player.context = {}
        player.status_flags = NS(pulse_wait=4, pulse_daze=3)
        body = Mobile.__new__(Mobile)
        body.context = {"controller_original": player}
        body.status_flags = NS(pulse_wait=2, pulse_daze=1)
        for entity in (player, body):
            before = vars(entity.status_flags).copy()
            FightHandler._decrement_combat_timers(entity)
            self.assertEqual(before, vars(entity.status_flags))


class TestPersistenceBoundary(unittest.IsolatedAsyncioTestCase):
    def service(self):
        service = CharacterService.__new__(CharacterService)
        service.logger = Mock()
        service.characters_endpoint = "http://unused/characters"
        service.character_registry = Mock()
        service._serialize_character = lambda character: character.state
        character = NS(lock=threading.RLock(), state={"id": "player", "level": 1,
                                                     "inventory": [{"name": "bag"}]})
        return service, character

    async def test_saves_snapshot_on_caller_and_commit_in_order_without_blocking_loop(self):
        service, character = self.service()
        entered, release = threading.Event(), threading.Event()
        writes = []

        def put(url, *, json, timeout):
            writes.append(json)
            entered.set()
            if not release.wait(2):
                raise requests.Timeout("test release timed out")
            return Mock()

        with patch("player.CharacterService.requests.put", side_effect=put):
            first = service.queue_save_character(character)
            try:
                self.assertTrue(await asyncio.to_thread(entered.wait, 1))
                character.state["level"] = 2
                second = service.queue_save_character(character)
                character.state["inventory"][0]["name"] = "changed"
                self.assertFalse(first.done())
                self.assertFalse(second.done())
                # A scheduled callback still runs while the HTTP worker is held.
                progress = asyncio.Event()
                asyncio.get_running_loop().call_soon(progress.set)
                await asyncio.wait_for(progress.wait(), 1)
            finally:
                release.set()
            self.assertTrue(await asyncio.wrap_future(first))
            self.assertTrue(await asyncio.wrap_future(second))
        self.assertEqual([1, 2], [payload["level"] for payload in writes])
        self.assertEqual(["bag", "bag"], [payload["inventory"][0]["name"] for payload in writes])

    async def test_manual_save_returns_actual_http_failure(self):
        service, character = self.service()
        with patch("player.CharacterService.requests.put", side_effect=requests.Timeout("offline")):
            self.assertFalse(await service.save_character_async(character))

    async def test_cancelled_manual_wait_does_not_cancel_its_queued_write(self):
        service, character = self.service()
        entered, release = threading.Event(), threading.Event()
        writes = []

        def put(*args, **kwargs):
            entered.set()
            if not release.wait(2):
                raise requests.Timeout("test release timed out")
            writes.append(kwargs["json"])
            return Mock()

        with patch("player.CharacterService.requests.put", side_effect=put):
            first = service.queue_save_character(character)
            try:
                self.assertTrue(await asyncio.to_thread(entered.wait, 1))
                pending = asyncio.create_task(service.save_character_async(character))
                await asyncio.sleep(0)
                pending.cancel()
                await asyncio.gather(pending, return_exceptions=True)
            finally:
                release.set()
            await asyncio.wrap_future(first)
            # A sentinel write completes after the cancelled caller's write.
            await asyncio.wrap_future(service.queue_save_character(character))
        self.assertEqual(3, len(writes))

    async def test_account_and_deny_list_queues_capture_values_before_worker_runs(self):
        entered, release = threading.Event(), threading.Event()
        from server.BackgroundIO import submit

        def hold_worker():
            entered.set()
            return release.wait(2)

        blocker = submit(hold_worker)
        self.assertTrue(await asyncio.to_thread(entered.wait, 1))
        player_service = PlayerService.__new__(PlayerService)
        player_service._serialize_player = lambda player: player.state
        player_service._persist_player = Mock(return_value=True)
        player = NS(lock=threading.Lock(), state={"id": "account", "banned": True})
        game = GameService.__new__(GameService)
        game.game_data = NS(id="game", denyList=["site"])
        game._persist_deny_list = Mock(return_value=True)
        try:
            account_save = player_service.queue_save_player(player)
            deny_save = game.queue_save_deny_list()
            player.state["banned"] = False
            game.game_data.denyList.clear()
        finally:
            release.set()
        await asyncio.gather(*(asyncio.wrap_future(future) for future in (blocker, account_save, deny_save)))
        player_service._persist_player.assert_called_once_with({"id": "account", "banned": True})
        game._persist_deny_list.assert_called_once_with("game", {"denyList": ["site"]})

    async def test_autosave_and_level_gain_queue_without_waiting_for_completion(self):
        service, character = self.service()
        character.id, character.name = "player", "Player"
        entered, release = threading.Event(), threading.Event()
        futures = []
        original_queue = service.queue_save_character

        def queue(actor):
            future = original_queue(actor)
            futures.append(future)
            return future

        service.queue_save_character = queue
        update = UpdateHandler.__new__(UpdateHandler)
        update._live_player_characters = lambda: [character]
        update.character_service = service
        update._autosave_bucket = lambda _: 0
        update.save_number = 0
        advancement = AdvancementHandler(service, Mock(), Mock())

        def put(*args, **kwargs):
            entered.set()
            if not release.wait(2):
                raise requests.Timeout("test release timed out")
            return Mock()

        with patch("player.CharacterService.requests.put", side_effect=put):
            try:
                await asyncio.wait_for(update._autosave_due_characters(), 0.5)
                self.assertTrue(await asyncio.to_thread(entered.wait, 1))
                advancement.level_gained(character, NS(level=2))
                self.assertEqual(2, len(futures))
                self.assertFalse(futures[-1].done())
            finally:
                release.set()
            await asyncio.gather(*(asyncio.wrap_future(future) for future in futures))

    async def test_slow_note_fetch_yields_before_domain_read_state_changes(self):
        entered, release = threading.Event(), threading.Event()
        character = NS(name="Reader", context={})
        note = InGameNote(id="note", to_list="all", subject="Hello", date_stamp=10)

        def fetch(kind):
            entered.set()
            if not release.wait(2):
                raise RuntimeError("test release timed out")
            return [note]

        handler = NoteHandler(None, NS(get_notes_by_type=fetch), None, Mock())
        context = NS(command=NS(name="note"), result="read 1", parameters=[], finish=lambda: None)
        task = asyncio.create_task(handler.execute(character, context))
        try:
            self.assertTrue(await asyncio.to_thread(entered.wait, 1))
            self.assertFalse(task.done())
            self.assertNotIn("note_read_stamps", character.context)
        finally:
            release.set()
        payload = await asyncio.wait_for(task, 1)
        self.assertIn("Hello", payload["to_char"])
        self.assertEqual(10, character.context["note_read_stamps"]["0"])


if __name__ == "__main__":
    unittest.main()
