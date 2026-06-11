from __future__ import annotations

from injector import inject

from game.EnumProvider import EnumProvider
from game.GameData import GameData
from util.GenericUtil import GenericUtil
from game.RegistryService import RegistryService
from interp.Context import Context
from api.InterpApi import InterpApi
from api.MovementApi import MovementApi
from fight.FightHandler import FightHandler
from item.Item import Item
from util.MobileUtil import MobileUtil
from util.PlayerUtil import PlayerUtil
from player.Character import Character
from api.CharacterApi import CharacterApi
from server.LoggerFactory import LoggerFactory


class Movement:
    @inject
    def __init__(self,
                 registry_service: RegistryService,
                 game_data: GameData,
                 fight_handler: FightHandler,
                 enum_provider: EnumProvider,
                 interp_api: InterpApi):
        self.__name__ = "Movement"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry_service = registry_service
        self.room_registry = registry_service.room_registry
        self.game_data = game_data
        self.fight_handler = fight_handler
        self.interp_api = interp_api
        self.exit_flags = enum_provider.get("exitFlags")
        self.room_flags = enum_provider.get("roomFlags")
        self.affected_bits = enum_provider.get("affectedBy")
        self.act_bits = enum_provider.get("actBits")
        self.sector_types = enum_provider.get("sectorTypes")

    def move_char(self, character: Character, direction: str, context: Context):
        state = MovementApi.move_state(context, direction=direction, room_registry=self.room_registry)
        context.room = state.in_room
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked

        if not CharacterApi.is_npc(character):
            character.movement -= state.move_cost

        in_room = state.in_room
        to_room = state.to_room
        from_room_targets = in_room.player_targets(character)
        in_room.remove_player_from_room(character)
        to_room.add_player_to_room(character)
        character.room_id = to_room.id

        to_room_targets = to_room.player_targets(character)
        context.finish()
        return {
            "payloads": [
                self._command_payload(
                    "default",
                    channel="to_room",
                    targets=from_room_targets,
                    tokens=self._actor_tokens(character),
                ),
                self._command_payload(
                    "arrived",
                    channel="to_room",
                    targets=to_room_targets,
                    tokens=self._actor_tokens(character),
                    to_room_obj=to_room,
                    aggressive_rounds=self.fight_handler.aggressive_entry_rounds(character, to_room),
                ),
            ]
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
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked

        state = MovementApi.door_state(context, room_registry=self.room_registry, exit_flags=self.exit_flags)
        room = state.room
        ex = state.exit_obj
        MovementApi.open_exit(self.room_registry, room, ex, self.exit_flags)
        context.finish()
        return self._command_payload(
            "open_door",
            targets=self._room_targets(room, character),
            tokens=self._actor_door_tokens(character, state.keyword),
        )

    def do_close(self, character: Character, context: Context) -> dict:
        room = self._room(character, context)
        context.target_item = MovementApi.target_item(context)
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked

        target_item = getattr(context, "target_item", None)
        if target_item is not None:
            MovementApi.close_container(target_item)
            context.finish()
            return self._command_payload(
                "close_container",
                targets=self._room_targets(room, character),
                tokens=self._actor_item_tokens(character, Item.short(target_item)),
            )

        state = MovementApi.door_state(context, room_registry=self.room_registry, exit_flags=self.exit_flags)
        room = state.room
        ex = state.exit_obj
        MovementApi.close_exit(self.room_registry, room, ex, self.exit_flags)
        context.finish()
        return self._command_payload(
            "close_door",
            targets=self._room_targets(room, character),
            tokens=self._actor_door_tokens(character, state.keyword),
        )

    def do_lock(self, character: Character, context: Context) -> dict:
        room = self._room(character, context)
        context.target_item = MovementApi.target_item(context)
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked

        target_item = getattr(context, "target_item", None)
        if target_item is not None:
            MovementApi.lock_container(target_item)
            context.finish()
            return self._command_payload(
                "container_locked",
                targets=self._room_targets(room, character),
                tokens=self._actor_item_tokens(character, Item.short(target_item)),
            )

        state = MovementApi.door_state(context, room_registry=self.room_registry, exit_flags=self.exit_flags)
        room = state.room
        ex = state.exit_obj
        MovementApi.lock_exit(self.room_registry, room, ex, self.exit_flags)
        context.finish()
        return self._command_payload(
            "exit_locked",
            targets=self._room_targets(room, character),
            tokens=self._actor_door_tokens(character, state.keyword),
        )

    def do_unlock(self, character: Character, context: Context) -> dict:
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked

        state = MovementApi.door_state(context, room_registry=self.room_registry, exit_flags=self.exit_flags)
        room = state.room
        ex = state.exit_obj
        MovementApi.unlock_exit(self.room_registry, room, ex, self.exit_flags)
        context.finish()
        return {
            "payloads": [
                self._command_payload("click", channel="to_char"),
                self._command_payload(
                    "unlocks_exit",
                    channel="to_room",
                    targets=self._room_targets(room, character),
                    tokens=self._actor_door_tokens(character, state.keyword),
                ),
            ]
        }

    def do_pick(self, character: Character, context: Context) -> dict:
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked

        state = MovementApi.door_state(context, room_registry=self.room_registry, exit_flags=self.exit_flags)
        room = state.room
        ex = state.exit_obj
        MovementApi.unlock_exit(self.room_registry, room, ex, self.exit_flags)
        context.finish()
        return self._command_payload(
            "door_picked",
            targets=self._room_targets(room, character),
            tokens=self._actor_door_tokens(character, state.keyword),
        )

    def do_stand(self, character: Character, context: Context) -> dict:
        pos = CharacterApi.position_value(character)
        if pos <= CharacterApi.pos_value("POS_STUNNED"):
            context.finish()
            return self._command_payload("can_t_do_that_right_now", channel="to_char")
        if pos == CharacterApi.pos_value("POS_SLEEPING"):
            if CharacterApi.is_affected_by_name(character, self.affected_bits, "AFF_SLEEP"):
                context.finish()
                return self._command_payload("can_t_wake_up", channel="to_char")
            CharacterApi.set_position(character, "POS_STANDING")
            context.finish()
            return self._command_payload("wake_stand_up", channel="to_char")
        if pos in (CharacterApi.pos_value("POS_RESTING"), CharacterApi.pos_value("POS_SITTING")):
            CharacterApi.set_position(character, "POS_STANDING")
            context.finish()
            return self._command_payload("stand_up", channel="to_char")
        if pos == CharacterApi.pos_value("POS_STANDING"):
            context.finish()
            return self._command_payload("already_standing", channel="to_char")
        if pos == CharacterApi.pos_value("POS_FIGHTING"):
            context.finish()
            return self._command_payload("already_fighting", channel="to_char")
        context.finish()
        return {}

    def do_rest(self, character: Character, context: Context) -> dict:
        pos = CharacterApi.position_value(character)
        if pos == CharacterApi.pos_value("POS_FIGHTING"):
            context.finish()
            return self._command_payload("already_fighting", channel="to_char")
        if pos == CharacterApi.pos_value("POS_SLEEPING"):
            if CharacterApi.is_affected_by_name(character, self.affected_bits, "AFF_SLEEP"):
                context.finish()
                return self._command_payload("can_t_wake_up", channel="to_char")
            CharacterApi.set_position(character, "POS_RESTING")
            context.finish()
            return self._command_payload("wake_up_start_resting", channel="to_char")
        if pos in (CharacterApi.pos_value("POS_STANDING"), CharacterApi.pos_value("POS_SITTING")):
            CharacterApi.set_position(character, "POS_RESTING")
            context.finish()
            return self._command_payload("rest", channel="to_char")
        context.finish()
        return self._command_payload("already_resting", channel="to_char")

    def do_sit(self, character: Character, context: Context) -> dict:
        pos = CharacterApi.position_value(character)
        if pos == CharacterApi.pos_value("POS_FIGHTING"):
            context.finish()
            return self._command_payload("maybe_should_finish_fight", channel="to_char")
        if pos == CharacterApi.pos_value("POS_SLEEPING"):
            if CharacterApi.is_affected_by_name(character, self.affected_bits, "AFF_SLEEP"):
                context.finish()
                return self._command_payload("can_t_wake_up", channel="to_char")
            CharacterApi.set_position(character, "POS_SITTING")
            context.finish()
            return self._command_payload("wake_sit_up", channel="to_char")
        if pos == CharacterApi.pos_value("POS_RESTING"):
            CharacterApi.set_position(character, "POS_SITTING")
            context.finish()
            return self._command_payload("stop_resting", channel="to_char")
        if pos == CharacterApi.pos_value("POS_STANDING"):
            CharacterApi.set_position(character, "POS_SITTING")
            context.finish()
            return self._command_payload("sit_down", channel="to_char")
        context.finish()
        return self._command_payload("already_sitting_down", channel="to_char")

    def do_sleep(self, character: Character, context: Context) -> dict:
        pos = CharacterApi.position_value(character)
        if pos == CharacterApi.pos_value("POS_SLEEPING"):
            context.finish()
            return self._command_payload("is_asleep", channel="to_char")
        if pos == CharacterApi.pos_value("POS_FIGHTING"):
            context.finish()
            return self._command_payload("is_fighting", channel="to_char")
        CharacterApi.set_position(character, "POS_SLEEPING")
        context.finish()
        return self._command_payload("default", channel="to_char")

    def do_wake(self, character: Character, context: Context) -> dict:
        arg = MovementApi.argument_text(context)
        if not arg:
            return {"self_stand": True}
        if not CharacterApi.is_awake(character):
            context.finish()
            return self._command_payload("is_asleep", channel="to_char")

        room = self._room(character, context)
        victim = None
        if room is not None:
            for ch in room.characters.values():
                name = (ch.name or "").lower()
                if name == arg or name.startswith(arg):
                    victim = ch
                    break
        if victim is None:
            context.finish()
            return self._command_payload("target_missing", channel="to_char")
        if CharacterApi.is_awake(victim):
            context.finish()
            return self._command_payload("target_awake", channel="to_char", tokens={"t": victim.name})
        if CharacterApi.is_affected_by_name(victim, self.affected_bits, "AFF_SLEEP"):
            context.finish()
            return self._command_payload("affect_sleep", channel="to_char", tokens={"t": victim.name})

        CharacterApi.set_position(victim, "POS_STANDING")
        context.finish()
        return self._command_payload(
            "wake_target",
            victim=victim,
            tokens={"c": character.name, "t": victim.name},
        )

    def do_sneak(self, character: Character, context: Context) -> dict:
        CharacterApi.set_affected_by_name(character, self.affected_bits, "AFF_SNEAK", True)
        context.finish()
        return self._command_payload("attempt_move_silently", channel="to_char")

    def do_hide(self, character: Character, context: Context) -> dict:
        CharacterApi.set_affected_by_name(character, self.affected_bits, "AFF_HIDE", True)
        context.finish()
        return self._command_payload("attempt_hide", channel="to_char")

    def do_visible(self, character: Character, context: Context) -> dict:
        CharacterApi.set_affected_by_name(character, self.affected_bits, "AFF_HIDE", False)
        CharacterApi.set_affected_by_name(character, self.affected_bits, "AFF_INVISIBLE", False)
        CharacterApi.set_affected_by_name(character, self.affected_bits, "AFF_SNEAK", False)
        context.finish()
        return self._command_payload("default", channel="to_char")

    def do_recall(self, character: Character, context: Context):
        room_flags = self.room_flags
        temple_vnum = "3001"
        temple_room = self.room_registry.get_or_none(vnum=temple_vnum)
        if temple_room is None:
            context.finish()
            return self._command_payload("null_temple", channel="to_char")

        current = self._room(character, context)
        if current is None or current.id == temple_room.id:
            context.finish()
            return {}

        no_recall = MovementApi.flag_value(room_flags, "ROOM_NO_RECALL")
        if MovementApi.has_flag(GenericUtil.to_int(current.room_flags, 0), no_recall):
            context.finish()
            return self._command_payload("no_recall", channel="to_char")

        from_targets = current.player_targets(character)
        current.remove_player_from_room(character)
        temple_room.add_player_to_room(character)
        character.room_id = temple_room.id
        character.movement = max(0, GenericUtil.to_int(getattr(character, "movement", 0), 0) // 2)
        to_targets = temple_room.player_targets(character)
        context.finish()
        return {
            "payloads": [
                self._command_payload(
                    "disappears",
                    channel="to_room",
                    targets=from_targets,
                    tokens=self._actor_tokens(character),
                ),
                self._command_payload(
                    "appears_room",
                    channel="to_room",
                    targets=to_targets,
                    tokens=self._actor_tokens(character),
                    to_room_obj=temple_room,
                    aggressive_rounds=self.fight_handler.aggressive_entry_rounds(character, temple_room),
                ),
            ]
        }

    def do_train(self, character: Character, context: Context) -> dict | None:
        if CharacterApi.is_npc(character):
            context.finish()
            return None

        raw = (context.result if isinstance(context.result, str) else "").strip().lower()
        if not raw and context.parameters:
            raw = " ".join(context.parameters).strip().lower()

        room = self.room_registry.get_or_none(id=character.room_id)
        act_bits = self.act_bits or CharacterApi.get_enum("actBits")
        trainer_found = False
        if room is not None:
            train_bit = act_bits.ACT_TRAIN.value if act_bits is not None else 0
            for mob in room.mobiles.values():
                if MobileUtil.is_train_trainer(mob, train_bit):
                    trainer_found = True
                    break
        if not trainer_found:
            context.finish()
            return self._command_payload("no_trainer", channel="to_char")

        attrs = getattr(character, "character_attributes", None)
        trains = GenericUtil.to_int(getattr(attrs, "trains", 0), 0) if attrs is not None else 0
        if raw == "":
            context.finish()
            return {
                "payloads": [
                    self._command_payload("training_sessions", channel="to_char", tokens={"d": trains}),
                    self._train_options_payload(character),
                ]
            }

        if attrs is None:
            context.finish()
            return self._command_payload("invalid_state", channel="to_char")

        if raw == "hp":
            if trains < 1:
                context.finish()
                return self._command_payload("insufficient_sessions", channel="to_char")
            attrs.trains = trains - 1
            character.max_hit = GenericUtil.to_int(getattr(character, "max_hit", 0), 0) + 10
            character.hit = GenericUtil.to_int(getattr(character, "hit", 0), 0) + 10
            context.finish()
            return self._command_payload(
                "durability_increases",
                targets=self._room_targets(room, character),
                tokens=self._actor_tokens(character),
            )

        if raw == "mana":
            if trains < 1:
                context.finish()
                return self._command_payload("insufficient_sessions", channel="to_char")
            attrs.trains = trains - 1
            character.max_mana = GenericUtil.to_int(getattr(character, "max_mana", 0), 0) + 10
            character.mana = GenericUtil.to_int(getattr(character, "mana", 0), 0) + 10
            context.finish()
            return self._command_payload(
                "power_increases",
                targets=self._room_targets(room, character),
                tokens=self._actor_tokens(character),
            )

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
            return self._train_options_payload(character)

        attr_name, output_name, stat_index = stat_spec
        current = GenericUtil.to_int(getattr(attrs, attr_name, 0), 0)
        max_train = CharacterApi.get_max_train(character, stat_index, current)
        if current >= max_train:
            context.finish()
            return self._command_payload("already_at_maximum", channel="to_char", tokens={"t": output_name})
        if trains < 1:
            context.finish()
            return self._command_payload("insufficient_sessions", channel="to_char")

        setattr(attrs, attr_name, current + 1)
        attrs.trains = trains - 1
        context.finish()
        return self._command_payload(
            "increases",
            targets=self._room_targets(room, character),
            tokens={"c": character.name, "t": output_name},
        )

    def _train_options_payload(self, character: Character) -> dict:
        options = PlayerUtil.format_train_options(character).strip()
        if options.startswith("You have nothing left to train, you ") and options.endswith("!"):
            ending = options.removeprefix("You have nothing left to train, you ").removesuffix("!")
            return self._command_payload("nothing_left_train", channel="to_char", tokens={"s": ending})
        trainable = options.removeprefix("You can train: ").removesuffix(".")
        return self._command_payload("train_options", channel="to_char", tokens={"t": trainable})

    def _room(self, character: Character, context: Context):
        room = getattr(context, "room", None)
        if room is not None:
            return room
        return self.room_registry.get_or_none(id=character.room_id)

    @staticmethod
    def _room_targets(room, character: Character) -> list:
        return room.player_targets(character) if room is not None else []

    @staticmethod
    def _actor_tokens(character: Character) -> dict:
        return {"c": str(getattr(character, "name", "") or "")}

    @staticmethod
    def _actor_door_tokens(character: Character, keyword: str) -> dict:
        return {"c": str(getattr(character, "name", "") or ""), "t": str(keyword or "door")}

    @staticmethod
    def _actor_item_tokens(character: Character, short_name: str) -> dict:
        return {"c": str(getattr(character, "name", "") or ""), "t": str(short_name or "it")}

    @staticmethod
    def _command_payload(message_key: str, *, victim=None, targets=None, channel: str = "", tokens: dict | None = None, **extra) -> dict:
        payload = {"message_key": str(message_key or "")}
        if channel:
            payload["channel"] = channel
        if victim is not None:
            payload["victim"] = victim
        if targets is not None:
            payload["targets"] = list(targets)
        if tokens:
            payload["tokens"] = dict(tokens)
        payload.update(extra)
        return payload
