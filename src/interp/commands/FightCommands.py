from __future__ import annotations

from injector import inject

from area.RoomHelper import RoomHelper
from game.RegistryService import RegistryService
from interp.Context import Context
from interp.commands.FightUtil import FightUtil
from player.Character import Character
from player.CharacterMacros import CharacterMacros
from player.PlayerUtil import PlayerUtil
from server.LoggerFactory import LoggerFactory


class FightCommands:
    @inject
    def __init__(self, registry_service: RegistryService, character_macros: CharacterMacros, room_helper: RoomHelper):
        self.__name__ = "FightCommands"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry_service = registry_service
        self.room_registry = registry_service.room_registry
        self.skill_registry = registry_service.skill_registry
        self.character_macros = character_macros
        self.room_helper = room_helper

    def execute(self, character: Character, context: Context):
        name = (getattr(context.command, "name", "") or "").strip().lower()
        if name == "cast":
            return self.do_cast(character, context)
        context.finish()
        return {"to_char": f"{name} is not implemented yet.\r\n"}

    def do_cast(self, character: Character, context: Context):
        spell_name, target_arg = FightUtil.parse_cast_argument(context.result, context.parameters)
        if not spell_name:
            context.finish()
            return {"to_char": "Cast which what where?\r\n"}

        skill = self._find_spell_skill(character, spell_name)
        if skill is None:
            context.finish()
            return {"to_char": "You don't know any spells of that name.\r\n"}

        mana_cost = FightUtil.min_mana(skill)
        if getattr(character, "mana", 0) < mana_cost:
            context.finish()
            return {"to_char": "You don't have enough mana.\r\n"}

        room = self.room_registry.get_or_none(id=character.room_id)
        if room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}

        target_type = str(getattr(skill, "target", "") or "").upper()
        victim = None
        if target_type in ("CHAR_OFFENSIVE", "CHAR_DEFENSIVE", "CHAR_SELF", "OBJ_CHAR_OFF", "OBJ_CHAR_DEF"):
            if target_arg:
                victim = PlayerUtil.get_target(character, target_arg, room, self.character_macros, self.room_helper)
            elif target_type in ("CHAR_DEFENSIVE", "CHAR_SELF", "OBJ_CHAR_DEF"):
                victim = character
            else:
                victim = getattr(character, "fighting", None)
            if victim is None:
                context.finish()
                return {"to_char": "Cast the spell on whom?\r\n"}

        character.mana -= mana_cost
        cast_text = f"You cast {skill.name}"
        if victim is not None and victim is not character:
            cast_text += f" on {victim.name}"
        cast_text += ".\r\n"

        room_text = f"{character.name} casts {skill.name}"
        if victim is not None and victim is not character:
            room_text += f" on {victim.name}"
        room_text += ".\r\n"

        payload = {
            "to_char": cast_text,
            "to_room": room_text,
            "targets": [ch for ch in room.characters.values() if ch.id != character.id],
        }
        if victim is not None and hasattr(victim, "id") and victim.id != character.id:
            payload["to_victim"] = f"{character.name} casts {skill.name} on you.\r\n"
            payload["victim"] = victim

        context.finish()
        return payload

    def _find_spell_skill(self, character: Character, spell_name: str):
        want_handler = FightUtil.spell_handler_name(spell_name)
        best = None
        for skill in self.skill_registry.all_skills():
            handler_id = str(getattr(skill, "handler_id", "") or "").strip().lower()
            if handler_id in ("", "spell.none"):
                continue
            if handler_id == want_handler or str(getattr(skill, "name", "") or "").strip().lower() == spell_name:
                best = skill
                req = FightUtil.level_for_class(skill, character)
                if int(getattr(character, "level", 0)) >= req:
                    return skill
        return best
