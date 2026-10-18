import json
import unittest

from tests.test_update_handler_active_players import build_character_data
from item.Effect import Effect
from item.Item import Item
from player.Character import Character
from player.CharacterService import CharacterService
from util.ItemUtil import ItemUtil


class TestItemPersistence(unittest.TestCase):
    @staticmethod
    def _document(item_id, *, contains=None):
        return {
            "id": item_id, "areaId": "area", "vnum": "100", "name": item_id,
            "shortDescription": item_id, "longDescription": item_id, "material": "cloth",
            "itemType": "container", "extraFlags": "0", "wearFlags": "1",
            "value0": "10", "value1": "0", "value2": "0", "value3": "0", "value4": "0",
            "condition": "G", "level": 1, "weight": 1, "cost": 10, "affectData": [],
            "contains": contains if contains is not None else [],
        }

    def _nested_document(self):
        child = self._document("gem")
        child.update(itemType="treasure", timer=5, effects=[{
            "type": "spell.bless", "level": 10, "duration": 3, "bitvector": 0,
        }])
        return self._document("bag", contains=[self._document("pouch", contains=[child])])

    def _assert_contents(self, bag):
        self.assertIsInstance(bag, Item)
        self.assertEqual("bag", bag.id)
        self.assertEqual(1, len(bag.contains))
        pouch = bag.contains[0]
        self.assertIsInstance(pouch, Item)
        self.assertEqual("pouch", pouch.id)
        self.assertEqual(1, len(pouch.contains))
        gem = pouch.contains[0]
        self.assertIsInstance(gem, Item)
        self.assertEqual("gem", gem.id)
        self.assertEqual(5, gem.timer)
        self.assertIsInstance(gem.effects[0], Effect)
        self.assertEqual("spell.bless", gem.effects[0].type)

    def test_loading_nested_item_documents_preserves_contents_and_source(self):
        document = self._nested_document()
        original = json.dumps(document, sort_keys=True)
        for payload in (document, json.dumps(document)):
            with self.subTest(encoded=isinstance(payload, str)):
                self._assert_contents(Item.from_json(payload))
        self.assertEqual(original, json.dumps(document, sort_keys=True))

    def test_loading_preserves_already_hydrated_children(self):
        child = Item.from_json(self._nested_document())
        document = self._document("outer", contains=[child])
        restored = Item.from_json(document)
        self.assertIs(child, restored.contains[0])
        self._assert_contents(restored.contains[0])

    def test_missing_null_and_empty_contents_load_as_independent_empty_lists(self):
        for form in ("missing", "null", "empty"):
            with self.subTest(form=form):
                document = self._document("empty")
                if form == "missing":
                    document.pop("contains")
                elif form == "null":
                    document["contains"] = None
                first = Item.from_json(document)
                second = Item.from_json(document)
                self.assertEqual([], first.contains)
                self.assertIsNot(first.contains, second.contains)

    def test_character_inventory_and_equipment_round_trip_nested_contents(self):
        for equipped in (False, True):
            with self.subTest(equipped=equipped):
                document = build_character_data()
                bag = self._nested_document()
                if equipped:
                    document["equipped"] = {"held": bag}
                else:
                    document["inventory"] = [bag]
                character = Character.from_json(document)
                payload = CharacterService._serialize_character(character)
                restored = Character.from_json(json.loads(json.dumps(payload)))
                loaded_bag = restored.equipped.held if equipped else restored.get_items()[0]
                self._assert_contents(loaded_bag)
                self.assertEqual(payload, CharacterService._serialize_character(restored))

    def test_spawning_a_new_object_still_starts_empty(self):
        prototype = Item.from_json(self._nested_document())
        spawned = ItemUtil.create_object(prototype)
        self.assertEqual([], spawned.contains)
        self.assertNotEqual(prototype.id, spawned.id)
        self._assert_contents(prototype)

    def test_explicit_instance_cloning_still_copies_nested_contents(self):
        original = Item.from_json(self._nested_document())
        clone = ItemUtil.clone_object_instance(original)
        self.assertEqual(1, len(clone.contains))
        self.assertEqual(1, len(clone.contains[0].contains))
        self.assertNotEqual(original.id, clone.id)
        self.assertNotEqual(original.contains[0].id, clone.contains[0].id)
        clone.contains[0].contains.clear()
        self._assert_contents(original)


if __name__ == "__main__":
    unittest.main()
