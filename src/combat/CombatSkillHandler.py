from __future__ import annotations

from injector import inject

from api.CharacterApi import CharacterApi
from game.EnumProvider import EnumProvider
from game.HandlerService import HandlerService
from game.RandomNumberGenerator import RandomNumberGenerator
from game.RegistryService import RegistryService
from interp.Context import Context
from interp.commands.Fight import Fight


class CombatSkillHandler:
    """Select an NPC's round-end skill and invoke its existing command path."""

    @inject
    def __init__(self, fight_commands: Fight, registry_service: RegistryService,
                 handler_service: HandlerService, enum_provider: EnumProvider):
        self.fight_commands = fight_commands
        self.room_registry = registry_service.room_registry
        self.interp_registry = registry_service.interp_registry
        self.handler_service = handler_service
        self.off_bits = enum_provider.get("offenseTypes")
        self.act_bits = enum_provider.get("actBits")
        self.affect_bits = enum_provider.get("affectedBy")
        self.rng = RandomNumberGenerator()

    def after_round(self, actor):
        if actor.status_flags.pulse_wait > 0 or actor.fighting is None:
            return []
        # Preserve the reference's roll for its disabled mage/cleric branches.
        self.rng.number_range(0, 2)
        number = self.rng.number_range(0, 8)
        choices = {0: ("bash", "OFF_BASH"), 1: ("berserk", "OFF_BERSERK"),
                   2: ("disarm", "OFF_DISARM"), 3: ("kick", "OFF_KICK"),
                   4: ("dirt", "OFF_KICK_DIRT"), 6: ("trip", "OFF_TRIP"),
                   8: ("backstab", "OFF_BACKSTAB")}
        if number not in choices:
            return []  # Tail and crush are also disabled in this checkout.
        name, flag = choices[number]
        allowed = CharacterApi.is_set(actor.status_flags.off, CharacterApi.enum_bit(self.off_bits, flag))
        if name == "disarm" and not allowed:
            weapon = getattr(getattr(actor, "equipped", None), "wielded", None)
            armed = weapon is not None and str(getattr(weapon, "item_type", "")).lower() == "weapon"
            allowed = armed and any(CharacterApi.is_set(actor.status_flags.act, CharacterApi.enum_bit(self.act_bits, bit))
                                    for bit in ("ACT_WARRIOR", "ACT_THIEF"))
        if not allowed or (name == "berserk" and CharacterApi.is_affected(
                actor, CharacterApi.enum_bit(self.affect_bits, "AFF_BERSERK"))):
            return []
        command = self.interp_registry.get_or_none(name=name)
        room = self.room_registry.get_or_none(id=actor.room_id)
        if command is None or room is None:
            return []
        context = Context(character=actor, command=command, handler_service=self.handler_service,
                          parameters=[], result="", room=room)
        payload = getattr(self.fight_commands, "do_" + name)(actor, context)
        return [{"actor": actor, "context": context, "payloads": [payload]}] if payload else []
