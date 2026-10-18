import importlib.util
import sys
import types
import unittest
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


class _Mobile:
    pass


class _GameApi:
    pass


def _load_character_api():
    module_name = "_test_character_api_module"
    player_package = types.ModuleType("player")
    player_package.__path__ = []
    mobile_package = types.ModuleType("mobile")
    mobile_package.__path__ = []
    replacements = {
        "mobile": mobile_package,
        "mobile.Mobile": types.SimpleNamespace(Mobile=_Mobile),
        "player": player_package,
        "player.Character": types.SimpleNamespace(Character=object),
        "api.GameApi": types.SimpleNamespace(GameApi=_GameApi),
        "util.GenericUtil": types.SimpleNamespace(GenericUtil=types.SimpleNamespace(to_int=lambda value, default=0: int(value))),
        "game.RandomNumberGenerator": types.SimpleNamespace(RandomNumberGenerator=lambda: SimpleNamespace()),
    }
    originals = {name: sys.modules.get(name) for name in replacements}
    try:
        sys.modules.update(replacements)
        spec = importlib.util.spec_from_file_location(module_name, SRC / "api" / "CharacterApi.py")
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module.CharacterApi
    finally:
        sys.modules.pop(module_name, None)
        for name, original in originals.items():
            if original is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = original


CharacterApi = _load_character_api()
CharacterApi.GameParameters = SimpleNamespace(
    LEVEL_IMMORTAL=SimpleNamespace(value=55),
    HERO=SimpleNamespace(value=51),
)
CharacterApi.get_trust = classmethod(lambda cls, character: getattr(character, "level", 0))


class TestCharacterApiImmortal(unittest.TestCase):
    def test_is_immortal_accepts_session(self):
        session = SimpleNamespace(character=SimpleNamespace(level=55, trust=0))

        self.assertTrue(CharacterApi.is_immortal(session))

    def test_is_immortal_returns_false_for_empty_session(self):
        session = SimpleNamespace(character=None)

        self.assertFalse(CharacterApi.is_immortal(session))


if __name__ == "__main__":
    unittest.main()
