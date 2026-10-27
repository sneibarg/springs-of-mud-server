"""Coordinate a saved shutdown on the socket event loop."""

import asyncio

from injector import inject

from api.CharacterApi import CharacterApi
from game.GameService import GameService
from player.CharacterService import CharacterService
from server.connection.ConnectionManager import ConnectionManager
from server.session.SessionHandler import SessionHandler
from server.LoggerFactory import LoggerFactory


class RuntimeControl:
    @inject
    def __init__(self, game_service: GameService, character_service: CharacterService,
                 session_handler: SessionHandler, connection_manager: ConnectionManager):
        self.game_service = game_service
        self.character_service = character_service
        self.session_handler = session_handler
        self.connection_manager = connection_manager
        self.shutting_down = False
        self.shutdown_kind = None
        self._listener = None
        self._stopped = asyncio.Event()
        self.logger = LoggerFactory.get_logger(__name__)

    def bind_listener(self, listener):
        self._listener = listener

    async def wait_stopped(self):
        await self._stopped.wait()

    async def shutdown(self, kind: str, before_close=None) -> bool:
        if self.shutting_down or self._listener is None:
            return False
        self.shutting_down = True
        sessions = self.session_handler.get_active_sessions()
        committed = False
        try:
            for session in sessions:
                session.metadata['shutdown_pending'] = True
            await self.game_service.pause_updates()
            current = asyncio.current_task()
            pending_commands = [session.metadata['command_idle'].wait() for session in sessions
                                if session.metadata.get('command_task') is not None
                                and session.metadata['command_task'] is not current]
            if pending_commands:
                await asyncio.gather(*pending_commands)
            characters = {}
            for session in sessions:
                character = session.metadata.get('switched_original') or session.character
                if character is not None and not CharacterApi.is_npc(character):
                    characters[character.id] = character
            # Every snapshot is captured on the owner loop before waiting for I/O.
            futures = [self.character_service.queue_save_character(character) for character in characters.values()]
            results = await asyncio.gather(*(asyncio.wrap_future(future) for future in futures), return_exceptions=True)
            if any(result is not True for result in results):
                return False
            if before_close is not None:
                await before_close()
            self.shutdown_kind = kind
            committed = True
            try:
                self._listener.close()
                await self._listener.wait_closed()
            finally:
                self.game_service.stop()
                try:
                    await self.connection_manager.close_all()
                finally:
                    self._stopped.set()
            return True
        except Exception:
            self.logger.exception("Saved shutdown failed")
            return committed
        finally:
            if not committed:
                self.shutting_down = False
                self.game_service.resume_updates()
                for session in sessions:
                    session.metadata.pop('shutdown_pending', None)
