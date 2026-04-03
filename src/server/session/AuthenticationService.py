from typing import Optional, Tuple
from injector import inject

from player.CharacterRegistry import CharacterRegistry
from player.Player import Player
from player.Character import Character
from player.PlayerRegistry import PlayerRegistry
from server.connection.Connection import Connection
from server.protocol.Message import Message, MessageType
from server.session.SessionState import SessionState, SessionStatus
from server.LoggerFactory import LoggerFactory


class AuthenticationService:
    @inject
    def __init__(self, player_registry: PlayerRegistry, character_registry: CharacterRegistry):
        self.__name__ = "AuthenticationService"
        self.player_registry = player_registry
        self.character_registry = character_registry
        self.logger = LoggerFactory.get_logger(self.__name__)

    def _get_account(self, account_name: str) -> Player | None:
        try:
            account = self.player_registry.get_player_by_name(account_name)
            if account:
                return account
        except Exception as e:
            self.logger.error(f"Failed to get account: {e}")
        return None

    @staticmethod
    def _find_character(character_list: list, character_name: str) -> Optional[Character]:
        for character in character_list:
            if character_name.upper() in character['name'].upper():
                return character
        return None

    async def authenticate_with_payload(self, connection: Connection, session: SessionState, payload: dict) -> Tuple[bool, Optional[str], Optional[Character]]:
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

        character_list = self.player_registry.get_player_characters(account_id)
        character = self._get_character_by_id(character_id, character_list)
        if not character:
            await connection.send_message(Message(MessageType.ERROR, data={"text": "Invalid authentication payload for registered character.\r\n"}))
            return False, None, None

        session.player_id = account_id
        session.account_name = account.account_name

        await connection.send_message(Message(MessageType.AUTH, data={"text": f"Authentication successful. Logging in as {character_name}...\r\n"}))
        return True, account_id, character

    def _get_character_by_id(self, character_id: str, character_list: list) -> Optional[Character]:
        for char in character_list:
            if char == character_id:
                return self.character_registry.registry[char]['playing']
        return None

    def _get_account_by_id(self, account_id: str) -> Optional[Player]:
        try:
            account = self.player_registry.registry[account_id]
            if account:
                return account
        except Exception as e:
            self.logger.error(f"Failed to get account by ID {account_id}: {e}")
        return None
