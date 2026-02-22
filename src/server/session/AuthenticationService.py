from typing import Optional, Tuple
from server.connection import Connection
from server.protocol import MessageType
from .SessionState import SessionState, SessionPhase


class AuthenticationService:
    def __init__(self, player_service, injector):
        self.player_service = player_service
        self.injector = injector

    def _get_account(self, account_name: str) -> Optional[dict]:
        try:
            from server.server_util import camel_to_snake_case
            account = self.player_service.get_account_by_name(account_name)
            if account:
                return camel_to_snake_case(account)
        except Exception:
            pass
        return None

    @staticmethod
    def _find_character(character_list: list, character_name: str) -> Optional[dict]:
        for character in character_list:
            if character_name.upper() in character['name'].upper():
                return character
        return None

    async def authenticate_with_payload(self, connection: Connection, session: SessionState, payload: dict) -> Tuple[bool, Optional[str], Optional[dict]]:
        session.phase = SessionPhase.AUTHENTICATING
        account_id = payload.get('accountId')
        character_id = payload.get('characterId')
        character_name = payload.get('characterName')

        if not account_id or not character_id:
            await connection.send_text("Invalid authentication payload.\r\n", MessageType.AUTH_FAILURE)
            return False, None, None

        account = self._get_account_by_id(account_id)
        if not account:
            await connection.send_text("Account validation failed.\r\n", MessageType.AUTH_FAILURE)
            return False, None, None

        character_list = self.player_service.get_player_characters(account_id)
        character_data = None
        for char in character_list:
            if char.get('id') == character_id:
                character_data = char
                break

        if not character_data:
            await connection.send_text("Character validation failed.\r\n", MessageType.AUTH_FAILURE)
            return False, None, None

        session.player_id = account_id
        session.character_id = character_id
        session.account_name = account.get('account_name', 'Unknown')

        await connection.send_text(f"Authentication successful. Logging in as {character_name}...\r\n", MessageType.AUTH_SUCCESS)

        return True, account_id, character_data

    def _get_account_by_id(self, account_id: str) -> Optional[dict]:
        try:
            from server.server_util import camel_to_snake_case
            account = self.player_service.get_account_by_id(account_id)
            if account:
                return camel_to_snake_case(account)
        except Exception:
            pass
        return None
