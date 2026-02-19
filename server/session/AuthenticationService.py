from typing import Optional, Tuple
from server.connection import Connection
from server.protocol import Message, MessageType
from .SessionState import SessionState, SessionPhase


class AuthenticationService:
    """
    Handles player authentication and character selection.
    Extracted from player_util.py for better separation of concerns.
    """

    def __init__(self, player_service, injector):
        self.player_service = player_service
        self.injector = injector

    async def authenticate(self, connection: Connection, session: SessionState) -> Tuple[bool, Optional[str]]:
        """
        Authenticate a player account.
        Returns (success, player_id)
        """
        session.phase = SessionPhase.AUTHENTICATING

        # Send welcome message
        await connection.send_text("You are not logged in.\r\n\nWhat is your account name? ", MessageType.SYSTEM)

        # Get account name
        msg = await connection.receive_message()
        if not msg or msg.get('text') == '':
            return False, None

        account_name = msg.get('text', '').strip()
        account = self._get_account(account_name)

        if not account:
            await connection.send_text("That account does not exist.\r\n", MessageType.ERROR)
            session.auth_attempts += 1
            return False, None

        # Get password
        await connection.send_text("What is your password?\r\n", MessageType.SYSTEM)
        msg = await connection.receive_message()
        if not msg:
            return False, None

        password = msg.get('text', '').strip()

        if password == account.get('password'):
            await connection.send_text("You have authenticated successfully.\r\n", MessageType.AUTH_SUCCESS)
            session.player_id = account['id']
            session.account_name = account_name
            return True, account['id']
        else:
            await connection.send_text("The password you supplied does not match our records.\r\n", MessageType.AUTH_FAILURE)
            session.auth_attempts += 1
            return False, None

    async def select_character(self, connection: Connection, session: SessionState) -> Optional[dict]:
        """
        Handle character selection for authenticated player.
        Returns character data or None.
        """
        if not session.is_authenticated():
            return None

        session.phase = SessionPhase.SELECTING_CHARACTER

        # Get character list
        character_list = self.player_service.get_player_characters(session.player_id)

        if not character_list:
            await connection.send_text(
                "You don't have any characters! Would you like to create one? yes or no\r\n",
                MessageType.SYSTEM
            )
            msg = await connection.receive_message()
            if msg and msg.get('text', '').lower() == 'no':
                await connection.send_text("Maybe next time...\r\n", MessageType.SYSTEM)
            return None

        # Show character list
        await connection.send_text("Select one of the following characters:\r\n\n", MessageType.CHAR_LIST)
        for character in character_list:
            line = f"- {character['name']}\r\n"
            await connection.send_text(line, MessageType.SYSTEM)

        await connection.send_text("\r\n", MessageType.SYSTEM)

        # Get selection
        msg = await connection.receive_message()
        if not msg:
            return None

        character_name = msg.get('text', '').strip()
        character = self._find_character(character_list, character_name)

        if character:
            session.character_id = character.get('id')
            await connection.send_text(f"Logging you onto the server as {character_name}\r\n", MessageType.CHAR_SELECTED)
            return character
        else:
            await connection.send_text("That is not one of your characters.\r\n", MessageType.ERROR)
            return None

    def _get_account(self, account_name: str) -> Optional[dict]:
        """Get account by name"""
        try:
            from utilities.server_util import camel_to_snake_case
            account = self.player_service.get_account_by_name(account_name)
            if account:
                return camel_to_snake_case(account)
        except Exception:
            pass
        return None

    def _find_character(self, character_list: list, character_name: str) -> Optional[dict]:
        """Find character in list by name"""
        for character in character_list:
            if character_name.upper() in character['name'].upper():
                return character
        return None

    async def authenticate_with_payload(self, connection: Connection, session: SessionState,
                                       payload: dict) -> Tuple[bool, Optional[str], Optional[dict]]:
        """
        Authenticate using a payload from the UI client.
        The UI has already authenticated via REST API and sends the full account + character data.
        Server validates the account_id and character_id exist.

        Returns (success, player_id, character_data)
        """
        session.phase = SessionPhase.AUTHENTICATING

        # Extract data from payload
        account_id = payload.get('accountId')
        character_id = payload.get('characterId')
        character_name = payload.get('characterName')

        if not account_id or not character_id:
            await connection.send_text("Invalid authentication payload.\r\n", MessageType.AUTH_FAILURE)
            return False, None, None

        # Validate account exists
        account = self._get_account_by_id(account_id)
        if not account:
            await connection.send_text("Account validation failed.\r\n", MessageType.AUTH_FAILURE)
            return False, None, None

        # Validate character exists and belongs to account
        character_list = self.player_service.get_player_characters(account_id)
        character_data = None

        for char in character_list:
            if char.get('id') == character_id:
                character_data = char
                break

        if not character_data:
            await connection.send_text("Character validation failed.\r\n", MessageType.AUTH_FAILURE)
            return False, None, None

        # Validation successful
        session.player_id = account_id
        session.character_id = character_id
        session.account_name = account.get('account_name', 'Unknown')

        await connection.send_text(
            f"Authentication successful. Logging in as {character_name}...\r\n",
            MessageType.AUTH_SUCCESS
        )

        return True, account_id, character_data

    def _get_account_by_id(self, account_id: str) -> Optional[dict]:
        """Get account by ID"""
        try:
            from utilities.server_util import camel_to_snake_case
            account = self.player_service.get_account_by_id(account_id)
            if account:
                return camel_to_snake_case(account)
        except Exception:
            pass
        return None
