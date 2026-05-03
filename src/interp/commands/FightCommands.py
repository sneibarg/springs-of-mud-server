from __future__ import annotations

import random

from injector import inject

from area.RoomHelper import RoomHelper
from fight.FightHandler import FightHandler
from game.RegistryService import RegistryService
from game.WeatherHandler import WeatherHandler
from interp.Context import Context
from object.Effect import Effect
from player.Character import Character
from player.CharacterAdvancement import CharacterAdvancement
from player.CharacterMacros import CharacterMacros
from server.LoggerFactory import LoggerFactory
from skill.SpellApi import SpellApi
from skill.SpellContext import SpellContext
from util.EffectUtil import EffectUtil
from util.FightUtil import FightUtil
from util.GenericUtil import GenericUtil
from util.MovementUtil import MovementUtil
from util.ObjectUtil import ObjectUtils
from util.PlayerUtil import PlayerUtil


class FightCommands:
    @inject
    def __init__(self, registry_service: RegistryService, room_helper: RoomHelper, fight_handler: FightHandler, weather_handler: WeatherHandler = None):
        self.__name__ = "FightCommands"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry_service = registry_service
        self.room_registry = registry_service.room_registry
        self.skill_registry = registry_service.skill_registry
        self.spell_registry = getattr(registry_service, "spell_registry", None)
        self.room_helper = room_helper
        self.fight_handler = fight_handler
        self.weather_handler = weather_handler
        self.spell_api = SpellApi()
        self._handlers = {
            "hit": self.do_kill,
            "kill": self.do_kill,
            "murde": self.do_murde,
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

    def execute(self, character: Character, context: Context):
        name = (getattr(context.command, "name", "") or "").strip().lower()
        handler = self._handlers.get(name)
        if handler is not None:
            return handler(character, context)
        context.finish()
        return {"to_char": f"{name} is not implemented yet.\r\n"}

    def do_murde(self, character: Character, context: Context):
        context.finish()
        return {"to_char": "If you want to MURDER, spell it out.\r\n"}

    def do_murder(self, character: Character, context: Context):
        argument = FightUtil.parse_action_argument(context.result, context.parameters)
        if not argument:
            context.finish()
            return {"to_char": "Murder whom?\r\n"}

        if CharacterMacros.is_npc(character):
            return self.do_kill(character, context)

        room = self._room_for(character)
        if room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}
        victim = PlayerUtil.get_target(character, argument, room, self.room_helper)
        if victim is character:
            context.finish()
            return {"to_char": "Suicide is a mortal sin.\r\n"}
        return self.do_kill(character, context)

    def do_kill(self, character: Character, context: Context):
        argument = FightUtil.parse_action_argument(context.result, context.parameters)
        if not argument:
            context.finish()
            return {"to_char": "Kill whom?\r\n"}

        room = self._room_for(character)
        if room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}

        victim = PlayerUtil.get_target(character, argument, room, self.room_helper)
        if victim is None:
            context.finish()
            return {"to_char": "They aren't here.\r\n"}
        if victim is character:
            context.finish()
            return {"to_char": "You hit yourself. Ouch!\r\n"}

        safe, safe_msg = self.fight_handler.is_safe(character, victim, room=room)
        if safe:
            context.finish()
            return {"to_char": safe_msg or "You cannot attack them.\r\n"}

        current_fighting = getattr(character, "fighting", None)
        if current_fighting is victim:
            victim_name = self.fight_handler._combat_target_name(victim)
            context.finish()
            return {"to_char": f"You are already fighting {victim_name}.\r\n"}
        if current_fighting is not None and current_fighting is not victim:
            context.finish()
            return {"to_char": "You do the best you can!\r\n"}

        if getattr(character, "fighting", None) is None:
            self.fight_handler.set_fighting(character, victim, room.id)
        if getattr(victim, "fighting", None) is None:
            self.fight_handler.set_fighting(victim, character, room.id)

        pre_corpse_ids = self._pre_corpse_ids(room)
        result = self.fight_handler.multi_hit(character, victim, dt="TYPE_UNDEFINED")
        context.finish()
        return self.fight_handler.build_round_payload(character, victim, room, result, pre_corpse_ids)

    def do_cast(self, character: Character, context: Context):
        spell_name, target_arg = FightUtil.parse_cast_argument(context.result, context.parameters)
        if not spell_name:
            context.finish()
            return {"to_char": "Cast which what where?\r\n"}

        spell = FightUtil.find_spell(self.spell_registry, spell_name)
        if spell is None:
            context.finish()
            return {"to_char": "You don't know any spells of that name.\r\n"}

        mana_cost = FightUtil.min_mana(spell)
        if getattr(character, "mana", 0) < mana_cost:
            context.finish()
            return {"to_char": "You don't have enough mana.\r\n"}

        room = self._room_for(character)
        if room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}

        target, target_kind, error = self._resolve_spell_target(character, room, spell, target_arg)
        if error:
            context.finish()
            return {"to_char": error}

        spell_context = SpellContext(
            actor=character,
            spell=spell,
            handler=self,
            room=room,
            target=target,
            target_name=target_arg,
            target_kind=target_kind,
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
        skill = self._skill_meta("backstab")
        if not self._has_skill_access(character, "backstab", skill):
            context.finish()
            return {"to_char": "You better leave the assassin trade to thieves.\r\n"}

        argument = FightUtil.parse_action_argument(context.result, context.parameters)
        if not argument:
            context.finish()
            return {"to_char": "Backstab whom?\r\n"}
        if getattr(character, "fighting", None) is not None:
            context.finish()
            return {"to_char": "You're facing the wrong end.\r\n"}

        room = self._room_for(character)
        if room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}

        victim = PlayerUtil.get_target(character, argument, room, self.room_helper)
        if victim is None:
            context.finish()
            return {"to_char": "They aren't here.\r\n"}
        if victim is character:
            context.finish()
            return {"to_char": "How can you sneak up on yourself?\r\n"}

        safe, safe_msg = self.fight_handler.is_safe(character, victim, room=room)
        if safe:
            context.finish()
            return {"to_char": safe_msg or "You cannot attack them.\r\n"}
        if self._kill_steal_blocked(character, victim):
            context.finish()
            return {"to_char": "Kill stealing is not permitted.\r\n"}

        weapon = getattr(getattr(character, "equipped", None), "wielded", None)
        if weapon is None or str(getattr(weapon, "item_type", "") or "").strip().lower() != "weapon":
            context.finish()
            return {"to_char": "You need to wield a weapon to backstab.\r\n"}
        if GenericUtil.to_int(getattr(victim, "hit", 0), 0) < max(1, GenericUtil.to_int(getattr(victim, "max_hit", 0), 0) // 3):
            context.finish()
            return {"to_char": "They are hurt and suspicious. You can't sneak up.\r\n"}

        self._set_wait(character, self._skill_beats(skill, 12))
        pre_corpse_ids = self._pre_corpse_ids(room)
        skill_percent = self._skill_percent(character, "backstab")
        success = random.randint(1, 100) <= max(1, skill_percent)
        if not CharacterMacros.is_awake(victim) and skill_percent >= 2:
            success = True

        if success:
            result = self.fight_handler.multi_hit(character, victim, dt="backstab")
        else:
            result = self.fight_handler.damage(character, victim, 0, dt="backstab")

        context.finish()
        return self.fight_handler.build_round_payload(character, victim, room, result, pre_corpse_ids)

    def do_bash(self, character: Character, context: Context):
        skill = self._skill_meta("bash")
        if not self._has_skill_access(character, "bash", skill):
            context.finish()
            return {"to_char": "Bashing? What's that?\r\n"}

        room = self._room_for(character)
        if room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}

        victim, error = self._resolve_optional_target(character, room, context, "But you aren't fighting anyone!\r\n")
        if error:
            context.finish()
            return {"to_char": error}
        if self._position(victim) < self._pos("POS_FIGHTING"):
            context.finish()
            return {"to_char": "You'll have to let them get back up first.\r\n"}
        if victim is character:
            context.finish()
            return {"to_char": "You try to bash your brains out, but fail.\r\n"}

        safe, safe_msg = self.fight_handler.is_safe(character, victim, room=room)
        if safe:
            context.finish()
            return {"to_char": safe_msg or "You cannot attack them.\r\n"}
        if self._kill_steal_blocked(character, victim):
            context.finish()
            return {"to_char": "Kill stealing is not permitted.\r\n"}

        chance = self._combat_skill_chance(character, victim, "bash", primary_stat="strength", defend_stat="dexterity", level_scale=2)
        self._set_wait(character, self._skill_beats(skill, 12))
        pre_corpse_ids = self._pre_corpse_ids(room)
        if random.randint(1, 100) <= chance:
            self._set_daze(victim, 24)
            CharacterMacros.set_position(victim, "POS_RESTING")
            result = self.fight_handler.damage(character, victim, random.randint(4, max(4, GenericUtil.to_int(getattr(character, "level", 1), 1))), dt="bash")
            payload = self.fight_handler.build_round_payload(character, victim, room, result, pre_corpse_ids)
            self._prepend_payload(
                payload,
                "You slam into them and send them flying!\r\n",
                f"{self._target_name(character)} sends you sprawling with a powerful bash!\r\n",
                f"{self._target_name(character)} sends {self._target_name(victim)} sprawling with a powerful bash.\r\n",
            )
        else:
            result = self.fight_handler.damage(character, victim, 0, dt="bash")
            payload = self.fight_handler.build_round_payload(character, victim, room, result, pre_corpse_ids)
        context.finish()
        return payload

    def do_berserk(self, character: Character, context: Context):
        skill = self._skill_meta("berserk")
        if not self._has_skill_access(character, "berserk", skill):
            context.finish()
            return {"to_char": "You turn red in the face, but nothing happens.\r\n"}
        if self._entity_has_effect_type(character, "skill.berserk") or self._affected(character, "AFF_BERSERK") or self._entity_has_effect_type(character, "spell.frenzy"):
            context.finish()
            return {"to_char": "You get a little madder.\r\n"}
        if self._affected(character, "AFF_CALM"):
            context.finish()
            return {"to_char": "You're feeling too mellow to berserk.\r\n"}
        if GenericUtil.to_int(getattr(character, "mana", 0), 0) < 50:
            context.finish()
            return {"to_char": "You can't get up enough energy.\r\n"}

        chance = self._skill_percent(character, "berserk")
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
            EffectUtil.affect_to_char(character, Effect(where="TO_AFFECTS", type="skill.berserk", level=getattr(character, "level", 0), duration=duration, location="APPLY_HITROLL", modifier=bonus, bitvector="AFF_BERSERK"))
            EffectUtil.affect_to_char(character, Effect(where="TO_AFFECTS", type="skill.berserk", level=getattr(character, "level", 0), duration=duration, location="APPLY_DAMROLL", modifier=bonus, bitvector="0"))
            EffectUtil.affect_to_char(character, Effect(where="TO_AFFECTS", type="skill.berserk", level=getattr(character, "level", 0), duration=duration, location="APPLY_AC", modifier=ac_penalty, bitvector="0"))
            room = self._room_for(character)
            context.finish()
            return {
                "to_char": "Your pulse races as you are consumed by rage!\r\n",
                "to_room": f"{character.name} gets a wild look in their eyes.\r\n",
                "targets": room.player_targets(character),
            }

        self._set_wait(character, self._skill_beats(skill, 12) * 3)
        character.mana = max(0, GenericUtil.to_int(getattr(character, "mana", 0), 0) - 25)
        character.movement = max(0, GenericUtil.to_int(getattr(character, "movement", 0), 0) // 2)
        context.finish()
        return {"to_char": "Your pulse speeds up, but nothing happens.\r\n"}

    def do_dirt(self, character: Character, context: Context):
        skill = self._skill_meta("dirt")
        if not self._has_skill_access(character, "dirt", skill):
            context.finish()
            return {"to_char": "You get your feet dirty.\r\n"}

        room = self._room_for(character)
        if room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}

        victim, error = self._resolve_optional_target(character, room, context, "But you aren't in combat!\r\n")
        if error:
            context.finish()
            return {"to_char": error}
        if self._affected(victim, "AFF_BLIND"):
            context.finish()
            return {"to_char": "They have already been blinded.\r\n"}
        if victim is character:
            context.finish()
            return {"to_char": "Very funny.\r\n"}

        safe, safe_msg = self.fight_handler.is_safe(character, victim, room=room)
        if safe:
            context.finish()
            return {"to_char": safe_msg or "You cannot attack them.\r\n"}
        if self._kill_steal_blocked(character, victim):
            context.finish()
            return {"to_char": "Kill stealing is not permitted.\r\n"}

        terrain_adjustment = self._dirt_terrain_adjustment(room)
        if terrain_adjustment is None:
            context.finish()
            return {"to_char": "There isn't any dirt to kick.\r\n"}

        chance = self._combat_skill_chance(character, victim, "dirt", primary_stat="dexterity", defend_stat="dexterity", level_scale=2)
        chance += terrain_adjustment
        self._set_wait(character, self._skill_beats(skill, 12))
        pre_corpse_ids = self._pre_corpse_ids(room)
        if random.randint(1, 100) <= chance:
            EffectUtil.affect_to_char(victim, Effect(where="TO_AFFECTS", type="skill.dirt", level=getattr(character, "level", 0), duration=0, location="APPLY_HITROLL", modifier=-4, bitvector="AFF_BLIND"))
            result = self.fight_handler.damage(character, victim, random.randint(2, 5), dt="dirt")
            payload = self.fight_handler.build_round_payload(character, victim, room, result, pre_corpse_ids)
            self._prepend_payload(
                payload,
                "You kick dirt in their eyes!\r\n",
                f"{self._target_name(character)} kicks dirt in your eyes!\r\nYou can't see a thing!\r\n",
                f"{self._target_name(victim)} is blinded by dirt in their eyes!\r\n",
            )
        else:
            result = self.fight_handler.damage(character, victim, 0, dt="dirt")
            payload = self.fight_handler.build_round_payload(character, victim, room, result, pre_corpse_ids)
        context.finish()
        return payload

    def do_disarm(self, character: Character, context: Context):
        skill = self._skill_meta("disarm")
        if not self._has_skill_access(character, "disarm", skill):
            context.finish()
            return {"to_char": "You don't know how to disarm opponents.\r\n"}

        weapon = getattr(getattr(character, "equipped", None), "wielded", None)
        hand_to_hand = self._skill_percent(character, "hand to hand")
        if weapon is None and hand_to_hand <= 0:
            context.finish()
            return {"to_char": "You must wield a weapon to disarm.\r\n"}

        room = self._room_for(character)
        if room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}
        victim = getattr(character, "fighting", None)
        if victim is None:
            context.finish()
            return {"to_char": "You aren't fighting anyone.\r\n"}
        obj = getattr(getattr(victim, "equipped", None), "wielded", None)
        if obj is None:
            context.finish()
            return {"to_char": "Your opponent is not wielding a weapon.\r\n"}

        chance = self._combat_skill_chance(character, victim, "disarm", primary_stat="dexterity", defend_stat="strength", level_scale=2)
        if weapon is None and hand_to_hand > 0:
            chance = chance * hand_to_hand // 150

        self._set_wait(character, self._skill_beats(skill, 12))
        if random.randint(1, 100) <= chance:
            payload = self._disarm_payload(character, victim, room, obj)
        else:
            payload = {
                "to_char": f"You fail to disarm {self._target_name(victim)}.\r\n",
                "to_victim": f"{self._target_name(character)} tries to disarm you, but fails.\r\n",
                "to_room": f"{self._target_name(character)} tries to disarm {self._target_name(victim)}, but fails.\r\n",
                "victim": victim,
                "targets": self._room_targets(room, character, victim),
            }
        context.finish()
        return payload

    def do_flee(self, character: Character, context: Context):
        victim = getattr(character, "fighting", None)
        if victim is None:
            if self._position(character) == self._pos("POS_FIGHTING"):
                CharacterMacros.set_position(character, "POS_STANDING")
            context.finish()
            return {"to_char": "You aren't fighting anyone.\r\n"}

        was_in = self._room_for(character)
        if was_in is None:
            context.finish()
            return {"to_char": "PANIC! You couldn't escape!\r\n"}

        exits = list(getattr(was_in, "exits", []) or [])
        random.shuffle(exits)
        to_room = None
        for ex in exits[:6]:
            candidate = self._flee_destination(character, was_in, ex)
            if candidate is not None:
                to_room = candidate
                break

        if to_room is None:
            context.finish()
            return {"to_char": "PANIC! You couldn't escape!\r\n"}

        move_cost = self._movement_cost(character, was_in, to_room)
        if not CharacterMacros.is_npc(character):
            character.movement = max(0, GenericUtil.to_int(getattr(character, "movement", 0), 0) - move_cost)

        from_targets = was_in.player_targets(character)
        if CharacterMacros.is_npc(character):
            was_in.remove_mobile_from_room(character)
            to_room.add_mobile_to_room(character)
        else:
            was_in.remove_player_from_room(character)
            to_room.add_player_to_room(character)
        character.room_id = to_room.id
        character.area_id = getattr(to_room, "area_id", getattr(character, "area_id", ""))
        self.fight_handler.stop_fighting(character, both=True)

        exp_text = ""
        if not CharacterMacros.is_npc(character):
            CharacterAdvancement.gain_experience(character, -10)
            exp_text = "You lost 10 exp.\r\n"

        context.finish()
        return {
            "to_char": f"You flee from combat!\r\n{exp_text}",
            "from_room_message": f"{character.name} has fled!\r\n",
            "from_room_targets": from_targets,
            "to_room_targets": to_room.player_targets(character),
            "to_room_message": f"{character.name} has arrived.\r\n",
            "to_room_obj": to_room,
            "aggressive_rounds": self.fight_handler.aggressive_entry_rounds(character, to_room),
        }

    def do_rescue(self, character: Character, context: Context):
        skill = self._skill_meta("rescue")
        if not self._has_skill_access(character, "rescue", skill):
            context.finish()
            return {"to_char": "You don't know how to rescue others.\r\n"}

        argument = FightUtil.parse_action_argument(context.result, context.parameters)
        if not argument:
            context.finish()
            return {"to_char": "Rescue whom?\r\n"}

        room = self._room_for(character)
        if room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}

        victim = PlayerUtil.get_target(character, argument, room, self.room_helper)
        if victim is None:
            context.finish()
            return {"to_char": "They aren't here.\r\n"}
        if victim is character:
            context.finish()
            return {"to_char": "What about fleeing instead?\r\n"}
        if not CharacterMacros.is_npc(character) and CharacterMacros.is_npc(victim):
            context.finish()
            return {"to_char": "Doesn't need your help!\r\n"}
        if getattr(character, "fighting", None) is victim:
            context.finish()
            return {"to_char": "Too late.\r\n"}

        foe = getattr(victim, "fighting", None)
        if foe is None:
            context.finish()
            return {"to_char": "That person is not fighting right now.\r\n"}

        self._set_wait(character, self._skill_beats(skill, 12))
        if random.randint(1, 100) > max(1, self._skill_percent(character, "rescue")):
            context.finish()
            return {"to_char": "You fail the rescue.\r\n"}

        self.fight_handler.stop_fighting(foe, both=False)
        self.fight_handler.stop_fighting(victim, both=False)
        self.fight_handler.stop_fighting(character, both=False)
        self.fight_handler.set_fighting(character, foe, room.id)
        self.fight_handler.set_fighting(foe, character, room.id)
        context.finish()
        return {
            "to_char": f"You rescue {self._target_name(victim)}!\r\n",
            "to_victim": f"{self._target_name(character)} rescues you!\r\n",
            "to_room": f"{self._target_name(character)} rescues {self._target_name(victim)}!\r\n",
            "victim": victim,
            "targets": self._room_targets(room, character, victim),
        }

    def do_kick(self, character: Character, context: Context):
        skill = self._skill_meta("kick")
        if not self._has_skill_access(character, "kick", skill):
            context.finish()
            return {"to_char": "You better leave the martial arts to fighters.\r\n"}

        room = self._room_for(character)
        victim = getattr(character, "fighting", None)
        if room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}
        if victim is None:
            context.finish()
            return {"to_char": "You aren't fighting anyone.\r\n"}

        self._set_wait(character, self._skill_beats(skill, 12))
        pre_corpse_ids = self._pre_corpse_ids(room)
        if random.randint(1, 100) <= max(1, self._skill_percent(character, "kick")):
            result = self.fight_handler.damage(character, victim, random.randint(1, max(1, GenericUtil.to_int(getattr(character, "level", 1), 1))), dt="kick")
        else:
            result = self.fight_handler.damage(character, victim, 0, dt="kick")
        context.finish()
        return self.fight_handler.build_round_payload(character, victim, room, result, pre_corpse_ids)

    def do_trip(self, character: Character, context: Context):
        skill = self._skill_meta("trip")
        if not self._has_skill_access(character, "trip", skill):
            context.finish()
            return {"to_char": "Tripping? What's that?\r\n"}

        room = self._room_for(character)
        if room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}

        victim, error = self._resolve_optional_target(character, room, context, "But you aren't fighting anyone!\r\n")
        if error:
            context.finish()
            return {"to_char": error}

        safe, safe_msg = self.fight_handler.is_safe(character, victim, room=room)
        if safe:
            context.finish()
            return {"to_char": safe_msg or "You cannot attack them.\r\n"}
        if self._kill_steal_blocked(character, victim):
            context.finish()
            return {"to_char": "Kill stealing is not permitted.\r\n"}
        if self._affected(victim, "AFF_FLYING"):
            context.finish()
            return {"to_char": "Their feet aren't on the ground.\r\n"}
        if self._position(victim) < self._pos("POS_FIGHTING"):
            context.finish()
            return {"to_char": "They are already down.\r\n"}
        if victim is character:
            self._set_wait(character, self._skill_beats(skill, 12) * 2)
            context.finish()
            return {"to_char": "You fall flat on your face!\r\n", "to_room": f"{character.name} trips over their own feet!\r\n", "targets": room.player_targets(character)}

        chance = self._combat_skill_chance(character, victim, "trip", primary_stat="dexterity", defend_stat="dexterity", level_scale=2)
        self._set_wait(character, self._skill_beats(skill, 12))
        pre_corpse_ids = self._pre_corpse_ids(room)
        if random.randint(1, 100) <= chance:
            self._set_daze(victim, 24)
            CharacterMacros.set_position(victim, "POS_RESTING")
            size = max(1, GenericUtil.to_int(getattr(victim, "size", 1), 1))
            result = self.fight_handler.damage(character, victim, random.randint(2, 2 + (2 * size)), dt="trip")
            payload = self.fight_handler.build_round_payload(character, victim, room, result, pre_corpse_ids)
            self._prepend_payload(
                payload,
                f"You trip {self._target_name(victim)} and they go down!\r\n",
                f"{self._target_name(character)} trips you and you go down!\r\n",
                f"{self._target_name(character)} trips {self._target_name(victim)}, sending them to the ground.\r\n",
            )
        else:
            result = self.fight_handler.damage(character, victim, 0, dt="trip")
            payload = self.fight_handler.build_round_payload(character, victim, room, result, pre_corpse_ids)
        context.finish()
        return payload

    def _resolve_spell_target(self, character: Character, room, spell, target_arg: str):
        target_type = str(getattr(spell, "target", "") or "").upper()
        argument = str(target_arg or "").strip()

        if target_type == "IGNORE":
            return None, "ignore", ""

        if target_type == "CHAR_SELF":
            if argument and argument.lower() not in {"self", str(getattr(character, "name", "")).lower()}:
                return None, "", "You cannot cast this spell on another.\r\n"
            return character, "char", ""

        if target_type == "CHAR_DEFENSIVE":
            victim = PlayerUtil.get_target(character, argument, room, self.room_helper) if argument else character
            return (victim, "char", "") if victim is not None else (None, "", "Cast the spell on whom?\r\n")

        if target_type == "CHAR_OFFENSIVE":
            victim = PlayerUtil.get_target(character, argument, room, self.room_helper) if argument else getattr(character, "fighting", None)
            if victim is None:
                return None, "", "Cast the spell on whom?\r\n"
            safe, safe_msg = self.fight_handler.is_safe(character, victim, room=room)
            if safe and victim is not character:
                return None, "", safe_msg or "Not on that target.\r\n"
            return victim, "char", ""

        if target_type == "OBJ_INV":
            if not argument:
                return None, "", "What should the spell be cast upon?\r\n"
            obj = ObjectUtils.find_inventory_item(character, argument)
            if obj is None:
                return None, "", "You are not carrying that.\r\n"
            return obj, "obj", ""

        if target_type == "OBJ_CHAR_DEF":
            if not argument:
                return character, "char", ""
            victim = PlayerUtil.get_target(character, argument, room, self.room_helper)
            if victim is not None:
                return victim, "char", ""
            obj = ObjectUtils.find_inventory_item(character, argument)
            if obj is None:
                return None, "", "You don't see that here.\r\n"
            return obj, "obj", ""

        if target_type == "OBJ_CHAR_OFF":
            if not argument:
                victim = getattr(character, "fighting", None)
                if victim is None:
                    return None, "", "Cast the spell on whom or what?\r\n"
                return victim, "char", ""
            victim = PlayerUtil.get_target(character, argument, room, self.room_helper)
            if victim is not None:
                safe, safe_msg = self.fight_handler.is_safe(character, victim, room=room)
                if safe and victim is not character:
                    return None, "", safe_msg or "Not on that target.\r\n"
                return victim, "char", ""
            obj = ObjectUtils.find_room_item(room, argument) or ObjectUtils.find_inventory_item(character, argument)
            if obj is None:
                return None, "", "You don't see that here.\r\n"
            return obj, "obj", ""

        return None, "", "You can't cast that right now.\r\n"

    def _room_for(self, character):
        return self.room_registry.get_or_none(id=getattr(character, "room_id", ""))

    @staticmethod
    def _skill_entry_name(entry) -> str:
        if isinstance(entry, dict):
            return str(entry.get("name", "") or "").strip().lower()
        return str(getattr(entry, "name", "") or "").strip().lower()

    @staticmethod
    def _skill_entry_percent(entry) -> int:
        if isinstance(entry, dict):
            for key in ("level", "learned", "percent", "value"):
                if key in entry:
                    return max(0, min(100, GenericUtil.to_int(entry.get(key, 0), 0)))
            return 0
        for key in ("level", "learned", "percent", "value"):
            if hasattr(entry, key):
                return max(0, min(100, GenericUtil.to_int(getattr(entry, key, 0), 0)))
        return 0

    def _skill_meta(self, skill_name: str):
        registry = getattr(self.skill_registry, "all_skills", None)
        if not callable(registry):
            return None
        wanted = str(skill_name or "").strip().lower()
        for skill in registry():
            if str(getattr(skill, "name", "") or "").strip().lower() == wanted:
                return skill
        return None

    def _skill_percent(self, character: Character, skill_name: str) -> int:
        wanted = str(skill_name or "").strip().lower()
        for entry in list(getattr(character, "skills", []) or []):
            if self._skill_entry_name(entry) == wanted:
                return self._skill_entry_percent(entry)
        return 0

    def _has_skill_access(self, character: Character, skill_name: str, skill_meta=None) -> bool:
        if CharacterMacros.is_npc(character):
            return True
        skill_meta = skill_meta or self._skill_meta(skill_name)
        if skill_meta is None:
            return False
        if GenericUtil.to_int(getattr(character, "level", 0), 0) < FightUtil.level_for_class(skill_meta, character):
            return False
        return self._skill_percent(character, skill_name) > 0

    @staticmethod
    def _skill_beats(skill_meta, default: int = 12) -> int:
        return max(1, GenericUtil.to_int(getattr(skill_meta, "beats", default), default))

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
    def _prepend_payload(payload: dict, to_char: str = "", to_victim: str = "", to_room: str = "") -> dict:
        payload["to_char"] = str(to_char or "") + str(payload.get("to_char", "") or "")
        if "victim" in payload:
            payload["to_victim"] = str(to_victim or "") + str(payload.get("to_victim", "") or "")
        payload["to_room"] = str(to_room or "") + str(payload.get("to_room", "") or "")
        return payload

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
            victim = PlayerUtil.get_target(character, argument, room, self.room_helper)
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
        perm = getattr(entity, "perm_stat", None)
        if perm is not None and hasattr(perm, field_name):
            return GenericUtil.to_int(getattr(perm, field_name, default), default)
        return GenericUtil.to_int(getattr(entity, field_name, default), default)

    @staticmethod
    def _size(entity) -> int:
        return GenericUtil.to_int(getattr(entity, "size", 2), 2)

    @staticmethod
    def _position(entity) -> int:
        return CharacterMacros.position_value(entity)

    @staticmethod
    def _pos(name: str) -> int:
        return CharacterMacros.pos_value(name)

    def _combat_skill_chance(self, character: Character, victim, skill_name: str, primary_stat: str, defend_stat: str, level_scale: int = 1) -> int:
        chance = self._skill_percent(character, skill_name)
        chance += self._attribute(character, primary_stat, 10)
        chance -= self._attribute(victim, defend_stat, 10)
        chance += (GenericUtil.to_int(getattr(character, "level", 0), 0) - GenericUtil.to_int(getattr(victim, "level", 0), 0)) * level_scale
        if self._affected(character, "AFF_HASTE"):
            chance += 10
        if self._affected(victim, "AFF_HASTE"):
            chance -= 20
        if self._affected(character, "AFF_SLOW"):
            chance -= 10
        if self._affected(victim, "AFF_SLOW"):
            chance += 10
        if self._size(character) < self._size(victim):
            chance += (self._size(character) - self._size(victim)) * 10
        return max(5, min(95, chance))

    def _affected(self, entity, affect_name: str) -> bool:
        return self.fight_handler._entity_has_affect(entity, affect_name)

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
        return CharacterMacros.is_npc(victim) and current is not None and current is not character

    def _disarm_payload(self, character, victim, room, obj) -> dict:
        item_flags = CharacterMacros.get_enum("itemFlags")
        if hasattr(item_flags, "ITEM_NOREMOVE") and ObjectUtils.has_flag(getattr(obj, "extra_flags", 0), item_flags.ITEM_NOREMOVE.value):
            return {
                "to_char": "Their weapon won't budge!\r\n",
                "to_victim": f"{self._target_name(character)} tries to disarm you, but your weapon won't budge!\r\n",
                "to_room": f"{self._target_name(character)} tries to disarm {self._target_name(victim)}, but fails.\r\n",
                "victim": victim,
                "targets": self._room_targets(room, character, victim),
            }

        if not CharacterMacros.is_npc(victim):
            EffectUtil.remove_item_effects(victim, obj)
        victim.unequip_item("wielded")

        keep_inventory = False
        if hasattr(item_flags, "ITEM_NODROP") and ObjectUtils.has_flag(getattr(obj, "extra_flags", 0), item_flags.ITEM_NODROP.value):
            keep_inventory = True
        if hasattr(item_flags, "ITEM_INVENTORY") and ObjectUtils.has_flag(getattr(obj, "extra_flags", 0), item_flags.ITEM_INVENTORY.value):
            keep_inventory = True

        if not keep_inventory:
            victim.remove_item(obj)
            room.add_item_to_room(obj)

        return {
            "to_char": f"You disarm {self._target_name(victim)}!\r\n",
            "to_victim": f"{self._target_name(character)} disarms you and sends your weapon flying!\r\n",
            "to_room": f"{self._target_name(character)} disarms {self._target_name(victim)}!\r\n",
            "victim": victim,
            "targets": self._room_targets(room, character, victim),
        }

    def _movement_cost(self, character, in_room, to_room) -> int:
        if CharacterMacros.is_npc(character):
            return 0
        move = (MovementUtil.sector_cost(getattr(in_room, "sector_type", 0)) + MovementUtil.sector_cost(getattr(to_room, "sector_type", 0))) // 2
        if self._affected(character, "AFF_FLYING") or self._affected(character, "AFF_HASTE"):
            move //= 2
        if self._affected(character, "AFF_SLOW"):
            move *= 2
        return max(1, move)

    def _flee_destination(self, character, room, ex):
        exit_flags = CharacterMacros.get_enum("exitFlags")
        room_flags = CharacterMacros.get_enum("roomFlags")
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
        if to_room.is_room_private(room_flags):
            return None
        if not CharacterMacros.is_npc(character):
            if (room.is_air_room(CharacterMacros.get_enum("sectorTypes")) or to_room.is_air_room(CharacterMacros.get_enum("sectorTypes"))) and not self._affected(character, "AFF_FLYING") and not CharacterMacros.is_immortal(character):
                return None
            if (room.requires_boat(CharacterMacros.get_enum("sectorTypes")) or to_room.requires_boat(CharacterMacros.get_enum("sectorTypes"))) and not self._affected(character, "AFF_FLYING") and not character.has_boat():
                return None
            if GenericUtil.to_int(getattr(character, "movement", 0), 0) < self._movement_cost(character, room, to_room):
                return None
        return to_room

    def _dirt_terrain_adjustment(self, room) -> int | None:
        sector_types = CharacterMacros.get_enum("sectorTypes")
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
