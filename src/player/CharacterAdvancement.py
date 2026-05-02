from __future__ import annotations

import random

from dataclasses import dataclass, field

from player.CharacterMacros import CharacterMacros
from util.GenericUtil import GenericUtil


@dataclass
class LevelAdvanceResult:
    level: int
    hp_gain: int
    mana_gain: int
    move_gain: int
    practice_gain: int
    train_gain: int
    title: str = ""

    @property
    def message(self) -> str:
        practice_suffix = "" if self.practice_gain == 1 else "s"
        hp_suffix = "" if self.hp_gain == 1 else "s"
        return (
            "You raise a level!!\r\n"
            f"You gain {self.hp_gain} hit point{hp_suffix}, {self.mana_gain} mana, "
            f"{self.move_gain} move, and {self.practice_gain} practice{practice_suffix}.\r\n"
        )


@dataclass
class ExperienceGainResult:
    applied_gain: int
    current_experience: int
    accumulated_experience: int
    levels_gained: list[LevelAdvanceResult] = field(default_factory=list)

    @property
    def level_up_messages(self) -> str:
        return "".join(entry.message for entry in self.levels_gained)


class CharacterAdvancement:
    @staticmethod
    def gain_experience(character, gain: int) -> ExperienceGainResult:
        attrs = getattr(character, "character_attributes", None)
        try:
            is_npc = CharacterMacros.is_npc(character)
        except Exception:
            is_npc = False
        if character is None or attrs is None or is_npc:
            return ExperienceGainResult(0, 0, 0, [])

        hero_level = CharacterAdvancement._hero_level()
        current_level = GenericUtil.to_int(getattr(character, "level", 0), 0)
        current_xp = GenericUtil.to_int(getattr(attrs, "experience", 0), 0)
        accumulated_xp = GenericUtil.to_int(getattr(attrs, "accumulated_experience", 0), 0)
        xp_per_level = max(0, GenericUtil.to_int(getattr(attrs, "experience_per_level", 0), 0))
        applied_gain = GenericUtil.to_int(gain, 0)

        if current_level >= hero_level:
            return ExperienceGainResult(0, current_xp, accumulated_xp, [])

        current_xp = max(0, current_xp + applied_gain)
        accumulated_xp = max(0, accumulated_xp + applied_gain)

        attrs.experience = current_xp
        attrs.accumulated_experience = accumulated_xp

        levels_gained: list[LevelAdvanceResult] = []
        if xp_per_level > 0:
            while GenericUtil.to_int(getattr(character, "level", 0), 0) < hero_level and GenericUtil.to_int(getattr(attrs, "experience", 0), 0) >= xp_per_level:
                attrs.experience = GenericUtil.to_int(getattr(attrs, "experience", 0), 0) - xp_per_level
                character.level = GenericUtil.to_int(getattr(character, "level", 0), 0) + 1
                levels_gained.append(CharacterAdvancement.advance_level(character, hide=False))

        return ExperienceGainResult(
            applied_gain=applied_gain,
            current_experience=GenericUtil.to_int(getattr(attrs, "experience", 0), 0),
            accumulated_experience=GenericUtil.to_int(getattr(attrs, "accumulated_experience", 0), 0),
            levels_gained=levels_gained,
        )

    @staticmethod
    def advance_level(character, hide: bool = False) -> LevelAdvanceResult:
        del hide
        attrs = getattr(character, "character_attributes", None)
        class_data = getattr(character, "character_class", None)

        con = CharacterAdvancement._stat(character, "constitution")
        intel = CharacterAdvancement._stat(character, "intelligence")
        wis = CharacterAdvancement._stat(character, "wisdom")
        dex = CharacterAdvancement._stat(character, "dexterity")

        hp_min = max(0, GenericUtil.to_int(getattr(class_data, "hp_min", 0), 0))
        hp_max = max(hp_min, GenericUtil.to_int(getattr(class_data, "hp_max", hp_min), hp_min))
        hp_bonus = CharacterAdvancement._attribute_bonus("constitution", con, "hitp", 0)
        add_hp = hp_bonus + random.randint(hp_min, hp_max)

        mana_max = max(2, (2 * intel + wis) // 5)
        add_mana = random.randint(2, mana_max)
        if not bool(getattr(class_data, "mana_gain", False)):
            add_mana //= 2

        move_max = max(1, (con + dex) // 6)
        add_move = random.randint(1, move_max)
        add_prac = CharacterAdvancement._attribute_bonus("wisdom", wis, "practice", 0)

        add_hp = max(2, add_hp * 9 // 10)
        add_mana = max(2, add_mana * 9 // 10)
        add_move = max(6, add_move * 9 // 10)

        character.max_hit = GenericUtil.to_int(getattr(character, "max_hit", 0), 0) + add_hp
        character.max_mana = GenericUtil.to_int(getattr(character, "max_mana", 0), 0) + add_mana
        character.max_movement = GenericUtil.to_int(getattr(character, "max_movement", 0), 0) + add_move

        if attrs is not None:
            attrs.practices = GenericUtil.to_int(getattr(attrs, "practices", 0), 0) + add_prac
            attrs.trains = GenericUtil.to_int(getattr(attrs, "trains", 0), 0) + 1

        title = CharacterMacros.title_for_level(character, GenericUtil.to_int(getattr(character, "level", 0), 0))
        if title:
            character.title = title

        return LevelAdvanceResult(
            level=GenericUtil.to_int(getattr(character, "level", 0), 0),
            hp_gain=add_hp,
            mana_gain=add_mana,
            move_gain=add_move,
            practice_gain=add_prac,
            train_gain=1,
            title=title,
        )

    @staticmethod
    def _hero_level() -> int:
        try:
            params = CharacterMacros.get_enum("gameParameters")
        except Exception:
            params = None
        if hasattr(params, "LEVEL_HERO"):
            return GenericUtil.to_int(getattr(params.LEVEL_HERO, "value", 51), 51)
        return 51

    @staticmethod
    def _stat(character, field_name: str) -> int:
        attrs = getattr(character, "character_attributes", None)
        return GenericUtil.to_int(getattr(attrs, field_name, 0), 0) if attrs is not None else 0

    @staticmethod
    def _attribute_bonus(table_name: str, stat_value: int, key: str, default: int = 0) -> int:
        try:
            bonuses = CharacterMacros._attribute_bonus_map()
        except Exception:
            return default
        table = bonuses.get(str(table_name or "").lower(), {})
        row = table.get(str(GenericUtil.to_int(stat_value, 0)), {})
        return GenericUtil.to_int(row.get(key, default), default)
