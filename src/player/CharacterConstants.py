from dataclasses import dataclass
from injector import inject
from game.GameData import GameData


@dataclass
class CharacterConstants:
    immortal_levels: dict[str, int]
    str_bonuses: dict[str, int]
    int_bonuses: dict[str, int]
    wis_bonuses: dict[str, int]
    con_bonuses: dict[str, int]

    @inject
    def __init__(self, game_data: GameData):
        self.game_data = game_data
        self._populate_immortal_levels()

    def get_max_level(self):
        return int(self.game_data.constants.max['level'])

    def _populate_str_bonuses(self):
        self.str_bonuses = dict()
        self.str_bonuses['tohit'] = 0
        self.str_bonuses['todam'] = 0
        self.str_bonuses['carry'] = 0
        self.str_bonuses['wield'] = 0

    def _populate_int_bonuses(self):
        self.int_bonuses = dict()
        self.int_bonuses['learn'] = 0

    def _populate_wis_bonuses(self):
        self.wis_bonuses = dict()
        self.wis_bonuses['practice'] = 0

    def _populate_con_bonuses(self):
        self.con_bonuses = dict()
        self.con_bonuses['hitp'] = 0
        self.con_bonuses['shock'] = 0

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