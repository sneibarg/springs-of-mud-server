from typing import Any
from injector import inject

from player.CharacterMacros import CharacterMacros
from server.LoggerFactory import LoggerFactory
from skill import Skill
from skill.SkillRegistry import SkillRegistry
from util.GenericUtil import GenericUtil


class SkillApi:
    @inject
    def __init__(self, skill_registry: SkillRegistry):
        self.skill_registry = skill_registry
        self.logger = LoggerFactory.get_logger("SkillApi")
        self.ActBits = None
        self.OffBits = None
        self.CondBits = None

    def lazy_load(self):
        self.ActBits = CharacterMacros.get_enum("actBits")
        self.OffBits = CharacterMacros.get_enum("offenseTypes")
        self.CondBits = CharacterMacros.get_enum("conditions")
        self.logger.info("Loaded SkillApi enums.")

    def get_rating(self, char: Any, skill: Skill) -> int:
        if skill is None:
            return GenericUtil.to_int(char.level * 5 / 2)

        rating = 0
        if not CharacterMacros.is_npc(char):
            rating = char.skill_level(skill.name)
        else:
            # TO-DO: this function should never be called when a spell is being cast
            if skill is None:
                rating = 40 + 2 * char.level
            elif skill.name in ("sneak", "hide"):
                rating = char.level * 2 + 20
            elif (skill.name == "dodge" and CharacterMacros.is_set(char.off_flags, self.OffBits.OFF_DODGE)) or \
                    (skill.name == "parry" and CharacterMacros.is_set(char.off_flags, self.OffBits.OFF_PARRY)):
                rating = char.level * 2
            elif skill.name == "shield block":
                rating = 10 + 2 * char.level
            elif skill.name == "second attack" and \
                    (CharacterMacros.is_set(char.act, self.ActBits.ACT_WARRIOR) or
                     CharacterMacros.is_set(char.act, self.ActBits.ACT_THIEF)):
                rating = 10 + 3 * char.level

            elif skill.name == "third attack" and CharacterMacros.is_set(char.act, self.ActBits.ACT_WARRIOR):
                rating = 4 * char.level - 40
            elif skill.name == "hand to hand":
                rating = 40 + 2 * char.level
            elif skill.name == "trip" and CharacterMacros.is_set(char.off_flags, self.OffBits.OFF_TRIP):
                rating = 10 + 3 * char.level
            elif skill.name == "bash" and CharacterMacros.is_set(char.off_flags, self.OffBits.OFF_BASH):
                rating = 10 + 3 * char.level
            elif skill.name == "disarm" and (
                    CharacterMacros.is_set(char.off_flags, self.OffBits.OFF_DISARM) or
                    CharacterMacros.is_set(char.act, self.ActBits.ACT_WARRIOR) or
                    CharacterMacros.is_set(char.act, self.ActBits.ACT_THIEF)):
                rating = 20 + 3 * char.level
            elif skill.name == "berserk" and CharacterMacros.is_set(char.off_flags, self.OffBits.OFF_BERSERK):
                rating = 3 * char.level
            elif skill.name == "kick":
                rating = 10 + 3 * char.level
            elif skill.name == "backstab" and CharacterMacros.is_set(char.act, self.ActBits.ACT_THIEF):
                rating = 20 + 2 * char.level
            elif skill.name == "rescue":
                rating = 40 + char.level
            elif skill.name == "recall":
                rating = 40 + char.level
            elif skill.name in ("sword", "dagger", "spear", "mace", "axe", "flail", "whip", "polearm"):
                rating = 40 + 5 * char.level // 2

            #  TO-DO - this needs validated for correctness
            if char.status_flags.pulse_daze > 0:
                if skill is None:
                    rating //= 2
                else:
                    rating = 2 * rating // 3

            if not CharacterMacros.is_npc(char) and char.status_flags.condition.drunk > 10:
                rating = 9 * rating // 10

            return max(0, min(100, rating))
        return rating
