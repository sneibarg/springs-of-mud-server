from typing import Any

from interp.Context import Context


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

        name = (
            getattr(target, "short_description", None)
            or getattr(target, "name", None)
            or "They"
        )
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

    @staticmethod
    def score_ac_phrase(ac_value: int, ac_type: str) -> str:
        if ac_value >= 101:
            return f"hopelessly vulnerable to {ac_type}"
        if ac_value >= 80:
            return f"defenseless against {ac_type}"
        if ac_value >= 60:
            return f"barely protected from {ac_type}"
        if ac_value >= 40:
            return f"slightly armored against {ac_type}"
        if ac_value >= 20:
            return f"somewhat armored against {ac_type}"
        if ac_value >= 0:
            return f"armored against {ac_type}"
        if ac_value >= -20:
            return f"well-armored against {ac_type}"
        if ac_value >= -40:
            return f"very well-armored against {ac_type}"
        if ac_value >= -60:
            return f"heavily armored against {ac_type}"
        if ac_value >= -80:
            return f"superbly armored against {ac_type}"
        if ac_value >= -100:
            return f"almost invulnerable to {ac_type}"
        return f"divinely armored against {ac_type}"

    @staticmethod
    def score_alignment_word(alignment: int) -> str:
        if alignment > 900:
            return "angelic"
        if alignment > 700:
            return "saintly"
        if alignment > 350:
            return "good"
        if alignment > 100:
            return "kind"
        if alignment > -100:
            return "neutral"
        if alignment > -350:
            return "mean"
        if alignment > -700:
            return "evil"
        if alignment > -900:
            return "demonic"
        return "satanic"

    @staticmethod
    def look_register_match(context: Context) -> bool:
        context.count += 1
        return context.count == context.number

    @staticmethod
    def look_keyword_matches(token: str, keyword: str) -> bool:
        t = (token or "").strip().lower()
        k = (keyword or "").strip().lower()
        if not t or not k:
            return False
        words = [w for w in k.split() if w]
        return any(w == t or w.startswith(t) for w in words)