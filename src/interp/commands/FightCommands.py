from __future__ import annotations

from injector import inject

from area.RoomHelper import RoomHelper
from fight.FightHandler import FightHandler
from game.RegistryService import RegistryService
from interp.Context import Context
from interp.commands.FightUtil import FightUtil
from object.EffectUtil import EffectUtil
from player.Character import Character
from player.CharacterMacros import CharacterMacros
from player.PlayerUtil import PlayerUtil
from server.LoggerFactory import LoggerFactory


class FightCommands:
    @inject
    def __init__(self, registry_service: RegistryService, room_helper: RoomHelper, fight_handler: FightHandler):
        self.__name__ = "FightCommands"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry_service = registry_service
        self.room_registry = registry_service.room_registry
        self.skill_registry = registry_service.skill_registry
        self.spell_registry = getattr(registry_service, "spell_registry", None)
        self.room_helper = room_helper
        self.fight_handler = fight_handler

    def execute(self, character: Character, context: Context):
        name = (getattr(context.command, "name", "") or "").strip().lower()
        if name in ("hit", "kill"):
            return self.do_kill(character, context)
        if name == "murde":
            return self.do_murde(character, context)
        if name == "murder":
            return self.do_murder(character, context)
        if name == "cast":
            return self.do_cast(character, context)
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

        room = self.room_registry.get_or_none(id=character.room_id)
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

        room = self.room_registry.get_or_none(id=character.room_id)
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

        pre_corpse_ids = {
            str(getattr(item, "id", "") or "")
            for item in room.contents.values()
            if "corpse" in str(getattr(item, "item_type", "") or "").lower()
        }
        result = self.fight_handler.multi_hit(character, victim, dt="TYPE_UNDEFINED")
        context.finish()
        return self.fight_handler.build_round_payload(character, victim, room, result, pre_corpse_ids)

    def do_cast(self, character: Character, context: Context):
        spell_name, target_arg = FightUtil.parse_cast_argument(context.result, context.parameters)
        if not spell_name:
            context.finish()
            return {"to_char": "Cast which what where?\r\n"}

        spell = FightUtil.find_spell(self.spell_registry, spell_name)
        skill = FightUtil.find_spell_skill(self.skill_registry, character, spell_name)
        if spell is None and skill is None:
            context.finish()
            return {"to_char": "You don't know any spells of that name.\r\n"}

        meta = spell if spell is not None else skill
        mana_cost = FightUtil.min_mana(meta)
        if getattr(character, "mana", 0) < mana_cost:
            context.finish()
            return {"to_char": "You don't have enough mana.\r\n"}

        room = self.room_registry.get_or_none(id=character.room_id)
        if room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}

        target_type = str(getattr(meta, "target", "") or "").upper()
        victim = None
        if target_type in ("CHAR_OFFENSIVE", "CHAR_DEFENSIVE", "CHAR_SELF", "OBJ_CHAR_OFF", "OBJ_CHAR_DEF"):
            if target_arg:
                victim = PlayerUtil.get_target(character, target_arg, room, self.room_helper)
            elif target_type in ("CHAR_DEFENSIVE", "CHAR_SELF", "OBJ_CHAR_DEF"):
                victim = character
            else:
                victim = getattr(character, "fighting", None)
            if victim is None:
                context.finish()
                return {"to_char": "Cast the spell on whom?\r\n"}

        if spell is not None:
            EffectUtil.apply_spell_effects(character, victim, spell)

        character.mana -= mana_cost
        spell_label = getattr(meta, "name", spell_name)
        cast_text = f"You cast {spell_label}"
        if victim is not None and victim is not character:
            cast_text += f" on {victim.name}"
        cast_text += ".\r\n"

        room_text = f"{character.name} casts {spell_label}"
        if victim is not None and victim is not character:
            room_text += f" on {victim.name}"
        room_text += ".\r\n"

        payload = {
            "to_char": cast_text,
            "to_room": room_text,
            "targets": [ch for ch in room.characters.values() if ch.id != character.id],
        }
        if victim is not None and hasattr(victim, "id") and victim.id != character.id:
            payload["to_victim"] = f"{character.name} casts {spell_label} on you.\r\n"
            payload["victim"] = victim

        context.finish()
        return payload
