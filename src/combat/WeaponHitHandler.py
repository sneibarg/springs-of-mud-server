from __future__ import annotations

from util.ElementalExposure import ElementalExposure

from injector import inject

from api.CharacterApi import CharacterApi
from game.EnumProvider import EnumProvider
from game.GameData import GameData
from item.Effect import Effect
from item.EffectHandler import EffectHandler


class WeaponHitHandler:
    """Apply weapon procs, delegating collateral exposure without sending IO."""

    @inject
    def __init__(self, effect_handler: EffectHandler, enum_provider: EnumProvider, game_data: GameData,
                 elemental_exposure: ElementalExposure = None):
        self._exposure = elemental_exposure or ElementalExposure(effect_handler, enum_provider, game_data)
        self.effect_handler = effect_handler
        self.weapon_types = enum_provider.get("weaponType")
        self.rules = game_data.weapon_hit_effects

    @property
    def elemental_exposure(self):
        return self._exposure

    @property
    def rng(self):
        return self._exposure.rng

    @rng.setter
    def rng(self, value):
        self._exposure.rng = value

    _merge = staticmethod(ElementalExposure._merge)

    def _flag(self, raw, enums, name):
        return self.elemental_exposure._flag(raw, enums, name)

    _messages = staticmethod(ElementalExposure._messages)

    def _saves(self, level, victim, dam_type, immunity):
        # This new path includes ROM's type immunity and mana-class adjustments;
        # existing spell callers retain their current saving-throw implementation.
        return self.elemental_exposure._saves(level, victim, dam_type, immunity)

    def apply(self, attacker, victim, weapon, *, damage, immunity, room):
        result = {}
        level = int(weapon.level)
        for name in ("poison", "vampiric", "flaming", "frost", "shocking"):
            if attacker.fighting is not victim:
                break
            rule = self.rules.get(name)
            if not rule or not self._flag(weapon.value4, self.weapon_types, rule["flag"]):
                continue
            if name == "poison":
                coating = next((effect for effect in self.effect_handler.ensure_effects(weapon)
                                if str(effect.type).lower() == "spell.poison"), None)
                poison_level = int(coating.level) if coating is not None else level
                if not self._saves(poison_level // 2, victim, "DAM_POISON", immunity):
                    self.effect_handler.affect_join(victim, Effect(
                        where="TO_AFFECTS", type="spell.poison", level=poison_level * 3 // 4,
                        duration=poison_level // 2, location="APPLY_STR", modifier=-1, bitvector="AFF_POISON"))
                    result = self._merge(result, self._messages(rule, "hit", attacker, victim, weapon, room))
                if coating is not None:
                    coating.level = max(0, coating.level - 2)
                    coating.duration = max(0, coating.duration - 1)
                    if coating.level == 0 or coating.duration == 0:
                        result = self._merge(result, self._messages(rule, "worn_off", attacker, victim, weapon, room))
                continue

            rolled = self.rng.number_range(1, level // rule["damageDivisor"] + rule["damageOffset"])
            result = self._merge(result, self._messages(rule, "hit", attacker, victim, weapon, room))
            if name != "vampiric":
                result = self._merge(result, self._element(name, rule, attacker, victim, level // 2,
                                                         rolled, room, immunity))
            result = self._merge(result, damage(attacker, victim, rolled, dt="0", dam_type=rule["damageType"], show=False))
            if name == "vampiric":
                attacker.set_alignment(max(-1000, attacker.get_alignment() - 1))
                # ROM heals from the rolled amount, even if secondary damage is
                # resisted/immune, and does not cap the result at maximum HP.
                attacker.hit += rolled // 2
        return result

    def expose(self, name, attacker, target, level, dam, room, immunity, *, payload):
        return self.elemental_exposure.expose(name, attacker, target, level, dam, room, immunity, payload=payload)

    def _element(self, name, rule, attacker, victim, level, dam, room, immunity):
        return self.elemental_exposure._element(name, rule, attacker, victim, level, dam, room, immunity)

    def _object_effect(self, name, rule, attacker, victim, item, level, dam, room, *, carrier):
        return self.elemental_exposure._object_effect(name, rule, attacker, victim, item, level, dam, room, carrier=carrier)
