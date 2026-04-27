from __future__ import annotations

from injector import inject

from area.RoomHelper import RoomHelper
from fight.FightHandler import FightHandler
from game.RegistryService import RegistryService
from game.WeatherHandler import WeatherHandler
from interp.Context import Context
from interp.commands.FightUtil import FightUtil
from interp.commands.ObjectUtils import ObjectUtils
from player.Character import Character
from player.CharacterMacros import CharacterMacros
from player.PlayerUtil import PlayerUtil
from server.LoggerFactory import LoggerFactory
from skill.SpellApi import SpellApi
from skill.SpellContext import SpellContext


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
        if spell is None:
            context.finish()
            return {"to_char": "You don't know any spells of that name.\r\n"}

        mana_cost = FightUtil.min_mana(spell)
        if getattr(character, "mana", 0) < mana_cost:
            context.finish()
            return {"to_char": "You don't have enough mana.\r\n"}

        room = self.room_registry.get_or_none(id=character.room_id)
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
