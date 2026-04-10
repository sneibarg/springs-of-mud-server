import threading

from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid1
from game import GameData
from mobile.ArmorClass import ArmorClass
from mobile.Dice import Dice
from mobile.MobileFlags import MobileFlags
from player.CharacterAttributes import CharacterAttributes
from server.LoggerFactory import LoggerFactory


@dataclass
class Mobile:
    # === Fields without defaults (required) ===
    area_id: str
    vnum: str
    name: str
    short_description: str
    long_description: str
    description: str
    race: str
    act_flags: str
    affect_flags: str
    alignment: str
    group: str
    dam_type: str
    start_pos: str
    default_pos: str
    sex: str
    form: int
    parts: int
    size: str
    material: str
    flags: str
    id: str
    act: str
    level: int
    hit_roll: int
    pulse_wait: int
    pulse_daze: int
    gold: int
    silver: int
    combat_flags: str
    perm_stat: Optional[CharacterAttributes] = None
    armor_class: Optional[ArmorClass] = None
    hit_dice: Optional[Dice] = None
    mana_dice: Optional[Dice] = None
    damage_dice: Optional[Dice] = None
    mobile_flags: Optional[MobileFlags] = None
    lock: threading.Lock = field(default_factory=threading.Lock)

    def __post_init__(self):
        self.instance_id = uuid1()
        if self.lock is None:
            self.lock = threading.Lock()
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
        data['combat_flags'] = str(data.get('combat_flags', '') or '')
        if 'mobile_flags' not in data:
            data['mobile_flags'] = MobileFlags.default()
        return cls(**data)
