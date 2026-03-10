import threading

from dataclasses import dataclass, field
from uuid import uuid1
from server.LoggerFactory import LoggerFactory


@dataclass
class Mobile:
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
    off_flags: str
    imm_flags: str
    res_flags: str
    vuln_flags: str
    start_pos: str
    default_pos: str
    sex: str
    form: str
    parts: str
    size: str
    material: str
    flags: str
    id: str
    level: int
    hit_roll: int
    hit_dice_number: int
    hit_dice_type: int
    hit_dice_bonus: int
    mana_dice_number: int
    mana_dice_type: int
    mana_dice_bonus: int
    damage_dice_number: int
    damage_dice_type: int
    damage_dice_bonus: int
    ac_pierce: int
    ac_bash: int
    ac_slash: int
    ac_exotic: int
    gold: int
    lock: threading.Lock = field(default_factory=threading.Lock)

    def __post_init__(self):
        self.instance_id = uuid1()
        if self.lock is None:
            self.lock = threading.Lock()
        self.__name__ = "Mobile-" + str(self.instance_id)
        self.logger = LoggerFactory.get_logger(self.__name__)

    @classmethod
    def from_json(cls, data):
        data.setdefault('lock', None)
        return cls(**data)
