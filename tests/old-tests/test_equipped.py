import sys
import types
import unittest
from pathlib import Path
from types import SimpleNamespace

SRC_ROOT = Path(__file__).resolve().parents[1] / "src"

for package_name in ("game", "object"):
    if package_name not in sys.modules:
        package = types.ModuleType(package_name)
        package.__path__ = [str(SRC_ROOT / package_name)]
        sys.modules[package_name] = package

if "server" not in sys.modules:
    server = types.ModuleType("server")
    server.__path__ = []
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

if "object.ObjectMacros" not in sys.modules:
    object_macros = types.ModuleType("object.ObjectMacros")

    class ObjectMacros:
        @staticmethod
        def flags_to_int(value):
            return int(value or 0)

    object_macros.ObjectMacros = ObjectMacros
    sys.modules["object.ObjectMacros"] = object_macros

from game.Equipped import Equipped


class WearFlags:
    ITEM_HOLD = SimpleNamespace(value=1 << 0)
    ITEM_WEAR_FINGER = SimpleNamespace(value=1 << 1)


class TestEquipped(unittest.TestCase):
    def test_equip_item_moves_item_out_of_inventory_and_sets_wear_loc(self):
        item = SimpleNamespace(id="item1", name="sword")
        character = SimpleNamespace(loot=[item], equipped=Equipped())

        Equipped.equip_item(character, item, "wielded")

        self.assertNotIn(item, character.loot)
        self.assertIs(character.equipped.wielded, item)
        self.assertEqual("wielded", item.wear_location)
        self.assertEqual(16, item.wear_loc)

    def test_unequip_item_returns_item_to_inventory_and_clears_wear_loc(self):
        item = SimpleNamespace(id="item1", name="sword", wear_location="wielded", wear_loc=16)
        character = SimpleNamespace(loot=[], equipped=Equipped(wielded=item))

        returned = Equipped.unequip_item(character, "wielded")

        self.assertIs(returned, item)
        self.assertIn(item, character.loot)
        self.assertIsNone(character.equipped.wielded)
        self.assertEqual("", item.wear_location)
        self.assertEqual(-1, item.wear_loc)

    def test_equip_item_uses_character_remove_item_hook_when_available(self):
        item = SimpleNamespace(id="item1", name="sword")
        removed = []
        character = SimpleNamespace(
            loot=[item],
            equipped=Equipped(),
            remove_item=lambda value: removed.append(value),
        )

        Equipped.equip_item(character, item, "wielded")

        self.assertEqual([item], removed)
        self.assertIs(character.equipped.wielded, item)

    def test_unequip_item_uses_character_add_item_hook_when_available(self):
        item = SimpleNamespace(id="item1", name="sword", wear_location="wielded", wear_loc=16)
        added = []
        character = SimpleNamespace(
            loot=[],
            equipped=Equipped(wielded=item),
            add_item=lambda value: added.append(value),
        )

        returned = Equipped.unequip_item(character, "wielded")

        self.assertIs(returned, item)
        self.assertEqual([item], added)
        self.assertIsNone(character.equipped.wielded)

    def test_wear_slot_groups_for_light_maps_hold_request_to_light_slot(self):
        item = SimpleNamespace(item_type="light", wear_flags=WearFlags.ITEM_HOLD.value, short_description="a lamp")

        groups = Equipped.wear_slot_groups_for_item(item, WearFlags, preferred_slot="held")

        self.assertEqual([("light",)], groups)

    def test_resolve_wear_slot_returns_empty_slot_without_replacement(self):
        equipped = Equipped()

        slot, payload = equipped.resolve_wear_slot(
            SimpleNamespace(name="Tester"),
            ("finger1", "finger2"),
            replace=False,
            can_remove_item=lambda _item: True,
            remove_item=lambda *_args: None,
        )

        self.assertEqual("finger1", slot)
        self.assertEqual({}, payload)

    def test_resolve_wear_slot_rejects_nonremovable_item(self):
        equipped = Equipped(finger1=SimpleNamespace(short_description="a ring"))

        slot, payload = equipped.resolve_wear_slot(
            SimpleNamespace(name="Tester"),
            ("finger1",),
            replace=True,
            can_remove_item=lambda _item: False,
            remove_item=lambda *_args: None,
        )

        self.assertIsNone(slot)
        self.assertEqual("You can't remove a ring.\r\n", payload["to_char"])

    def test_resolve_wear_slot_removes_existing_item_when_replacing(self):
        removed = []
        equipped = Equipped(finger1=SimpleNamespace(short_description="a ring"))

        def remove_item(character, slot, item):
            removed.append((character.name, slot, item.short_description))
            setattr(equipped, slot, None)

        slot, payload = equipped.resolve_wear_slot(
            SimpleNamespace(name="Tester"),
            ("finger1",),
            replace=True,
            can_remove_item=lambda _item: True,
            remove_item=remove_item,
        )

        self.assertEqual("finger1", slot)
        self.assertEqual([("Tester", "finger1", "a ring")], removed)
        self.assertEqual("You stop using a ring.\r\n", payload["to_char"])
        self.assertEqual("Tester stops using a ring.\r\n", payload["to_room"])

    def test_slot_wear_payload_uses_slot_specific_message(self):
        room = SimpleNamespace(player_targets=lambda _character: [SimpleNamespace(id="char2")])
        payload = Equipped.slot_wear_payload(
            SimpleNamespace(id="char1", name="Tester"),
            room,
            SimpleNamespace(short_description="a shield"),
            "shield",
        )

        self.assertEqual("You wear a shield as a shield.\r\n", payload["to_char"])
        self.assertEqual("Tester wears a shield as a shield.\r\n", payload["to_room"])
        self.assertEqual(["char2"], [target.id for target in payload["targets"]])
