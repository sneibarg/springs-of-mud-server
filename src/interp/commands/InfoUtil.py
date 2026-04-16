from typing import Any


class InfoUtil:
    @staticmethod
    def target_condition_line(target: Any) -> str:
        hit = getattr(target, "hit")
        max_hit = getattr(target, "max_hit")
        try:
            hit = int(hit)
            max_hit = int(max_hit)
        except (TypeError, ValueError):
            hit, max_hit = 0, 0

        if max_hit > 0:
            percent = (100 * hit) // max_hit
        else:
            percent = -1

        name = (getattr(target, "name", None) or "They")
        if percent >= 100:
            return f"{name} is in excellent condition."
        if percent >= 90:
            return f"{name} has a few scratches."
        if percent >= 75:
            return f"{name} has some small wounds and bruises."
        if percent >= 50:
            return f"{name} has quite a few wounds."
        if percent >= 30:
            return f"{name} has some big nasty wounds and scratches."
        if percent >= 15:
            return f"{name} looks pretty hurt."
        if percent >= 0:
            return f"{name} is in awful condition."
        return f"{name} is bleeding to death."

    @staticmethod
    def find_inventory_item_for_slot(target: Any, slot: str):
        from game.Equipped import WEAR_LOC_TO_EQUIPPED_SLOT
        wanted_locs = [loc for loc, slot_name in WEAR_LOC_TO_EQUIPPED_SLOT.items() if slot_name == slot]
        if not wanted_locs:
            return None
        inventory = getattr(target, "inventory", None) or []
        for item in inventory:
            try:
                wear_loc = int(getattr(item, "wear_loc", -1))
            except (TypeError, ValueError):
                wear_loc = -1
            if wear_loc in wanted_locs:
                return item
        return None
