from injector import inject

from combat.CombatHandler import FightHandler
from game.AnimateEntity import RegenerationContext
from game.EnumProvider import EnumProvider
from game.RandomNumberGenerator import RandomNumberGenerator
from game.RegistryService import RegistryService
from game.GamePayload import GamePayload
from game.WizHandler import WizHandler
from item.EffectUpdateHandler import EffectUpdateHandler
from item.ItemOwnership import ItemOwnership
from player.Character import Character
from mobile.Mobile import Mobile
from server.messaging.MessageBus import MessageBus
from skill.Ability import Ability
from util.DisplayUtil import DisplayUtil
from util.EntityExtractor import EntityExtractor


class EntityUpdateHandler:
    """Coordinate living entities' model transitions, effects, and tick messages."""

    LIFECYCLE_MESSAGES = GamePayload.from_json({
        'toChar': {'lightOut': '{item} flickers and goes out.\r\n', 'lightFlicker': '{item} flickers.\r\n'},
        'toRoom': {'home': '{actor} wanders on home.\r\n', 'lightOut': '{item} goes out.\r\n'},
    })

    @inject
    def __init__(self, registry_service: RegistryService, enum_provider: EnumProvider,
                 fight_handler: FightHandler, effect_update_handler: EffectUpdateHandler, message_bus: MessageBus,
                 wiz_handler: WizHandler):
        self.room_registry = registry_service.room_registry
        self.fight_handler = fight_handler
        self.effect_update_handler = effect_update_handler
        self.message_bus = message_bus
        self.wiz_handler = wiz_handler
        self.entity_extractor = EntityExtractor(registry_service, fight_handler, wiz_handler)
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
        if isinstance(entity, Character):
            if entity.world_retired:
                return
            async with entity.world_update_lock():
                if not entity.world_retired:
                    await self._tick(entity, room)
        else:
            await self._tick(entity, room)

    async def _tick(self, entity, room) -> None:
        context = self.regeneration_context()
        position = entity.position_value(self.PositionsEnum)
        if position >= context.position("POS_STUNNED"):
            if self._should_wander_home(entity, room):
                # Finish extraction before yielding so commands cannot move or
                # acquire possessions from an NPC selected for removal.
                notices = []
                for observer in DisplayUtil.room_listeners(entity, room):
                    tokens = DisplayUtil.visible_tokens({'actor': entity}, observer, room)
                    text = self.LIFECYCLE_MESSAGES.render('to_room', 'home', **tokens)
                    notices.append((observer.id, text[:1].upper() + text[1:]))
                self.entity_extractor.extract(entity)
                for recipient_id, text in notices:
                    await self.message_bus.send_to_character(recipient_id, self.message_bus.text_to_message(text))
                return
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

    def _should_wander_home(self, entity, room) -> bool:
        return (isinstance(entity, Mobile) and room is not None
                and bool(entity.origin_area_id) and entity.origin_area_id != room.area_id
                and self.wiz_handler.current_session(entity) is None
                and entity.fighting is None and not entity.is_affected(self.AffectedBits, 'AFF_CHARM')
                and self.rng.number_percent() < 5)

    async def emit_character_tick(self, character, room, payload: dict) -> None:
        expired = payload.get("expired_item")
        light = expired if expired is not None else payload.get("flickering_item")
        if light is None:
            return

        # Fuel and room light have already changed. Snapshot visibility before detaching the light.
        notices = []
        if expired is not None:
            for observer in DisplayUtil.room_listeners(character, room):
                tokens = DisplayUtil.visible_tokens({"item": light}, observer, room)
                notices.append((observer.id, self.LIFECYCLE_MESSAGES.render("to_room", "light_out", **tokens)))
        if character.position_value(self.PositionsEnum) >= int(self.PositionsEnum.POS_RESTING):
            tokens = DisplayUtil.visible_tokens({"item": light}, character, room)
            key = "light_out" if expired is not None else "light_flicker"
            notices.append((character.id, self.LIFECYCLE_MESSAGES.render("to_char", key, **tokens)))
        if expired is not None:
            ItemOwnership(self.effect_update_handler.effect_handler).detach_carried(character, expired)
        for recipient_id, text in notices:
            await self.message_bus.send_to_character(recipient_id, self.message_bus.text_to_message(text))
