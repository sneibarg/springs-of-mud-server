import asyncio
import threading

from asyncio import StreamReader, StreamWriter
from typing import Tuple
from injector import inject
from area.RoomService import RoomService
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
from server.ServerUtil import ServerUtil
from player.Character import Character
from player.Player import Player
from player.PlayerService import PlayerService


class ConnectionHandler:
    @inject
    def __init__(self,
                 connection_manager: ConnectionManager,
                 session_handler: SessionHandler,
                 message_bus: MessageBus,
                 player_service: PlayerService,
                 room_service: RoomService,
                 auth_service: AuthenticationService,
                 command_service: CommandService):
        self.logger = LoggerFactory.get_logger(__name__)
        self.session_handler = session_handler
        self.connection_manager = connection_manager
        self.session_handler = session_handler
        self.message_bus = message_bus
        self.player_service = player_service
        self.room_service = room_service
        self.registry_service = player_service.registry_service
        self.auth_service = auth_service
        self.command_service = command_service

    async def _receive_initial_message(self, connection: TelnetConnection, session: SessionState) -> Tuple[bool, None | str, None | dict]:
        first_msg = await connection.receive_message()
        self.logger.debug(
            f"Received message: {first_msg.type if first_msg else 'None'}, data: {first_msg.data if first_msg else 'None'}")
        if first_msg and first_msg.type == MessageType.AUTH:
            self.logger.info(f"Payload-based auth attempt on session {session.session_id}")
            success, player_id, character_data = await self.auth_service.authenticate_with_payload(connection, session,                                                                               first_msg.data)
            if success:
                self.connection_manager.bind_player(player_id, session.session_id)
                self.logger.info(f"Player {player_id} authenticated via payload on session {session.session_id}")
                return success, player_id, character_data
            else:
                await connection.send_text("Authentication failed.\r\n", MessageType.ERROR)
                return False, None, None
        else:
            self.logger.warning(
                f"Invalid authentication message. Expected AUTH_PAYLOAD, got: {first_msg.type if first_msg else 'None'}")
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
            success, player_id, character_data = await self._receive_initial_message(connection, session)
            if not success:
                return

            player, character = await self._nanny(character_data, session, connection)
            area, room = self._get_area_and_room(character)

            await self.room_service.print_room(player.id, self.registry_service.room_registry[character.room_id])
            await self.message_bus.send_prompt(session.player_id, character, area, room)
            await self._game_loop(connection, session, player, character)
        except Exception as e:
            self.logger.error(f"Error handling connection: {e}", exc_info=True)
        finally:
            if connection:
                await connection.close()
            if session:
                self.session_handler.remove_session(session.session_id)
                if session.player_id:
                    self.connection_manager.unbind_player(session.player_id)
                self.connection_manager.remove_connection(connection.session_id)
            self.logger.info(f"Connection closed: {peer_info if connection else 'unknown'}")

    @staticmethod
    async def _send_welcome(connection: TelnetConnection) -> None:
        welcome = f"Welcome to the server!\n\n\n\n"
        await connection.send_text(welcome, MessageType.GAME)

    async def _game_loop(self, connection: TelnetConnection, session, player, character) -> None:
        while not connection.is_closed() and session.is_playing() or session.is_idle():
            try:
                if not session.is_idle() and self.session_handler.is_session_idle(session):
                    session.status = SessionStatus.IDLING

                message = await self._wait_for_message(connection, session)
                if message is None:
                    break
                session.update_activity()
                if message.type == MessageType.GAME and not message.get('text'):
                    area, room = self._get_area_and_room(character)
                    await self.message_bus.send_prompt(session.player_id, character, area, room)
                    continue

                if message.type == MessageType.GAME:
                    area, room = self._get_area_and_room(character)
                    await self.command_service.handle_command(player, message.get('text', ''))
                    await self.message_bus.send_prompt(session.player_id, character, area, room)
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
    def _get_character(character_data) -> Character:
        character_definition = ServerUtil.camel_to_snake_case(character_data) if character_data else {}
        character_definition['lock'] = threading.Lock()
        return Character.from_json(character_definition)

    def _get_or_create_player(self, session, character):
        account = self.player_service.get_account_by_id(session.player_id)
        if account:
            account_data = ServerUtil.camel_to_snake_case(account)
            account_data['current_character'] = character
            account_data['ansi_enabled'] = session.ansi_enabled
            return Player.from_json(account_data)
        return None

    def _get_area_and_room(self, character) -> Tuple[Area, Room]:
        area = self.registry_service.area_registry[character.area_id]
        room = self.registry_service.room_registry[character.room_id]
        return area, room

    async def _nanny(self, character_data, session, connection) -> Tuple[Player, Character]:
        character = self._get_character(character_data)
        session.character = character
        player = self._get_or_create_player(session, character)

        if player.banned:
            await connection.send_text("You have been banned from the server.\r\n", MessageType.ERROR)
            await connection.close()

        self.registry_service.register_character(character)
        session.status = SessionStatus.PLAYING
        return player, character
