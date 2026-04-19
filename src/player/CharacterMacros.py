from datetime import datetime
from enum import IntEnum
from typing import Any, TYPE_CHECKING

from area.Room import Room
from game.GameMacros import GameMacros
from game.GenericUtil import GenericUtil
from game.RandomNumberGenerator import RandomNumberGenerator
from mobile.Mobile import Mobile
from player.Character import Character
from server.LoggerFactory import LoggerFactory


if TYPE_CHECKING:
    from area.RoomHelper import RoomHelper

rng = RandomNumberGenerator()


class CharacterMacros(GameMacros):
    def __init__(self,
                 registry_service,
                 character_constants,
                 enums: dict[str, IntEnum],
                 attribute_bonuses: dict[str, dict[str, dict[str, int]]]):
        self.__name__ = "CharacterMacros"
        self.registry_service = registry_service
        self.enums = enums
        self.character_constants = character_constants
        self.weather_handler = None
        self.RoomFlagsEnum = self.enums.get("roomFlags")
        self.PlayerActBits = self.enums.get("playerActBits")
        self.AffectedBits = self.enums.get('affectedBy')
        self.TimeAndWeatherEnum = enums.get('timeAndWeather')
        self.PositionsEnum = enums.get('positions')
        self.GameParametersEnum = enums.get('gameParameters')
        self.attribute_bonuses = attribute_bonuses
        self.logger = LoggerFactory.get_logger(__name__)

    def lazy_load(self, weather_handler):
        self.weather_handler = weather_handler

    def get_trust(self, char: Any) -> int:
        if type(char) is Character and char.trust > 0:
            return char.trust
        if self.is_npc(char) and char.level >= self.character_constants.immortal_levels.get("LEVEL_HERO"):
            return self.character_constants.immortal_levels.get("LEVEL_HERO") - 1
        else:
            return char.level

    def get_attribute_bonus(self, attr_name: str, attr_level: str):
        bonus_table = self.attribute_bonuses.get(attr_name, {})
        if not bonus_table:
            return {}

        normalized = GenericUtil.to_int(attr_level)
        normalized = max(0, min(25, normalized))
        bonus = bonus_table.get(str(normalized))
        if bonus is not None:
            return bonus
        return bonus_table.get(normalized, {})

    def is_immortal_sufficient(self, level: int, immortal_name: str) -> bool:
        return level >= self.character_constants.immortal_levels.get(immortal_name)

    # let's deprecate ACT_IS_NPC
    @staticmethod
    def is_npc(char: Any) -> bool:
        return True if type(char) is Mobile else False

    def is_immortal(self, char: Character) -> bool:
        return self.get_trust(char) >= self.GameParametersEnum.LEVEL_IMMORTAL.value

    def is_hero(self, char: Character) -> bool:
        return self.get_trust(char) >= self.GameParametersEnum.LEVEL_HERO.value

    def is_trusted(self, char: Character) -> bool:
        return self.get_trust(char) >= char.level

    def is_affected(self, char: Any, effect) -> bool:
        if type(char) is Character:
            return self.is_set(self.convert_flags(char.character_flags.affected_by), effect)
        else:
            return self.is_set(self.convert_flags(char.mobile_flags.affected_by), effect)

    def is_blind(self, character: Any) -> bool:
        return self.is_set(int(self.convert_flags(character.character_flags.act)), self.AffectedBits.AFF_BLIND.value)

    def is_awake(self, char: Any) -> bool:
        return char.character_attributes.position > self.character_constants.positions.POS_SLEEPING.value

    @staticmethod
    def get_age(char: Character) -> int:
        return int(17 + (char.played + datetime.now().timestamp() - char.logon) / 72000)

    @staticmethod
    def is_good(char: Any) -> bool:
        if type(char) is Character:
            return char.character_attributes.alignment >= 350
        else:
            return char.perm_stat.alignment >= 350

    @staticmethod
    def is_evil(char: Any) -> bool:
        if type(char) is Character:
            return char.character_attributes.alignment <= -350
        else:
            return char.perm_stat.alignment <= -350

    def is_neutral(self, char: Any) -> bool:
        return not self.is_good(char) and not self.is_evil(char)

    def get_ac(self, char: Any, ac: int) -> int:
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
        dex_defensive = self.get_attribute_bonus("dexterity", str(dex_value)).get("defensive", 0)
        return int(base) + int(dex_defensive)

    def get_hitroll(self, char: Any) -> int:
        strength = getattr(getattr(char, "character_attributes", None), "strength", 0)
        return int(self.get_attribute_bonus(attr_name="strength", attr_level=str(strength)).get('tohit', 0))

    def get_damroll(self, char: Any) -> int:
        strength = getattr(getattr(char, "character_attributes", None), "strength", 0)
        return int(self.get_attribute_bonus(attr_name="strength", attr_level=str(strength)).get('todam', 0))

    def is_outside(self, char: Any) -> bool:
        room: Room = self.registry_service.room_registry.get(id=char.room_id)
        self.logger.debug(f"is_outside: {room.room_flags}={self.RoomFlagsEnum.ROOM_INDOORS}")
        return (room.room_flags & self.RoomFlagsEnum.ROOM_INDOORS) == 0

    @staticmethod
    def get_carry_weight(char: Any) -> int:
        return int(char.character_attributes.max_weight + ((char.silver / 10) + (char.gold * 2 / 5)))

    @staticmethod
    def wait_state(char: Character, npulse: int) -> int:
        return max(char.temporal_mechanics.pulse_wait, npulse)

    @staticmethod
    def daze_state(char: Character, npulse: int) -> int:
        return max(char.temporal_mechanics.pulse_daze, npulse)

    @staticmethod
    def normalize_help_token(value: str) -> str:
        token = str(value or "").strip().lower()
        return token.strip("~`'\".,;:!?()[]{}<>")

    def get_act_flags(self, character: Character) -> int:
        return int(self.convert_flags(getattr(character.character_flags, "act", "0") or "0"))

    @staticmethod
    def set_act_flags(character: Character, value: int) -> None:
        character.character_flags.act = GenericUtil.flags_to_letters(value)

    def get_comm_flags(self, character: Character) -> int:
        return int(self.convert_flags(getattr(character.character_flags, "comm", "0") or "0"))

    @staticmethod
    def set_comm_flags(character: Character, value: int) -> None:
        character.character_flags.comm = GenericUtil.flags_to_letters(value)

    def is_comm_enabled(self, character: Character, bit_name: str) -> bool:
        comm_bits = self.enums.get("commFlags")
        if comm_bits is None or not hasattr(comm_bits, bit_name):
            return False
        comm = self.get_comm_flags(character)
        return self.is_set(comm, getattr(comm_bits, bit_name).value)

    def toggle_player_act(self, character: Character, player_act_bits, bit_name: str, off_text: str, on_text: str) -> str:
        if self.is_npc(character):
            return ""
        if player_act_bits is None or not hasattr(player_act_bits, bit_name):
            return ""
        bit_value = getattr(player_act_bits, bit_name).value
        act = self.get_act_flags(character)
        if self.is_set(act, bit_value):
            act = self.unset_bit(act, bit_value)
            self.set_act_flags(character, act)
            return off_text
        act = self.set_bit(act, bit_value)
        self.set_act_flags(character, act)
        return on_text

    def toggle_comm(self, character: Character, bit_name: str, off_text: str, on_text: str) -> str:
        comm_bits = self.enums.get("commFlags")
        if comm_bits is None or not hasattr(comm_bits, bit_name):
            return ""
        bit_value = getattr(comm_bits, bit_name).value
        comm = self.get_comm_flags(character)
        if self.is_set(comm, bit_value):
            comm = self.unset_bit(comm, bit_value)
            self.set_comm_flags(character, comm)
            return off_text
        comm = self.set_bit(comm, bit_value)
        self.set_comm_flags(character, comm)
        return on_text

    def format_affects(self, character: Character) -> str:
        affected_bits = self.AffectedBits
        if affected_bits is None:
            return "You are not affected by any spells.\r\n"
        raw = int(self.convert_flags(getattr(character.character_flags, "affected_by", "") or ""))
        lines = []
        for name, member in affected_bits.__members__.items():
            if self.is_set(raw, member.value):
                pretty = name.replace("AFF_", "").replace("_", " ").lower()
                lines.append(f"Spell: {pretty}\r\n")
        if not lines:
            return "You are not affected by any spells.\r\n"
        return "You are affected by the following spells:\r\n" + "".join(lines)

    def target_equipment_lines(self, target: Any, equip_slot_labels: list[tuple[str, str]]) -> list[str]:
        from object.ItemUtil import ItemUtil

        item_flags = self.enums.get("itemFlags")
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

            item_text = ItemUtil.format_obj_to_char(obj, item_flags_enum=item_flags, f_short=True)
            lines.append(f"{label}{item_text}")

        return lines

    def who_line(self, viewer: Character, target: Character) -> str:
        trust = GenericUtil.to_int(self.get_trust(viewer), 0)
        incog_level = GenericUtil.to_int(getattr(target, "incog_level", 0), 0)
        invis_level = GenericUtil.to_int(getattr(target, "invis_level", 0), 0)

        flags = []
        if 0 < incog_level <= trust:
            flags.append("(Incog)")
        if 0 < invis_level <= trust:
            flags.append("(Wizi)")

        flag_text = (" " + " ".join(flags)) if flags else ""
        class_name = getattr(getattr(target, "character_class", None), "name", "") or ""
        return f"[{target.level}    {target.race}    {class_name}]{flag_text} {target.name} {target.title}"

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

    def score_position_line(self, attributes: Any) -> str:
        position_value = GenericUtil.to_int(getattr(attributes, "position", 0), 0)
        positions = self.PositionsEnum
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
    def room_targets(character: Character, room):
        if room is None:
            return []
        return [ch for ch in room.characters.values() if ch.id != character.id]

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
    def find_character_in_room(room, arg: str, name_matches_fn):
        if room is None:
            return None
        q = (arg or "").strip().lower()
        for ch in room.characters.values():
            if name_matches_fn(q, getattr(ch, "name", "")):
                return ch
        return None

    @staticmethod
    def find_item_in_room(room, arg: str, name_matches_fn):
        if room is None:
            return None
        q = (arg or "").strip().lower()
        for item in room.contents.values():
            if name_matches_fn(q, getattr(item, "name", "")):
                return item
        return None

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

    def find_location(self, arg: str, room_registry, character_registry, name_matches_fn):
        value = (arg or "").strip()
        if value.isdigit():
            room = room_registry.get_or_none(vnum=value)
            if room is not None:
                return room

        victim = self.find_character_world(value, character_registry, name_matches_fn, allow_self=False)
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

    @staticmethod
    def enum_bit(enum_obj, name: str) -> int:
        if enum_obj is None or not hasattr(enum_obj, name):
            return 0
        return int(getattr(enum_obj, name).value)

    @staticmethod
    def enum_names(enum_obj, prefix: str) -> list[str]:
        if enum_obj is None:
            return []
        names = []
        for field in dir(enum_obj):
            if field.startswith(prefix):
                names.append(field)
        return sorted(names)

    def wiz_toggle_comm_on_target(self, context: Any, argument: str, bit_name: str, label: str, comm_flags, find_character_world_fn):
        victim = find_character_world_fn((argument or "").strip())
        if victim is None:
            context.finish()
            return {"to_char": f"{label.lower()} whom?\r\n"}

        bit = self.enum_bit(comm_flags, bit_name)
        if bit == 0:
            context.finish()
            return {"to_char": "This feature is unavailable.\r\n"}

        raw = GenericUtil.to_int(self.convert_flags(getattr(victim.character_flags, "comm", "") or "0"), 0)
        if self.is_set(raw, bit):
            raw = self.unset_bit(raw, bit)
            self.set_comm_flags(victim, raw)
            context.finish()
            return {"to_char": f"{label} removed.\r\n", "victim": victim, "to_victim": "The gods have restored your privileges.\r\n"}

        raw = self.set_bit(raw, bit)
        self.set_comm_flags(victim, raw)
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
            return {"to_char": "The gods have revoked your channel priviliges.\r\n"}

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

    def wiz_do_mload(self, context: Any, vnum_text: str, mobile_registry, room_registry):
        from mobile.MobileUtil import MobileUtil

        vnum = (vnum_text or "").strip()
        proto = mobile_registry.get_or_none(vnum=vnum)
        if proto is None:
            context.finish()
            return {"to_char": "No mobile has that vnum.\r\n"}

        mob = MobileUtil.create_mobile(proto, self.enums, self)
        room = room_registry.get_or_none(id=context.character.room_id)
        if room is not None:
            room.add_mobile_to_room(mob)
        context.finish()
        return {"to_char": "Mobile loaded.\r\n"}

    @staticmethod
    def wiz_do_oload(context: Any, vnum_text: str, item_registry, room_registry):
        from object.ItemUtil import ItemUtil

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

    @staticmethod
    def has_boat(character: Character) -> bool:
        for item in list(getattr(character, "loot", []) or []):
            item_type = str(getattr(item, "item_type", "") or "").lower()
            if "boat" in item_type:
                return True
        return False

    def is_affected_by_name(self, character: Character, affected_bits, bit_name: str) -> bool:
        if affected_bits is None or not hasattr(affected_bits, bit_name):
            return False
        bit = getattr(affected_bits, bit_name).value
        return self.is_set(
            GenericUtil.to_int(self.convert_flags(getattr(character.character_flags, "affected_by", "")), 0),
            bit,
        )

    def set_affected_by_name(self, character: Character, affected_bits, bit_name: str, enabled: bool):
        if affected_bits is None or not hasattr(affected_bits, bit_name):
            return
        bit = getattr(affected_bits, bit_name).value
        raw = GenericUtil.to_int(self.convert_flags(getattr(character.character_flags, "affected_by", "")), 0)
        raw = self.set_bit(raw, bit) if enabled else self.unset_bit(raw, bit)
        character.character_flags.affected_by = GenericUtil.flags_to_letters(raw)

    def pos_value(self, name: str) -> int:
        if self.PositionsEnum is None or not hasattr(self.PositionsEnum, name):
            return -1
        return int(getattr(self.PositionsEnum, name).value)

    def position_value(self, character: Character) -> int:
        attrs = getattr(character, "character_attributes", None)
        raw = getattr(attrs, "position", None)
        if raw is None:
            raw = getattr(character, "position", None)
        if isinstance(raw, str):
            name = raw.strip().upper()
            if name and not name.startswith("POS_"):
                name = f"POS_{name}"
            if self.PositionsEnum is not None and hasattr(self.PositionsEnum, name):
                return int(getattr(self.PositionsEnum, name).value)
        standing = self.pos_value("POS_STANDING")
        default_pos = standing if standing >= 0 else 0
        return GenericUtil.to_int(raw, default_pos)

    def movement_position_block_message(self, character: Character) -> str:
        pos = self.position_value(character)
        if pos == self.pos_value("POS_DEAD"):
            return "Lie still; you are DEAD.\r\n"
        if pos in (self.pos_value("POS_MORTAL"), self.pos_value("POS_INCAP")):
            return "You are hurt far too bad for that.\r\n"
        if pos == self.pos_value("POS_STUNNED"):
            return "You are too stunned to do that.\r\n"
        if pos == self.pos_value("POS_SLEEPING"):
            return "In your dreams, or what?\r\n"
        if pos == self.pos_value("POS_RESTING"):
            return "Nah... You feel too relaxed...\r\n"
        if pos == self.pos_value("POS_SITTING"):
            return "Better stand up first.\r\n"
        if pos == self.pos_value("POS_FIGHTING"):
            return "No way! You are still fighting!\r\n"
        return ""

    def set_position(self, character: Character, pos_name: str):
        if self.PositionsEnum is None or not hasattr(self.PositionsEnum, pos_name):
            return
        value = int(getattr(self.PositionsEnum, pos_name).value)
        attrs = getattr(character, "character_attributes", None)
        if attrs is not None:
            attrs.position = value
        setattr(character, "position", value)

    @staticmethod
    def is_room_private(room, room_flags) -> bool:
        if room is None:
            return False
        private = GenericUtil.to_int(getattr(getattr(room_flags, "ROOM_PRIVATE", None), "value", 0), 0)
        solitary = GenericUtil.to_int(getattr(getattr(room_flags, "ROOM_SOLITARY", None), "value", 0), 0)
        flags = GenericUtil.to_int(getattr(room, "room_flags", 0), 0)
        if private and (flags & private) and len(getattr(room, "characters", {})) >= 2:
            return True
        if solitary and (flags & solitary) and len(getattr(room, "characters", {})) >= 1:
            return True
        return False

    @staticmethod
    def is_air_room(room, sector_types) -> bool:
        if room is None or sector_types is None:
            return False
        air = getattr(sector_types, "SECT_AIR", None)
        return air is not None and GenericUtil.to_int(getattr(room, "sector_type", 0), 0) == int(air.value)

    @staticmethod
    def requires_boat(room, sector_types) -> bool:
        if room is None or sector_types is None:
            return False
        no_swim = getattr(sector_types, "SECT_WATER_NOSWIM", None)
        return no_swim is not None and GenericUtil.to_int(getattr(room, "sector_type", 0), 0) == int(no_swim.value)

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

    def act(self, act_format: str, char: Any, arg1: str, arg2: str, act_type: int):
        pass

    def has_holy_light(self, character) -> bool:
        return self.is_set(int(self.convert_flags(character.character_flags.act)), self.PlayerActBits.PLR_HOLYLIGHT.value)

    def can_see(self, character: Any, victim: Any, room_helper: RoomHelper) -> bool:
        if character == victim:
            return True

        if self.get_trust(character) < victim.invis_level:
            return False

        if self.get_trust(character) < victim.incog_level and character.room_id != victim.room_id:
            return False

        if ((not self.is_npc(character) and self.has_holy_light(character))
                or (self.is_npc(character) and self.is_immortal(character))):
            return True

        if self.is_affected(character, self.AffectedBits.AFF_BLIND.value):
            return False

        if room_helper.is_room_dark(character.room_id) and not self.is_affected(character, self.AffectedBits.AFF_INFRARED.value):
            return False

        if self.is_affected(victim, self.AffectedBits.AFF_INVISIBLE.value) and not self.is_affected(character, self.AffectedBits.AFF_DETECT_INVIS.value):
            return False

        # to-do: implement sneak chance
        #     int chance;
        #     chance = get_skill(victim, gsn_sneak);
        #     chance += get_curr_stat(victim, STAT_DEX) * 3 / 2;
        #     chance -= get_curr_stat(ch, STAT_INT) * 2;
        #     chance -= ch->level - victim->level * 3 / 2;
        if self.is_affected(victim, self.AffectedBits.AFF_SNEAK.value) \
                and not self.is_affected(character, self.AffectedBits.AFF_DETECT_HIDDEN.value)\
                and victim.fighting is None:
            pass

        if self.weather_handler.weather_info.sunlight == self.TimeAndWeatherEnum.SUN_SET.value\
                or self.weather_handler.weather_info.sunlight == self.TimeAndWeatherEnum.SUN_DARK.value:
            return True
        chance = 0
        if rng.number_percent() < chance:
            return False
        return True
