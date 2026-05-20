from __future__ import annotations

import random

from injector import inject

from api.FightApi import FightApi
from fight.FightHandler import FightHandler
from game.EnumProvider import EnumProvider
from game.RegistryService import RegistryService
from game.WeatherHandler import WeatherHandler
from interp.Context import Context
from item.Effect import Effect
from item.EffectHandler import EffectHandler
from player.Character import Character
from player.CharacterAdvancement import CharacterAdvancement
from api.CharacterApi import CharacterApi
from api.InterpApi import InterpApi
from server.LoggerFactory import LoggerFactory
from skill import Skill
from api.SkillApi import SkillApi
from api.SpellApi import SpellApi
from skill.SpellContext import SpellContext
from util.EffectUtil import EffectUtil
from util.FightUtil import FightUtil
from util.GenericUtil import GenericUtil
from util.ItemUtil import ItemUtil
from util.MovementUtil import MovementUtil
from util.PlayerUtil import PlayerUtil
from util.SkillUtil import SkillUtil


class Fight:
    @inject
    def __init__(self, registry_service: RegistryService,
                 enum_provider: EnumProvider,
                 skill_api: SkillApi,
                 fight_api: FightApi,
                 interp_api: InterpApi = None,
                 weather_handler: WeatherHandler = None,
                 effect_handler: EffectHandler = None):
        self.__name__ = "Fight"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry_service = registry_service
        self.skill_api = skill_api
        self.room_registry = registry_service.room_registry
        self.skill_registry = registry_service.skill_registry
        self.spell_registry = getattr(registry_service, "spell_registry", None)
        self.fight_handler = fight_api.fight_handler
        self.fight_api = fight_api
        self.interp_api = interp_api or InterpApi()
        self.weather_handler = weather_handler
        self.effect_handler = effect_handler or EffectUtil.handler()
        self.spell_api = SpellApi(effect_handler=self.effect_handler)
        self._handlers = {
            "hit": self.do_kill,
            "kill": self.do_kill,
            "murder": self.do_murder,
            "cast": self.do_cast,
            "backstab": self.do_backstab,
            "bs": self.do_backstab,
            "bash": self.do_bash,
            "berserk": self.do_berserk,
            "dirt": self.do_dirt,
            "disarm": self.do_disarm,
            "flee": self.do_flee,
            "kick": self.do_kick,
            "rescue": self.do_rescue,
            "trip": self.do_trip,
        }
        self.AffectBits = enum_provider.get("affectedBy")

    def execute(self, character: Character, context: Context):
        name = (getattr(context.command, "name", "") or "").strip().lower()
        handler = self._handlers.get(name)
        if handler is not None:
            return handler(character, context)
        context.finish()
        return {"to_char": f"{name} is not implemented yet.\r\n"}

    def do_murder(self, character: Character, context: Context):
        argument = FightUtil.parse_action_argument(context.result, context.parameters)
        room = context.room if context.room is not None else self.room_registry.get(id=character.room_id)
        victim = PlayerUtil.get_target(character, argument, room) if room is not None and argument else None
        context.murder_argument = argument
        context.murder_room = room
        context.murder_victim = victim
        payload = self.interp_api.evaluate_guards_only(context, context.command.name)
        if payload is not None:
            return payload
        return self.do_kill(character, context)

    def do_kill(self, character, context):
        return self.fight_api.run_action(self, context)

    def do_cast(self, character: Character, context: Context):
        spell_name, target_arg = FightUtil.parse_cast_argument(context.result, context.parameters)
        spell = FightUtil.find_spell(self.spell_registry, spell_name) if spell_name else None
        mana_cost = FightUtil.min_mana(spell) if spell is not None else 0
        room = context.room if context.room is not None else self.room_registry.get(id=character.room_id)
        target = None
        target_kind = ""
        target_error = ""
        if spell is not None and room is not None and getattr(character, "mana", 0) >= mana_cost:
            target, target_kind, target_error = self._resolve_spell_target(character, room, spell, target_arg)

        context.cast_spell_name = spell_name
        context.cast_target_arg = target_arg
        context.cast_spell = spell
        context.cast_mana_cost = mana_cost
        context.cast_room = room
        context.cast_target = target
        context.cast_target_kind = target_kind
        context.cast_target_error = target_error
        payload = self.interp_api.evaluate_guards_only(context, context.command.name)
        if payload is not None:
            return payload

        spell_context = SpellContext(
            actor=character,
            spell=context.cast_spell,
            handler=self,
            room=context.cast_room,
            target=context.cast_target,
            target_name=target_arg,
            target_kind=context.cast_target_kind,
            source="player",
            command_context=context,
        )
        self.spell_api.execute_lambdas(spell_context)
        if spell_context.performed:
            character.mana -= mana_cost
            self.spell_api.queue_cast_announcement(spell_context)
            self.spell_api.start_offensive_combat(spell_context)
        context.finish()
        return {"payloads": spell_context.payloads}

    def do_backstab(self, character: Character, context: Context):
        return self.fight_api.run_action(self, context)

    def do_bash(self, character: Character, context: Context):
        view = self.fight_api.build_fight_view(context, skill_name="bash", current_target_fallback=True)
        payload = self.fight_api.evaluate_guards_only_view(view)
        if payload is not None:
            return payload

        skill = view.skill
        room = view.room
        victim = view.victim

        chance = self._combat_skill_chance(character, victim, skill, primary_stat="strength", defend_stat="dexterity", level_scale=2)
        self._set_wait(character, self._skill_beats(skill, 12))
        pre_corpse_ids = self._pre_corpse_ids(room)
        if random.randint(1, 100) <= chance:
            self._set_daze(victim, 24)
            CharacterApi.set_position(victim, "POS_RESTING")
            self._check_improve(character, skill, True, 1)
            result = self.fight_handler.damage(character, victim, random.randint(4, max(4, GenericUtil.to_int(getattr(character, "level", 1), 1))), dt="bash")
            round_payload = self.fight_handler.build_round_payload(character, victim, room, result, pre_corpse_ids)
            payload = {
                "payloads": [
                    self._command_payload("success", victim=victim, targets=self._room_targets(room, character, victim), token_factory=self._actor_victim_tokens),
                    round_payload,
                ]
            }
        else:
            self._check_improve(character, skill, False, 1)
            payload = self.fight_handler.build_round_payload(character, victim, room, self.fight_handler.damage(character, victim, 0, dt="bash"), pre_corpse_ids)
        context.finish()
        return payload

    def do_berserk(self, character: Character, context: Context):
        view = self.fight_api.build_fight_view(context, skill_name="berserk")
        payload = self.fight_api.evaluate_guards_only_view(view)
        if payload is not None:
            return payload

        skill = view.skill

        chance = self.skill_api.get_rating(character, skill)
        if self._position(character) == self._pos("POS_FIGHTING"):
            chance += 10
        hp = GenericUtil.to_int(getattr(character, "hit", 0), 0)
        max_hit = max(1, GenericUtil.to_int(getattr(character, "max_hit", 1), 1))
        hp_percent = (100 * hp) // max_hit
        chance += 25 - hp_percent // 2

        if random.randint(1, 100) <= max(1, min(95, chance)):
            duration = max(1, GenericUtil.to_int(getattr(character, "level", 1), 1) // 8)
            bonus = max(1, GenericUtil.to_int(getattr(character, "level", 1), 1) // 5)
            ac_penalty = max(10, 10 * max(1, GenericUtil.to_int(getattr(character, "level", 1), 1) // 5))
            self._set_wait(character, self._skill_beats(skill, 12))
            character.mana = max(0, GenericUtil.to_int(getattr(character, "mana", 0), 0) - 50)
            character.movement = max(0, GenericUtil.to_int(getattr(character, "movement", 0), 0) // 2)
            character.hit = min(GenericUtil.to_int(getattr(character, "max_hit", 0), 0), GenericUtil.to_int(getattr(character, "hit", 0), 0) + GenericUtil.to_int(getattr(character, "level", 0), 0) * 2)
            self._check_improve(character, skill, True, 2)
            self.effect_handler.affect_to_char(character, Effect(where="TO_AFFECTS", type="skill.berserk", level=getattr(character, "level", 0), duration=duration, location="APPLY_HITROLL", modifier=bonus, bitvector="AFF_BERSERK"))
            self.effect_handler.affect_to_char(character, Effect(where="TO_AFFECTS", type="skill.berserk", level=getattr(character, "level", 0), duration=duration, location="APPLY_DAMROLL", modifier=bonus, bitvector="0"))
            self.effect_handler.affect_to_char(character, Effect(where="TO_AFFECTS", type="skill.berserk", level=getattr(character, "level", 0), duration=duration, location="APPLY_AC", modifier=ac_penalty, bitvector="0"))
            room = context.room if context.room is not None else self.room_registry.get(id=character.room_id)
            context.finish()
            return {"payloads": [self._command_payload("success", targets=room.player_targets(character), token_factory=self._actor_tokens)]}

        self._set_wait(character, self._skill_beats(skill, 12) * 3)
        character.mana = max(0, GenericUtil.to_int(getattr(character, "mana", 0), 0) - 25)
        character.movement = max(0, GenericUtil.to_int(getattr(character, "movement", 0), 0) // 2)
        self._check_improve(character, skill, False, 2)
        context.finish()
        return {"payloads": [self._command_payload("failed")]}

    def do_dirt(self, character: Character, context: Context):
        view = self.fight_api.build_fight_view(context, skill_name="dirt kicking", current_target_fallback=True)
        view.extra["terrain_adjustment"] = self._dirt_terrain_adjustment(view.room) if view.room is not None else None
        payload = self.fight_api.evaluate_guards_only_view(view)
        if payload is not None:
            return payload

        skill = view.skill
        room = view.room
        victim = view.victim
        terrain_adjustment = view.extra.get("terrain_adjustment")

        chance = self._combat_skill_chance(character, victim, skill, primary_stat="dexterity", defend_stat="dexterity", level_scale=2)
        chance += terrain_adjustment
        self._set_wait(character, self._skill_beats(skill, 12))
        pre_corpse_ids = self._pre_corpse_ids(room)
        if random.randint(1, 100) <= chance:
            self.effect_handler.affect_to_char(victim, Effect(where="TO_AFFECTS", type="skill.dirt", level=getattr(character, "level", 0), duration=0, location="APPLY_HITROLL", modifier=-4, bitvector="AFF_BLIND"))
            self._check_improve(character, skill, True, 2)
            result = self.fight_handler.damage(character, victim, random.randint(2, 5), dt="dirt")
            round_payload = self.fight_handler.build_round_payload(character, victim, room, result, pre_corpse_ids)
            payload = {
                "payloads": [
                    self._command_payload("success", victim=victim, targets=self._room_targets(room, character, victim), token_factory=self._actor_victim_tokens),
                    round_payload,
                ]
            }
        else:
            self._check_improve(character, skill, False, 2)
            payload = self.fight_handler.build_round_payload(character, victim, room, self.fight_handler.damage(character, victim, 0, dt="dirt"), pre_corpse_ids)
        context.finish()
        return payload

    def do_disarm(self, character: Character, context: Context):
        view = self.fight_api.build_fight_view(context, skill_name="disarm", current_target_fallback=True)
        weapon = getattr(getattr(character, "equipped", None), "wielded", None)
        hand_to_hand = self.skill_api.get_rating(character, self.skill_registry.get(name="hand to hand"))
        view.extra["hand_to_hand"] = hand_to_hand
        payload = self.fight_api.evaluate_guards_only_view(view)
        if payload is not None:
            return payload

        skill = view.skill
        room = view.room
        victim = view.victim
        obj = getattr(getattr(victim, "equipped", None), "wielded", None)

        chance = self._combat_skill_chance(character, victim, skill, primary_stat="dexterity", defend_stat="strength", level_scale=2)
        if weapon is None and hand_to_hand > 0:
            chance = chance * hand_to_hand // 150

        self._set_wait(character, self._skill_beats(skill, 12))
        if random.randint(1, 100) <= chance:
            self._check_improve(character, skill, True, 1)
            payload = {"payloads": [self._disarm_payload(character, victim, room, obj)]}
        else:
            self._check_improve(character, skill, False, 1)
            payload = {"payloads": [self._command_payload("failed", victim=victim, targets=self._room_targets(room, character, victim), token_factory=self._actor_victim_tokens)]}
        context.finish()
        return payload

    def do_flee(self, character: Character, context: Context):
        was_in = context.room if context.room is not None else self.room_registry.get(id=character.room_id)
        exits = list(getattr(was_in, "exits", []) or [])
        to_room = None
        if was_in is not None:
            random.shuffle(exits)
            for ex in exits[:6]:
                candidate = self._flee_destination(character, was_in, ex)
                if candidate is not None:
                    to_room = candidate
                    break

        context.flee_room = was_in
        context.flee_to_room = to_room
        payload = self.interp_api.evaluate_guards_only(context, context.command.name)
        if payload is not None:
            if payload.get("blocked_key") == "not_fighting" and self._position(character) == self._pos("POS_FIGHTING"):
                CharacterApi.set_position(character, "POS_STANDING")
            return payload

        move_cost = self._movement_cost(character, was_in, to_room)
        if not CharacterApi.is_npc(character):
            character.movement = max(0, GenericUtil.to_int(getattr(character, "movement", 0), 0) - move_cost)

        from_targets = was_in.player_targets(character)
        if CharacterApi.is_npc(character):
            was_in.remove_mobile_from_room(character)
            to_room.add_mobile_to_room(character)
        else:
            was_in.remove_player_from_room(character)
            to_room.add_player_to_room(character)
        character.room_id = to_room.id
        character.area_id = getattr(to_room, "area_id", getattr(character, "area_id", ""))
        self.fight_handler.stop_fighting(character, both=True)

        exp_text = ""
        if not CharacterApi.is_npc(character):
            CharacterAdvancement.gain_experience(character, -10)
            exp_text = "lost_exp"

        context.finish()
        payloads = [
            self._command_payload("flee", channel="to_char"),
            self._command_payload("departed", channel="to_room", targets=from_targets, token_factory=self._actor_tokens),
            self._command_payload("arrived", channel="to_room", targets=to_room.player_targets(character), token_factory=self._actor_tokens),
            {"to_room_obj": to_room, "aggressive_rounds": self.fight_handler.aggressive_entry_rounds(character, to_room)},
        ]
        if exp_text:
            payloads.insert(1, self._command_payload(exp_text, channel="to_char"))
        return {"payloads": payloads}

    def do_rescue(self, character: Character, context: Context):
        view = self.fight_api.build_fight_view(context, skill_name="rescue")
        payload = self.fight_api.evaluate_guards_only_view(view)
        if payload is not None:
            return payload

        skill = view.skill
        room = view.room
        victim = view.victim
        foe = getattr(victim, "fighting", None)

        self._set_wait(character, self._skill_beats(skill, 12))
        if random.randint(1, 100) > max(1, self.skill_api.get_rating(character, skill)):
            self._check_improve(character, skill, False, 1)
            context.finish()
            return {"payloads": [self._command_payload("failed")]}

        self._check_improve(character, skill, True, 1)
        self.fight_handler.stop_fighting(foe, both=False)
        self.fight_handler.stop_fighting(victim, both=False)
        self.fight_handler.stop_fighting(character, both=False)
        self.fight_handler.set_fighting(character, foe, room.id)
        self.fight_handler.set_fighting(foe, character, room.id)
        context.finish()
        return {"payloads": [self._command_payload("success", victim=victim, targets=self._room_targets(room, character, victim), token_factory=self._actor_victim_tokens)]}

    def do_kick(self, character: Character, context: Context):
        view = self.fight_api.build_fight_view(context, skill_name="kick", current_target_fallback=True)
        payload = self.fight_api.evaluate_guards_only_view(view)
        if payload is not None:
            return payload

        skill = view.skill
        room = view.room
        victim = view.victim

        self._set_wait(character, self._skill_beats(skill, 12))
        pre_corpse_ids = self._pre_corpse_ids(room)
        if random.randint(1, 100) <= max(1, self._skill_percent(character, "kick")):
            self._check_improve(character, skill, True, 1)
            result = self.fight_handler.damage(character, victim, random.randint(1, max(1, GenericUtil.to_int(getattr(character, "level", 1), 1))), dt="kick")
        else:
            self._check_improve(character, skill, False, 1)
            result = self.fight_handler.damage(character, victim, 0, dt="kick")
        context.finish()
        return self.fight_handler.build_round_payload(character, victim, room, result, pre_corpse_ids)

    def do_trip(self, character: Character, context: Context):
        view = self.fight_api.build_fight_view(context, skill_name="trip", current_target_fallback=True)
        payload = self.fight_api.evaluate_guards_only_view(view)
        if payload is not None:
            if payload.get("blocked_key") == "target_self":
                self._set_wait(character, self._skill_beats(view.skill, 12) * 2)
                payload["payloads"] = [
                    {key: value for key, value in payload.items() if key != "payloads"},
                    self._command_payload("self_room", channel="to_room", targets=view.room.player_targets(character) if view.room is not None else [], token_factory=self._actor_tokens),
                ]
            return payload

        skill = view.skill
        room = view.room
        victim = view.victim

        chance = self._combat_skill_chance(character, victim, skill, primary_stat="dexterity", defend_stat="dexterity", level_scale=2)
        self._set_wait(character, self._skill_beats(skill, 12))
        pre_corpse_ids = self._pre_corpse_ids(room)
        if random.randint(1, 100) <= chance:
            self._set_daze(victim, 24)
            CharacterApi.set_position(victim, "POS_RESTING")
            size = max(1, GenericUtil.to_int(getattr(victim, "size", 1), 1))
            self._check_improve(character, skill, True, 1)
            result = self.fight_handler.damage(character, victim, random.randint(2, 2 + (2 * size)), dt="trip")
            round_payload = self.fight_handler.build_round_payload(character, victim, room, result, pre_corpse_ids)
            payload = {
                "payloads": [
                    self._command_payload("success", victim=victim, targets=self._room_targets(room, character, victim), token_factory=self._actor_victim_tokens),
                    round_payload,
                ]
            }
        else:
            self._check_improve(character, skill, False, 1)
            payload = self.fight_handler.build_round_payload(character, victim, room, self.fight_handler.damage(character, victim, 0, dt="trip"), pre_corpse_ids)
        context.finish()
        return payload

    def _resolve_spell_target(self, character: Character, room, spell, target_arg: str):
        from util.ItemUtil import ItemUtil
        target_type = str(getattr(spell, "target", "") or "").upper()
        argument = str(target_arg or "").strip()

        if target_type == "IGNORE":
            return None, "ignore", ""

        if target_type == "CHAR_SELF":
            if argument and argument.lower() not in {"self", str(getattr(character, "name", "")).lower()}:
                return None, "", "invalid_target"
            return character, "char", ""

        if target_type == "CHAR_DEFENSIVE":
            victim = PlayerUtil.get_target(character, argument, room) if argument else character
            return (victim, "char", "") if victim is not None else (None, "", "no_target")

        if target_type == "CHAR_OFFENSIVE":
            victim = PlayerUtil.get_target(character, argument, room) if argument else getattr(character, "fighting", None)
            if victim is None:
                return None, "", "no_target"
            safe, safe_msg = self.fight_handler.is_safe(character, victim, room=room)
            if safe and victim is not character:
                return None, "", "target_safe"
            return victim, "char", ""

        if target_type == "OBJ_INV":
            if not argument:
                return None, "", "no_inventory_target"
            obj = ItemUtil.find_inventory_item(character, argument)
            if obj is None:
                return None, "", "not_carrying"
            return obj, "obj", ""

        if target_type == "OBJ_CHAR_DEF":
            if not argument:
                return character, "char", ""
            victim = PlayerUtil.get_target(character, argument, room)
            if victim is not None:
                return victim, "char", ""
            obj = ItemUtil.find_inventory_item(character, argument)
            if obj is None:
                return None, "", "target_not_visible"
            return obj, "obj", ""

        if target_type == "OBJ_CHAR_OFF":
            if not argument:
                victim = getattr(character, "fighting", None)
                if victim is None:
                    return None, "", "missing_target"
                return victim, "char", ""
            victim = PlayerUtil.get_target(character, argument, room)
            if victim is not None:
                safe, safe_msg = self.fight_handler.is_safe(character, victim, room=room)
                if safe and victim is not character:
                    return None, "", "target_safe"
                return victim, "char", ""
            obj = ItemUtil.find_room_item(room, argument) or ItemUtil.find_inventory_item(character, argument)
            if obj is None:
                return None, "", "target_not_visible"
            return obj, "obj", ""

        return None, "", "unsupported_target"

    def _has_skill_access(self, character: Character, skill: Skill) -> bool:
        if CharacterApi.is_npc(character):
            return True
        if GenericUtil.to_int(getattr(character, "level", 0), 0) < FightUtil.level_for_class(skill, character):
            return False
        return self.skill_api.get_rating(character, skill) > 0

    @staticmethod
    def _skill_beats(skill_meta, default: int = 12) -> int:
        return max(1, GenericUtil.to_int(getattr(skill_meta, "beats", default), default))

    @staticmethod
    def _check_improve(character: Character, skill_meta, success: bool, multiplier: int) -> None:
        skill_id = str(getattr(skill_meta, "id", "") or "").strip()
        if not skill_id:
            return
        SkillUtil.check_improve(character, skill_id, success, multiplier)

    @staticmethod
    def _room_targets(room, *excluded):
        excluded_ids = {str(getattr(entity, "id", "") or "") for entity in excluded if entity is not None}
        if room is None:
            return []
        return [ch for ch in room.characters.values() if ch.id not in excluded_ids]

    @staticmethod
    def _target_name(target) -> str:
        return FightHandler._combat_target_name(target)

    @staticmethod
    def _pre_corpse_ids(room) -> set[str]:
        return {
            str(getattr(item, "id", "") or "")
            for item in getattr(room, "contents", {}).values()
            if "corpse" in str(getattr(item, "item_type", "") or "").lower()
        }

    def _resolve_optional_target(self, character: Character, room, context: Context, no_target_text: str):
        argument = FightUtil.parse_action_argument(context.result, context.parameters)
        if argument:
            victim = PlayerUtil.get_target(character, argument, room)
            if victim is None:
                return None, "They aren't here.\r\n"
            return victim, ""
        victim = getattr(character, "fighting", None)
        if victim is None:
            return None, no_target_text
        return victim, ""

    @staticmethod
    def _attribute(entity, field_name: str, default: int = 10) -> int:
        attrs = getattr(entity, "character_attributes", None)
        if attrs is not None and hasattr(attrs, field_name):
            return GenericUtil.to_int(getattr(attrs, field_name, default), default)
        perm = getattr(entity, "character_attributes", None)
        if perm is not None and hasattr(perm, field_name):
            return GenericUtil.to_int(getattr(perm, field_name, default), default)
        return GenericUtil.to_int(getattr(entity, field_name, default), default)

    @staticmethod
    def _size(entity) -> int:
        return GenericUtil.to_int(getattr(entity, "size", 2), 2)

    @staticmethod
    def _position(entity) -> int:
        return CharacterApi.position_value(entity)

    @staticmethod
    def _pos(name: str) -> int:
        return CharacterApi.pos_value(name)

    def _combat_skill_chance(self, character: Character, victim, skill: Skill, primary_stat: str, defend_stat: str, level_scale: int = 1) -> int:
        chance = self.skill_api.get_rating(character, skill)
        chance += self._attribute(character, primary_stat, 10)
        chance -= self._attribute(victim, defend_stat, 10)
        chance += (GenericUtil.to_int(getattr(character, "level", 0), 0) - GenericUtil.to_int(getattr(victim, "level", 0), 0)) * level_scale
        if CharacterApi.is_affected_by_name(character, self.AffectBits, "AFF_HASTE"):
            chance += 10
        if CharacterApi.is_affected_by_name(victim, self.AffectBits, "AFF_HASTE"):
            chance -= 20
        if CharacterApi.is_affected_by_name(character, self.AffectBits, "AFF_SLOW"):
            chance -= 10
        if CharacterApi.is_affected_by_name(victim, self.AffectBits, "AFF_SLOW"):
            chance += 10
        if self._size(character) < self._size(victim):
            chance += (self._size(character) - self._size(victim)) * 10
        return max(5, min(95, chance))

    @staticmethod
    def _entity_has_effect_type(entity, effect_type: str) -> bool:
        wanted = str(effect_type or "").strip().lower()
        for effect in list(getattr(entity, "effects", []) or []):
            if str(getattr(effect, "type", "") or "").strip().lower() == wanted:
                return True
        return False

    @staticmethod
    def _current_wait(entity) -> int:
        status_flags = getattr(entity, "status_flags", None)
        if status_flags is not None:
            return GenericUtil.to_int(getattr(status_flags, "pulse_wait", 0), 0)
        return 0

    @staticmethod
    def _current_daze(entity) -> int:
        status_flags = getattr(entity, "status_flags", None)
        if status_flags is not None:
            return GenericUtil.to_int(getattr(status_flags, "pulse_daze", 0), 0)
        return 0

    def _set_wait(self, entity, pulses: int) -> None:
        amount = max(self._current_wait(entity), GenericUtil.to_int(pulses, 0))
        status_flags = getattr(entity, "status_flags", None)
        if status_flags is not None:
            status_flags.pulse_wait = amount
            return

    def _set_daze(self, entity, pulses: int) -> None:
        amount = max(self._current_daze(entity), GenericUtil.to_int(pulses, 0))
        status_flags = getattr(entity, "status_flags", None)
        if status_flags is not None:
            status_flags.pulse_daze = amount
            return

    def _kill_steal_blocked(self, character, victim) -> bool:
        current = getattr(victim, "fighting", None)
        print(f"Checking kill steal block for {character.name} against {victim.name}, current: {current}")
        return CharacterApi.is_npc(victim) and current is not None and current is not character

    def _disarm_payload(self, character, victim, room, obj) -> dict:
        item_flags = CharacterApi.get_enum("itemFlags")
        if hasattr(item_flags, "ITEM_NOREMOVE") and ItemUtil.has_flag(getattr(obj, "extra_flags", 0), item_flags.ITEM_NOREMOVE.value):
            return self._command_payload("no_remove", victim=victim, targets=self._room_targets(room, character, victim), token_factory=self._actor_victim_tokens)

        if not CharacterApi.is_npc(victim):
            self.effect_handler.remove_item_effects(victim, obj)
        victim.unequip_item("wielded")

        keep_inventory = False
        if hasattr(item_flags, "ITEM_NODROP") and ItemUtil.has_flag(getattr(obj, "extra_flags", 0), item_flags.ITEM_NODROP.value):
            keep_inventory = True
        if hasattr(item_flags, "ITEM_INVENTORY") and ItemUtil.has_flag(getattr(obj, "extra_flags", 0), item_flags.ITEM_INVENTORY.value):
            keep_inventory = True

        if not keep_inventory:
            victim.remove_item(obj)
            room.add_item_to_room(obj)

        return self._command_payload("success", victim=victim, targets=self._room_targets(room, character, victim), token_factory=self._actor_victim_tokens)

    @staticmethod
    def _actor_tokens(*, character: Character, context: Context, payload: dict) -> dict:
        return {"actor_name": str(getattr(character, "name", "") or "")}

    @staticmethod
    def _actor_victim_tokens(*, character: Character, context: Context, payload: dict) -> dict:
        victim = payload.get("victim")
        return {
            "actor_name": str(getattr(character, "name", "") or ""),
            "victim_name": Fight._target_name(victim),
        }

    @staticmethod
    def _command_payload(message_key: str, *, victim=None, targets=None, token_factory=None, channel: str = "", tokens: dict | None = None, **extra) -> dict:
        payload = {"message_key": str(message_key or "")}
        if channel:
            payload["channel"] = channel
        if victim is not None:
            payload["victim"] = victim
        if targets is not None:
            payload["targets"] = list(targets)
        if callable(token_factory):
            payload["token_factory"] = token_factory
        if tokens:
            payload["tokens"] = dict(tokens)
        payload.update(extra)
        return payload

    def _movement_cost(self, character, in_room, to_room) -> int:
        if CharacterApi.is_npc(character):
            return 0
        move = (MovementUtil.sector_cost(getattr(in_room, "sector_type", 0)) + MovementUtil.sector_cost(getattr(to_room, "sector_type", 0))) // 2
        if CharacterApi.is_affected_by_name(character, self.AffectBits, "AFF_FLYING") or CharacterApi.is_affected_by_name(character, self.AffectBits, "AFF_HASTE"):
            move //= 2
        if CharacterApi.is_affected_by_name(character, self.AffectBits, "AFF_SLOW"):
            move *= 2
        return max(1, move)

    def _flee_destination(self, character, room, ex):
        exit_flags = CharacterApi.get_enum("exitFlags")
        room_flags = CharacterApi.get_enum("roomFlags")
        if ex is None or getattr(ex, "to_room_vnum", None) is None:
            return None
        closed = MovementUtil.get_exit_flag(exit_flags, "EX_CLOSED", "CLOSED")
        flags = GenericUtil.to_int(getattr(ex, "exit_flags", 0), 0)
        if closed and (flags & closed) != 0:
            return None
        if self._current_daze(character) > 0 and random.randint(0, self._current_daze(character)) != 0:
            return None

        to_room = self.room_registry.get_or_none(vnum=str(getattr(ex, "to_room_vnum", "")))
        if to_room is None:
            return None
        if to_room.is_private(room_flags):
            return None
        if not CharacterApi.is_npc(character):
            if (room.is_air_room(CharacterApi.get_enum("sectorTypes")) or to_room.is_air_room(CharacterApi.get_enum("sectorTypes"))) and not CharacterApi.is_affected_by_name(character, self.AffectBits, "AFF_FLYING") and not CharacterApi.is_immortal(character):
                return None
            if (room.requires_boat(CharacterApi.get_enum("sectorTypes")) or to_room.requires_boat(CharacterApi.get_enum("sectorTypes"))) and not CharacterApi.is_affected_by_name(character, self.AffectBits, "AFF_FLYING") and not character.has_boat():
                return None
            if GenericUtil.to_int(getattr(character, "movement", 0), 0) < self._movement_cost(character, room, to_room):
                return None
        return to_room

    def _dirt_terrain_adjustment(self, room) -> int | None:
        sector_types = CharacterApi.get_enum("sectorTypes")
        inside = GenericUtil.to_int(getattr(getattr(sector_types, "SECT_INSIDE", None), "value", -1), -1)
        city = GenericUtil.to_int(getattr(getattr(sector_types, "SECT_CITY", None), "value", -1), -1)
        field = GenericUtil.to_int(getattr(getattr(sector_types, "SECT_FIELD", None), "value", -1), -1)
        mountain = GenericUtil.to_int(getattr(getattr(sector_types, "SECT_MOUNTAIN", None), "value", -1), -1)
        water_swim = GenericUtil.to_int(getattr(getattr(sector_types, "SECT_WATER_SWIM", None), "value", -1), -1)
        water_noswim = GenericUtil.to_int(getattr(getattr(sector_types, "SECT_WATER_NOSWIM", None), "value", -1), -1)
        air = GenericUtil.to_int(getattr(getattr(sector_types, "SECT_AIR", None), "value", -1), -1)
        desert = GenericUtil.to_int(getattr(getattr(sector_types, "SECT_DESERT", None), "value", -1), -1)
        sector = GenericUtil.to_int(getattr(room, "sector_type", 0), 0)
        if sector in (water_swim, water_noswim, air):
            return None
        if sector == inside:
            return -20
        if sector == city:
            return -10
        if sector == field:
            return 5
        if sector == mountain:
            return -10
        if sector == desert:
            return 10
        return 0
