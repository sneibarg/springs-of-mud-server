from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from api.CharacterApi import CharacterApi
from api.GameApi import GameApi
from util.GenericUtil import GenericUtil
from util.MovementUtil import MovementUtil


@dataclass(frozen=True)
class MovementState:
    direction: str = ""
    door: int = -1
    in_room: Any = None
    exit_obj: Any = None
    to_room: Any = None
    exit_closed: bool = False
    exit_keyword: str = "door"
    private_room: bool = False
    air_blocked: bool = False
    water_blocked: bool = False
    insufficient_movement: bool = False
    move_cost: int = 0


class MovementApi(GameApi):
    @staticmethod
    def move_state(subject, direction: str = "", room_registry=None) -> MovementState:
        character = MovementApi._character(subject)
        direction_name = MovementApi._direction(subject, direction)
        door = MovementUtil.direction_index(direction_name)
        in_room = MovementApi._room(subject, room_registry=room_registry)
        exit_obj = None
        if in_room is not None and door >= 0:
            exit_obj = in_room.get_exit(door) if hasattr(in_room, "get_exit") else MovementUtil.find_exit(in_room, door)

        to_room = MovementApi._destination_room(exit_obj, subject, room_registry=room_registry)
        exit_flags = CharacterApi.get_enum("exitFlags")
        room_flags = CharacterApi.get_enum("roomFlags")
        affected_bits = CharacterApi.get_enum("affectedBy")
        sector_types = CharacterApi.get_enum("sectorTypes")

        flags = GenericUtil.to_int(getattr(exit_obj, "exit_flags", 0), 0) if exit_obj is not None else 0
        ex_closed = MovementUtil.get_exit_flag(exit_flags, "EX_CLOSED", "CLOSED")
        ex_nopass = MovementUtil.get_exit_flag(exit_flags, "EX_NOPASS", "NOPASS")
        pass_door = bool(
            character is not None
            and CharacterApi.is_affected_by_name(character, affected_bits, "AFF_PASS_DOOR")
        )
        exit_closed = bool(
            exit_obj is not None
            and ex_closed
            and (flags & ex_closed) != 0
            and ((not pass_door) or (ex_nopass and (flags & ex_nopass) != 0))
        )

        is_npc = bool(character is not None and CharacterApi.is_npc(character))
        is_flying = bool(character is not None and CharacterApi.is_flying(character))
        air_blocked = False
        water_blocked = False
        move_cost = 0
        insufficient_movement = False
        if not is_npc and in_room is not None and to_room is not None and character is not None:
            air_blocked = bool(
                (in_room.is_air_room(sector_types) or to_room.is_air_room(sector_types))
                and not is_flying
                and not CharacterApi.is_immortal(character)
            )
            water_blocked = bool(
                (in_room.requires_boat(sector_types) or to_room.requires_boat(sector_types))
                and not is_flying
                and not character.has_boat()
            )
            move_cost = MovementApi._movement_cost(character, in_room, to_room, is_flying, affected_bits)
            insufficient_movement = GenericUtil.to_int(getattr(character, "movement", 0), 0) < move_cost

        return MovementState(
            direction=direction_name,
            door=door,
            in_room=in_room,
            exit_obj=exit_obj,
            to_room=to_room,
            exit_closed=exit_closed,
            exit_keyword=(getattr(exit_obj, "keyword", "") or "door") if exit_obj is not None else "door",
            private_room=bool(to_room is not None and to_room.is_private(room_flags)),
            air_blocked=air_blocked,
            water_blocked=water_blocked,
            insufficient_movement=insufficient_movement,
            move_cost=move_cost,
        )

    @staticmethod
    def invalid_exit(view) -> bool:
        state = MovementApi.move_state(view)
        return state.exit_obj is None or state.to_room is None

    @staticmethod
    def exit_closed(view) -> bool:
        return MovementApi.move_state(view).exit_closed

    @staticmethod
    def closed_tokens(view) -> dict[str, Any]:
        return {"t": MovementApi.move_state(view).exit_keyword}

    @staticmethod
    def private_room(view) -> bool:
        return MovementApi.move_state(view).private_room

    @staticmethod
    def air_blocked(view) -> bool:
        return MovementApi.move_state(view).air_blocked

    @staticmethod
    def water_blocked(view) -> bool:
        return MovementApi.move_state(view).water_blocked

    @staticmethod
    def insufficient_movement(view) -> bool:
        return MovementApi.move_state(view).insufficient_movement

    @staticmethod
    def leave_message(character, direction: str) -> str | None:
        door = MovementUtil.direction_index(direction)
        if door < 0 or not MovementApi.shows_movement_messages(character):
            return None
        return f"{character.name} leaves {MovementUtil.DIR_NAME[door]}.\r\n"

    @staticmethod
    def arrive_message(character) -> str | None:
        if not MovementApi.shows_movement_messages(character):
            return None
        return f"{character.name} has arrived.\r\n"

    @staticmethod
    def shows_movement_messages(character) -> bool:
        affected_bits = CharacterApi.get_enum("affectedBy")
        return (
            not CharacterApi.is_affected_by_name(character, affected_bits, "AFF_SNEAK")
            and GenericUtil.to_int(getattr(character.status_flags, "invis_level", 0), 0) < 51
        )

    @staticmethod
    def _movement_cost(character, in_room, to_room, is_flying: bool, affected_bits) -> int:
        move = (MovementUtil.sector_cost(in_room.sector_type) + MovementUtil.sector_cost(to_room.sector_type)) // 2
        if is_flying or CharacterApi.is_affected_by_name(character, affected_bits, "AFF_HASTE"):
            move //= 2
        if CharacterApi.is_affected_by_name(character, affected_bits, "AFF_SLOW"):
            move *= 2
        return max(1, move)

    @staticmethod
    def _character(subject):
        context = MovementApi._context(subject)
        if context is None:
            return getattr(subject, "character", None)
        return getattr(context, "character", None)

    @staticmethod
    def _context(subject):
        return getattr(subject, "context", subject)

    @staticmethod
    def _direction(subject, direction: str = "") -> str:
        if direction:
            return str(direction).strip().lower()
        context = MovementApi._context(subject)
        command = getattr(context, "command", None)
        return str(getattr(command, "name", "") or "").strip().lower()

    @staticmethod
    def _room(subject, room_registry=None):
        context = MovementApi._context(subject)
        room = getattr(context, "room", None)
        if room is not None:
            return room

        registry = MovementApi._room_registry(subject, room_registry=room_registry)
        character = MovementApi._character(subject)
        if registry is None or character is None:
            return None
        return registry.get_or_none(id=getattr(character, "room_id", None))

    @staticmethod
    def _destination_room(exit_obj, subject, room_registry=None):
        if exit_obj is None:
            return None
        registry = MovementApi._room_registry(subject, room_registry=room_registry)
        if registry is None:
            return None

        to_room_id = getattr(exit_obj, "to_room_id", None)
        if to_room_id:
            room = registry.get_or_none(id=to_room_id)
            if room is not None:
                return room

        to_room_vnum = getattr(exit_obj, "to_room_vnum", None)
        if to_room_vnum not in (None, ""):
            return registry.get_or_none(vnum=str(to_room_vnum))
        return None

    @staticmethod
    def _room_registry(subject, room_registry=None):
        if room_registry is not None:
            return room_registry

        context = MovementApi._context(subject)
        registry = getattr(context, "room_registry", None)
        if registry is not None:
            return registry

        for accessor_name in ("player_handler", "room_handler"):
            accessor = getattr(context, accessor_name, None)
            if accessor is None:
                continue
            try:
                handler = accessor()
            except TypeError:
                handler = None
            registry = getattr(handler, "room_registry", None)
            if registry is not None:
                return registry
        return None

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