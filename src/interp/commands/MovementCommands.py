from __future__ import annotations

from injector import inject

from game.GenericUtil import GenericUtil
from game.RegistryService import RegistryService
from interp.Context import Context
from interp.commands.MovementUtil import MovementUtil
from player.Character import Character
from player.CharacterMacros import CharacterMacros
from player.PlayerHelper import PlayerHelper
from server.LoggerFactory import LoggerFactory


class MovementCommands:
    @inject
    def __init__(self, registry_service: RegistryService, character_macros: CharacterMacros, player_helper: PlayerHelper):
        self.__name__ = "MovementCommands"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry_service = registry_service
        self.room_registry = registry_service.room_registry
        self.character_macros = character_macros
        self.player_helper = player_helper
        self.exit_flags = character_macros.enums.get("exitFlags")
        self.room_flags = character_macros.enums.get("roomFlags")
        self.affected_bits = character_macros.enums.get("affectedBy")
        self.act_bits = character_macros.enums.get("actBits")
        self.sector_types = character_macros.enums.get("sectorTypes")

    def move_char(self, character: Character, direction: str, context: Context):
        blocked = self._movement_position_block_message(character)
        if blocked:
            context.finish()
            return {"to_char": blocked}

        door = MovementUtil.direction_index(direction)
        if door < 0:
            context.finish()
            return {"to_char": "Alas, you cannot go that way.\r\n"}

        in_room = self.room_registry.get_or_none(id=character.room_id)
        if in_room is None:
            context.finish()
            return {"to_char": "Alas, you cannot go that way.\r\n"}

        pexit = MovementUtil.find_exit(in_room, door)
        if pexit is None or not getattr(pexit, "to_room_id", None):
            context.finish()
            return {"to_char": "Alas, you cannot go that way.\r\n"}

        to_room = self.room_registry.get_or_none(id=pexit.to_room_id)
        if to_room is None:
            context.finish()
            return {"to_char": "Alas, you cannot go that way.\r\n"}

        ex_closed = MovementUtil.get_exit_flag(self.exit_flags, "EX_CLOSED", "CLOSED")
        ex_nopass = MovementUtil.get_exit_flag(self.exit_flags, "EX_NOPASS", "NOPASS")
        flags = GenericUtil.to_int(getattr(pexit, "exit_flags", 0), 0)
        pass_door = self._is_affected(character, "AFF_PASS_DOOR")
        if ex_closed and (flags & ex_closed) != 0 and ((not pass_door) or (ex_nopass and (flags & ex_nopass) != 0)):
            keyword = (getattr(pexit, "keyword", "") or "door")
            context.finish()
            return {"to_char": f"The {keyword} is closed.\r\n"}

        if self._is_room_private(to_room):
            context.finish()
            return {"to_char": "That room is private right now.\r\n"}

        if not self.character_macros.is_npc(character):
            if self._is_air_room(in_room) or self._is_air_room(to_room):
                if not self._is_affected(character, "AFF_FLYING") and not self.character_macros.is_immortal(character):
                    context.finish()
                    return {"to_char": "You can't fly.\r\n"}

            if self._requires_boat(in_room) or self._requires_boat(to_room):
                if not self._is_affected(character, "AFF_FLYING") and not self._has_boat(character):
                    context.finish()
                    return {"to_char": "You need a boat to go there.\r\n"}

            move = (MovementUtil.sector_cost(in_room.sector_type) + MovementUtil.sector_cost(to_room.sector_type)) // 2
            if self._is_affected(character, "AFF_FLYING") or self._is_affected(character, "AFF_HASTE"):
                move //= 2
            if self._is_affected(character, "AFF_SLOW"):
                move *= 2
            move = max(1, move)

            if GenericUtil.to_int(getattr(character, "movement", 0), 0) < move:
                context.finish()
                return {"to_char": "You are too exhausted.\r\n"}
            character.movement -= move

        from_room_targets = self.player_helper.players_in_room(character, in_room)
        leave_msg = None
        if not self._is_affected(character, "AFF_SNEAK") and GenericUtil.to_int(getattr(character, "invis_level", 0), 0) < 51:
            leave_msg = f"{character.name} leaves {MovementUtil.DIR_NAME[door]}.\r\n"

        in_room.remove_player_from_room(character)
        to_room.add_player_to_room(character)
        character.room_id = to_room.id

        to_room_targets = self.player_helper.players_in_room(character, to_room)
        arrive_msg = None
        if not self._is_affected(character, "AFF_SNEAK") and GenericUtil.to_int(getattr(character, "invis_level", 0), 0) < 51:
            arrive_msg = f"{character.name} has arrived.\r\n"

        return {
            "from_room_targets": from_room_targets,
            "from_room_message": leave_msg,
            "to_room_targets": to_room_targets,
            "to_room_message": arrive_msg,
            "to_room_obj": to_room,
        }

    def do_north(self, character: Character, context: Context):
        return self.move_char(character, "north", context)

    def do_east(self, character: Character, context: Context):
        return self.move_char(character, "east", context)

    def do_south(self, character: Character, context: Context):
        return self.move_char(character, "south", context)

    def do_west(self, character: Character, context: Context):
        return self.move_char(character, "west", context)

    def do_up(self, character: Character, context: Context):
        return self.move_char(character, "up", context)

    def do_down(self, character: Character, context: Context):
        return self.move_char(character, "down", context)

    def do_open(self, character: Character, context: Context) -> dict:
        arg = (context.result if isinstance(context.result, str) else "").strip().lower()
        if not arg and context.parameters:
            arg = context.parameters[0].strip().lower()
        if not arg:
            context.finish()
            return {"to_char": "Open what?\r\n"}

        room = self.room_registry.get_or_none(id=character.room_id)
        door = MovementUtil.find_door(room, arg)
        if door < 0:
            context.finish()
            return {"to_char": "I see no door here.\r\n"}

        ex = MovementUtil.find_exit(room, door)
        flags = GenericUtil.to_int(getattr(ex, "exit_flags", 0), 0)
        ex_closed = MovementUtil.get_exit_flag(self.exit_flags, "EX_CLOSED", "CLOSED")
        ex_locked = MovementUtil.get_exit_flag(self.exit_flags, "EX_LOCKED", "LOCKED")
        if ex_closed and (flags & ex_closed) == 0:
            context.finish()
            return {"to_char": "It's already open.\r\n"}
        if ex_locked and (flags & ex_locked) != 0:
            context.finish()
            return {"to_char": "It's locked.\r\n"}

        ex.exit_flags = flags & ~ex_closed if ex_closed else flags
        self._mirror_exit_flag(room, ex, clear_mask=ex_closed)
        context.finish()
        return {"to_char": "Ok.\r\n", "to_room": f"{character.name} opens the {ex.keyword or 'door'}.\r\n", "targets": self.player_helper.players_in_room(character, room)}

    def do_close(self, character: Character, context: Context) -> dict:
        arg = (context.result if isinstance(context.result, str) else "").strip().lower()
        if not arg and context.parameters:
            arg = context.parameters[0].strip().lower()
        if not arg:
            context.finish()
            return {"to_char": "Close what?\r\n"}

        room = self.room_registry.get_or_none(id=character.room_id)
        door = MovementUtil.find_door(room, arg)
        if door < 0:
            context.finish()
            return {"to_char": "I see no door here.\r\n"}

        ex = MovementUtil.find_exit(room, door)
        flags = GenericUtil.to_int(getattr(ex, "exit_flags", 0), 0)
        ex_closed = MovementUtil.get_exit_flag(self.exit_flags, "EX_CLOSED", "CLOSED")
        if ex_closed and (flags & ex_closed) != 0:
            context.finish()
            return {"to_char": "It's already closed.\r\n"}

        ex.exit_flags = flags | ex_closed if ex_closed else flags
        self._mirror_exit_flag(room, ex, set_mask=ex_closed)
        context.finish()
        return {"to_char": "Ok.\r\n", "to_room": f"{character.name} closes the {ex.keyword or 'door'}.\r\n", "targets": self.player_helper.players_in_room(character, room)}

    def do_lock(self, character: Character, context: Context) -> dict:
        arg = (context.result if isinstance(context.result, str) else "").strip().lower()
        if not arg and context.parameters:
            arg = context.parameters[0].strip().lower()
        if not arg:
            context.finish()
            return {"to_char": "Lock what?\r\n"}

        room = self.room_registry.get_or_none(id=character.room_id)
        door = MovementUtil.find_door(room, arg)
        if door < 0:
            context.finish()
            return {"to_char": "I see no door here.\r\n"}

        ex = MovementUtil.find_exit(room, door)
        flags = GenericUtil.to_int(getattr(ex, "exit_flags", 0), 0)
        ex_closed = MovementUtil.get_exit_flag(self.exit_flags, "EX_CLOSED", "CLOSED")
        ex_locked = MovementUtil.get_exit_flag(self.exit_flags, "EX_LOCKED", "LOCKED")
        key = GenericUtil.to_int(getattr(ex, "key", -1), -1)

        if ex_closed and (flags & ex_closed) == 0:
            context.finish()
            return {"to_char": "It's not closed.\r\n"}
        if key < 0:
            context.finish()
            return {"to_char": "It can't be locked.\r\n"}
        if not MovementUtil.has_key(character, key):
            context.finish()
            return {"to_char": "You lack the key.\r\n"}
        if ex_locked and (flags & ex_locked) != 0:
            context.finish()
            return {"to_char": "It's already locked.\r\n"}

        ex.exit_flags = flags | ex_locked if ex_locked else flags
        self._mirror_exit_flag(room, ex, set_mask=ex_locked)
        context.finish()
        return {"to_char": "*Click*\r\n", "to_room": f"{character.name} locks the {ex.keyword or 'door'}.\r\n", "targets": self.player_helper.players_in_room(character, room)}

    def do_unlock(self, character: Character, context: Context) -> dict:
        arg = (context.result if isinstance(context.result, str) else "").strip().lower()
        if not arg and context.parameters:
            arg = context.parameters[0].strip().lower()
        if not arg:
            context.finish()
            return {"to_char": "Unlock what?\r\n"}

        room = self.room_registry.get_or_none(id=character.room_id)
        door = MovementUtil.find_door(room, arg)
        if door < 0:
            context.finish()
            return {"to_char": "I see no door here.\r\n"}

        ex = MovementUtil.find_exit(room, door)
        flags = GenericUtil.to_int(getattr(ex, "exit_flags", 0), 0)
        ex_closed = MovementUtil.get_exit_flag(self.exit_flags, "EX_CLOSED", "CLOSED")
        ex_locked = MovementUtil.get_exit_flag(self.exit_flags, "EX_LOCKED", "LOCKED")
        key = GenericUtil.to_int(getattr(ex, "key", -1), -1)

        if ex_closed and (flags & ex_closed) == 0:
            context.finish()
            return {"to_char": "It's not closed.\r\n"}
        if key < 0:
            context.finish()
            return {"to_char": "It can't be unlocked.\r\n"}
        if not MovementUtil.has_key(character, key):
            context.finish()
            return {"to_char": "You lack the key.\r\n"}
        if ex_locked and (flags & ex_locked) == 0:
            context.finish()
            return {"to_char": "It's already unlocked.\r\n"}

        ex.exit_flags = flags & ~ex_locked if ex_locked else flags
        self._mirror_exit_flag(room, ex, clear_mask=ex_locked)
        context.finish()
        return {"to_char": "*Click*\r\n", "to_room": f"{character.name} unlocks the {ex.keyword or 'door'}.\r\n", "targets": self.player_helper.players_in_room(character, room)}

    def do_pick(self, character: Character, context: Context) -> dict:
        arg = (context.result if isinstance(context.result, str) else "").strip().lower()
        if not arg and context.parameters:
            arg = context.parameters[0].strip().lower()
        if not arg:
            context.finish()
            return {"to_char": "Pick what?\r\n"}

        room = self.room_registry.get_or_none(id=character.room_id)
        door = MovementUtil.find_door(room, arg)
        if door < 0:
            context.finish()
            return {"to_char": "I see no door here.\r\n"}

        ex = MovementUtil.find_exit(room, door)
        flags = GenericUtil.to_int(getattr(ex, "exit_flags", 0), 0)
        ex_closed = MovementUtil.get_exit_flag(self.exit_flags, "EX_CLOSED", "CLOSED")
        ex_locked = MovementUtil.get_exit_flag(self.exit_flags, "EX_LOCKED", "LOCKED")
        ex_pickproof = MovementUtil.get_exit_flag(self.exit_flags, "EX_PICKPROOF", "PICKPROOF")

        if ex_closed and (flags & ex_closed) == 0:
            context.finish()
            return {"to_char": "It's not closed.\r\n"}
        if ex_locked and (flags & ex_locked) == 0:
            context.finish()
            return {"to_char": "It's already unlocked.\r\n"}
        if ex_pickproof and (flags & ex_pickproof) != 0:
            context.finish()
            return {"to_char": "You failed.\r\n"}

        ex.exit_flags = flags & ~ex_locked if ex_locked else flags
        self._mirror_exit_flag(room, ex, clear_mask=ex_locked)
        context.finish()
        return {"to_char": "*Click*\r\n", "to_room": f"{character.name} picks the {ex.keyword or 'door'}.\r\n", "targets": self.player_helper.players_in_room(character, room)}

    def do_stand(self, character: Character, context: Context) -> str:
        pos = self._position(character)
        if pos <= self._pos("POS_STUNNED"):
            context.finish()
            return "You can't do that right now.\r\n"
        if pos == self._pos("POS_SLEEPING"):
            if self._is_affected(character, "AFF_SLEEP"):
                context.finish()
                return "You can't wake up!\r\n"
            self._set_position(character, "POS_STANDING")
            context.finish()
            return "You wake and stand up.\r\n"
        if pos in (self._pos("POS_RESTING"), self._pos("POS_SITTING")):
            self._set_position(character, "POS_STANDING")
            context.finish()
            return "You stand up.\r\n"
        if pos == self._pos("POS_STANDING"):
            context.finish()
            return "You are already standing.\r\n"
        if pos == self._pos("POS_FIGHTING"):
            context.finish()
            return "You are already fighting!\r\n"
        context.finish()
        return ""

    def do_rest(self, character: Character, context: Context) -> str:
        pos = self._position(character)
        if pos == self._pos("POS_FIGHTING"):
            context.finish()
            return "You are already fighting!\r\n"
        if pos == self._pos("POS_SLEEPING"):
            if self._is_affected(character, "AFF_SLEEP"):
                context.finish()
                return "You can't wake up!\r\n"
            self._set_position(character, "POS_RESTING")
            context.finish()
            return "You wake up and start resting.\r\n"
        if pos in (self._pos("POS_STANDING"), self._pos("POS_SITTING")):
            self._set_position(character, "POS_RESTING")
            context.finish()
            return "You rest.\r\n"
        context.finish()
        return "You are already resting.\r\n"

    def do_sit(self, character: Character, context: Context) -> str:
        pos = self._position(character)
        if pos == self._pos("POS_FIGHTING"):
            context.finish()
            return "Maybe you should finish this fight first?\r\n"
        if pos == self._pos("POS_SLEEPING"):
            if self._is_affected(character, "AFF_SLEEP"):
                context.finish()
                return "You can't wake up!\r\n"
            self._set_position(character, "POS_SITTING")
            context.finish()
            return "You wake and sit up.\r\n"
        if pos == self._pos("POS_RESTING"):
            self._set_position(character, "POS_SITTING")
            context.finish()
            return "You stop resting.\r\n"
        if pos == self._pos("POS_STANDING"):
            self._set_position(character, "POS_SITTING")
            context.finish()
            return "You sit down.\r\n"
        context.finish()
        return "You are already sitting down.\r\n"

    def do_sleep(self, character: Character, context: Context) -> str:
        pos = self._position(character)
        if pos == self._pos("POS_SLEEPING"):
            context.finish()
            return "You are already sleeping.\r\n"
        if pos == self._pos("POS_FIGHTING"):
            context.finish()
            return "You are already fighting!\r\n"
        self._set_position(character, "POS_SLEEPING")
        context.finish()
        return "You go to sleep.\r\n"

    def do_wake(self, character: Character, context: Context) -> dict:
        arg = (context.result if isinstance(context.result, str) else "").strip().lower()
        if not arg and context.parameters:
            arg = context.parameters[0].strip().lower()
        if not arg:
            return {"self_stand": True}
        if not self.character_macros.is_awake(character):
            context.finish()
            return {"to_char": "You are asleep yourself!\r\n"}

        room = self.room_registry.get_or_none(id=character.room_id)
        victim = None
        if room is not None:
            for ch in room.characters.values():
                name = (ch.name or "").lower()
                if name == arg or name.startswith(arg):
                    victim = ch
                    break
        if victim is None:
            context.finish()
            return {"to_char": "They aren't here.\r\n"}
        if self.character_macros.is_awake(victim):
            context.finish()
            return {"to_char": f"{victim.name} is already awake.\r\n"}
        if self._is_affected(victim, "AFF_SLEEP"):
            context.finish()
            return {"to_char": f"You can't wake {victim.name}!\r\n"}

        self._set_position(victim, "POS_STANDING")
        context.finish()
        return {"to_char": f"You wake {victim.name}.\r\n", "to_victim": f"{character.name} wakes you.\r\n", "victim": victim}

    def do_sneak(self, character: Character, context: Context) -> str:
        self._set_affected(character, "AFF_SNEAK", True)
        context.finish()
        return "You attempt to move silently.\r\n"

    def do_hide(self, character: Character, context: Context) -> str:
        self._set_affected(character, "AFF_HIDE", True)
        context.finish()
        return "You attempt to hide.\r\n"

    def do_visible(self, character: Character, context: Context) -> str:
        self._set_affected(character, "AFF_HIDE", False)
        self._set_affected(character, "AFF_INVISIBLE", False)
        self._set_affected(character, "AFF_SNEAK", False)
        context.finish()
        return "Ok.\r\n"

    def do_recall(self, character: Character, context: Context):
        room_flags = self.room_flags
        temple_vnum = "3001"
        destination = None
        for room in self.room_registry.all_rooms():
            r = self.room_registry.get_or_none(id=room)
            if r is not None and str(getattr(r, "vnum", "")) == temple_vnum:
                destination = r
                break
        if destination is None:
            context.finish()
            return {"to_char": "You are completely lost.\r\n"}

        current = self.room_registry.get_or_none(id=character.room_id)
        if current is None or current.id == destination.id:
            context.finish()
            return {"to_char": ""}

        no_recall = MovementUtil.get_exit_flag(room_flags, "ROOM_NO_RECALL")
        if no_recall and (GenericUtil.to_int(current.room_flags, 0) & no_recall) != 0:
            context.finish()
            return {"to_char": "Mota has forsaken you.\r\n"}

        from_targets = self.player_helper.players_in_room(character, current)
        current.remove_player_from_room(character)
        destination.add_player_to_room(character)
        character.room_id = destination.id
        character.movement = max(0, GenericUtil.to_int(getattr(character, "movement", 0), 0) // 2)
        to_targets = self.player_helper.players_in_room(character, destination)
        return {
            "from_room_targets": from_targets,
            "from_room_message": f"{character.name} disappears.\r\n",
            "to_room_targets": to_targets,
            "to_room_message": f"{character.name} appears in the room.\r\n",
            "to_room_obj": destination,
        }

    def do_train(self, character: Character, context: Context) -> str:
        if self.character_macros.is_npc(character):
            context.finish()
            return ""
        raw = (context.result if isinstance(context.result, str) else "").strip().lower()
        if not raw and context.parameters:
            raw = " ".join(context.parameters).strip().lower()

        room = self.room_registry.get_or_none(id=character.room_id)
        trainer_found = False
        if room is not None and self.act_bits is not None and hasattr(self.act_bits, "ACT_TRAIN"):
            train_bit = self.act_bits.ACT_TRAIN.value
            for mob in room.mobiles.values():
                mob_flags = GenericUtil.to_int(getattr(getattr(mob, "mobile_flags", None), "act", 0), 0)
                if self.character_macros.is_set(mob_flags, train_bit):
                    trainer_found = True
                    break
        if not trainer_found:
            context.finish()
            return "You can't do that here.\r\n"

        attrs = getattr(character, "character_attributes", None)
        trains = GenericUtil.to_int(getattr(attrs, "trains", 0), 0) if attrs is not None else 0
        if raw == "":
            context.finish()
            return f"You have {trains} training sessions.\r\n"
        context.finish()
        return "Training specialization is not implemented yet.\r\n"

    def _mirror_exit_flag(self, room, ex, set_mask: int = 0, clear_mask: int = 0):
        to_room = self.room_registry.get_or_none(id=getattr(ex, "to_room_id", None))
        if to_room is None:
            return
        rev = MovementUtil.REV_DIR[int(getattr(ex, "direction", 0))]
        rev_exit = MovementUtil.find_exit(to_room, rev)
        if rev_exit is None or getattr(rev_exit, "to_room_id", None) != room.id:
            return
        flags = GenericUtil.to_int(getattr(rev_exit, "exit_flags", 0), 0)
        if clear_mask:
            flags &= ~clear_mask
        if set_mask:
            flags |= set_mask
        rev_exit.exit_flags = flags

    def _is_room_private(self, room) -> bool:
        if room is None:
            return False
        private = MovementUtil.get_exit_flag(self.room_flags, "ROOM_PRIVATE")
        solitary = MovementUtil.get_exit_flag(self.room_flags, "ROOM_SOLITARY")
        flags = GenericUtil.to_int(getattr(room, "room_flags", 0), 0)
        if private and (flags & private) and len(getattr(room, "characters", {})) >= 2:
            return True
        if solitary and (flags & solitary) and len(getattr(room, "characters", {})) >= 1:
            return True
        return False

    def _is_air_room(self, room) -> bool:
        if room is None or self.sector_types is None:
            return False
        air = getattr(self.sector_types, "SECT_AIR", None)
        return air is not None and GenericUtil.to_int(getattr(room, "sector_type", 0), 0) == int(air.value)

    def _requires_boat(self, room) -> bool:
        if room is None or self.sector_types is None:
            return False
        no_swim = getattr(self.sector_types, "SECT_WATER_NOSWIM", None)
        return no_swim is not None and GenericUtil.to_int(getattr(room, "sector_type", 0), 0) == int(no_swim.value)

    @staticmethod
    def _has_boat(character: Character) -> bool:
        for item in list(getattr(character, "loot", []) or []):
            item_type = str(getattr(item, "item_type", "") or "").lower()
            if "boat" in item_type:
                return True
        return False

    def _is_affected(self, character: Character, bit_name: str) -> bool:
        if self.affected_bits is None or not hasattr(self.affected_bits, bit_name):
            return False
        bit = getattr(self.affected_bits, bit_name).value
        return self.character_macros.is_set(
            GenericUtil.to_int(self.character_macros.convert_flags(getattr(character.character_flags, "affected_by", "")), 0),
            bit,
        )

    def _set_affected(self, character: Character, bit_name: str, enabled: bool):
        if self.affected_bits is None or not hasattr(self.affected_bits, bit_name):
            return
        bit = getattr(self.affected_bits, bit_name).value
        raw = GenericUtil.to_int(self.character_macros.convert_flags(getattr(character.character_flags, "affected_by", "")), 0)
        raw = self.character_macros.set_bit(raw, bit) if enabled else self.character_macros.unset_bit(raw, bit)
        character.character_flags.affected_by = GenericUtil.flags_to_letters(raw)

    def _position(self, character: Character) -> int:
        attrs = getattr(character, "character_attributes", None)
        raw = getattr(attrs, "position", None)
        if raw is None:
            raw = getattr(character, "position", None)
        if isinstance(raw, str):
            name = raw.strip().upper()
            if name and not name.startswith("POS_"):
                name = f"POS_{name}"
            if self.character_macros.PositionsEnum is not None and hasattr(self.character_macros.PositionsEnum, name):
                return int(getattr(self.character_macros.PositionsEnum, name).value)
        standing = self._pos("POS_STANDING")
        default_pos = standing if standing >= 0 else 0
        return GenericUtil.to_int(raw, default_pos)

    def _movement_position_block_message(self, character: Character) -> str:
        pos = self._position(character)
        if pos == self._pos("POS_DEAD"):
            return "Lie still; you are DEAD.\r\n"
        if pos in (self._pos("POS_MORTAL"), self._pos("POS_INCAP")):
            return "You are hurt far too bad for that.\r\n"
        if pos == self._pos("POS_STUNNED"):
            return "You are too stunned to do that.\r\n"
        if pos == self._pos("POS_SLEEPING"):
            return "In your dreams, or what?\r\n"
        if pos == self._pos("POS_RESTING"):
            return "Nah... You feel too relaxed...\r\n"
        if pos == self._pos("POS_SITTING"):
            return "Better stand up first.\r\n"
        if pos == self._pos("POS_FIGHTING"):
            return "No way! You are still fighting!\r\n"
        return ""

    def _set_position(self, character: Character, pos_name: str):
        if self.character_macros.PositionsEnum is None or not hasattr(self.character_macros.PositionsEnum, pos_name):
            return
        value = int(getattr(self.character_macros.PositionsEnum, pos_name).value)
        attrs = getattr(character, "character_attributes", None)
        if attrs is not None:
            attrs.position = value
        # Keep parity with any legacy paths still reading/writing character.position directly.
        setattr(character, "position", value)

    def _pos(self, name: str) -> int:
        if self.character_macros.PositionsEnum is None or not hasattr(self.character_macros.PositionsEnum, name):
            return -1
        return int(getattr(self.character_macros.PositionsEnum, name).value)
