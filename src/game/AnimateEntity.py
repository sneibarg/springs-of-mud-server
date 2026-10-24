from __future__ import annotations

import threading

from dataclasses import dataclass, field
from typing import Any, Optional, TYPE_CHECKING

from game.Equipped import Equipped
from player.CharacterAttributes import CharacterAttributes
from server.LoggerFactory import LoggerFactory
from util.GenericUtil import GenericUtil

if TYPE_CHECKING:
    from item.Item import Item


@dataclass(frozen=True)
class RegenerationContext:
    """Runtime enum and random inputs shared by character and mobile regeneration."""

    positions: Any
    affected_bits: Any
    rng: Any

    def position(self, name: str) -> int:
        member = getattr(self.positions, name, None)
        return int(member.value) if member is not None else -1


@dataclass
class AnimateEntity:
    id: str
    area_id: str
    room_id: str
    name: str
    sex: str
    level: int
    gold: int
    silver: int
    fighting: Optional[Any] = field(default=None, kw_only=True)
    master: Optional[Any] = field(default=None, kw_only=True)
    leader: Optional[Any] = field(default=None, kw_only=True)
    equipped: Optional[Equipped] = field(default=None, kw_only=True)
    inventory: list[Any] = field(default_factory=list, kw_only=True)
    effects: list[Any] = field(default_factory=list, kw_only=True)
    status_flags: Optional[Any] = field(default=None, kw_only=True)
    character_attributes: Optional[CharacterAttributes] = field(default=None, kw_only=True)
    armor_class: Optional[Any] = field(default=None, kw_only=True)
    lock: threading.RLock = field(default_factory=threading.RLock, kw_only=True)

    def __post_init__(self):
        logger_name = self.__dict__["__name__"] if "__name__" in self.__dict__ else self.__class__.__name__
        self.logger = LoggerFactory.get_logger(logger_name)
        if self.lock is None:
            self.lock = threading.RLock()

    def get_alignment(self) -> int:
        return GenericUtil.to_int(self.character_attributes.alignment, 0)

    def set_alignment(self, value: int) -> None:
        attrs = self.character_attributes
        if attrs is not None:
            attrs.alignment = int(value)
            return
        setattr(self, "alignment", int(value))

    def his_her(self) -> str:
        sex = str(self.sex or "").strip().lower()
        if sex in {"male", "m", "1"}:
            return "his"
        if sex in {"female", "f", "2"}:
            return "her"
        return "its"

    def him_her(self) -> str:
        return {"his": "him", "her": "her"}.get(self.his_her(), "it")

    def display_name(self) -> str:
        return str(getattr(self, "name", "") or getattr(self, "short_description", "") or "Someone")

    def condition_value(self, condition_name: str) -> int:
        status_flags = getattr(self, "status_flags", None)
        return GenericUtil.to_int(getattr(status_flags, condition_name, -1), -1)

    def position_value(self, positions) -> int:
        standing = getattr(getattr(positions, "POS_STANDING", None), "value", -1)
        raw = getattr(getattr(self, "character_attributes", None), "position", None)
        if raw is None:
            raw = getattr(self, "position", getattr(self, "start_pos", standing))
        if isinstance(raw, str):
            name = raw.strip().upper()
            if not name.startswith("POS_"):
                name = f"POS_{name}"
            member = getattr(positions, name, None)
            if member is not None:
                return int(member.value)
        return GenericUtil.to_int(raw, standing)

    def is_affected(self, affected_bits, bit_name: str) -> bool:
        from api.GameApi import GameApi

        bit = getattr(getattr(affected_bits, bit_name, None), "value", 0)
        flags = getattr(getattr(self, "status_flags", None), "affected_by", 0)
        return bit > 0 and GameApi.is_set(GameApi.flags_to_int(flags), bit)

    def set_affected(self, affected_bits, bit_name: str, enabled: bool) -> None:
        from api.GameApi import GameApi

        bit = getattr(getattr(affected_bits, bit_name, None), "value", 0)
        flags = getattr(self, "status_flags", None)
        if bit <= 0 or flags is None:
            return
        raw = GameApi.flags_to_int(getattr(flags, "affected_by", 0))
        updated = GameApi.set_bit(raw, bit) if enabled else GameApi.unset_bit(raw, bit)
        if hasattr(flags, "assign_bitfield"):
            flags.assign_bitfield("affected_by", updated)
        else:
            flags.affected_by = updated

    def find_effect(self, *type_names: str, affected_bits=None, bit_name: str = ""):
        from item.Effect import Effect

        wanted = {str(name or "").strip().lower() for name in type_names if str(name or "").strip()}
        bit = getattr(getattr(affected_bits, bit_name, None), "value", 0)
        for effect in list(getattr(self, "effects", []) or []):
            if str(getattr(effect, "type", "") or "").strip().lower() in wanted:
                return effect
            if bit > 0 and Effect.has_bit(effect, bit_name, bit):
                return effect
        return None

    def _item_collection_name(self) -> str:
        loot = getattr(self, "loot", None)
        if loot is not None:
            return "loot"
        return "inventory"

    def _item_collection(self) -> list[Any]:
        collection_name = self._item_collection_name()
        collection = getattr(self, collection_name, None)
        if collection is None:
            collection = []
            setattr(self, collection_name, collection)
        return collection

    def add_item(self, item: Any) -> None:
        with self.lock:
            collection = self._item_collection()
            if item not in collection:
                collection.append(item)

    def remove_item(self, item: Any) -> bool:
        with self.lock:
            inv = self._item_collection()
            try:
                inv.remove(item)
                return True
            except ValueError:
                return False

    def find_inventory_item(self, wanted: str, *, observer=None, room=None) -> Optional[Item]:
        from util.LookupUtil import LookupUtil
        viewer = self if observer is None else observer
        return LookupUtil.inventory(self, wanted, visible=lambda item: LookupUtil.object_visible(viewer, room, item))

    def ensure_equipped(self):
        return Equipped.ensure_on(self)

    def equipped_slot_of(self, item: Item) -> Optional[str]:
        equipped = self.equipped
        if equipped is None:
            return None
        return equipped.slot_of(item)

    def equip_item(self, item: Item, slot_name: str):
        return Equipped.equip_item(self, item, slot_name)

    def unequip_item(self, slot_name: str):
        return Equipped.unequip_item(self, slot_name)

    def owned_items(self) -> list:
        seen = set()
        items = []
        for item in list(self._item_collection()):
            item_id = id(item)
            if item is not None and item_id not in seen:
                items.append(item)
                seen.add(item_id)
        equipped = getattr(self, "equipped", None)
        for item in getattr(equipped, "__dict__", {}).values() if equipped is not None else []:
            item_id = id(item)
            if item is not None and item_id not in seen:
                items.append(item)
                seen.add(item_id)
        return items

    def find_owned_item(self, wanted: str, *, observer=None, room=None):
        from util.LookupUtil import LookupUtil
        viewer = self if observer is None else observer
        return LookupUtil.find(self.owned_items(), wanted, visible=lambda item: LookupUtil.object_visible(viewer, room, item))

    def regenerate(self, room, context: RegenerationContext) -> None:
        max_hit = GenericUtil.to_int(getattr(self, "max_hit", 0), 0)
        max_mana = GenericUtil.to_int(getattr(self, "max_mana", 0), 0)
        max_move = GenericUtil.to_int(getattr(self, "max_movement", 0), 0)

        hit = GenericUtil.to_int(getattr(self, "hit", 0), 0)
        mana = GenericUtil.to_int(getattr(self, "mana", 0), 0)
        move = GenericUtil.to_int(getattr(self, "movement", 0), 0)

        if hit < max_hit:
            setattr(self, "hit", min(max_hit, hit + self.hit_gain(room, context)))
        if mana < max_mana:
            setattr(self, "mana", min(max_mana, mana + self.mana_gain(room, context)))
        if move < max_move:
            setattr(self, "movement", min(max_move, move + self.move_gain(room, context)))

    def hit_gain(self, room, context: RegenerationContext) -> int:
        from api.CharacterApi import CharacterApi
        from skill.Ability import Ability

        if room is None:
            return 0

        max_hit = GenericUtil.to_int(getattr(self, "max_hit", 0), 0)
        hit = GenericUtil.to_int(getattr(self, "hit", 0), 0)
        if hit >= max_hit:
            return 0

        level = GenericUtil.to_int(getattr(self, "level", 0), 0)
        position = self.position_value(context.positions)
        if CharacterApi.is_npc(self):
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
        else:
            attrs = getattr(self, "character_attributes", None)
            constitution = GenericUtil.to_int(getattr(attrs, "constitution", 0), 0)
            gain = max(3, constitution - 3 + level // 2)
            gain += GenericUtil.to_int(getattr(getattr(self, "character_class", None), "hp_max", 10), 10) - 10
            number = context.rng.number_percent()
            if number < self._skill_percent("fast healing"):
                gain += number * gain // 100
                if hit < max_hit:
                    Ability.check_improve_by_name(self, "fast healing", True, 8)

            if position == context.position("POS_SLEEPING"):
                pass
            elif position == context.position("POS_RESTING"):
                gain //= 2
            elif position == context.position("POS_FIGHTING"):
                gain //= 6
            else:
                gain //= 4

            if self.condition_value("hunger") == 0:
                gain //= 2
            if self.condition_value("thirst") == 0:
                gain //= 2

        gain = gain * GenericUtil.to_int(getattr(room, "heal_rate", 100), 100) // 100
        gain = self._apply_furniture_regen_rate(gain, "value3")
        gain = self._apply_regen_affect_penalties(gain, context)
        return min(gain, max_hit - hit)

    def mana_gain(self, room, context: RegenerationContext) -> int:
        from api.CharacterApi import CharacterApi
        from skill.Ability import Ability

        if room is None:
            return 0

        max_mana = GenericUtil.to_int(getattr(self, "max_mana", 0), 0)
        mana = GenericUtil.to_int(getattr(self, "mana", 0), 0)
        if mana >= max_mana:
            return 0

        level = GenericUtil.to_int(getattr(self, "level", 0), 0)
        position = self.position_value(context.positions)
        if CharacterApi.is_npc(self):
            gain = 5 + level
            if position == context.position("POS_SLEEPING"):
                gain = 3 * gain // 2
            elif position == context.position("POS_RESTING"):
                pass
            elif position == context.position("POS_FIGHTING"):
                gain //= 3
            else:
                gain //= 2
        else:
            attrs = getattr(self, "character_attributes", None)
            wisdom = GenericUtil.to_int(getattr(attrs, "wisdom", 0), 0)
            intelligence = GenericUtil.to_int(getattr(attrs, "intelligence", 0), 0)
            gain = (wisdom + intelligence + level) // 2
            number = context.rng.number_percent()
            if number < self._skill_percent("meditation"):
                gain += number * gain // 100
                if mana < max_mana:
                    Ability.check_improve_by_name(self, "meditation", True, 8)

            if not bool(getattr(getattr(self, "character_class", None), "mana_gain", True)):
                gain //= 2

            if position == context.position("POS_SLEEPING"):
                pass
            elif position == context.position("POS_RESTING"):
                gain //= 2
            elif position == context.position("POS_FIGHTING"):
                gain //= 6
            else:
                gain //= 4

            if self.condition_value("hunger") == 0:
                gain //= 2
            if self.condition_value("thirst") == 0:
                gain //= 2

        gain = gain * GenericUtil.to_int(getattr(room, "mana_rate", 100), 100) // 100
        gain = self._apply_furniture_regen_rate(gain, "value4")
        gain = self._apply_regen_affect_penalties(gain, context)
        return min(gain, max_mana - mana)

    def move_gain(self, room, context: RegenerationContext) -> int:
        from api.CharacterApi import CharacterApi

        if room is None:
            return 0

        max_move = GenericUtil.to_int(getattr(self, "max_movement", 0), 0)
        move = GenericUtil.to_int(getattr(self, "movement", 0), 0)
        if move >= max_move:
            return 0

        level = GenericUtil.to_int(getattr(self, "level", 0), 0)
        position = self.position_value(context.positions)
        if CharacterApi.is_npc(self):
            gain = level
        else:
            attrs = getattr(self, "character_attributes", None)
            dexterity = GenericUtil.to_int(getattr(attrs, "dexterity", 0), 0)
            gain = max(15, level)
            if position == context.position("POS_SLEEPING"):
                gain += dexterity
            elif position == context.position("POS_RESTING"):
                gain += dexterity // 2

            if self.condition_value("hunger") == 0:
                gain //= 2
            if self.condition_value("thirst") == 0:
                gain //= 2

        gain = gain * GenericUtil.to_int(getattr(room, "heal_rate", 100), 100) // 100
        gain = self._apply_furniture_regen_rate(gain, "value3")
        gain = self._apply_regen_affect_penalties(gain, context)
        return min(gain, max_move - move)

    def _apply_regen_affect_penalties(self, gain: int, context) -> int:
        if self.is_affected(context.affected_bits, "AFF_POISON"):
            gain //= 4
        if self.is_affected(context.affected_bits, "AFF_PLAGUE"):
            gain //= 8
        if self.is_affected(context.affected_bits, "AFF_HASTE") or self.is_affected(context.affected_bits, "AFF_SLOW"):
            gain //= 2
        return gain

    def _apply_furniture_regen_rate(self, gain: int, field_name: str) -> int:
        furniture = getattr(self, "on", None)
        if furniture is None:
            return gain
        if str(getattr(furniture, "item_type", "") or "").strip().upper() not in {"ITEM_FURNITURE", "FURNITURE"}:
            return gain
        return gain * GenericUtil.to_int(getattr(furniture, field_name, 100), 100) // 100

    def _skill_percent(self, skill_name: str) -> int:
        from api.CharacterApi import CharacterApi
        from player.Character import Character

        if CharacterApi.is_npc(self):
            return 0
        return Character.learned_entry_level(Character.get_learned(self, skill_name, collection_name="skills"))
