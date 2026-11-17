from __future__ import annotations

import random

from types import SimpleNamespace
from typing import Any, Optional

from api.GameApi import GameApi
from api.ItemApi import ItemApi
from game.AnimateEntity import AnimateEntity
from item.Item import Item
from mobile.Mobile import Mobile
from util.DisplayUtil import DisplayUtil, RecipientText
from util.GenericUtil import GenericUtil
from util.FightUtil import FightUtil
from mobile.MobileContext import MobileContext
from api.CharacterApi import CharacterApi
from server.LoggerFactory import LoggerFactory
from skill.SpellContext import SpellContext


class MobileApi(GameApi):
    _logger = None

    @classmethod
    def lazy_load(cls, weather_handler, registry_service) -> None:
        cls.load_actor_runtime(weather_handler, registry_service)

    @classmethod
    def _reset_internal_variables(cls) -> None:
        cls._registry_service = None
        cls._weather_handler = None
        cls._logger = None

    @classmethod
    def _logger_obj(cls):
        if cls._logger is None:
            cls._logger = LoggerFactory.get_logger("MobileApi")
        return cls._logger

    @staticmethod
    def _actor_label(entity) -> str:
        actor = getattr(entity, "actor", entity)
        if actor is None:
            return "unknown-mobile"
        short_desc = str(getattr(actor, "short_description", "") or "").strip()
        vnum = str(getattr(actor, "vnum", "") or "").strip()
        if short_desc:
            return f"{short_desc} [vnum={vnum}, id={actor.id}]"
        name = str(actor.name or "unknown-mobile").strip()
        return f"{name} [vnum={vnum}, id={actor.id}]"

    @staticmethod
    def _room_label(room) -> str:
        if room is None:
            return "no-room"
        name = str(room.name).strip()
        vnum = str(room.vnum).strip()
        room_id = str(room.id).strip()
        return f"{name or 'unnamed-room'} [vnum={vnum}, id={room_id}]"

    @classmethod
    def require_awake(cls, ctx: MobileContext):
        if not CharacterApi.is_awake(ctx.actor):
            ctx.finish()
            return False
        return True

    @staticmethod
    def require_not_fighting(ctx: MobileContext):
        if ctx.actor.fighting is not None:
            ctx.finish()
            return False
        return True

    @staticmethod
    def require_in_room(ctx: MobileContext):
        ctx.room = MobileApi.resolve_room(ctx.handler.room_registry, ctx.actor)
        if ctx.room is None:
            ctx.finish()
            return False
        return True

    @staticmethod
    def require_position(ctx: MobileContext, pos_name: str):
        wanted = str(pos_name or "").strip().upper()
        if wanted and not wanted.startswith("POS_"):
            wanted = f"POS_{wanted}"
        if CharacterApi.position_value(ctx.actor) != CharacterApi.pos_value(wanted):
            ctx.finish()
            return False
        return True

    @staticmethod
    def require_not_affected(ctx: MobileContext, affect_name: str):
        affected = CharacterApi.get_enum("affectedBy")
        bit = MobileApi.enum_bit(affected, str(affect_name or "").strip().upper())
        if bit and CharacterApi.is_affected(ctx.actor, bit):
            ctx.finish()
            return False
        return True

    @staticmethod
    def dispatch_weighted_special(ctx: MobileContext, weighted: list[tuple[str, int]]):
        chosen = MobileApi.choose_weighted(weighted)
        if not chosen:
            return False
        return ctx.handler.execute_special_by_name(ctx.actor, chosen, ctx.room, ctx)

    @staticmethod
    def dispatch_special_by_bits(ctx: MobileContext, bits: int, choices: list[str]):
        index = ctx.handler.rng.number_bits(bits)
        if index >= len(choices) or not choices[index]:
            return False
        return ctx.handler.execute_special_by_name(ctx.actor, choices[index], ctx.room, ctx)

    @staticmethod
    def when_fighting_delegate(ctx: MobileContext, special_name: str):
        if ctx.actor.fighting is None:
            return False
        return ctx.handler.execute_special_by_name(ctx.actor, special_name, ctx.room, ctx)

    @staticmethod
    def select_visible_room_player(ctx: MobileContext, alias: str, exclude_self: bool = True, max_level: Optional[int] = None, chance_bits: int = 0):
        target = None
        for candidate in ctx.room.people_newest_first():
            if exclude_self and candidate is ctx.actor:
                continue
            if not CharacterApi.can_see(ctx.actor, candidate, ctx.room):
                continue
            if chance_bits > 0 and ctx.handler.rng.number_bits(GenericUtil.to_int(chance_bits, 0)) != 0:
                continue
            if CharacterApi.is_npc(candidate):
                continue
            if max_level is not None and GenericUtil.to_int(candidate.level, 0) > GenericUtil.to_int(max_level, 0):
                continue
            target = candidate
            break
        ctx.set_alias(alias, target)
        return target

    @staticmethod
    def select_room_combat_victim(ctx: MobileContext, alias: str, chance_bits: int = 0):
        target = None
        for entity in ctx.room.people_newest_first():
            if entity.fighting is ctx.actor:
                if chance_bits > 0 and ctx.handler.rng.number_bits(GenericUtil.to_int(chance_bits, 0)) != 0:
                    continue
                target = entity
                break
        ctx.set_alias(alias, target)
        return target

    @classmethod
    def cast_dragon_breath(cls, ctx: MobileContext, spell_name: str):
        cls.select_room_combat_victim(ctx, "victim", chance_bits=3)
        return cls.cast_spell(ctx, spell_name, target="victim")

    @classmethod
    def cast_spell(cls, ctx: MobileContext, spell_name: str, target: Any = "victim", *,
                   direct: bool = False, claim_pulse: bool = True):
        """Resolve a mobile spell and return whether it claims the pulse."""
        target_value = target if target == "room" else ctx.resolve(target)
        area = target_value == "room"
        if target_value is None or (not area and isinstance(target_value, str)):
            return False

        spell_key = str(spell_name or "").strip().lower()
        spell = FightUtil.find_spell(ctx.handler.spell_registry, spell_key)
        skill = FightUtil.find_spell_skill(ctx.handler.skill_registry, ctx.actor, spell_key)
        meta = spell if spell is not None else skill
        if meta is None:
            return False

        victim = None if area else target_value
        object_target = hasattr(victim, "item_type")
        spell_context = SpellContext(
            actor=ctx.actor,
            spell=meta,
            handler=ctx.handler,
            room=ctx.room,
            target=victim,
            target_name="room" if area else str(victim.name or ""),
            target_kind="room" if area else "obj" if object_target else "char",
            source="mobile",
        )
        ctx.handler.spell_api.execute_lambdas(spell_context)
        if spell_context.script_failed:
            return False
        # A save can end the spell without an effect and still produce notices.
        if not direct and spell_context.performed and not spell_context.announced:
            cls._queue_spell_payload(ctx, meta, None if object_target else victim, area=area)
        for payload in spell_context.payloads:
            ctx.queue_payload(payload)
        return claim_pulse and ctx.mark_performed()

    @classmethod
    def cast_support_spell_by_bits(cls, ctx: MobileContext, target_alias: str, bits: int, choices: list[tuple[str, str, bool]]):
        target = ctx.resolve(target_alias)
        if target is None:
            return False
        index = ctx.handler.rng.number_bits(bits)
        if index >= len(choices):
            return False
        spell, message, claim_pulse = choices[index]
        cls._queue_room_message(ctx, message, prompt_listeners=True)
        return cls.cast_spell(ctx, spell, target=target, direct=True, claim_pulse=claim_pulse)

    @classmethod
    def cast_weighted_support_spell(cls, ctx: MobileContext, target_alias: str, weighted_spells: list[tuple[str, int, str]], miss_weight: int = 0):
        victim = ctx.resolve(target_alias)
        if victim is None:
            return False
        choices = []
        for spell_name, min_level, message in weighted_spells:
            if GenericUtil.to_int(ctx.actor.level, 0) >= GenericUtil.to_int(min_level, 0):
                choices.append(((spell_name, message), 1))
        if miss_weight > 0:
            choices.append((None, GenericUtil.to_int(miss_weight, 0)))
        picked = MobileApi.choose_weighted(choices)
        if not picked:
            return False
        spell_name, message = picked
        if message:
            cls._queue_room_message(ctx, message, target=victim)
        return cls.cast_spell(ctx, spell_name, target=victim)

    @classmethod
    def cast_weighted_combat_spell(cls, ctx: MobileContext, target_alias: str, weighted_spells: list[tuple[str, int, int]]):
        victim = ctx.resolve(target_alias)
        if victim is None:
            return False
        choices = []
        for spell_name, min_level, weight in weighted_spells:
            if GenericUtil.to_int(ctx.actor.level, 0) >= GenericUtil.to_int(min_level, 0):
                choices.append((spell_name, weight))
        chosen = MobileApi.choose_weighted(choices)
        if not chosen:
            return False
        return cls.cast_spell(ctx, chosen, target=victim)

    @staticmethod
    def select_room_criminal(ctx: MobileContext, alias: str, crime_alias: str, priorities: list[str], visible_only: bool = True):
        player_bits = CharacterApi.get_enum("playerActBits")
        victim = None
        crime = ""
        for player in reversed(ctx.room.players_in_room()):
            if visible_only and not CharacterApi.can_see(ctx.actor, player, ctx.room):
                continue
            act_flags = player.status_flags.act
            for flag_name in priorities:
                bit = MobileApi.enum_bit(player_bits, flag_name)
                if bit and CharacterApi.is_set(act_flags, bit):
                    victim = player
                    crime = flag_name.replace("PLR_", "")
                    break
            if victim is not None:
                break
        ctx.set_alias(alias, victim)
        ctx.set_alias(crime_alias, crime)
        return victim

    @staticmethod
    def yell(ctx: MobileContext, text: str, allow_noshout_override: bool = False):
        victim = ctx.get_alias("victim")
        crime = ctx.get_alias("crime", "")
        if victim is None and "{victim" in str(text):
            return False
        formatted = str(text or "").format(victim=victim, crime=crime)
        if allow_noshout_override:
            return ctx.handler.run_special_yell(ctx, formatted) and ctx.mark_performed()
        ctx.queue_payload({"area_message": f"{formatted}\r\n", "area_id": ctx.actor.area_id})
        return ctx.mark_performed()

    @staticmethod
    def multi_hit(ctx: MobileContext, victim_alias: str, *, check_safe: bool = True):
        victim = ctx.resolve(victim_alias)
        if victim is None or ctx.room is None:
            return False
        fight = ctx.handler.fight_handler
        if check_safe and ctx.is_safe(victim):
            return False
        result = fight.multi_hit(ctx.actor, victim, dt="TYPE_UNDEFINED")
        round_payload = fight.build_round_payload(ctx.actor, victim, ctx.room, result)
        ctx.queue_payload({"actor": ctx.actor, "combat_round": round_payload})
        return ctx.mark_performed()

    @staticmethod
    def when_selected(ctx: MobileContext, alias: str, *expressions: str):
        if ctx.resolve(alias) is None:
            return False
        for expression in expressions:
            ctx.exec_expr(expression)
        return True

    @staticmethod
    def select_most_evil_fighter(ctx: MobileContext, alias: str, minimum_alignment: int = 300, exclude_target: str = ""):
        threshold = GenericUtil.to_int(minimum_alignment, 300)
        if threshold < 0:
            threshold = abs(threshold)
        best = None
        max_evil = threshold
        for entity in ctx.room.people_newest_first():
            if exclude_target == "self" and entity is ctx.actor:
                continue
            if entity.fighting is None or entity.fighting is ctx.actor:
                continue
            alignment = GenericUtil.to_int(entity.character_attributes.alignment, 0)
            if alignment < max_evil:
                max_evil = alignment
                best = entity
        ctx.set_alias(alias, best)
        return best

    @classmethod
    def when_selected_attack(cls, ctx: MobileContext, alias: str, room_message: str = "", *, check_safe: bool = True):
        victim = ctx.resolve(alias)
        if victim is None:
            return False
        if room_message:
            cls._queue_room_message(ctx, room_message, target=victim)
        return cls.multi_hit(ctx, alias, check_safe=check_safe)

    @staticmethod
    def select_room_npc_by_group(ctx: MobileContext, alias: str, group_vnum: str, exclude_vnum: str = "", where: str = "", randomize: bool = False):
        excluded = str(exclude_vnum or "").strip().upper()
        if excluded == "MOB_VNUM_PATROLMAN":
            excluded = "2106"

        wanted_group = MobileApi.group_vnum(group_vnum)
        selected = None
        count = 0
        for mob in reversed(ctx.room.mobiles_in_room()):
            if mob is ctx.actor:
                continue
            if str(mob.vnum) == excluded:
                return ctx.set_alias(alias, None)
            if str(mob.group or "") != wanted_group:
                continue
            if where and not ctx.eval_bool(where, candidate=mob):
                continue
            if randomize:
                if ctx.handler.rng.number_range(0, count) == 0:
                    selected = mob
                count += 1
            else:
                selected = mob
                break
        ctx.set_alias(alias, selected)
        return selected

    @classmethod
    def say_random(cls, ctx: MobileContext, messages: list[str], target: Any = None, allow_none: bool = False):
        if not messages:
            return False
        target_value = ctx.resolve(target)
        if allow_none and ctx.handler.rng.number_range(0, len(messages)) == 0:
            return False
        selected = messages[ctx.handler.rng.number_range(0, len(messages) - 1)] if len(messages) > 1 else messages[0]
        cls._queue_room_message(ctx, selected, target=target_value)
        return ctx.mark_performed()

    @staticmethod
    def select_room_item(ctx: MobileContext, alias: str, where: str = ""):
        chosen = None
        owners = None
        for obj in ctx.room.items_newest_first():
            if obj.owner and owners is None:
                owners = list(MobileApi._live_loot_owners(ctx))
            proxy = SimpleNamespace(
                obj=obj,
                can_take=ItemApi.item_takeable(obj, ctx.handler.wear_flags),
                can_loot=ItemApi.can_loot(ctx.actor, obj, owners or ()),
                item_type=Item.enum_type_name(obj),
                cost=GenericUtil.to_int(obj.cost, 0),
            )
            if where and not ctx.eval_bool(where, candidate=proxy):
                continue
            chosen = obj
            break
        ctx.set_alias(alias, chosen)
        return chosen

    @classmethod
    def pick_up_selected_item(cls, ctx: MobileContext, alias: str, room_message: str = ""):
        item = ctx.resolve(alias)
        if item is None:
            return False
        if not MobileApi.give_room_item_to_mobile(ctx.room, ctx.actor, item):
            return False
        if room_message:
            cls._queue_room_message(ctx, room_message, item=item)
        return ctx.mark_performed()

    @classmethod
    def devour_first_npc_corpse(cls, ctx: MobileContext, room_message: str = "$n savagely devours a corpse.", spill_contents: bool = True):
        actor_label = cls._actor_label(ctx.actor)
        room_label = cls._room_label(ctx.room)
        cls._logger_obj().debug(f"{actor_label}: checking for npc corpse to devour in {room_label}")
        for corpse in ctx.room.items_newest_first():
            item_type = str(corpse.item_type).strip().lower()
            if item_type not in {"npc_corpse", "item_corpse_npc", "corpse_npc"}:
                continue
            cls._logger_obj().debug(
                f"{actor_label}: devouring corpse {corpse.short_description or corpse.name} "
                f"[id={corpse.id}] in {room_label}"
            )
            if room_message:
                cls._queue_room_message(ctx, room_message, item=corpse)
            if spill_contents:
                item_count = len(corpse.contains)
                cls._logger_obj().debug(f"{actor_label}: spilling {item_count} corpse item(s) into {room_label}")
                for item in corpse.contains:
                    ctx.room.add_item_to_room(item)
                corpse.contains = []
            ctx.room.contents.pop(str(corpse.id))
            cls._logger_obj().debug(f"{actor_label}: corpse devoured and removed from {room_label}")
            return ctx.mark_performed()
        cls._logger_obj().debug(f"{actor_label}: no npc corpse available to devour in {room_label}")
        return False

    @classmethod
    def follow_time_script(cls, ctx: MobileContext, open_hour: int, close_hour: int, open_path: str, close_path: str, combat_special: str = ""):
        weather = ctx.handler.weather_handler.time_info
        hour = GenericUtil.to_int((weather.hour if weather is not None else -1), -1)
        state = getattr(ctx.actor, "_special_state", None)
        if not isinstance(state, dict):
            state = {}
            setattr(ctx.actor, "_special_state", state)

        if not state.get("move"):
            if hour == GenericUtil.to_int(open_hour, -1):
                state.update({"path": str(open_path or ""), "move": True, "pos": 0})
            elif hour == GenericUtil.to_int(close_hour, -1):
                state.update({"path": str(close_path or ""), "move": True, "pos": 0})

        if combat_special and ctx.actor.fighting is not None:
            return cls.when_fighting_delegate(ctx, combat_special)

        if not state.get("move"):
            return False
        if CharacterApi.position_value(ctx.actor) < CharacterApi.pos_value("POS_SLEEPING"):
            return False

        path = str(state.get("path", "") or "")
        pos = GenericUtil.to_int(state.get("pos", 0), 0)
        if pos < 0 or pos >= len(path):
            state["move"] = False
            return False

        step = path[pos]
        performed = ctx.performed
        if step in "012345":
            cls._travel_mobile_direction(ctx, int(step))
        elif step == "W":
            CharacterApi.set_position(ctx.actor, "POS_STANDING")
            cls._queue_room_message(ctx, "$n awakens and groans loudly.")
        elif step == "S":
            CharacterApi.set_position(ctx.actor, "POS_SLEEPING")
            cls._queue_room_message(ctx, "$n lies down and falls asleep.")
        elif step == "a":
            cls.say_random(ctx, ["$n says 'Hello Honey!'"])
        elif step == "b":
            cls.say_random(ctx, ["$n says 'What a view!  I must do something about that dump!'"])
        elif step == "c":
            cls.say_random(ctx, ["$n says 'Vandals!  Youngsters have no respect for anything!'"])
        elif step == "d":
            cls.say_random(ctx, ["$n says 'Good day, citizens!'"])
        elif step == "e":
            cls.say_random(ctx, ["$n says 'I hereby declare the city of Midgaard open!'"])
        elif step == "E":
            cls.say_random(ctx, ["$n says 'I hereby declare the city of Midgaard closed!'"])
        elif step == "O":
            ctx.handler.run_door_command(ctx, "open", "gate")
        elif step == "C":
            ctx.handler.run_door_command(ctx, "close", "gate")
        elif step == ".":
            state["move"] = False

        state["pos"] = pos + 1
        # Route steps leave the rest of the mobile pulse available.
        ctx.performed = performed
        return False

    @classmethod
    def poison_bite(cls, ctx: MobileContext, chance_percent: str, messages: tuple[str, str, str]):
        victim = ctx.actor.fighting
        if victim is None or CharacterApi.position_value(ctx.actor) != CharacterApi.pos_value("POS_FIGHTING"):
            return False
        try:
            chance = int(eval(str(chance_percent or "0"), {"__builtins__": {}}, ctx.eval_locals()))
        except Exception:
            chance = 0
        if ctx.handler.rng.number_percent() > chance:
            return False
        cls._queue_combat_act(ctx, victim, messages)
        cls.cast_spell(ctx, "poison", target=victim, direct=True)
        return ctx.mark_performed()

    @classmethod
    def pickpocket_room_player(cls, ctx: MobileContext, discovery_bits: int = 5, immortal_level: str = "LEVEL_IMMORTAL", require_visibility: bool = True, awake_discovery_check: bool = True, gold_cap: str = "", silver_cap: str = ""):
        game_parameters = CharacterApi.get_enum("gameParameters")
        imm_name = str(immortal_level or "").strip().upper()
        imm_value = int(game_parameters[imm_name].value)
        thief_level = max(0, GenericUtil.to_int(ctx.actor.level, 0))
        percentage_cap = thief_level // 2
        for victim in reversed(ctx.room.players_in_room()):
            if GenericUtil.to_int(victim.level, 0) >= imm_value:
                continue
            if ctx.handler.rng.number_bits(GenericUtil.to_int(discovery_bits, 0)) != 0:
                continue
            if require_visibility and not CharacterApi.can_see(ctx.actor, victim, ctx.room):
                continue
            if awake_discovery_check and CharacterApi.is_awake(victim) and ctx.handler.rng.number_range(0, thief_level) == 0:
                cls._queue_combat_act(ctx, victim, ("", "$N discovers $n's hands in $S wallet!",
                                                    "You discover $n's hands in your wallet!"))
                return ctx.mark_performed()

            gold_roll = min(ctx.handler.rng.number_range(1, 20), percentage_cap)
            gold = GenericUtil.to_int(victim.gold, 0) * gold_roll // 100
            if gold_cap:
                try:
                    gold = min(gold, int(eval(str(gold_cap), {"__builtins__": {}}, ctx.eval_locals(victim=victim))))
                except Exception:
                    pass
            victim.gold = max(0, GenericUtil.to_int(victim.gold, 0) - gold)
            ctx.actor.gold = GenericUtil.to_int(ctx.actor.gold, 0) + gold

            silver_roll = min(ctx.handler.rng.number_range(1, 20), percentage_cap)
            silver = GenericUtil.to_int(victim.silver, 0) * silver_roll // 100
            if silver_cap:
                try:
                    silver = min(silver, int(eval(str(silver_cap), {"__builtins__": {}}, ctx.eval_locals(victim=victim))))
                except Exception:
                    pass
            victim.silver = max(0, GenericUtil.to_int(victim.silver, 0) - silver)
            ctx.actor.silver = GenericUtil.to_int(ctx.actor.silver, 0) + silver
            return ctx.mark_performed()
        return False

    @classmethod
    def nasty_opening_attack(cls, ctx: MobileContext, level_window: tuple[int, int], skills: list[str]):
        if CharacterApi.position_value(ctx.actor) == CharacterApi.pos_value("POS_FIGHTING"):
            return False
        minimum, maximum = level_window
        for victim in reversed(ctx.room.players_in_room()):
            delta = GenericUtil.to_int(victim.level, 0) - GenericUtil.to_int(ctx.actor.level, 0)
            if delta < GenericUtil.to_int(minimum, 0) or delta > GenericUtil.to_int(maximum, 0):
                continue
            ctx.set_alias("victim", victim)
            for name in skills:
                ctx.handler.run_combat_command(ctx, name, victim.name)
                if CharacterApi.position_value(ctx.actor) == CharacterApi.pos_value("POS_FIGHTING"):
                    break
            ctx.finish()
            return ctx.mark_performed()
        return False

    @classmethod
    def nasty_combat_turn(cls, ctx: MobileContext, coin_purse_fraction: float = 0.10, flee_weight: int = 1,
                          purse_weight: int = 1, idle_weight: int = 0, purse_messages: tuple[str, str, str] = (
                              "", "$N's coin purse is ripped apart!", "$n rips apart your coin purse, spilling your gold!")):
        victim = ctx.actor.fighting
        if victim is None or CharacterApi.position_value(ctx.actor) != CharacterApi.pos_value("POS_FIGHTING"):
            return False
        action = MobileApi.choose_weighted([("purse", purse_weight), ("flee", flee_weight), ("idle", idle_weight)])
        if action == "purse":
            cls._queue_combat_act(ctx, victim, purse_messages)
            stolen = int(GenericUtil.to_int(victim.gold, 0) * float(coin_purse_fraction))
            victim.gold = max(0, GenericUtil.to_int(victim.gold, 0) - stolen)
            ctx.actor.gold = GenericUtil.to_int(ctx.actor.gold, 0) + stolen
            return ctx.mark_performed()
        if action == "flee":
            ctx.handler.run_combat_command(ctx, "flee")
            return ctx.mark_performed()
        return False

    @staticmethod
    def select_room_fight_intervention_target(ctx: MobileContext, alias: str, exclude_self: bool = True, choose: str = "", randomize: bool = False):
        victim = None
        count = 0
        for entity in ctx.room.people_newest_first():
            if exclude_self and entity is ctx.actor:
                continue
            defender = entity.fighting
            if defender is None:
                continue
            candidate = entity
            if choose == "higher_level_combatant":
                candidate = entity if GenericUtil.to_int(entity.level, 0) > GenericUtil.to_int(defender.level, 0) else defender
            if randomize:
                if ctx.handler.rng.number_range(0, count) == 0:
                    victim = candidate
                count += 1
            else:
                victim = candidate
                break
        ctx.set_alias(alias, victim)
        return victim

    @staticmethod
    def reject_if(ctx: MobileContext, expression: str):
        if ctx.eval_bool(expression):
            ctx.finish()
            return True
        return False

    @classmethod
    def blow_patrol_whistle(cls, ctx: MobileContext, item_vnum: str, slots: list[str],
                           to_char: str, to_room: str, to_area: str):
        if ctx.actor.equipped is None:
            return False
        found = None
        for slot in slots:
            attr = str(slot or "").strip().lower()
            item = getattr(ctx.actor.equipped, attr, None)
            if item is not None and str(item.vnum) == str(item_vnum):
                found = item
                break
        if found is None:
            return False
        if (getattr(ctx.actor, "context", None) or {}).get("controller_original") is not None:
            item_name = found.short_description or found.name
            ctx.queue_payload({"to_victim": to_char.replace("$p", item_name) + "\r\n", "victim": ctx.actor})
        cls._queue_room_message(ctx, to_room, item=found)
        targets = []
        for room in ctx.handler.room_registry.all_rooms():
            if room is None or room is ctx.room:
                continue
            if room.area_id != ctx.room.area_id:
                continue
            targets.extend(room.players_in_room())
            targets.extend(mob for mob in room.mobiles_in_room()
                           if (getattr(mob, "context", None) or {}).get("controller_original") is not None)
        if targets:
            ctx.queue_payload({"global_message": to_area + "\r\n", "global_targets": targets})
        return ctx.mark_performed()

    @classmethod
    def scavenge(cls, ctx: MobileContext, room_message: str = ""):
        actor_label = cls._actor_label(ctx.actor)
        room_label = cls._room_label(ctx.room)
        if not MobileApi.mobile_has_act(ctx.actor, ctx.handler.act_bits, "ACT_SCAVENGER"):
            cls._logger_obj().debug(f"{actor_label}: scavenge skipped in {room_label} because ACT_SCAVENGER is not set")
            return False
        if not ctx.room.contents:
            cls._logger_obj().debug(f"{actor_label}: scavenge skipped in {room_label} because the room has no contents")
            return False
        scavenge_roll = ctx.handler.rng.number_bits(6)
        if scavenge_roll != 0:
            cls._logger_obj().debug(f"{actor_label}: scavenge skipped in {room_label} because number_bits(6) rolled {scavenge_roll}")
            return False

        obj_best = None
        max_cost = 1
        owners = list(cls._live_loot_owners(ctx))
        for obj in ctx.room.items_newest_first():
            if not ItemApi.item_takeable(obj, ctx.handler.wear_flags):
                continue
            if not ItemApi.can_loot(ctx.actor, obj, owners):
                continue
            cost = GenericUtil.to_int(obj.cost, 0)
            if cost > max_cost:
                max_cost = cost
                obj_best = obj
        if obj_best is None:
            cls._logger_obj().debug(f"{actor_label}: scavenge found no takeable item worth taking in {room_label}")
            return False
        MobileApi.give_room_item_to_mobile(ctx.room, ctx.actor, obj_best)
        if room_message:
            cls._queue_room_message(ctx, room_message, item=obj_best)
        cls._logger_obj().debug(
            f"{actor_label}: scavenged {obj_best.short_description or obj_best.name} "
            f"[id={obj_best.id}, cost={obj_best.cost}] in {room_label}"
        )
        return ctx.mark_performed()

    @staticmethod
    def _live_loot_owners(ctx: MobileContext):
        registry = ctx.handler.registry_service.character_registry
        yield from registry.playing.values()
        for room in ctx.handler.room_registry.all_rooms():
            yield from room.characters.values()
            yield from room.mobiles.values()

    @classmethod
    def wander(cls, ctx: MobileContext):
        actor_label = cls._actor_label(ctx.actor)
        room_label = cls._room_label(ctx.room)
        if MobileApi.mobile_has_act(ctx.actor, ctx.handler.act_bits, "ACT_SENTINEL"):
            cls._logger_obj().debug(f"{actor_label}: wander skipped in {room_label} because ACT_SENTINEL is set")
            return False
        wander_roll = ctx.handler.rng.number_bits(3)
        if wander_roll != 0:
            cls._logger_obj().debug(f"{actor_label}: wander skipped in {room_label} because number_bits(3) rolled {wander_roll}")
            return False
        door = ctx.handler.rng.number_bits(5)
        if door > 5:
            cls._logger_obj().debug(f"{actor_label}: wander skipped in {room_label} because chosen door {door} is invalid")
            return False
        cls._logger_obj().debug(f"{actor_label}: wander selected door {door} from {room_label}")
        return cls._wander_mobile_direction(ctx, door)

    @classmethod
    def _wander_mobile_direction(cls, ctx: MobileContext, door: int):
        actor_label = cls._actor_label(ctx.actor)
        room_label = cls._room_label(ctx.room)
        pexit = None
        for ex in ctx.room.exits or []:
            if GenericUtil.to_int(ex.direction, -1) == GenericUtil.to_int(door, -1):
                pexit = ex
                break
        if pexit is None:
            cls._logger_obj().debug(f"{actor_label}: move blocked from {room_label} because no exit exists for door {door}")
            return False

        to_room = MobileApi.resolve_exit_destination(ctx.handler.room_registry, pexit)
        if to_room is None:
            cls._logger_obj().debug(f"{actor_label}: move blocked from {room_label} because door {door} has no destination room")
            return False

        closed_bit = MobileApi.enum_bit(ctx.handler.exit_flags, "EX_CLOSED", "CLOSED")
        if closed_bit and (GenericUtil.to_int(pexit.exit_flags, 0) & closed_bit) != 0:
            cls._logger_obj().debug(f"{actor_label}: move blocked from {room_label} to {cls._room_label(to_room)} because door {door} is closed")
            return False

        no_mob_bit = MobileApi.enum_bit(ctx.handler.room_flags, "ROOM_NO_MOB")
        if no_mob_bit and (GenericUtil.to_int(to_room.room_flags, 0) & no_mob_bit) != 0:
            cls._logger_obj().debug(f"{actor_label}: move blocked from {room_label} to {cls._room_label(to_room)} because ROOM_NO_MOB is set")
            return False

        if MobileApi.mobile_has_act(ctx.actor, ctx.handler.act_bits, "ACT_STAY_AREA") and to_room.area_id != ctx.room.area_id:
            cls._logger_obj().debug(f"{actor_label}: move blocked from {room_label} to {cls._room_label(to_room)} because ACT_STAY_AREA is set")
            return False

        indoors_bit = MobileApi.enum_bit(ctx.handler.room_flags, "ROOM_INDOORS")
        to_indoor = indoors_bit and (GenericUtil.to_int(to_room.room_flags, 0) & indoors_bit) != 0
        if MobileApi.mobile_has_act(ctx.actor, ctx.handler.act_bits, "ACT_OUTDOORS") and to_indoor:
            cls._logger_obj().debug(f"{actor_label}: move blocked from {room_label} to {cls._room_label(to_room)} because ACT_OUTDOORS forbids indoor rooms")
            return False
        if MobileApi.mobile_has_act(ctx.actor, ctx.handler.act_bits, "ACT_INDOORS") and not to_indoor:
            cls._logger_obj().debug(f"{actor_label}: move blocked from {room_label} to {cls._room_label(to_room)} because ACT_INDOORS forbids outdoor rooms")
            return False

        return cls._travel_mobile_direction(ctx, door)

    @classmethod
    def _travel_mobile_direction(cls, ctx: MobileContext, door: int):
        from util.MovementUtil import MovementUtil

        from_room = ctx.room
        payload = ctx.handler.movement_commands.travel(ctx.actor, MovementUtil.DIR_NAME[door], from_room)
        if ctx.actor.room_id == from_room.id:
            return False
        to_room = cls.resolve_room(ctx.handler.room_registry, ctx.actor)
        ctx.queue_payload(payload)
        ctx.room = to_room
        ctx.set_alias("room", to_room)
        cls._logger_obj().debug("%s: moved from %s to %s via door %s", cls._actor_label(ctx.actor),
                               cls._room_label(from_room), cls._room_label(to_room), door)
        return ctx.mark_performed()

    @staticmethod
    def _queue_combat_act(ctx, victim, messages):
        to_char, to_room, to_victim = messages
        for payload in DisplayUtil.combat_act(ctx.actor, victim, ctx.room,
                                              to_char=to_char, to_room=to_room, to_victim=to_victim):
            ctx.queue_payload(payload)

    @staticmethod
    def _queue_room_message(ctx: MobileContext, text: str, *, target=None, item=None,
                            exclude_ids: Optional[set[str]] = None, prompt_listeners: bool = False):
        exclude = {str(ctx.actor.id)} | (exclude_ids or set())
        targets = [listener for listener in DisplayUtil.room_listeners(None, ctx.room)
                   if str(listener.id) not in exclude]
        if not targets:
            return
        def render(observer):
            return DisplayUtil.act_text(text, observer, ctx.room, ctx.actor, target, item)

        fallback = render(None)
        variants = {str(listener.id): render(listener) for listener in targets}
        payload = {"room_message": RecipientText(fallback, variants, fallback), "room_targets": targets}
        if prompt_listeners:
            payload["prompt_listeners"] = True
        ctx.queue_payload(payload)

    @staticmethod
    def _queue_spell_payload(ctx: MobileContext, meta, victim, area: bool):
        spell_label = meta.name
        actor_name = MobileApi.render_mobile_name(ctx.actor)
        payload = {
            "room_message": f"{actor_name} casts {spell_label}" + (".\r\n" if area or victim is None else f" on {MobileApi.render_mobile_name(victim)}.\r\n"),
            "room_targets": ctx.room_players(exclude_ids={str(victim.id)} if victim is not None else set()),
        }
        if victim is not None and not CharacterApi.is_npc(victim):
            payload["victim"] = victim
            payload["to_victim"] = f"{actor_name} casts {spell_label} on you.\r\n"
        ctx.queue_payload(payload)

    @staticmethod
    def choose_weighted(weighted: list[tuple[Any, int]]) -> Any:
        choices = [(value, max(0, GenericUtil.to_int(weight, 0))) for value, weight in weighted]
        total = sum(weight for _, weight in choices)
        if total <= 0:
            return None
        roll = random.randint(1, total)
        running = 0
        for value, weight in choices:
            running += weight
            if roll <= running:
                return value
        return choices[-1][0] if choices else None

    @staticmethod
    def resolve_room(room_registry, entity) -> Any:
        room_id = str(entity.room_id)
        if room_id:
            room = room_registry.get_or_none(id=room_id)
            if room is not None:
                return room
        entity_id = str(entity.id)
        if not entity_id:
            return None
        for room in room_registry.all_rooms():
            if room is None:
                continue
            if entity_id in room.mobiles or entity_id in room.characters:
                return room
        return None

    @staticmethod
    def resolve_exit_destination(room_registry, exit_obj):
        if exit_obj is None:
            return None
        to_room_vnum = exit_obj.to_room_vnum
        if to_room_vnum not in (None, "", "0", 0):
            room = room_registry.get_or_none(vnum=str(to_room_vnum))
            if room is not None:
                return room
        to_room_id = str(exit_obj.to_room_id)
        if to_room_id:
            return room_registry.get_or_none(id=to_room_id)
        return None

    @staticmethod
    def move_mobile(room, to_room, mob) -> bool:
        if room is None or to_room is None or mob is None:
            return False
        if callable(getattr(room, 'remove_mobile_from_room', None)):
            room.remove_mobile_from_room(mob)
        else:
            room.mobiles.pop(str(mob.id))
        if callable(getattr(to_room, 'add_mobile_to_room', None)):
            to_room.add_mobile_to_room(mob)
        else:
            to_room.mobiles[str(mob.id)] = mob
        mob.room_id = to_room.id
        mob.area_id = to_room.area_id
        return True

    @staticmethod
    def give_room_item_to_mobile(room, mob, item) -> bool:
        if room is None or mob is None or item is None:
            return False
        room.contents.pop(str(item.id))
        mob.add_item(item)
        return True

    @staticmethod
    def render_mobile_name(entity) -> str:
        return DisplayUtil.entity_name(entity, is_npc=CharacterApi.is_npc)

    @staticmethod
    def group_vnum(group_name: str) -> str:
        mapping = {
            "GROUP_VNUM_TROLLS": "2100",
            "GROUP_VNUM_OGRES": "2101",
        }
        normalized = str(group_name or "").strip().upper()
        return mapping.get(normalized, normalized)

    @classmethod
    def mobile_is_charmed(cls, mob: Any) -> bool:
        charm = cls.enum_bit(cls.get_enum("affectedBy"), "AFF_CHARM")
        if charm == 0:
            return False
        status_flags = mob.status_flags if mob is not None else None
        flags = GenericUtil.to_int(status_flags.affected_by if status_flags is not None else 0, 0)
        return (flags & charm) != 0

    @classmethod
    def mobile_has_act(cls, mob: Any, act_bits, name: str) -> bool:
        bit = cls.enum_bit(act_bits, name)
        if bit == 0:
            return False
        status_flags = mob.status_flags if mob is not None else None
        flags = GenericUtil.to_int(status_flags.act if status_flags is not None else 0, 0)
        return (flags & bit) != 0

    @classmethod
    def mobile_is_standing(cls, mob: Any) -> bool:
        positions = cls.get_enum("positions")
        standing = cls.enum_bit(positions, "POS_STANDING")
        return AnimateEntity.position_value(mob, positions, default_position=standing) == standing

    @classmethod
    def mobile_will_assist(cls, char: Mobile) -> bool:
        if type(char) is not Mobile:
            return False
        OffenseTypes = cls.get_enum("offenseTypes")
        return cls.is_set(char.status_flags.off, OffenseTypes.ASSIST_PLAYERS.value)

    @staticmethod
    def is_train_trainer(mob, train_bit: int) -> bool:
        mob_flags = GenericUtil.to_int(mob.status_flags.act, 0)
        if train_bit and CharacterApi.is_set(mob_flags, train_bit):
            return True

        special_name = str(mob.special_name).strip().lower()
        if special_name == "spec_cast_adept":
            return True

        description_text = " ".join(
            [
                str(mob.long_description.strip().lower()),
                str(mob.description.strip().lower())
            ]
        )
        trainer_phrases = (
            "waiting to train you",
            "ready to train you",
            "ready to help you train",
            "help you train",
            "training young students",
            "training students",
        )
        return any(phrase in description_text for phrase in trainer_phrases)

    @staticmethod
    def is_practice_trainer(mob, practice_bit: int) -> bool:
        mob_flags = GenericUtil.to_int(mob.status_flags.act, 0)
        if practice_bit and CharacterApi.is_set(mob_flags, practice_bit):
            return True

        special_name = str(mob.special_name).strip().lower()
        if special_name == "spec_cast_adept":
            return True

        long_description = str(mob.long_description).strip().lower()
        if "help you practice" in long_description or "ready to help you practice" in long_description:
            return True

        return False
