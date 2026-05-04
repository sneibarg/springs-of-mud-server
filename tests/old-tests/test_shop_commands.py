import sys
import types
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

SRC_ROOT = Path(__file__).resolve().parents[2] / "src"

for package_name in ("area", "fight", "game", "interp", "mobile", "item", "player", "util"):
    if package_name not in sys.modules:
        package = types.ModuleType(package_name)
        package.__path__ = [str(SRC_ROOT / package_name)]
        sys.modules[package_name] = package

if "registries" not in sys.modules:
    registries = types.ModuleType("registries")

    class Registry:
        def __class_getitem__(cls, _item):
            return cls

    registries.Registry = Registry
    sys.modules["registries"] = registries

if "injector" not in sys.modules:
    injector = types.ModuleType("injector")

    def inject(target):
        return target

    injector.inject = inject
    sys.modules["injector"] = injector

if "server" not in sys.modules:
    server = types.ModuleType("server")
    server.__path__ = [str(SRC_ROOT / "server")]
    sys.modules["server"] = server

if "server.LoggerFactory" not in sys.modules:
    logger_factory = types.ModuleType("server.LoggerFactory")

    class _Logger:
        def info(self, *_args, **_kwargs):
            return None

        def debug(self, *_args, **_kwargs):
            return None

        def warning(self, *_args, **_kwargs):
            return None

        def error(self, *_args, **_kwargs):
            return None

    class LoggerFactory:
        @staticmethod
        def get_logger(_name):
            return _Logger()

    logger_factory.LoggerFactory = LoggerFactory
    sys.modules["server.LoggerFactory"] = logger_factory

from area.Shop import Shop
from game.Equipped import Equipped
from interp.commands.ObjectCommands import ObjectCommands


class TestShopCommands(unittest.TestCase):
    INVENTORY_BIT = 1 << 0
    HAD_TIMER_BIT = 1 << 1
    SELL_EXTRACT_BIT = 1 << 2
    PET_SHOP_BIT = 1 << 3
    ITEM_WEAPON = 5

    def _build_commands(self, room, shop, hour=12):
        room_registry = Mock()
        room_registry.get_or_none.return_value = room
        shop_registry = SimpleNamespace(
            find_by_keeper_vnum=lambda keeper_vnum: shop if str(keeper_vnum) == str(shop.keeper) else None
        )
        registry_service = SimpleNamespace(
            room_registry=room_registry,
            mobile_registry=Mock(),
            shop_registry=shop_registry,
        )
        player_helper = Mock()
        player_helper.players_in_room.return_value = []
        commands = ObjectCommands(
            registry_service=registry_service,
            player_helper=player_helper,
            weather_handler=SimpleNamespace(time_info=SimpleNamespace(hour=hour)),
            room_helper=None,
        )
        commands.item_types = SimpleNamespace(ITEM_WEAPON=SimpleNamespace(value=self.ITEM_WEAPON))
        commands.item_flags = SimpleNamespace(
            ITEM_INVENTORY=SimpleNamespace(value=self.INVENTORY_BIT),
            ITEM_HAD_TIMER=SimpleNamespace(value=self.HAD_TIMER_BIT),
            ITEM_SELL_EXTRACT=SimpleNamespace(value=self.SELL_EXTRACT_BIT),
        )
        commands.wear_flags = SimpleNamespace()
        commands.room_flags = SimpleNamespace(ROOM_PET_SHOP=SimpleNamespace(value=self.PET_SHOP_BIT))
        commands.act_bits = SimpleNamespace()
        commands.affected_bits = SimpleNamespace()
        commands.comm_flags = SimpleNamespace()
        return commands

    @staticmethod
    def _build_character(gold=0, silver=0, item=None):
        loot = [] if item is None else [item]
        character = SimpleNamespace(
            id="char1",
            name="Tester",
            level=20,
            room_id="room1",
            gold=gold,
            silver=silver,
            loot=loot,
            equipped=Equipped(),
            character_attributes=SimpleNamespace(max_items=30, max_weight=500),
        )
        character.add_item = lambda added: character.loot.append(added)
        character.remove_item = lambda removed: character.loot.remove(removed)
        character.equipped_slot_of = lambda wanted: None
        character.ensure_equipped = lambda: character.equipped
        return character

    @staticmethod
    def _build_item(item_id, name, short_description, *, vnum, cost, level=1, weight=1, extra_flags=0,
                    item_type="ITEM_WEAPON", timer=0):
        return SimpleNamespace(
            id=item_id,
            vnum=str(vnum),
            name=name,
            short_description=short_description,
            item_type=item_type,
            level=level,
            cost=cost,
            weight=weight,
            extra_flags=extra_flags,
            timer=timer,
        )

    def test_list_groups_shop_stock_and_marks_inventory_rows(self):
        shop = Shop(
            id="shop1",
            area_id="area1",
            comment="",
            keeper=100,
            buy_type0=self.ITEM_WEAPON,
            buy_type1=0,
            buy_type2=0,
            buy_type3=0,
            buy_type4=0,
            profit_buy=120,
            profit_sell=50,
            open_hour=0,
            close_hour=23,
        )
        potion = self._build_item(
            "obj1", "potion healing", "a healing potion",
            vnum=200, cost=100, level=5, extra_flags=self.INVENTORY_BIT, item_type="ITEM_WEAPON"
        )
        sword1 = self._build_item("obj2", "sword steel", "a steel sword", vnum=201, cost=80, level=7)
        sword2 = self._build_item("obj3", "sword steel", "a steel sword", vnum=201, cost=80, level=7)
        keeper = SimpleNamespace(vnum="100", inventory=[potion, sword1, sword2], short_description="the shopkeeper")
        room = SimpleNamespace(id="room1", vnum="3001", room_flags=0, mobiles={"keeper": keeper})
        commands = self._build_commands(room, shop)
        context = SimpleNamespace(result="", parameters=[], finish=Mock())

        payload = commands.do_list(self._build_character(), context)

        self.assertIn("[Lv Price Qty] Item\r\n", payload["to_char"])
        self.assertIn("[ 5   120 -- ] a healing potion\r\n", payload["to_char"])
        self.assertIn("[ 7    96  2 ] a steel sword\r\n", payload["to_char"])

    def test_buy_moves_stock_to_character_and_updates_money(self):
        shop = Shop(
            id="shop1",
            area_id="area1",
            comment="",
            keeper=100,
            buy_type0=self.ITEM_WEAPON,
            buy_type1=0,
            buy_type2=0,
            buy_type3=0,
            buy_type4=0,
            profit_buy=120,
            profit_sell=50,
            open_hour=0,
            close_hour=23,
        )
        sword1 = self._build_item("obj2", "sword steel", "a steel sword", vnum=201, cost=80, level=7)
        sword2 = self._build_item("obj3", "sword steel", "a steel sword", vnum=201, cost=80, level=7)
        keeper = SimpleNamespace(vnum="100", inventory=[sword1, sword2], short_description="the shopkeeper", gold=0, silver=0)
        room = SimpleNamespace(id="room1", vnum="3001", room_flags=0, mobiles={"keeper": keeper})
        commands = self._build_commands(room, shop)
        character = self._build_character(gold=5, silver=0)
        context = SimpleNamespace(result="2*sword", parameters=[], finish=Mock())

        payload = commands.do_buy(character, context)

        self.assertEqual(2, len(character.loot))
        self.assertEqual([], keeper.inventory)
        self.assertEqual(3, character.gold)
        self.assertEqual(8, character.silver)
        self.assertEqual(1, keeper.gold)
        self.assertEqual(92, keeper.silver)
        self.assertEqual("You buy a steel sword[2] for 192 silver.\r\n", payload["to_char"])

    def test_value_and_sell_use_shop_profit_and_stock_the_item(self):
        shop = Shop(
            id="shop1",
            area_id="area1",
            comment="",
            keeper=100,
            buy_type0=self.ITEM_WEAPON,
            buy_type1=0,
            buy_type2=0,
            buy_type3=0,
            buy_type4=0,
            profit_buy=200,
            profit_sell=50,
            open_hour=0,
            close_hour=23,
        )
        weapon = self._build_item("obj4", "blade iron", "an iron blade", vnum=202, cost=100, level=5)
        keeper = SimpleNamespace(vnum="100", inventory=[], short_description="the shopkeeper", gold=1, silver=0)
        room = SimpleNamespace(id="room1", vnum="3001", room_flags=0, mobiles={"keeper": keeper})
        commands = self._build_commands(room, shop)
        character = self._build_character(item=weapon)

        value_payload = commands.do_value(character, SimpleNamespace(result="blade", parameters=[], finish=Mock()))
        sell_payload = commands.do_sell(character, SimpleNamespace(result="blade", parameters=[], finish=Mock()))

        self.assertEqual("I'll give you 50 silver and 0 gold coins for an iron blade.\r\n", value_payload["to_char"])
        self.assertEqual([], character.loot)
        self.assertEqual([weapon], keeper.inventory)
        self.assertEqual(0, keeper.gold)
        self.assertEqual(50, keeper.silver)
        self.assertEqual(0, character.gold)
        self.assertEqual(50, character.silver)
        self.assertGreaterEqual(weapon.timer, 50)
        self.assertLessEqual(weapon.timer, 100)
        self.assertEqual("You sell an iron blade for 50 silver and 0 gold pieces.\r\n", sell_payload["to_char"])

    def test_selling_new_item_prepends_to_keeper_inventory(self):
        shop = Shop(
            id="shop1",
            area_id="area1",
            comment="",
            keeper=100,
            buy_type0=self.ITEM_WEAPON,
            buy_type1=0,
            buy_type2=0,
            buy_type3=0,
            buy_type4=0,
            profit_buy=120,
            profit_sell=50,
            open_hour=0,
            close_hour=23,
        )
        existing = self._build_item("obj1", "axe bronze", "a bronze axe", vnum=210, cost=100)
        sold = self._build_item("obj2", "blade iron", "an iron blade", vnum=202, cost=100)
        keeper = SimpleNamespace(vnum="100", inventory=[existing], short_description="the shopkeeper", gold=1, silver=0)
        room = SimpleNamespace(id="room1", vnum="3001", room_flags=0, mobiles={"keeper": keeper})
        commands = self._build_commands(room, shop)
        character = self._build_character(item=sold)

        commands.do_sell(character, SimpleNamespace(result="blade", parameters=[], finish=Mock()))

        self.assertEqual([sold, existing], keeper.inventory)

    def test_selling_duplicate_to_inventory_stock_does_not_add_second_entry(self):
        shop = Shop(
            id="shop1",
            area_id="area1",
            comment="",
            keeper=100,
            buy_type0=self.ITEM_WEAPON,
            buy_type1=0,
            buy_type2=0,
            buy_type3=0,
            buy_type4=0,
            profit_buy=120,
            profit_sell=50,
            open_hour=0,
            close_hour=23,
        )
        stocked = self._build_item(
            "obj1", "blade iron", "an iron blade",
            vnum=202, cost=100, extra_flags=self.INVENTORY_BIT
        )
        sold = self._build_item("obj2", "blade iron", "an iron blade", vnum=202, cost=100)
        keeper = SimpleNamespace(vnum="100", inventory=[stocked], short_description="the shopkeeper", gold=1, silver=0)
        room = SimpleNamespace(id="room1", vnum="3001", room_flags=0, mobiles={"keeper": keeper})
        commands = self._build_commands(room, shop)
        character = self._build_character(item=sold)

        commands.do_sell(character, SimpleNamespace(result="blade", parameters=[], finish=Mock()))

        self.assertEqual([stocked], keeper.inventory)


if __name__ == "__main__":
    unittest.main()
