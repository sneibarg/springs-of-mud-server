from __future__ import annotations

from injector import inject

from api.CharacterApi import CharacterApi
from api.GameApi import GameApi
from game.EnumProvider import EnumProvider
from game.GameData import GameData
from game.GamePayload import GamePayload
from game.RandomNumberGenerator import RandomNumberGenerator
from item.Effect import Effect
from item.EffectHandler import EffectHandler
from util.DisplayUtil import DisplayUtil


class WeaponHitHandler:
    """Apply weapon procs and reusable elemental exposure without sending IO."""

    @inject
    def __init__(self, effect_handler: EffectHandler, enum_provider: EnumProvider, game_data: GameData):
        self.effect_handler = effect_handler
        self.weapon_types = enum_provider.get("weaponType")
        self.item_flags = enum_provider.get("itemFlags")
        self.affected_by = enum_provider.get("affectedBy")
        self.game_parameters = enum_provider.get("gameParameters")
        self.rules = game_data.weapon_hit_effects
        self.item_table = game_data.item_table
        self.rng = RandomNumberGenerator()

    @staticmethod
    def _merge(base, extra):
        result = {**base, **extra}
        for channel in ("to_char", "to_victim", "to_room", "level_up_messages"):
            result[channel] = base.get(channel, "") + extra.get(channel, "")
        result["killed"] = bool(base.get("killed") or extra.get("killed"))
        result["xp_gain"] = base.get("xp_gain", 0) + extra.get("xp_gain", 0)
        for key in ("reward_payloads", "post_damage_actions", "pre_damage_payloads"):
            if key in base or key in extra:
                result[key] = base.get(key, []) + extra.get(key, [])
        return result

    def _flag(self, raw, enums, name):
        return GameApi.is_set(GameApi.flags_to_int(raw), CharacterApi.enum_bit(enums, name))

    @staticmethod
    def _messages(rule, key, attacker, victim, weapon, room=None):
        payload = GamePayload.from_json(rule.get("payload", {}))
        tokens = {
            "attacker": DisplayUtil.entity_name(attacker, is_npc=CharacterApi.is_npc),
            "victim": DisplayUtil.entity_name(victim, is_npc=CharacterApi.is_npc),
            "weapon": str(getattr(weapon, "short_description", "") or getattr(weapon, "name", "")),
        }
        messages = {}
        for channel in ("to_char", "to_victim", "to_room"):
            text = payload.render(channel, key, **tokens)
            messages[channel] = text.rstrip("\r\n") + "\r\n" if text else ""
        entities = {"attacker": attacker, "victim": victim, "weapon": weapon}

        def render(channel, observer):
            text = payload.render(channel, key, **DisplayUtil.visible_tokens(entities, observer, room))
            return text.rstrip("\r\n") + "\r\n" if text else ""

        messages["to_char"] = render("to_char", attacker)
        messages["to_victim"] = render("to_victim", victim)
        messages["to_room"] = DisplayUtil.room_text(messages["to_room"], lambda observer: render("to_room", observer), room)
        return messages

    def _saves(self, level, victim, dam_type, immunity):
        # This new path includes ROM's type immunity and mana-class adjustments;
        # existing spell callers retain their current saving-throw implementation.
        status = immunity(victim, dam_type)
        if status == "IS_IMMUNE":
            return True
        save = 50 + (victim.level - level) * 5 - int(getattr(victim, "saving_throw", 0)) * 2
        if self._flag(victim.status_flags.affected_by, self.affected_by, "AFF_BERSERK"):
            save += victim.level // 2
        if status == "IS_RESISTANT":
            save += 2
        elif status == "IS_VULNERABLE":
            save -= 2
        if not CharacterApi.is_npc(victim) and getattr(getattr(victim, "character_class", None), "mana_gain", False):
            save = int(9 * save / 10)
        return self.rng.number_percent() < max(5, min(95, save))

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
        """Expose a character or room, using the calling ability's messages."""
        if name not in ("flaming", "frost", "shocking"):
            raise ValueError(f"Unsupported elemental exposure: {name}")
        rule = {**self.rules[name], "payload": payload}
        if hasattr(target, "owned_items"):
            return self._element(name, rule, attacker, target, level, dam, room, immunity)
        result = {}
        for item in list(target.contents.values()):
            result = self._merge(result, self._object_effect(
                name, rule, attacker, None, item, level, dam, target, carrier=None))
        return result

    def _element(self, name, rule, attacker, victim, level, dam, room, immunity):
        result = {}
        save_level = level // 4 + dam // 20
        if name == "flaming":
            if (not self._flag(victim.status_flags.affected_by, self.affected_by, "AFF_BLIND")
                    and not self._saves(save_level, victim, rule["damageType"], immunity)):
                self.effect_handler.affect_to_char(victim, Effect(
                    where="TO_AFFECTS", type="spell.fire_breath", level=level,
                    duration=self.rng.number_range(0, level // 10), location="APPLY_HITROLL",
                    modifier=-4, bitvector="AFF_BLIND"))
                result = self._messages(rule, "secondary", attacker, victim, None, room)
            condition = "thirst"
        elif name == "frost":
            if not self._saves(save_level, victim, rule["damageType"], immunity):
                self.effect_handler.affect_join(victim, Effect(
                    where="TO_AFFECTS", type="spell.chill_touch", level=level, duration=6,
                    location="APPLY_STR", modifier=-1, bitvector=0))
                result = self._messages(rule, "secondary", attacker, victim, None, room)
            condition = "hunger"
        else:
            if not self._saves(save_level, victim, rule["damageType"], immunity):
                victim.status_flags.pulse_daze = max(victim.status_flags.pulse_daze, 12, save_level)
                result = self._messages(rule, "secondary", attacker, victim, None, room)
            condition = ""
        if (condition and not CharacterApi.is_npc(victim)
                and victim.level < self.game_parameters.LEVEL_IMMORTAL.value):
            text = victim.gain_condition(condition, dam // 20)
            result["to_victim"] = result.get("to_victim", "") + text
        for item in victim.owned_items():
            result = self._merge(result, self._object_effect(name, rule, attacker, victim, item,
                                                           level, dam, room, carrier=victim))
        return result

    def _object_effect(self, name, rule, attacker, victim, item, level, dam, room, *, carrier):
        if (self._flag(item.extra_flags, self.item_flags, "ITEM_BURN_PROOF")
                or self._flag(item.extra_flags, self.item_flags, "ITEM_NOPURGE")
                or self.rng.number_range(0, 4) == 0):
            return {}
        chance = level // 4 + dam // 10
        if chance > 25:
            chance = (chance - 25) // 2 + 25
        if chance > 50:
            chance = (chance - 50) // 2 + 50
        if self._flag(item.extra_flags, self.item_flags, "ITEM_BLESS"):
            chance -= 5
        chance -= int(item.level) * 2
        raw_type = str(item.item_type).lower()
        item_type = self.item_table.get(raw_type, {}).get("type", raw_type).lower().removeprefix("item_")
        entry = rule.get("objects", {}).get(item_type)
        if entry is None or self.rng.number_percent() > max(5, min(95, chance + entry["chanceBonus"])):
            return {}
        result = self._messages(rule, entry["messageKey"], attacker, victim, item, room)
        if name == "flaming":
            for child in list(item.contains):
                item.contains.remove(child)
                if room is not None:
                    room.add_item_to_room(child)
                    result = self._merge(result, self._object_effect(name, rule, attacker, victim, child,
                                                                   level // 2, dam // 2, room, carrier=None))
        # Use normal unequip and effect removal so destroyed equipment stops
        # contributing stats. Live items are held by their owner/room, not the
        # prototype item registry.
        if carrier is not None:
            equipped = getattr(carrier, "equipped", None)
            slot = next((slot for slot, value in vars(equipped).items() if value is item), None) if equipped else None
            if slot is not None:
                self.effect_handler.remove_item_effects(carrier, item)
                carrier.unequip_item(slot)
            carrier.remove_item(item)
        elif room is not None:
            room.remove_item_from_room(item)
        item.contains.clear()
        return result
