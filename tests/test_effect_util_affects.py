import sys
import types
import unittest
import importlib.util
import json
from enum import IntEnum
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


class _AffectedBits(IntEnum):
    AFF_SANCTUARY = 1


class _ApplyTypes(IntEnum):
    APPLY_NONE = 0
    APPLY_STR = 1
    APPLY_DEX = 2
    APPLY_AC = 17


class _CharacterApi:
    @staticmethod
    def get_enum(name):
        if name == "affectedBy":
            return _AffectedBits
        if name == "applyTypes":
            return _ApplyTypes
        return SimpleNamespace(__members__={})

    @staticmethod
    def is_set(raw, bit):
        return (int(raw) & int(bit)) != 0


def _to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _load_effect_util():
    module_name = "_test_effect_util_module"
    replacements = {
        "api.CharacterApi": types.SimpleNamespace(CharacterApi=_CharacterApi),
        "player.Character": types.SimpleNamespace(Character=object),
        "util.GenericUtil": types.SimpleNamespace(
            GenericUtil=types.SimpleNamespace(to_int=_to_int)
        ),
    }
    originals = {name: sys.modules.get(name) for name in replacements}
    try:
        sys.modules.update(replacements)
        spec = importlib.util.spec_from_file_location(module_name, SRC / "util" / "EffectUtil.py")
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module.EffectUtil
    finally:
        sys.modules.pop(module_name, None)
        for name, original in originals.items():
            if original is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = original


EffectUtil = _load_effect_util()


def _load_effect_runtime():
    game_api = SimpleNamespace(
        set_bit=lambda raw, bit: raw | bit, unset_bit=lambda raw, bit: raw & ~bit,
        convert_flags=lambda raw: sum(1 << (ord(c) - ord("A")) for c in str(raw)),
        flags_to_letters=lambda raw: "".join(chr(ord("A") + bit) for bit in range(26) if raw & (1 << bit)),
        flags_to_int=lambda raw: int(raw or 0) if str(raw or 0).lstrip('-').isdigit()
            else sum(1 << (ord(c) - ord('A')) for c in str(raw)),
        is_set=lambda raw, bit: bool(int(raw) & int(bit)),
    )
    replacements = {
        "injector": SimpleNamespace(inject=lambda cls: cls),
        "api.GameApi": SimpleNamespace(GameApi=game_api),
        "game.EnumProvider": SimpleNamespace(EnumProvider=object),
        "server.LoggerFactory": SimpleNamespace(LoggerFactory=SimpleNamespace(get_logger=lambda _: Mock())),
        "util.EffectUtil": SimpleNamespace(EffectUtil=EffectUtil),
    }
    with patch.dict(sys.modules, replacements):
        modules = {}
        for name, path in [("util.GenericUtil", "util/GenericUtil.py"),
                           ("game.RandomNumberGenerator", "game/RandomNumberGenerator.py"),
                           ("item.Effect", "item/Effect.py"),
                           ("item.EffectHandler", "item/EffectHandler.py")]:
            spec = importlib.util.spec_from_file_location(name, SRC / path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)
            modules[name] = module
    return (modules["item.EffectHandler"].EffectHandler, modules["item.Effect"].Effect,
            modules["util.GenericUtil"].GenericUtil, modules["game.RandomNumberGenerator"].RandomNumberGenerator)


class TestSpellEffectApplication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.Handler, cls.Effect, cls.GenericUtil, cls.RNG = _load_effect_runtime()
        cls.documents = {doc["name"]: doc for doc in json.loads(
            (ROOT / "resources/collections/SOMDB.Spells.json").read_text(encoding="utf-8"))}
        data = json.loads((ROOT / "resources/collections/SOMDB.GameData.json").read_text(encoding="utf-8"))[0]
        cls.enums = {name: IntEnum(name, data["enums"][name])
                     for name in ("whereAffect", "applyTypes", "affectedBy", "itemFlags", "weaponType")}

    def setUp(self):
        self.handler = self.Handler(SimpleNamespace(get=self.enums.get))
        self.actor = SimpleNamespace(level=24)
        self.target = SimpleNamespace(
            effects=[], hit_roll=10, dam_roll=20, saving_throw=5,
            character_attributes=SimpleNamespace(strength=15),
            armor_class=SimpleNamespace(piercing=100, bashing=100, slashing=100, magic=100),
            status_flags=SimpleNamespace(affected_by=0),
        )
        self.target.status_flags.assign_bitfield = lambda name, value: setattr(self.target.status_flags, name, value)

    def spell(self, name):
        doc = self.documents[name]
        with patch.dict(sys.modules, {"util.GenericUtil": SimpleNamespace(GenericUtil=self.GenericUtil)}):
            effects = [self.Effect.from_json(entry) for entry in doc["affectData"]]
        return SimpleNamespace(name=name, handler_id=doc["handlerId"], affect_data=effects)

    def stats(self):
        return (self.target.hit_roll, self.target.dam_roll, self.target.saving_throw,
                self.target.armor_class.magic, self.target.character_attributes.strength)

    def test_dispel_stops_at_first_failed_save_and_strips_the_entire_spell(self):
        spell = self.spell("frenzy")
        self.handler.apply_spell_effects(self.actor, self.target, spell)
        original = list(self.target.effects)
        unrelated = self.Effect(type="spell.other", duration=5)
        self.handler.affect_to_char(self.target, unrelated)
        with patch.object(EffectUtil, "saves_dispel", side_effect=[True, False]) as saves:
            removed = self.handler.dispel_effects(20, self.target, "SPELL.FRENZY")
        self.assertEqual(original, removed)
        self.assertEqual(2, saves.call_count)
        self.assertEqual([23, 24, 24], [effect.level for effect in removed])
        self.assertEqual(["spell.other"], [effect.type for effect in self.target.effects])
        self.assertEqual((10, 20, 5, 100, 15), self.stats())

    def test_saved_dispel_weakens_every_record_without_clamping_at_zero(self):
        self.handler.apply_spell_effects(self.actor, self.target, self.spell("curse"))
        for effect in self.target.effects:
            effect.level = 0
        with patch.object(EffectUtil, "saves_dispel", return_value=True) as saves:
            self.assertEqual([], self.handler.dispel_effects(20, self.target, "spell.curse"))
        self.assertEqual(2, saves.call_count)
        self.assertEqual([-1, -1], [effect.level for effect in self.target.effects])
        self.assertEqual((7, 20, 8, 100, 15), self.stats())
        with patch.object(EffectUtil, "saves_dispel") as saves:
            self.assertEqual([], self.handler.dispel_effects(20, self.target, "spell.absent"))
            saves.assert_not_called()

    def test_fuzzy_expressions_use_rom_four_way_roll_in_both_expression_paths(self):
        from tests.test_spell_affect_payload_messages import _load_spell_api

        api = _load_spell_api()(Mock(), Mock())
        ctx = SimpleNamespace(actor=self.actor, spell=object(), room=None, target=self.target,
                              victim=self.target, obj=None, level=20)
        rng = self.RNG()
        with patch.dict(sys.modules, {"game.RandomNumberGenerator": SimpleNamespace(RandomNumberGenerator=lambda: rng)}), \
             patch.dict(api.eval_int.__globals__, EffectUtil=EffectUtil):
            for roll, expected in ((0, 4), (1, 5), (2, 5), (3, 6)):
                with self.subTest(roll=roll), patch.object(rng, "number_bits", return_value=roll):
                    self.assertEqual(expected, EffectUtil.safe_eval_int("number_fuzzy(level / 4)", level=20))
                    self.assertEqual(expected, api.eval_int(ctx, "number_fuzzy(level / 4)"))
            with patch.object(rng, "number_bits", return_value=0):
                self.assertEqual(1, EffectUtil.number_fuzzy(0))

    def test_frenzy_uses_integer_division_before_multiplying_armor_modifier(self):
        spell = self.spell("frenzy")
        for level, expected in ((11, 0), (12, 10), (23, 10), (24, 20), (25, 20)):
            with self.subTest(level=level):
                effect = self.handler.effect_from_spell_affect(spell, spell.affect_data[2], level)
                self.assertEqual(expected, effect.modifier)

    def test_chill_touch_data_joins_strength_penalty_and_restores_it_on_removal(self):
        spell = self.spell("chill touch")
        for expected in (14, 13):
            self.handler.apply_spell_effects(self.actor, self.target, spell, caster_level=50, join=True)
            self.assertEqual(expected, self.target.character_attributes.strength)
            self.assertEqual(1, len(self.target.effects))
        effect = self.target.effects[0]
        self.assertEqual((50, 12, -2), (effect.level, effect.duration, effect.modifier))
        self.handler.affect_strip(self.target, spell.handler_id)
        self.assertEqual(15, self.target.character_attributes.strength)

    def test_multi_part_spells_keep_separate_stats_durations_and_reverse_on_removal(self):
        for name, count, stats, duration in [
            ("bless", 2, (13, 20, 2, 100, 15), 30),
            ("curse", 2, (7, 20, 8, 100, 15), 48),
            ("frenzy", 3, (14, 24, 5, 120, 15), 8),
            ("calm", 2, (8, 18, 5, 100, 15), 6),
        ]:
            with self.subTest(spell=name):
                spell = self.spell(name)
                self.handler.apply_spell_effects(self.actor, self.target, spell)
                self.assertEqual(count, len(self.target.effects))
                self.assertEqual(stats, self.stats())
                self.assertTrue(all(effect.duration == duration for effect in self.target.effects))
                self.assertTrue(all(effect.where == "TO_AFFECTS" for effect in self.target.effects))
                self.assertEqual(len(spell.affect_data), len(self.documents[name]["affectData"]))
                self.handler.affect_strip(self.target, spell.handler_id)
                self.assertEqual([], self.target.effects)
                self.assertEqual((10, 20, 5, 100, 15), self.stats())
                self.assertEqual(0, self.target.status_flags.affected_by)

    def test_expiration_reverses_all_multi_part_modifiers(self):
        for name in ("bless", "curse", "frenzy", "calm"):
            with self.subTest(spell=name):
                self.handler.apply_spell_effects(self.actor, self.target, self.spell(name))
                for effect in self.target.effects:
                    effect.duration = 0
                self.handler.tick_effects(self.target)
                self.assertEqual([], self.target.effects)
                self.assertEqual((10, 20, 5, 100, 15), self.stats())
                self.assertEqual(0, self.target.status_flags.affected_by)

    def test_shared_flag_survives_partial_removal_without_reapplying_sibling_stats(self):
        for numeric in (False, True):
            with self.subTest(numeric=numeric):
                self.handler.apply_spell_effects(self.actor, self.target, self.spell("curse"))
                first, second = self.target.effects
                bit = self.enums["affectedBy"].AFF_CURSE.value
                if numeric:
                    first.bitvector = bit
                self.handler.remove_effect(self.target, first)
                self.assertEqual((10, 20, 8, 100, 15), self.stats())
                self.assertEqual(bit, self.target.status_flags.affected_by)
                self.handler.remove_effect(self.target, second)
                self.assertEqual((10, 20, 5, 100, 15), self.stats())
                self.assertEqual(0, self.target.status_flags.affected_by)

    def test_mixed_spell_templates_only_apply_to_their_target_kind(self):
        for name, character_count in [("bless", 2), ("curse", 2), ("invisibility", 1)]:
            with self.subTest(spell=name):
                spell = self.spell(name)
                obj = SimpleNamespace(item_type="weapon", effects=[], extra_flags="")
                self.handler.apply_spell_effects(self.actor, obj, spell)
                self.assertEqual(1, len(obj.effects))
                self.assertEqual("TO_OBJECT", obj.effects[0].where)
                self.assertTrue(obj.extra_flags)
                self.handler.apply_spell_effects(self.actor, self.target, spell)
                self.assertEqual(character_count, len(self.target.effects))
                self.assertTrue(all(effect.where == "TO_AFFECTS" for effect in self.target.effects))
                self.handler.affect_strip(self.target, spell.handler_id)

    def test_numeric_where_and_both_object_target_aliases_are_filtered(self):
        for where, apply_to in [(1, ""), (1, "item"), (1, "object"), (5, "object")]:
            with self.subTest(where=where, apply_to=apply_to):
                effect = self.Effect(where=where, apply_to=apply_to, type="sn", bitvector=0)
                spell = SimpleNamespace(handler_id="spell.test", affect_data=[effect])
                obj = SimpleNamespace(item_type="weapon", effects=[], extra_flags="", value4="0")
                self.handler.apply_spell_effects(self.actor, self.target, spell)
                self.assertEqual([], self.target.effects)
                self.handler.apply_spell_effects(self.actor, obj, spell)
                self.assertEqual(1, len(obj.effects))

    def test_plague_collection_explicitly_joins_and_accumulates(self):
        spell = self.spell("plague")
        ctx = SimpleNamespace(apply_affect_data=lambda **kwargs: self.handler.apply_spell_effects(
            self.actor, self.target, spell, **kwargs))
        for _ in range(2):
            eval(self.documents["plague"]["lambdas"][-1])(ctx)
        self.assertEqual(1, len(self.target.effects))
        effect = self.target.effects[0]
        self.assertEqual((18, 48, -10), (effect.level, effect.duration, effect.modifier))
        self.assertEqual(5, self.target.character_attributes.strength)
        self.handler.affect_strip(self.target, spell.handler_id)
        self.assertEqual(15, self.target.character_attributes.strength)


class TestEffectUtilAffects(unittest.TestCase):
    def test_spell_saves_match_rom_thresholds_and_strict_endpoints(self):
        cases = [
            ("IS_NORMAL", False, False, False, 10, 10, 49, True),
            ("IS_NORMAL", False, False, False, 10, 10, 50, False),
            ("IS_RESISTANT", False, False, False, 10, 10, 51, True),
            ("IS_RESISTANT", False, False, False, 10, 10, 52, False),
            ("IS_VULNERABLE", False, False, False, 10, 10, 47, True),
            ("IS_VULNERABLE", False, False, False, 10, 10, 48, False),
            ("IS_NORMAL", True, False, False, 10, 10, 44, True),
            ("IS_NORMAL", True, False, False, 10, 10, 45, False),
            ("IS_NORMAL", True, True, False, 10, 10, 49, True),
            ("IS_NORMAL", True, True, False, 10, 10, 50, False),
            ("IS_RESISTANT", True, False, True, 10, 10, 50, True),
            ("IS_RESISTANT", True, False, True, 10, 10, 51, False),
            ("IS_NORMAL", False, False, False, 100, 10, 4, True),
            ("IS_NORMAL", False, False, False, 100, 10, 5, False),
            ("IS_NORMAL", False, False, False, 1, 100, 94, True),
            ("IS_NORMAL", False, False, False, 1, 100, 95, False),
            ("IS_IMMUNE", False, False, False, 100, 1, 100, True),
        ]
        globals_ = EffectUtil.saves_spell.__globals__
        for status, mana, npc, berserk, level, victim_level, roll, expected in cases:
            with self.subTest(status=status, mana=mana, npc=npc, berserk=berserk, level=level, roll=roll):
                victim = SimpleNamespace(level=victim_level, saving_throw=0, is_npc=npc,
                                         character_class=SimpleNamespace(mana_gain=mana))
                api = SimpleNamespace(get_enum=lambda _: None,
                                      is_affected_by_name=lambda *_: berserk,
                                      is_npc=lambda entity: entity.is_npc)
                immunity = Mock(return_value=status)
                with patch.dict(globals_, CharacterApi=api), \
                     patch.object(globals_["random"], "randint", return_value=roll) as rng:
                    self.assertEqual(expected, EffectUtil.saves_spell(level, victim, "DAM_FIRE", immunity=immunity))
                    immunity.assert_called_once_with(victim, "DAM_FIRE")
                    if status == "IS_IMMUNE":
                        rng.assert_not_called()
                    else:
                        rng.assert_called_once_with(1, 100)

    def test_mana_class_adjustment_does_not_depend_on_immunity_callback(self):
        victim = SimpleNamespace(level=10, saving_throw=0, character_class=SimpleNamespace(mana_gain=True))
        api = SimpleNamespace(get_enum=lambda _: None, is_affected_by_name=lambda *_: False, is_npc=lambda _: False)
        globals_ = EffectUtil.saves_spell.__globals__
        with patch.dict(globals_, CharacterApi=api), patch.object(globals_["random"], "randint", return_value=45):
            self.assertFalse(EffectUtil.saves_spell(10, victim, "DAM_OTHER"))

    def test_format_affects_includes_spell_effect_records_without_bitvectors(self):
        character = SimpleNamespace(
            status_flags=SimpleNamespace(affected_by=0),
            effects=[
                SimpleNamespace(type="spell.armor"),
                SimpleNamespace(type="spell.bless"),
                SimpleNamespace(type="spell.giant_strength"),
                SimpleNamespace(type="spell.shield"),
            ],
        )

        text = EffectUtil.format_affects(character)

        self.assertIn("Spell: armor\r\n", text)
        self.assertIn("Spell: bless\r\n", text)
        self.assertIn("Spell: giant strength\r\n", text)
        self.assertIn("Spell: shield\r\n", text)

    def test_format_affects_skips_numeric_sentinel_effect_types(self):
        character = SimpleNamespace(
            status_flags=SimpleNamespace(affected_by=0),
            effects=[
                SimpleNamespace(type="-1"),
                SimpleNamespace(type="spell.armor"),
            ],
        )

        text = EffectUtil.format_affects(character)

        self.assertNotIn("Spell: -1\r\n", text)
        self.assertIn("Spell: armor\r\n", text)

    def test_format_affects_hides_stat_details_below_level_twenty(self):
        character = SimpleNamespace(
            level=19,
            status_flags=SimpleNamespace(affected_by=0),
            effects=[
                SimpleNamespace(type="spell.giant_strength", location="APPLY_STR", modifier=3, duration=5),
                SimpleNamespace(type="spell.giant_strength", location="APPLY_DEX", modifier=2, duration=-1),
            ],
        )

        text = EffectUtil.format_affects(character)

        self.assertEqual(1, text.count("Spell: giant strength\r\n"))
        self.assertNotIn("modifies strength by 3", text)
        self.assertNotIn("permanently", text)

    def test_format_affects_shows_stat_details_at_level_twenty(self):
        character = SimpleNamespace(
            level=20,
            status_flags=SimpleNamespace(affected_by=0),
            effects=[
                SimpleNamespace(type="spell.giant_strength", location="APPLY_STR", modifier=3, duration=5),
                SimpleNamespace(type="spell.giant_strength", location="APPLY_DEX", modifier=2, duration=-1),
                SimpleNamespace(type="spell.armor", location="APPLY_AC", modifier=-20, duration=12),
            ],
        )

        text = EffectUtil.format_affects(character)

        self.assertIn("Spell: giant strength : modifies strength by 3 for 5 hours\r\n", text)
        self.assertIn("                      : modifies dexterity by 2 permanently\r\n", text)
        self.assertIn("Spell: armor          : modifies armor class by -20 for 12 hours\r\n", text)


if __name__ == "__main__":
    unittest.main()
