from util.ExposureUtil import exposure_chance, item_kind
from api.GameApi import GameApi
from item.Effect import Effect


class PoisonExposure:
    """Environmental poison, independent of weapon poison coatings."""

    def __init__(self, effects, item_flags, item_table, rng):
        self.effects = effects
        self.item_flags = item_flags
        self.item_table = item_table
        self.rng = rng

    def character(self, victim, level, damage, saves, notify):
        if not saves(level // 4 + damage // 20, victim, "DAM_POISON"):
            notify(victim)
            self.effects.affect_join(victim, Effect(
                where="TO_AFFECTS", type="spell.poison", level=level, duration=level // 2,
                location="APPLY_STR", modifier=-1, bitvector="AFF_POISON"))
        # A successful character save does not protect carried consumables.
        for item in victim.owned_items():
            self.object(item, level, damage)

    def room(self, room, level, damage):
        for item in list(room.contents.values()):
            self.object(item, level, damage)

    def object(self, item, level, damage):
        flags = GameApi.flags_to_int(item.extra_flags)
        if (GameApi.is_set(flags, self.item_flags.ITEM_BURN_PROOF.value)
                or GameApi.is_set(flags, self.item_flags.ITEM_BLESS.value)
                or self.rng.number_range(0, 4) == 0):
            return
        chance = exposure_chance(level, damage)
        chance -= int(item.level) * 2
        kind = item_kind(item, self.item_table)
        if kind == "drink_con":
            if int(item.value0) == int(item.value1):
                return
        elif kind != "food":
            return
        if self.rng.number_percent() > max(5, min(95, chance)):
            return
        item.value3 = "1"
