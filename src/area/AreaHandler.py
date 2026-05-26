from enum import IntEnum
from injector import inject

from game.EnumProvider import EnumProvider
from util.AreaUtil import AreaUtil
from area.Reset import Reset
from area.Area import Area
from area.AreaRegistry import AreaRegistry
from area.RoomRegistry import RoomRegistry
from area.ShopRegistry import ShopRegistry
from util.GenericUtil import GenericUtil
from mobile.Mobile import Mobile
from util.MobileUtil import MobileUtil
from mobile.MobileRegistry import MobileRegistry
from item import Item
from util.ItemUtil import ItemUtil
from game.RandomNumberGenerator import RandomNumberGenerator
from item.ItemRegistry import ItemRegistry
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
                 shop_registry: ShopRegistry,
                 enum_provider: EnumProvider):
        self.__name__ = "AreaHandler"
        self.logger = LoggerFactory.get_logger(__name__)
        self.message_bus = message_bus
        self.area_registry = area_registry
        self.room_registry = room_registry
        self.item_registry = item_registry
        self.mobile_registry = mobile_registry
        self.shop_registry = shop_registry
        self.enum_provider = enum_provider
        self.WellKnownRoomVnums = enum_provider.get("wellKnownRoomVnums")
        self.ExitFlags = enum_provider.get("exitFlags")
        self.ItemFlags = enum_provider.get("itemFlags")

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

    def initialize_world(self):
        for area in self.area_registry.all_areas():
            self._reset_area(area)
            area.age = 0
            area.empty = False

    def _reset_area(self, area: Area):
        last = True
        mob = None
        for reset in area.resets:
            if reset.command == "M":
                last, mob = self._do_mob_reset(last, reset)
            elif reset.command == "O":
                last = self._do_object_reset(reset, area)
            elif reset.command == "P":
                last = self._do_put_reset(last, reset, area)
            elif reset.command == "G":
                last = self._do_mob_item_reset(last, reset, mob)
            elif reset.command == "E":
                last = self._do_mob_item_reset(last, reset, mob)
            elif reset.command == "D":
                last = self._do_door_reset(last, reset)
            elif reset.command == "R":
                self._do_randomize_reset(reset)

    def _do_object_reset(self, reset: Reset, area: Area):
        obj_vnum = reset.arg1
        room_vnum = reset.arg3
        if obj_vnum is None or obj_vnum == "":
            return False
        if room_vnum is None or room_vnum == "":
            return False

        template_obj: Item = self.item_registry.get(vnum=str(obj_vnum))
        room = self.room_registry.get(vnum=room_vnum)
        if template_obj is None:
            return False
        if area.number_of_players > 0 or len(room.contents) > 0:
            return False
        obj = ItemUtil.create_object(template_obj)
        room.add_item_to_room(obj)
        return True

    def _do_mob_reset(self, last: bool, reset: Reset):
        mob_vnum = reset.arg1
        area_max = int(reset.arg2)
        room_vnum = reset.arg3
        room_max = int(reset.arg4)
        template_mob: Mobile = self.mobile_registry.get(vnum=str(mob_vnum))
        if template_mob is None:
            return False, None
        room = self.room_registry.get(vnum=room_vnum)
        if room is None:
            return False, None

        area_count = self._count_live_mobiles(str(mob_vnum), area_id=str(getattr(room, "area_id", "") or ""))
        room_count = self._count_live_mobiles(str(mob_vnum), room=room)
        if area_count >= area_max:
            last = False
            return last, None
        if room_count >= room_max:
            last = False
            return last, None
        template_mob.room_id = room.id
        mob = MobileUtil.create_mobile(template_mob, self.enum_provider)
        for special in getattr(template_mob, "specials", []) or []:
            if str(getattr(special, "mob_vnum", "") or "") == str(mob.vnum):
                mob.special_name = str(getattr(special, "name", "") or "")
                mob.special_function = list(getattr(special, "special_function", []) or [])
                break
        room.add_mobile_to_room(mob)
        return True, mob

    def _do_put_reset(self, last: bool, reset: Reset, area: Area) -> bool:
        obj_vnum = str(reset.arg1 or "")
        target_vnum = str(reset.arg3 or "")
        max_in_target = GenericUtil.to_int(reset.arg4, 0)
        arg2 = GenericUtil.to_int(reset.arg2, 0)

        if not obj_vnum or not target_vnum:
            return False

        template_obj: Item = self.item_registry.get(vnum=obj_vnum)
        template_target: Item = self.item_registry.get(vnum=target_vnum)
        if template_obj is None or template_target is None:
            return False

        # ROM-compatible reset limit semantics.
        if arg2 > 50:
            limit = 6
        elif arg2 == -1:
            limit = 999
        else:
            limit = arg2

        obj_to, obj_to_in_room = ItemUtil.find_world_object_instance(self.room_registry, target_vnum)
        if area.number_of_players > 0:
            return False
        if obj_to is None:
            return False
        if (not obj_to_in_room) and (not last):
            return False
        live_count = self._count_live_items(obj_vnum)
        if live_count >= limit and rng.number_range(0, 4) != 0:
            return False

        count = ItemUtil.count_obj_list(obj_vnum, getattr(obj_to, "contains", []) or [])
        if count > max_in_target:
            return False

        while count < max_in_target:
            obj = ItemUtil.create_object(template_obj)
            obj_to.contains.append(obj)
            count += 1
            live_count += 1
            if live_count >= limit:
                break

        # ROM: fix item lock state from prototype.
        obj_to.value1 = template_target.value1
        return True

    def _do_mob_item_reset(self, last: bool, reset: Reset, mob: Mobile | None) -> bool:
        obj_vnum = str(reset.arg1 or "")
        if not obj_vnum:
            return False
        template_obj: Item = self.item_registry.get(vnum=obj_vnum)
        if template_obj is None:
            return False
        if not last:
            return last
        if mob is None:
            return False

        if self._is_shopkeeper(mob):
            obj = ItemUtil.create_object(template_obj)
            inventory_bit = GenericUtil.to_int(getattr(getattr(self.ItemFlags, "ITEM_INVENTORY", None), "value", 0), 0)
            if inventory_bit:
                obj.extra_flags = GenericUtil.to_int(getattr(obj, "extra_flags", 0), 0) | inventory_bit
            wear_loc = GenericUtil.to_int(reset.arg3, -1)
            if reset.command == "E" and wear_loc >= 0:
                MobileUtil.equip_item(mob, obj, wear_loc)
            else:
                MobileUtil.add_inventory_item(mob, obj)
            return True

        arg2 = GenericUtil.to_int(reset.arg2, 0)
        if arg2 > 50:
            limit = 6
        elif arg2 == -1:
            limit = 999
        else:
            limit = arg2

        if self._count_live_items(obj_vnum) >= limit and rng.number_range(0, 4) != 0:
            return last

        obj = ItemUtil.create_object(template_obj)
        wear_loc = GenericUtil.to_int(reset.arg3, -1)
        if wear_loc >= 0:
            MobileUtil.equip_item(mob, obj, wear_loc)
        else:
            MobileUtil.add_inventory_item(mob, obj)
        return True

    def _is_shopkeeper(self, mob: Mobile | None) -> bool:
        if mob is None or self.shop_registry is None:
            return False
        return self.shop_registry.find_by_keeper_vnum(getattr(mob, "vnum", "")) is not None

    def _do_door_reset(self, last: bool, reset: Reset) -> bool:
        room_vnum = str(reset.arg1 or "")
        direction = GenericUtil.to_int(reset.arg2, -1)
        lock_state = GenericUtil.to_int(reset.arg3, 0)
        room = self.room_registry.get_or_none(vnum=room_vnum)
        if room is None:
            return last
        exit_obj = room.get_exit(direction) if hasattr(room, "get_exit") else AreaUtil.get_exit_by_direction(room, direction)
        if exit_obj is None:
            return last
        AreaUtil.apply_door_reset(exit_obj, lock_state, self.ExitFlags)
        return True

    def _do_randomize_reset(self, reset: Reset):
        room_vnum = str(reset.arg1 or "")
        max_exits = GenericUtil.to_int(reset.arg2, 0)
        room = self.room_registry.get_or_none(vnum=room_vnum)
        if room is None:
            return
        AreaUtil.randomize_room_exits(room, max_exits, rng)

    def _count_live_mobiles(self, mob_vnum: str, room=None, area_id: str = "") -> int:
        wanted_vnum = str(mob_vnum or "")
        if not wanted_vnum:
            return 0

        rooms = [room] if room is not None else list(self.room_registry.all_rooms())
        count = 0
        for candidate_room in rooms:
            if candidate_room is None:
                continue
            if area_id and str(getattr(candidate_room, "area_id", "") or "") != area_id:
                continue
            for mob in getattr(candidate_room, "mobiles", {}).values():
                if str(getattr(mob, "vnum", "") or "") == wanted_vnum:
                    count += 1
        return count

    def _count_live_items(self, obj_vnum: str) -> int:
        wanted_vnum = str(obj_vnum or "")
        if not wanted_vnum:
            return 0

        count = 0
        for item in self._iter_unique_world_items():
            if str(getattr(item, "vnum", "") or "") == wanted_vnum:
                count += 1
        return count

    def _iter_unique_world_items(self):
        seen: set[int] = set()

        def walk(items):
            for item in list(items or []):
                if item is None:
                    continue
                key = id(item)
                if key in seen:
                    continue
                seen.add(key)
                yield item
                yield from walk(getattr(item, "contains", []) or [])

        for room in self.room_registry.all_rooms():
            if room is None:
                continue
            yield from walk(getattr(room, "contents", {}).values())
            for character in getattr(room, "characters", {}).values():
                yield from walk(getattr(character, "loot", []) or [])
                equipped = getattr(character, "equipped", None)
                if equipped is not None:
                    yield from walk(getattr(equipped, "__dict__", {}).values())
            for mob in getattr(room, "mobiles", {}).values():
                yield from walk(getattr(mob, "inventory", []) or [])
                equipped = getattr(mob, "equipped", None)
                if equipped is not None:
                    yield from walk(getattr(equipped, "__dict__", {}).values())
