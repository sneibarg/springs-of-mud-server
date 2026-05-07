import random
from enum import IntEnum
from threading import RLock

from typing import Any, Optional, Callable

from game.GameMacros import GameMacros
from mobile.Mobile import Mobile
from util.GenericUtil import GenericUtil
from util.MobileUtil import MobileUtil
from player.CharacterMacros import CharacterMacros


class MobileMacros(GameMacros):
    _lock = RLock()
    _configured = False

    _races_provider: Optional[Callable[[], dict]] = None
    _item_table_provider: Optional[Callable[[], dict]] = None
    _enums_provider: Optional[Callable[[], dict[str, IntEnum]]] = None

    _races = None
    _item_table = None
    _enums = None

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("MobileMacros may not be instantiated. Use MobileMacros.<method>(...).")

    @classmethod
    def configure(
        cls,
        *,
        races_provider: Callable[[], dict],
        item_table_provider: Callable[[], dict],
        enums_provider: Callable[[], dict[str, IntEnum]],
    ) -> None:
        with cls._lock:
            cls._races_provider = races_provider
            cls._item_table_provider = item_table_provider
            cls._enums_provider = enums_provider
            cls._configured = True

    @classmethod
    def configure(
        cls,
        *,
        races_provider: Callable[[], dict],
        item_table_provider: Callable[[], dict],
        enums_provider: Callable[[], dict[str, IntEnum]],
    ) -> None:
        with cls._lock:
            cls._races_provider = races_provider
            cls._item_table_provider = item_table_provider
            cls._enums_provider = enums_provider
            cls._configured = True

    @classmethod
    def reset_for_tests(cls) -> None:
        with cls._lock:
            cls._configured = False
            cls._races_provider = None
            cls._item_table_provider = None
            cls._enums_provider = None
            cls._races = None
            cls._item_table = None
            cls._enums = None

    @classmethod
    def _require_configured(cls) -> None:
        if not cls._configured:
            raise RuntimeError("MobileMacros has not been configured.")

    @classmethod
    def _races_map(cls) -> dict:
        if cls._races is None:
            cls._require_configured()
            if cls._races_provider is None:
                raise RuntimeError("MobileMacros races provider not configured.")
            cls._races = cls._races_provider()
        return cls._races

    @classmethod
    def _item_table_map(cls) -> dict:
        if cls._item_table is None:
            cls._require_configured()
            if cls._item_table_provider is None:
                raise RuntimeError("MobileMacros item_table provider not configured.")
            cls._item_table = cls._item_table_provider()
        return cls._item_table

    @classmethod
    def _enums_map(cls) -> dict[str, IntEnum]:
        if cls._enums is None:
            cls._require_configured()
            if cls._enums_provider is None:
                raise RuntimeError("MobileMacros enums provider not configured.")
            cls._enums = cls._enums_provider()
        return cls._enums

    @classmethod
    def get_enum(cls, enum_name: str) -> Any:
        return cls._enums_map().get(enum_name)

    @staticmethod
    def choose_weighted(weighted: list[tuple[Any, int]]) -> Any:
        choices = [(value, max(0, GenericUtil.to_int(weight, 0))) for value, weight in weighted]
        total = sum(weight for _, weight in choices)
        if total <= 0:
            return None
        roll = random.randint(1, total)
        running = 0
        for value, weight in choices:
            running += weight
            if roll <= running:
                return value
        return choices[-1][0] if choices else None

    @staticmethod
    def resolve_room(room_registry, entity) -> Any:
        room_id = str(getattr(entity, "room_id", "") or "")
        if room_id:
            room = room_registry.get_or_none(id=room_id)
            if room is not None:
                return room
        entity_id = str(getattr(entity, "id", "") or "")
        if not entity_id:
            return None
        for room in room_registry.all_rooms():
            if room is None:
                continue
            if entity_id in getattr(room, "mobiles", {}) or entity_id in getattr(room, "characters", {}):
                return room
        return None

    @staticmethod
    def resolve_exit_destination(room_registry, exit_obj):
        if exit_obj is None:
            return None
        to_room_vnum = getattr(exit_obj, "to_room_vnum", None)
        if to_room_vnum not in (None, "", "0", 0):
            room = room_registry.get_or_none(vnum=str(to_room_vnum))
            if room is not None:
                return room
        to_room_id = str(getattr(exit_obj, "to_room_id", "") or "")
        if to_room_id:
            return room_registry.get_or_none(id=to_room_id)
        return None

    @staticmethod
    def move_mobile(room, to_room, mob) -> bool:
        if room is None or to_room is None or mob is None:
            return False
        room.mobiles.pop(str(getattr(mob, "id", "") or ""), None)
        to_room.mobiles[str(getattr(mob, "id", "") or "")] = mob
        setattr(mob, "room_id", getattr(to_room, "id", ""))
        setattr(mob, "area_id", getattr(to_room, "area_id", ""))
        return True

    @staticmethod
    def give_room_item_to_mobile(room, mob, item) -> bool:
        if room is None or mob is None or item is None:
            return False
        room.contents.pop(str(getattr(item, "id", "") or ""), None)
        MobileUtil.add_inventory_item(mob, item)
        return True

    @staticmethod
    def enum_bit(enum_obj, *names: str) -> int:
        for name in names:
            value = CharacterMacros.enum_bit(enum_obj, name)
            if value:
                return value
        return 0

    @staticmethod
    def render_mobile_name(entity) -> str:
        if entity is None:
            return "someone"
        if CharacterMacros.is_npc(entity):
            return str(getattr(entity, "short_description", "") or getattr(entity, "name", "someone"))
        return str(getattr(entity, "name", "someone"))

    @staticmethod
    def render_act(text: str, actor, target=None) -> str:
        rendered = str(text or "")
        rendered = rendered.replace("$n", MobileMacros.render_mobile_name(actor))
        rendered = rendered.replace("$N", MobileMacros.render_mobile_name(target))
        if target is not None:
            sex = str(getattr(target, "sex", "") or "").lower()
            poss = "their"
            if sex in ("1", "m", "male"):
                poss = "his"
            elif sex in ("2", "f", "female"):
                poss = "her"
            rendered = rendered.replace("$S", poss)
        return rendered

    @staticmethod
    def group_vnum(group_name: str) -> str:
        mapping = {
            "GROUP_VNUM_TROLLS": "2100",
            "GROUP_VNUM_OGRES": "2101",
        }
        normalized = str(group_name or "").strip().upper()
        return mapping.get(normalized, normalized)

    @classmethod
    def mobile_is_charmed(cls, mob: Any) -> bool:
        charm = cls.enum_bit(cls.get_enum("affectedBy"), "AFF_CHARM")
        if charm == 0:
            return False
        flags = GenericUtil.to_int(getattr(getattr(mob, "status_flags", None), "affected_by", 0), 0)
        return (flags & charm) != 0

    @classmethod
    def mobile_has_act(cls, mob: Any, act_bits, name: str) -> bool:
        bit = cls.enum_bit(act_bits, name)
        if bit == 0:
            return False
        flags = GenericUtil.to_int(getattr(getattr(mob, "status_flags", None), "act", 0), 0)
        return (flags & bit) != 0

    @classmethod
    def mobile_is_standing(cls, mob: Any) -> bool:
        standing = cls.enum_bit(cls.get_enum("positions"), "POS_STANDING")
        current = GenericUtil.to_int(getattr(mob, "position", getattr(mob, "start_pos", standing)), standing)
        return current == standing

    @classmethod
    def mobile_will_assist(cls, char: Mobile) -> bool:
        if type(char) is not Mobile:
            return False
        OffenseTypes = cls.get_enum("offenseTypes")
        return cls.is_set(char.status_flags.off, OffenseTypes.ASSIST_PLAYERS.value)
