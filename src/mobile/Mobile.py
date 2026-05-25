from dataclasses import dataclass, field
from typing import Optional

from game.AnimateEntity import AnimateEntity
from mobile.Dice import Dice
from mobile.MobileFlags import MobileFlags
from util.GenericUtil import GenericUtil


@dataclass
class Mobile(AnimateEntity):
    vnum: str
    short_description: str
    long_description: str
    description: str
    race: str
    flags: str
    alignment: str
    group: str
    dam_type: str
    size: str
    material: str
    hit_roll: int
    count: int = 0
    killed: int = 0
    start_pos: int = 0
    default_pos: int = 0
    hit_dice: Optional[Dice] = None
    mana_dice: Optional[Dice] = None
    damage_dice: Optional[Dice] = None
    extra_flags: Optional[MobileFlags] = None
    special_name: Optional[str] = None
    special_function: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.instance_id = GenericUtil.generate_mongo_id()
        self.__name__ = "Mobile-" + str(self.instance_id)
        super().__post_init__()

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Mobile):
            return self.id == other.id
        return False

    @classmethod
    def from_json(cls, data):
        data.setdefault('room_id', "")
        data.setdefault('lock', None)
        return cls(**data)
