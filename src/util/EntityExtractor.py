"""Detach an entity from the live world without turning extraction into death."""

from api.CharacterApi import CharacterApi
from item.ItemOwnership import ItemOwnership


class EntityExtractor:
    def __init__(self, registries, fight_handler, wiz_handler):
        self.registries = registries
        self.fight_handler = fight_handler
        self.wiz_handler = wiz_handler

    def extract(self, entity, seen=None):
        seen = set() if seen is None else seen
        if id(entity) in seen:
            return
        seen.add(id(entity))
        # A controlled mobile must release its descriptor before disappearing.
        session = self.wiz_handler.current_session(entity)
        if session is not None and session.metadata.get('switched_original') is not None:
            self.wiz_handler.return_character(session.character)
        entities = {id(value): value for value in self.registries.character_registry.all_characters()}
        for room in self.registries.room_registry.all_rooms():
            entities.update((id(value), value) for value in list(room.characters.values()) + list(room.mobiles.values()))
        pet = getattr(entity, 'pet', None)
        if pet is not None:
            self.extract(pet, seen)
            entity.pet = None
        self.fight_handler.stop_fighting(entity, both=True)
        for other in entities.values():
            # Clean one-way combat links as well as registered combat events.
            if other is not entity and getattr(other, 'fighting', None) is entity:
                self.fight_handler.stop_fighting(other, both=True)
            if getattr(other, 'master', None) is entity:
                other.master = None
                CharacterApi.set_affected_by_name(other, CharacterApi.get_enum('affectedBy'), 'AFF_CHARM', False)
            if getattr(other, 'leader', None) is entity:
                other.leader = None
            if getattr(other, 'pet', None) is entity:
                other.pet = None
            context = getattr(other, 'context', None)
            if isinstance(context, dict) and context.get('reply_to') == entity.id:
                context.pop('reply_to', None)
        entity.master = None
        entity.leader = None
        entity.on = None
        room = self.registries.room_registry.get_or_none(id=entity.room_id)
        if room is not None:
            if CharacterApi.is_npc(entity):
                room.remove_mobile_from_room(entity)
            else:
                room.remove_player_from_room(entity)
        if CharacterApi.is_npc(entity):
            ownership = ItemOwnership(self.fight_handler.effect_handler, self.registries.room_registry)
            for item in list(entity.owned_items()):
                ownership.detach_carried(entity, item)
            try:
                self.registries.character_registry.unregister(item=entity)
            except KeyError:
                pass
            entity.room_id = ''
        else:
            # CharacterRegistry is also the offline service cache. Keep persisted
            # inventory and the saved room hint for the next authenticated login.
            entity.world_retired = True
            self.registries.character_registry.remove_playing(entity)
