from game import GameData
from object import Item


class ObjectMacros:
    def __init__(self, game_data: GameData):
        self.game_data = game_data

    def can_wear(self, obj: Item, part: int) -> bool:
        pass

    def is_obj_stat(self, obj: Item, stat: int) -> bool:
        pass

    def is_weapon_stat(self, obj: Item, stat: int) -> bool:
        pass

    def weight_multiplier(self, obj: Item) -> int:
        pass