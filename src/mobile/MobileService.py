import asyncio
import requests

from injector import inject
from game import GameData
from mobile.Mobile import Mobile
from server.LoggerFactory import LoggerFactory
from server.ServerUtil import ServerUtil
from server.ServiceConfig import ServiceConfig
from registry import RegistryService
from event import EventHandler
from area import AreaService


class MobileService:
    POS_SLEEPING = 4
    POS_STANDING = 8

    @inject
    def __init__(self, config: ServiceConfig, game_data: GameData, registry: RegistryService, area_service: AreaService, event_handler: EventHandler):
        self.__name__ = "MobileService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry = registry
        self.game_data = game_data
        self.mobiles_endpoint = config.mobiles_endpoint
        self.area_service = area_service
        self.event_handler = event_handler
        self.task = None
        self.stop_flag = False
        self.all_mobiles = {}
        self.kill_table: dict[int, int] = {}
        self.load_mobiles()
        self.logger.info("Initialized MobileService instance with a total of "+str(len(self.all_mobiles))+" mobiles in memory.")

    async def start(self):
        initial_spawn = False
        while not self.stop_flag:
            if not initial_spawn:
                for room_id in self.area_service.rooms:
                    room = self.area_service.rooms[room_id]

    def return_mobile_by_id(self, mobile_id):
        return self.all_mobiles[mobile_id]

    def start_task(self):
        self.task = asyncio.create_task(self.start())

    def load_mobiles(self) -> dict[str, Mobile]:
        """
        REST-backed equivalent of ROM db2.c load_mobiles.

        Expected behavior mirrored from db2.c:
        - duplicate mobile rejection by vnum/id
        - capitalize long_description and description
        - act_flags = persisted act_flags | ACT_IS_NPC | race.act
        - affect_flags = persisted affect_flags | race.aff
        - merge race off/imm/res/vuln/form/parts
        - allow explicit flag removals from optional REST fields
        - normalize start/default position
        - track kill_table by level bucket
        """
        loaded: dict[str, Mobile] = {}
        kill_table: dict[int, int] = {}
        npc_flag = self._resolve_npc_flag()
        payload = self._get_mobiles()
        for raw_mobile in payload:
            mobile_data = ServerUtil.camel_to_snake_case(raw_mobile)
            mobile_id = self._resolve_mobile_id(mobile_data, raw_mobile)
            if mobile_id is None:
                continue

            if mobile_id in loaded:
                raise ValueError(f"Load_mobiles: vnum/id {mobile_id} duplicated.")

            mobile, level = self._build_mobile(mobile_id, mobile_data, npc_flag)
            loaded[mobile_id] = mobile
            self._increment_kill_table(kill_table, level)

        self.all_mobiles = loaded
        self.kill_table = kill_table
        return self.all_mobiles

    def _build_mobile(self, mobile_id: str, mobile_data: dict, npc_flag: int) -> tuple[Mobile, int]:
        player_name = str(mobile_data.get("name", "") or "")
        race_name = self._resolve_race_name(mobile_data.get("race"), player_name)
        race = self.game_data.get_race(race_name) or {}

        flags = self._resolve_mobile_flags(mobile_data, race, npc_flag)
        level = self._safe_int(mobile_data.get("level", 0), default=0)
        normalized = self._build_normalized_mobile_data(mobile_id, mobile_data, player_name, race_name, flags, level)

        mobile = Mobile.from_json(normalized)
        self._apply_extended_mobile_fields(mobile, mobile_data, flags)
        return mobile, level

    def _resolve_mobile_id(self, mobile_data: dict, raw_mobile: dict) -> str | None:
        mobile_id = str(mobile_data.get("id") or mobile_data.get("_id") or mobile_data.get("vnum") or "").strip()
        if mobile_id:
            return mobile_id
        self.logger.error("Skipping mobile with missing id/vnum: " + str(raw_mobile))
        return None

    def _resolve_mobile_flags(self, mobile_data: dict, race: dict, npc_flag: int) -> dict[str, int]:
        flags = {
            "act_flags": self._safe_int(mobile_data.get("act_flags", 0), default=0) | npc_flag | self._race_flag_value(race, "act"),
            "affect_flags": self._safe_int(mobile_data.get("affect_flags", 0), default=0) | self._race_flag_value(race, "aff"),
            "off_flags": self._safe_int(mobile_data.get("off_flags", 0), default=0) | self._race_flag_value(race, "off"),
            "imm_flags": self._safe_int(mobile_data.get("imm_flags", 0), default=0) | self._race_flag_value(race, "imm"),
            "res_flags": self._safe_int(mobile_data.get("res_flags", 0), default=0) | self._race_flag_value(race, "res"),
            "vuln_flags": self._safe_int(mobile_data.get("vuln_flags", 0), default=0) | self._race_flag_value(race, "vuln"),
            "form": self._safe_int(mobile_data.get("form", 0), default=0) | self._race_flag_value(race, "form"),
            "parts": self._safe_int(mobile_data.get("parts", 0), default=0) | self._race_flag_value(race, "parts"),
        }
        self._apply_flag_removes(flags, mobile_data.get("flag_removes", []) or [])
        return flags

    def _apply_flag_removes(self, flags: dict[str, int], removals: list[dict]):
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
            vector = self._safe_int(removal.get("vector", 0), default=0)
            key = self._resolve_flag_domain_key(domain, domain_map)
            if key is None:
                raise ValueError(f"Flag remove: flag not found: {domain}")
            flags[key] &= ~vector

    @staticmethod
    def _resolve_flag_domain_key(domain: str, domain_map: dict[str, str]) -> str | None:
        for prefix, key in domain_map.items():
            if domain.startswith(prefix):
                return key
        return None

    def _build_normalized_mobile_data(self, mobile_id: str, mobile_data: dict, player_name: str, race_name: str, flags: dict[str, int], level: int) -> dict:
        start_pos = self._normalize_position(mobile_data.get("start_pos"), fallback_key="standing")
        default_pos = self._normalize_position(mobile_data.get("default_pos"), fallback_key="standing")
        sex_value = self._normalize_enum_value("sex", mobile_data.get("sex"), fallback=0)

        return {
            "area_id": str(mobile_data.get("area_id", "") or ""),
            "vnum": str(mobile_data.get("vnum", mobile_id) or mobile_id),
            "name": player_name,
            "short_description": str(mobile_data.get("short_description", "") or ""),
            "long_description": self._capitalize_first(mobile_data.get("long_description", "")),
            "description": self._capitalize_first(mobile_data.get("description", "")),
            "race": race_name,
            "act_flags": str(flags["act_flags"]),
            "affect_flags": str(flags["affect_flags"]),
            "alignment": str(mobile_data.get("alignment", "0") or "0"),
            "group": str(self._safe_int(mobile_data.get("group", 0), default=0)),
            "dam_type": str(mobile_data.get("dam_type", "") or ""),
            "off_flags": str(flags["off_flags"]),
            "imm_flags": str(flags["imm_flags"]),
            "res_flags": str(flags["res_flags"]),
            "vuln_flags": str(flags["vuln_flags"]),
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
            "hit_roll": self._safe_int(mobile_data.get("hit_roll", 0), default=0),
            "hit_dice_number": 0,
            "hit_dice_type": 0,
            "hit_dice_bonus": 0,
            "mana_dice_number": 0,
            "mana_dice_type": 0,
            "mana_dice_bonus": 0,
            "damage_dice_number": 0,
            "damage_dice_type": 0,
            "damage_dice_bonus": 0,
            "ac_pierce": 0,
            "ac_bash": 0,
            "ac_slash": 0,
            "ac_exotic": 0,
            "gold": self._safe_int(mobile_data.get("gold", 0), default=0),
            "lock": mobile_data.get("lock"),
        }

    def _apply_extended_mobile_fields(self, mobile: Mobile, mobile_data: dict, flags: dict[str, int]):
        # Parse dice notation and set individual fields
        hit_dice = self._parse_dice(mobile_data.get("hit") or mobile_data.get("hit_dice"))
        mobile.hit_dice_number = hit_dice["number"]
        mobile.hit_dice_type = hit_dice["type"]
        mobile.hit_dice_bonus = hit_dice["bonus"]

        mana_dice = self._parse_dice(mobile_data.get("mana") or mobile_data.get("mana_dice"))
        mobile.mana_dice_number = mana_dice["number"]
        mobile.mana_dice_type = mana_dice["type"]
        mobile.mana_dice_bonus = mana_dice["bonus"]

        damage_dice = self._parse_dice(mobile_data.get("damage") or mobile_data.get("damage_dice"))
        mobile.damage_dice_number = damage_dice["number"]
        mobile.damage_dice_type = damage_dice["type"]
        mobile.damage_dice_bonus = damage_dice["bonus"]

        # Parse AC values
        ac_data = self._parse_ac(mobile_data)
        mobile.ac_pierce = ac_data["pierce"]
        mobile.ac_bash = ac_data["bash"]
        mobile.ac_slash = ac_data["slash"]
        mobile.ac_exotic = ac_data["exotic"]

        # Set other extended fields that might not be in the dataclass
        mobile.hitroll = self._safe_int(mobile_data.get("hitroll", 0), default=0)
        mobile.hit = hit_dice  # Keep for backwards compatibility
        mobile.mana = mana_dice  # Keep for backwards compatibility
        mobile.damage = damage_dice  # Keep for backwards compatibility
        mobile.ac = ac_data  # Keep for backwards compatibility
        mobile.wealth = self._safe_int(mobile_data.get("wealth", mobile_data.get("gold", 0)), default=0)

        # Resolve attack type if provided
        dam_type_value = self._resolve_attack(mobile_data.get("dam_type") or mobile_data.get("damage_type"))
        if dam_type_value:
            mobile.dam_type = str(dam_type_value)

        # Resolve size if provided
        size_value = self._resolve_size(mobile_data.get("size"))
        if size_value:
            mobile.size = str(size_value)

    @staticmethod
    def _increment_kill_table(kill_table: dict[int, int], level: int):
        level_bucket = max(0, min(level, 100))
        kill_table[level_bucket] = kill_table.get(level_bucket, 0) + 1

    def _resolve_npc_flag(self) -> int:
        for domain in ("act", "mob", "mobile", "mob_act"):
            for flag_name in ("ACT_IS_NPC", "IS_NPC"):
                try:
                    return self.game_data.flag_value(domain, flag_name)
                except KeyError:
                    pass
        self.logger.warning("ACT_IS_NPC not found in GameData; defaulting to 1.")
        return 1

    def _resolve_race_name(self, explicit_race, player_name: str) -> str:
        candidates = []
        if explicit_race is not None:
            candidates.append(str(explicit_race).strip().lower())
        if player_name:
            first = player_name.strip().split()[0].lower()
            if first:
                candidates.append(first)
        candidates.append("human")

        for candidate in candidates:
            race = self.game_data.get_race(candidate)
            if race is not None:
                race_id = race.get("id")
                if race_id:
                    return str(race_id)
                name = race.get("name")
                if name:
                    return str(name).lower()
                return candidate
        return "human"

    @staticmethod
    def _race_flag_value(race: dict, key: str) -> int:
        if not race:
            return 0
        value = race.get(key, 0)
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _capitalize_first(value) -> str:
        text = str(value or "")
        return text[:1].upper() + text[1:] if text else ""

    @staticmethod
    def _safe_int(value, default=0) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def _normalize_position(self, value, fallback_key="standing") -> int:
        enum_list = self.game_data.enums.get("position", [])
        if isinstance(value, int):
            result = value
        else:
            text = str(value or "").strip()
            if text.isdigit():
                result = int(text)
            elif text:
                try:
                    result = next(i for i, v in enumerate(enum_list) if str(v).lower() == text.lower())
                except StopIteration:
                    result = 0
            else:
                result = 0

        try:
            fallback = next(i for i, v in enumerate(enum_list) if str(v).lower() == fallback_key.lower())
        except StopIteration:
            fallback = 8

        return result if result > 0 else fallback

    def _normalize_enum_value(self, enum_name: str, value, fallback=0) -> int:
        enum_map = self.game_data.enums.get(enum_name, {})
        if isinstance(value, int):
            return value
        text = str(value or "").strip()
        if text.isdigit():
            return int(text)
        if text:
            return enum_map.get(text.lower(), enum_map.get(text.upper(), fallback))
        return fallback

    def _resolve_attack(self, value):
        if value is None:
            return None
        attack = self.game_data.get_attack(str(value).strip().lower())
        if attack is not None:
            return attack.get("id", value)
        return value

    def _resolve_size(self, value):
        if value is None:
            return None

        enum_list = self.game_data.enums.get("size", [])
        if isinstance(value, int):
            return value

        text = str(value).strip()
        if text.isdigit():
            return int(text)

        text_lower = text.lower()
        for i, v in enumerate(enum_list):
            if str(v).lower() == text_lower:
                return i

        return None

    def _get_mobiles(self):
        try:
            return requests.get(self.mobiles_endpoint).json()
        except Exception as e:
            self.logger.error("Failed to load mobiles: " + str(e))
            self.all_mobiles = {}
            self.kill_table = {}
            return self.all_mobiles

    @staticmethod
    def _parse_dice(value):
        """
        Accepts values like:
          '3d8+12'
          {'number': 3, 'type': 8, 'bonus': 12}
          [3, 8, 12]
        """
        if value is None:
            return {"number": 0, "type": 0, "bonus": 0}

        if isinstance(value, dict):
            return {"number": int(value.get("number", 0)), "type": int(value.get("type", 0)), "bonus": int(value.get("bonus", 0))}

        if isinstance(value, (list, tuple)) and len(value) >= 3:
            return {"number": int(value[0]), "type": int(value[1]), "bonus": int(value[2])}

        text = str(value).strip().lower()
        if "d" in text:
            left, right = text.split("d", 1)
            if "+" in right:
                die_type, bonus = right.split("+", 1)
            else:
                die_type, bonus = right, "0"
            return {"number": int(left or 0), "type": int(die_type or 0), "bonus": int(bonus or 0)}
        return {"number": 0, "type": 0, "bonus": 0}

    @staticmethod
    def _parse_ac(mobile_data: dict) -> dict:
        """
        db2.c multiplies each AC component by 10 when loading from file.
        """
        if "ac" in mobile_data and isinstance(mobile_data["ac"], dict):
            return {
                "pierce": int(mobile_data["ac"].get("pierce", 0)),
                "bash": int(mobile_data["ac"].get("bash", 0)),
                "slash": int(mobile_data["ac"].get("slash", 0)),
                "exotic": int(mobile_data["ac"].get("exotic", 0)),
            }

        return {
            "pierce": int(mobile_data.get("ac_pierce", 0)),
            "bash": int(mobile_data.get("ac_bash", 0)),
            "slash": int(mobile_data.get("ac_slash", 0)),
            "exotic": int(mobile_data.get("ac_exotic", 0)),
        }
