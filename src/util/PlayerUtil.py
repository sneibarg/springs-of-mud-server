from __future__ import annotations

from typing import List
from typing import Any, TYPE_CHECKING

from util.GenericUtil import GenericUtil
from util.InterpUtil import InterpUtil
from api.CharacterApi import CharacterApi
from server.session.SessionHandler import SessionHandler


if TYPE_CHECKING:
    from area.Room import Room
    from player.Character import Character


class PlayerUtil:
    @staticmethod
    def format_train_options(character: Character) -> str:
        attrs = getattr(character, "character_attributes", None)
        if attrs is None:
            return "You can train: hp mana.\r\n"

        trainable_stats = (
            ("str", "strength", 0),
            ("int", "intelligence", 1),
            ("wis", "wisdom", 2),
            ("dex", "dexterity", 3),
            ("con", "constitution", 4),
        )
        options = [
            short_name
            for short_name, attr_name, stat_index in trainable_stats
            if (current := GenericUtil.to_int(getattr(attrs, attr_name, 0), 0))
               < CharacterApi.get_max_train(character, stat_index, current)
        ]

        options.extend(["hp", "mana"])
        if options:
            return f"You can train: {' '.join(options)}.\r\n"

        sex = str(getattr(character, "sex", "") or "").strip().lower()
        if sex in ("2", "female"):
            ending = "hot babe"
        elif sex in ("1", "male"):
            ending = "big stud"
        else:
            ending = "wild thing"
        return f"You have nothing left to train, you {ending}!\r\n"

    @staticmethod
    def format_visible_character_line(observer: Any, target: Any) -> str:
        affected_bits = CharacterApi.get_enum('affectedBy')
        player_act_bits = CharacterApi.get_enum('playerActBits')

        def _has_player_act_bit(char, bit_name: str) -> bool:
            if CharacterApi.is_npc(char) or not hasattr(player_act_bits, bit_name):
                return False
            act_value = char.status_flags.comm
            return CharacterApi.is_set(act_value, getattr(player_act_bits, bit_name).value)

        def _is_affected(char, bit_name: str) -> bool:
            if not hasattr(affected_bits, bit_name):
                return False
            return CharacterApi.is_affected(char, getattr(affected_bits, bit_name).value)

        prefixes = []
        if _is_affected(target, "AFF_INVISIBLE"):
            prefixes.append("(Invis)")
        GameParameters = CharacterApi.get_enum("gameParameters")
        if GenericUtil.to_int(getattr(target.status_flags, "invis_level", 0)) >= GenericUtil.to_int(GameParameters.HERO.value, 51):
            prefixes.append("(Wizi)")
        if _is_affected(target, "AFF_HIDE"):
            prefixes.append("(Hide)")
        if _is_affected(target, "AFF_CHARM"):
            prefixes.append("(Charmed)")
        if _is_affected(target, "AFF_PASS_DOOR"):
            prefixes.append("(Translucent)")
        if _is_affected(target, "AFF_FAERIE_FIRE"):
            prefixes.append("(Pink Aura)")
        if _is_affected(observer, "AFF_DETECT_EVIL") and CharacterApi.is_evil(target):
            prefixes.append("(Red Aura)")
        if _is_affected(observer, "AFF_DETECT_GOOD") and CharacterApi.is_good(target):
            prefixes.append("(Golden Aura)")
        if _is_affected(target, "AFF_SANCTUARY"):
            prefixes.append("(White Aura)")
        if _has_player_act_bit(target, "PLR_KILLER"):
            prefixes.append("(KILLER)")
        if _has_player_act_bit(target, "PLR_THIEF"):
            prefixes.append("(THIEF)")
        prefix = (" ".join(prefixes) + " ") if prefixes else ""

        target_pos = getattr(target, "position", None)
        if target_pos is None and hasattr(target, "character_attributes"):
            target_pos = getattr(target.character_attributes, "position", None)
        target_pos = GenericUtil.to_int(target_pos, -1)

        start_pos = GenericUtil.to_int(getattr(target, "start_pos", -9999), -9999)
        long_desc = (getattr(target, "long_description", "") or "").rstrip("\r\n")
        if start_pos != -9999 and target_pos == start_pos and long_desc:
            return f"{prefix}{long_desc}\r\n"

        name = (getattr(target, "name", "") or "").strip()
        if CharacterApi.is_npc(target):
            name = (getattr(target, "short_description", "") or name).strip()
        if not name:
            name = "Someone"

        positions = CharacterApi.get_enum("positions")

        def _pos(name: str, default: int = -9999) -> int:
            if not hasattr(positions, name):
                return default
            return GenericUtil.to_int(getattr(positions, name).value, default)

        if target_pos == _pos("POS_DEAD"):
            suffix = " is DEAD!!"
        elif target_pos == _pos("POS_MORTAL"):
            suffix = " is mortally wounded."
        elif target_pos == _pos("POS_INCAP"):
            suffix = " is incapacitated."
        elif target_pos == _pos("POS_STUNNED"):
            suffix = " is lying here stunned."
        elif target_pos == _pos("POS_SLEEPING"):
            suffix = " is sleeping here."
        elif target_pos == _pos("POS_RESTING"):
            suffix = " is resting here."
        elif target_pos == _pos("POS_SITTING"):
            suffix = " is sitting here."
        elif target_pos == _pos("POS_FIGHTING"):
            suffix = " is here, fighting "
            fighting = getattr(target, "fighting", None)
            if fighting is None:
                suffix += "thin air??"
            elif fighting == observer:
                suffix += "YOU!"
            else:
                fight_name = getattr(fighting, "name", "someone who left??")
                if getattr(fighting, "room_id", None) == getattr(target, "room_id", None):
                    suffix += f"{fight_name}."
                else:
                    suffix += "someone who left??"
        else:
            suffix = " is here."

        line = f"{prefix}{name}{suffix}"
        return f"{line[:1].upper() + line[1:]}\r\n"

    @staticmethod
    def visible(character: Character, session_handler: SessionHandler) -> List[Character]:
        visible = []
        observer_trust = GenericUtil.to_int(CharacterApi.get_trust(character))
        for session in session_handler.get_playing_sessions():
            char = session.character
            if char is None:
                continue
            if char.id == character.id:
                continue
            if char.cloaked and character.role == "player":
                continue

            invis_level = GenericUtil.to_int(getattr(char.status_flags, "invis_level", 0))
            incog_level = GenericUtil.to_int(getattr(char.status_flags, "incog_level", 0))
            if observer_trust < invis_level:
                continue
            if observer_trust < incog_level:
                continue
            visible.append(char)
        return visible

    @staticmethod
    def is_target_playing(target: str, session_handler: SessionHandler) -> bool:
        for session in session_handler.get_playing_sessions():
            char: Character = session.character
            if char.name == target:
                return True
        return False

    @staticmethod
    def get_target(character: Character, victim: str, room: Room):
        if room is None:
            return None

        if hasattr(room, "find_visible_target"):
            return room.find_visible_target(character, victim)

        if (victim or "").strip().lower() == "self":
            return character

        target = PlayerUtil._get_character_target(character, victim, room)
        if target is None:
            target = PlayerUtil._get_mobile_target(character, victim, room)

        return target

    @staticmethod
    def _get_character_target(character: Character, victim: str, room: Room):
        wanted = (victim or "").strip().lower()
        if not wanted:
            return None

        for char in room.characters.values():
            if not CharacterApi.can_see(character, char, room):
                continue

            if char.room_id == room.id:
                char_name = (char.name or "").strip().lower()
                if char_name == wanted or char_name.startswith(wanted):
                    return char
        return None

    @staticmethod
    def _get_mobile_target(character, victim: str, room: Room):
        mob = InterpUtil.find_nth_by_keyword(room.mobiles, victim)  # support for 1.mob_name; 2.mob_name, etc
        if mob is not None and CharacterApi.can_see(character, mob, room):
            return mob
        else:
            return None
