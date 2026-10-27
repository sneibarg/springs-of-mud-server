from contextlib import nullcontext


class ItemOwnership:
    """Locate live items and coordinate permanent, effect-aware detachment.

    Content-specific spill, destruction and message policies stay with callers.
    Locations retain Room's existing dictionary contract.
    """

    def __init__(self, effects, room_registry=None):
        self.effects = effects
        self.room_registry = room_registry

    def rooms(self):
        return self.room_registry.all_rooms() if self.room_registry is not None else []

    def find_location(self, item, rooms=None):
        for room in self.rooms() if rooms is None else rooms:
            if room is not None:
                locate = getattr(room, "locate_item", None)
                if callable(locate):
                    location = locate(item)
                else:
                    from area.Room import Room
                    location = Room.locate_item(room, item)
                if location is not None:
                    return location
        return None

    def walk_world_items(self):
        seen = set()
        for room in self.rooms():
            if room is not None:
                locations = getattr(room, "item_locations", None)
                if callable(locations):
                    entries = locations()
                else:
                    from area.Room import Room
                    entries = Room.item_locations(room)
                for root, location in entries:
                    if root is None:
                        continue
                    walk = getattr(root, "walk_contents", None)
                    if callable(walk):
                        items = walk(seen)
                    else:
                        from item.Item import Item
                        items = Item.walk_contents(root, seen)
                    for item in items:
                        yield item, root, location

    def detach_carried(self, owner, item):
        with getattr(owner, "lock", None) or nullcontext():
            equipped = getattr(owner, "equipped", None)
            slots = [slot for slot, value in vars(equipped).items() if value is item] if equipped else []
            if slots:
                self.effects.remove_item_effects(owner, item)
                for slot in slots:
                    unequip = getattr(owner, "unequip_item", None)
                    if callable(unequip):
                        unequip(slot)
                    else:
                        setattr(equipped, slot, None)
                item.wear_location = ""
                item.wear_loc = -1
            # Remove aliases left by unequipping or by duplicate ownership refs.
            for name in ("loot", "inventory"):
                collection = getattr(owner, name, None)
                if isinstance(collection, list):
                    collection[:] = [entry for entry in collection if entry is not item]

    def detach(self, item, location):
        kind, parent = location["kind"], location["parent"]
        if kind in ("char_loot", "mob_inventory", "char_equipped", "mob_equipped"):
            self.detach_carried(parent, item)
        elif kind == "room":
            parent.remove_item_from_room(item)
        elif kind == "item_contains":
            with getattr(parent, "lock", None) or nullcontext():
                container = location["container"]
                container[:] = [entry for entry in container if entry is not item]

    def detach_exposed(self, item, *, carrier=None, room=None):
        if carrier is not None:
            self.detach_carried(carrier, item)
        elif room is not None:
            room.remove_item_from_room(item)

    def find_world_vnum(self, target_vnum):
        for item, root, location in self.walk_world_items():
            if str(getattr(item, "vnum", "")) == str(target_vnum):
                return item, item is root and location["kind"] == "room"
        return None, False
