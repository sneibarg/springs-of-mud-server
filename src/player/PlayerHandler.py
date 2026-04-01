from typing import List

from injector import inject
from player.Character import Character
from registry.CharacterRegistry import CharacterRegistry
from server.messaging import MessageBus
from server.protocol import Message, MessageType
from server.session.SessionHandler import SessionHandler


class PlayerHandler:
    @inject
    def __init__(self, message_bus: MessageBus, character_registry: CharacterRegistry, session_handler: SessionHandler):
        self.__name__ = "PlayerHandler"
        self.message_bus = message_bus
        self.character_registry = character_registry
        self.session_handler = session_handler

    async def print_visible(self, character):
        who_list = [character] + self._visible(character)
        who_line = ""
        players_found = "Players found: " + str(len(who_list)) + "\r\n"
        for c in who_list:
            who_line = who_line + f"[{c.level}    {c.race}    {c.character_class.name}] {c.name} {c.title}\r\n"

        who_line = who_line + players_found
        message = self.message_bus.text_to_message(who_line)
        await self.message_bus.send_to_character(character.id, message)

    async def to_player(self, character_id, text):
        text += "\r\n"
        message = self.message_bus.text_to_message(text)
        await self.message_bus.send_to_character(character_id, message)

    def _visible(self, character) -> List[Character]:
        visible = []
        for session in self.session_handler.get_playing_sessions():
            char = session.character
            if char.id == character.id:
                continue
            if char.cloaked and character.role == "player":
                continue
            visible.append(char)
        return visible
