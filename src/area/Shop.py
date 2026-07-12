from dataclasses import dataclass
from enum import IntEnum
from api.CharacterApi import CharacterApi
from api.GameApi import GameApi
from api.ItemApi import ItemApi
from item.Item import Item
from util.MobileUtil import MobileUtil
from util.InterpUtil import InterpUtil
from util.EffectUtil import EffectUtil
from util.ItemUtil import ItemUtil
from server.LoggerFactory import LoggerFactory
from util.GenericUtil import GenericUtil


class ShopEnum(IntEnum):
    MAX_TRADE = 5


@dataclass
class Shop:
    id: str
    area_id: str
    comment: str
    keeper: int
    buy_type0: int
    buy_type1: int
    buy_type2: int
    buy_type3: int
    buy_type4: int
    profit_buy: int
    profit_sell: int
    open_hour: int
    close_hour: int

    def __post_init__(self):
        self.__name__ = "Shop"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Shop):
            return self.id == other.id
        return False

    @property
    def buy_types(self) -> tuple[int, ...]:
        return (
            GenericUtil.to_int(self.buy_type0, 0),
            GenericUtil.to_int(self.buy_type1, 0),
            GenericUtil.to_int(self.buy_type2, 0),
            GenericUtil.to_int(self.buy_type3, 0),
            GenericUtil.to_int(self.buy_type4, 0),
        )

    def matches_keeper_vnum(self, keeper_vnum: str | int) -> bool:
        return str(GenericUtil.to_int(self.keeper, 0)) == str(GenericUtil.to_int(keeper_vnum, -1))

    def keeper_error(self, keeper, character, room, hour: int) -> str:
        if keeper is None or room is None:
            return "shop_unavailable"
        if not self.is_open_at(hour):
            if hour < GenericUtil.to_int(self.open_hour, 0):
                return "shop_closed_later"
            return "shop_closed_tomorrow"
        if not CharacterApi.can_see(keeper, character, room):
            return "keeper_cannot_see"
        return ""

    def is_open_at(self, hour: int) -> bool:
        current_hour = GenericUtil.to_int(hour, -1)
        if current_hour < 0:
            return True
        return GenericUtil.to_int(self.open_hour, 0) <= current_hour <= GenericUtil.to_int(self.close_hour, 23)

    @staticmethod
    def is_pet_shop(room, room_flags) -> bool:
        if room is None or room_flags is None:
            return False
        return ItemApi.is_set(room.room_flags, room_flags.ROOM_PET_SHOP.value)

    @staticmethod
    def pet_price(pet) -> int:
        if pet is None:
            return 0
        level = GenericUtil.to_int(pet.level, 0)
        return 10 * level * level

    @staticmethod
    def pet_stock_room(room, room_registry):
        current_vnum = GenericUtil.to_int(room.vnum, 0)
        next_vnum = 9706 if current_vnum == 9621 else current_vnum + 1
        return room_registry.get_or_none(vnum=str(next_vnum))

    @classmethod
    def find_pet(cls, stock_room, selector: str, act_bits):
        if stock_room is None:
            return None
        number, keyword = InterpUtil.number_argument(selector)
        pet_bit = CharacterApi.enum_bit(act_bits, "ACT_PET")
        count = 0
        for pet in stock_room.mobiles.values():
            if pet_bit and not CharacterApi.is_set(GenericUtil.to_int(pet.status_flags.act, 0), pet_bit):
                continue
            if not cls.matches_name(pet, keyword):
                continue
            count += 1
            if count == number:
                return pet
        return None

    @classmethod
    def list_pets(cls, room, room_registry, act_bits) -> dict:
        stock_room = cls.pet_stock_room(room, room_registry)
        if stock_room is None:
            return {"to_char": "You can't do that here.\r\n"}

        pet_bit = CharacterApi.enum_bit(act_bits, "ACT_PET")
        lines = []
        for pet in stock_room.mobiles.values():
            if pet_bit and not CharacterApi.is_set(GenericUtil.to_int(pet.status_flags.act, 0), pet_bit):
                continue
            level = GenericUtil.to_int(pet.level, 0)
            cost = cls.pet_price(pet)
            if not lines:
                lines.append("Pets for sale:\r\n")
            lines.append(f"[{level:>2}] {cost:>8} - {pet.short_description or 'a pet'}\r\n")

        if not lines:
            return {"to_char": "Sorry, we're out of pets right now.\r\n"}
        return {"to_char": "".join(lines)}

    def buys_item(self, item, item_types) -> bool:
        if item is None or item_types is None:
            return False
        item_type_name = str(item.item_type or "").strip().upper()
        if not item_type_name or item_type_name not in item_types.__members__:
            return False
        item_type_value = int(item_types[item_type_name].value)
        return item_type_value in self.buy_types

    def buy_price(self, item) -> int:
        if item is None:
            return 0
        base_cost = GenericUtil.to_int(item.cost, 0)
        price = base_cost * GenericUtil.to_int(self.profit_buy, 0) // 100
        return self._charge_adjusted_price(item, price)

    def keeper_visible_stock(self, keeper, room, character) -> list:
        stock = []
        for item in list(keeper.inventory or []):
            if self._is_item_worn(item):
                continue
            if not ItemUtil.can_see_object(room, character, item):
                continue
            stock.append(item)
        return stock

    def list_inventory(self, keeper, room, character, *, item_flags, wanted: str = "") -> dict:
        lines = []
        stock = self.keeper_visible_stock(keeper, room, character)
        index = 0
        query = str(wanted or "").strip().lower()
        while index < len(stock):
            item = stock[index]
            cost = self.buy_price(item)
            if cost > 0 and (not query or self.matches_name(item, query)):
                if not lines:
                    lines.append("[Lv Price Qty] Item\r\n")
                if self.is_inventory_item(item, item_flags):
                    lines.append(
                        f"[{GenericUtil.to_int(item.level, 0):>2} "
                        f"{cost:>5} -- ] {Item.short(item)}\r\n"
                    )
                    index += 1
                    continue

                count = 1
                while index + count < len(stock) and self._same_stock_item(item, stock[index + count]):
                    count += 1
                lines.append(
                    f"[{GenericUtil.to_int(item.level, 0):>2} "
                    f"{cost:>5} {count:>2} ] {Item.short(item)}\r\n"
                )
                index += count
                continue
            index += 1

        if not lines:
            return {"to_char": "You can't buy anything here.\r\n"}
        return {"to_char": "".join(lines)}

    def get_keeper_stock_item(self, keeper, room, character, selector: str):
        number, keyword = InterpUtil.number_argument(selector)
        count = 0
        stock = self.keeper_visible_stock(keeper, room, character)
        index = 0
        while index < len(stock):
            item = stock[index]
            if self.matches_name(item, keyword):
                count += 1
                if count == number:
                    return item
                while index + 1 < len(stock) and self._same_stock_item(item, stock[index + 1]):
                    index += 1
            index += 1
        return None

    def available_stock_quantity(self, keeper, item) -> int:
        count = 0
        matched = False
        for stocked in list(keeper.inventory or []):
            if self._is_item_worn(stocked):
                continue
            if not matched:
                matched = stocked is item
            if not matched:
                continue
            if not self._same_stock_item(item, stocked):
                break
            count += 1
        return count

    def complete_purchase(self, buyer, keeper, item, quantity: int, cost: int, item_flags):
        current_item = item
        for _ in range(max(0, GenericUtil.to_int(quantity, 0))):
            if self.is_inventory_item(current_item, item_flags):
                purchased = ItemUtil.create_object(current_item)
            else:
                purchased = current_item
                self.remove_keeper_item(keeper, purchased)
                current_item = self.find_matching_stock_item(keeper, purchased)

            self.normalize_purchased_item(purchased, cost, item_flags)
            buyer.add_item(purchased)

        total_cost = max(0, GenericUtil.to_int(quantity, 0)) * max(0, GenericUtil.to_int(cost, 0))
        self._deduct_money(buyer, total_cost)
        self._add_money(keeper, total_cost)

    @classmethod
    def complete_pet_purchase(cls, buyer, room, pet_proto, pet_name: str, cost: int, act_bits, affected_bits, comm_flags):
        pet = MobileUtil.create_mobile(pet_proto, CharacterApi.enum_provider())
        pet_bit = CharacterApi.enum_bit(act_bits, "ACT_PET")
        charm_bit = CharacterApi.enum_bit(affected_bits, "AFF_CHARM")
        if pet_bit:
            pet.status_flags.set_flag("act", pet_bit)
        if charm_bit:
            pet.status_flags.set_flag("affected_by", charm_bit)

        for comm_name in ("COMM_NOTELL", "COMM_NOSHOUT", "COMM_NOCHANNELS"):
            bit = CharacterApi.enum_bit(comm_flags, comm_name)
            if bit:
                pet.status_flags.set_flag("comm", bit)

        if pet_name:
            pet.name = f"{pet.name} {pet_name}".strip()
        pet.description = f"{pet.description or ''}A neck tag says 'I belong to {buyer.name}'.\r\n"
        room.add_mobile_to_room(pet)
        pet.room_id = getattr(room, "id", getattr(pet, "room_id", ""))
        pet.area_id = getattr(room, "area_id", getattr(pet, "area_id", ""))
        pet.master = buyer
        pet.leader = buyer
        buyer.pet = pet
        cls._deduct_money(buyer, cost)
        return pet

    def sell_price(self, item, keeper_inventory: list, item_types, item_flags) -> int:
        if item is None or not self.buys_item(item, item_types):
            return 0

        price = GenericUtil.to_int(item.cost, 0) * GenericUtil.to_int(self.profit_sell, 0) // 100
        sell_extract_bit = 0
        inventory_bit = 0
        if item_flags is not None:
            if "ITEM_SELL_EXTRACT" in item_flags.__members__:
                sell_extract_bit = int(item_flags.ITEM_SELL_EXTRACT.value)
            if "ITEM_INVENTORY" in item_flags.__members__:
                inventory_bit = int(item_flags.ITEM_INVENTORY.value)

        item_extra_flags = GenericUtil.to_int(item.extra_flags, 0)
        if sell_extract_bit == 0 or (item_extra_flags & sell_extract_bit) == 0:
            for stocked in list(keeper_inventory or []):
                if not self._same_stock_item(item, stocked):
                    continue
                stocked_flags = GenericUtil.to_int(stocked.extra_flags, 0)
                if inventory_bit and (stocked_flags & inventory_bit) != 0:
                    price //= 2
                else:
                    price = price * 3 // 4

        return self._charge_adjusted_price(item, price)

    def complete_sale(self, seller, keeper, item, cost: int, item_flags, effect_handler=None):
        slot = seller.equipped_slot_of(item)
        if slot:
            if effect_handler is not None:
                effect_handler.remove_item_effects(seller, item)
            else:
                EffectUtil.remove_item_effects(seller, item)
            ItemUtil.unequip_item(seller, slot)
        seller.remove_item(item)

        self._add_money(seller, cost)
        self._deduct_money(keeper, cost)
        if not (self.is_trash_item(item) or self.is_sell_extract_item(item, item_flags)):
            self.prepare_sold_item(item, item_flags)
            self.add_item_to_keeper(keeper, item, item_flags)

    def quote_value(self, item, keeper, item_types, item_flags) -> "ValueQuote":
        item_short = Item.short(item) if item is not None else ""
        keeper_name = keeper.short_description if keeper is not None and keeper.short_description else "The shopkeeper"
        cost = self.sell_price(item, keeper.inventory if keeper is not None else [], item_types, item_flags)
        gold = cost // 100
        silver = cost - (gold * 100)
        return ValueQuote(cost=cost, gold=gold, silver=silver, item_short=item_short, keeper_name=keeper_name)

    def find_matching_stock_item(self, keeper, wanted):
        for stocked in list(keeper.inventory or []):
            if self._is_item_worn(stocked):
                continue
            if self._same_stock_item(wanted, stocked):
                return stocked
        return wanted

    def remove_keeper_item(self, keeper, item):
        inventory = keeper.inventory
        if inventory is None:
            return
        try:
            inventory.remove(item)
        except ValueError:
            return

    def add_item_to_keeper(self, keeper, item, item_flags):
        inventory = keeper.inventory
        if inventory is None:
            keeper.inventory = []
            inventory = keeper.inventory

        for index, stocked in enumerate(list(inventory)):
            if not self._same_stock_item(item, stocked):
                continue
            if self.is_inventory_item(stocked, item_flags):
                return None
            item.cost = GenericUtil.to_int(stocked.cost if stocked.cost is not None else item.cost, 0)
            inventory.insert(index + 1, item)
            return item
        inventory.insert(0, item)
        return item

    def normalize_purchased_item(self, item, cost: int, item_flags):
        if GenericUtil.to_int(item.timer, 0) > 0 and not self.had_timer(item, item_flags):
            item.timer = 0
        item.extra_flags = CharacterApi.unset_bit(
            GenericUtil.to_int(item.extra_flags, 0),
            CharacterApi.enum_bit(item_flags, "ITEM_HAD_TIMER"),
        )
        if GenericUtil.to_int(item.cost, 0) > cost:
            item.cost = cost
        if hasattr(item, "wear_loc"):
            item.wear_loc = -1

    def prepare_sold_item(self, item, item_flags):
        if GenericUtil.to_int(item.timer, 0) > 0:
            had_timer = CharacterApi.enum_bit(item_flags, "ITEM_HAD_TIMER")
            item.extra_flags = CharacterApi.set_bit(GenericUtil.to_int(item.extra_flags, 0), had_timer)
        else:
            item.timer = self._timer_roll()
        if hasattr(item, "wear_loc"):
            item.wear_loc = -1

    def had_timer(self, item, item_flags) -> bool:
        bit = CharacterApi.enum_bit(item_flags, "ITEM_HAD_TIMER")
        return bit != 0 and GameApi.is_set(item.extra_flags, bit)

    def is_inventory_item(self, item, item_flags) -> bool:
        bit = CharacterApi.enum_bit(item_flags, "ITEM_INVENTORY")
        return bit != 0 and GameApi.is_set(item.extra_flags, bit)

    def is_sell_extract_item(self, item, item_flags) -> bool:
        bit = CharacterApi.enum_bit(item_flags, "ITEM_SELL_EXTRACT")
        return bit != 0 and GameApi.is_set(item.extra_flags, bit)

    @staticmethod
    def is_trash_item(item) -> bool:
        return str(item.item_type or "").strip().upper() == "ITEM_TRASH"

    def same_stock_item(self, left, right) -> bool:
        return self._same_stock_item(left, right)

    @staticmethod
    def _same_stock_item(left, right) -> bool:
        return (
            left is not None
            and right is not None
            and str(left.vnum or "") == str(right.vnum or "")
            and str(left.short_description or "") == str(right.short_description or "")
        )

    @staticmethod
    def matches_name(entity, wanted: str) -> bool:
        query = str(wanted or "").strip().lower()
        if not query:
            return True
        name = str(entity.name or "").strip().lower()
        words = [word for word in name.split() if word]
        return name == query or name.startswith(query) or query in words or any(word.startswith(query) for word in words)

    @staticmethod
    def _is_item_worn(item) -> bool:
        wear_loc = GenericUtil.to_int(getattr(item, "wear_loc", -1), -1)
        return wear_loc >= 0

    @staticmethod
    def _money_value(entity) -> int:
        return (GenericUtil.to_int(entity.gold, 0) * 100) + GenericUtil.to_int(entity.silver, 0)

    @staticmethod
    def _add_money(entity, amount: int):
        total = Shop._money_value(entity) + GenericUtil.to_int(amount, 0)
        entity.gold = total // 100
        entity.silver = total - (entity.gold * 100)

    @staticmethod
    def _deduct_money(entity, amount: int):
        total = max(0, Shop._money_value(entity) - GenericUtil.to_int(amount, 0))
        entity.gold = total // 100
        entity.silver = total - (entity.gold * 100)

    @staticmethod
    def _timer_roll() -> int:
        from game.RandomNumberGenerator import RandomNumberGenerator
        return RandomNumberGenerator().number_range(50, 100)

    @staticmethod
    def _charge_adjusted_price(item, base_price: int) -> int:
        price = max(0, GenericUtil.to_int(base_price, 0))
        item_type_name = str(item.item_type or "").strip().upper()
        if item_type_name not in {"ITEM_STAFF", "ITEM_WAND"}:
            return price

        max_charges = GenericUtil.to_int(item.value1, 0)
        current_charges = GenericUtil.to_int(item.value2, 0)
        if max_charges <= 0:
            return price // 4
        return price * current_charges // max_charges

    @classmethod
    def from_json(cls, data):
        from util.GenericUtil import GenericUtil
        data = GenericUtil.camel_to_snake_case(data)
        return cls(**data)


@dataclass
class ValueQuote:
    cost: int = 0
    gold: int = 0
    silver: int = 0
    item_short: str = ""
    keeper_name: str = "The shopkeeper"
