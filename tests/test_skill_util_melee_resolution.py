import importlib.util
import sys
import types
import unittest
from enum import IntEnum
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def _stub_package(name: str):
    if name in sys.modules:
        return sys.modules[name]
    module = types.ModuleType(name)
    module.__path__ = [str(SRC / name)]
    sys.modules[name] = module
    return module


def _stub_module(name: str, **attrs):
    module = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    sys.modules[name] = module
    return module


def _load_module(name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(name, SRC / relative_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class _Logger:
    def info(self, *_args, **_kwargs):
        return None

    def debug(self, *_args, **_kwargs):
        return None

    def error(self, *_args, **_kwargs):
        return None


class _LoggerFactory:
    @staticmethod
    def get_logger(_name):
        return _Logger()


class _CharacterApi:
    @staticmethod
    def is_npc(_entity):
        return False

    @staticmethod
    def get_registry():
        return SimpleNamespace()

    @staticmethod
    def get_attribute_bonus(_stat, _value):
        return {"learn": 18}

    @staticmethod
    def skill_value_for_class(mapping, class_name, fallback=0):
        return mapping.get(class_name, fallback)

    @staticmethod
    def get_enum(_name):
        return SimpleNamespace()


_stub_package("server")
_stub_module("server.LoggerFactory", LoggerFactory=_LoggerFactory)
_stub_package("player")
_stub_module("player.Character", Character=object)
_stub_module("player.CharacterAdvancement", CharacterAdvancement=SimpleNamespace(gain_experience=lambda *_args, **_kwargs: None))
_stub_package("api")
_stub_module("api.CharacterApi", CharacterApi=_CharacterApi)
_stub_package("util")
_load_module("util.GenericUtil", "util/GenericUtil.py")
_skill_util_module = _load_module("util.SkillUtil", "util/SkillUtil.py")
SkillUtil = _skill_util_module.SkillUtil


class TestSkillUtilMeleeResolution(unittest.TestCase):
    def test_active_melee_skill_name_resolves_numeric_weapon_class(self):
        weapon = SimpleNamespace(value0=1)
        weapon_class_names = IntEnum("WeaponClass", {"WEAPON_DAGGER": 1})

        with patch.object(_skill_util_module.CharacterApi, "get_enum", return_value=SimpleNamespace(WEAPON_DAGGER=SimpleNamespace(value=1))):
            skill_name = SkillUtil.active_melee_skill_name(weapon, weapon_class_names)

        self.assertEqual("dagger", skill_name)

    def test_active_melee_skill_name_resolves_string_weapon_name_from_enum(self):
        weapon = SimpleNamespace(value0="sword")
        weapon_class_names = IntEnum("WeaponClass", {"WEAPON_SWORD": 1, "WEAPON_DAGGER": 2})

        skill_name = SkillUtil.active_melee_skill_name(weapon, weapon_class_names)

        self.assertEqual("sword", skill_name)

    def test_check_improve_by_name_resolves_skill_id(self):
        character = SimpleNamespace()
        registry = SimpleNamespace(
            skill_registry=SimpleNamespace(all_skills=Mock(return_value=[SimpleNamespace(id="skill-dagger", name="dagger")])),
            spell_registry=SimpleNamespace(all_spells=Mock(return_value=[])),
        )

        with patch.object(_skill_util_module.CharacterApi, "get_registry", return_value=registry), \
                patch.object(SkillUtil, "check_improve") as check_improve:
            SkillUtil.check_improve_by_name(character, "dagger", True, 5)

        check_improve.assert_called_once_with(character, "skill-dagger", True, 5)


if __name__ == "__main__":
    unittest.main()
