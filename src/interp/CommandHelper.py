from injector import inject

from server.LoggerFactory import LoggerFactory
from server.messaging.MessageBus import MessageBus
from player.Character import Character
from player.CharacterMacros import CharacterMacros


class CommandHelper:
    @inject
    def __init__(self, message_bus: MessageBus, character_macros: CharacterMacros):
        self.__name__ = "CommandHelper"
        self.logger = LoggerFactory.get_logger(__name__)
        self.message_bus = message_bus
        self.character_macros = character_macros
        self.PositionsEnum = character_macros.PositionsEnum

    async def check_position(self, character: Character) -> bool:
        if character.character_attributes.position < self.PositionsEnum.POS_SLEEPING.value:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("You can't see anything but stars!\n\r"))
            return False

        if character.character_attributes.position == self.PositionsEnum.POS_SLEEPING.value:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("You can't see anything; you're sleeping!\n\r"))
            return False
        return True
