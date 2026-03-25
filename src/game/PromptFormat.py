from dataclasses import dataclass

from player import Character
from server.protocol import Message, MessageType


@dataclass
class PromptFormat:
    hp: bool
    max_hp: bool
    mana: bool
    max_mana: bool
    movement: bool
    max_movement: bool
    xp: bool
    max_xp: bool
    gold: bool
    silver: bool

    @staticmethod
    def default_prompt(character: Character) -> Message:
        text = f"<{character.health}hp {character.mana}m {character.movement}mv>\r\n"
        return Message(type=MessageType.GAME, data={'text': text})
