from typing import Tuple

from mobile import Mobile
from mobile.ArmorClass import ArmorClass
from mobile.Dice import Dice
from server.LoggerFactory import LoggerFactory

logger = LoggerFactory.get_logger('MobileUtil')


class MobileUtil:
    pass

    @staticmethod
    def build_mobile(mobile_id: str, races: dict, mobile_data: dict, npc_flag: int) -> tuple[Mobile, int]:
        player_name = str(mobile_data.get("name", "") or "")
        race_name = MobileUtil.resolve_race_name(races, mobile_data.get("race"), player_name)
        race = races[race_name] or {}
        flags = MobileUtil.resolve_mobile_flags(mobile_data, race, npc_flag)
        level = MobileUtil.safe_int(mobile_data.get("level", 0), default=0)
        normalized = MobileUtil.build_normalized_mobile_data(mobile_id, mobile_data, player_name, race_name, flags, level)

        mobile = Mobile.from_json(normalized)
        MobileUtil.apply_extended_mobile_fields(mobile, mobile_data)
        return mobile, level

    @staticmethod
    def resolve_mobile_id(mobile_data: dict, raw_mobile: dict) -> str | None:
        mobile_id = str(mobile_data.get("id") or mobile_data.get("_id") or mobile_data.get("vnum") or "").strip()
        if mobile_id:
            return mobile_id
        logger.error("Skipping mobile with missing id/vnum: " + str(raw_mobile))
        return None

    @staticmethod
    def resolve_mobile_flags(mobile_data: dict, race: dict, npc_flag: int) -> dict[str, int]:
        flags = {
            "act_flags": MobileUtil.safe_int(mobile_data.get("act_flags", 0), default=0) | npc_flag | MobileUtil.race_flag_value(race, "act"),
            "affect_flags": MobileUtil.safe_int(mobile_data.get("affect_flags", 0), default=0) | MobileUtil.race_flag_value(race, "aff"),
            "form": MobileUtil.safe_int(mobile_data.get("form", 0), default=0) | MobileUtil.race_flag_value(race, "form"),
            "parts": MobileUtil.safe_int(mobile_data.get("parts", 0), default=0) | MobileUtil.race_flag_value(race, "parts"),
        }
        MobileUtil.apply_flag_removes(flags, mobile_data.get("flag_removes", []) or [])
        return flags

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
    def normalize_position(enums: dict, value, fallback_key="standing") -> int:
        pos_enum = enums["positions"]
        if isinstance(value, int):
            result = value
        else:
            text = str(value or "").strip()
            if text.isdigit():
                result = int(text)
            elif text:
                result = pos_enum.get(text.lower(), 0)
            else:
                result = 0

        fallback = enums.get(fallback_key.lower(), 8)
        return result if result > 0 else fallback

    @staticmethod
    def resolve_attack(attacks, value):
        if value is None:
            return None
        attack = attacks.get(value)
        if attack is not None:
            return attack.get("message", value)
        return value

    @staticmethod
    def resolve_size(enums, value):
        if value is None:
            return None

        enum_lookup = enums.get("size")
        if isinstance(value, int):
            return value

        text = str(value).strip()
        if text.isdigit():
            return int(text)

        return enum_lookup.get(text.lower())

    @staticmethod
    def parse_dice(mobile_data: dict) -> Tuple[Dice, Dice, Dice]:
        hit_dice = Dice.get_dice(str(mobile_data.get("hit_dice")))
        mana_dice = Dice.get_dice(str(mobile_data.get("mana_dice")))
        damage_dice = Dice.get_dice(str(mobile_data.get("damage_dice")))
        return hit_dice, mana_dice, damage_dice

    @staticmethod
    def parse_ac(mobile_data: dict) -> ArmorClass:
        ac = mobile_data.get("armor_class")
        if ac is None:
            logger.warn(f"AC is None for mobile: {mobile_data}")
            return ArmorClass(bash=0, pierce=0, slash=0, exotic=0)
        return ArmorClass.from_json(mobile_data.get("armor_class"))

    @staticmethod
    def resolve_flag_domain_key(domain: str, domain_map: dict[str, str]) -> str | None:
        for prefix, key in domain_map.items():
            if domain.startswith(prefix):
                return key
        return None
    
    @staticmethod
    def apply_extended_mobile_fields(mobile: Mobile, mobile_data: dict):
        mobile.armor_class = MobileUtil.parse_ac(mobile_data)
        mobile.hit_dice, mobile.mana_dice, mobile.damage_dice = MobileUtil.parse_dice(mobile_data)
        mobile.hitroll = MobileUtil.safe_int(mobile_data.get("hitroll", 0), default=0)
        mobile.wealth = MobileUtil.safe_int(mobile_data.get("wealth", mobile_data.get("gold", 0)), default=0)
    
    @staticmethod
    def build_normalized_mobile_data(mobile_id: str, mobile_data: dict, player_name: str, race_name: str, flags: dict[str, int], level: int) -> dict:
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
            "act_flags": str(flags["act_flags"]),
            "affect_flags": str(flags["affect_flags"]),
            "alignment": str(mobile_data.get("alignment", "0") or "0"),
            "group": str(MobileUtil.safe_int(mobile_data.get("group", 0), default=0)),
            "act": str(mobile_data.get("act", "") or ""),
            "dam_type": str(mobile_data.get("dam_type", "") or ""),
            "combat_flags": None,
            "start_pos": str(start_pos),
            "default_pos": str(default_pos),
            "sex": str(sex_value),
            "form": str(flags["form"]),
            "parts": str(flags["parts"]),
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
    def apply_flag_removes(flags: dict[str, int], removals: list[dict]):
        domain_map = {
            "act": "act_flags",
            "aff": "affect_flags",
            "off": "off_flags",
            "imm": "imm_flags",
            "res": "res_flags",
            "vul": "vuln_flags",
            "for": "form",
            "par": "parts",
        }

        for removal in removals:
            domain = str(removal.get("domain", "")).lower()
            vector = MobileUtil.safe_int(removal.get("vector", 0), default=0)
            key = MobileUtil.resolve_flag_domain_key(domain, domain_map)
            if key is None:
                raise ValueError(f"Flag remove: flag not found: {domain}")
            flags[key] &= ~vector
            