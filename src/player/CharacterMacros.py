from __future__ import annotations

from datetime import datetime
from enum import IntEnum
from threading import RLock
from typing import Any, TYPE_CHECKING, Callable, Optional

from area.Room import Room
from game.GameMacros import GameMacros
from util.GenericUtil import GenericUtil
from game.RandomNumberGenerator import RandomNumberGenerator
from mobile.Mobile import Mobile
from player.Character import Character
from server.LoggerFactory import LoggerFactory


if TYPE_CHECKING:
    from area.RoomHelper import RoomHelper

rng = RandomNumberGenerator()


class CharacterMacros(GameMacros):
    _lock = RLock()
    _configured = False

    _registry_provider: Optional[Callable[[], Any]] = None
    _enums_provider: Optional[Callable[[], dict[str, IntEnum]]] = None
    _attribute_bonuses_provider: Optional[Callable[[], dict[str, dict[str, dict[str, int]]]]] = None
    _pc_races_provider: Optional[Callable[[], dict[str, dict[str, Any]]]] = None
    _titles_provider: Optional[Callable[[], dict[str, dict[str, Any]]]] = None
    _weather_handler_provider: Optional[Callable[[], Any]] = None

    _registry_service = None
    _enums = None
    _attribute_bonuses = None
    _pc_races = None
    _titles = None
    _weather_handler = None
    _logger = None

    def __new__(cls, *args, **kwargs):
        raise RuntimeError(
            "CharacterMacros may not be instantiated. Use CharacterMacros.<method>(...)."
        )

    @classmethod
    def configure(
        cls,
        *,
        registry_provider: Callable[[], Any],
        enums_provider: Callable[[], dict[str, IntEnum]],
        attribute_bonuses_provider: Callable[[], dict[str, dict[str, dict[str, int]]]],
        pc_races_provider: Callable[[], dict[str, dict[str, Any]]],
        titles_provider: Optional[Callable[[], dict[str, dict[str, Any]]]] = None,
        weather_handler_provider: Optional[Callable[[], Any]] = None,
    ) -> None:
        with cls._lock:
            cls._registry_provider = registry_provider
            cls._enums_provider = enums_provider
            cls._attribute_bonuses_provider = attribute_bonuses_provider
            cls._pc_races_provider = pc_races_provider
            cls._titles_provider = titles_provider
            cls._weather_handler_provider = weather_handler_provider
            cls._configured = True

    @classmethod
    def reset_for_tests(cls) -> None:
        with cls._lock:
            cls._configured = False
            cls._registry_provider = None
            cls._enums_provider = None
            cls._attribute_bonuses_provider = None
            cls._pc_races_provider = None
            cls._titles_provider = None
            cls._weather_handler_provider = None
            cls._registry_service = None
            cls._enums = None
            cls._attribute_bonuses = None
            cls._pc_races = None
            cls._titles = None
            cls._weather_handler = None
            cls._logger = None

    @classmethod
    def lazy_load(cls, weather_handler) -> None:
        cls._weather_handler = weather_handler

    @classmethod
    def _require_configured(cls) -> None:
        if not cls._configured:
            raise RuntimeError("CharacterMacros has not been configured.")

    @classmethod
    def _logger_obj(cls):
        if cls._logger is None:
            cls._logger = LoggerFactory.get_logger(__name__)
        return cls._logger

    @classmethod
    def _registry(cls):
        if cls._registry_service is None:
            cls._require_configured()
            if cls._registry_provider is None:
                raise RuntimeError("CharacterMacros registry provider not configured.")
            cls._registry_service = cls._registry_provider()
        return cls._registry_service

    @classmethod
    def _enums_map(cls):
        if cls._enums is None:
            cls._require_configured()
            if cls._enums_provider is None:
                raise RuntimeError("CharacterMacros enums provider not configured.")
            cls._enums = cls._enums_provider()
        return cls._enums

    @classmethod
    def _attribute_bonus_map(cls):
        if cls._attribute_bonuses is None:
            cls._require_configured()
            if cls._attribute_bonuses_provider is None:
                raise RuntimeError("CharacterMacros attribute_bonuses provider not configured.")
            cls._attribute_bonuses = cls._attribute_bonuses_provider()
        return cls._attribute_bonuses

    @classmethod
    def _pc_races_map(cls):
        if cls._pc_races is None:
            cls._require_configured()
            if cls._pc_races_provider is None:
                raise RuntimeError("CharacterMacros pc_races provider not configured.")
            cls._pc_races = cls._pc_races_provider()
        return cls._pc_races

    @classmethod
    def _titles_map(cls):
        if cls._titles is None:
            cls._require_configured()
            if cls._titles_provider is None:
                raise RuntimeError("CharacterMacros titles provider not configured.")
            cls._titles = cls._titles_provider()
        return cls._titles

    @classmethod
    def _weather(cls):
        if cls._weather_handler is None and cls._weather_handler_provider is not None:
            cls._weather_handler = cls._weather_handler_provider()
        return cls._weather_handler

    @classmethod
    def get_trust(cls, char: Any) -> int:
        GameParameters = cls.get_enum("gameParameters")
        if type(char) is Character and char.trust > 0:
            return char.trust
        if cls.is_npc(char) and char.level >= GameParameters.HERO.value:
            return GameParameters.HERO.value - 1
        return char.level

    @classmethod
    def get_attribute_bonus(cls, attr_name: str, attr_level: str):
        bonus_table = cls._attribute_bonus_map().get(attr_name, {})
        if not bonus_table:
            return {}

        normalized = GenericUtil.to_int(attr_level)
        normalized = max(0, min(25, normalized))
        bonus = bonus_table.get(str(normalized))
        if bonus is not None:
            return bonus
        return bonus_table.get(normalized,{})

    @staticmethod
    def is_npc(char: Any) -> bool:
        return type(char) is Mobile

    @classmethod
    def is_immortal(cls, char: Character) -> bool:
        GameParameters = cls.get_enum("gameParameters")
        return GameParameters is not None and cls.get_trust(char) >= GameParameters.LEVEL_IMMORTAL.value

    @classmethod
    def is_trusted(cls, char: Character) -> bool:
        return cls.get_trust(char) >= char.level

    @classmethod
    def is_affected(cls, char: Any, effect) -> bool:
        return cls.is_set(cls.convert_flags(char.status_flags.affected_by), effect)

    @classmethod
    def is_blind(cls, character: Any) -> bool:
        AffectedBits = cls.get_enum("affectedBy")
        if not hasattr(AffectedBits, "AFF_BLIND"):
            return False
        return cls.is_set(
            int(cls.convert_flags(getattr(character.status_flags, "affected_by", "0") or "0")),
            AffectedBits.AFF_BLIND.value,
        )

    @classmethod
    def is_awake(cls, char: Any) -> bool:
        positions = cls.get_enum("positions")
        return cls.position_value(char) > positions.POS_SLEEPING.value

    @staticmethod
    def is_good(char: Any) -> bool:
        if type(char) is Character:
            return char.character_attributes.alignment >= 350
        return char.perm_stat.alignment >= 350

    @staticmethod
    def is_evil(char: Any) -> bool:
        if type(char) is Character:
            return char.character_attributes.alignment <= -350
        return char.perm_stat.alignment <= -350

    @classmethod
    def is_neutral(cls, char: Any) -> bool:
        return not cls.is_good(char) and not cls.is_evil(char)

    @classmethod
    def get_ac(cls, char: Any, ac: int) -> int:
        armor = getattr(char, "armor_class", None)
        if armor is None:
            return 0

        key = ac
        if isinstance(ac, int):
            if ac == 0:
                key = "pierce"
            elif ac == 1:
                key = "bash"
            elif ac == 2:
                key = "slash"
            elif ac == 3:
                key = "exotic"
            else:
                key = "pierce"

        if isinstance(key, str):
            normalized_key = key.lower()
            if normalized_key in ("pierce", "piercing"):
                base = getattr(armor, "piercing", getattr(armor, "pierce", 0))
            elif normalized_key == "bash":
                base = getattr(armor, "bashing", getattr(armor, "bash", 0))
            elif normalized_key == "slash":
                base = getattr(armor, "slashing", getattr(armor, "slash", 0))
            else:
                base = getattr(armor, "magic", getattr(armor, "exotic", 0))
        else:
            base = 0

        dex_value = 0
        if hasattr(char, "character_attributes"):
            dex_value = getattr(char.character_attributes, "dexterity", 0)
        dex_defensive = cls.get_attribute_bonus("dexterity", str(dex_value)).get("defensive", 0)
        return int(base) + int(dex_defensive)

    @classmethod
    def get_hitroll(cls, char: Any) -> int:
        strength = getattr(getattr(char, "character_attributes", None), "strength", 0)
        return int(cls.get_attribute_bonus(attr_name="strength", attr_level=str(strength)).get("tohit", 0))

    @classmethod
    def get_damroll(cls, char: Any) -> int:
        strength = getattr(getattr(char, "character_attributes", None), "strength", 0)
        return int(cls.get_attribute_bonus(attr_name="strength", attr_level=str(strength)).get("todam", 0))

    @classmethod
    def is_outside(cls, char: Any) -> bool:
        room: Room = cls._registry().room_registry.get(id=char.room_id)
        room_flags = cls.get_enum("roomFlags")
        cls._logger_obj().debug(f"is_outside: {room.room_flags}={room_flags.ROOM_INDOORS}")
        return (room.room_flags & room_flags.ROOM_INDOORS) == 0

    @staticmethod
    def get_carry_weight(char: Any) -> int:
        return int(char.character_attributes.max_weight + ((char.silver / 10) + (char.gold * 2 / 5)))

    @staticmethod
    def wait_state(char: Character, npulse: int) -> int:
        return max(char.status_flags.pulse_wait, npulse)

    @staticmethod
    def daze_state(char: Character, npulse: int) -> int:
        return max(char.status_flags.pulse_daze, npulse)

    @staticmethod
    def normalize_help_token(value: str) -> str:
        token = str(value or "").strip().lower()
        return token.strip("~`'\".,;:!?()[]{}<>")

    @classmethod
    def get_act_flags(cls, character: Character) -> int:
        return int(cls.convert_flags(getattr(character.status_flags, "act", "0") or "0"))

    @staticmethod
    def set_act_flags(character: Character, value: int) -> None:
        character.status_flags.act = GameMacros.flags_to_letters(value)

    @classmethod
    def get_comm_flags(cls, character: Character) -> int:
        return int(cls.convert_flags(getattr(character.status_flags, "comm", "0") or "0"))

    @staticmethod
    def set_comm_flags(character: Character, value: int) -> None:
        character.status_flags.comm = GameMacros.flags_to_letters(value)

    @classmethod
    def is_comm_enabled(cls, character: Character, bit_name: str) -> bool:
        comm_bits = cls.get_enum("commFlags")
        if not hasattr(comm_bits, bit_name):
            return False
        comm = cls.get_comm_flags(character)
        return cls.is_set(comm, getattr(comm_bits, bit_name).value)

    @classmethod
    def toggle_player_act(cls, character: Character, bit_name: str, off_text: str, on_text: str) -> str:
        if cls.is_npc(character):
            return ""
        player_act_bits = cls.get_enum("playerActBits")
        if not hasattr(player_act_bits, bit_name):
            return ""
        bit_value = getattr(player_act_bits, bit_name).value
        act = cls.get_act_flags(character)
        if cls.is_set(act, bit_value):
            act = cls.unset_bit(act, bit_value)
            cls.set_act_flags(character, act)
            return off_text
        act = cls.set_bit(act, bit_value)
        cls.set_act_flags(character, act)
        return on_text

    @classmethod
    def toggle_comm(cls, character: Character, bit_name: str, off_text: str, on_text: str) -> str:
        comm_bits = cls.get_enum("commFlags")
        bit_value = getattr(comm_bits, bit_name).value
        comm = cls.get_comm_flags(character)
        if cls.is_set(comm, bit_value):
            comm = cls.unset_bit(comm, bit_value)
            cls.set_comm_flags(character, comm)
            return off_text
        comm = cls.set_bit(comm, bit_value)
        cls.set_comm_flags(character, comm)
        return on_text

    @classmethod
    def format_affects(cls, character: Character) -> str:
        affected_bits = cls.get_enum("affectedBy")
        raw = int(cls.convert_flags(getattr(character.status_flags, "affected_by", "") or ""))
        lines = []
        for name, member in affected_bits.__members__.items():
            if cls.is_set(raw, member.value):
                pretty = name.replace("AFF_", "").replace("_", " ").lower()
                lines.append(f"Spell: {pretty}\r\n")
        if not lines:
            return "You are not affected by any spells.\r\n"
        return "You are affected by the following spells:\r\n" + "".join(lines)

    @classmethod
    def target_equipment_lines(cls, target: Any, equip_slot_labels: list[tuple[str, str]]) -> list[str]:
        from util.ItemUtil import ItemUtil

        item_flags = cls._enums_map().get("itemFlags")
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
                from object.Item import Item
                obj = Item.from_json(obj)

            item_text = ItemUtil.format_obj_to_char(obj, item_flags_enum=item_flags, f_short=True)
            lines.append(f"{label}{item_text}")

        return lines

    @classmethod
    def who_line(cls, viewer: Character, target: Character) -> str:
        trust = GenericUtil.to_int(cls.get_trust(viewer), 0)
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

        params = cls.get_enum("gameParameters")
        if hasattr(params, "MAX_LEVEL"):
            max_level = params.MAX_LEVEL.value
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

        return f"[{target.level}    {target.race}    {class_name.capitalize()}]{flag_text} {target.name} {target.title}"

    @staticmethod
    def owned_items(character: Character) -> list:
        seen = set()
        items = []
        for item in list(getattr(character, "loot", []) or []):
            item_id = id(item)
            if item is not None and item_id not in seen:
                items.append(item)
                seen.add(item_id)
        equipped = getattr(character, "equipped", None)
        for item in getattr(equipped, "__dict__", {}).values() if equipped is not None else []:
            item_id = id(item)
            if item is not None and item_id not in seen:
                items.append(item)
                seen.add(item_id)
        return items

    @staticmethod
    def find_owned_item(character: Character, wanted: str):
        key = (wanted or "").strip().lower()
        if not key:
            return None
        for item in CharacterMacros.owned_items(character):
            name = (getattr(item, "name", "") or "").lower()
            if name == key or name.startswith(key):
                return item
        return None

    @staticmethod
    def find_comparable_equipped_item(character: Character, source_item):
        src_type = str(getattr(source_item, "item_type", "") or "").strip().lower()
        equipped = getattr(character, "equipped", None)
        for slot_item in getattr(equipped, "__dict__", {}).values() if equipped is not None else []:
            if slot_item is None or slot_item == source_item:
                continue
            item_type = str(getattr(slot_item, "item_type", "") or "").strip().lower()
            if item_type == src_type:
                return slot_item
        return None

    @staticmethod
    def compare_value(item) -> int | None:
        item_type = str(getattr(item, "item_type", "") or "").strip().lower()
        if "weapon" in item_type:
            dam_min = GenericUtil.to_int(getattr(item, "value1", 0), 0)
            dam_max = GenericUtil.to_int(getattr(item, "value2", 0), 0)
            return (dam_min + dam_max) // 2
        if "armor" in item_type:
            return GenericUtil.to_int(getattr(item, "value0", 0), 0)
        return None

    @staticmethod
    def skill_value_for_class(values: dict, class_name: str, default: int = 0) -> int:
        if not isinstance(values, dict):
            return default
        if class_name in values:
            return GenericUtil.to_int(values.get(class_name), default)
        class_lower = class_name.lower()
        for key, value in values.items():
            if str(key).lower() == class_lower:
                return GenericUtil.to_int(value, default)
        return default

    @classmethod
    def title_for_level(cls, character: Character, level: int | None = None) -> str:
        try:
            titles = cls._titles_map()
        except Exception:
            return str(getattr(character, "title", "") or "")

        class_name = str(getattr(getattr(character, "character_class", None), "name", "") or "").strip().lower()
        if not class_name:
            return str(getattr(character, "title", "") or "")

        class_titles = titles.get(class_name, {})
        title_row = class_titles.get(str(GenericUtil.to_int(level if level is not None else getattr(character, "level", 0), 0)), {})
        if not isinstance(title_row, dict):
            return str(getattr(character, "title", "") or "")

        sex = str(getattr(character, "sex", "") or "").strip().lower()
        sex_key = "female" if sex in ("2", "f", "female") else "male"
        title = str(title_row.get(sex_key, title_row.get("male", title_row.get("female", ""))) or "").strip()
        if not title:
            return str(getattr(character, "title", "") or "")
        return f"the {title}"

    @classmethod
    def score_position_line(cls, attributes: Any) -> str:
        position_value = GenericUtil.to_int(getattr(attributes, "position", 0), 0)
        positions = cls.get_enum("positions")
        pos_dead = positions.POS_DEAD.value if positions and hasattr(positions, "POS_DEAD") else -1
        pos_mortal = positions.POS_MORTAL.value if positions and hasattr(positions, "POS_MORTAL") else -1
        pos_incap = positions.POS_INCAP.value if positions and hasattr(positions, "POS_INCAP") else -1
        pos_stunned = positions.POS_STUNNED.value if positions and hasattr(positions, "POS_STUNNED") else -1
        pos_sleeping = positions.POS_SLEEPING.value if positions and hasattr(positions, "POS_SLEEPING") else -1
        pos_resting = positions.POS_RESTING.value if positions and hasattr(positions, "POS_RESTING") else -1
        pos_sitting = positions.POS_SITTING.value if positions and hasattr(positions, "POS_SITTING") else -1
        pos_fighting = positions.POS_FIGHTING.value if positions and hasattr(positions, "POS_FIGHTING") else -1
        if position_value == pos_dead:
            return "You are DEAD!!"
        if position_value == pos_mortal:
            return "You are mortally wounded."
        if position_value == pos_incap:
            return "You are incapacitated."
        if position_value == pos_stunned:
            return "You are stunned."
        if position_value == pos_sleeping:
            return "You are sleeping."
        if position_value == pos_resting:
            return "You are resting."
        if position_value == pos_sitting:
            return "You are sitting."
        if position_value == pos_fighting:
            return "You are fighting."
        return "You are standing."

    @staticmethod
    def find_playing_character(name: str, session_handler):
        wanted = (name or "").strip().lower()
        if not wanted:
            return None
        for session in session_handler.get_playing_sessions():
            ch = session.character
            if ch is None:
                continue
            n = (ch.name or "").lower()
            if n == wanted or n.startswith(wanted):
                return ch
        return None

    @staticmethod
    def restore_character(victim: Character):
        victim.hit = int(getattr(victim, "max_hit", 0))
        victim.mana = int(getattr(victim, "max_mana", 0))
        victim.movement = int(getattr(victim, "max_movement", 0))

    @staticmethod
    def find_character_world(arg: str, character_registry, name_matches_fn, allow_self: bool = False):
        q = (arg or "").strip().lower()
        if not q:
            return None
        if not allow_self and q == "self":
            return None
        for ch in character_registry.all_characters():
            if name_matches_fn(q, getattr(ch, "name", "")):
                return ch
        return None

    @classmethod
    def find_location(cls, arg: str, room_registry, character_registry, name_matches_fn):
        value = (arg or "").strip()
        if value.isdigit():
            room = room_registry.get_or_none(vnum=value)
            if room is not None:
                return room

        victim = cls.find_character_world(value, character_registry, name_matches_fn, allow_self=False)
        if victim is not None:
            return room_registry.get_or_none(id=victim.room_id)

        q = value.lower()
        for room in room_registry.all_rooms():
            if room is None:
                continue
            for mob in room.mobiles.values():
                mob_name = f"{getattr(mob, 'name', '')} {getattr(mob, 'short_description', '')}".strip()
                if name_matches_fn(q, mob_name):
                    return room

        for room in room_registry.all_rooms():
            if room is None:
                continue
            if name_matches_fn(value, getattr(room, "name", "")):
                return room
        return None

    @classmethod
    def wiz_toggle_comm_on_target(cls, context: Any, argument: str, bit_name: str, label: str, comm_flags, find_character_world_fn):
        victim = find_character_world_fn((argument or "").strip())
        if victim is None:
            context.finish()
            return {"to_char": f"{label.lower()} whom?\r\n"}

        bit = cls.enum_bit(comm_flags, bit_name)
        if bit == 0:
            context.finish()
            return {"to_char": "This feature is unavailable.\r\n"}

        raw = GenericUtil.to_int(cls.convert_flags(getattr(victim.status_flags, "comm", "") or "0"), 0)
        if cls.is_set(raw, bit):
            raw = cls.unset_bit(raw, bit)
            cls.set_comm_flags(victim, raw)
            context.finish()
            return {"to_char": f"{label} removed.\r\n", "victim": victim, "to_victim": "The gods have restored your privileges.\r\n"}

        raw = cls.set_bit(raw, bit)
        cls.set_comm_flags(victim, raw)
        context.finish()
        return {"to_char": f"{label} set.\r\n", "victim": victim, "to_victim": "The gods have revoked your privileges.\r\n"}

    @staticmethod
    def channel_payload(character: Character,
                        context: Any,
                        off_flag: str,
                        verb: str,
                        on_msg: str,
                        off_msg: str,
                        comm_flags,
                        session_handler,
                        parse_argument_fn,
                        has_comm_fn,
                        set_comm_fn):
        text = parse_argument_fn(context.result, context.parameters)
        if not text:
            is_off = has_comm_fn(character, comm_flags, off_flag)
            set_comm_fn(character, comm_flags, off_flag, not is_off)
            context.finish()
            return {"to_char": on_msg if is_off else off_msg}

        if has_comm_fn(character, comm_flags, "COMM_QUIET"):
            context.finish()
            return {"to_char": "You must turn off quiet mode first.\r\n"}
        if has_comm_fn(character, comm_flags, "COMM_NOCHANNELS"):
            context.finish()
            return {"to_char": "The gods have revoked your channel privileges.\r\n"}

        set_comm_fn(character, comm_flags, off_flag, False)
        channel_map = {
            "gossip": "COMM_NOGOSSIP",
            "auction": "COMM_NOAUCTION",
            "music": "COMM_NOMUSIC",
            "question": "COMM_NOQUESTION",
            "quote": "COMM_NOQUOTE",
            "grats": "COMM_NOGRATS",
        }
        targets = []
        for session in session_handler.get_playing_sessions():
            victim = session.character
            if victim is None or victim.id == character.id:
                continue
            if has_comm_fn(victim, comm_flags, "COMM_QUIET"):
                continue
            if has_comm_fn(victim, comm_flags, channel_map[verb]):
                continue
            targets.append(victim)

        context.finish()
        return {
            "to_char": f"You {verb} '{text}'\r\n",
            "global_message": f"{character.name} {verb}s '{text}'\r\n",
            "global_targets": targets,
        }

    @classmethod
    def wiz_do_mload(cls, context: Any, vnum_text: str, mobile_registry, room_registry):
        from util.MobileUtil import MobileUtil

        vnum = (vnum_text or "").strip()
        proto = mobile_registry.get_or_none(vnum=vnum)
        if proto is None:
            context.finish()
            return {"to_char": "No mobile has that vnum.\r\n"}

        mob = MobileUtil.create_mobile(proto, cls._enums_map(), cls)
        room = room_registry.get_or_none(id=context.character.room_id)
        if room is not None:
            room.add_mobile_to_room(mob)
        context.finish()
        return {"to_char": "Mobile loaded.\r\n"}

    @staticmethod
    def wiz_do_oload(context: Any, vnum_text: str, item_registry, room_registry):
        from util.ItemUtil import ItemUtil

        vnum = (vnum_text or "").strip()
        proto = item_registry.get_or_none(vnum=vnum)
        if proto is None:
            context.finish()
            return {"to_char": "No object has that vnum.\r\n"}

        obj = ItemUtil.create_object(proto)
        room = room_registry.get_or_none(id=context.character.room_id)
        if room is not None:
            room.add_item_to_room(obj)
        context.finish()
        return {"to_char": "Object loaded.\r\n"}

    @classmethod
    def is_affected_by_name(cls, character: Character, affected_bits, bit_name: str) -> bool:
        if affected_bits is None or not hasattr(affected_bits, bit_name):
            return False
        bit = getattr(affected_bits, bit_name).value
        return cls.is_set(
            GenericUtil.to_int(cls.convert_flags(getattr(character.status_flags, "affected_by", "")), 0),
            bit,
        )

    @classmethod
    def set_affected_by_name(cls, character: Character, affected_bits, bit_name: str, enabled: bool):
        if affected_bits is None or not hasattr(affected_bits, bit_name):
            return
        bit = getattr(affected_bits, bit_name).value
        raw = GenericUtil.to_int(cls.convert_flags(getattr(character.status_flags, "affected_by", "")), 0)
        raw = cls.set_bit(raw, bit) if enabled else cls.unset_bit(raw, bit)
        character.status_flags.affected_by = GameMacros.flags_to_letters(raw)

    @classmethod
    def pos_value(cls, name: str) -> int:
        positions = cls.get_enum("positions")
        if not hasattr(positions, name):
            return -1
        return int(getattr(positions, name).value)

    @classmethod
    def position_value(cls, character: Character) -> int:
        attrs = getattr(character, "character_attributes", None)
        raw = getattr(attrs, "position", None)
        if raw is None:
            raw = getattr(character, "position", None)
        if isinstance(raw, str):
            name = raw.strip().upper()
            if name and not name.startswith("POS_"):
                name = f"POS_{name}"
            positions = cls.get_enum("positions")
            if hasattr(positions, name):
                return int(getattr(positions, name).value)
        standing = cls.pos_value("POS_STANDING")
        default_pos = standing if standing >= 0 else 0
        return GenericUtil.to_int(raw, default_pos)

    @classmethod
    def movement_position_block_message(cls, character: Character) -> str:
        pos = cls.position_value(character)
        if pos == cls.pos_value("POS_DEAD"):
            return "Lie still; you are DEAD.\r\n"
        if pos in (cls.pos_value("POS_MORTAL"), cls.pos_value("POS_INCAP")):
            return "You are hurt far too bad for that.\r\n"
        if pos == cls.pos_value("POS_STUNNED"):
            return "You are too stunned to do that.\r\n"
        if pos == cls.pos_value("POS_SLEEPING"):
            return "In your dreams, or what?\r\n"
        if pos == cls.pos_value("POS_RESTING"):
            return "Nah... You feel too relaxed...\r\n"
        if pos == cls.pos_value("POS_SITTING"):
            return "Better stand up first.\r\n"
        if pos == cls.pos_value("POS_FIGHTING"):
            return "No way! You are still fighting!\r\n"
        return ""

    @classmethod
    def set_position(cls, character: Character, pos_name: str):
        positions = cls.get_enum("positions")
        if not hasattr(positions, pos_name):
            return
        value = int(getattr(positions, pos_name).value)
        attrs = getattr(character, "character_attributes", None)
        if attrs is not None:
            attrs.position = value
        setattr(character, "position", value)

    @staticmethod
    def mirror_exit_flag(room_registry, room, ex, rev_dir_map, find_exit_fn, set_mask: int = 0, clear_mask: int = 0):
        to_room = room_registry.get_or_none(id=getattr(ex, "to_room_id", None))
        if to_room is None:
            return
        rev = rev_dir_map[int(getattr(ex, "direction", 0))]
        rev_exit = find_exit_fn(to_room, rev)
        if rev_exit is None or getattr(rev_exit, "to_room_id", None) != room.id:
            return
        flags = GenericUtil.to_int(getattr(rev_exit, "exit_flags", 0), 0)
        if clear_mask:
            flags &= ~clear_mask
        if set_mask:
            flags |= set_mask
        rev_exit.exit_flags = flags

    @classmethod
    def has_holy_light(cls, character) -> bool:
        player_bits = cls.get_enum("playerActBits")
        if not hasattr(player_bits, "PLR_HOLYLIGHT"):
            return False
        return cls.is_set(
            int(cls.convert_flags(character.status_flags.act)),
            player_bits.PLR_HOLYLIGHT.value,
        )

    @classmethod
    def can_see(cls, character: Any, victim: Any, room_helper: RoomHelper) -> bool:
        if character == victim:
            return True

        if cls.get_trust(character) < victim.status_flags.invis_level:
            return False

        if cls.get_trust(character) < victim.status_flags.incog_level and character.room_id != victim.room_id:
            return False

        if ((not cls.is_npc(character) and cls.has_holy_light(character))
                or (cls.is_npc(character) and cls.is_immortal(character))):
            return True

        affected_bits = cls.get_enum("affectedBy")
        if cls.is_affected(character, affected_bits.AFF_BLIND.value):
            return False

        if type(character) is Character and room_helper.is_room_dark(character.room_id) and not cls.is_affected(character, affected_bits.AFF_INFRARED.value):
            return False

        if cls.is_affected(victim, affected_bits.AFF_INVISIBLE.value) and not cls.is_affected(character, affected_bits.AFF_DETECT_INVIS.value):
            return False

        if cls.is_affected(victim, affected_bits.AFF_SNEAK.value) \
                and not cls.is_affected(character, affected_bits.AFF_DETECT_HIDDEN.value) \
                and victim.fighting is None:
            pass

        weather = cls._weather()
        time_enum = cls.get_enum("timeAndWeather")
        if weather.weather_info.sunlight == time_enum.SUN_SET.value \
                or weather.weather_info.sunlight == time_enum.SUN_DARK.value:
            return True

        chance = 0
        if rng.number_percent() < chance:
            return False
        return True

    @classmethod
    def mobile_has_act(cls, mob: Any, act_bits, name: str) -> bool:
        bit = cls.enum_bit(act_bits, name)
        if bit == 0:
            return False
        flags = GenericUtil.to_int(getattr(getattr(mob, "status_flags", None), "act", 0), 0)
        return (flags & bit) != 0

    @classmethod
    def mobile_is_charmed(cls, mob: Any) -> bool:
        charm = cls.enum_bit(cls.get_enum("affectedBy"), "AFF_CHARM")
        if charm == 0:
            return False
        flags = GenericUtil.to_int(getattr(getattr(mob, "status_flags", None), "affected_by", 0), 0)
        return (flags & charm) != 0

    @classmethod
    def mobile_is_standing(cls, mob: Any) -> bool:
        standing = cls.enum_bit(cls.get_enum("positions"), "POS_STANDING")
        current = GenericUtil.to_int(getattr(mob, "position", getattr(mob, "start_pos", standing)), standing)
        return current == standing

    @classmethod
    def item_takeable(cls, obj: Any, wear_flags_enum) -> bool:
        take_bit = cls.enum_bit(wear_flags_enum, "ITEM_TAKE")
        if take_bit == 0:
            return False
        wear_flags = GameMacros.flags_to_int(getattr(obj, "wear_flags", 0))
        return (wear_flags & take_bit) != 0

    @classmethod
    def get_enum(cls, enum_name: str) -> IntEnum:
        return cls._enums_map()[enum_name]

    @classmethod
    def get_max_train(cls, character: Character, stat_index: int, current_value: int) -> int:
        race_obj = getattr(character, "character_race", None)
        race_fields = (
            "max_strength",
            "max_intelligence",
            "max_wisdom",
            "max_dexterity",
            "max_constitution",
        )
        if race_obj is not None and 0 <= stat_index < len(race_fields):
            value = GenericUtil.to_int(getattr(race_obj, race_fields[stat_index], 0), 0)
            if value > 0:
                return value

        race_name = str(getattr(character, "race", "") or "").strip().lower()
        race_data = cls._pc_races_map().get(race_name, {})
        max_stats = race_data.get("max_stats", [])
        if isinstance(max_stats, list) and 0 <= stat_index < len(max_stats):
            return GenericUtil.to_int(max_stats[stat_index], current_value)
        return current_value

    @classmethod
    def mobile_will_assist(cls, char: Mobile) -> bool:
        if type(char) is not Mobile:
            return False
        OffenseTypes = cls.get_enum("offenseTypes")
        return cls.is_set(OffenseTypes.ASSIST_PLAYERS.value, char.status_flags.off)

    @classmethod
    def player_auto_assist(cls, char: Mobile) -> bool:
        if type(char) is not Mobile:
            return False
        PlayerActBits = cls.get_enum("playerActBits")
        return cls.is_set(PlayerActBits.PLR_AUTOASSIST.value, char.status_flags.off)

    @classmethod
    def will_npc_assist(self, rch: Mobile, ch: Character) -> bool | str | Any | Any:
        if not CharacterMacros.is_npc(rch):
            return False

        OffenseTypes = self.get_enum("offenseTypes")
        off = rch.status_flags.off
        return (
                CharacterMacros.is_set(off, OffenseTypes.ASSIST_ALL.value) or
                (rch.group and rch.group == ch.group) or
                (rch.race == ch.race and CharacterMacros.is_set(off, OffenseTypes.ASSIST_RACE.value)) or
                (CharacterMacros.is_set(off, OffenseTypes.ASSIST_ALIGN.value) and
                 CharacterMacros.same_alignment(rch, ch)) or
                (rch.vnum == ch.vnum and CharacterMacros.is_set(off, OffenseTypes.ASSIST_VNUM.value))
        )

    @classmethod
    def is_same_group(cls, ach: Any, bch: Any) -> bool:
        if ach is None or bch is None:
            return False
        if ach.leader is not None:
            ach = ach.leader
        if bch.leader is not None:
            bch = bch.leader
        return ach == bch
