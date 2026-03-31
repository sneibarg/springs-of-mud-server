from typing import List

from injector import inject
from player.Character import Character
from registry.CharacterRegistry import CharacterRegistry
from server.messaging import MessageBus
from server.protocol import Message, MessageType


class PlayerHandler:
    @inject
    def __init__(self, message_bus: MessageBus, character_registry: CharacterRegistry):
        self.__name__ = "PlayerHandler"
        self.message_bus = message_bus
        self.character_registry = character_registry

    async def print_visible(self, player_id, character, visible):
        who_list = [character] + visible
        who_line = ""
        players_found = "Players found: " + str(len(who_list)) + "\r\n"
        for character in who_list:
            who_line = who_line + f"[{character.level}    {character.race}    {character.character_class.name}] {character.name} {character.title}\r\n"

        who_line = who_line + players_found
        await self.message_bus.send_to_character(player_id, Message(type=MessageType.GAME, data={"text": who_line}))

    def to_player(self, player_id, message):
        message += "\r\n"
        self.message_bus.send_to_character(player_id, Message(type=MessageType.GAME, data={"text": message}))

    def to_room(self, player_service, message, pattern):
        player_service.to_room(self, message, pattern)

    def visible(self, player) -> List[Character]:
        visible = []
        current_character = player.current_character
        role = current_character.role
        for character in self.character_registry.registry.values():
            registered_character: Character = character.get("current_character")
            if current_character is not None or character.name == registered_character.name:
                continue
            if character.cloaked and role == "player":
                continue
            else:
                visible.append(registered_character)
        return visible
