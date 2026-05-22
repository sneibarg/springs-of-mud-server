from __future__ import annotations

from typing import Any, TYPE_CHECKING

from mobile.Mobile import Mobile
from player.Character import Character
from api.GameApi import GameApi
from util.GenericUtil import GenericUtil
from game.RandomNumberGenerator import RandomNumberGenerator


if TYPE_CHECKING:
    from area.Room import Room

rng = RandomNumberGenerator()


class CharacterApi(GameApi):
    _registry_service = None
    _weather_handler = None
    _logger = None

    @classmethod
    def _reset_internal_variables(cls) -> None:
        cls._registry_service = None
        cls._weather_handler = None
        cls._logger = None

    @classmethod
    def set_registry(cls, registry_service) -> None:
        cls._registry_service = registry_service

    @classmethod
    def lazy_load(cls, weather_handler, registry_service=None) -> None:
        if registry_service is not None:
            cls._registry_service = registry_service
        cls._weather_handler = weather_handler
        cls.load_enums(
            TimeAndWeather="timeAndWeather",
            GameParameters="gameParameters",
            AffectedBits="affectedBy",
            positions="positions",
            RoomFlags="roomFlags",
            CommFlags="commFlags",
            PlayerActBits="playerActBits",
            OffenseTypes="offenseTypes",
            SectorTypes="sectorTypes",
        )

    @classmethod
    def _registry(cls):
        if cls._registry_service is None:
            cls._require_configured()
            raise RuntimeError("CharacterApi registry service not configured.")
        return cls._registry_service

    @classmethod
    def _weather(cls):
        return cls._weather_handler

    @classmethod
    def get_trust(cls, char: Any) -> int:
        from player.Character import Character
        controller = (getattr(char, "context", {}) or {}).get("controller_original")
        if controller is not None and controller is not char:
            return cls.get_trust(controller)
        if type(char) is Character and char.trust > 0:
            return char.trust
        if cls.is_npc(char) and char.level >= cls.GameParameters.HERO.value:
            return cls.GameParameters.HERO.value - 1
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

    @classmethod
    def get_registry(cls):
        return cls._registry()

    @staticmethod
    def is_npc(char: Any) -> bool:
        return type(char) is Mobile

    @classmethod
    def is_immortal(cls, char: Character) -> bool:
        return cls.GameParameters is not None and cls.get_trust(char) >= cls.GameParameters.LEVEL_IMMORTAL.value

    @classmethod
    def is_trusted(cls, char: Character) -> bool:
        return cls.get_trust(char) >= char.level

    @classmethod
    def is_affected(cls, char: Any, effect) -> bool:
        return cls.is_set(char.status_flags.affected_by, effect)

    @classmethod
    def is_blind(cls, character: Any) -> bool:
        return cls.is_set(character.status_flags.affected_by, cls.AffectedBits.AFF_BLIND.value)

    @classmethod
    def is_awake(cls, char: Any) -> bool:
        return cls.position_value(char) > cls.positions.POS_SLEEPING.value

    @staticmethod
    def is_good(char: Any) -> bool:
        from player.Character import Character
        if type(char) is Character:
            return char.character_attributes.alignment >= 350
        return char.character_attributes.alignment >= 350

    @staticmethod
    def is_evil(char: Any) -> bool:
        from player.Character import Character
        if type(char) is Character:
            return char.character_attributes.alignment <= -350
        return char.character_attributes.alignment <= -350

    @classmethod
    def is_neutral(cls, char: Any) -> bool:
        return not cls.is_good(char) and not cls.is_evil(char)

    @classmethod
    def get_hitroll(cls, char: Any) -> int:
        strength = char.character_attributes.strength
        return int(cls.get_attribute_bonus(attr_name="strength", attr_level=str(strength)).get("tohit", 0))

    @classmethod
    def get_damroll(cls, char: Any) -> int:
        strength = char.character_attributes.strength
        return int(cls.get_attribute_bonus(attr_name="strength", attr_level=str(strength)).get("todam", 0))

    @classmethod
    def is_outside(cls, char: Any) -> bool:
        room: Room = cls._registry().room_registry.get(id=char.room_id)

        cls._logger_obj().debug(f"is_outside: {room.room_flags}={cls.RoomFlags.ROOM_INDOORS}")
        return (room.room_flags & cls.RoomFlags.ROOM_INDOORS) == 0

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
    def assign_act_flags(character: Character, value: int) -> None:
        character.status_flags.assign_bitfield("act", GenericUtil.to_int(value, 0))

    @classmethod
    def set_act_flags(cls, character: Character, bit) -> None:
        cls.assign_act_flags(character, cls.set_bit(character.status_flags.act, bit))

    @classmethod
    def unset_act_flags(cls, character: Character, bit) -> None:
        cls.assign_act_flags(character, cls.unset_bit(character.status_flags.act, bit))

    @staticmethod
    def assign_comm_flags(character: Character, value: int) -> None:
        character.status_flags.assign_bitfield("comm", GenericUtil.to_int(value, 0))

    @classmethod
    def set_comm_flags(cls, character: Character, bit) -> None:
        cls.assign_comm_flags(character, cls.set_bit(character.status_flags.comm, bit))

    @classmethod
    def unset_comm_flags(cls, character: Character, bit) -> None:
        cls.assign_comm_flags(character, cls.unset_bit(character.status_flags.comm, bit))

    @classmethod
    def is_comm_enabled(cls, character: Character, bit_name: str) -> bool:
        return cls.is_set(character.status_flags.comm, getattr(cls.CommFlags, bit_name).value)

    @classmethod
    def toggle_player_act(cls, character: Character, bit_name: str, off_text: str, on_text: str) -> str:
        if cls.is_npc(character):
            return ""
        if not hasattr(cls.PlayerActBits, bit_name):
            return ""
        bit_value = getattr(cls.PlayerActBits, bit_name).value
        act = character.status_flags.act
        if cls.is_set(act, bit_value):
            cls.unset_act_flags(character, bit_value)
            return off_text
        cls.set_act_flags(character, bit_value)
        return on_text

    @classmethod
    def toggle_comm(cls, character: Character, bit_name: str, off_text: str, on_text: str) -> str:
        bit_value = getattr(cls.CommFlags, bit_name).value
        comm = character.status_flags.comm
        if cls.is_set(comm, bit_value):
            cls.unset_comm_flags(character, bit_value)
            return off_text
        cls.set_comm_flags(character, bit_value)
        return on_text

    @classmethod
    def format_affects(cls, character: Character) -> str:
        raw = GenericUtil.to_int(getattr(character.status_flags, "affected_by", 0), 0)
        lines = []
        for name, member in cls.AffectedBits.__members__.items():
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
                from item.Item import Item
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
        max_level = cls.GameParameters.MAX_LEVEL.value
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
        for item in CharacterApi.owned_items(character):
            name = (getattr(item, "name", "") or "").lower()
            if name == key or name.startswith(key):
                return item
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
    def class_names(cls) -> list[str]:
        return sorted(str(name or "") for name in cls._classes_map().keys() if str(name or "").strip())

    @classmethod
    def class_data(cls, class_name: str) -> dict:
        wanted = str(class_name or "").strip().lower()
        if not wanted:
            return {}
        classes = cls._classes_map()
        if wanted in classes:
            return dict(classes.get(wanted) or {})
        for key, value in classes.items():
            label = str(key or "").strip().lower()
            if label == wanted or label.startswith(wanted):
                return dict(value or {})
        return {}

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
        pos_dead = cls.positions.POS_DEAD.value if cls.positions and hasattr(cls.positions, "POS_DEAD") else -1
        pos_mortal = cls.positions.POS_MORTAL.value if cls.positions and hasattr(cls.positions, "POS_MORTAL") else -1
        pos_incap = cls.positions.POS_INCAP.value if cls.positions and hasattr(cls.positions, "POS_INCAP") else -1
        pos_stunned = cls.positions.POS_STUNNED.value if cls.positions and hasattr(cls.positions, "POS_STUNNED") else -1
        pos_sleeping = cls.positions.POS_SLEEPING.value if cls.positions and hasattr(cls.positions, "POS_SLEEPING") else -1
        pos_resting = cls.positions.POS_RESTING.value if cls.positions and hasattr(cls.positions, "POS_RESTING") else -1
        pos_sitting = cls.positions.POS_SITTING.value if cls.positions and hasattr(cls.positions, "POS_SITTING") else -1
        pos_fighting = cls.positions.POS_FIGHTING.value if cls.positions and hasattr(cls.positions, "POS_FIGHTING") else -1
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

        raw = GenericUtil.to_int(getattr(victim.status_flags, "comm", 0), 0)
        if cls.is_set(raw, bit):
            cls.unset_comm_flags(victim, bit)
            context.finish()
            return {"to_char": f"{label} removed.\r\n", "victim": victim, "to_victim": "The gods have restored your privileges.\r\n"}

        cls.set_comm_flags(victim, bit)
        context.finish()
        return {"to_char": f"{label} set.\r\n", "victim": victim, "to_victim": "The gods have revoked your privileges.\r\n"}

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
            return {"to_char": "No item has that vnum.\r\n"}

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
        return cls.is_set(character.status_flags.affected_by, bit)

    @classmethod
    def set_affected_by_name(cls, character: Character, affected_bits, bit_name: str, enabled: bool):
        if affected_bits is None or not hasattr(affected_bits, bit_name):
            return
        bit = getattr(affected_bits, bit_name).value
        if enabled:
            character.status_flags.set_flag("affected_by", bit)
            return
        character.status_flags.unset_flag("affected_by", bit)

    @classmethod
    def pos_value(cls, name: str) -> int:
        if not hasattr(cls.positions, name):
            return -1
        return int(getattr(cls.positions, name).value)

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
            if hasattr(cls.positions, name):
                return int(getattr(cls.positions, name).value)
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
        if not hasattr(cls.positions, pos_name):
            return
        value = int(getattr(cls.positions, pos_name).value)
        attrs = getattr(character, "character_attributes", None)
        if attrs is not None:
            attrs.position = value
        setattr(character, "position", value)

    @classmethod
    def is_fighting(cls, char: Character) -> bool:
        return char.character_attributes.position == cls.pos_value("POS_FIGHTING")

    @classmethod
    def is_stunned(cls, char: Character) -> bool:
        return char.character_attributes.position == cls.pos_value("POS_STUNNED")

    @classmethod
    def is_dead(cls, char: Character) -> bool:
        return char.character_attributes.position == cls.pos_value("POS_DEAD")

    @classmethod
    def is_mortal(cls, char: Character) -> bool:
        return char.character_attributes.position == cls.pos_value("POS_MORTAL")

    @classmethod
    def is_sleeping(cls, char: Character) -> bool:
        return char.character_attributes.position == cls.pos_value("POS_SLEEPING")

    @classmethod
    def is_resting(cls, char: Character) -> bool:
        return char.character_attributes.position == cls.pos_value("POS_RESTING")

    @classmethod
    def is_sitting(cls, char: Character) -> bool:
        return char.character_attributes.position == cls.pos_value("POS_SITTING")

    @classmethod
    def is_standing(cls, char: Character) -> bool:
        return char.character_attributes.position == cls.pos_value("POS_STANDING")

    @classmethod
    def is_flying(cls, char: Character) -> bool:
        return char.character_attributes.position == cls.pos_value("POS_FLYING")

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
        if not hasattr(cls.PlayerActBits, "PLR_HOLYLIGHT"):
            return False
        return cls.is_set(
            GenericUtil.to_int(character.status_flags.act, 0),
            cls.PlayerActBits.PLR_HOLYLIGHT.value,
        )

    @classmethod
    def can_see(cls, character: Any, victim: Any, room: Room) -> bool:
        if character == victim:
            return True

        if cls.get_trust(character) < victim.status_flags.invis_level:
            return False

        if cls.get_trust(character) < victim.status_flags.incog_level and character.room_id != victim.room_id:
            return False

        if ((not cls.is_npc(character) and cls.has_holy_light(character))
                or (cls.is_npc(character) and cls.is_immortal(character))):
            return True

        if cls.is_affected(character, cls.AffectedBits.AFF_BLIND.value):
            return False

        if type(character) is Character and room.is_room_dark() and not cls.is_affected(character, cls.AffectedBits.AFF_INFRARED.value):
            return False

        if cls.is_affected(victim, cls.AffectedBits.AFF_INVISIBLE.value) and not cls.is_affected(character, cls.AffectedBits.AFF_DETECT_INVIS.value):
            return False

        if cls.is_affected(victim, cls.AffectedBits.AFF_SNEAK.value) \
                and not cls.is_affected(character, cls.AffectedBits.AFF_DETECT_HIDDEN.value) \
                and victim.fighting is None:
            pass

        weather = cls._weather()
        if weather.weather_info.sunlight == cls.TimeAndWeather.SUN_SET.value \
                or weather.weather_info.sunlight == cls.TimeAndWeather.SUN_DARK.value:
            return True

        chance = 0
        if rng.number_percent() < chance:
            return False
        return True

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
    def player_auto_assist(cls, char: Character) -> bool:
        if cls.is_npc(char):
            return False
        return cls.is_set(char.status_flags.act, cls.PlayerActBits.PLR_AUTOASSIST.value)

    @classmethod
    def will_npc_assist(cls, rch: Mobile, ch: Character) -> bool | str | Any | Any:
        if not CharacterApi.is_npc(rch):
            return False

        off = rch.status_flags.off
        return (
                CharacterApi.is_set(off, cls.OffenseTypes.ASSIST_ALL.value) or
                (rch.group and rch.group == ch.group) or
                (rch.race == ch.race and CharacterApi.is_set(off, cls.OffenseTypes.ASSIST_RACE.value)) or
                (CharacterApi.is_set(off, cls.OffenseTypes.ASSIST_ALIGN.value) and
                 CharacterApi.same_alignment(rch, ch)) or
                (rch.vnum == ch.vnum and CharacterApi.is_set(off, cls.OffenseTypes.ASSIST_VNUM.value))
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
