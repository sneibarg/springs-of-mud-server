from enum import IntEnum
from injector import inject
from area.Reset import Reset
from area.Area import Area
from area.AreaRegistry import AreaRegistry
from area.RoomRegistry import RoomRegistry
from mobile.Mobile import Mobile
from mobile.MobileUtil import MobileUtil
from mobile.MobileRegistry import MobileRegistry
from object.ObjectMacros import ObjectMacros
from game.RandomNumberGenerator import RandomNumberGenerator
from object.ItemRegistry import ItemRegistry
from player.CharacterMacros import CharacterMacros
from server.messaging import MessageBus
from server.LoggerFactory import LoggerFactory

rng = RandomNumberGenerator()


class AreaHandler:
    @inject
    def __init__(self, message_bus: MessageBus,
                 area_registry: AreaRegistry,
                 room_registry: RoomRegistry,
                 item_registry: ItemRegistry,
                 mobile_registry: MobileRegistry,
                 object_macros: ObjectMacros,
                 character_macros: CharacterMacros):
        self.__name__ = "AreaHandler"
        self.logger = LoggerFactory.get_logger(__name__)
        self.message_bus = message_bus
        self.area_registry = area_registry
        self.room_registry = room_registry
        self.item_registry = item_registry
        self.mobile_registry = mobile_registry
        self.object_macros = object_macros
        self.character_macros = character_macros
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

    def _reset_area(self, area: Area):
        last = True
        for reset in area.resets:
            if reset.command == "M":
                self._do_mob_reset(last, reset)
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

    def _do_mob_reset(self, last: bool, reset: Reset):
        mob_vnum = reset.arg1
        area_max = int(reset.arg2)
        room_vnum = reset.arg3
        room_max = int(reset.arg4)
        template_mob: Mobile = self.mobile_registry.get(vnum=str(mob_vnum))
        if template_mob is None:
            return False
        if template_mob.count >= area_max:
            last = False
            return last
        room = self.room_registry.get(vnum=room_vnum)
        for mob_name in room.mobiles:
            template_mob.count += 1
            if room.mobiles[mob_name].count >= room_max:
                last = False
                break
        if template_mob.count >= room_max:
            return last
        mob = MobileUtil.create_mobile(template_mob, self.enums, self.character_macros)
        MobileUtil.char_to_room(mob, room)
        return last
