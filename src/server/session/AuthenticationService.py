from typing import Optional, Tuple
from injector import inject

from registry import RegistryService
from server.connection.Connection import Connection
from server.protocol.Message import Message, MessageType
from server.session.SessionState import SessionState, SessionStatus
from server.LoggerFactory import LoggerFactory


class AuthenticationService:
    @inject
    def __init__(self, registry_service: RegistryService):
        self.__name__ = "AuthenticationService"
        self.registry_service = registry_service
        self.logger = LoggerFactory.get_logger(self.__name__)

    def _get_account(self, account_name: str) -> Optional[dict]:
        try:
            account = self.registry_service.get_player_by_name(account_name)
            if account:
                from server.ServerUtil import ServerUtil
                return ServerUtil.camel_to_snake_case(account)
        except Exception as e:
            self.logger.error(f"Failed to get account: {e}")
        return None

    @staticmethod
    def _find_character(character_list: list, character_name: str) -> Optional[dict]:
        for character in character_list:
            if character_name.upper() in character['name'].upper():
                return character
        return None

    async def authenticate_with_payload(self, connection: Connection, session: SessionState, payload: dict) -> Tuple[bool, Optional[str], Optional[dict]]:
        session.status = SessionStatus.AUTHENTICATING
        account_id = payload.get('accountId')
        character_id = payload.get('characterId')
        character_name = payload.get('characterName')
        if not account_id or not character_id:
            await connection.send_message(Message(MessageType.ERROR, data={"text": "Invalid authentication payload.\r\n"}))
            return False, None, None

        account = self._get_account_by_id(account_id)
        if not account:
            await connection.send_message(Message(MessageType.ERROR, data={"text": "Invalid authentication payload for registered account.\r\n"}))
            return False, None, None

        character_list = self.registry_service.get_player_characters(account_id)
        character = self._get_character_by_id(character_id, character_list)
        if not character:
            await connection.send_message(Message(MessageType.ERROR, data={"text": "Invalid authentication payload for registered character.\r\n"}))
            return False, None, None

        session.player_id = account_id
        session.account_name = account.get('account_name', 'Unknown')

        await connection.send_message(Message(MessageType.AUTH, data={"text": f"Authentication successful. Logging in as {character_name}...\r\n"}))
        return True, account_id, character

    def _get_character_by_id(self, character_id: str, character_list: list) -> Optional[dict]:
        for char in character_list:
            if char == character_id:
                return self.registry_service.character_list[char]
        return None

    def _get_account_by_id(self, account_id: str) -> Optional[dict]:
        try:
            account = self.registry_service.player_list[account_id]
            if account:
                from server.ServerUtil import ServerUtil
                return ServerUtil.camel_to_snake_case(account)
        except Exception as e:
            self.logger.error(f"Failed to get account by ID {account_id}: {e}")
        return None
