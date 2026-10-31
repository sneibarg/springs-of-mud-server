"""ROM get_obj_here semantics for offensive character/object spells."""
import unittest

from tests.test_movement_rules_parity import MovementFixture, item
from tests.test_review_application_fixes import ROOT
from api.ItemApi import ItemApi
from devtools.collection_query import load_collections
from interp.commands.Fight import Fight
from skill.Spell import Spell


class SpellObjectTargetingTests(MovementFixture, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        documents = load_collections(ROOT / 'resources/collections', ['spells'])['spells'].documents
        cls.spells = [Spell.from_json(doc) for doc in documents if doc['name'] in ('curse', 'poison')]

    def setUp(self):
        super().setUp()
        self.commands = Fight.__new__(Fight)

    def resolve(self, spell, selector):
        return self.commands._resolve_spell_target(self.actor, self.room, spell, selector)

    def test_invisible_floor_object_is_rejected(self):
        hidden = item('secretblade', itemType='weapon',
                      extraFlags=int(self.enums.get('itemFlags').ITEM_INVIS))
        self.room.contents[hidden.id] = hidden
        self.assertFalse(ItemApi.can_see_object(self.room, self.actor, hidden))
        for spell in self.spells:
            with self.subTest(spell=spell.name):
                self.assertEqual((None, '', 'target_not_visible'), self.resolve(spell, 'secretblade'))

    def test_visible_equipped_object_is_selected(self):
        weapon = item('steelblade', itemType='weapon')
        self.actor.equip_item(weapon, 'wielded')
        for spell in self.spells:
            with self.subTest(spell=spell.name):
                self.assertEqual((weapon, 'obj', ''), self.resolve(spell, 'steelblade'))

    def test_visible_ordinals_restart_for_floor_inventory_and_equipment(self):
        hidden = item('blade hidden', extraFlags=int(self.enums.get('itemFlags').ITEM_INVIS))
        floor = item('blade floor')
        carried = item('blade carried')
        worn = item('blade worn')
        self.room.contents = {hidden.id: hidden, floor.id: floor}
        self.actor.loot.append(carried)
        self.actor.equip_item(worn, 'wielded')
        for spell in self.spells:
            with self.subTest(spell=spell.name):
                self.assertEqual((floor, 'obj', ''), self.resolve(spell, 'blade'))
                # One visible floor/inventory match: 2.blade resolves nowhere.
                self.assertEqual((None, '', 'target_not_visible'), self.resolve(spell, '2.blade'))
        self.room.contents.clear()
        for spell in self.spells:
            self.assertEqual((carried, 'obj', ''), self.resolve(spell, 'blade'))
        self.actor.loot.remove(carried)
        for spell in self.spells:
            self.assertEqual((worn, 'obj', ''), self.resolve(spell, 'blade'))


if __name__ == '__main__':
    unittest.main()
