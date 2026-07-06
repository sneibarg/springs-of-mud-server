from __future__ import annotations

from api.CharacterApi import CharacterApi
from player.Character import Character
from util.AreaUtil import AreaUtil
from util.GenericUtil import GenericUtil
from util.InterpUtil import InterpUtil
from util.WizUtil import WizUtil


class WizApi:
    @staticmethod
    def current_prefix(view) -> str:
        return str((view.context.character.context or {}).get("prefix", "") or "")

    @staticmethod
    def room_registry(view):
        player_handler = view.context.player_handler()
        return None if player_handler is None else player_handler.room_registry

    @staticmethod
    def character_registry(view):
        player_handler = view.context.player_handler()
        return None if player_handler is None else player_handler.character_registry

    @staticmethod
    def restore_character(victim: Character):
        victim.hit = int(victim.max_hit)
        victim.mana = int(victim.max_mana)
        victim.movement = int(victim.max_movement)

    @staticmethod
    def location(view):
        return AreaUtil.find_location(
            InterpUtil.argument_text(view),
            WizApi.room_registry(view),
            WizApi.character_registry(view),
            WizUtil.name_matches,
        )

    @staticmethod
    def at_argument_parts(view) -> tuple[str, str]:
        return InterpUtil.one_argument(InterpUtil.argument_text(view))

    @staticmethod
    def at_missing_argument(view) -> bool:
        location_arg, nested_command = WizApi.at_argument_parts(view)
        return not location_arg or not nested_command

    @staticmethod
    def at_location(view):
        location_arg, _nested_command = WizApi.at_argument_parts(view)
        return AreaUtil.find_location(
            location_arg,
            WizApi.room_registry(view),
            WizApi.character_registry(view),
            WizUtil.name_matches,
        )

    @staticmethod
    def explicit_level_out_of_range(view, attr_name: str) -> bool:
        arg = InterpUtil.argument_text(view)
        if not arg:
            return False
        if not arg.lstrip("-").isdigit():
            return True
        level = GenericUtil.to_int(arg, 0)
        return level < 2 or level > CharacterApi.get_trust(view.context.character)

    @staticmethod
    def max_level_token(_view) -> dict:
        return {"d": WizApi.max_level()}

    @staticmethod
    def max_level() -> int:
        params = CharacterApi.get_enum("gameParameters")
        return 60 if params is None or not hasattr(params, "MAX_LEVEL") else GenericUtil.to_int(params.MAX_LEVEL.value, 60)

    @staticmethod
    def advance_parts(view) -> tuple[str, str]:
        arg1, rest = InterpUtil.one_argument(InterpUtil.argument_text(view))
        arg2, _rest = InterpUtil.one_argument(rest)
        return arg1, arg2

    @staticmethod
    def advance_syntax_invalid(view) -> bool:
        arg1, arg2 = WizApi.advance_parts(view)
        return not arg1 or not arg2 or not str(arg2).lstrip("-").isdigit()

    @staticmethod
    def advance_target(view):
        target_name, _level = WizApi.advance_parts(view)
        return WizUtil.find_world_entity(
            WizApi.character_registry(view),
            WizApi.room_registry(view),
            target_name,
            include_players=True,
            include_mobiles=True,
        )

    @staticmethod
    def advance_target_missing(view) -> bool:
        return WizApi.advance_target(view) is None

    @staticmethod
    def advance_target_is_npc(view) -> bool:
        target = WizApi.advance_target(view)
        return target is not None and CharacterApi.is_npc(target)

    @staticmethod
    def advance_level_invalid(view) -> bool:
        _target_name, level_text = WizApi.advance_parts(view)
        level = GenericUtil.to_int(level_text, 0)
        return level < 1 or level > WizApi.max_level()

    @staticmethod
    def advance_trust_limited(view) -> bool:
        _target_name, level_text = WizApi.advance_parts(view)
        return GenericUtil.to_int(level_text, 0) > CharacterApi.get_trust(view.context.character)

    @staticmethod
    def flag_parts(view) -> dict:
        arg1, rest = InterpUtil.one_argument(InterpUtil.argument_text(view))
        arg2, rest = InterpUtil.one_argument(rest)
        arg3, rest = InterpUtil.one_argument(rest)
        rest = str(rest or "").lstrip()
        op = rest[0] if rest[:1] in ("=", "-", "+") else ""
        changes = rest
        if op:
            _operator, changes = InterpUtil.one_argument(rest)
        return {
            "kind": arg1,
            "target": arg2,
            "field": arg3,
            "op": op,
            "changes": str(changes or "").strip(),
        }

    @staticmethod
    def flag_kind_missing(view) -> bool:
        return not WizApi.flag_parts(view)["kind"]

    @staticmethod
    def flag_target_arg_missing(view) -> bool:
        return bool(WizApi.flag_parts(view)["kind"]) and not WizApi.flag_parts(view)["target"]

    @staticmethod
    def flag_field_missing(view) -> bool:
        parts = WizApi.flag_parts(view)
        return bool(parts["target"]) and not parts["field"]

    @staticmethod
    def flag_changes_missing(view) -> bool:
        parts = WizApi.flag_parts(view)
        return bool(parts["field"]) and not parts["changes"]

    @staticmethod
    def flag_kind_invalid(view) -> bool:
        kind = WizApi.flag_parts(view)["kind"]
        return bool(kind) and not (WizApi._is_prefix(kind, "mob") or WizApi._is_prefix(kind, "char"))

    @staticmethod
    def flag_target(view):
        target_name = WizApi.flag_parts(view)["target"]
        return WizUtil.find_world_entity(
            WizApi.character_registry(view),
            WizApi.room_registry(view),
            target_name,
            include_players=True,
            include_mobiles=True,
        )

    @staticmethod
    def flag_target_missing(view) -> bool:
        return WizApi.flag_target(view) is None

    @staticmethod
    def flag_field_code(view) -> str:
        field = WizApi.flag_parts(view)["field"]
        if WizApi._is_prefix(field, "act"):
            return "act"
        if WizApi._is_prefix(field, "plr"):
            return "plr"
        if WizApi._is_prefix(field, "aff"):
            return "aff"
        if WizApi._is_prefix(field, "immunity"):
            return "imm"
        if WizApi._is_prefix(field, "resist"):
            return "res"
        if WizApi._is_prefix(field, "vuln"):
            return "vuln"
        if WizApi._is_prefix(field, "form"):
            return "form"
        if WizApi._is_prefix(field, "parts"):
            return "parts"
        if WizApi._is_prefix(field, "comm"):
            return "comm"
        return ""

    @staticmethod
    def flag_plr_is_npc(view) -> bool:
        target = WizApi.flag_target(view)
        return target is not None and WizApi.flag_field_code(view) == "plr" and CharacterApi.is_npc(target)

    @staticmethod
    def flag_act_is_pc(view) -> bool:
        target = WizApi.flag_target(view)
        return target is not None and WizApi.flag_field_code(view) == "act" and not CharacterApi.is_npc(target)

    @staticmethod
    def flag_form_pc(view) -> bool:
        target = WizApi.flag_target(view)
        return target is not None and WizApi.flag_field_code(view) == "form" and not CharacterApi.is_npc(target)

    @staticmethod
    def flag_parts_pc(view) -> bool:
        target = WizApi.flag_target(view)
        return target is not None and WizApi.flag_field_code(view) == "parts" and not CharacterApi.is_npc(target)

    @staticmethod
    def flag_comm_npc(view) -> bool:
        target = WizApi.flag_target(view)
        return target is not None and WizApi.flag_field_code(view) == "comm" and CharacterApi.is_npc(target)

    @staticmethod
    def flag_field_invalid(view) -> bool:
        return not WizApi.flag_field_code(view)

    @staticmethod
    def flag_unknown_name(view) -> bool:
        field_code = WizApi.flag_field_code(view)
        if not field_code:
            return False
        return any(WizApi.flag_bit(field_code, word) == 0 for word in WizApi.flag_parts(view)["changes"].split())

    @staticmethod
    def flag_bit(field_code: str, word: str) -> int:
        aliases = {
            "act": ("actBits", "ACT_", {"npc": "ACT_IS_NPC", "healer": "ACT_IS_HEALER", "changer": "ACT_IS_CHANGER"}),
            "plr": ("playerActBits", "PLR_", {"npc": "PLR_IS_NPC", "can_loot": "PLR_CANLOOT"}),
            "aff": ("affectedBy", "AFF_", {}),
            "imm": ("mobImmunity", "IMM_", {}),
            "res": ("mobResistance", "RES_", {}),
            "vuln": ("mobVulnerability", "VULN_", {}),
            "form": ("bodyForm", "FORM_", {}),
            "parts": ("bodyParts", "PART_", {"ear": "PART_EAR", "eye": "PART_EYE"}),
            "comm": ("commFlags", "COMM_", {"noclangossip": "COMM_NOAUCTION", "shoutsoff": "COMM_SHOUTSOFF"}),
        }
        enum_name, prefix, special = aliases.get(field_code, ("", "", {}))
        enum_obj = CharacterApi.get_enum(enum_name) if enum_name else None
        query = str(word or "").strip().lower()
        if not query or enum_obj is None:
            return 0
        if query in special:
            return CharacterApi.enum_bit(enum_obj, special[query])
        for member_name, member in enum_obj.__members__.items():
            label = member_name
            if prefix and label.startswith(prefix):
                label = label[len(prefix):]
            label = label.lower()
            if label == query or label.startswith(query):
                return int(member.value)
        return 0

    @staticmethod
    def _is_prefix(value: str, full: str) -> bool:
        text = str(value or "").strip().lower()
        return bool(text) and str(full or "").lower().startswith(text)

    @staticmethod
    def room_private_for_actor(view, room, *, implementor_only: bool = False) -> bool:
        handler = view.context.wiz_handler()
        if handler is None:
            return False
        return handler.room_is_private_for_actor(view.context.character, room, implementor_only=implementor_only)

    @staticmethod
    def goto_private(view) -> bool:
        room = WizApi.location(view)
        return room is not None and WizApi.room_private_for_actor(view, room)

    @staticmethod
    def at_private(view) -> bool:
        room = WizApi.at_location(view)
        return room is not None and WizApi.room_private_for_actor(view, room)

    @staticmethod
    def poof_missing_name(view) -> bool:
        arg = InterpUtil.argument_text(view)
        if not arg:
            return False
        return str(view.context.character.name or "") not in arg

    @staticmethod
    def smote_noemote(view) -> bool:
        comm_flags = CharacterApi.get_enum("commFlags")
        bit = CharacterApi.enum_bit(comm_flags, "COMM_NOEMOTE")
        return bit and CharacterApi.is_set(view.context.character.status_flags.comm, bit)

    @staticmethod
    def world_target(view):
        argument = InterpUtil.argument_text(view).strip().lower()
        if argument == "self":
            return view.context.character
        return WizUtil.find_world_entity(
            WizApi.character_registry(view),
            WizApi.room_registry(view),
            argument,
        )

    @staticmethod
    def world_player_target(view):
        return WizUtil.find_world_entity(
            WizApi.character_registry(view),
            WizApi.room_registry(view),
            InterpUtil.argument_text(view),
            include_mobiles=False,
        )

    @staticmethod
    def switch_target(view):
        return WizUtil.find_world_entity(
            WizApi.character_registry(view),
            WizApi.room_registry(view),
            InterpUtil.argument_text(view),
            include_players=True,
            include_mobiles=True,
        )

    @staticmethod
    def switch_without_session(view) -> bool:
        handler = view.context.wiz_handler()
        if handler is None:
            return True
        return handler.current_session(view.context.character) is None

    @staticmethod
    def switch_self(view) -> bool:
        return WizApi.switch_target(view) == view.context.character

    @staticmethod
    def switch_non_mobile(view) -> bool:
        target = WizApi.switch_target(view)
        return target is not None and target != view.context.character and not CharacterApi.is_npc(target)

    @staticmethod
    def switch_private(view) -> bool:
        target = WizApi.switch_target(view)
        room = None if target is None else WizUtil.room_of_entity(WizApi.room_registry(view), target)
        return room is not None and WizApi.room_private_for_actor(view, room, implementor_only=True)

    @staticmethod
    def switch_in_use(view) -> bool:
        target = WizApi.switch_target(view)
        if target is None:
            return False
        if target == view.context.character:
            return False
        handler = view.context.wiz_handler()
        if handler is None:
            return False
        return handler.current_session(target) is not None

    @staticmethod
    def switched(view) -> bool:
        handler = view.context.wiz_handler()
        if handler is None:
            return False
        return handler.is_switched(view.context.character)

    @staticmethod
    def snoop_target(view):
        return WizApi.world_target(view)

    @staticmethod
    def snoop_private(view) -> bool:
        target = WizApi.snoop_target(view)
        room = None if target is None else WizUtil.room_of_entity(WizApi.room_registry(view), target)
        return room is not None and WizApi.room_private_for_actor(view, room, implementor_only=True)

    @staticmethod
    def snoop_failed(view) -> bool | int:
        target = WizApi.snoop_target(view)
        if target is None:
            return False
        if target == view.context.character:
            return False
        comm_flags = CharacterApi.get_enum("commFlags")
        snoop_proof = CharacterApi.enum_bit(comm_flags, "COMM_SNOOP_PROOF")
        return (CharacterApi.get_trust(target) >= CharacterApi.get_trust(view.context.character)) or (
            snoop_proof and CharacterApi.is_set(target.status_flags.comm, snoop_proof)
        )

    @staticmethod
    def snoop_loop(view) -> bool:
        target = WizApi.snoop_target(view)
        handler = view.context.wiz_handler()
        if target is None or handler is None:
            return False
        if target == view.context.character:
            return False
        return handler.snoop_loop(view.context.character, target)

    @staticmethod
    def session_target_missing(view) -> bool:
        target = WizApi.snoop_target(view)
        handler = view.context.wiz_handler()
        if target is None or handler is None or target == view.context.character:
            return False
        return handler.current_session(target) is None

    @staticmethod
    def session_target_busy(view) -> bool:
        target = WizApi.snoop_target(view)
        handler = view.context.wiz_handler()
        if target is None or handler is None or target == view.context.character:
            return False
        session = handler.current_session(target)
        if session is None:
            return False
        return bool(session.metadata.get("snoop_by_session_id"))
