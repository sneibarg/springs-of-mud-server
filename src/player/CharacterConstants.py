from dataclasses import dataclass
from injector import inject
from game.GameData import GameData


@dataclass
class CharacterConstants:
    immortal_levels: dict[str, int]

    @inject
    def __init__(self, game_data: GameData):
        self.game_data = game_data
        self._populate_immortal_levels()

    def get_max_level(self):
        return int(self.game_data.constants.max['level'])

    def get_attribute_bonus(self, attr_name: str, attr_level: str):
        return self.game_data.attribute_bonuses.get(attr_name).get(attr_level)

    def is_immortal_sufficient(self, level: int, immortal_name: str) -> bool:
        return level >= self.immortal_levels.get(immortal_name)

    def _populate_immortal_levels(self):
        self.immortal_levels = dict()
        self.immortal_levels['IMPLEMENTOR'] = self.get_max_level()
        self.immortal_levels['CREATOR'] = self.get_max_level() - 1
        self.immortal_levels['SUPREME'] = self.get_max_level() - 2
        self.immortal_levels['DEITY'] = self.get_max_level() - 3
        self.immortal_levels['GOD'] = self.get_max_level() - 4
        self.immortal_levels['IMMORTAL'] = self.get_max_level() - 5
        self.immortal_levels['DEMI'] = self.get_max_level() - 6
        self.immortal_levels['ANGEL'] = self.get_max_level() - 7
        self.immortal_levels['AVATAR'] = self.get_max_level() - 8
        self.immortal_levels['HERO'] = self.get_max_level() - 9
