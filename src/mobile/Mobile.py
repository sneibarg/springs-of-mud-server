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

    def ensure_effects(self):
        with self.lock:
            if self.effects is None:
                self.effects = []
            return self.effects

    def apply_effect(self, effect):
        from util.EffectUtil import EffectUtil

        with self.lock:
            self.ensure_effects().append(effect)
            EffectUtil.affect_modify(self, effect, True)
        return effect

    def remove_effect(self, effect) -> bool:
        from util.EffectUtil import EffectUtil

        with self.lock:
            effects = self.ensure_effects()
            if effect not in effects:
                return False
            where = getattr(effect, "where", 0)
            vector = getattr(effect, "bitvector", 0)
            EffectUtil.affect_modify(self, effect, False)
            effects.remove(effect)
            EffectUtil.affect_check(self, where, vector)
        return True

    def join_effect(self, effect):
        from util.EffectUtil import EffectUtil

        new_effect = EffectUtil.as_effect(effect)
        matched = None
        for old in list(self.ensure_effects()):
            if str(getattr(old, "type", "")).strip().lower() == str(getattr(new_effect, "type", "")).strip().lower():
                matched = old
                break
        if matched is not None:
            new_effect.level = (GenericUtil.to_int(new_effect.level, 0) + GenericUtil.to_int(matched.level, 0)) // 2
            new_effect.duration = GenericUtil.to_int(new_effect.duration, 0) + GenericUtil.to_int(matched.duration, 0)
            new_effect.modifier = GenericUtil.to_int(new_effect.modifier, 0) + GenericUtil.to_int(matched.modifier, 0)
            self.remove_effect(matched)
        return self.apply_effect(new_effect)

    @classmethod
    def from_json(cls, data):
        data.setdefault('lock', None)
        return cls(**data)
