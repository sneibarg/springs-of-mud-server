from typing import Any

from api.CharacterApi import CharacterApi
from interp.Context import Context
from player.Character import Character
from util.GenericUtil import GenericUtil


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

    @staticmethod
    def who_line(viewer: Character, target: Character) -> str:
        trust = GenericUtil.to_int(CharacterApi.get_trust(viewer), 0)
        incog_level = GenericUtil.to_int(getattr(target.status_flags, "incog_level", 0), 0)
        invis_level = GenericUtil.to_int(getattr(target.status_flags, "invis_level", 0), 0)

        flags = []
        if 0 < incog_level <= trust:
            flags.append("(Incog)")
        if 0 < invis_level <= trust:
            flags.append("(Wizi)")

        flag_text = (" " + " ".join(flags)) if flags else ""
        class_name = getattr(getattr(target, "character_class", None), "name", "") or ""
        class_name = class_name[0:3]
        max_level = CharacterApi.get_enum("gameParameters").MAX_LEVEL.value
        if target.level == max_level:
            class_name = "IMP"
        elif target.level == max_level - 1:
            class_name = "CRE"
        elif target.level == max_level - 2:
            class_name = "SUP"
        elif target.level == max_level - 3:
            class_name = "DEI"
        elif target.level == max_level - 4:
            class_name = "GOD"
        elif target.level == max_level - 5:
            class_name = "IMM"
        elif target.level == max_level - 6:
            class_name = "DEM"
        elif target.level == max_level - 7:
            class_name = "ANG"
        elif target.level == max_level - 8:
            class_name = "AVA"
        else:
            class_name = class_name.capitalize()

        return f"[{target.level}    {target.race}    {class_name}]{flag_text} {target.name} {target.title}"
    
    @staticmethod
    def score_position_line(attributes: Any) -> str:
        position_value = GenericUtil.to_int(getattr(attributes, "position", 0), 0)
        positions = CharacterApi.get_enum("positions")
        if position_value == positions.POS_DEAD.value:
            return "You are DEAD!!"
        if position_value == positions.POS_MORTAL.value:
            return "You are mortally wounded."
        if position_value == positions.POS_INCAP.value:
            return "You are incapacitated."
        if position_value == positions.POS_STUNNED.value:
            return "You are stunned."
        if position_value == positions.POS_SLEEPING.value:
            return "You are sleeping."
        if position_value == positions.POS_RESTING.value:
            return "You are resting."
        if position_value == positions.POS_SITTING.value:
            return "You are sitting."
        if position_value == positions.POS_FIGHTING.value:
            return "You are fighting."
        return "You are standing."

    @staticmethod
    def target_equipment_lines(target: Any, equip_slot_labels: list[tuple[str, str]]) -> list[str]:
        from util.ItemUtil import ItemUtil
        item_flags = CharacterApi.get_enum("itemFlags")
        lines: list[str] = []
        equipped = getattr(target, "equipped", None)
        for slot, label in equip_slot_labels:
            obj = None
            if equipped is not None:
                obj = equipped.get(slot) if isinstance(equipped, dict) else getattr(equipped, slot, None)

            if obj is None:
                for item in list(getattr(target, "loot", []) or []):
                    wear_location = str(getattr(item, "wear_location", "") or "").strip().lower()
                    if wear_location == slot:
                        obj = item
                        break

            if obj is None:
                continue

            if isinstance(obj, dict):
                from item.Item import Item
                obj = Item.from_json(obj)

            item_text = ItemUtil.format_obj_to_char(obj, item_flags_enum=item_flags, f_short=True)
            lines.append(f"{label}{item_text}")

        return lines
