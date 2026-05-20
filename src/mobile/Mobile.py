import threading

from dataclasses import dataclass, field
from typing import Optional, Any
from game.Equipped import Equipped
from mobile.ArmorClass import ArmorClass
from mobile.Dice import Dice
from game.StatusFlags import StatusFlags
from mobile.MobileFlags import MobileFlags
from player.CharacterAttributes import CharacterAttributes
from server.LoggerFactory import LoggerFactory
from util.GenericUtil import GenericUtil


@dataclass
class Mobile:
    id: str
    area_id: str
    vnum: str
    name: str
    short_description: str
    long_description: str
    description: str
    race: str
    flags: str
    alignment: str
    group: str
    dam_type: str
    sex: str
    size: str
    material: str
    level: int
    hit_roll: int
    gold: int
    silver: int
    count: int = 0
    killed: int = 0
    start_pos: int = 0
    default_pos: int = 0
    fighting: Optional[Any] = None
    character_attributes: Optional[CharacterAttributes] = None
    armor_class: Optional[ArmorClass] = None
    hit_dice: Optional[Dice] = None
    mana_dice: Optional[Dice] = None
    damage_dice: Optional[Dice] = None
    status_flags: Optional[StatusFlags] = None
    extra_flags: Optional[MobileFlags] = None
    equipped: Optional[Equipped] = None
    leader: Optional[Any] = None
    inventory: list = field(default_factory=list)
    effects: list = field(default_factory=list)
    special_name: Optional[str] = None
    special_function: list[str] = field(default_factory=list)
    lock: threading.RLock = field(default_factory=threading.RLock)

    def __post_init__(self):
        from util.GenericUtil import GenericUtil
        self.instance_id = GenericUtil.generate_mongo_id()
        if self.lock is None:
            self.lock = threading.RLock()
        self.__name__ = "Mobile-" + str(self.instance_id)
        self.logger = LoggerFactory.get_logger(self.__name__)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Mobile):
            return self.id == other.id
        return False

    @classmethod
    def from_json(cls, data):
        data.setdefault('lock', None)
        return cls(**data)
