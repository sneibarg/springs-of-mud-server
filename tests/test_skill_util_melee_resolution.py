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


class _Character:
    @staticmethod
    def learned_entry_name(entry) -> str:
        return str(entry.get("name", "") or "").strip() if isinstance(entry, dict) else str(getattr(entry, "name", "") or "").strip()

    @staticmethod
    def learned_entry_level(entry) -> int:
        return int(entry.get("level", 0)) if isinstance(entry, dict) else int(getattr(entry, "level", 0))

    @staticmethod
    def get_learned(character, learned_name, *, collection_name: str = "", **_kwargs):
        wanted = str(learned_name or "").strip().lower()
        collections = [getattr(character, collection_name, [])] if collection_name else [getattr(character, "skills", []), getattr(character, "spells", [])]
        for collection in collections:
            for entry in list(collection or []):
                if _Character.learned_entry_name(entry).lower() == wanted:
                    return entry
        return None

    @staticmethod
    def set_learned(character, learned_name, learned_level, *, collection_name: str = "", create: bool = False):
        entry = _Character.get_learned(character, learned_name, collection_name=collection_name)
        if entry is None:
            if not create:
                raise ValueError(learned_name)
            collection_key = "spells" if collection_name == "spells" else "skills"
            collection = getattr(character, collection_key, None)
            if collection is None:
                collection = []
                setattr(character, collection_key, collection)
            entry = {"name": str(learned_name or "").strip(), "level": 0}
            collection.append(entry)
        entry["level"] = int(learned_level)
        return entry


_stub_package("server")
_stub_module("server.LoggerFactory", LoggerFactory=_LoggerFactory)
_stub_package("player")
_stub_module("player.Character", Character=_Character)
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

    def test_check_improve_queues_success_message(self):
        character = SimpleNamespace(
            name="Tester",
            level=20,
            character_class=SimpleNamespace(name="warrior", skill_adept=75),
            character_attributes=SimpleNamespace(intelligence=18),
            skills=[{"name": "sword", "level": 40}],
            spells=[],
        )
        ability = SimpleNamespace(name="sword", rating_by_class={"warrior": 2})
        registry = SimpleNamespace(
            skill_registry=SimpleNamespace(get_or_none=Mock(return_value=ability)),
            spell_registry=SimpleNamespace(get_or_none=Mock(return_value=None)),
        )

        with patch.object(_skill_util_module.CharacterApi, "get_registry", return_value=registry), \
                patch.object(_skill_util_module.CharacterAdvancement, "gain_experience"), \
                patch.object(_skill_util_module.random, "randint", side_effect=[1, 1]):
            SkillUtil.check_improve(character, "skill-sword", True)

        self.assertEqual(41, character.skills[0]["level"])
        self.assertEqual("You have become better at sword!\r\n", SkillUtil.take_improve_messages(character))
        self.assertEqual("", SkillUtil.take_improve_messages(character))

    def test_check_improve_queues_failure_message(self):
        character = SimpleNamespace(
            name="Tester",
            level=30,
            character_class=SimpleNamespace(name="mage", skill_adept=52),
            character_attributes=SimpleNamespace(intelligence=20),
            skills=[],
            spells=[{"name": "magic missile", "level": 51}],
        )
        ability = SimpleNamespace(name="magic missile", rating_by_class={"mage": 4})
        registry = SimpleNamespace(
            skill_registry=SimpleNamespace(get_or_none=Mock(return_value=None)),
            spell_registry=SimpleNamespace(get_or_none=Mock(return_value=ability)),
        )

        with patch.object(_skill_util_module.CharacterApi, "get_registry", return_value=registry), \
                patch.object(_skill_util_module.CharacterAdvancement, "gain_experience"), \
                patch.object(_skill_util_module.random, "randint", side_effect=[1, 1, 3]):
            SkillUtil.check_improve(character, "spell-magic-missile", False)

        self.assertEqual(52, character.spells[0]["level"])
        self.assertEqual(
            "You learn from your mistakes, and your magic missile skill improves.\r\n",
            SkillUtil.take_improve_messages(character),
        )

    def test_check_improve_creates_missing_skill_entry_before_incrementing(self):
        character = SimpleNamespace(
            name="Tester",
            level=20,
            character_class=SimpleNamespace(name="warrior", skill_adept=75),
            character_attributes=SimpleNamespace(intelligence=18),
            skills=[],
            spells=[],
        )
        ability = SimpleNamespace(name="sword", rating_by_class={"warrior": 2})
        registry = SimpleNamespace(
            skill_registry=SimpleNamespace(get_or_none=Mock(return_value=ability)),
            spell_registry=SimpleNamespace(get_or_none=Mock(return_value=None)),
        )

        with patch.object(_skill_util_module.CharacterApi, "get_registry", return_value=registry), \
                patch.object(_skill_util_module.CharacterAdvancement, "gain_experience"), \
                patch.object(_skill_util_module.random, "randint", side_effect=[1]), \
                patch.object(_skill_util_module.rng, "number_percent", return_value=1):
            SkillUtil.check_improve(character, "skill-sword", True)

        self.assertEqual([{"name": "sword", "level": 1}], character.skills)
        self.assertEqual("You have become better at sword!\r\n", SkillUtil.take_improve_messages(character))


if __name__ == "__main__":
    unittest.main()
