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

    def credit_expired_stock(self, item) -> int:
        """Recover ROM's silver value when a shopkeeper's carried stock expires."""
        credit = GenericUtil.to_int(getattr(item, "cost", 0), 0) // 5
        self.silver = GenericUtil.to_int(getattr(self, "silver", 0), 0) + credit
        return credit

    def __eq__(self, other):
        if isinstance(other, Mobile):
            return self.id == other.id
        return False

    @classmethod
    def from_json(cls, data):
        data.setdefault('room_id', "")
        data.setdefault('lock', None)
        return cls(**data)

    def _base_hit_gain(self, level, position, context):
        gain = 5 + level
        if self.is_affected(context.affected_bits, "AFF_REGENERATION"):
            gain *= 2
        if position == context.position("POS_SLEEPING"):
            gain = 3 * gain // 2
        elif position == context.position("POS_RESTING"):
            pass
        elif position == context.position("POS_FIGHTING"):
            gain //= 3
        else:
            gain //= 2

        return gain

    def _base_mana_gain(self, level, position, context):
        gain = 5 + level
        if position == context.position("POS_SLEEPING"):
            gain = 3 * gain // 2
        elif position == context.position("POS_RESTING"):
            pass
        elif position == context.position("POS_FIGHTING"):
            gain //= 3
        else:
            gain //= 2

        return gain

    def _base_move_gain(self, level, position, context):
        gain = level

        return gain
