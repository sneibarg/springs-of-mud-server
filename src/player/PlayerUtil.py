from area import Room
from area.RoomHelper import RoomHelper
from game.GenericUtil import GenericUtil
from interp.InterpUtil import InterpUtil
from player.Character import Character
from player.CharacterMacros import CharacterMacros
from server.session.SessionHandler import SessionHandler
from typing import List
from typing import Any


class PlayerUtil:
    pass

    @staticmethod
    def format_visible_character_line(observer: Any, target: Any, character_macros: CharacterMacros) -> str:
        affected_bits = character_macros.AffectedBits
        player_act_bits = character_macros.PlayerActBits

        def _has_player_act_bit(char, bit_name: str) -> bool:
            if character_macros.is_npc(char) or player_act_bits is None or not hasattr(player_act_bits, bit_name):
                return False
            act_value = GenericUtil.to_int(character_macros.convert_flags(getattr(char.character_flags, "act", "0")))
            return character_macros.is_set(act_value, getattr(player_act_bits, bit_name).value)

        def _is_affected(char, bit_name: str) -> bool:
            if affected_bits is None or not hasattr(affected_bits, bit_name):
                return False
            return character_macros.is_affected(char, getattr(affected_bits, bit_name).value)

        prefixes = []
        if _is_affected(target, "AFF_INVISIBLE"):
            prefixes.append("(Invis)")
        hero_level = getattr(character_macros.character_constants, "immortal_levels", {}).get("LEVEL_HERO", 51)
        if GenericUtil.to_int(getattr(target, "invis_level", 0)) >= GenericUtil.to_int(hero_level, 51):
            prefixes.append("(Wizi)")
        if _is_affected(target, "AFF_HIDE"):
            prefixes.append("(Hide)")
        if _is_affected(target, "AFF_CHARM"):
            prefixes.append("(Charmed)")
        if _is_affected(target, "AFF_PASS_DOOR"):
            prefixes.append("(Translucent)")
        if _is_affected(target, "AFF_FAERIE_FIRE"):
            prefixes.append("(Pink Aura)")
        if _is_affected(observer, "AFF_DETECT_EVIL") and character_macros.is_evil(target):
            prefixes.append("(Red Aura)")
        if _is_affected(observer, "AFF_DETECT_GOOD") and character_macros.is_good(target):
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
        if character_macros.is_npc(target):
            name = (getattr(target, "short_description", "") or name).strip()
        if not name:
            name = "Someone"

        positions = character_macros.PositionsEnum

        def _pos(name: str, default: int = -9999) -> int:
            if positions is None or not hasattr(positions, name):
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
    def visible(character: Character, session_handler: SessionHandler,
                character_macros: CharacterMacros | None = None) -> List[Character]:
        visible = []
        observer_trust = 0
        if character_macros is not None:
            observer_trust = GenericUtil.to_int(character_macros.get_trust(character))
        for session in session_handler.get_playing_sessions():
            char: Character = session.character
            if char is None:
                continue
            if char.id == character.id:
                continue
            if char.cloaked and character.role == "player":
                continue
            if character_macros is not None:
                invis_level = GenericUtil.to_int(getattr(char, "invis_level", 0))
                incog_level = GenericUtil.to_int(getattr(char, "incog_level", 0))
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
    def get_target(character: Character, victim: str, room: Room, character_macros: CharacterMacros,
                   room_helper: RoomHelper):
        if room is None:
            return None

        if (victim or "").strip().lower() == "self":
            return character

        target = PlayerUtil._get_character_target(character, victim, room, character_macros, room_helper)
        if target is None:
            target = PlayerUtil._get_mobile_target(character, victim, room, character_macros, room_helper)

        return target

    @staticmethod
    def _get_character_target(character: Character, victim: str, room: Room, character_macros: CharacterMacros,
                              room_helper: RoomHelper):
        wanted = (victim or "").strip().lower()
        if not wanted:
            return None

        for char in room.characters.values():
            if not character_macros.can_see(character, char, room_helper):
                continue

            if char.room_id == room.id:
                char_name = (char.name or "").strip().lower()
                if char_name == wanted or char_name.startswith(wanted):
                    return char
        return None

    @staticmethod
    def _get_mobile_target(character, victim: str, room: Room, character_macros: CharacterMacros,
                           room_helper: RoomHelper):
        mob = InterpUtil.find_nth_by_keyword(room.mobiles, victim)  # support for 1.mob_name; 2.mob_name, etc
        if mob is not None and character_macros.can_see(character, mob, room_helper):
            return mob
        else:
            return None
