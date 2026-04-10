import json
from enum import IntEnum
from typing import Tuple

from game.GameMacros import GameMacros
from mobile.Mobile import Mobile
from mobile.ArmorClass import ArmorClass
from mobile.Dice import Dice
from mobile.MobileFlags import MobileFlags
from object.ObjectMacros import ObjectMacros
from server.LoggerFactory import LoggerFactory

logger = LoggerFactory.get_logger('MobileUtil')


class MobileUtil:
    pass

    @staticmethod
    def build_mobile(mobile_id: str, races: dict, mobile_data: dict, npc_flag: int, enums: dict[str, type[IntEnum]]) -> tuple[Mobile, int]:
        player_name = str(mobile_data.get("name", "") or "")
        race_name = MobileUtil.resolve_race_name(races, mobile_data.get("race"), player_name)
        race = races[race_name] or {}
        flag_letters = enums.get("flagLetters")
        flags = MobileUtil.resolve_mobile_flags(mobile_data, race, npc_flag, flag_letters)
        level = MobileUtil.safe_int(mobile_data.get("level", 0), default=0)
        normalized = MobileUtil.build_normalized_mobile_data(mobile_id, mobile_data, player_name, race_name, level)

        mobile = Mobile.from_json(normalized)
        mobile.flags = flags
        MobileUtil.apply_extended_mobile_fields(mobile, mobile_data)
        return mobile, level

    @staticmethod
    def convert_form(race: str, form: int, object_macros: ObjectMacros):
        return object_macros.set_bit(form, object_macros.races[race].get(form, 0))

    @staticmethod
    def convert_parts(race: str, parts: int, object_macros: ObjectMacros):
        return object_macros.set_bit(parts, object_macros.races[race].get(parts, 0))

    @staticmethod
    def resolve_mobile_id(mobile_data: dict, raw_mobile: dict) -> str | None:
        mobile_id = str(mobile_data.get("id") or mobile_data.get("_id") or mobile_data.get("vnum") or "").strip()
        if mobile_id:
            return mobile_id
        logger.error("Skipping mobile with missing id/vnum: " + str(raw_mobile))
        return None

    @staticmethod
    def resolve_mobile_flags(mobile_data: dict, race: dict, npc_flag: int, flag_letters: type[IntEnum]) -> MobileFlags:
        raw_act = MobileUtil.safe_int(mobile_data.get("actFlags") or mobile_data.get("act_flags"), 0)
        raw_aff = MobileUtil.safe_int(mobile_data.get("affectFlags") or mobile_data.get("affect_flags"), 0)
        combat_raw = MobileUtil.parse_combat_flags(mobile_data.get("combat_flags"))
        raw_off = MobileUtil.resolve_combat_flag(
            mobile_data, combat_raw, "off_flags", "offFlags", flag_letters
        )
        raw_imm = MobileUtil.resolve_combat_flag(
            mobile_data, combat_raw, "imm_flags", "immFlags", flag_letters
        )
        raw_res = MobileUtil.resolve_combat_flag(
            mobile_data, combat_raw, "res_flags", "resFlags", flag_letters
        )
        raw_vuln = MobileUtil.resolve_combat_flag(
            mobile_data, combat_raw, "vuln_flags", "vulnFlags", flag_letters
        )

        raw_form = MobileUtil.safe_int(mobile_data.get("form"), 0)
        raw_parts = MobileUtil.safe_int(mobile_data.get("parts"), 0)
        race_act = MobileUtil.race_flag_value(race, "act")
        race_aff = MobileUtil.race_flag_value(race, "aff")
        race_off = MobileUtil.race_flag_value(race, "off")
        race_imm = MobileUtil.race_flag_value(race, "imm")
        race_res = MobileUtil.race_flag_value(race, "res")
        race_vuln = MobileUtil.race_flag_value(race, "vuln")
        race_form = MobileUtil.race_flag_value(race, "form")
        race_parts = MobileUtil.race_flag_value(race, "parts")
        mobile_flags = MobileFlags(
            act=raw_act | npc_flag | race_act,
            affect=raw_aff | race_aff,
            off=raw_off | race_off,
            imm=raw_imm | race_imm,
            res=raw_res | race_res,
            vuln=raw_vuln | race_vuln,
            form=raw_form | race_form,
            parts=raw_parts | race_parts,
        )
        MobileUtil.apply_flag_removes(mobile_flags, mobile_data.get("flag_removes", []))
        return mobile_flags

    @staticmethod
    def parse_combat_flags(value) -> dict:
        if isinstance(value, dict):
            return value
        text = str(value or "").strip()
        if not text:
            return {}
        try:
            parsed = json.loads(text.replace("'", '"'))
            return parsed if isinstance(parsed, dict) else {}
        except json.JSONDecodeError:
            return {}

    @staticmethod
    def resolve_combat_flag(mobile_data: dict, combat_raw: dict, snake_key: str, camel_key: str, flag_letters: type[IntEnum]) -> int:
        value = combat_raw.get(snake_key, combat_raw.get(camel_key))
        if value in (None, ""):
            value = mobile_data.get(snake_key, mobile_data.get(camel_key))
        if isinstance(value, str):
            return GameMacros.parse_flag_string(value, flag_letters)
        return MobileUtil.safe_int(value, default=0)

    @staticmethod
    def increment_kill_table(kill_table: dict[int, int], level: int):
        level_bucket = max(0, min(level, 100))
        kill_table[level_bucket] = kill_table.get(level_bucket, 0) + 1

    @staticmethod
    def resolve_npc_flag(game_data) -> int:
        for domain in ("act", "mob", "mobile", "mob_act"):
            for flag_name in ("ACT_IS_NPC", "IS_NPC"):
                try:
                    return game_data.flag_value(domain, flag_name)
                except KeyError:
                    pass
        logger.warning("ACT_IS_NPC not found in GameData; defaulting to 1.")
        return 1

    @staticmethod
    def resolve_race_name(races, explicit_race, player_name: str) -> str:
        candidates = []
        if explicit_race is not None:
            candidates.append(str(explicit_race).strip().lower())
        if player_name:
            first = player_name.strip().split()[0].lower()
            if first:
                candidates.append(first)
        candidates.append("human")

        for candidate in candidates:
            if candidate in races:
                race = races[candidate]
                race_id = race.get("id")
                if race_id:
                    return str(race_id)
                name = race.get("name")
                if name:
                    return str(name).lower()
                return candidate
        return "human"

    @staticmethod
    def race_flag_value(race: dict, key: str) -> int:
        if not race:
            return 0
        value = race.get(key, 0)
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def parse_dice(mobile_data: dict) -> Tuple[Dice, Dice, Dice]:
        hit_dice = Dice.from_json(str(mobile_data.get("hit_dice")))
        mana_dice = Dice.from_json(str(mobile_data.get("mana_dice")))
        damage_dice = Dice.from_json(str(mobile_data.get("damage_dice")))
        return hit_dice, mana_dice, damage_dice

    @staticmethod
    def parse_ac(mobile_data: dict) -> ArmorClass:
        ac = mobile_data.get("armor_class")
        if ac is None:
            logger.warn("AC is None for mobile: {mobile_data")
            return ArmorClass(bash=0, pierce=0, slash=0, exotic=0)
        return ArmorClass.from_json(mobile_data.get("armor_class"))

    @staticmethod
    def apply_extended_mobile_fields(mobile: Mobile, mobile_data: dict):
        mobile.armor_class = MobileUtil.parse_ac(mobile_data)
        mobile.hit_dice, mobile.mana_dice, mobile.damage_dice = MobileUtil.parse_dice(mobile_data)
        mobile.hitroll = MobileUtil.safe_int(mobile_data.get("hitroll", 0), default=0)
        mobile.wealth = MobileUtil.safe_int(mobile_data.get("wealth", mobile_data.get("gold", 0)), default=0)
    
    @staticmethod
    def build_normalized_mobile_data(mobile_id: str, mobile_data: dict, player_name: str, race_name: str, level: int) -> dict:
        start_pos = mobile_data.get("start_pos")
        default_pos = mobile_data.get("default_pos")
        sex_value = mobile_data.get("sex")
        return {
            "area_id": str(mobile_data.get("area_id", "") or ""),
            "vnum": str(mobile_data.get("vnum", mobile_id) or mobile_id),
            "name": player_name,
            "short_description": str(mobile_data.get("short_description", "") or ""),
            "long_description": MobileUtil.capitalize_first(mobile_data.get("long_description", "")),
            "description": MobileUtil.capitalize_first(mobile_data.get("description", "")),
            "race": race_name,
            "act_flags": None,  # str(flags["act_flags"]),
            "affect_flags": None,  # str(flags["affect_flags"]),
            "alignment": str(mobile_data.get("alignment", "0") or "0"),
            "group": str(MobileUtil.safe_int(mobile_data.get("group", 0), default=0)),
            "act": str(mobile_data.get("act", "") or ""),
            "dam_type": str(mobile_data.get("dam_type", "") or ""),
            "combat_flags": str(mobile_data.get("combat_flags", "") or ""),
            "start_pos": str(start_pos),
            "default_pos": str(default_pos),
            "sex": str(sex_value),
            "form": None,
            "parts": None,
            "size": str(mobile_data.get("size", "") or ""),
            "material": str(mobile_data.get("material", "") or ""),
            "flags": str(mobile_data.get("flags", "") or ""),
            "id": mobile_id,
            "level": level,
            "hit_roll": MobileUtil.safe_int(mobile_data.get("hit_roll", 0), default=0),
            "hit_dice": None,
            "mana_dice": None,
            "damage_dice": None,
            "armor_class": None,
            "gold": MobileUtil.safe_int(mobile_data.get("gold", 0), default=0),
            "silver": MobileUtil.safe_int(mobile_data.get("silver", 0), default=0),
            "pulse_wait": MobileUtil.safe_int(mobile_data.get("pulse_wait", 0), default=0),
            "pulse_daze": MobileUtil.safe_int(mobile_data.get("pulse_daze", 0), default=0),
            "mobile_flags": None,
            "lock": mobile_data.get("lock"),
        }
    
    @staticmethod
    def capitalize_first(value) -> str:
        text = str(value or "")
        return text[:1].upper() + text[1:] if text else ""

    @staticmethod
    def safe_int(value, default=0) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def apply_flag_removes(flags: MobileFlags, removals: list):
        for removal in removals:
            domain = str(removal.get("domain", "")).lower().strip()
            vector = MobileUtil.safe_int(removal.get("vector", 0))
            if domain == "act":
                flags.act &= ~vector
            elif domain.startswith("aff"):
                flags.affect &= ~vector
            elif domain == "off":
                flags.off &= ~vector
            elif domain == "imm":
                flags.imm &= ~vector
            elif domain == "res":
                flags.res &= ~vector
            elif domain.startswith("vul"):
                flags.vuln &= ~vector
            elif domain.startswith("for"):
                flags.form &= ~vector
            elif domain.startswith("par"):
                flags.parts &= ~vector
