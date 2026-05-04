from __future__ import annotations

import json
import threading

from dataclasses import dataclass, field
from typing import Optional, List, TYPE_CHECKING

from item.ExtraDescriptionData import ExtraDescriptionData
from item.Effect import Effect
from player.Character import Character
from player.CharacterMacros import CharacterMacros
from server.LoggerFactory import LoggerFactory
from util.GenericUtil import GenericUtil

if TYPE_CHECKING:
    from area.Room import Room


@dataclass
class Item:
    id: str
    area_id: str
    vnum: str
    name: str
    short_description: str
    long_description: str
    material: str
    item_type: str
    extra_flags: str
    wear_flags: str
    value0: str
    value1: str
    value2: str
    value3: str
    value4: str
    condition: str
    level: int
    weight: int
    cost: int
    affect_data: list
    extra_descr: list
    contains: list
    count: int = 0
    room_data: dict[str, Room] = field(default_factory=dict)
    enchanted: Optional[bool] = False
    timer: Optional[int] = None
    damage_type: Optional[str] = None
    weapon_type: Optional[str] = None
    liquid_color: Optional[str] = None
    liquid_affect_data: Optional[list] = None
    effects: Optional[List[Effect]] = None
    extra_description: Optional[ExtraDescriptionData] = None

    def __post_init__(self):
        self.__name__ = "Item"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.lock = threading.RLock()

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.id == other.id
        return False

    def contents(self) -> str:
        text = ""
        if len(self.contains) > 0:
            for item in self.contains:
                text = text + "\t" + item.name + "\r\n"
        return text

    def short(self) -> str:
        return self.short_description or self.name or "it"

    def add_contained_item(self, item) -> None:
        with self.lock:
            if self.contains is None:
                self.contains = []
            self.contains.append(item)

    def remove_contained_item(self, item) -> bool:
        with self.lock:
            contents = self.contains or []
            try:
                contents.remove(item)
                return True
            except ValueError:
                return False

    def find_contained_item(self, wanted: str):
        q = (wanted or "").strip().lower()
        if not q:
            return None
        for obj in list(self.contains or []):
            name = (getattr(obj, "name", "") or "").lower()
            if name == q or name.startswith(q):
                return obj
        return None

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
            EffectUtil.affect_modify(self, effect, False)
            effects.remove(effect)
        return True

    def add_item_to_room(self, room: Room):
        with self.lock:
            if room.id not in self.room_data:
                self.room_data[room.id] = room

    def remove_item_from_room(self, room: Room):
        with self.lock:
            if room.id in self.room_data:
                del self.room_data[room.id]

    @classmethod
    def from_json(cls, data):
        if isinstance(data, str):
            data = json.loads(data)
        from util.GenericUtil import GenericUtil
        data = GenericUtil.camel_to_snake_case(data)
        data['contains'] = []
        data['extra_description'] = cls._normalize_extra_description(
            data.get('extra_description'),
            data.get('extra_descr'),
        )
        return cls(**data)

    @staticmethod
    def _normalize_extra_description(extra_description, extra_descr):
        if extra_description:
            try:
                return ExtraDescriptionData.from_json(extra_description)
            except (TypeError, ValueError):
                return None

        if isinstance(extra_descr, list) and len(extra_descr) >= 2:
            keyword = str(extra_descr[0] or "").strip()
            description = str(extra_descr[1] or "")
            if keyword or description:
                return ExtraDescriptionData(valid=True, keyword=keyword, description=description)

        return None

    def weapon_too_heavy(self, character: Character) -> bool:
        if CharacterMacros.is_npc(character):
            return False
        strength = max(0, GenericUtil.to_int(getattr(getattr(character, "character_attributes", None), "strength", 0), 0))
        try:
            strength_bonus = CharacterMacros.get_attribute_bonus("strength", str(character.level))
        except RuntimeError:
            strength_bonus = {}
        wield_limit = GenericUtil.to_int(strength_bonus.get(str(strength), {}).get("wield", 0), 0) * 10
        return 0 < wield_limit < GenericUtil.to_int(getattr(self, "weight", 0), 0)

    def is_two_handed_weapon(self) -> bool:
        from util.ItemUtil import ItemUtil

        try:
            weapon_flags = CharacterMacros.get_enum("weaponType")
        except RuntimeError:
            return False
        if not hasattr(weapon_flags, "WEAPON_TWO_HANDS"):
            return False
        return ItemUtil.has_flag(getattr(self, "value4", 0), weapon_flags.WEAPON_TWO_HANDS.value)
