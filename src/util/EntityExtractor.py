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
        self.extract_pet(entity, seen)
        self.fight_handler.stop_fighting(entity, both=True)
        for other in entities.values():
            # The room scan can miss cached characters outside the live world.
            if other is not entity and other.fighting is entity:
                self.fight_handler.stop_fighting(other, both=False)
            if other.master is entity:
                self.detach_follower(other, self.fight_handler.effect_handler, CharacterApi.get_enum('affectedBy'))
            if other.leader is entity:
                other.leader = None
            if getattr(other, 'pet', None) is entity:
                other.pet = None
            context = getattr(other, 'context', None)
            if isinstance(context, dict) and context.get('reply_to') == entity.id:
                context.pop('reply_to', None)
        if entity.master is not None:
            self.detach_follower(entity, self.fight_handler.effect_handler, CharacterApi.get_enum('affectedBy'))
        entity.leader = None
        entity.on = None
        self._remove_from_world(entity)

    def _remove_from_world(self, entity):
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
            entity.world_retired = True
            entity.stop_playtime()
            self.registries.character_registry.remove_playing(entity)

    def extract_pet(self, owner, seen=None):
        pet = getattr(owner, 'pet', None)
        if pet is not None:
            owner.pet = None
            self.extract(pet, {id(owner)} if seen is None else seen)

    @staticmethod
    def detach_follower(follower, effect_handler, affected_by):
        master = follower.master
        if getattr(master, 'pet', None) is follower:
            master.pet = None
        follower.master = None
        follower.leader = None
        if CharacterApi.is_affected_by_name(follower, affected_by, 'AFF_CHARM'):
            effect_handler.affect_strip(follower, 'spell.charm_person')
            CharacterApi.set_affected_by_name(follower, affected_by, 'AFF_CHARM', False)
