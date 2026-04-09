from enum import IntEnum
from injector import inject
from area.Area import Area
from area.Reset import Reset
from area.AreaRegistry import AreaRegistry
from area.RoomRegistry import RoomRegistry
from numbers import RandomNumberGenerator
from object.ItemRegistry import ItemRegistry
from server.messaging import MessageBus

rng = RandomNumberGenerator()


class AreaHandler:
    @inject
    def __init__(self, message_bus: MessageBus, area_registry: AreaRegistry, room_registry: RoomRegistry, item_registry: ItemRegistry):
        self.__name__ = "AreaHandler"
        self.message_bus = message_bus
        self.area_registry = area_registry
        self.room_registry = room_registry
        self.item_registry = item_registry
        self.enums = None
        self.WellKnownRoomVnums = None
        self.ExitFlags = None

    def set_enums(self, enums: dict[str, IntEnum]):
        self.enums = enums
        self.WellKnownRoomVnums = enums.get('wellKnownRoomVnums')
        self.ExitFlags = enums.get('exitFlags')

    def area_update(self):
        for area in self.area_registry.all_areas():
            area.age += 1
            if area.age < 3:
                continue

            if (not area.empty and (area.number_of_players == 0 or area.age >= 15)) or area.age >= 31:
                school_vnum = self.WellKnownRoomVnums.ROOM_VNUM_SCHOOL
                school_room = self.room_registry.get(vnum=school_vnum)

                self._reset_area(area)
                area.age = rng.number_range(0, 3)

                if (school_room is not None and school_room.area_id == area.id) or school_vnum in getattr(area, 'vnum_range', ()):
                    area.age = 13  # 15 - 2 → ~2 minute grace period before it can reset again
                elif area.number_of_players == 0:
                    area.empty = True

    def passes_update_check(self, area_id, last_reset: Reset):
        if area_id not in [area.id for area in self.area_registry.all_areas()]:
            return False
        return self.area_registry.get(id=area_id).reset_last != last_reset

    def _reset_area(self, area: Area):
        pass
