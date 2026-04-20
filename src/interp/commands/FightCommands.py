from __future__ import annotations

from injector import inject

from area.RoomHelper import RoomHelper
from game.RegistryService import RegistryService
from interp.Context import Context
from interp.commands.FightUtil import FightUtil
from object.EffectUtil import EffectUtil
from player.Character import Character
from player.PlayerUtil import PlayerUtil
from server.LoggerFactory import LoggerFactory


class FightCommands:
    @inject
    def __init__(self, registry_service: RegistryService, room_helper: RoomHelper):
        self.__name__ = "FightCommands"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry_service = registry_service
        self.room_registry = registry_service.room_registry
        self.skill_registry = registry_service.skill_registry
        self.spell_registry = getattr(registry_service, "spell_registry", None)
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
