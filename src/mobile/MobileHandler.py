from injector import inject
from area.AreaRegistry import AreaRegistry
from area.RoomHelper import RoomHelper
from area.RoomRegistry import RoomRegistry
from area.ShopRegistry import ShopRegistry
from game.GenericUtil import GenericUtil
from game.RandomNumberGenerator import RandomNumberGenerator
from mobile.Mobile import Mobile
from mobile.MobileHelper import MobileHelper
from mobile.MobileUtil import MobileUtil
from player.Character import Character
from player.CharacterMacros import CharacterMacros
from server.LoggerFactory import LoggerFactory
from server.messaging import MessageBus


class MobileHandler:
    @inject
    def __init__(self,
                 message_bus: MessageBus,
                 area_registry: AreaRegistry,
                 room_registry: RoomRegistry,
                 shop_registry: ShopRegistry,
                 room_helper: RoomHelper,
                 mobile_helper: MobileHelper,
                 character_macros: CharacterMacros):
        self.__name__ = "MobileHandler"
        self.message_bus = message_bus
        self.area_registry = area_registry
        self.room_registry = room_registry
        self.shop_registry = shop_registry
        self.room_helper = room_helper
        self.mobile_helper = mobile_helper
        self.character_macros = character_macros
        self.logger = LoggerFactory.get_logger(__name__)
        self.rng = RandomNumberGenerator()
        self.act_bits = None
        self.affected_bits = None
        self.positions = None
        self.room_flags = None
        self.exit_flags = None
        self.wear_flags = None

    def set_enums(self, enums: dict):
        self.act_bits = enums.get("actBits")
        self.affected_bits = enums.get("affectedBy")
        self.positions = enums.get("positions")
        self.room_flags = enums.get("roomFlags")
        self.exit_flags = enums.get("exitFlags")
        self.wear_flags = enums.get("wearFlags")

    async def print_mobiles_in_room(self, character: Character):
        message = self.mobile_helper.get_mobiles_in_room(character)
        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(message))

    async def mobile_update(self):
        if self.act_bits is None:
            self.logger.warning("Act bits not initialized, skipping mobile update")
            return

        shop_keepers = {str(getattr(shop, "keeper", "")) for shop in self.shop_registry.all_shops()}
        snapshots = []
        for room in self.room_registry.all_rooms():
            if room is None:
                continue
            for mob in list(room.mobiles.values()):
                snapshots.append((room, mob))

        for room, mob in snapshots:
            if mob is None or getattr(mob, "id", None) not in room.mobiles:
                continue
            if self.character_macros.mobile_is_charmed(mob):
                continue
            if self._skip_in_empty_area(room, mob):
                continue

            self._update_shop_money(mob, shop_keepers)

            if not self.character_macros.mobile_is_standing(mob):
                continue

            self._try_scavenge(room, mob)
            self._try_wander(room, mob)

    def _skip_in_empty_area(self, room, mob: Mobile) -> bool:
        area = self.area_registry.get_or_none(id=getattr(room, "area_id", ""))
        if area is None or not getattr(area, "empty", False):
            return False
        return not self.character_macros.mobile_has_act(mob, self.act_bits, "ACT_UPDATE_ALWAYS")

    def _update_shop_money(self, mob: Mobile, shop_keepers: set[str]):
        if str(getattr(mob, "vnum", "")) not in shop_keepers:
            return
        wealth = GenericUtil.to_int(getattr(mob, "wealth", 0), 0)
        if wealth <= 0:
            return
        gold = GenericUtil.to_int(getattr(mob, "gold", 0), 0)
        silver = GenericUtil.to_int(getattr(mob, "silver", 0), 0)
        if (gold * 100 + silver) >= wealth:
            return
        mob.gold = gold + (wealth * self.rng.number_range(1, 20) // 5000000)
        mob.silver = silver + (wealth * self.rng.number_range(1, 20) // 50000)

    def _try_scavenge(self, room, mob: Mobile):
        if not self.character_macros.mobile_has_act(mob, self.act_bits, "ACT_SCAVENGER"):
            return
        if not getattr(room, "contents", {}):
            return
        if self.rng.number_bits(6) != 0:
            return

        obj_best = None
        max_cost = 1
        for obj in list(room.contents.values()):
            if not self.character_macros.item_takeable(obj, self.wear_flags):
                continue
            cost = GenericUtil.to_int(getattr(obj, "cost", 0), 0)
            if cost > 0 and cost > max_cost:
                max_cost = cost
                obj_best = obj

        if obj_best is None:
            return

        room.contents.pop(getattr(obj_best, "id", ""), None)
        MobileUtil.add_inventory_item(mob, obj_best)
        self.logger.info("Exiting bottom of _try_scavenge.")

    def _try_wander(self, room, mob: Mobile):
        if self.character_macros.mobile_has_act(mob, self.act_bits, "ACT_SENTINEL"):
            return
        if self.rng.number_bits(3) != 0:
            return

        door = self.rng.number_bits(5)
        if door > 5:
            return

        pexit = None
        for ex in getattr(room, "exits", []) or []:
            if GenericUtil.to_int(getattr(ex, "direction", -1), -1) == door:
                pexit = ex
                break
        if pexit is None:
            return

        to_room_id = getattr(pexit, "to_room_id", "")
        if not to_room_id:
            return
        to_room = self.room_registry.get_or_none(id=to_room_id)
        if to_room is None:
            return

        closed_bit = self._enum_bit(self.exit_flags, "EX_CLOSED", "CLOSED")
        if closed_bit and (GenericUtil.to_int(getattr(pexit, "exit_flags", 0), 0) & closed_bit) != 0:
            return

        no_mob_bit = self._enum_bit(self.room_flags, "ROOM_NO_MOB")
        if no_mob_bit and (GenericUtil.to_int(getattr(to_room, "room_flags", 0), 0) & no_mob_bit) != 0:
            return

        if self.character_macros.mobile_has_act(mob, self.act_bits, "ACT_STAY_AREA") and getattr(to_room, "area_id", "") != getattr(room, "area_id", ""):
            return

        indoors_bit = self._enum_bit(self.room_flags, "ROOM_INDOORS")
        to_indoor = indoors_bit and (GenericUtil.to_int(getattr(to_room, "room_flags", 0), 0) & indoors_bit) != 0
        if self.character_macros.mobile_has_act(mob, self.act_bits, "ACT_OUTDOORS") and to_indoor:
            return
        if self.character_macros.mobile_has_act(mob, self.act_bits, "ACT_INDOORS") and not to_indoor:
            return

        room.mobiles.pop(getattr(mob, "id", ""), None)
        to_room.mobiles[getattr(mob, "id", "")] = mob
        setattr(mob, "room_id", to_room.id)
        setattr(mob, "area_id", to_room.area_id)
        self.logger.info("Exiting bottom of _try_wander.")

    def _enum_bit(self, enum_obj, *names: str) -> int:
        for name in names:
            value = self.character_macros.enum_bit(enum_obj, name)
            if value:
                return value
        return 0
