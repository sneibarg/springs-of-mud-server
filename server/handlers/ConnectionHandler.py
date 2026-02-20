from asyncio import StreamReader, StreamWriter
from server.connection import TelnetConnection, ConnectionManager
from server.session import SessionHandler, SessionPhase, AuthenticationService
from server.messaging import MessageBus, MessageFormatter
from server.protocol import MessageType
from server.LoggerFactory import LoggerFactory


class ConnectionHandler:
    """
    Handles new client connections and manages the connection lifecycle.
    Orchestrates authentication, character selection, and gameplay.
    """

    def __init__(self, mud_server):
        self.mud_server = mud_server
        self.injector = mud_server.injector
        self.connection_manager = ConnectionManager()
        self.session_handler = SessionHandler()
        self.message_bus = MessageBus(self.connection_manager, self.session_handler)
        self.logger = LoggerFactory.get_logger(__name__)

    async def handle_new_connection(self, reader: StreamReader, writer: StreamWriter) -> None:
        """
        Handle a new client connection.
        This is the main entry point for new connections.
        """
        connection = None
        session = None

        try:
            # Create connection and session
            connection = TelnetConnection(reader, writer)
            session = self.session_handler.create_session(connection.session_id)

            self.connection_manager.add_connection(connection)

            peer_info = connection.get_peer_info()
            self.logger.info(f"New connection from {peer_info}: session {session.session_id}")

            await self._send_welcome(connection)
            auth_service = AuthenticationService(self.injector.get(self.mud_server.player_service_class), self.injector)

            authenticated = False
            character_data = None

            first_msg = await connection.receive_message()
            if first_msg and first_msg.type == MessageType.CHAR_LOGON:
                self.logger.info(f"Payload-based auth attempt on session {session.session_id}")
                success, player_id, character_data = await auth_service.authenticate_with_payload(
                    connection, session, first_msg.data
                )

                if success:
                    authenticated = True
                    self.connection_manager.bind_player(player_id, session.session_id)
                    self.logger.info(f"Player {player_id} authenticated via payload on session {session.session_id}")
                else:
                    await connection.send_text("Authentication failed.\r\n", MessageType.ERROR)
                    return

            else:
                # Legacy authentication flow
                self.logger.info(f"Legacy auth flow on session {session.session_id}")

                # Prompt for ANSI support
                ansi_enabled = await self._prompt_ansi(connection)
                connection.set_ansi_enabled(ansi_enabled)
                session.ansi_enabled = ansi_enabled
                while session.can_authenticate() and not authenticated:
                    success, player_id = await auth_service.authenticate(connection, session)
                    if success:
                        authenticated = True
                        self.connection_manager.bind_player(player_id, session.session_id)
                        self.logger.info(f"Player {player_id} authenticated on session {session.session_id}")
                    elif session.auth_attempts >= 3:
                        await connection.send_text(
                            "You have exceeded the number of attempts. Connection will be terminated.\r\n",
                            MessageType.ERROR
                        )
                        return

                if not authenticated:
                    return

                attempts = 0
                max_attempts = 3
                while attempts < max_attempts and not character_data:
                    character_data = await auth_service.select_character(connection, session)
                    attempts += 1

                    if not character_data and attempts >= max_attempts:
                        await connection.send_text(
                            "Logging you off until you can stop making typos.\r\n",
                            MessageType.ERROR
                        )
                        return

                if not character_data:
                    return
            from player.Character import Character
            from server.server_util import camel_to_snake_case
            import threading

            character_definition = camel_to_snake_case(character_data)
            character_definition['injector'] = self.injector
            character_definition['writer'] = writer
            character_definition['reader'] = reader
            character_definition['lock'] = threading.Lock()
            character = Character.from_json(character_definition)
            from player import PlayerService
            player_service = self.injector.get(PlayerService)
            player = self._get_or_create_player(session, character)
            from event import EventHandler
            event_handler = self.injector.get(EventHandler)
            event_handler.register_character(character)
            session.phase = SessionPhase.PLAYING

            await self._show_room(connection, character)
            await self.message_bus.send_prompt(
                session.player_id,
                character.health,
                character.mana,
                character.movement
            )

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

    async def _send_welcome(self, connection: TelnetConnection) -> None:
        """Send welcome message"""
        welcome = f"Welcome to the server!\n\n\n\n"
        await connection.send_text(welcome, MessageType.WELCOME)

    async def _prompt_ansi(self, connection: TelnetConnection) -> bool:
        """Prompt for ANSI support"""
        await connection.send_text("Do you want ANSI colors? (Y/N) ", MessageType.ANSI_PROMPT)
        msg = await connection.receive_message()

        if msg:
            response = msg.get('text', '').strip().lower()
            return response == 'y'
        return False

    async def _show_room(self, connection: TelnetConnection, character) -> None:
        """Show current room to character"""
        from area.AreaService import AreaService
        area_service = self.injector.get(AreaService)

        room = area_service.get_registry().room_registry[character.room_id]
        exits = []
        if room.exit_north: exits.append("north")
        if room.exit_south: exits.append("south")
        if room.exit_east: exits.append("east")
        if room.exit_west: exits.append("west")
        if room.exit_up: exits.append("up")
        if room.exit_down: exits.append("down")

        message = MessageFormatter.format_room_description(room.name, room.description, exits)
        await connection.send_message(message)

    def _get_or_create_player(self, session, character):
        """Get or create Player object for session"""
        from player import PlayerService
        from player.Player import Player
        from server.server_util import camel_to_snake_case

        player_service = self.injector.get(PlayerService)
        account = player_service.get_account_by_id(session.player_id)

        if account:
            account_data = camel_to_snake_case(account)
            account_data['connection'] = (character.reader, character.writer)
            account_data['current_character'] = character
            account_data['ansi_enabled'] = session.ansi_enabled
            return Player.from_json(account_data)

        return None

    async def _game_loop(self, connection: TelnetConnection, session, player, character) -> None:
        """Main game loop for handling player commands"""
        from command import CommandHandler
        command_handler = self.injector.get(CommandHandler)

        while not connection.is_closed() and session.is_playing():
            try:
                message = await connection.receive_message()

                if not message:
                    break

                session.update_activity()
                if message.type == MessageType.INPUT and not message.get('text'):
                    await self.message_bus.send_prompt(
                        session.player_id,
                        character.health,
                        character.mana,
                        character.movement
                    )
                    continue

                if message.type == MessageType.COMMAND:
                    command_text = message.get('text', '')
                    command_handler.handle_command(player, command_text)
                    await self.message_bus.send_prompt(session.player_id, character.health, character.mana, character.movement)

            except Exception as e:
                self.logger.error(f"Error in game loop: {e}", exc_info=True)
                break
