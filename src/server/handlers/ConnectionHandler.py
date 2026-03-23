from asyncio import StreamReader, StreamWriter
from typing import Tuple
from injector import inject, Injector
from area import AreaService, RoomService
from command import CommandHandler
from event import EventHandler
from server.connection import TelnetConnection, ConnectionManager
from server.session import SessionHandler, SessionStatus, AuthenticationService
from server.messaging import MessageBus
from server.protocol import MessageType
from server.LoggerFactory import LoggerFactory
from server.ServerUtil import ServerUtil
from player import Character, Player, PlayerService

import threading


class ConnectionHandler:
    @inject
    def __init__(self,
                 injector: Injector,
                 connection_manager: ConnectionManager,
                 session_handler: SessionHandler,
                 message_bus: MessageBus,
                 player_service: PlayerService,
                 auth_service: AuthenticationService,
                 command_handler: CommandHandler,
                 event_handler: EventHandler):
        self.injector = injector
        self.logger = LoggerFactory.get_logger(__name__)
        self.connection_manager = connection_manager
        self.session_handler = session_handler
        self.message_bus = message_bus
        self.player_service = player_service
        self.auth_service = auth_service
        self.command_handler = command_handler
        self.event_handler = event_handler

    async def handle_new_connection(self, reader: StreamReader, writer: StreamWriter) -> None:
        connection, session, peer_info = None, None, None
        try:
            connection = TelnetConnection(reader, writer)
            session = self.session_handler.create_session(connection.session_id)
            self.connection_manager.add_connection(connection)
            peer_info = connection.get_peer_info()
            self.logger.info(f"New connection from {peer_info}: session {session.session_id}")

            await self._send_welcome(connection)

            first_msg = await connection.receive_message()
            self.logger.debug(f"Received message: {first_msg.type if first_msg else 'None'}, data: {first_msg.data if first_msg else 'None'}")
            if first_msg and first_msg.type == MessageType.AUTH:
                self.logger.info(f"Payload-based auth attempt on session {session.session_id}")
                success, player_id, character_data = await self.auth_service.authenticate_with_payload(connection, session, first_msg.data)
                if success:
                    self.connection_manager.bind_player(player_id, session.session_id)
                    self.logger.info(f"Player {player_id} authenticated via payload on session {session.session_id}")
                else:
                    await connection.send_text("Authentication failed.\r\n", MessageType.ERROR)
                    return
            else:
                self.logger.warning(f"Invalid authentication message. Expected AUTH_PAYLOAD, got: {first_msg.type if first_msg else 'None'}")
                await connection.send_text("Invalid authentication message.\r\n", MessageType.ERROR)
                return

            character, player = self._nanny(character_data, writer, reader, session, connection)
            self.player_service.registry_service.character_registry[character.id] = character
            session.status = SessionStatus.PLAYING

            await self._show_room(connection, character)
            await self.message_bus.send_prompt(session.player_id, character.health, character.mana, character.movement)
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

    async def _show_room(self, connection: TelnetConnection, character) -> None:
        area_service = self.injector.get(AreaService)
        room_service = self.injector.get(RoomService)
        room = area_service.get_registry().room_registry[character.room_id]
        exits = []
        if room.exit_north: exits.append("north")
        if room.exit_south: exits.append("south")
        if room.exit_east: exits.append("east")
        if room.exit_west: exits.append("west")
        if room.exit_up: exits.append("up")
        if room.exit_down: exits.append("down")

        message = room_service.format_room_description(room.name, room.description, exits)
        await connection.send_message(message)

    async def _game_loop(self, connection: TelnetConnection, session, player, character) -> None:
        while not connection.is_closed() and session.is_playing():
            try:
                if not session.is_idle() and self.session_handler.is_session_idle(session):
                    session.status = SessionStatus.IDLING

                message = await connection.receive_message()
                if not message:
                    break

                session.update_activity()
                if message.type == MessageType.GAME and not message.get('text'):
                    await self.message_bus.send_prompt(session.player_id, character.health, character.mana, character.movement)
                    continue

                if message.type == MessageType.GAME:
                    command_text = message.get('text', '')
                    self.command_handler.handle_command(player, command_text)

                    await self.message_bus.send_prompt(session.player_id, character.health, character.mana, character.movement)
            except Exception as e:
                self.logger.error(f"Error in game loop: {e}", exc_info=True)
                break

    def _get_character(self, character_data, writer, reader) -> Character:
        character_definition = ServerUtil.camel_to_snake_case(character_data) if character_data else {}
        character_definition['injector'] = self.injector
        character_definition['writer'] = writer
        character_definition['reader'] = reader
        character_definition['lock'] = threading.Lock()
        return Character.from_json(character_definition)

    def _get_or_create_player(self, session, character):
        account = self.player_service.get_account_by_id(session.player_id)
        if account:
            account_data = ServerUtil.camel_to_snake_case(account)
            account_data['connection'] = (character.reader, character.writer)
            account_data['current_character'] = character
            account_data['ansi_enabled'] = session.ansi_enabled
            return Player.from_json(account_data)
        return None

    async def _nanny(self, character_data, writer, reader, session, connection) -> Tuple[Player, Character]:
        character = self._get_character(character_data, writer, reader)
        session.character = character
        player = self._get_or_create_player(session, character)

        if player.banned:
            await connection.send_text("You have been banned from the server.\r\n", MessageType.ERROR)
            connection.disconnect()

        return player, character
