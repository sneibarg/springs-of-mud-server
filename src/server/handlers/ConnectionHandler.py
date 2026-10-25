import asyncio

from asyncio import StreamReader, StreamWriter
from typing import Optional
from injector import inject

from area.RoomHandler import RoomHandler
from area.Area import Area
from area.Room import Room
from interp.InterpHandler import InterpHandler
from api.CharacterApi import CharacterApi
from api.GameApi import GameApi
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
from game.RegistryService import RegistryService
from game.GamePayload import GamePayload
from game.WizHandler import WizHandler
from combat.CombatHandler import FightHandler


class ConnectionHandler:
    LINK_MESSAGES = GamePayload.from_json({
        "toChar": {"reconnect": "Reconnecting. Type replay to see missed tells.\r\n"},
        "toRoom": {"lost": "{name} has lost {possessive} link.\r\n", "reconnect": "{name} has reconnected.\r\n"},
        "toWiznet": {"lost": "Net death has claimed {name}.\r\n",
                     "reconnect": "{name} groks the fullness of {possessive} link.\r\n"},
    })

    @inject
    def __init__(self,
                 connection_manager: ConnectionManager,
                 session_handler: SessionHandler,
                 message_bus: MessageBus,
                 registry_service: RegistryService,
                 room_handler: RoomHandler,
                 auth_service: AuthenticationService,
                 command_handler: InterpHandler,
                 fight_handler: FightHandler,
                 wiz_handler: WizHandler):
        self.logger = LoggerFactory.get_logger(__name__)
        self.session_handler = session_handler
        self.connection_manager = connection_manager
        self.message_bus = message_bus
        self.registry_service = registry_service
        self.room_handler = room_handler
        self.auth_service = auth_service
        self.command_handler = command_handler
        self.fight_handler = fight_handler
        self.wiz_handler = wiz_handler
        self._character_locks: dict[str, asyncio.Lock] = {}

    async def _receive_initial_message(self, connection: TelnetConnection, session: SessionState) -> tuple[bool, str | None, Character | None] | tuple[bool, None, None]:
        first_msg = await connection.receive_message()
        self.logger.debug(f"Received message: {first_msg.type if first_msg else 'None'}, data: {first_msg.data if first_msg else 'None'}")
        if first_msg and first_msg.type == MessageType.AUTH:
            self.logger.info(f"Payload-based auth attempt on session {session.session_id}")
            success, player_id, character = await self.auth_service.authenticate_with_payload(connection, session, first_msg.data)
            if success:
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
            if self._peer_denied(peer_info):
                await connection.send_text("Your site has been banned from this mud.\r\n", MessageType.ERROR)
                await connection.close()
                return

            await self._send_welcome(connection)
            success, player_id, character = await self._receive_initial_message(connection, session)
            if not success:
                return

            attached = await self._attach_character(character, session, connection)
            if attached is None:
                return
            player, character = attached
            if not session.metadata.get("entered_world", False):
                session.metadata["entered_world"] = True
                area, room = self._get_area_and_room(character)

                if room is not None:
                    occupants = list(room.characters.values())
                    room.add_player_to_room(character)
                    await self.room_handler.print_room(character.id, room)
                    players_text = room.get_players_in_room(character)
                    mobiles_text = room.get_mobiles_in_room(character)
                    if players_text:
                        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(players_text))
                    if mobiles_text:
                        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(mobiles_text))
                    for attacker, payload in self.fight_handler.aggressive_entry_rounds(character, room):
                        await self.fight_handler.emit_round_payload(attacker, payload)
                    await self.message_bus.send_prompt(character, area, room)
                    for viewer in occupants:
                        if viewer.id == character.id:
                            continue
                        if CharacterApi.can_see(viewer, character, room):
                            text = f"{character.name} has entered the game.\r\n"
                        else:
                            text = "Someone has entered the game.\r\n"
                        await self.message_bus.send_to_character(viewer.id, self.message_bus.text_to_message(text))

            await self._game_loop(connection, session, player, character)
        except Exception as e:
            self.logger.error(f"Error handling connection: {e}", exc_info=True)
        finally:
            try:
                if session:
                    await self._cleanup_session(session)
            finally:
                if connection:
                    await connection.close()
            self.logger.info(f"Connection closed: {peer_info if connection else 'unknown'}")

    def _character_lock(self, character_id: str) -> asyncio.Lock:
        return self._character_locks.setdefault(character_id, asyncio.Lock())

    def _live_character(self, character_id: str):
        for room in self.registry_service.room_registry.all_rooms():
            if room is not None:
                character = room.characters.get(character_id)
                if character is not None:
                    return character
        return None

    def _existing_connection(self, character_id: str):
        session = self.session_handler.get_session_by_character(character_id)
        if session is not None:
            connection = self.connection_manager.get_connection(session.session_id)
            if connection is not None:
                return connection
        return self.connection_manager.get_connection_by_character(character_id)

    async def _confirm_replacement(self, connection) -> bool:
        await connection.send_text("That character is already playing.\r\n")
        await connection.send_text("Do you wish to connect anyway (Y/N)?")
        while not connection.is_closed():
            try:
                message = await asyncio.wait_for(connection.receive_message(), self.session_handler.max_idle_time)
            except asyncio.TimeoutError:
                return False
            if message is None:
                return False
            answer = str(message.get("text", "") or "").strip().lower()
            if answer.startswith("y"):
                return True
            if answer.startswith("n"):
                return False
            await connection.send_text("Please type Y or N? ")
        return False

    async def _attach_character(self, character, session, connection):
        account = self.registry_service.player_registry.get_or_none(id=session.player_id)
        if account is None or account.banned:
            await self._nanny(character, session, connection)
            return None
        confirmed = False
        while not connection.is_closed():
            existing = self._existing_connection(character.id)
            if existing is not None and existing is not connection and not existing.is_closed() and not confirmed:
                if not await self._confirm_replacement(connection):
                    return None
                confirmed = True

            async with self._character_lock(character.id):
                # Another login may have completed while this client answered the prompt.
                existing = self._existing_connection(character.id)
                if existing is not None and existing is not connection:
                    if not existing.is_closed() and not confirmed:
                        continue
                    old_session = self.session_handler.get_session(existing.session_id)
                    if old_session is not None:
                        await self._detach_session(old_session)
                    else:
                        self.connection_manager.remove_connection(existing.session_id)
                    await existing.close()

                live_character = self._live_character(character.id)
                character = live_character or character
                player = await self._nanny(character, session, connection)
                if player is None:
                    return None
                session.metadata["entered_world"] = live_character is not None
                self.connection_manager.bind_character(character.id, session.session_id)
                if live_character is not None:
                    text = self.LINK_MESSAGES.render("to_char", "reconnect")
                    await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))
                    await self._announce_link(character, "reconnect")
                    area, room = self._get_area_and_room(character)
                    if room is not None and area is not None:
                        await self.message_bus.send_prompt(character, area, room)
                    self.logger.info(f"{character.name}@{connection.get_peer_info()} reconnected.")
                return player, character
        return None

    async def _cleanup_session(self, session):
        character = session.metadata.get("switched_original") or session.character
        if character is None:
            await self._detach_session(session)
        else:
            async with self._character_lock(character.id):
                await self._detach_session(session)

    async def _detach_session(self, session):
        if session.metadata.get("connection_cleaned", False):
            return
        session.metadata["connection_cleaned"] = True
        current = session.character
        character = session.metadata.get("switched_original") or current
        owned = any(candidate is not None and self.connection_manager.owns_character(candidate.id, session.session_id)
                    for candidate in (current, character))
        for candidate in (current, character):
            if candidate is not None:
                self.connection_manager.unbind_character(candidate.id, session_id=session.session_id)
        self.connection_manager.remove_connection(session.session_id)
        self.session_handler.remove_session(session.session_id)
        snooper_id = session.metadata.pop("snoop_by_session_id", None)
        for other in self.session_handler.get_active_sessions():
            if other.metadata.get("snoop_by_session_id") == session.session_id:
                other.metadata.pop("snoop_by_session_id", None)
        if snooper_id:
            snooper = self.connection_manager.get_connection(snooper_id)
            if snooper is not None and not snooper.is_closed():
                await snooper.send_text("Your victim has left the game.\r\n")
        if not owned or character is None:
            return

        if current is not character and getattr(current, "context", None) is not None:
            current.context.pop("controller_original", None)
            current.context.pop("controller_original_id", None)
        account = self.registry_service.player_registry.get_or_none(id=session.player_id)
        if account is not None:
            account.current_characters = [ch for ch in (account.current_characters or []) if ch.id != character.id]
        if self._live_character(character.id) is not None:
            await self._announce_link(character, "lost")
        else:
            self.registry_service.character_registry.remove_playing(character)

    async def _announce_link(self, character, key: str):
        _, room = self._get_area_and_room(character)
        if room is not None:
            positions = CharacterApi.get_enum("positions")
            for viewer in room.players_in_room():
                if viewer.id == character.id or CharacterApi.position_value(viewer) < positions.POS_RESTING.value:
                    continue
                name = character.name if CharacterApi.can_see(viewer, character, room) else "Someone"
                text = self.LINK_MESSAGES.render("to_room", key, name=name, possessive=character.his_her())
                await self.message_bus.send_to_character(viewer.id, self.message_bus.text_to_message(text))
        text = self.LINK_MESSAGES.render("to_wiznet", key, name=character.name, possessive=character.his_her())
        for recipient in self.wiz_handler.wiznet_targets(character, flag_name="WIZ_LINKS"):
            message = self.wiz_handler.decorate_wiznet_text(recipient, text)
            await self.message_bus.send_to_character(recipient.id, self.message_bus.text_to_message(message))

    @staticmethod
    async def _send_welcome(connection: TelnetConnection) -> None:
        welcome = f"Welcome to the server!\n\n\n\n"
        await connection.send_text(welcome, MessageType.GAME)

    @staticmethod
    def _peer_denied(peer_info) -> bool:
        if isinstance(peer_info, tuple) and peer_info:
            return GameApi.is_site_denied(str(peer_info[0] or ""))
        return GameApi.is_site_denied(str(peer_info or ""))

    async def _game_loop(self, connection: TelnetConnection, session, player, character) -> None:
        while not connection.is_closed() and (session.is_playing() or session.is_idle()):
            try:
                character = session.character or character
                if not session.is_idle() and self.session_handler.is_session_idle(session):
                    if CharacterApi.is_immortal(session):
                        session.update_activity()
                    else:
                        session.status = SessionStatus.IDLING

                message = await self._wait_for_message(connection, session)
                if message is None:
                    break
                if connection.is_closed() or not (session.is_playing() or session.is_idle()):
                    break
                session.update_activity()
                if message.type == MessageType.GAME and not await self._wait_for_action_ready(connection, session):
                    break
                character = session.character or character
                area, room = self._get_area_and_room(character)
                if message.type == MessageType.GAME and session.metadata.get("paging_active", False):
                    await self._continue_paging(connection, session)
                    if not session.metadata.get("paging_active", False):
                        character = session.character or character
                        area, room = self._get_area_and_room(character)
                        await self.message_bus.send_prompt(character, area, room)
                    continue

                if message.type == MessageType.GAME:
                    character = session.character or character
                    command_text = message.get('text', '')
                    await self.message_bus.mirror_snoop_input(session, command_text)
                    await self.command_handler.handle_command(player, character, command_text)
                    character = session.character or character
                    area, room = self._get_area_and_room(character)
                    await self.message_bus.send_prompt(character, area, room)
            except Exception as e:
                self.logger.error(f"Error in game loop: {e}", exc_info=True)
                break

    async def _wait_for_action_ready(self, connection, session) -> bool:
        """Keep typed input ordered; nested/forced commands do not enter this gate."""
        while not connection.is_closed() and (session.is_playing() or session.is_idle()):
            character = session.character
            status = getattr(character, "status_flags", None)
            if status is None or status.pulse_wait <= 0:
                return True
            await asyncio.sleep(0.05)
        return False

    async def _wait_for_message(self, connection: TelnetConnection, session: SessionState) -> Message | None:
        while True:
            try:
                return await asyncio.wait_for(connection.receive_message(), timeout=self.session_handler.max_idle_time)
            except asyncio.TimeoutError:
                if CharacterApi.is_immortal(session):
                    session.update_activity()
                    self.logger.debug(f"Immortal session {session.session_id} idle timer reset")
                    continue
                if not session.is_idle():
                    session.status = SessionStatus.IDLING
                    self.logger.info(f"Session {session.session_id} timed out")
                    await connection.send_text("You have disappeared into the void.\n\r", MessageType.GAME)
                return None

    def _update_player(self, session, character) -> Player | None:
        account = self.registry_service.player_registry.get(id=session.player_id)
        if account:
            if account.current_characters is None:
                account.current_characters = []
            if not any(current.id == character.id for current in account.current_characters):
                account.current_characters.append(character)
            account.ansi_enabled = session.ansi_enabled
        return account

    def _get_area_and_room(self, character) -> tuple[Area | None, Room | None]:
        area = self.registry_service.area_registry.get_or_none(id=character.area_id)
        room = self.registry_service.room_registry.get_or_none(id=character.room_id)
        return area, room

    async def _nanny(self, character, session, connection) -> Optional[Player]:
        player = self.registry_service.player_registry.get_or_none(id=session.player_id)

        if player is not None and player.banned:
            await connection.send_text("You have been banned from the server.\r\n", MessageType.ERROR)
            await connection.close()
            return None
        elif player is None:
            await connection.send_text("Player not registered. Please try again.\r\n", MessageType.ERROR)
            return None
        session.character = character
        self._update_player(session, character)
        self.registry_service.character_registry.set_playing(character)
        self.logger.info(f"Player {player.first_name} {player.last_name} is now playing {character.name}.")
        session.status = SessionStatus.PLAYING
        return player

    @staticmethod
    async def _continue_paging(connection: TelnetConnection, session: SessionState) -> None:
        queue = session.metadata.get("paging_queue", []) or []
        if not queue:
            session.metadata["paging_active"] = False
            session.metadata["paging_queue"] = []
            return

        page = queue.pop(0)
        suffix = "\r\n[Hit Enter to continue]\r\n" if queue else ""
        await connection.send_text(page + suffix, MessageType.GAME)

        if not queue:
            session.metadata["paging_active"] = False
            session.metadata["paging_queue"] = []
