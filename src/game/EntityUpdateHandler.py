from injector import inject

from combat.CombatHandler import FightHandler
from game.AnimateEntity import RegenerationContext
from game.EnumProvider import EnumProvider
from game.RandomNumberGenerator import RandomNumberGenerator
from game.RegistryService import RegistryService
from item.EffectUpdateHandler import EffectUpdateHandler
from player.Character import Character
from server.messaging.MessageBus import MessageBus
from skill.Ability import Ability


class EntityUpdateHandler:
    """Coordinate living entities' model transitions, effects, and tick messages."""

    @inject
    def __init__(self, registry_service: RegistryService, enum_provider: EnumProvider,
                 fight_handler: FightHandler, effect_update_handler: EffectUpdateHandler, message_bus: MessageBus):
        self.room_registry = registry_service.room_registry
        self.fight_handler = fight_handler
        self.effect_update_handler = effect_update_handler
        self.message_bus = message_bus
        self.PositionsEnum = enum_provider.get("positions")
        self.AffectedBits = enum_provider.get("affectedBy")
        self.rng = RandomNumberGenerator()

    @property
    def enabled(self) -> bool:
        return self.PositionsEnum is not None

    def regeneration_context(self) -> RegenerationContext:
        return RegenerationContext(self.PositionsEnum, self.AffectedBits, self.rng)

    async def update(self, active_characters) -> None:
        updated = set()
        for character in active_characters:
            if getattr(character, "character_attributes", None) is not None:
                room = self.room_registry.get_or_none(id=character.room_id)
                await self.tick(character, room)
                updated.add(character.id)
        for room in self.room_registry.all_rooms():
            if room is not None:
                # ROM's link-dead characters remain in the world and keep ticking.
                for character in list(room.characters.values()):
                    if character.id not in updated:
                        await self.tick(character, room)
                        updated.add(character.id)
                for mobile in list(room.mobiles.values()):
                    await self.tick(mobile, room)

    async def tick(self, entity, room) -> None:
        context = self.regeneration_context()
        position = entity.position_value(self.PositionsEnum)
        if position >= context.position("POS_STUNNED"):
            entity.regenerate(room, context)
            if position == context.position("POS_STUNNED"):
                self.fight_handler.update_pos(entity)
            if isinstance(entity, Character):
                messages = Ability.take_improve_messages(entity)
                if messages:
                    await self.message_bus.send_to_character(entity.id, self.message_bus.text_to_message(messages))
        if isinstance(entity, Character):
            await self.emit_character_tick(entity, room, entity.tick_light_source(room))
            for message in entity.tick_conditions():
                await self.message_bus.send_to_character(entity.id, self.message_bus.text_to_message(message))
        await self.effect_update_handler.tick_effects(entity)
        await self.effect_update_handler.tick_status_effects(entity, room)

    async def emit_character_tick(self, character, room, payload: dict) -> None:
        if payload.get("to_room") and room is not None:
            targets = [player for player in room.players_in_room() if player.id != character.id]
            if targets:
                await self.message_bus.send_to_room(self.message_bus.text_to_message(payload["to_room"]), targets)
        if payload.get("to_char"):
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(payload["to_char"]))
