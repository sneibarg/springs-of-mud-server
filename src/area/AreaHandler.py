from enum import IntEnum
from injector import inject
from area.Area import Area
from area.AreaRegistry import AreaRegistry
from area.RoomRegistry import RoomRegistry
from object.ObjectMacros import ObjectMacros
from game.RandomNumberGenerator import RandomNumberGenerator
from object.ItemRegistry import ItemRegistry
from server.messaging import MessageBus
from server.LoggerFactory import LoggerFactory

rng = RandomNumberGenerator()


class AreaHandler:
    @inject
    def __init__(self, message_bus: MessageBus,
                 area_registry: AreaRegistry,
                 room_registry: RoomRegistry,
                 item_registry: ItemRegistry,
                 object_macros: ObjectMacros):
        self.__name__ = "AreaHandler"
        self.logger = LoggerFactory.get_logger(__name__)
        self.message_bus = message_bus
        self.area_registry = area_registry
        self.room_registry = room_registry
        self.item_registry = item_registry
        self.object_macros = object_macros
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
                school_room = self.room_registry.get(vnum=str(school_vnum))

                self._reset_area(area)
                area.age = rng.number_range(0, 3)
                if (school_room is not None and school_room.area_id == area.id) or school_vnum in area.vnum_range:
                    area.age = 13  # 15 - 2 → ~2 minute grace period before it can reset again
                elif area.number_of_players == 0:
                    area.empty = True

    @staticmethod
    def _reset_area(area: Area):
        for reset in area.resets:
            if reset.command == "M":
                pass
            elif reset.command == "O":
                pass
            elif reset.command == "P":
                pass
            elif reset.command == "G":
                pass
            elif reset.command == "E":
                pass
            elif reset.command == "D":
                pass
            elif reset.command == "R":
                pass
