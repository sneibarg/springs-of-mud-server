from __future__ import annotations

from typing import Any

from api.CharacterApi import CharacterApi
from util.GenericUtil import GenericUtil
from util.InterpUtil import InterpUtil
from util.WizUtil import WizUtil


class WizApi:
    @staticmethod
    def current_prefix(view) -> str:
        return str((getattr(view.context.character, "context", {}) or {}).get("prefix", "") or "")

    @staticmethod
    def room_registry(view):
        player_handler = view.context.player_handler()
        return None if player_handler is None else getattr(player_handler, "room_registry", None)

    @staticmethod
    def character_registry(view):
        player_handler = view.context.player_handler()
        return None if player_handler is None else getattr(player_handler, "character_registry", None)

    @staticmethod
    def location(view):
        return CharacterApi.find_location(
            InterpUtil.argument_text(view),
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
    def poof_missing_name(view) -> bool:
        arg = InterpUtil.argument_text(view)
        if not arg:
            return False
        return str(getattr(view.context.character, "name", "") or "") not in arg

    @staticmethod
    def smote_noemote(view) -> bool:
        comm_flags = CharacterApi.get_enum("commFlags")
        bit = CharacterApi.enum_bit(comm_flags, "COMM_NOEMOTE")
        return bit and CharacterApi.is_set(getattr(view.context.character.status_flags, "comm", 0), bit)

    @staticmethod
    def world_target(view):
        return WizUtil.find_world_entity(
            WizApi.character_registry(view),
            WizApi.room_registry(view),
            InterpUtil.argument_text(view),
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
            snoop_proof and CharacterApi.is_set(getattr(target.status_flags, "comm", 0), snoop_proof)
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

    @classmethod
    def wiz_do_mload(cls, context: Any, vnum_text: str, mobile_registry, room_registry):
        from util.MobileUtil import MobileUtil

        vnum = (vnum_text or "").strip()
        proto = mobile_registry.get_or_none(vnum=vnum)
        if proto is None:
            context.finish()
            return {"to_char": "No mobile has that vnum.\r\n"}

        mob = MobileUtil.create_mobile(proto, cls.enum_provider())
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
