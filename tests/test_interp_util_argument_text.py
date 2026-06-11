import importlib.util
import os
import sys
import types
import unittest
from types import SimpleNamespace


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")

def _module(name: str, **attrs):
    module = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    return module


def _load_interp_util():
    replacements = {
        "interp.Command": _module("interp.Command", Command=object),
        "interp.InterpView": _module("interp.InterpView", InterpView=object),
        "server.LoggerFactory": _module(
            "server.LoggerFactory",
            LoggerFactory=SimpleNamespace(get_logger=lambda _name: SimpleNamespace()),
        ),
    }
    originals = {name: sys.modules.get(name) for name in replacements}
    try:
        sys.modules.update(replacements)
        spec = importlib.util.spec_from_file_location("_test_interp_util_module", os.path.join(SRC, "util", "InterpUtil.py"))
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        sys.modules["_test_interp_util_module"] = module
        spec.loader.exec_module(module)
        return module.InterpUtil
    finally:
        sys.modules.pop("_test_interp_util_module", None)
        for name, original in originals.items():
            if original is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = original


InterpUtil = _load_interp_util()


class TestInterpUtilArgumentText(unittest.TestCase):
    def test_argument_text_tolerates_non_command_context_without_result(self):
        view = SimpleNamespace(context=SimpleNamespace())

        self.assertEqual("", InterpUtil.argument_text(view))


if __name__ == "__main__":
    unittest.main()
