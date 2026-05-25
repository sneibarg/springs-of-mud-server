from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TYPE_CHECKING

from api.CharacterApi import CharacterApi
from api.GameApi import GameApi
from item.Item import Item
from util.GenericUtil import GenericUtil
from util.MovementUtil import MovementUtil

if TYPE_CHECKING:
    from area.Room import Room


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


@dataclass(frozen=True)
class DoorState:
    argument: str = ""
    room: Any = None
    door: int = -1
    exit_obj: Any = None
    flags: int = 0
    keyword: str = "door"
    key: int = -1
    has_key: bool = False
    closed_flag: int = 0
    locked_flag: int = 0
    pickproof_flag: int = 0


@dataclass(frozen=True)
class ContainerState:
    argument: str = ""
    item: Any = None
    flags: int = 0
    short: str = "container"
    key: int = -1
    has_key: bool = False
    closeable_flag: int = 0
    closed_flag: int = 0
    locked_flag: int = 0


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
        ex_closed = MovementApi.flag_value(exit_flags, "EX_CLOSED", "CLOSED")
        ex_nopass = MovementApi.flag_value(exit_flags, "EX_NOPASS", "NOPASS")
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
    def door_state(subject, room_registry=None, exit_flags=None) -> DoorState:
        character = MovementApi._character(subject)
        room: Room | None = MovementApi._room(subject, room_registry=room_registry)
        argument = MovementApi.argument_text(subject)
        door = -1 if room is None else room.find_door(argument)
        exit_obj = MovementUtil.find_exit(room, door) if door >= 0 else None
        flags = GenericUtil.to_int(getattr(exit_obj, "exit_flags", 0), 0) if exit_obj is not None else 0
        exit_flags = exit_flags or CharacterApi.get_enum("exitFlags")
        key = GenericUtil.to_int(getattr(exit_obj, "key", -1), -1) if exit_obj is not None else -1
        return DoorState(
            argument=argument,
            room=room,
            door=door,
            exit_obj=exit_obj,
            flags=flags,
            keyword=(getattr(exit_obj, "keyword", "") or "door") if exit_obj is not None else "door",
            key=key,
            has_key=MovementApi.has_key(character, key),
            closed_flag=MovementApi.flag_value(exit_flags, "EX_CLOSED", "CLOSED"),
            locked_flag=MovementApi.flag_value(exit_flags, "EX_LOCKED", "LOCKED"),
            pickproof_flag=MovementApi.flag_value(exit_flags, "EX_PICKPROOF", "PICKPROOF"),
        )

    @staticmethod
    def container_state(subject) -> ContainerState:
        character = MovementApi._character(subject)
        item = MovementApi.target_item(subject)
        flags = GenericUtil.to_int(getattr(item, "value1", 0), 0) if item is not None else 0
        key = GenericUtil.to_int(getattr(item, "value2", -1), -1) if item is not None else -1
        container_state = CharacterApi.get_enum("containerState")
        return ContainerState(
            argument=MovementApi.argument_text(subject),
            item=item,
            flags=flags,
            short=Item.short(item) if item is not None else "container",
            key=key,
            has_key=MovementApi.has_key(character, key),
            closeable_flag=MovementApi.flag_value(container_state, "CONT_CLOSEABLE"),
            closed_flag=MovementApi.flag_value(container_state, "CONT_CLOSED"),
            locked_flag=MovementApi.flag_value(container_state, "CONT_LOCKED"),
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
    def missing_argument(view) -> bool:
        return not MovementApi.argument_text(view)

    @staticmethod
    def invalid_door(view) -> bool:
        state = MovementApi.door_state(view)
        return state.exit_obj is None

    @staticmethod
    def has_target_item(view) -> bool:
        return MovementApi.target_item(view) is not None

    @staticmethod
    def is_container_target(view) -> bool:
        item = MovementApi.target_item(view)
        return item is not None and Item.is_container(item)

    @staticmethod
    def container_not_closeable(view) -> bool:
        state = MovementApi.container_state(view)
        return state.item is not None and state.closeable_flag != 0 and not MovementApi.has_flag(state.flags, state.closeable_flag)

    @staticmethod
    def container_already_closed(view) -> bool:
        state = MovementApi.container_state(view)
        return state.item is not None and state.closed_flag != 0 and MovementApi.has_flag(state.flags, state.closed_flag)

    @staticmethod
    def container_not_closed(view) -> bool:
        state = MovementApi.container_state(view)
        return state.item is not None and state.closed_flag != 0 and not MovementApi.has_flag(state.flags, state.closed_flag)

    @staticmethod
    def container_cannot_lock(view) -> bool:
        state = MovementApi.container_state(view)
        return state.item is not None and state.key < 0

    @staticmethod
    def container_missing_key(view) -> bool:
        state = MovementApi.container_state(view)
        return state.item is not None and state.key >= 0 and not state.has_key

    @staticmethod
    def container_already_locked(view) -> bool:
        state = MovementApi.container_state(view)
        return state.item is not None and state.locked_flag != 0 and MovementApi.has_flag(state.flags, state.locked_flag)

    @staticmethod
    def container_tokens(view) -> dict[str, Any]:
        return {"t": MovementApi.container_state(view).short}

    @staticmethod
    def door_already_open(view) -> bool:
        state = MovementApi.door_state(view)
        return state.exit_obj is not None and state.closed_flag and not MovementApi.has_flag(state.flags, state.closed_flag)

    @staticmethod
    def door_locked(view) -> bool:
        state = MovementApi.door_state(view)
        return state.exit_obj is not None and state.locked_flag and MovementApi.has_flag(state.flags, state.locked_flag)

    @staticmethod
    def door_already_closed(view) -> bool:
        state = MovementApi.door_state(view)
        return state.exit_obj is not None and state.closed_flag and MovementApi.has_flag(state.flags, state.closed_flag)

    @staticmethod
    def door_not_closed(view) -> bool:
        state = MovementApi.door_state(view)
        return state.exit_obj is not None and state.closed_flag and not MovementApi.has_flag(state.flags, state.closed_flag)

    # TO-DO with portals
    @staticmethod
    def invalid_portal(view):
        pass

    @staticmethod
    def is_portal(view):
        pass

    @staticmethod
    def door_cannot_lock(view) -> bool:
        state = MovementApi.door_state(view)
        return state.exit_obj is not None and state.key < 0

    @staticmethod
    def door_cannot_unlock(view) -> bool:
        return MovementApi.door_cannot_lock(view)

    @staticmethod
    def door_missing_key(view) -> bool:
        state = MovementApi.door_state(view)
        return state.exit_obj is not None and state.key >= 0 and not state.has_key

    @staticmethod
    def door_already_locked(view) -> bool:
        state = MovementApi.door_state(view)
        return state.exit_obj is not None and state.locked_flag and MovementApi.has_flag(state.flags, state.locked_flag)

    @staticmethod
    def door_already_unlocked(view) -> bool:
        state = MovementApi.door_state(view)
        return state.exit_obj is not None and state.locked_flag and not MovementApi.has_flag(state.flags, state.locked_flag)

    @staticmethod
    def door_pickproof(view) -> bool:
        state = MovementApi.door_state(view)
        return state.exit_obj is not None and state.pickproof_flag and MovementApi.has_flag(state.flags, state.pickproof_flag)

    @staticmethod
    def door_tokens(view) -> dict[str, Any]:
        return {"t": MovementApi.door_state(view).keyword}

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
    def has_key(character, key: int) -> bool:
        if character is None or key is None or GenericUtil.to_int(key, -1) < 0:
            return False
        if hasattr(character, "has_key"):
            return bool(character.has_key(key))
        wanted = str(key)
        for item in list(getattr(character, "loot", []) or []):
            if str(getattr(item, "vnum", "")) == wanted:
                return True
        return False

    @staticmethod
    def flag_value(enum_obj, *names: str) -> int:
        if enum_obj is None:
            return 0
        for name in names:
            member = getattr(enum_obj, name, None)
            if member is not None:
                return int(member.value)
        return 0

    @staticmethod
    def has_flag(value: int, mask: int) -> bool:
        return bool(mask and (GenericUtil.to_int(value, 0) & mask) != 0)

    @staticmethod
    def set_flag(value: int, mask: int) -> int:
        return GenericUtil.to_int(value, 0) | GenericUtil.to_int(mask, 0)

    @staticmethod
    def clear_flag(value: int, mask: int) -> int:
        return GenericUtil.to_int(value, 0) & ~GenericUtil.to_int(mask, 0)

    @staticmethod
    def update_exit_flags(room_registry, room, exit_obj, *, set_mask: int = 0, clear_mask: int = 0):
        if exit_obj is None:
            return

        flags = GenericUtil.to_int(getattr(exit_obj, "exit_flags", 0), 0)
        if clear_mask:
            flags = MovementApi.clear_flag(flags, clear_mask)
        if set_mask:
            flags = MovementApi.set_flag(flags, set_mask)
        exit_obj.exit_flags = flags
        MovementApi._mirror_exit_flags(room_registry, room, exit_obj, set_mask=set_mask, clear_mask=clear_mask)

    @staticmethod
    def open_exit(room_registry, room, exit_obj, exit_flags):
        MovementApi.update_exit_flags(
            room_registry,
            room,
            exit_obj,
            clear_mask=MovementApi.flag_value(exit_flags, "EX_CLOSED", "CLOSED"),
        )

    @staticmethod
    def close_exit(room_registry, room, exit_obj, exit_flags):
        MovementApi.update_exit_flags(
            room_registry,
            room,
            exit_obj,
            set_mask=MovementApi.flag_value(exit_flags, "EX_CLOSED", "CLOSED"),
        )

    @staticmethod
    def close_container(item):
        if item is None:
            return
        container_state = CharacterApi.get_enum("containerState")
        flags = GenericUtil.to_int(getattr(item, "value1", 0), 0)
        item.value1 = str(MovementApi.set_flag(flags, MovementApi.flag_value(container_state, "CONT_CLOSED")))

    @staticmethod
    def lock_exit(room_registry, room, exit_obj, exit_flags):
        MovementApi.update_exit_flags(
            room_registry,
            room,
            exit_obj,
            set_mask=MovementApi.flag_value(exit_flags, "EX_LOCKED", "LOCKED"),
        )

    @staticmethod
    def lock_container(item):
        if item is None:
            return
        container_state = CharacterApi.get_enum("containerState")
        flags = GenericUtil.to_int(getattr(item, "value1", 0), 0)
        item.value1 = str(MovementApi.set_flag(flags, MovementApi.flag_value(container_state, "CONT_LOCKED")))

    @staticmethod
    def unlock_exit(room_registry, room, exit_obj, exit_flags):
        MovementApi.update_exit_flags(
            room_registry,
            room,
            exit_obj,
            clear_mask=MovementApi.flag_value(exit_flags, "EX_LOCKED", "LOCKED"),
        )

    @staticmethod
    def argument_text(subject) -> str:
        context = MovementApi._context(subject)
        text = getattr(context, "result", "")
        argument = text.strip().lower() if isinstance(text, str) else ""
        parameters = list(getattr(context, "parameters", []) or [])
        if not argument and parameters:
            argument = str(parameters[0] or "").strip().lower()
        return argument

    @staticmethod
    def target_item(subject):
        context = MovementApi._context(subject)
        item = getattr(context, "target_item", None)
        if item is not None:
            return item

        room = MovementApi._room(subject)
        character = MovementApi._character(subject)
        argument = MovementApi.argument_text(subject)
        if not argument:
            return None

        inventory_item = None if character is None else character.find_inventory_item(argument)
        room_item = None if room is None else room.find_room_item(argument)
        item = inventory_item or room_item
        if context is not None:
            context.target_item = item
        return item

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
    def _room(subject, room_registry=None) -> Room | None:
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
    def _mirror_exit_flags(room_registry, room, ex, *, set_mask: int = 0, clear_mask: int = 0):
        if room_registry is None or room is None or ex is None:
            return
        to_room = room_registry.get_or_none(id=getattr(ex, "to_room_id", None))
        if to_room is None:
            return
        rev = MovementUtil.REV_DIR[int(getattr(ex, "direction", 0))]
        rev_exit = MovementUtil.find_exit(to_room, rev)
        if rev_exit is None or getattr(rev_exit, "to_room_id", None) != room.id:
            return
        flags = GenericUtil.to_int(getattr(rev_exit, "exit_flags", 0), 0)
        if clear_mask:
            flags = MovementApi.clear_flag(flags, clear_mask)
        if set_mask:
            flags = MovementApi.set_flag(flags, set_mask)
        rev_exit.exit_flags = flags
