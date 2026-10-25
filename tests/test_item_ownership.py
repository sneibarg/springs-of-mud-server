import sys
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from item.ItemOwnership import ItemOwnership
from tests.test_acid_exposure import Effect, EffectHandler, ENUMS


class TestItemOwnership(unittest.TestCase):
    def test_expiration_reverses_worn_effects_for_both_entity_locations(self):
        # Exercise expiration's production removal boundary with real effects.
        from tests.test_update_handler_active_players import ItemUpdateHandler

        for kind, inventory in (("char_equipped", "loot"), ("mob_equipped", "inventory")):
            with self.subTest(kind=kind):
                effects = EffectHandler(NS(get=ENUMS.get))
                owner = NS(equipped=NS(shield=None), effects=[],
                           character_attributes=NS(strength=10), status_flags=NS(affected_by=0))
                setattr(owner, inventory, [])
                item = NS(id="shield", wear_location="shield", wear_loc=11, effects=[
                    Effect(where="TO_AFFECTS", location="APPLY_STR", modifier=3, duration=-1)])
                owner.equipped.shield = item
                effects.apply_item_effects(owner, item)
                self.assertEqual(13, owner.character_attributes.strength)
                handler = ItemUpdateHandler.__new__(ItemUpdateHandler)
                handler.room_registry = None
                handler.effect_update_handler = NS(effect_handler=effects)
                handler._remove_item_at_location(item, kind, owner, None)
                self.assertEqual(10, owner.character_attributes.strength)
                self.assertEqual([], owner.effects)
                self.assertIsNone(owner.equipped.shield)
                self.assertIsNone(item._effect_wearer)
                self.assertEqual(("", -1), (item.wear_location, item.wear_loc))
                self.assertEqual([], getattr(owner, inventory))

    def test_aliases_are_removed_by_identity_and_cleanup_runs_once(self):
        item, other = NS(id="same"), NS(id="same")
        owner = NS(equipped=NS(shield=item, held=item), loot=[item, item, other])
        effects = Mock()
        service = ItemOwnership(effects)
        service.detach_carried(owner, item)
        service.detach_carried(owner, item)
        effects.remove_item_effects.assert_called_once_with(owner, item)
        self.assertEqual([other], owner.loot)
        self.assertTrue(all(value is None for value in vars(owner.equipped).values()))

    def test_nested_detachment_preserves_equal_but_distinct_items(self):
        item, other = NS(id="same"), NS(id="same")
        container = NS(contains=[item, other])
        ItemOwnership(Mock()).detach(item, {"kind": "item_contains", "parent": container,
                                            "container": container.contains})
        self.assertEqual(1, len(container.contains))
        self.assertIs(other, container.contains[0])
