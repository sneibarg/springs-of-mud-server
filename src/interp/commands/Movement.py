from __future__ import annotations
from api.MobileApi import MobileApi

import random

from injector import inject

from game.EnumProvider import EnumProvider
from game.GameData import GameData
from util.GenericUtil import GenericUtil
from util.InterpUtil import InterpUtil
from game.RegistryService import RegistryService
from interp.Context import Context
from api.InterpApi import InterpApi
from api.MovementApi import MovementApi
from combat.CombatHandler import FightHandler
from item.Item import Item
from util.PayloadUtil import PayloadUtil
from util.PlayerUtil import PlayerUtil
from player.Character import Character
from player.CharacterAdvancement import CharacterAdvancement
from skill.GroupOwnership import GroupOwnership
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
        self.group_registry = getattr(registry_service, "group_registry", None)
        self.skill_registry = getattr(registry_service, "skill_registry", None)
        self.spell_registry = getattr(registry_service, "spell_registry", None)
        self.game_data = game_data
        self.fight_handler = fight_handler
        self.interp_api = interp_api
        self.item_types = enum_provider.get("itemTypes")
        self.exit_flags = enum_provider.get("exitFlags")
        self.gate_flags = enum_provider.get("gateFlags")
        self.room_flags = enum_provider.get("roomFlags")
        self.affected_bits = enum_provider.get("affectedBy")
        self.act_bits = enum_provider.get("actBits")
        self.sector_types = enum_provider.get("sectorTypes")

    def move_char(self, character: Character, direction: str, context: Context):
        return self._move_char(character, direction, context, follow=False, leader=None, visited=set())

    def _move_char(self, character: Character, direction: str, context: Context, *, follow: bool, leader, visited: set[str]):
        character_key = str(getattr(character, "id", id(character)))
        if character_key in visited:
            return {"payloads": []}
        visited.add(character_key)

        original_character = context.character
        original_room = getattr(context, "room", None)
        context.character = character
        state = MovementApi.move_state(context, direction=direction, room_registry=self.room_registry)
        context.room = state.in_room
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        context.character = original_character
        context.room = original_room
        if blocked is not None:
            if follow:
                text = str(blocked.get("to_char", "") or "")
                return {"payloads": [], "target_messages": ([{"id": getattr(character, "id", ""), "text": text}] if text else [])}
            return blocked

        if not CharacterApi.is_npc(character):
            character.movement -= state.move_cost

        in_room = state.in_room
        to_room = state.to_room
        followers = self._followers_in_room(character, in_room)
        from_room_targets = in_room.player_targets(character)
        self._remove_from_room(in_room, character)
        self._add_to_room(to_room, character)
        character.room_id = to_room.id
        if getattr(to_room, "area_id", None) is not None:
            character.area_id = to_room.area_id

        to_room_targets = to_room.player_targets(character)
        payloads = []
        target_messages = []
        if follow and leader is not None:
            target_messages.append({
                "id": getattr(character, "id", ""),
                "text": f"You follow {getattr(leader, 'name', '')}.\r\n",
            })
        payloads.extend([
            PayloadUtil.command_payload(
                "default",
                channel="to_room",
                targets=from_room_targets,
                tokens=self._actor_tokens(character),
            ),
            PayloadUtil.command_payload(
                "arrived",
                channel="to_room",
                targets=to_room_targets,
                tokens=self._actor_tokens(character),
                to_room_obj=to_room,
                view_character=character,
                aggressive_rounds=self.fight_handler.aggressive_entry_rounds(character, to_room),
            ),
        ])

        if in_room != to_room:
            for follower in followers:
                if self._should_stand_charmed_follower(follower, character):
                    CharacterApi.set_position(follower, "POS_STANDING")
                if not self._should_follow(follower, character, to_room):
                    continue
                follower_payload = self._move_char(follower, direction, context, follow=True, leader=character, visited=visited)
                payloads.extend(follower_payload.get("payloads", []))
                target_messages.extend(follower_payload.get("target_messages", []))

        if target_messages:
            payloads.append({"target_messages": target_messages})

        context.finish()
        return {
            "payloads": payloads,
            "target_messages": [],
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
        return self._door_action(character, context, MovementApi.open_exit, "open_door")

    def do_close(self, character: Character, context: Context) -> dict:
        return self._container_or_door_action(
            character,
            context,
            MovementApi.close_container,
            "close_container",
            MovementApi.close_exit,
            "close_door",
        )

    def do_lock(self, character: Character, context: Context) -> dict:
        return self._container_or_door_action(
            character,
            context,
            MovementApi.lock_container,
            "container_locked",
            MovementApi.lock_exit,
            "exit_locked",
        )

    def _container_or_door_action(
            self,
            character: Character,
            context: Context,
            container_action,
            container_message_key: str,
            door_action,
            door_message_key: str,
    ) -> dict:
        room = self._room(character, context)
        context.target_item = MovementApi.target_item(context)
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked

        target_item = getattr(context, "target_item", None)
        if target_item is not None:
            container_action(target_item)
            context.finish()
            return PayloadUtil.command_payload(
                container_message_key,
                targets=self._room_targets(room, character),
                tokens=self._actor_item_tokens(character, Item.short(target_item)),
            )

        return self._door_action(character, context, door_action, door_message_key, evaluate_guards=False)

    def do_unlock(self, character: Character, context: Context) -> dict:
        payload = self._door_action(character, context, MovementApi.unlock_exit, "unlocks_exit", channel="to_room")
        if payload.get("message_key") != "unlocks_exit":
            return payload
        return {
            "payloads": [
                PayloadUtil.command_payload("click", channel="to_char"),
                payload,
            ]
        }

    def do_pick(self, character: Character, context: Context) -> dict:
        return self._door_action(character, context, MovementApi.unlock_exit, "door_picked")

    def _door_action(
            self,
            character: Character,
            context: Context,
            action,
            message_key: str,
            *,
            channel: str = "",
            evaluate_guards: bool = True,
    ) -> dict:
        if evaluate_guards:
            blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
            if blocked is not None:
                return blocked

        state = MovementApi.door_state(context, room_registry=self.room_registry, exit_flags=self.exit_flags)
        room = state.room
        ex = state.exit_obj
        action(self.room_registry, room, ex, self.exit_flags)
        context.finish()
        return PayloadUtil.command_payload(
            message_key,
            channel=channel,
            targets=self._room_targets(room, character),
            tokens=self._actor_door_tokens(character, state.keyword),
        )

    def do_stand(self, character: Character, context: Context) -> dict:
        pos = CharacterApi.position_value(character)
        if pos <= CharacterApi.pos_value("POS_STUNNED"):
            context.finish()
            return PayloadUtil.command_payload("can_t_do_that_right_now", channel="to_char")
        if pos == CharacterApi.pos_value("POS_SLEEPING"):
            if CharacterApi.is_affected_by_name(character, self.affected_bits, "AFF_SLEEP"):
                context.finish()
                return PayloadUtil.command_payload("can_t_wake_up", channel="to_char")
            CharacterApi.set_position(character, "POS_STANDING")
            context.finish()
            return PayloadUtil.command_payload("wake_stand_up", channel="to_char")
        if pos in (CharacterApi.pos_value("POS_RESTING"), CharacterApi.pos_value("POS_SITTING")):
            CharacterApi.set_position(character, "POS_STANDING")
            context.finish()
            return PayloadUtil.command_payload("stand_up", channel="to_char")
        if pos == CharacterApi.pos_value("POS_STANDING"):
            context.finish()
            return PayloadUtil.command_payload("already_standing", channel="to_char")
        if pos == CharacterApi.pos_value("POS_FIGHTING"):
            context.finish()
            return PayloadUtil.command_payload("already_fighting", channel="to_char")
        context.finish()
        return {}

    def do_rest(self, character: Character, context: Context) -> dict:
        pos = CharacterApi.position_value(character)
        if pos == CharacterApi.pos_value("POS_FIGHTING"):
            context.finish()
            return PayloadUtil.command_payload("already_fighting", channel="to_char")
        if pos == CharacterApi.pos_value("POS_SLEEPING"):
            if CharacterApi.is_affected_by_name(character, self.affected_bits, "AFF_SLEEP"):
                context.finish()
                return PayloadUtil.command_payload("can_t_wake_up", channel="to_char")
            CharacterApi.set_position(character, "POS_RESTING")
            context.finish()
            return PayloadUtil.command_payload("wake_up_start_resting", channel="to_char")
        if pos in (CharacterApi.pos_value("POS_STANDING"), CharacterApi.pos_value("POS_SITTING")):
            CharacterApi.set_position(character, "POS_RESTING")
            context.finish()
            return PayloadUtil.command_payload("rest", channel="to_char")
        context.finish()
        return PayloadUtil.command_payload("already_resting", channel="to_char")

    def do_sit(self, character: Character, context: Context) -> dict:
        pos = CharacterApi.position_value(character)
        if pos == CharacterApi.pos_value("POS_FIGHTING"):
            context.finish()
            return PayloadUtil.command_payload("maybe_should_finish_fight", channel="to_char")
        if pos == CharacterApi.pos_value("POS_SLEEPING"):
            if CharacterApi.is_affected_by_name(character, self.affected_bits, "AFF_SLEEP"):
                context.finish()
                return PayloadUtil.command_payload("can_t_wake_up", channel="to_char")
            CharacterApi.set_position(character, "POS_SITTING")
            context.finish()
            return PayloadUtil.command_payload("wake_sit_up", channel="to_char")
        if pos == CharacterApi.pos_value("POS_RESTING"):
            CharacterApi.set_position(character, "POS_SITTING")
            context.finish()
            return PayloadUtil.command_payload("stop_resting", channel="to_char")
        if pos == CharacterApi.pos_value("POS_STANDING"):
            CharacterApi.set_position(character, "POS_SITTING")
            context.finish()
            return PayloadUtil.command_payload("sit_down", channel="to_char")
        context.finish()
        return PayloadUtil.command_payload("already_sitting_down", channel="to_char")

    def do_sleep(self, character: Character, context: Context) -> dict:
        pos = CharacterApi.position_value(character)
        if pos == CharacterApi.pos_value("POS_SLEEPING"):
            context.finish()
            return PayloadUtil.command_payload("is_asleep", channel="to_char")
        if pos == CharacterApi.pos_value("POS_FIGHTING"):
            context.finish()
            return PayloadUtil.command_payload("is_fighting", channel="to_char")
        CharacterApi.set_position(character, "POS_SLEEPING")
        context.finish()
        return PayloadUtil.command_payload("default", channel="to_char")

    def do_wake(self, character: Character, context: Context) -> dict:
        arg = MovementApi.argument_text(context)
        if not arg:
            return {"self_stand": True}
        if not CharacterApi.is_awake(character):
            context.finish()
            return PayloadUtil.command_payload("is_asleep", channel="to_char")

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
            return PayloadUtil.command_payload("target_missing", channel="to_char")
        if CharacterApi.is_awake(victim):
            context.finish()
            return PayloadUtil.command_payload("target_awake", channel="to_char", tokens={"t": victim.name})
        if CharacterApi.is_affected_by_name(victim, self.affected_bits, "AFF_SLEEP"):
            context.finish()
            return PayloadUtil.command_payload("affect_sleep", channel="to_char", tokens={"t": victim.name})

        CharacterApi.set_position(victim, "POS_STANDING")
        context.finish()
        return PayloadUtil.command_payload(
            "wake_target",
            victim=victim,
            tokens={"c": character.name, "t": victim.name},
        )

    def do_sneak(self, character: Character, context: Context) -> dict:
        CharacterApi.set_affected_by_name(character, self.affected_bits, "AFF_SNEAK", True)
        context.finish()
        return PayloadUtil.command_payload("attempt_move_silently", channel="to_char")

    def do_hide(self, character: Character, context: Context) -> dict:
        CharacterApi.set_affected_by_name(character, self.affected_bits, "AFF_HIDE", True)
        context.finish()
        return PayloadUtil.command_payload("attempt_hide", channel="to_char")

    def do_visible(self, character: Character, context: Context) -> dict:
        CharacterApi.set_affected_by_name(character, self.affected_bits, "AFF_HIDE", False)
        CharacterApi.set_affected_by_name(character, self.affected_bits, "AFF_INVISIBLE", False)
        CharacterApi.set_affected_by_name(character, self.affected_bits, "AFF_SNEAK", False)
        context.finish()
        return PayloadUtil.command_payload("default", channel="to_char")

    def do_recall(self, character: Character, context: Context):
        room_flags = self.room_flags
        temple_vnum = "3001"
        temple_room = self.room_registry.get_or_none(vnum=temple_vnum)
        if temple_room is None:
            context.finish()
            return PayloadUtil.command_payload("null_temple", channel="to_char")

        current = self._room(character, context)
        if current is None or current.id == temple_room.id:
            context.finish()
            return {}

        no_recall = MovementApi.flag_value(room_flags, "ROOM_NO_RECALL")
        if MovementApi.has_flag(GenericUtil.to_int(current.room_flags, 0), no_recall):
            context.finish()
            return PayloadUtil.command_payload("no_recall", channel="to_char")

        from_targets = current.player_targets(character)
        current.remove_player_from_room(character)
        temple_room.add_player_to_room(character)
        character.room_id = temple_room.id
        character.area_id = temple_room.area_id
        self.fight_handler.stop_fighting(character, both=True)
        character.movement = max(0, GenericUtil.to_int(getattr(character, "movement", 0), 0) // 2)
        to_targets = temple_room.player_targets(character)
        context.finish()
        return {
            "payloads": [
                PayloadUtil.command_payload(
                    "disappears",
                    channel="to_room",
                    targets=from_targets,
                    tokens=self._actor_tokens(character),
                ),
                PayloadUtil.command_payload(
                    "appears_room",
                    channel="to_room",
                    targets=to_targets,
                    tokens=self._actor_tokens(character),
                    to_room_obj=temple_room,
                    aggressive_rounds=self.fight_handler.aggressive_entry_rounds(character, temple_room),
                ),
            ]
        }

    def do_enter(self, character: Character, context: Context) -> dict | None:
        if getattr(character, "fighting", None) is not None:
            context.finish()
            return None

        raw = (context.result if isinstance(context.result, str) else "").strip()
        if not raw and context.parameters:
            raw = " ".join(context.parameters).strip()
        if not raw:
            context.finish()
            return PayloadUtil.command_payload("nope_can_t_do", channel="to_char")

        room = self._room(character, context)
        portal = self._find_room_item(room, raw)
        if portal is None:
            context.finish()
            return PayloadUtil.command_payload("don_t_see", channel="to_char")
        if not self._is_portal(portal) or self._portal_closed(portal, character):
            context.finish()
            return PayloadUtil.command_payload("can_t_seem_find", channel="to_char")
        if self._portal_curse_blocked(portal, character, room):
            context.finish()
            return PayloadUtil.command_payload("something_prevents_from_leaving", channel="to_char")

        destination = self._portal_destination(portal, room)
        if destination is None or destination == room or not self._can_see_room(character, destination) or self._room_private_for(destination, character):
            context.finish()
            return PayloadUtil.command_payload("doesn_t_seem_go", channel="to_char", tokens={"t": Item.short(portal)})
        if self._aggressive_npc_law_blocked(character, destination):
            context.finish()
            return PayloadUtil.command_payload("something_prevents_from_leaving2", channel="to_char")

        from_targets = self._room_targets(room, character)
        self._remove_from_room(room, character)
        self._add_to_room(destination, character)
        character.room_id = destination.id
        if getattr(destination, "area_id", None) is not None:
            character.area_id = destination.area_id

        if self._portal_flag(portal, "GATE_GOWITH"):
            self._remove_item_from_room(room, portal)
            self._add_item_to_room(destination, portal)

        normal_exit = self._portal_flag(portal, "GATE_NORMAL_EXIT")
        to_targets = self._room_targets(destination, character)
        item_short = Item.short(portal)
        payloads = [
            PayloadUtil.command_payload(
                "steps_into",
                channel="to_room",
                targets=from_targets,
                tokens={"c": character.name, "t": item_short},
            ),
            PayloadUtil.command_payload(
                "enter" if normal_exit else "walk_through_find_yourself",
                channel="to_char",
                tokens={"t": item_short},
            ),
            PayloadUtil.command_payload(
                "arrived" if normal_exit else "arrived_through",
                channel="to_room",
                targets=to_targets,
                tokens={"c": character.name, "t": item_short},
                to_room_obj=destination,
                view_character=character,
                aggressive_rounds=self.fight_handler.aggressive_entry_rounds(character, destination),
            ),
        ]

        if self._decrement_portal_charge(portal):
            self._remove_item_from_room(destination if self._portal_flag(portal, "GATE_GOWITH") else room, portal)
            payloads.append(PayloadUtil.command_payload("fades_out_existence", channel="to_char", tokens={"t": item_short}))

        context.finish()
        return {"payloads": payloads}

    def do_go(self, character: Character, context: Context) -> dict | None:
        return self.do_enter(character, context)

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
                if MobileApi.is_train_trainer(mob, train_bit):
                    trainer_found = True
                    break
        if not trainer_found:
            context.finish()
            return PayloadUtil.command_payload("no_trainer", channel="to_char")

        attrs = getattr(character, "character_attributes", None)
        trains = GenericUtil.to_int(getattr(attrs, "trains", 0), 0) if attrs is not None else 0
        if raw == "":
            context.finish()
            return {
                "payloads": [
                    PayloadUtil.command_payload("training_sessions", channel="to_char", tokens={"d": trains}),
                    self._train_options_payload(character),
                ]
            }

        if attrs is None:
            context.finish()
            return PayloadUtil.command_payload("invalid_state", channel="to_char")

        if raw == "hp":
            if trains < 1:
                context.finish()
                return PayloadUtil.command_payload("insufficient_sessions", channel="to_char")
            attrs.trains = trains - 1
            character.max_hit = GenericUtil.to_int(getattr(character, "max_hit", 0), 0) + 10
            character.hit = GenericUtil.to_int(getattr(character, "hit", 0), 0) + 10
            context.finish()
            return PayloadUtil.command_payload(
                "durability_increases",
                targets=self._room_targets(room, character),
                tokens=self._actor_tokens(character),
            )

        if raw == "mana":
            if trains < 1:
                context.finish()
                return PayloadUtil.command_payload("insufficient_sessions", channel="to_char")
            attrs.trains = trains - 1
            character.max_mana = GenericUtil.to_int(getattr(character, "max_mana", 0), 0) + 10
            character.mana = GenericUtil.to_int(getattr(character, "mana", 0), 0) + 10
            context.finish()
            return PayloadUtil.command_payload(
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
            return PayloadUtil.command_payload("already_at_maximum", channel="to_char", tokens={"t": output_name})
        if trains < 1:
            context.finish()
            return PayloadUtil.command_payload("insufficient_sessions", channel="to_char")

        setattr(attrs, attr_name, current + 1)
        attrs.trains = trains - 1
        context.finish()
        return PayloadUtil.command_payload(
            "increases",
            targets=self._room_targets(room, character),
            tokens={"c": character.name, "t": output_name},
        )

    def do_gain(self, character: Character, context: Context) -> dict | None:
        if CharacterApi.is_npc(character):
            context.finish()
            return None

        raw = (context.result if isinstance(context.result, str) else "").strip().lower()
        if not raw and context.parameters:
            raw = " ".join(context.parameters).strip().lower()

        room = self._room(character, context)
        trainer = self._gain_trainer(room, character)
        if trainer is None:
            context.finish()
            return PayloadUtil.command_payload("can_t_do", channel="to_char")
        if not raw:
            context.finish()
            return PayloadUtil.command_payload("tells_i_do_not", channel="to_char", tokens={"t": self._entity_label(trainer)})

        attrs = getattr(character, "character_attributes", None)
        subcommand, _ = InterpUtil.one_argument(raw)
        if subcommand and "list".startswith(subcommand):
            context.finish()
            return {"to_char": self._gain_list(character)}

        if subcommand and "convert".startswith(subcommand):
            practices = GenericUtil.to_int(getattr(attrs, "practices", 0), 0) if attrs is not None else 0
            if practices < 10:
                context.finish()
                return PayloadUtil.command_payload("tells_not_yet_ready", channel="to_char", tokens={"t": self._entity_label(trainer)})
            attrs.practices = practices - 10
            attrs.trains = GenericUtil.to_int(getattr(attrs, "trains", 0), 0) + 1
            context.finish()
            return PayloadUtil.command_payload("helps_apply_practice_training", channel="to_char", tokens={"t": self._entity_label(trainer)})

        if subcommand and "points".startswith(subcommand):
            trains = GenericUtil.to_int(getattr(attrs, "trains", 0), 0) if attrs is not None else 0
            points = GenericUtil.to_int(getattr(attrs, "points", 0), 0) if attrs is not None else 0
            if trains < 2:
                context.finish()
                return PayloadUtil.command_payload("tells_not_yet_ready2", channel="to_char", tokens={"t": self._entity_label(trainer)})
            if points <= 40:
                context.finish()
                return PayloadUtil.command_payload("tells_would_no_point", channel="to_char", tokens={"t": self._entity_label(trainer)})
            attrs.trains = trains - 2
            attrs.points = points - 1
            CharacterAdvancement.reset_experience_for_points(character)
            context.finish()
            return PayloadUtil.command_payload("trains_feel_more_at", channel="to_char", tokens={"t": self._entity_label(trainer)})

        group = self._find_gain_group(raw)
        if group is not None:
            cost = self._group_rating(character, group)
            if self._knows_group(character, group):
                context.finish()
                return PayloadUtil.command_payload("tells_already_know_group", channel="to_char", tokens={"t": self._entity_label(trainer)})
            if cost <= 0:
                context.finish()
                return PayloadUtil.command_payload("tells_group_beyond_powers", channel="to_char", tokens={"t": self._entity_label(trainer)})
            trains = GenericUtil.to_int(getattr(attrs, "trains", 0), 0) if attrs is not None else 0
            if trains < cost:
                context.finish()
                return PayloadUtil.command_payload("tells_not_yet_ready3", channel="to_char", tokens={"t": self._entity_label(trainer)})
            self._add_group(character, group)
            attrs.trains = trains - cost
            context.finish()
            return PayloadUtil.command_payload("trains_art", channel="to_char", tokens={"t": self._entity_label(trainer), "s": getattr(group, "name", raw)})

        skill = self._find_gain_skill(raw)
        if skill is not None:
            skill_name = str(getattr(skill, "name", raw) or raw)
            if str(getattr(skill, "kind", "skill") or "skill").strip().lower() != "skill":
                context.finish()
                return PayloadUtil.command_payload("tells_must_learn_full", channel="to_char", tokens={"t": self._entity_label(trainer)})
            if self._has_learned(character, skill_name, "skills"):
                context.finish()
                return PayloadUtil.command_payload("tells_already_know_skill", channel="to_char", tokens={"t": self._entity_label(trainer)})
            cost = self._ability_rating(character, skill)
            if cost <= 0:
                context.finish()
                return PayloadUtil.command_payload("tells_skill_beyond_powers", channel="to_char", tokens={"t": self._entity_label(trainer)})
            trains = GenericUtil.to_int(getattr(attrs, "trains", 0), 0) if attrs is not None else 0
            if trains < cost:
                context.finish()
                return PayloadUtil.command_payload("tells_not_yet_ready4", channel="to_char", tokens={"t": self._entity_label(trainer)})
            self._set_learned(character, skill_name, 1, "skills")
            attrs.trains = trains - cost
            context.finish()
            return PayloadUtil.command_payload("trains_art2", channel="to_char", tokens={"t": self._entity_label(trainer), "s": skill_name})

        if self._find_gain_spell(raw) is not None:
            context.finish()
            return PayloadUtil.command_payload("tells_must_learn_full", channel="to_char", tokens={"t": self._entity_label(trainer)})

        context.finish()
        return PayloadUtil.command_payload("tells_i_do_not", channel="to_char", tokens={"t": self._entity_label(trainer)})

    def _train_options_payload(self, character: Character) -> dict:
        options = PlayerUtil.format_train_options(character).strip()
        if options.startswith("You have nothing left to train, you ") and options.endswith("!"):
            ending = options.removeprefix("You have nothing left to train, you ").removesuffix("!")
            return PayloadUtil.command_payload("nothing_left_train", channel="to_char", tokens={"s": ending})
        trainable = options.removeprefix("You can train: ").removesuffix(".")
        return PayloadUtil.command_payload("train_options", channel="to_char", tokens={"t": trainable})

    def _gain_list(self, character: Character) -> str:
        lines = [self._format_gain_row_header("group"), "\r\n"]
        groups = sorted(self._all_groups(), key=lambda group: str(getattr(group, "name", "") or "").lower())
        entries = [
            (str(getattr(group, "name", "") or ""), self._group_rating(character, group))
            for group in groups
            if not self._knows_group(character, group) and self._group_rating(character, group) > 0
        ]
        lines.append(self._format_gain_rows(entries))
        lines.append("\r\n")
        lines.append(self._format_gain_row_header("skill"))
        lines.append("\r\n")
        skills = sorted(self._all_skills(), key=lambda skill: str(getattr(skill, "name", "") or "").lower())
        skill_entries = [
            (str(getattr(skill, "name", "") or ""), self._ability_rating(character, skill))
            for skill in skills
            if str(getattr(skill, "name", "") or "").strip().lower() != "reserved"
            and str(getattr(skill, "kind", "skill") or "skill").strip().lower() == "skill"
            and not self._has_learned(character, str(getattr(skill, "name", "") or ""), "skills")
            and self._ability_rating(character, skill) > 0
        ]
        lines.append(self._format_gain_rows(skill_entries))
        return "".join(lines)

    @staticmethod
    def _format_gain_row_header(kind: str) -> str:
        return f"{kind:<18} {'cost':<5} {kind:<18} {'cost':<5} {kind:<18} {'cost':<5}"

    @staticmethod
    def _format_gain_rows(entries: list[tuple[str, int]]) -> str:
        if not entries:
            return ""
        lines = []
        for index, (name, cost) in enumerate(entries, start=1):
            lines.append(f"{name:<18} {cost:<5d} ")
            if index % 3 == 0:
                lines.append("\r\n")
        if len(entries) % 3 != 0:
            lines.append("\r\n")
        return "".join(lines)

    def _gain_trainer(self, room, character):
        if room is None:
            return None
        act_bits = self.act_bits or CharacterApi.get_enum("actBits")
        gain_bit = EnumProvider.value(act_bits, "ACT_GAIN")
        for mob in list((getattr(room, "mobiles", {}) or {}).values()):
            if gain_bit and CharacterApi.is_set(self._mobile_act(mob), gain_bit) and self._can_see_character(character, mob, room):
                return mob
        return None

    def _find_gain_group(self, raw: str):
        return self._find_gain_entry(raw, self._all_groups(), self.group_registry)

    def _find_gain_skill(self, raw: str):
        return self._find_gain_entry(raw, self._all_skills(), self.skill_registry)

    def _find_gain_spell(self, raw: str):
        return self._find_gain_entry(raw, self._all_spells(), self.spell_registry)

    @staticmethod
    def _find_gain_entry(raw: str, candidates: list, registry):
        wanted = str(raw or "").strip().lower()
        if not wanted:
            return None
        # Registry order supplies the stable first match, as ROM's tables do.
        for entry in candidates:
            name = str(getattr(entry, "name", "") or "").strip().lower()
            if name.startswith(wanted):
                return entry
        getter = getattr(registry, "get_or_none", None)
        return getter(name=raw) if callable(getter) else None

    def _all_groups(self) -> list:
        getter = getattr(self.group_registry, "all_groups", None)
        return list(getter()) if callable(getter) else []

    def _all_skills(self) -> list:
        getter = getattr(self.skill_registry, "all_skills", None)
        return list(getter()) if callable(getter) else []

    def _all_spells(self) -> list:
        getter = getattr(self.spell_registry, "all_spells", None)
        return list(getter()) if callable(getter) else []

    def _group_rating(self, character: Character, group) -> int:
        ratings = list(getattr(group, "rating", []) or [])
        index = self._class_index(character)
        return GenericUtil.to_int(ratings[index], 0) if 0 <= index < len(ratings) else 0

    def _ability_rating(self, character: Character, ability) -> int:
        rating_map = getattr(ability, "rating_by_class", None)
        if rating_map is None:
            rating_map = getattr(ability, "ratingByClass", None)
        class_name = self._class_name(character)
        return CharacterApi.skill_value_for_class(rating_map or {}, class_name, 0)

    @staticmethod
    def _class_name(character: Character) -> str:
        return str(getattr(getattr(character, "character_class", None), "name", "") or "").strip().lower()

    def _class_index(self, character: Character) -> int:
        return {"mage": 0, "cleric": 1, "thief": 2, "warrior": 3}.get(self._class_name(character), -1)

    def _knows_group(self, character: Character, group) -> bool:
        return GroupOwnership.knows(character, group.name)

    def _add_group(self, character: Character, group, visited: set[str] | None = None) -> None:
        visited = set() if visited is None else visited
        key = str(group.name).strip().casefold()
        if key in visited:
            return
        visited.add(key)
        GroupOwnership.add(character, group.name)
        for name in list(group.skills or []) + list(group.spells or []):
            # Resolve abilities before groups, matching ROM group_add. Nested
            # groups may appear in either designer-authored member list.
            skill = self._find_gain_skill(name)
            spell = None if skill is not None else self._find_gain_spell(name)
            ability = skill if skill is not None else spell
            if ability is not None:
                collection = "skills" if skill is not None else "spells"
                if not self._has_learned(character, ability.name, collection):
                    self._set_learned(character, ability.name, 1, collection)
            else:
                nested = self._find_gain_group(name)
                if nested is not None:
                    self._add_group(character, nested, visited)

    @staticmethod
    def _has_learned(character: Character, name: str, collection_name: str) -> bool:
        wanted = str(name or "").strip().lower()
        for entry in list(getattr(character, collection_name, []) or []):
            entry_name = str(entry.get("name", "") if isinstance(entry, dict) else getattr(entry, "name", "")).strip().lower()
            entry_level = GenericUtil.to_int(entry.get("level", 0) if isinstance(entry, dict) else getattr(entry, "level", 0), 0)
            if entry_name == wanted and entry_level > 0:
                return True
        return False

    @staticmethod
    def _set_learned(character: Character, name: str, level: int, collection_name: str) -> None:
        collection = getattr(character, collection_name, None)
        if collection is None:
            collection = []
            setattr(character, collection_name, collection)
        wanted = str(name or "").strip().lower()
        for entry in collection:
            entry_name = str(entry.get("name", "") if isinstance(entry, dict) else getattr(entry, "name", "")).strip().lower()
            if entry_name == wanted:
                if isinstance(entry, dict):
                    entry["level"] = level
                else:
                    setattr(entry, "level", level)
                return
        collection.append({"name": str(name or "").strip(), "level": level})

    @staticmethod
    def _mobile_act(mob) -> int:
        raw = getattr(getattr(mob, "status_flags", None), "act", 0)
        return GenericUtil.to_int(raw, 0)

    @staticmethod
    def _can_see_character(character, target, room) -> bool:
        can_see = getattr(CharacterApi, "can_see", None)
        if callable(can_see):
            return bool(can_see(character, target, room))
        return True

    @staticmethod
    def _entity_label(entity) -> str:
        return str(getattr(entity, "short_description", "") or getattr(entity, "name", "") or "Someone")

    def _is_portal(self, item) -> bool:
        item_type = getattr(item, "item_type", "")
        portal_type = EnumProvider.value(self.item_types, "ITEM_PORTAL")
        if portal_type and GenericUtil.to_int(item_type, None) == portal_type:
            return True
        return "portal" in str(item_type or "").strip().lower()

    def _portal_closed(self, portal, character) -> bool:
        if CharacterApi.is_immortal(character):
            return False
        closed_bit = EnumProvider.value(self.exit_flags, "EX_CLOSED")
        return bool(closed_bit and (GenericUtil.to_int(getattr(portal, "value1", 0), 0) & closed_bit))

    def _portal_curse_blocked(self, portal, character, room) -> bool:
        if CharacterApi.is_immortal(character) or self._portal_flag(portal, "GATE_NOCURSE"):
            return False
        no_recall = EnumProvider.value(self.room_flags, "ROOM_NO_RECALL")
        return CharacterApi.is_affected_by_name(character, self.affected_bits, "AFF_CURSE") or bool(room is not None and no_recall and (GenericUtil.to_int(getattr(room, "room_flags", 0), 0) & no_recall))

    def _portal_destination(self, portal, current_room):
        destination_ref = str(getattr(portal, "value3", "") or "").strip()
        if self._portal_flag(portal, "GATE_RANDOM") or destination_ref == "-1":
            destination = self._random_room(current_room)
            if destination is not None:
                setattr(portal, "value3", str(getattr(destination, "vnum", "") or getattr(destination, "id", "")))
            return destination
        if self._portal_flag(portal, "GATE_BUGGY") and random.randint(1, 100) <= 5:
            return self._random_room(current_room)
        if not destination_ref:
            return None
        return self.room_registry.get_or_none(vnum=destination_ref) or self.room_registry.get_or_none(id=destination_ref)

    def _random_room(self, current_room):
        all_rooms = getattr(self.room_registry, "all_rooms", None)
        rooms = list(all_rooms()) if callable(all_rooms) else []
        rooms = [room for room in rooms if room is not current_room]
        return random.choice(rooms) if rooms else None

    def _portal_flag(self, portal, flag_name: str) -> bool:
        bit = EnumProvider.value(self.gate_flags, flag_name)
        return bool(bit and (GenericUtil.to_int(getattr(portal, "value2", 0), 0) & bit))

    def _room_private_for(self, room, character) -> bool:
        if room is None or CharacterApi.is_immortal(character):
            return False
        private = getattr(room, "is_private", None)
        return bool(private(self.room_flags)) if callable(private) else False

    def _aggressive_npc_law_blocked(self, character, destination) -> bool:
        if not CharacterApi.is_npc(character):
            return False
        aggressive = EnumProvider.value(self.act_bits, "ACT_AGGRESSIVE")
        law = EnumProvider.value(self.room_flags, "ROOM_LAW")
        return bool(aggressive and law and (self._mobile_act(character) & aggressive) and (GenericUtil.to_int(getattr(destination, "room_flags", 0), 0) & law))

    @staticmethod
    def _find_room_item(room, wanted: str):
        if room is None:
            return None
        finder = getattr(room, "find_room_item", None)
        if callable(finder):
            return finder(wanted)
        query = str(wanted or "").strip().lower()
        for item in list((getattr(room, "contents", {}) or {}).values()):
            name = str(getattr(item, "name", "") or "").lower()
            if name == query or name.startswith(query):
                return item
        return None

    @staticmethod
    def _remove_item_from_room(room, item) -> None:
        remover = getattr(room, "remove_item_from_room", None)
        if callable(remover):
            remover(item)
        elif room is not None:
            getattr(room, "contents", {}).pop(getattr(item, "id", ""), None)

    @staticmethod
    def _add_item_to_room(room, item) -> None:
        adder = getattr(room, "add_item_to_room", None)
        if callable(adder):
            adder(item)
        elif room is not None:
            getattr(room, "contents", {})[getattr(item, "id", "")] = item

    @staticmethod
    def _decrement_portal_charge(portal) -> bool:
        charges = GenericUtil.to_int(getattr(portal, "value0", 0), 0)
        if charges <= 0:
            return charges == -1
        charges -= 1
        setattr(portal, "value0", str(-1 if charges == 0 else charges))
        return charges == 0

    def _room(self, character: Character, context: Context):
        room = getattr(context, "room", None)
        if room is not None:
            return room
        return self.room_registry.get_or_none(id=character.room_id)

    @staticmethod
    def _room_targets(room, character: Character) -> list:
        return room.player_targets(character) if room is not None else []

    @staticmethod
    def _followers_in_room(character, room) -> list:
        if room is None:
            return []
        people = getattr(room, "people", None)
        if callable(people):
            candidates = list(people())
        else:
            candidates = list((getattr(room, "characters", {}) or {}).values()) + list((getattr(room, "mobiles", {}) or {}).values())
        return [candidate for candidate in candidates if candidate is not character and getattr(candidate, "master", None) == character]

    def _should_stand_charmed_follower(self, follower, master) -> bool:
        return (
            getattr(follower, "master", None) == master
            and CharacterApi.is_affected_by_name(follower, self.affected_bits, "AFF_CHARM")
            and CharacterApi.position_value(follower) < CharacterApi.pos_value("POS_STANDING")
        )

    def _should_follow(self, follower, master, to_room) -> bool:
        if getattr(follower, "master", None) != master:
            return False
        if CharacterApi.position_value(follower) != CharacterApi.pos_value("POS_STANDING"):
            return False
        return self._can_see_room(follower, to_room)

    @staticmethod
    def _can_see_room(_character, room) -> bool:
        return room is not None

    @staticmethod
    def _remove_from_room(room, character) -> None:
        if CharacterApi.is_npc(character):
            remover = getattr(room, "remove_mobile_from_room", None)
        else:
            remover = getattr(room, "remove_player_from_room", None)
        if callable(remover):
            remover(character)

    @staticmethod
    def _add_to_room(room, character) -> None:
        if CharacterApi.is_npc(character):
            adder = getattr(room, "add_mobile_to_room", None)
        else:
            adder = getattr(room, "add_player_to_room", None)
        if callable(adder):
            adder(character)

    @staticmethod
    def _actor_tokens(character: Character) -> dict:
        return {"c": str(getattr(character, "name", "") or "")}

    @staticmethod
    def _actor_door_tokens(character: Character, keyword: str) -> dict:
        return {"c": str(getattr(character, "name", "") or ""), "t": str(keyword or "door")}

    @staticmethod
    def _actor_item_tokens(character: Character, short_name: str) -> dict:
        return {"c": str(getattr(character, "name", "") or ""), "t": str(short_name or "it")}
