from __future__ import annotations

import random

from types import SimpleNamespace
from typing import Any, Optional

from api.GameApi import GameApi
from api.ItemApi import ItemApi
from mobile.Mobile import Mobile
from util.GenericUtil import GenericUtil
from util.FightUtil import FightUtil
from mobile.MobileContext import MobileContext
from api.CharacterApi import CharacterApi
from server.LoggerFactory import LoggerFactory
from skill.SpellContext import SpellContext


class MobileApi(GameApi):
    _logger = None

    @classmethod
    def lazy_load(cls, weather_handler, registry_service=None) -> None:
        if registry_service is not None:
            cls._registry_service = registry_service
        cls._weather_handler = weather_handler
        cls.load_enums(
            TimeAndWeather="timeAndWeather",
            GameParameters="gameParameters",
            AffectedBits="affectedBy",
            positions="positions",
            RoomFlags="roomFlags",
            CommFlags="commFlags",
            PlayerActBits="playerActBits",
            OffenseTypes="offenseTypes",
            SectorTypes="sectorTypes",
        )

    @classmethod
    def _reset_internal_variables(cls) -> None:
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
        actor_id = str(getattr(actor, "id", "") or "").strip()
        if short_desc:
            return f"{short_desc} [vnum={vnum}, id={actor_id}]"
        name = str(getattr(actor, "name", "unknown-mobile") or "unknown-mobile").strip()
        return f"{name} [vnum={vnum}, id={actor_id}]"

    @staticmethod
    def _room_label(room) -> str:
        if room is None:
            return "no-room"
        name = str(getattr(room, "name", "") or "").strip()
        vnum = str(getattr(room, "vnum", "") or "").strip()
        room_id = str(getattr(room, "id", "") or "").strip()
        return f"{name or 'unnamed-room'} [vnum={vnum}, id={room_id}]"

    @classmethod
    def require_awake(cls, ctx: MobileContext):
        if not CharacterApi.is_awake(ctx.actor):
            ctx.finish()
            return False
        return True

    @staticmethod
    def require_not_fighting(ctx: MobileContext):
        if getattr(ctx.actor, "fighting", None) is not None:
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
    def when_fighting_delegate(ctx: MobileContext, special_name: str):
        if getattr(ctx.actor, "fighting", None) is None:
            return False
        return ctx.handler.execute_special_by_name(ctx.actor, special_name, ctx.room, ctx)

    @staticmethod
    def select_visible_room_player(ctx: MobileContext, alias: str, exclude_self: bool = True, max_level: Optional[int] = None, chance_bits: int = 0):
        target = None
        for player in ctx.room.player_in_room().values():
            if exclude_self and player is ctx.actor:
                continue
            if max_level is not None and GenericUtil.to_int(getattr(player, "level", 0), 0) > GenericUtil.to_int(max_level, 0):
                continue
            if not CharacterApi.can_see(ctx.actor, player, ctx.handler.room_helper):
                continue
            if chance_bits > 0 and ctx.handler.rng.number_bits(GenericUtil.to_int(chance_bits, 0)) != 0:
                continue
            target = player
            break
        ctx.set_alias(alias, target)
        return target

    @staticmethod
    def select_room_combat_victim(ctx: MobileContext, alias: str, chance_bits: int = 0):
        target = None
        for entity in ctx.room.in_room().values():
            if getattr(entity, "fighting", None) is ctx.actor:
                if chance_bits > 0 and ctx.handler.rng.number_bits(GenericUtil.to_int(chance_bits, 0)) != 0:
                    continue
                target = entity
                break
        ctx.set_alias(alias, target)
        return target

    @classmethod
    def cast_dragon_breath(cls, ctx: MobileContext, spell_name: str):
        target = getattr(ctx.actor, "fighting", None)
        if target is None:
            ctx.finish()
            return False
        return cls.cast_spell(ctx, spell_name, target=target)

    @classmethod
    def cast_spell(cls, ctx: MobileContext, spell_name: str, target: Any = "victim"):
        spell_key = str(spell_name or "").strip().lower()
        spell = FightUtil.find_spell(ctx.handler.spell_registry, spell_key)
        skill = FightUtil.find_spell_skill(ctx.handler.skill_registry, ctx.actor, spell_key)
        meta = spell if spell is not None else skill
        if meta is None:
            return False

        target_value = ctx.resolve(target)
        if target_value == "room":
            spell_context = SpellContext(
                actor=ctx.actor,
                spell=meta,
                handler=ctx.handler,
                room=ctx.room,
                target=None,
                target_name="room",
                target_kind="room",
                source="mobile",
            )
            ctx.handler.spell_api.execute_lambdas(spell_context)
            if not spell_context.performed:
                return False
            cls._queue_spell_payload(ctx, meta, None, area=True)
            for payload in spell_context.payloads:
                ctx.queue_payload(payload)
            return ctx.mark_performed()

        victim = target_value
        if victim is None:
            return False
        spell_context = SpellContext(
            actor=ctx.actor,
            spell=meta,
            handler=ctx.handler,
            room=ctx.room,
            target=victim,
            target_name=str(getattr(victim, "name", getattr(victim, "short_description", "")) or ""),
            target_kind="obj" if hasattr(victim, "item_type") else "char",
            source="mobile",
        )
        ctx.handler.spell_api.execute_lambdas(spell_context)
        if not spell_context.performed:
            return False
        cls._queue_spell_payload(ctx, meta, victim if not hasattr(victim, "item_type") else None, area=False)
        for payload in spell_context.payloads:
            ctx.queue_payload(payload)
        return ctx.mark_performed()

    @classmethod
    def cast_weighted_support_spell(cls, ctx: MobileContext, target_alias: str, weighted_spells: list[tuple[str, int, str]], miss_weight: int = 0):
        victim = ctx.resolve(target_alias)
        if victim is None:
            return False
        choices = []
        for spell_name, min_level, message in weighted_spells:
            if GenericUtil.to_int(getattr(ctx.actor, "level", 0), 0) >= GenericUtil.to_int(min_level, 0):
                choices.append(((spell_name, message), 1))
        if miss_weight > 0:
            choices.append((None, GenericUtil.to_int(miss_weight, 0)))
        picked = MobileApi.choose_weighted(choices)
        if not picked:
            return False
        spell_name, message = picked
        if message:
            cls._queue_room_message(ctx, MobileApi.render_act(message, ctx.actor, victim) + "\r\n")
        return cls.cast_spell(ctx, spell_name, target=victim)

    @classmethod
    def cast_weighted_combat_spell(cls, ctx: MobileContext, target_alias: str, weighted_spells: list[tuple[str, int, int]]):
        victim = ctx.resolve(target_alias)
        if victim is None:
            return False
        choices = []
        for spell_name, min_level, weight in weighted_spells:
            if GenericUtil.to_int(getattr(ctx.actor, "level", 0), 0) >= GenericUtil.to_int(min_level, 0):
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
        for player in ctx.room.players_in_room().values():
            if visible_only and not CharacterApi.can_see(ctx.actor, player, ctx.handler.room_helper):
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
        ctx.queue_payload({"area_message": f"{formatted}\r\n", "area_id": getattr(ctx.actor, "area_id", "")})
        return ctx.mark_performed()

    @staticmethod
    def multi_hit(ctx: MobileContext, victim_alias: str):
        victim = ctx.resolve(victim_alias)
        if victim is None or ctx.room is None:
            return False
        safe, _ = ctx.handler.fight_handler.is_safe(ctx.actor, victim, room=ctx.room)
        if safe:
            return False
        if getattr(ctx.actor, "fighting", None) is None:
            ctx.handler.fight_handler.set_fighting(ctx.actor, victim, ctx.room.id)
        if getattr(victim, "fighting", None) is None:
            ctx.handler.fight_handler.set_fighting(victim, ctx.actor, ctx.room.id)
        result = ctx.handler.fight_handler.multi_hit(ctx.actor, victim, dt="TYPE_UNDEFINED")
        payload = {
            "to_room": result.get("to_room", ""),
            "targets": [player for player in ctx.room.players_in_room().values() if str(getattr(player, "id", "")) != str(getattr(victim, "id", ""))],
        }
        if not CharacterApi.is_npc(victim):
            payload["victim"] = victim
            payload["to_victim"] = result.get("to_victim", "")
        ctx.queue_payload(payload)
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
        for entity in ctx.room.in_room().values():
            if exclude_target == "self" and entity is ctx.actor:
                continue
            if getattr(entity, "fighting", None) is None or getattr(entity, "fighting", None) is ctx.actor:
                continue
            alignment = GenericUtil.to_int(getattr(entity, "alignment", getattr(getattr(entity, "character_attributes", None), "alignment", 0)), 0)
            if alignment < max_evil:
                max_evil = alignment
                best = entity
        ctx.set_alias(alias, best)
        return best

    @classmethod
    def when_selected_attack(cls, ctx: MobileContext, alias: str, room_message: str = ""):
        victim = ctx.resolve(alias)
        if victim is None:
            return False
        if room_message:
            cls._queue_room_message(ctx, f"{room_message}\r\n")
        return cls.multi_hit(ctx, alias)

    @staticmethod
    def select_room_npc_by_group(ctx: MobileContext, alias: str, group_vnum: str, exclude_vnum: str = "", where: str = "", randomize: bool = False):
        excluded = str(exclude_vnum or "").strip().upper()
        if excluded == "MOB_VNUM_PATROLMAN":
            for mob in list(getattr(ctx.room, "mobiles", {}).values()):
                if str(getattr(mob, "vnum", "") or "") == "2106":
                    ctx.set_alias(alias, None)
                    return None

        wanted_group = MobileApi.group_vnum(group_vnum)
        selected = None
        count = 0
        for mob in list(getattr(ctx.room, "mobiles", {}).values()):
            if mob is ctx.actor:
                continue
            if str(getattr(mob, "group", "") or "") != wanted_group:
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
        selected = random.choice(messages)
        if allow_none and ctx.handler.rng.number_range(0, len(messages)) == 0:
            return False
        cls._queue_room_message(ctx, MobileApi.render_act(selected, ctx.actor, target_value) + "\r\n")
        return ctx.mark_performed()

    @staticmethod
    def select_room_item(ctx: MobileContext, alias: str, where: str = ""):
        chosen = None
        for obj in list(getattr(ctx.room, "contents", {}).values()):
            proxy = SimpleNamespace(
                obj=obj,
                can_take=ItemApi.item_takeable(obj, ctx.handler.wear_flags),
                can_loot=True,
                item_type=str(getattr(obj, "item_type", "") or ""),
                cost=GenericUtil.to_int(getattr(obj, "cost", 0), 0),
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
            cls._queue_room_message(ctx, f"{room_message}\r\n")
        return ctx.mark_performed()

    @classmethod
    def devour_first_npc_corpse(cls, ctx: MobileContext, room_message: str = "$n savagely devours a corpse.", spill_contents: bool = True):
        actor_label = cls._actor_label(ctx.actor)
        room_label = cls._room_label(ctx.room)
        cls._logger_obj().debug(f"{actor_label}: checking for npc corpse to devour in {room_label}")
        for corpse in list(getattr(ctx.room, "contents", {}).values()):
            item_type = str(getattr(corpse, "item_type", "") or "").strip().lower()
            if item_type not in {"npc_corpse", "item_corpse_npc", "corpse_npc"}:
                continue
            cls._logger_obj().debug(
                f"{actor_label}: devouring corpse {getattr(corpse, 'short_description', '') or getattr(corpse, 'name', 'corpse')} "
                f"[id={getattr(corpse, 'id', '')}] in {room_label}"
            )
            if room_message:
                cls._queue_room_message(ctx, MobileApi.render_act(room_message, ctx.actor) + "\r\n")
            if spill_contents:
                item_count = len(list(getattr(corpse, "contains", []) or []))
                cls._logger_obj().debug(f"{actor_label}: spilling {item_count} corpse item(s) into {room_label}")
                for item in list(getattr(corpse, "contains", []) or []):
                    ctx.room.add_item_to_room(item)
                corpse.contains = []
            ctx.room.contents.pop(str(getattr(corpse, "id", "") or ""), None)
            cls._logger_obj().debug(f"{actor_label}: corpse devoured and removed from {room_label}")
            return ctx.mark_performed()
        cls._logger_obj().debug(f"{actor_label}: no npc corpse available to devour in {room_label}")
        return False

    @classmethod
    def follow_time_script(cls, ctx: MobileContext, open_hour: int, close_hour: int, open_path: str, close_path: str):
        weather = getattr(ctx.handler.weather_handler, "time_info", None)
        hour = GenericUtil.to_int(getattr(weather, "hour", -1), -1)
        state = getattr(ctx.actor, "_special_state", None)
        if not isinstance(state, dict):
            state = {}
            setattr(ctx.actor, "_special_state", state)

        if not state.get("move"):
            if hour == GenericUtil.to_int(open_hour, -1):
                state.update({"path": str(open_path or ""), "move": True, "pos": 0})
            elif hour == GenericUtil.to_int(close_hour, -1):
                state.update({"path": str(close_path or ""), "move": True, "pos": 0})

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
        acted = False
        if step in "012345":
            acted = cls._move_mobile_direction(ctx, int(step))
        elif step == "W":
            setattr(ctx.actor, "position", CharacterApi.pos_value("POS_STANDING"))
            cls._queue_room_message(ctx, f"{MobileApi.render_mobile_name(ctx.actor)} awakens and groans loudly.\r\n")
            acted = True
        elif step == "S":
            setattr(ctx.actor, "position", CharacterApi.pos_value("POS_SLEEPING"))
            cls._queue_room_message(ctx, f"{MobileApi.render_mobile_name(ctx.actor)} lies down and falls asleep.\r\n")
            acted = True
        elif step == "a":
            acted = bool(cls.say_random(ctx, ["$n says 'Hello Honey!'"]))
        elif step == "b":
            acted = bool(cls.say_random(ctx, ["$n says 'What a view!  I must do something about that dump!'"]))
        elif step == "c":
            acted = bool(cls.say_random(ctx, ["$n says 'Vandals!  Youngsters have no respect for anything!'"]))
        elif step == "d":
            acted = bool(cls.say_random(ctx, ["$n says 'Good day, citizens!'"]))
        elif step == "e":
            acted = bool(cls.say_random(ctx, ["$n says 'I hereby declare the city of Midgaard open!'"]))
        elif step == "E":
            acted = bool(cls.say_random(ctx, ["$n says 'I hereby declare the city of Midgaard closed!'"]))
        elif step == "O":
            acted = cls._toggle_gate(ctx, close=False)
        elif step == "C":
            acted = cls._toggle_gate(ctx, close=True)
        elif step == ".":
            state["move"] = False

        state["pos"] = pos + 1
        if acted:
            ctx.mark_performed()
        return acted

    @classmethod
    def poison_bite(cls, ctx: MobileContext, chance_percent: str, messages: tuple[str, str, str]):
        victim = getattr(ctx.actor, "fighting", None)
        if victim is None or CharacterApi.position_value(ctx.actor) != CharacterApi.pos_value("POS_FIGHTING"):
            return False
        try:
            chance = int(eval(str(chance_percent or "0"), {"__builtins__": {}}, ctx.eval_locals()))
        except Exception:
            chance = 0
        if ctx.handler.rng.number_percent() > chance:
            return False
        _to_char, to_room, to_victim = messages
        if to_room:
            cls._queue_room_message(ctx, MobileApi.render_act(to_room, ctx.actor, victim) + "\r\n", exclude_ids={str(getattr(victim, "id", ""))})
        if not CharacterApi.is_npc(victim) and to_victim:
            ctx.queue_payload({"victim": victim, "to_victim": MobileApi.render_act(to_victim, ctx.actor, victim) + "\r\n"})
        cls.cast_spell(ctx, "poison", target=victim)
        return ctx.mark_performed()

    @classmethod
    def pickpocket_room_player(cls, ctx: MobileContext, discovery_bits: int = 5, immortal_level: str = "LEVEL_IMMORTAL", require_visibility: bool = True, awake_discovery_check: bool = True, gold_cap: str = "", silver_cap: str = ""):
        game_parameters = CharacterApi.get_enum("gameParameters")
        imm_name = str(immortal_level or "").strip().upper()
        imm_value = int(getattr(getattr(game_parameters, imm_name, None), "value", 100))
        for victim in ctx.room.players_in_room().values():
            if GenericUtil.to_int(getattr(victim, "level", 0), 0) >= imm_value:
                continue
            if ctx.handler.rng.number_bits(GenericUtil.to_int(discovery_bits, 0)) != 0:
                continue
            if require_visibility and not CharacterApi.can_see(ctx.actor, victim, ctx.handler.room_helper):
                continue
            if awake_discovery_check and CharacterApi.is_awake(victim) and ctx.handler.rng.number_range(0, max(0, GenericUtil.to_int(getattr(ctx.actor, "level", 0), 0))) == 0:
                ctx.queue_payload({"victim": victim, "to_victim": f"You discover {MobileApi.render_mobile_name(ctx.actor)}'s hands in your wallet!\r\n"})
                cls._queue_room_message(ctx, f"{MobileApi.render_mobile_name(victim)} discovers {MobileApi.render_mobile_name(ctx.actor)}'s hands in {MobileApi.render_mobile_name(victim)}'s wallet!\r\n", exclude_ids={str(getattr(victim, 'id', ''))})
                return ctx.mark_performed()

            gold_roll = min(ctx.handler.rng.number_range(1, 20), max(1, GenericUtil.to_int(getattr(ctx.actor, "level", 0), 0) // 2))
            gold = GenericUtil.to_int(getattr(victim, "gold", 0), 0) * gold_roll // 100
            if gold_cap:
                try:
                    gold = min(gold, int(eval(str(gold_cap), {"__builtins__": {}}, ctx.eval_locals(victim=victim))))
                except Exception:
                    pass
            victim.gold = max(0, GenericUtil.to_int(getattr(victim, "gold", 0), 0) - gold)
            ctx.actor.gold = GenericUtil.to_int(getattr(ctx.actor, "gold", 0), 0) + gold

            silver_roll = min(ctx.handler.rng.number_range(1, 20), max(1, GenericUtil.to_int(getattr(ctx.actor, "level", 0), 0) // 2))
            silver = GenericUtil.to_int(getattr(victim, "silver", 0), 0) * silver_roll // 100
            if silver_cap:
                try:
                    silver = min(silver, int(eval(str(silver_cap), {"__builtins__": {}}, ctx.eval_locals(victim=victim))))
                except Exception:
                    pass
            victim.silver = max(0, GenericUtil.to_int(getattr(victim, "silver", 0), 0) - silver)
            ctx.actor.silver = GenericUtil.to_int(getattr(ctx.actor, "silver", 0), 0) + silver
            return ctx.mark_performed()
        return False

    @classmethod
    def nasty_opening_attack(cls, ctx: MobileContext, level_window: tuple[int, int], skills: list[str]):
        if CharacterApi.position_value(ctx.actor) == CharacterApi.pos_value("POS_FIGHTING"):
            return False
        minimum, maximum = level_window
        for victim in ctx.room.players_in_room().values():
            delta = GenericUtil.to_int(getattr(victim, "level", 0), 0) - GenericUtil.to_int(getattr(ctx.actor, "level", 0), 0)
            if delta < GenericUtil.to_int(minimum, 0) or delta > GenericUtil.to_int(maximum, 0):
                continue
            ctx.set_alias("victim", victim)
            return cls.multi_hit(ctx, "victim")
        return False

    @classmethod
    def nasty_combat_turn(cls, ctx: MobileContext, coin_purse_fraction: float = 0.10, flee_weight: int = 1, purse_weight: int = 1, idle_weight: int = 0):
        victim = getattr(ctx.actor, "fighting", None)
        if victim is None:
            return False
        action = MobileApi.choose_weighted([("purse", purse_weight), ("flee", flee_weight), ("idle", idle_weight)])
        if action == "purse":
            stolen = int(GenericUtil.to_int(getattr(victim, "gold", 0), 0) * float(coin_purse_fraction))
            victim.gold = max(0, GenericUtil.to_int(getattr(victim, "gold", 0), 0) - stolen)
            ctx.actor.gold = GenericUtil.to_int(getattr(ctx.actor, "gold", 0), 0) + stolen
            if not CharacterApi.is_npc(victim):
                ctx.queue_payload({"victim": victim, "to_victim": "Someone rips apart your coin purse, spilling your gold!\r\n"})
            cls._queue_room_message(ctx, f"{MobileApi.render_mobile_name(victim)}'s coin purse is ripped apart!\r\n", exclude_ids={str(getattr(victim, 'id', ''))})
            return ctx.mark_performed()
        if action == "flee":
            ctx.handler.fight_handler.stop_fighting(ctx.actor, both=False)
            return ctx.mark_performed()
        return False

    @staticmethod
    def select_room_fight_intervention_target(ctx: MobileContext, alias: str, exclude_self: bool = True, choose: str = "", randomize: bool = False):
        victim = None
        count = 0
        for entity in ctx.room.in_room().values():
            if exclude_self and entity is ctx.actor:
                continue
            defender = getattr(entity, "fighting", None)
            if defender is None:
                continue
            candidate = entity
            if choose == "higher_level_combatant":
                candidate = entity if GenericUtil.to_int(getattr(entity, "level", 0), 0) > GenericUtil.to_int(getattr(defender, "level", 0), 0) else defender
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
    def blow_patrol_whistle(cls, ctx: MobileContext, item_vnum: str, slots: list[str]):
        equipped = getattr(ctx.actor, "equipped", None)
        if equipped is None:
            return False
        found = None
        for slot in slots:
            attr = str(slot or "").strip().lower()
            item = getattr(equipped, attr, None)
            if item is not None and str(getattr(item, "vnum", "") or "") == "2116":
                found = item
                break
        if found is None:
            return False
        cls._queue_room_message(ctx, f"{MobileApi.render_mobile_name(ctx.actor)} blows on {MobileApi.render_mobile_name(found)}, ***WHEEEEEEEEEEEET***\r\n")
        targets = []
        for room in ctx.handler.room_registry.all_rooms():
            if room is None or room is ctx.room:
                continue
            if getattr(room, "area_id", "") != getattr(ctx.room, "area_id", ""):
                continue
            targets.extend(list(getattr(room, "characters", {}).values()))
        if targets:
            ctx.queue_payload({"global_message": "You hear a shrill whistling sound.\n\r", "global_targets": targets})
        return ctx.mark_performed()

    @classmethod
    def scavenge(cls, ctx: MobileContext):
        actor_label = cls._actor_label(ctx.actor)
        room_label = cls._room_label(ctx.room)
        if not MobileApi.mobile_has_act(ctx.actor, ctx.handler.act_bits, "ACT_SCAVENGER"):
            cls._logger_obj().debug(f"{actor_label}: scavenge skipped in {room_label} because ACT_SCAVENGER is not set")
            return False
        if not getattr(ctx.room, "contents", {}):
            cls._logger_obj().debug(f"{actor_label}: scavenge skipped in {room_label} because the room has no contents")
            return False
        scavenge_roll = ctx.handler.rng.number_bits(6)
        if scavenge_roll != 0:
            cls._logger_obj().debug(f"{actor_label}: scavenge skipped in {room_label} because number_bits(6) rolled {scavenge_roll}")
            return False

        obj_best = None
        max_cost = 1
        for obj in list(ctx.room.contents.values()):
            if not ItemApi.item_takeable(obj, ctx.handler.wear_flags):
                continue
            cost = GenericUtil.to_int(getattr(obj, "cost", 0), 0)
            if cost > max_cost:
                max_cost = cost
                obj_best = obj
        if obj_best is None:
            cls._logger_obj().debug(f"{actor_label}: scavenge found no takeable item worth taking in {room_label}")
            return False
        MobileApi.give_room_item_to_mobile(ctx.room, ctx.actor, obj_best)
        cls._logger_obj().debug(
            f"{actor_label}: scavenged {getattr(obj_best, 'short_description', '') or getattr(obj_best, 'name', 'item')} "
            f"[id={getattr(obj_best, 'id', '')}, cost={getattr(obj_best, 'cost', 0)}] in {room_label}"
        )
        return ctx.mark_performed()

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
        return cls._move_mobile_direction(ctx, door)

    @classmethod
    def _move_mobile_direction(cls, ctx: MobileContext, door: int):
        actor_label = cls._actor_label(ctx.actor)
        room_label = cls._room_label(ctx.room)
        pexit = None
        for ex in getattr(ctx.room, "exits", []) or []:
            if GenericUtil.to_int(getattr(ex, "direction", -1), -1) == GenericUtil.to_int(door, -1):
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
        if closed_bit and (GenericUtil.to_int(getattr(pexit, "exit_flags", 0), 0) & closed_bit) != 0:
            cls._logger_obj().debug(f"{actor_label}: move blocked from {room_label} to {cls._room_label(to_room)} because door {door} is closed")
            return False

        no_mob_bit = MobileApi.enum_bit(ctx.handler.room_flags, "ROOM_NO_MOB")
        if no_mob_bit and (GenericUtil.to_int(getattr(to_room, "room_flags", 0), 0) & no_mob_bit) != 0:
            cls._logger_obj().debug(f"{actor_label}: move blocked from {room_label} to {cls._room_label(to_room)} because ROOM_NO_MOB is set")
            return False

        if MobileApi.mobile_has_act(ctx.actor, ctx.handler.act_bits, "ACT_STAY_AREA") and getattr(to_room, "area_id", "") != getattr(ctx.room, "area_id", ""):
            cls._logger_obj().debug(f"{actor_label}: move blocked from {room_label} to {cls._room_label(to_room)} because ACT_STAY_AREA is set")
            return False

        indoors_bit = MobileApi.enum_bit(ctx.handler.room_flags, "ROOM_INDOORS")
        to_indoor = indoors_bit and (GenericUtil.to_int(getattr(to_room, "room_flags", 0), 0) & indoors_bit) != 0
        if MobileApi.mobile_has_act(ctx.actor, ctx.handler.act_bits, "ACT_OUTDOORS") and to_indoor:
            cls._logger_obj().debug(f"{actor_label}: move blocked from {room_label} to {cls._room_label(to_room)} because ACT_OUTDOORS forbids indoor rooms")
            return False
        if MobileApi.mobile_has_act(ctx.actor, ctx.handler.act_bits, "ACT_INDOORS") and not to_indoor:
            cls._logger_obj().debug(f"{actor_label}: move blocked from {room_label} to {cls._room_label(to_room)} because ACT_INDOORS forbids outdoor rooms")
            return False

        if not MobileApi.move_mobile(ctx.room, to_room, ctx.actor):
            cls._logger_obj().debug(f"{actor_label}: move failed from {room_label} to {cls._room_label(to_room)} for door {door}")
            return False
        ctx.room = to_room
        ctx.set_alias("room", to_room)
        cls._logger_obj().debug(f"{actor_label}: moved from {room_label} to {cls._room_label(to_room)} via door {door}")
        return ctx.mark_performed()

    @staticmethod
    def _toggle_gate(ctx: MobileContext, close: bool):
        changed = False
        closed_bit = MobileApi.enum_bit(ctx.handler.exit_flags, "EX_CLOSED", "CLOSED")
        if not closed_bit:
            return False
        for ex in getattr(ctx.room, "exits", []) or []:
            keyword = str(getattr(ex, "keyword", "") or "").strip().lower()
            if keyword != "gate":
                continue
            flags = GenericUtil.to_int(getattr(ex, "exit_flags", 0), 0)
            if close:
                flags |= closed_bit
            else:
                flags &= ~closed_bit
            ex.exit_flags = flags
            changed = True
        return changed

    @staticmethod
    def _queue_room_message(ctx: MobileContext, text: str, exclude_ids: Optional[set[str]] = None):
        targets = ctx.room_players(exclude_ids=exclude_ids)
        if not targets:
            return
        ctx.queue_payload({"room_message": text, "room_targets": targets})

    @staticmethod
    def _queue_spell_payload(ctx: MobileContext, meta, victim, area: bool):
        spell_label = getattr(meta, "name", "spell")
        actor_name = MobileApi.render_mobile_name(ctx.actor)
        payload = {
            "room_message": f"{actor_name} casts {spell_label}" + (".\r\n" if area or victim is None else f" on {MobileApi.render_mobile_name(victim)}.\r\n"),
            "room_targets": ctx.room_players(exclude_ids={str(getattr(victim, 'id', ''))} if victim is not None else set()),
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
        room_id = str(getattr(entity, "room_id", "") or "")
        if room_id:
            room = room_registry.get_or_none(id=room_id)
            if room is not None:
                return room
        entity_id = str(getattr(entity, "id", "") or "")
        if not entity_id:
            return None
        for room in room_registry.all_rooms():
            if room is None:
                continue
            if entity_id in getattr(room, "mobiles", {}) or entity_id in getattr(room, "characters", {}):
                return room
        return None

    @staticmethod
    def resolve_exit_destination(room_registry, exit_obj):
        if exit_obj is None:
            return None
        to_room_vnum = getattr(exit_obj, "to_room_vnum", None)
        if to_room_vnum not in (None, "", "0", 0):
            room = room_registry.get_or_none(vnum=str(to_room_vnum))
            if room is not None:
                return room
        to_room_id = str(getattr(exit_obj, "to_room_id", "") or "")
        if to_room_id:
            return room_registry.get_or_none(id=to_room_id)
        return None

    @staticmethod
    def move_mobile(room, to_room, mob) -> bool:
        if room is None or to_room is None or mob is None:
            return False
        room.mobiles.pop(str(getattr(mob, "id", "") or ""), None)
        to_room.mobiles[str(getattr(mob, "id", "") or "")] = mob
        setattr(mob, "room_id", getattr(to_room, "id", ""))
        setattr(mob, "area_id", getattr(to_room, "area_id", ""))
        return True

    @staticmethod
    def give_room_item_to_mobile(room, mob, item) -> bool:
        if room is None or mob is None or item is None:
            return False
        room.contents.pop(str(getattr(item, "id", "") or ""), None)
        MobileUtil.add_inventory_item(mob, item)
        return True

    @staticmethod
    def render_mobile_name(entity) -> str:
        if entity is None:
            return "someone"
        if CharacterApi.is_npc(entity):
            return str(getattr(entity, "short_description", "") or getattr(entity, "name", "someone"))
        return str(getattr(entity, "name", "someone"))

    @staticmethod
    def render_act(text: str, actor, target=None) -> str:
        rendered = str(text or "")
        rendered = rendered.replace("$n", MobileApi.render_mobile_name(actor))
        rendered = rendered.replace("$N", MobileApi.render_mobile_name(target))
        if target is not None:
            sex = str(getattr(target, "sex", "") or "").lower()
            poss = "their"
            if sex in ("1", "m", "male"):
                poss = "his"
            elif sex in ("2", "f", "female"):
                poss = "her"
            rendered = rendered.replace("$S", poss)
        return rendered

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
        flags = GenericUtil.to_int(getattr(getattr(mob, "status_flags", None), "affected_by", 0), 0)
        return (flags & charm) != 0

    @classmethod
    def mobile_has_act(cls, mob: Any, act_bits, name: str) -> bool:
        bit = cls.enum_bit(act_bits, name)
        if bit == 0:
            return False
        flags = GenericUtil.to_int(getattr(getattr(mob, "status_flags", None), "act", 0), 0)
        return (flags & bit) != 0

    @classmethod
    def mobile_is_standing(cls, mob: Any) -> bool:
        standing = cls.enum_bit(cls.get_enum("positions"), "POS_STANDING")
        current = GenericUtil.to_int(getattr(mob, "position", getattr(mob, "start_pos", standing)), standing)
        return current == standing

    @classmethod
    def mobile_will_assist(cls, char: Mobile) -> bool:
        if type(char) is not Mobile:
            return False
        OffenseTypes = cls.get_enum("offenseTypes")
        return cls.is_set(char.status_flags.off, OffenseTypes.ASSIST_PLAYERS.value)