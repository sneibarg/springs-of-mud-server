import unittest
from enum import IntEnum
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch

from tests import test_runtime_factories as runtime
from tests.test_update_handler_active_players import build_character_data
from api.CharacterApi import CharacterApi
from api.SpellApi import SpellApi
from area.Shop import Shop
from item.Effect import Effect
from item.Item import Item
from player.Character import Character
from util.EffectUtil import EffectUtil


class EffectOwnershipTests(unittest.TestCase):
    def test_effect_evaluates_its_own_numeric_fields_and_defaults(self):
        effect = Effect(level='level + 1', duration='level / 4', modifier='-2 * level')
        effect.evaluate_expressions(20, EffectUtil.safe_eval_int)
        self.assertEqual((21, 5, -40), (effect.level, effect.duration, effect.modifier))
        malformed = Effect(level='unknown', duration='unknown', modifier='unknown')
        malformed.evaluate_expressions(20, EffectUtil.safe_eval_int)
        self.assertEqual((20, 0, 0), (malformed.level, malformed.duration, malformed.modifier))

    def test_resisted_dispel_weakens_only_the_effect_record(self):
        effect = Effect(level=0, duration=-1, modifier=3)
        resisted = Mock(return_value=True)
        self.assertFalse(effect.try_dispel(10, resisted))
        resisted.assert_called_once_with(10, 0, -1)
        self.assertEqual((-1, 3), (effect.level, effect.modifier))
        failed_save = Mock(return_value=False)
        self.assertTrue(effect.try_dispel(10, failed_save))
        self.assertEqual(-1, effect.level)

    def test_shared_save_uses_caller_rng_and_berserk_context(self):
        victim = NS(level=10, saving_throw=0, character_class=NS(mana_gain=False), is_npc=False)
        percentile = Mock(return_value=54)
        with patch.object(CharacterApi, 'is_npc', return_value=False):
            self.assertTrue(EffectUtil.saves_spell(10, victim, berserk=True, roll=percentile))
            percentile.return_value = 55
            self.assertFalse(EffectUtil.saves_spell(10, victim, berserk=True, roll=percentile))
            percentile.reset_mock()
            self.assertTrue(EffectUtil.saves_spell(10, victim, immunity=lambda *_: 'IS_IMMUNE',
                                                 berserk=False, roll=percentile))
            percentile.assert_not_called()

    def test_spell_flag_queries_use_the_existing_entity_flag_contract(self):
        affected = IntEnum('Affected', {'AFF_BLIND': 1, 'AFF_SLEEP': 2})
        target = NS(effects=[Effect(type='spell.armor')], status_flags=NS(affected_by='A'))
        api = SpellApi.__new__(SpellApi)
        with patch.object(CharacterApi, 'get_enum', return_value=affected):
            self.assertTrue(api._effect_active(target, 'AFF_BLIND'))
            self.assertFalse(api._effect_active(target, 'AFF_SLEEP'))
            self.assertFalse(api._effect_active(target, 'AFF_UNKNOWN'))
            self.assertTrue(api._effect_active(target, 'spell.armor'))

    def test_equipped_sale_removes_effects_through_the_supplied_handler(self):
        seller = Character.from_json(build_character_data())
        document = runtime.item_fixtures.TestItemPersistence._document('ring')
        item = Item.from_json(document)
        seller.equip_item(item, 'finger1')
        keeper = NS(gold=10, silver=0)
        shop = Shop.__new__(Shop)
        effects = NS(remove_item_effects=Mock())
        with patch.object(shop, 'is_trash_item', return_value=True):
            shop.complete_sale(seller, keeper, item, 50, None, effect_handler=effects)
        effects.remove_item_effects.assert_called_once_with(seller, item)
        self.assertIsNone(seller.equipped.finger1)
        self.assertNotIn(item, seller.owned_items())


if __name__ == '__main__':
    unittest.main()
