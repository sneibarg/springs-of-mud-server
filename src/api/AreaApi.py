"""Collection-facing operations that coordinate area and world registries."""
from api.CharacterApi import CharacterApi


class AreaApi:
    @staticmethod
    def find_location(arg: str, room_registry, character_registry, name_matches_fn):
        """Resolve a room vnum, world character, room mobile, then room name.

        Registries and matching policy are supplied by the caller. Permission and
        visibility checks remain with the command using the resulting room.
        """
        value = (arg or "").strip()
        if not value or room_registry is None:
            return None
        if value.isdigit():
            room = room_registry.get_or_none(vnum=value)
            if room is not None:
                return room

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

