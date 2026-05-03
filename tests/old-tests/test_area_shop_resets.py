import sys
import types
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

SRC_ROOT = Path(__file__).resolve().parents[2] / "src"

for package_name in ("area", "fight", "game", "interp", "mobile", "object", "player", "util"):
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

if "server.messaging" not in sys.modules:
    messaging = types.ModuleType("server.messaging")
    messaging.__path__ = [str(SRC_ROOT / "server" / "messaging")]
    sys.modules["server.messaging"] = messaging

from area.AreaHandler import AreaHandler
from area.Reset import Reset


class TestAreaShopResets(unittest.TestCase):
    def _build_handler(self, *, shop_lookup):
        room = SimpleNamespace(id="room1", area_id="area1", mobiles={})
        room.add_mobile_to_room = lambda mob: room.mobiles.__setitem__(mob.id, mob)

        room_registry = Mock()
        room_registry.get.return_value = room
        room_registry.get_or_none.return_value = room
        room_registry.all_rooms.return_value = [room]

        mobile_registry = Mock()
        item_registry = Mock()
        shop_registry = SimpleNamespace(find_by_keeper_vnum=shop_lookup)

        handler = AreaHandler(
            message_bus=Mock(),
            area_registry=Mock(),
            room_registry=room_registry,
            item_registry=item_registry,
            mobile_registry=mobile_registry,
            shop_registry=shop_registry,
        )
        handler.set_enums(
            {
                "wellKnownRoomVnums": SimpleNamespace(ROOM_VNUM_SCHOOL=SimpleNamespace(value=3001)),
                "exitFlags": SimpleNamespace(),
                "itemFlags": SimpleNamespace(ITEM_INVENTORY=SimpleNamespace(value=1 << 5)),
            }
        )
        return handler, room, mobile_registry, item_registry

    @staticmethod
    def _build_area_with_g_reset():
        return SimpleNamespace(
            number_of_players=0,
            resets=[
                Reset(id="r1", area_id="area1", command="M", arg1="100", arg2="1", arg3="3001", arg4="1", comment="keeper"),
                Reset(id="r2", area_id="area1", command="G", arg1="200", arg2="10", arg3="0", arg4="0", comment="stock"),
            ],
        )

    def test_shopkeeper_g_reset_creates_inventory_stock(self):
        handler, room, mobile_registry, item_registry = self._build_handler(
            shop_lookup=lambda keeper_vnum: object() if str(keeper_vnum) == "100" else None
        )
        mob_template = SimpleNamespace(vnum="100", specials=[])
        mobile_registry.get.return_value = mob_template
        item_registry.get.return_value = SimpleNamespace(vnum="200")
        live_mob = SimpleNamespace(id="mob1", vnum="100", inventory=[])
        created_item = SimpleNamespace(extra_flags=0)

        with patch("area.AreaHandler.MobileUtil.create_mobile", return_value=live_mob), \
             patch("area.AreaHandler.ItemUtil.create_object", return_value=created_item):
            handler._reset_area(self._build_area_with_g_reset())

        self.assertEqual([created_item], live_mob.inventory)
        self.assertEqual(1 << 5, created_item.extra_flags)
        self.assertIn("mob1", room.mobiles)

    def test_non_shopkeeper_g_reset_adds_normal_inventory_item(self):
        handler, _room, mobile_registry, item_registry = self._build_handler(
            shop_lookup=lambda _keeper_vnum: None
        )
        mob_template = SimpleNamespace(vnum="101", specials=[])
        mobile_registry.get.return_value = mob_template
        item_registry.get.return_value = SimpleNamespace(vnum="200")
        live_mob = SimpleNamespace(id="mob2", vnum="101", inventory=[])
        created_item = SimpleNamespace(extra_flags=0)

        with patch("area.AreaHandler.MobileUtil.create_mobile", return_value=live_mob), \
             patch("area.AreaHandler.ItemUtil.create_object", return_value=created_item):
            handler._reset_area(self._build_area_with_g_reset())

        self.assertEqual([created_item], live_mob.inventory)
        self.assertEqual(0, created_item.extra_flags)


if __name__ == "__main__":
    unittest.main()
