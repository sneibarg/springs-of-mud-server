import asyncio
import threading

from asyncio import StreamReader, StreamWriter
from typing import Optional
from injector import inject

from area.RoomHandler import RoomHandler
from area.Area import Area
from area.Room import Room
from command.CommandService import CommandService
from server.connection.TelnetConnection import TelnetConnection
from server.connection.ConnectionManager import ConnectionManager
from server.session.SessionHandler import SessionHandler
from server.session.SessionState import SessionStatus, SessionState
from server.session.AuthenticationService import AuthenticationService
from server.messaging.MessageBus import MessageBus
from server.protocol.Message import MessageType, Message
from server.LoggerFactory import LoggerFactory
from player.Player import Player
from player.Character import Character
from registry.RegistryService import RegistryService


class ConnectionHandler:
    @inject
    def __init__(self,
                 connection_manager: ConnectionManager,
                 session_handler: SessionHandler,
                 message_bus: MessageBus,
                 registry_service: RegistryService,
                 room_handler: RoomHandler,
                 auth_service: AuthenticationService,
                 command_service: CommandService):
        self.logger = LoggerFactory.get_logger(__name__)
        self.session_handler = session_handler
        self.connection_manager = connection_manager
        self.message_bus = message_bus
        self.registry_service = registry_service
        self.room_handler = room_handler
        self.auth_service = auth_service
        self.command_service = command_service

    async def _receive_initial_message(self, connection: TelnetConnection, session: SessionState) -> tuple[bool, str | None, Character | None] | tuple[bool, None, None]:
        first_msg = await connection.receive_message()
        self.logger.debug(f"Received message: {first_msg.type if first_msg else 'None'}, data: {first_msg.data if first_msg else 'None'}")
        if first_msg and first_msg.type == MessageType.AUTH:
            self.logger.info(f"Payload-based auth attempt on session {session.session_id}")
            success, player_id, character = await self.auth_service.authenticate_with_payload(connection, session, first_msg.data)
            if success:
                self.connection_manager.bind_character(character.id, session.session_id)
                self.logger.debug(f"Character {character.id} authenticated via payload on session {session.session_id}")
                self.logger.debug(f"Player character is: {character}")
                return success, player_id, character
            else:
                await connection.send_text("Authentication failed.\r\n", MessageType.ERROR)
                return False, None, None
        else:
            self.logger.warning(f"Invalid authentication message. Expected AUTH_PAYLOAD, got: {first_msg.type if first_msg else 'None'}")
            await connection.send_text("Invalid authentication message.\r\n", MessageType.ERROR)
            return False, None, None

    async def handle_new_connection(self, reader: StreamReader, writer: StreamWriter) -> None:
        connection, session, peer_info = None, None, None
        try:
            connection = TelnetConnection(reader, writer)
            session = self.session_handler.create_session(connection.session_id)
            self.connection_manager.add_connection(connection)
            peer_info = connection.get_peer_info()
            self.logger.info(f"New connection from {peer_info}: session {session.session_id}")

            await self._send_welcome(connection)
            success, player_id, character = await self._receive_initial_message(connection, session)
            if not success:
                return

            player = await self._nanny(character, session, connection)
            area, room = self._get_area_and_room(character)
            await self.room_handler.print_room(character.id, room)
            await self.message_bus.send_prompt(character.id, character, area, room)
            await self._game_loop(connection, session, player, character)
        except Exception as e:
            self.logger.error(f"Error handling connection: {e}", exc_info=True)
        finally:
            if connection:
                await connection.close()
            if session:
                self.session_handler.remove_session(session.session_id)
                if session.character:
                    self.connection_manager.unbind_character(session.character.id)
                self.connection_manager.remove_connection(connection.session_id)
            self.logger.info(f"Connection closed: {peer_info if connection else 'unknown'}")

    @staticmethod
    async def _send_welcome(connection: TelnetConnection) -> None:
        welcome = f"Welcome to the server!\n\n\n\n"
        await connection.send_text(welcome, MessageType.GAME)

    async def _game_loop(self, connection: TelnetConnection, session, player, character) -> None:
        while not connection.is_closed() and (session.is_playing() or session.is_idle()):
            try:
                if not session.is_idle() and self.session_handler.is_session_idle(session):
                    session.status = SessionStatus.IDLING

                message = await self._wait_for_message(connection, session)
                if message is None:
                    break
                session.update_activity()
                area, room = self._get_area_and_room(character)
                if message.type == MessageType.GAME and not message.get('text'):
                    await self.message_bus.send_prompt(character.id, character, area, room)
                    continue

                if message.type == MessageType.GAME:
                    await self.command_service.handle_command(player, character, message.get('text', ''))
                    await self.message_bus.send_prompt(character.id, character, area, room)
            except Exception as e:
                self.logger.error(f"Error in game loop: {e}", exc_info=True)
                break

    async def _wait_for_message(self, connection: TelnetConnection, session: SessionState) -> Message | None:
        try:
            return await asyncio.wait_for(connection.receive_message(), timeout=self.session_handler.max_idle_time)
        except asyncio.TimeoutError:
            if not session.is_idle():
                session.status = SessionStatus.IDLING
                self.logger.info(f"Session {session.session_id} timed out")
                await connection.send_text("You have disappeared into the void.\n\r", MessageType.GAME)
                return None

    @staticmethod
    def _update_character(character) -> None:
        character.lock = threading.Lock()

    def _update_player(self, session, character) -> Player | None:
        account = self.registry_service.player_registry.get_player_by_id(session.player_id)
        if account:
            account.current_character = character
            account.ansi_enabled = session.ansi_enabled
        return account

    def _get_area_and_room(self, character) -> tuple[Area | None, Room | None]:
        area = self.registry_service.area_registry.get_area_by_id(character.area_id)
        room = self.registry_service.room_registry.get_room_by_id(character.room_id)
        return area, room

    async def _nanny(self, character, session, connection) -> Optional[Player]:
        self._update_character(character)
        session.character = character
        player = self._update_player(session, character)

        if player is not None and player.banned:
            await connection.send_text("You have been banned from the server.\r\n", MessageType.ERROR)
            await connection.close()
            return None
        elif player is None:
            await connection.send_text("Player not registered. Please try again.\r\n", MessageType.ERROR)
            return None
        player.current_characters.append(character)
        self.logger.info(f"Player {player.first_name} {player.last_name} is now playing {character.name}.")
        session.status = SessionStatus.PLAYING
        return player
