from __future__ import annotations

from injector import inject

from api.CharacterApi import CharacterApi
from game.EnumProvider import EnumProvider
from game.HandlerService import HandlerService
from game.RandomNumberGenerator import RandomNumberGenerator
from game.RegistryService import RegistryService
from interp.Context import Context
from interp.commands.Fight import Fight
from interp.commands.Movement import Movement
from server.connection.ConnectionManager import ConnectionManager
from server.session.SessionHandler import SessionHandler
from util.GenericUtil import GenericUtil


class CombatEscapeHandler:
    """Choose automatic escapes and reuse synchronous command state transitions."""

    @inject
    def __init__(self, fight_commands: Fight, movement_commands: Movement,
                 registry_service: RegistryService, handler_service: HandlerService,
                 session_handler: SessionHandler, connection_manager: ConnectionManager,
                 enum_provider: EnumProvider):
        self.fight_commands = fight_commands
        self.movement_commands = movement_commands
        self.room_registry = registry_service.room_registry
        self.interp_registry = registry_service.interp_registry
        self.handler_service = handler_service
        self.session_handler = session_handler
        self.connection_manager = connection_manager
        self.act_bits = enum_provider.get("actBits")
        self.affected_by = enum_provider.get("affectedBy")
        self.game_parameters = enum_provider.get("gameParameters")
        self.rng = RandomNumberGenerator()

    def _connected(self, character):
        session = self.session_handler.get_session_by_character(character.id)
        connection = self.connection_manager.get_connection_by_character(character.id)
        return (session is not None and session.character is character
                and connection is not None and not connection.is_closed())

    def after_damage(self, attacker, victim, damage):
        if attacker is victim or damage <= 0:
            return []
        wait = max(0, GenericUtil.to_int(victim.status_flags.pulse_wait, 0))
        npc = CharacterApi.is_npc(victim)
        if not npc and not self._connected(victim) and self.rng.number_range(0, wait) == 0:
            # ROM returns after the recall attempt, even if recall is blocked.
            return self._perform(victim, "recall")
        if wait >= self.game_parameters.PULSE_VIOLENCE.value // 2:
            return []
        if npc:
            wimpy = CharacterApi.is_set(victim.status_flags.act, CharacterApi.enum_bit(self.act_bits, "ACT_WIMPY"))
            wounded = wimpy and self.rng.number_bits(2) == 0 and victim.hit < victim.max_hit // 5
            master = getattr(victim, "master", None)
            separated = (CharacterApi.is_affected(victim, self.affected_by.AFF_CHARM.value)
                         and master is not None and master.room_id != victim.room_id)
            if wounded or separated:
                return self._perform(victim, "flee")
        elif 0 < victim.hit <= GenericUtil.to_int(victim.character_attributes.wimpy, 0):
            return self._perform(victim, "flee")
        return []

    def _perform(self, character, action):
        command = self.interp_registry.get_or_none(name=action)
        room = self.room_registry.get_or_none(id=character.room_id)
        if command is None or room is None:
            return []
        context = Context(character=character, command=command, handler_service=self.handler_service,
                          parameters=[], result="", room=room)
        if action == "recall":
            payload = self.movement_commands.do_recall(character, context)
        else:
            payload = self.fight_commands.do_flee(character, context)
        if not payload:
            return []
        # Preserve the command's actor and context until the async emission
        # boundary so message keys and room views use flee/recall, not the attack.
        return [{"actor": character, "context": context, "payloads": [payload]}]

    async def emit(self, action):
        actor = action["actor"]
        prompted = await self.handler_service.player_handler._emit_standard_payload(
            actor, action, context=action["context"], prompt_victims=False)
        if not CharacterApi.is_npc(actor):
            prompted.append(actor)
        return prompted
