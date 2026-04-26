from __future__ import annotations

from injector import inject

from game.GameData import GameData
from game.GenericUtil import GenericUtil
from game.RegistryService import RegistryService
from interp.Context import Context
from interp.commands.MovementUtil import MovementUtil
from mobile.MobileUtil import MobileUtil
from player.Character import Character
from player.CharacterMacros import CharacterMacros
from player.PlayerHelper import PlayerHelper
from server.LoggerFactory import LoggerFactory


class MovementCommands:
    @inject
    def __init__(self, registry_service: RegistryService, player_helper: PlayerHelper, game_data: GameData):
        self.__name__ = "MovementCommands"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry_service = registry_service
        self.room_registry = registry_service.room_registry
        self.player_helper = player_helper
        self.game_data = game_data
        self.exit_flags = None
        self.room_flags = None
        self.affected_bits = None
        self.act_bits = None
        self.sector_types = None

    def lazy_load(self):
        self.exit_flags = CharacterMacros.get_enum("exitFlags")
        self.room_flags = CharacterMacros.get_enum("roomFlags")
        self.affected_bits = CharacterMacros.get_enum("affectedBy")
        self.act_bits = CharacterMacros.get_enum("actBits")
        self.sector_types = CharacterMacros.get_enum("sectorTypes")

    def move_char(self, character: Character, direction: str, context: Context):
        blocked = CharacterMacros.movement_position_block_message(character)
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
        if pexit is None or not getattr(pexit, "to_room_vnum", None):
            context.finish()
            return {"to_char": "Alas, you cannot go that way.\r\n"}

        to_room = self.room_registry.get_or_none(vnum=str(pexit.to_room_vnum))
        if to_room is None:
            context.finish()
            return {"to_char": "Alas, you cannot go that way.\r\n"}

        ex_closed = MovementUtil.get_exit_flag(self.exit_flags, "EX_CLOSED", "CLOSED")
        ex_nopass = MovementUtil.get_exit_flag(self.exit_flags, "EX_NOPASS", "NOPASS")
        flags = GenericUtil.to_int(getattr(pexit, "exit_flags", 0), 0)
        pass_door = CharacterMacros.is_affected_by_name(character, self.affected_bits, "AFF_PASS_DOOR")
        if ex_closed and (flags & ex_closed) != 0 and ((not pass_door) or (ex_nopass and (flags & ex_nopass) != 0)):
            keyword = (getattr(pexit, "keyword", "") or "door")
            context.finish()
            return {"to_char": f"The {keyword} is closed.\r\n"}

        if CharacterMacros.is_room_private(to_room, self.room_flags):
            context.finish()
            return {"to_char": "That room is private right now.\r\n"}

        if not CharacterMacros.is_npc(character):
            if CharacterMacros.is_air_room(in_room, self.sector_types) or CharacterMacros.is_air_room(to_room, self.sector_types):
                if not CharacterMacros.is_affected_by_name(character, self.affected_bits, "AFF_FLYING") and not CharacterMacros.is_immortal(character):
                    context.finish()
                    return {"to_char": "You can't fly.\r\n"}

            if CharacterMacros.requires_boat(in_room, self.sector_types) or CharacterMacros.requires_boat(to_room, self.sector_types):
                if not CharacterMacros.is_affected_by_name(character, self.affected_bits, "AFF_FLYING") and not CharacterMacros.has_boat(character):
                    context.finish()
                    return {"to_char": "You need a boat to go there.\r\n"}

            move = (MovementUtil.sector_cost(in_room.sector_type) + MovementUtil.sector_cost(to_room.sector_type)) // 2
            if (CharacterMacros.is_affected_by_name(character, self.affected_bits, "AFF_FLYING")
                    or CharacterMacros.is_affected_by_name(character, self.affected_bits, "AFF_HASTE")):
                move //= 2
            if CharacterMacros.is_affected_by_name(character, self.affected_bits, "AFF_SLOW"):
                move *= 2
            move = max(1, move)

            if GenericUtil.to_int(getattr(character, "movement", 0), 0) < move:
                context.finish()
                return {"to_char": "You are too exhausted.\r\n"}
            character.movement -= move

        from_room_targets = self.player_helper.players_in_room(character, in_room)
        leave_msg = None
        if not CharacterMacros.is_affected_by_name(character, self.affected_bits,"AFF_SNEAK") and GenericUtil.to_int(getattr(character, "invis_level", 0), 0) < 51:
            leave_msg = f"{character.name} leaves {MovementUtil.DIR_NAME[door]}.\r\n"

        in_room.remove_player_from_room(character)
        to_room.add_player_to_room(character)
        character.room_id = to_room.id

        to_room_targets = self.player_helper.players_in_room(character, to_room)
        arrive_msg = None
        if not CharacterMacros.is_affected_by_name(character, self.affected_bits, "AFF_SNEAK") and GenericUtil.to_int(getattr(character, "invis_level", 0), 0) < 51:
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
        CharacterMacros.mirror_exit_flag(self.room_registry, room, ex, MovementUtil.REV_DIR, MovementUtil.find_exit, set_mask=ex_closed)
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
        CharacterMacros.mirror_exit_flag(self.room_registry, room, ex, MovementUtil.REV_DIR, MovementUtil.find_exit, set_mask=ex_closed)
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
        CharacterMacros.mirror_exit_flag(self.room_registry, room, ex, MovementUtil.REV_DIR, MovementUtil.find_exit, set_mask=ex_locked)
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
        CharacterMacros.mirror_exit_flag(self.room_registry, room, ex, MovementUtil.REV_DIR, MovementUtil.find_exit, clear_mask=ex_locked)
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
        CharacterMacros.mirror_exit_flag(self.room_registry, room, ex, MovementUtil.REV_DIR, MovementUtil.find_exit, clear_mask=ex_locked)
        context.finish()
        return {"to_char": "*Click*\r\n", "to_room": f"{character.name} picks the {ex.keyword or 'door'}.\r\n", "targets": self.player_helper.players_in_room(character, room)}

    def do_stand(self, character: Character, context: Context) -> str:
        pos = CharacterMacros.position_value(character)
        if pos <= CharacterMacros.pos_value("POS_STUNNED"):
            context.finish()
            return "You can't do that right now.\r\n"
        if pos == CharacterMacros.pos_value("POS_SLEEPING"):
            if CharacterMacros.is_affected_by_name(character, self.affected_bits, "AFF_SLEEP"):
                context.finish()
                return "You can't wake up!\r\n"
            CharacterMacros.set_position(character, "POS_STANDING")
            context.finish()
            return "You wake and stand up.\r\n"
        if pos in (CharacterMacros.pos_value("POS_RESTING"), CharacterMacros.pos_value("POS_SITTING")):
            CharacterMacros.set_position(character, "POS_STANDING")
            context.finish()
            return "You stand up.\r\n"
        if pos == CharacterMacros.pos_value("POS_STANDING"):
            context.finish()
            return "You are already standing.\r\n"
        if pos == CharacterMacros.pos_value("POS_FIGHTING"):
            context.finish()
            return "You are already fighting!\r\n"
        context.finish()
        return ""

    def do_rest(self, character: Character, context: Context) -> str:
        pos = CharacterMacros.position_value(character)
        if pos == CharacterMacros.pos_value("POS_FIGHTING"):
            context.finish()
            return "You are already fighting!\r\n"
        if pos == CharacterMacros.pos_value("POS_SLEEPING"):
            if CharacterMacros.is_affected_by_name(character, self.affected_bits, "AFF_SLEEP"):
                context.finish()
                return "You can't wake up!\r\n"
            CharacterMacros.set_position(character, "POS_RESTING")
            context.finish()
            return "You wake up and start resting.\r\n"
        if pos in (CharacterMacros.pos_value("POS_STANDING"), CharacterMacros.pos_value("POS_SITTING")):
            CharacterMacros.set_position(character, "POS_RESTING")
            context.finish()
            return "You rest.\r\n"
        context.finish()
        return "You are already resting.\r\n"

    def do_sit(self, character: Character, context: Context) -> str:
        pos = CharacterMacros.position_value(character)
        if pos == CharacterMacros.pos_value("POS_FIGHTING"):
            context.finish()
            return "Maybe you should finish this fight first?\r\n"
        if pos == CharacterMacros.pos_value("POS_SLEEPING"):
            if CharacterMacros.is_affected_by_name(character, self.affected_bits, "AFF_SLEEP"):
                context.finish()
                return "You can't wake up!\r\n"
            CharacterMacros.set_position(character, "POS_SITTING")
            context.finish()
            return "You wake and sit up.\r\n"
        if pos == CharacterMacros.pos_value("POS_RESTING"):
            CharacterMacros.set_position(character, "POS_SITTING")
            context.finish()
            return "You stop resting.\r\n"
        if pos == CharacterMacros.pos_value("POS_STANDING"):
            CharacterMacros.set_position(character, "POS_SITTING")
            context.finish()
            return "You sit down.\r\n"
        context.finish()
        return "You are already sitting down.\r\n"

    def do_sleep(self, character: Character, context: Context) -> str:
        pos = CharacterMacros.position_value(character)
        if pos == CharacterMacros.pos_value("POS_SLEEPING"):
            context.finish()
            return "You are already sleeping.\r\n"
        if pos == CharacterMacros.pos_value("POS_FIGHTING"):
            context.finish()
            return "You are already fighting!\r\n"
        CharacterMacros.set_position(character, "POS_SLEEPING")
        context.finish()
        return "You go to sleep.\r\n"

    def do_wake(self, character: Character, context: Context) -> dict:
        arg = (context.result if isinstance(context.result, str) else "").strip().lower()
        if not arg and context.parameters:
            arg = context.parameters[0].strip().lower()
        if not arg:
            return {"self_stand": True}
        if not CharacterMacros.is_awake(character):
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
        if CharacterMacros.is_awake(victim):
            context.finish()
            return {"to_char": f"{victim.name} is already awake.\r\n"}
        if CharacterMacros.is_affected_by_name(victim, self.affected_bits, "AFF_SLEEP"):
            context.finish()
            return {"to_char": f"You can't wake {victim.name}!\r\n"}

        CharacterMacros.set_position(victim, "POS_STANDING")
        context.finish()
        return {"to_char": f"You wake {victim.name}.\r\n", "to_victim": f"{character.name} wakes you.\r\n", "victim": victim}

    def do_sneak(self, character: Character, context: Context) -> str:
        CharacterMacros.set_affected_by_name(character, self.affected_bits, "AFF_SNEAK", True)
        context.finish()
        return "You attempt to move silently.\r\n"

    def do_hide(self, character: Character, context: Context) -> str:
        CharacterMacros.set_affected_by_name(character, self.affected_bits, "AFF_HIDE", True)
        context.finish()
        return "You attempt to hide.\r\n"

    def do_visible(self, character: Character, context: Context) -> str:
        CharacterMacros.set_affected_by_name(character, self.affected_bits, "AFF_HIDE", False)
        CharacterMacros.set_affected_by_name(character, self.affected_bits, "AFF_INVISIBLE", False)
        CharacterMacros.set_affected_by_name(character, self.affected_bits, "AFF_SNEAK", False)
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

    @staticmethod
    def _format_train_options(character: Character) -> str:
        attrs = getattr(character, "character_attributes", None)
        if attrs is None:
            return "You can train: hp mana.\r\n"

        options = []
        trainable_stats = (
            ("str", "strength", 0),
            ("int", "intelligence", 1),
            ("wis", "wisdom", 2),
            ("dex", "dexterity", 3),
            ("con", "constitution", 4),
        )
        for short_name, attr_name, stat_index in trainable_stats:
            current = GenericUtil.to_int(getattr(attrs, attr_name, 0), 0)
            max_train = CharacterMacros.get_max_train(character, stat_index, current)
            if current < max_train:
                options.append(short_name)

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

    def do_train(self, character: Character, context: Context) -> str | dict:
        if CharacterMacros.is_npc(character):
            context.finish()
            return ""

        raw = (context.result if isinstance(context.result, str) else "").strip().lower()
        if not raw and context.parameters:
            raw = " ".join(context.parameters).strip().lower()

        room = self.room_registry.get_or_none(id=character.room_id)
        act_bits = self.act_bits or CharacterMacros.get_enum("actBits")
        trainer_found = False
        if room is not None:
            train_bit = act_bits.ACT_TRAIN.value if act_bits is not None and hasattr(act_bits, "ACT_TRAIN") else 0
            for mob in room.mobiles.values():
                if MobileUtil.is_train_trainer(mob, train_bit):
                    trainer_found = True
                    break
        if not trainer_found:
            context.finish()
            return "You can't do that here.\r\n"

        attrs = getattr(character, "character_attributes", None)
        trains = GenericUtil.to_int(getattr(attrs, "trains", 0), 0) if attrs is not None else 0
        if raw == "":
            context.finish()
            return f"You have {trains} training sessions.\r\n{self._format_train_options(character)}"

        if attrs is None:
            context.finish()
            return "You can't do that.\r\n"

        if raw == "hp":
            if trains < 1:
                context.finish()
                return "You don't have enough training sessions.\r\n"
            attrs.trains = trains - 1
            character.max_hit = GenericUtil.to_int(getattr(character, "max_hit", 0), 0) + 10
            character.hit = GenericUtil.to_int(getattr(character, "hit", 0), 0) + 10
            context.finish()
            return {
                "to_char": "Your durability increases!\r\n",
                "to_room": f"{character.name}'s durability increases!\r\n",
                "targets": CharacterMacros.room_targets(character, room),
            }

        if raw == "mana":
            if trains < 1:
                context.finish()
                return "You don't have enough training sessions.\r\n"
            attrs.trains = trains - 1
            character.max_mana = GenericUtil.to_int(getattr(character, "max_mana", 0), 0) + 10
            character.mana = GenericUtil.to_int(getattr(character, "mana", 0), 0) + 10
            context.finish()
            return {
                "to_char": "Your power increases!\r\n",
                "to_room": f"{character.name}'s power increases!\r\n",
                "targets": CharacterMacros.room_targets(character, room),
            }

        stat_lookup = {
            "str": ("strength", "strength", 0),
            "strength": ("strength", "strength", 0),
            "int": ("intelligence", "intelligence", 1),
            "intelligence": ("intelligence", "intelligence", 1),
            "wis": ("wisdom", "wisdom", 2),
            "wisdom": ("wisdom", "wisdom", 2),
            "dex": ("dexterity", "dexterity", 3),
            "dexterity": ("dexterity", "dexterity", 3),
            "con": ("constitution", "constitution", 4),
            "constitution": ("constitution", "constitution", 4),
        }
        stat_spec = stat_lookup.get(raw)
        if stat_spec is None:
            context.finish()
            return self._format_train_options(character)

        attr_name, output_name, stat_index = stat_spec
        current = GenericUtil.to_int(getattr(attrs, attr_name, 0), 0)
        max_train = CharacterMacros.get_max_train(character, stat_index, current)
        if current >= max_train:
            context.finish()
            return f"Your {output_name} is already at maximum.\r\n"
        if trains < 1:
            context.finish()
            return "You don't have enough training sessions.\r\n"

        setattr(attrs, attr_name, current + 1)
        attrs.trains = trains - 1
        context.finish()
        return {
            "to_char": f"Your {output_name} increases!\r\n",
            "to_room": f"{character.name}'s {output_name} increases!\r\n",
            "targets": CharacterMacros.room_targets(character, room),
        }
