"""Visible keyword/ordinal selection and ROM object location precedence."""
import sys
import unittest
from types import SimpleNamespace as NS
from unittest.mock import patch
from tests import test_object_shop_equipment_parity as equipment
from tests.test_object_carry_limits_parity import Entity
from util.LookupUtil import LookupUtil

h = equipment.h
stubs = {name: NS(**{attr: object}) for name, attr in (
    ("util.AreaUtil", "AreaUtil"), ("area.Exit", "Exit"), ("mobile.Mobile", "Mobile"),
    ("item.ExtraDescriptionData", "ExtraDescriptionData"))}
with patch.dict(sys.modules, stubs):
    Room = h._load_module("lookup_room", "area/Room.py").Room


class TestObjectLookupParity(unittest.TestCase):
    def setUp(self):
        self.base = equipment.TestShopEquipmentParity()
        self.base.setUp()
        self.addCleanup(self.base.doCleanups)
        self.actor, self.room, self.commands = self.base.actor, self.base.room, self.base.commands
        self.swap = self.base.swap
        self.swap(sys.modules["util.ItemUtil"], "ItemUtil", new=equipment.RealItemUtil)
        self.swap(equipment.ObjectModule.CharacterApi, "can_see", create=True,
                  side_effect=lambda viewer, target, room=None: not getattr(target, "hidden", False))
        self.room.contents = {}

    def item(self, name, **kw):
        return self.base.item(name, **kw)

    def hidden(self, name):
        return self.item(name, extra_flags=str(self.base.enums["itemFlags"].ITEM_INVIS.value))

    def ctx(self, name, raw):
        return self.base.base.base.fixture._build_context(raw, self.room, self.actor, name)

    def test_room_get_keywords_ordinals_and_visibility_count_only_visible_matches(self):
        hidden, first, second = self.hidden("sword long steel"), self.item("sword short steel"), self.item("sword broad steel")
        self.room.contents = {str(i): obj for i, obj in enumerate((hidden, first, second))}
        ctx = self.ctx("get", "2.ste")
        self.commands.do_get(self.actor, ctx)
        self.assertIn(second, self.actor.loot)
        self.assertNotIn(hidden, self.actor.loot)
        self.assertNotIn(first, self.actor.loot)
        self.assertIsNone(self.commands._room_item(self.actor, self.room, "long"))

    def test_multiword_keyword_matching_requires_all_words(self):
        first, second = self.item("sword long steel"), self.item("sword long bronze")
        self.assertIs(first, LookupUtil.find([first, second], "ste lo"))
        self.assertIsNone(LookupUtil.find([first, second], "steel bronze"))
        self.assertIsNone(LookupUtil.find([first], "0.sword"))

    def test_here_searches_room_then_inventory_then_equipment_and_restarts_ordinal_per_location(self):
        floor, carried, worn = self.item("bag floor"), self.item("bag carried"), self.item("bag worn")
        self.room.contents[floor.id] = floor
        self.actor.loot.extend([carried, worn])
        self.actor.equip_item(worn, "held")
        self.assertIs(floor, self.commands._here_item(self.actor, self.room, "bag"))
        self.room.contents.clear()
        self.assertIs(carried, self.commands._here_item(self.actor, self.room, "bag"))
        self.actor.loot.remove(carried)
        self.assertIs(worn, self.commands._here_item(self.actor, self.room, "bag"))
        self.assertIsNone(self.commands._inventory_item(self.actor, self.room, "worn"))

    def test_get_selects_worn_container_and_visible_contained_keyword_ordinal(self):
        gem1, gem2 = self.item("gem red"), self.item("gem blue")
        bag = self.base.base.base.bag(contains=[gem1, gem2])
        self.actor.loot.append(bag)
        self.actor.equip_item(bag, "held")
        self.commands.do_get(self.actor, self.ctx("get", "2.gem bag"))
        self.assertIn(gem2, self.actor.loot)
        self.assertEqual([gem1], bag.contains)

    def test_put_uses_room_container_before_duplicate_carried_container(self):
        floor = self.base.base.base.bag()
        carried = self.base.base.base.bag()
        floor.id, carried.id = "floor", "carried"
        gem = self.item("gem steel")
        self.room.contents[floor.id] = floor
        self.actor.loot.extend([carried, gem])
        self.commands.do_put(self.actor, self.ctx("put", "ste bag"))
        self.assertIn(gem, floor.contains)
        self.assertEqual([], carried.contains)

    def test_drop_all_and_wear_all_skip_invisible_items(self):
        hidden = self.hidden("ring silver")
        visible = self.item("ring gold")
        self.actor.loot.extend([hidden, visible])
        self.commands.do_drop(self.actor, self.ctx("drop", "all.ri"))
        self.assertIn(hidden, self.actor.loot)
        self.assertIn(visible, self.room.contents.values())
        hidden.wear_flags = str(self.base.enums["wearFlags"].ITEM_WEAR_FINGER.value)
        self.commands.do_wear(self.actor, self.ctx("wear", "all"))
        self.assertIn(hidden, self.actor.loot)
        self.assertIsNone(self.actor.equipped.finger1)

    def test_inventory_single_drop_and_remove_use_keywords_ordinals_and_visibility(self):
        first, second = self.item("ring silver"), self.item("ring gold")
        self.actor.loot.extend([first, second])
        self.commands.do_drop(self.actor, self.ctx("drop", "2.ring"))
        self.assertIn(first, self.actor.loot)
        self.assertIn(second, self.room.contents.values())
        self.actor.equip_item(first, "finger1")
        self.commands.do_remove(self.actor, self.ctx("remove", "sil"))
        self.assertIsNone(self.actor.equipped.finger1)
        self.assertIn(first, self.actor.loot)

    def test_give_and_steal_character_selectors_skip_hidden_and_count_pc_npc_together(self):
        hidden = NS(id="hidden", name="guard hidden", hidden=True)
        player = self.base.base.base.fixture._build_character(name="guard red")
        player.id = "player"
        npc = self.base.base.base.fixture._build_character(name="guard blue")
        npc.id, npc.is_npc = "npc", True
        self.room.characters = {hidden.id: hidden, player.id: player}
        self.room.mobiles = {npc.id: npc}
        self.assertIs(npc, self.commands._find_give_target(self.room, "2.gu", self.actor))
        self.assertIs(npc, Room.find_visible_target(self.room, self.actor, "2.gu"))
        self.assertIs(player, self.commands._find_give_target(self.room, "red", self.actor))
        self.assertIs(self.actor, self.commands._find_give_target(self.room, "self", self.actor))
        ctx = self.ctx("steal", "sword 2.gu")
        self.commands._prepare_steal_context(self.actor, ctx)
        self.assertIs(npc, ctx.steal_victim)

    def test_steal_inventory_visibility_uses_thief_rather_than_owner(self):
        victim = self.base.base.base.fixture._build_character(name="Victim")
        victim.id = "victim"
        self.room.characters[victim.id] = victim
        item = self.hidden("sword steel")
        victim.loot.append(item)
        victim.status_flags.affected_by = self.base.enums["affectedBy"].AFF_DETECT_INVIS.value
        ctx = self.ctx("steal", "steel Victim")
        self.commands._prepare_steal_context(self.actor, ctx)
        self.commands._prepare_steal_item_context(self.actor, ctx)
        self.assertIsNone(ctx.steal_item)

    def test_domain_lookup_methods_share_keyword_ordinal_and_visibility_behavior(self):
        hidden, first, second = self.hidden("gem red"), self.item("gem red"), self.item("gem blue")
        self.actor.loot.extend([hidden, first, second])
        self.assertIs(second, Entity.find_inventory_item(self.actor, "2.gem", room=self.room))
        bag = self.base.base.base.bag(contains=[hidden, first, second])
        self.assertIs(second, bag.find_contained_item("2.gem", observer=self.actor, room=self.room))
        self.room.contents = {str(i): obj for i, obj in enumerate((hidden, first, second))}
        self.assertIs(second, Room.find_room_item(self.room, "2.gem", observer=self.actor))
        self.actor.equip_item(second, "held")
        self.assertIs(second, Entity.find_owned_item(self.actor, "blue", room=self.room))


if __name__ == "__main__":
    unittest.main()
