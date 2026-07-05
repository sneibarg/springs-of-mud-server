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
