import sys
import types
import unittest
import importlib.util
from enum import IntEnum
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


class _AffectedBits(IntEnum):
    AFF_SANCTUARY = 1


class _CharacterApi:
    @staticmethod
    def get_enum(name):
        if name == "affectedBy":
            return _AffectedBits
        return SimpleNamespace(__members__={})

    @staticmethod
    def is_set(raw, bit):
        return (int(raw) & int(bit)) != 0


def _load_effect_util():
    module_name = "_test_effect_util_module"
    replacements = {
        "api.CharacterApi": types.SimpleNamespace(CharacterApi=_CharacterApi),
        "player.Character": types.SimpleNamespace(Character=object),
        "util.GenericUtil": types.SimpleNamespace(
            GenericUtil=types.SimpleNamespace(to_int=lambda value, default=0: int(value) if str(value).strip() else default)
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


class TestEffectUtilAffects(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
