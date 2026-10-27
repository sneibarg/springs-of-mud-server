import importlib.util
from enum import IntEnum
from pathlib import Path
from types import SimpleNamespace
import unittest


source = Path(__file__).resolve().parents[1] / 'src/game/EnumProvider.py'
spec = importlib.util.spec_from_file_location('_enum_provider_contract', source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
EnumProvider = module.EnumProvider


class Flags(IntEnum):
    NONE = 0
    CLOSED = 2
    LOCKED = 4


class EnumProviderTests(unittest.TestCase):
    def test_value_selects_first_existing_enum_alias_including_zero(self):
        self.assertEqual(2, EnumProvider.value(Flags, 'EX_CLOSED', 'CLOSED'))
        self.assertEqual(4, EnumProvider.value(Flags, 'LOCKED', 'CLOSED'))
        self.assertEqual(0, EnumProvider.value(Flags, 'NONE', 'LOCKED'))

    def test_value_supports_attribute_based_runtime_adapters(self):
        flags = SimpleNamespace(INVALID='unparsed', EX_CLOSED=SimpleNamespace(value='2'), LOCKED=4)
        self.assertEqual(2, EnumProvider.value(flags, 'INVALID', 'EX_CLOSED'))
        self.assertEqual(4, EnumProvider.value(flags, 'LOCKED'))

    def test_missing_enum_members_and_empty_aliases_return_zero(self):
        self.assertEqual(0, EnumProvider.value(None, 'CLOSED'))
        self.assertEqual(0, EnumProvider.value(Flags, 'MISSING'))
        self.assertEqual(0, EnumProvider.value(Flags))

    def test_member_dictionary_keeps_existing_invalid_value_fallback(self):
        flags = SimpleNamespace(__members__={'BAD': SimpleNamespace(value='invalid')}, CLOSED=2)
        self.assertEqual(0, EnumProvider.value(flags, 'BAD', 'CLOSED'))

    def test_registered_enum_access_remains_strict(self):
        provider = EnumProvider({'flags': Flags})
        self.assertEqual(4, provider.get_value('flags', 'LOCKED'))
        self.assertEqual(2, provider.value(provider.get('flags'), 'CLOSED'))
        with self.assertRaises(KeyError):
            provider.get_value('flags', 'MISSING')
        with self.assertRaises(KeyError):
            provider.get('missing')


if __name__ == '__main__':
    unittest.main()
