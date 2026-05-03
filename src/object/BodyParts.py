from __future__ import annotations

import random
from enum import IntEnum

from game.GameData import GameData
from object.BodyForm import BodyForm


class BodyParts:
    _enum: type[IntEnum] | None = None
    _death_cry_drops = (
        (2, "PART_GUTS", "OBJ_VNUM_GUTS"),
        (3, "PART_HEAD", "OBJ_VNUM_SEVERED_HEAD"),
        (4, "PART_HEART", "OBJ_VNUM_TORN_HEART"),
        (5, "PART_ARMS", "OBJ_VNUM_SLICED_ARM"),
        (6, "PART_LEGS", "OBJ_VNUM_SLICED_LEG"),
        (7, "PART_BRAINS", "OBJ_VNUM_BRAINS"),
    )

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("BodyParts may not be instantiated.")

    @classmethod
    def configure(cls, game_data: GameData) -> None:
        member_map = dict(getattr(game_data, "enums", {}).get("bodyParts", {}))
        if not member_map:
            raise RuntimeError("GameData is missing bodyParts enum definitions.")

        cls.reset_for_tests()
        cls._enum = IntEnum("BodyParts", {str(name).strip().upper(): int(value) for name, value in member_map.items()})
        for name, member in cls._enum.__members__.items():
            setattr(cls, name, member)

    @classmethod
    def reset_for_tests(cls) -> None:
        for name in list(vars(cls).keys()):
            if name.startswith("PART_"):
                delattr(cls, name)
        cls._enum = None

    @classmethod
    def _require_configured(cls) -> type[IntEnum]:
        if cls._enum is None:
            raise RuntimeError("BodyParts has not been configured.")
        return cls._enum

    @classmethod
    def members(cls) -> dict[str, IntEnum]:
        return dict(cls._require_configured().__members__)

    @classmethod
    def value(cls, name: str) -> int:
        enum_type = cls._require_configured()
        return int(enum_type[str(name).strip().upper()].value)

    @classmethod
    def mask(cls, *names: str) -> int:
        total = 0
        for name in names:
            total |= cls.value(name)
        return total

    @classmethod
    def has(cls, flags: int, bit) -> bool:
        raw_bit = getattr(bit, "value", bit)
        return (int(flags) & int(raw_bit)) != 0

    @classmethod
    def default_player_parts(cls) -> int:
        return cls.mask(
            "PART_HEAD",
            "PART_ARMS",
            "PART_LEGS",
            "PART_HEART",
            "PART_BRAINS",
            "PART_GUTS",
            "PART_HANDS",
            "PART_FEET",
            "PART_FINGERS",
            "PART_EAR",
            "PART_EYE",
        )

    @classmethod
    def maybe_create_death_cry_part(cls, victim, room, item_registry, well_known_object_vnums, form_flags: int, parts_flags: int):
        if victim is None or room is None:
            return None

        selected_vnum = None
        roll = random.randint(0, 15)
        for target_roll, part_name, vnum_name in cls._death_cry_drops:
            if roll != target_roll:
                continue
            if not cls.has(parts_flags, cls.value(part_name)):
                return None
            selected_vnum = getattr(well_known_object_vnums, vnum_name, None)
            break

        if selected_vnum is None:
            return None

        proto = item_registry.get_or_none(vnum=str(int(getattr(selected_vnum, "value", selected_vnum))))
        if proto is None:
            return None

        from util.ItemUtil import ItemUtil

        part_item = ItemUtil.create_object(proto)
        part_item.timer = random.randint(4, 7)

        victim_name = cls._victim_name(victim)
        part_item.short_description = cls._format_template(getattr(part_item, "short_description", ""), victim_name)
        part_item.long_description = cls._format_template(getattr(part_item, "long_description", ""), victim_name)

        item_type = str(getattr(part_item, "item_type", "") or "").lower()
        if "food" in item_type:
            if BodyForm.has(form_flags, BodyForm.value("FORM_POISON")):
                part_item.value3 = "1"
            elif not BodyForm.has(form_flags, BodyForm.value("FORM_EDIBLE")):
                part_item.item_type = "trash"

        room.add_item_to_room(part_item)
        return part_item

    @staticmethod
    def _victim_name(victim) -> str:
        from player.CharacterMacros import CharacterMacros

        if CharacterMacros.is_npc(victim):
            return str(getattr(victim, "short_description", "") or getattr(victim, "name", "someone"))
        return str(getattr(victim, "name", "someone"))

    @staticmethod
    def _format_template(text: str, victim_name: str) -> str:
        raw = str(text or "")
        if "%s" in raw:
            try:
                return raw % victim_name
            except Exception:
                return raw.replace("%s", victim_name)
        return raw


__all__ = ["BodyParts"]
