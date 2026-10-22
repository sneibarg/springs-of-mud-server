from copy import deepcopy

from api.GameApi import GameApi
from item.Effect import Effect
from util.EffectUtil import EffectUtil


class AcidExposure:
    """ROM acid exposure for live objects; callers own message rendering."""

    def __init__(self, effects, item_flags, apply_types, item_table, rng):
        self.effects = effects
        self.item_flags = item_flags
        self.apply_types = apply_types
        self.item_table = item_table
        self.rng = rng

    def character(self, victim, level, damage, room, notify):
        for item in victim.owned_items():
            self.object(item, level, damage, room, notify, carrier=victim)

    def room(self, room, level, damage, notify):
        for item in list(room.contents.values()):
            self.object(item, level, damage, room, notify)

    def object(self, item, level, damage, room, notify, *, carrier=None):
        flags = GameApi.flags_to_int(item.extra_flags)
        if (GameApi.is_set(flags, self.item_flags.ITEM_BURN_PROOF.value)
                or GameApi.is_set(flags, self.item_flags.ITEM_NOPURGE.value)
                or self.rng.number_range(0, 4) == 0):
            return
        chance = level // 4 + damage // 10
        if chance > 25:
            chance = (chance - 25) // 2 + 25
        if chance > 50:
            chance = (chance - 50) // 2 + 50
        if GameApi.is_set(flags, self.item_flags.ITEM_BLESS.value):
            chance -= 5
        chance -= int(item.level) * 2
        raw_type = str(item.item_type).lower()
        kind = self.item_table.get(raw_type, {}).get("type", raw_type).lower().removeprefix("item_")
        if kind in ("container", "corpse_pc", "corpse_npc"):
            key = "acid_container"
        elif kind == "armor":
            key = "acid_armor"
        elif kind == "clothing":
            key = "acid_clothing"
        elif kind in ("staff", "wand"):
            chance -= 10
            key = "acid_focus"
        elif kind == "scroll":
            chance += 10
            key = "acid_scroll"
        else:
            return
        if self.rng.number_percent() > max(5, min(95, chance)):
            return
        if carrier is not None or room is not None:
            notify(key, item)
        slot = carrier.equipped_slot_of(item) if carrier is not None else None
        if kind == "armor":
            if slot is not None:
                self.effects.remove_item_effects(carrier, item)
            # Effects are normalized from prototype data when objects are built.
            # Own the records before mutating, including cloned-instance records.
            item.effects = deepcopy(self.effects.ensure_effects(item))
            item.enchanted = True
            ac = EffectUtil.enum_value(self.apply_types, "APPLY_AC")
            effect = next((effect for effect in item.effects
                           if EffectUtil.enum_value(self.apply_types, effect.location, -1) == ac), None)
            if effect is None:
                item.effects.insert(0, Effect(where="TO_OBJECT", type=-1, level=level,
                                             duration=-1, location="APPLY_AC", modifier=1))
            else:
                effect.type = -1
                effect.modifier = int(effect.modifier) + 1
                effect.level = max(int(effect.level), level)
            if slot is not None:
                self.effects.apply_item_effects(carrier, item)
            return
        for child in list(item.contains):
            item.contains.remove(child)
            if room is not None:
                room.add_item_to_room(child)
                self.object(child, level // 2, damage // 2, room, notify)
            else:
                self._discard_contents(child)
        if carrier is not None:
            if slot is not None:
                self.effects.remove_item_effects(carrier, item)
                carrier.unequip_item(slot)
            carrier.remove_item(item)
        elif room is not None:
            room.remove_item_from_room(item)

    @classmethod
    def _discard_contents(cls, item):
        for child in list(item.contains):
            cls._discard_contents(child)
        item.contains.clear()
