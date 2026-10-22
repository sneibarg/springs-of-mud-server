"""ROM act_obj ownership and sacrifice rules through real collection guards."""
import builtins
import sys
import unittest
from enum import IntEnum
from types import SimpleNamespace as NS
from unittest.mock import patch

from tests import test_object_get_dynamic_commands as harness


RealItemApi = harness._load_module("loot_parity_item_api", "api/ItemApi.py").ItemApi
with patch.dict(sys.modules, {"item.ItemRegistry": NS(ItemRegistry=object)}):
    with patch.object(builtins, "Room", object, create=True):
        RealItemUtil = harness._load_module("loot_parity_item_util", "util/ItemUtil.py").ItemUtil


class WearFlags(IntEnum):
    ITEM_TAKE = 1
    ITEM_NO_SAC = 32768


class PlayerFlags(IntEnum):
    PLR_CANLOOT = 128


class ContainerFlags(IntEnum):
    CONT_CLOSED = 4


class TestObjectLootAndSacrificeParity(unittest.TestCase):
    def setUp(self):
        self.fixture = harness.TestObjectGetDynamicCommands()
        object_module = sys.modules[harness.Object.__module__]
        interp_module = sys.modules[harness.InterpApi.__module__]
        for module in (object_module, interp_module):
            for name, value in (("ItemApi", RealItemApi), ("ItemUtil", RealItemUtil)):
                swap = patch.object(module, name, value)
                swap.start()
                self.addCleanup(swap.stop)
        enums = {"wearFlags": WearFlags, "playerActBits": PlayerFlags,
                 "containerState": ContainerFlags}
        swap = patch.object(RealItemApi, "get_enum", side_effect=enums.__getitem__)
        swap.start()
        self.addCleanup(swap.stop)
        swap = patch.object(RealItemUtil, "can_see_object", return_value=True)
        swap.start()
        self.addCleanup(swap.stop)
        swap = patch.object(harness._CharacterApi, "is_same_group", create=True,
                            side_effect=lambda a, b: (a.leader or a) is (b.leader or b))
        swap.start()
        self.addCleanup(swap.stop)
        self.actor = self.character("Tester")
        self.owner = self.character("Owner")
        self.room = harness._Room(id="room-1", contents={}, characters={self.actor.id: self.actor})
        self.other_room = harness._Room(id="room-2", contents={}, characters={self.owner.id: self.owner})
        self.commands = self.fixture._commands(self.room)
        self.commands.wear_flags = WearFlags
        self.commands.room_registry.all_rooms = lambda: [self.room, self.other_room]
        self.commands.registry_service.character_registry = NS(
            playing={self.actor.id: self.actor, self.owner.id: self.owner},
            all_characters=lambda: [self.actor, self.owner],
        )

    def character(self, name, **kwargs):
        character = self.fixture._build_character(name=name, **kwargs)
        character.leader = None
        return character

    @staticmethod
    def item(name="gem", **kwargs):
        values = dict(id=name, area_id="area-1", vnum="1", name=name,
                      short_description=name, long_description="", material="stone",
                      item_type="treasure", extra_flags="0", wear_flags="1",
                      value0="0", value1="0", value2="0", value3="0", value4="0",
                      condition="100", level=4, weight=1, cost=12, affect_data=[], contains=[])
        values.update(kwargs)
        return harness.Item(**values)

    def run_command(self, name, raw):
        context = self.fixture._build_context(raw, self.room, self.actor, name)
        return getattr(self.commands, "do_" + name)(self.actor, context)

    def corpse(self, **kwargs):
        gem = self.item()
        corpse = self.item("corpse", item_type="pc_corpse", owner="Owner", contains=[gem], **kwargs)
        self.room.contents[corpse.id] = corpse
        return corpse, gem

    def test_unrelated_player_cannot_get_single_or_all_from_owned_corpse(self):
        for selector in ("gem", "all", "all.gem"):
            with self.subTest(selector=selector):
                corpse, gem = self.corpse()
                payload = self.run_command("get", selector + " corpse")
                self.assertEqual("You can't do that.\r\n", payload["to_char"])
                self.assertEqual([gem], corpse.contains)
                self.assertEqual([], self.actor.loot)
                self.assertNotIn("to_room", payload)

    def test_owned_container_denial_precedes_closed_and_missing_item(self):
        self.corpse(value1="4")
        payload = self.run_command("get", "missing corpse")
        self.assertEqual("You can't do that.\r\n", payload["to_char"])

    def test_take_alias_uses_ownership_guard_and_item_denial_payload(self):
        corpse, gem = self.corpse(value1="4")
        context = self.fixture._build_context("gem corpse", self.room, self.actor, "take")
        payload = self.commands.execute(self.actor, context)
        self.assertEqual("You can't do that.\r\n", payload["to_char"])
        self.assertEqual([gem], corpse.contains)
        gem.owner = "Owner"
        self.room.contents = {gem.id: gem}
        context = self.fixture._build_context("gem", self.room, self.actor, "take")
        payload = self.commands.execute(self.actor, context)
        self.assertEqual("Corpse looting is not permitted.\r\n", payload["to_char"])
        self.assertIn(gem.id, self.room.contents)

    def test_owner_immortal_group_and_permission_can_loot(self):
        for permission in ("owner", "immortal", "group", "canloot"):
            with self.subTest(permission=permission):
                self.actor.name = "Tester"
                self.actor.is_immortal = False
                self.actor.leader = None
                self.owner.status_flags.act = 0
                if permission == "owner":
                    self.actor.name = "oWnEr"
                elif permission == "immortal":
                    self.actor.is_immortal = True
                elif permission == "group":
                    self.actor.leader = self.owner
                else:
                    self.owner.status_flags.act = PlayerFlags.PLR_CANLOOT
                corpse, gem = self.corpse()
                self.run_command("get", "gem corpse")
                self.assertEqual([], corpse.contains)
                self.assertIn(gem, self.actor.loot)
                self.actor.loot.clear()

    def test_absent_owner_allows_loot_even_when_persisted_player_exists(self):
        self.other_room.characters.clear()
        self.commands.registry_service.character_registry.playing.pop(self.owner.id)
        corpse, gem = self.corpse()
        self.run_command("get", "all corpse")
        self.assertEqual([], corpse.contains)
        self.assertIn(gem, self.actor.loot)

    def test_linkdead_owner_in_other_room_remains_protected(self):
        self.commands.registry_service.character_registry.playing.pop(self.owner.id)
        corpse, gem = self.corpse()
        self.run_command("get", "all corpse")
        self.assertEqual([gem], corpse.contains)

    def test_npc_owner_canloot_bit_does_not_grant_permission(self):
        self.other_room.characters.clear()
        self.commands.registry_service.character_registry.playing.pop(self.owner.id)
        self.owner.is_npc = True
        self.owner.status_flags.act = PlayerFlags.PLR_CANLOOT
        self.other_room.mobiles[self.owner.id] = self.owner
        self.assertFalse(self.commands.can_loot(self.actor, self.item(owner="OWNER"), self.room))

    def test_item_ownership_checked_for_single_and_bulk_pickup(self):
        for selector in ("gem", "all", "all.gem"):
            with self.subTest(selector=selector):
                gem = self.item(owner="Owner")
                self.room.contents = {gem.id: gem}
                payload = self.run_command("get", selector)
                self.assertEqual("Corpse looting is not permitted.\r\n", payload["to_char"])
                self.assertIn(gem.id, self.room.contents)
                self.assertEqual([], self.actor.loot)

    def test_individual_contents_ownership_and_shared_primitive_are_protected(self):
        gem = self.item(owner="Owner")
        bag = self.item("bag", item_type="container", contains=[gem])
        self.room.contents[bag.id] = bag
        payload = self.run_command("get", "all bag")
        self.assertIn("Corpse looting is not permitted.", payload["to_char"])
        self.assertEqual([gem], bag.contains)
        corpse, gem = self.corpse()
        context = self.fixture._build_context("gem corpse", self.room, self.actor)
        payload = self.commands._get_one(self.actor, self.room, context, gem, corpse)
        self.assertEqual("You can't do that.\r\n", payload["to_char"])
        self.assertEqual([gem], corpse.contains)

    def test_unowned_items_and_npc_corpses_keep_normal_pickup(self):
        for kind in ("npc_corpse", "ITEM_CORPSE_NPC", "container"):
            with self.subTest(kind=kind):
                gem = self.item()
                bag = self.item("bag", item_type=kind, contains=[gem])
                self.room.contents = {bag.id: bag}
                self.run_command("get", "all bag")
                self.assertIn(gem, self.actor.loot)
                self.actor.loot.clear()

    def test_loaded_pc_corpse_cannot_be_sacrificed_but_empty_one_can(self):
        for kind in ("pc_corpse", "ITEM_CORPSE_PC", "corpse_pc"):
            with self.subTest(kind=kind):
                corpse = self.item("corpse", item_type=kind, contains=[self.item()])
                self.room.contents = {corpse.id: corpse}
                silver = self.actor.silver
                payload = self.run_command("sacrifice", "corpse")
                self.assertEqual("Mota wouldn't like that.\r\n", payload["to_char"])
                self.assertIn(corpse.id, self.room.contents)
                self.assertEqual(silver, self.actor.silver)
                corpse.contains.clear()
                self.run_command("sacrifice", "corpse")
                self.assertNotIn(corpse.id, self.room.contents)
                self.assertGreater(self.actor.silver, silver)

    def test_take_and_no_sac_wear_flags_protect_sacrifices(self):
        for flags in ("0", "32769", "A" + "P"):
            with self.subTest(flags=flags):
                item = self.item("idol", wear_flags=flags)
                self.room.contents = {item.id: item}
                payload = self.run_command("sacrifice", "idol")
                self.assertEqual("idol is not an acceptable sacrifice.\r\n", payload["to_char"])
                self.assertIn(item.id, self.room.contents)
                self.assertEqual(0, self.actor.silver)

    def test_occupied_objects_by_player_or_npc_cannot_be_sacrificed(self):
        for npc in (False, True):
            with self.subTest(npc=npc):
                chair = self.item("chair", item_type="furniture")
                occupant = self.character("Sitter", is_npc=npc)
                occupant.on = chair
                collection = self.room.mobiles if npc else self.room.characters
                collection[occupant.id] = occupant
                self.room.contents = {chair.id: chair}
                payload = self.run_command("sacrifice", "chair")
                self.assertEqual("Sitter appears to be using chair.\r\n", payload["to_char"])
                self.assertIn(chair.id, self.room.contents)
                self.assertEqual(0, self.actor.silver)
                collection.pop(occupant.id)

    def test_unoccupied_takeable_object_can_be_sacrificed(self):
        chair = self.item("chair", item_type="furniture")
        self.room.contents[chair.id] = chair
        payload = self.run_command("sacrifice", "chair")
        self.assertNotIn(chair.id, self.room.contents)
        self.assertEqual(12, self.actor.silver)
        self.assertEqual("Tester sacrifices chair to Mota.\r\n", payload["to_room"])


if __name__ == "__main__":
    unittest.main()
