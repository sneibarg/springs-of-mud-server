import os
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import patch


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

import types
import importlib.util


def _stub_package(name: str):
    if name in sys.modules:
        return sys.modules[name]
    module = types.ModuleType(name)
    module.__path__ = [os.path.join(SRC, name)]
    sys.modules[name] = module
    return module


def _stub_module(name: str, **attrs):
    module = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    sys.modules[name] = module
    return module


class _LoggerFactory:
    @staticmethod
    def get_logger(_name):
        return SimpleNamespace(
            debug=lambda *_args, **_kwargs: None,
            info=lambda *_args, **_kwargs: None,
            warning=lambda *_args, **_kwargs: None,
            error=lambda *_args, **_kwargs: None,
        )


_stub_package("server")
_stub_module("server.LoggerFactory", LoggerFactory=_LoggerFactory)
_stub_package("api")
_stub_module("api.CharacterApi", CharacterApi=SimpleNamespace(is_npc=lambda _entity: False))
_stub_module(
    "util.InterpUtil",
    InterpUtil=SimpleNamespace(
        one_argument=lambda argument: tuple(((argument or "").split(maxsplit=1) + ["", ""])[:2]),
    ),
)

spec = importlib.util.spec_from_file_location("util.WizUtil", os.path.join(SRC, "util", "WizUtil.py"))
wiz_util_module = importlib.util.module_from_spec(spec)
sys.modules["util.WizUtil"] = wiz_util_module
spec.loader.exec_module(wiz_util_module)
WizUtil = wiz_util_module.WizUtil


class _CharacterRegistry:
    def __init__(self, characters):
        self._characters = list(characters)

    def all_characters(self):
        return list(self._characters)


class TestWizUtilWorldLookup(unittest.TestCase):
    def test_name_matches_rom_style_keyword_inside_mobile_name(self):
        self.assertTrue(WizUtil.name_matches("elite", "oldstyle royal elite guard"))
        self.assertTrue(WizUtil.name_matches("roya", "oldstyle royal elite guard"))

    def test_find_world_entity_finds_mobile_from_character_list(self):
        guard = SimpleNamespace(
            id="mob-9582",
            name="oldstyle royal elite guard",
            short_description="the oldstyle royal elite guard",
            vnum="9582",
        )
        registry = _CharacterRegistry([guard])

        with patch.object(wiz_util_module.CharacterApi, "is_npc", return_value=True):
            found = WizUtil.find_world_entity(registry, room_registry=None, query="elite")

        self.assertIs(guard, found)

    def test_find_world_entity_respects_include_mobiles_when_registry_contains_mobiles(self):
        guard = SimpleNamespace(
            id="mob-9582",
            name="oldstyle royal elite guard",
            short_description="the oldstyle royal elite guard",
            vnum="9582",
        )
        registry = _CharacterRegistry([guard])

        with patch.object(wiz_util_module.CharacterApi, "is_npc", return_value=True):
            found = WizUtil.find_world_entity(
                registry,
                room_registry=None,
                query="elite",
                include_mobiles=False,
            )

        self.assertIsNone(found)


if __name__ == "__main__":
    unittest.main()
