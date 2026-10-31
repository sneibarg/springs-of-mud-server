from item.Item import Item
from typing import Any

from api.CharacterApi import CharacterApi
from api.ItemApi import ItemApi
from util.LookupUtil import LookupUtil
from player.Character import Character
from util.GenericUtil import GenericUtil


class InfoUtil:
    """Presentation helpers shared by information commands and combat output."""

    @staticmethod
    def target_condition_line(target: Any) -> str:
        hit = target.hit
        max_hit = target.max_hit
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
            or target.name
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
    def who_line(viewer: Character, target: Character) -> str:
        trust = GenericUtil.to_int(CharacterApi.get_trust(viewer), 0)
        incog_level = GenericUtil.to_int(target.status_flags.incog_level, 0)
        invis_level = GenericUtil.to_int(target.status_flags.invis_level, 0)

        flags = []
        if 0 < incog_level <= trust:
            flags.append("(Incog)")
        if 0 < invis_level <= trust:
            flags.append("(Wizi)")

        flag_text = (" " + " ".join(flags)) if flags else ""
        class_name = target.character_class.name or ""
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
    def target_equipment_lines(target: Any, equip_slot_labels: list[tuple[str, str]], *, observer=None, room=None) -> list[str]:
        item_flags = CharacterApi.get_enum("itemFlags")
        lines: list[str] = []
        equipped = target.equipped
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
                obj = Item.from_json(obj)

            if observer is not None and not ItemApi.can_see_object(room, observer, obj):
                continue

            item_text = Item.format_obj_to_char(obj, item_flags_enum=item_flags, f_short=True)
            lines.append(f"{label}{item_text}")

        return lines

    @staticmethod
    def visible_inventory_lines(owner, observer, room) -> list[str]:
        """ROM's short inventory list: visible unworn roots, optionally combined by text."""
        return InfoUtil.visible_item_lines(
            (item for item in owner.owned_items() if not LookupUtil.worn(owner, item)), observer, room)

    @staticmethod
    def visible_item_lines(items, observer, room) -> list[str]:
        """Render a visible, unworn item list using the observer's combine setting."""
        flags = CharacterApi.get_enum('itemFlags')
        combine = CharacterApi.is_npc(observer) or CharacterApi.is_comm_enabled(observer, 'COMM_COMBINE')
        rows = []
        counts = {}
        for item in items:
            if (GenericUtil.to_int(getattr(item, 'wear_loc', -1), -1) != -1
                    or not ItemApi.can_see_object(room, observer, item)):
                continue
            text = Item.format_obj_to_char(item, item_flags_enum=flags, f_short=True)
            if combine and text in counts:
                counts[text] += 1
            else:
                rows.append(text)
                counts[text] = 1
        if not rows:
            return [('     ' if combine else '') + 'Nothing.']
        return [(f'({counts[text]:2d}) ' if counts[text] > 1 else '     ') + text
                if combine else text for text in rows]
