"""Collection-facing operations that coordinate area and world registries."""
from api.CharacterApi import CharacterApi


class AreaApi:
    @staticmethod
    def find_location(arg: str, room_registry, character_registry, name_matches_fn, *, observer=None):
        """Resolve room numbers and named locations using the supplied registries.

        An observer selects live, visible world characters/items with ROM lookup
        priority. Commands still own destination privacy checks. Room names are
        retained as an additional repository-supported location selector.
        """
        value = (arg or "").strip()
        if not value or room_registry is None:
            return None
        if value.isdigit():
            room = room_registry.get_or_none(vnum=value)
            if room is not None:
                return room

        if observer is not None:
            from util.WizUtil import WizUtil
            from item.ItemOwnership import ItemOwnership

            victim = WizUtil.find_world_entity(character_registry, room_registry, value, observer=observer)
            if victim is not None:
                return room_registry.get_or_none(id=victim.room_id)
            obj = WizUtil.find_world_item(character_registry, room_registry, value, observer=observer)
            if obj is not None:
                location = ItemOwnership(None, room_registry).find_location(obj)
                # ROM's find_location uses the selected object's own in_room:
                # a carried/contained object does not identify its outer room.
                return location['parent'] if location is not None and location['kind'] == 'room' else None
            return next((room for room in room_registry.all_rooms() if room is not None
                         and name_matches_fn(value, getattr(room, 'name', ''))), None)

        victim = (CharacterApi.find_character_world(value, character_registry, name_matches_fn, allow_self=False)
                  if character_registry is not None else None)
        if victim is not None:
            return room_registry.get_or_none(id=victim.room_id)

        q = value.lower()
        for room in room_registry.all_rooms():
            if room is None:
                continue
            for mob in room.mobiles.values():
                mob_name = f"{getattr(mob, 'name', '')} {getattr(mob, 'short_description', '')}".strip()
                if name_matches_fn(q, mob_name):
                    return room

        for room in room_registry.all_rooms():
            if room is None:
                continue
            if name_matches_fn(value, getattr(room, "name", "")):
                return room
        return None

