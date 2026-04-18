from __future__ import annotations

import random

from injector import inject

from game.GenericUtil import GenericUtil
from object.Effect import Effect
from object.EffectUtil import EffectUtil
from player.CharacterMacros import CharacterMacros


class EffectHelper:
    @inject
    def __init__(self, character_macros: CharacterMacros):
        self.character_macros = character_macros
        self.enums = character_macros.enums
        self.affected_by = self.enums.get("affectedBy")

    def effect_from_spell_affect(self, spell, affect_like, caster_level: int, source: str = "") -> Effect:
        effect = EffectUtil.as_effect(affect_like, source=source)
        raw_type = str(getattr(effect, "type", "") or "").strip().lower()
        if raw_type in ("sn", "skill", "spell"):
            effect.type = str(getattr(spell, "handler_id", "") or getattr(spell, "name", ""))
        level = getattr(effect, "level", 0)
        if str(level).strip().lower() == "level":
            effect.level = int(caster_level)
        else:
            effect.level = GenericUtil.to_int(level, int(caster_level))
        effect.duration = GenericUtil.to_int(getattr(effect, "duration", 0), 0)
        effect.modifier = GenericUtil.to_int(getattr(effect, "modifier", 0), 0)
        return effect

    def apply_spell_effects(self, caster, victim, spell):
        affects = list(getattr(spell, "affects", []) or [])
        if not affects or victim is None:
            return
        source = f"spell:{getattr(spell, 'handler_id', getattr(spell, 'name', ''))}"
        caster_level = GenericUtil.to_int(getattr(caster, "level", 0), 0)
        for affect_like in affects:
            effect = self.effect_from_spell_affect(spell, affect_like, caster_level, source=source)
            EffectUtil.affect_join(victim, effect, self.enums)

    def apply_item_effects(self, character, item):
        effects = list(getattr(item, "effects", []) or [])
        if not effects:
            return
        source = f"item:{getattr(item, 'id', '')}:{id(item)}"
        for affect_like in effects:
            effect = EffectUtil.as_effect(affect_like, source=source)
            EffectUtil.affect_to_char(character, effect, self.enums)

    def remove_item_effects(self, character, item):
        source = f"item:{getattr(item, 'id', '')}:{id(item)}"
        for effect in list(EffectUtil.ensure_effects(character)):
            if getattr(effect, "source", "") == source:
                EffectUtil.affect_remove(character, effect, self.enums)

    def is_affected(self, character, effect_type) -> bool:
        if EffectUtil.is_affected(character, effect_type):
            return True
        if self.affected_by is not None and hasattr(self.affected_by, str(effect_type)):
            bit = getattr(self.affected_by, str(effect_type)).value
            return self.character_macros.is_affected(character, bit)
        return False

    @staticmethod
    def saves_dispel(dis_level: int, spell_level: int, duration: int) -> bool:
        save = 50 + (GenericUtil.to_int(spell_level, 0) - GenericUtil.to_int(dis_level, 0)) * 5
        if GenericUtil.to_int(duration, 0) == -1:
            save += 5
        save = max(5, min(95, save))
        return random.randint(1, 100) < save

    def check_dispel(self, dis_level: int, victim, effect_type) -> bool:
        removed = False
        for effect in list(EffectUtil.ensure_effects(victim)):
            if str(getattr(effect, "type", "")).strip().lower() != str(effect_type).strip().lower():
                continue
            if not self.saves_dispel(dis_level, GenericUtil.to_int(getattr(effect, "level", 0), 0), GenericUtil.to_int(getattr(effect, "duration", 0), 0)):
                EffectUtil.affect_remove(victim, effect, self.enums)
                removed = True
            else:
                effect.level = max(0, GenericUtil.to_int(getattr(effect, "level", 0), 0) - 1)
        return removed

    def saves_spell(self, level: int, victim, _dam_type: int = 0) -> bool:
        victim_level = GenericUtil.to_int(getattr(victim, "level", 0), 0)
        saving_throw = GenericUtil.to_int(getattr(victim, "saving_throw", 0), 0)
        save = 50 + (victim_level - GenericUtil.to_int(level, 0)) * 5 - saving_throw * 2
        if self.is_affected(victim, "AFF_BERSERK"):
            save += victim_level // 2
        save = max(5, min(95, save))
        return random.randint(1, 100) < save
