from dataclasses import dataclass
from enum import IntEnum

from injector import inject
from game.GameData import Constants


@dataclass
class CharacterConstants:
    immortal_levels: dict[str, int]

    @inject
    def __init__(self, constants: Constants, positions: type[IntEnum], attribute_bonuses: dict):
        self.constants = constants
        self.positions = positions
        self.attribute_bonuses = attribute_bonuses
        self._populate_immortal_levels()

    def _populate_immortal_levels(self):
        self.immortal_levels = dict()
        self.immortal_levels['IMPLEMENTOR'] = self.constants.max['level']
        self.immortal_levels['CREATOR'] = self.constants.max['level'] - 1
        self.immortal_levels['SUPREME'] = self.constants.max['level'] - 2
        self.immortal_levels['DEITY'] = self.constants.max['level'] - 3
        self.immortal_levels['GOD'] = self.constants.max['level'] - 4
        self.immortal_levels['IMMORTAL'] = self.constants.max['level'] - 5
        self.immortal_levels['DEMI'] = self.constants.max['level'] - 6
        self.immortal_levels['ANGEL'] = self.constants.max['level'] - 7
        self.immortal_levels['AVATAR'] = self.constants.max['level'] - 8
        self.immortal_levels['HERO'] = self.constants.max['level'] - 9
