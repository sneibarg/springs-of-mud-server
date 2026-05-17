import json
import os
import sys
import types
import unittest
from copy import deepcopy
from types import SimpleNamespace


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
COMMANDS_PATH = os.path.join(ROOT, "resources", "collections", "SOMDB.Commands.json")
if SRC not in sys.path:
    sys.path.insert(0, SRC)


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


def _load_module(name: str, relative_path: str):
    import importlib.util

    spec = importlib.util.spec_from_file_location(name, os.path.join(SRC, relative_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class _Logger:
    def info(self, *_args, **_kwargs):
        return None

    def error(self, *_args, **_kwargs):
        return None

    def warn(self, *_args, **_kwargs):
        return None

    def debug(self, *_args, **_kwargs):
        return None


class _LoggerFactory:
    @staticmethod
    def get_logger(_name):
        return _Logger()


class _CharacterMacros:
    _positions = {
        "POS_DEAD": 0,
        "POS_MORTAL": 1,
        "POS_INCAP": 2,
        "POS_STUNNED": 3,
        "POS_SLEEPING": 4,
        "POS_RESTING": 5,
        "POS_SITTING": 6,
        "POS_FIGHTING": 7,
        "POS_STANDING": 8,
        "POS_FLYING": 9,
    }

    @staticmethod
    def get_enum(_name: str):
        return SimpleNamespace()

    @staticmethod
    def movement_position_block_message(character) -> str:
        return str(getattr(character, "position_block", "") or "")

    @staticmethod
    def is_affected_by_name(character, _bits, name: str) -> bool:
        return bool(getattr(character, "effects", {}).get(name, False))

    @staticmethod
    def is_npc(character) -> bool:
        return bool(getattr(character, "is_npc", False))

    @staticmethod
    def is_immortal(character) -> bool:
        return bool(getattr(character, "is_immortal", False))

    @classmethod
    def pos_value(cls, name: str) -> int:
        return cls._positions.get(name, -1)

    @classmethod
    def position_value(cls, character) -> int:
        attrs = getattr(character, "character_attributes", None)
        raw = getattr(attrs, "position", getattr(character, "position", cls.pos_value("POS_STANDING")))
        if isinstance(raw, str):
            return cls.pos_value(raw)
        return int(raw)

    @classmethod
    def is_dead(cls, character) -> bool:
        return cls.position_value(character) == cls.pos_value("POS_DEAD")

    @classmethod
    def is_stunned(cls, character) -> bool:
        return cls.position_value(character) == cls.pos_value("POS_STUNNED")

    @classmethod
    def is_sleeping(cls, character) -> bool:
        return cls.position_value(character) == cls.pos_value("POS_SLEEPING")

    @classmethod
    def is_resting(cls, character) -> bool:
        return cls.position_value(character) == cls.pos_value("POS_RESTING")

    @classmethod
    def is_sitting(cls, character) -> bool:
        return cls.position_value(character) == cls.pos_value("POS_SITTING")

    @classmethod
    def is_fighting(cls, character) -> bool:
        return cls.position_value(character) == cls.pos_value("POS_FIGHTING")

    @classmethod
    def is_flying(cls, character) -> bool:
        return cls.position_value(character) == cls.pos_value("POS_FLYING")


class _MovementUtil:
    DIR_NAME = ["north", "east", "south", "west", "up", "down"]
    REV_DIR = [2, 3, 0, 1, 5, 4]

    @staticmethod
    def direction_index(direction: str) -> int:
        return {"north": 0, "east": 1, "south": 2, "west": 3, "up": 4, "down": 5}.get(direction, -1)

    @staticmethod
    def find_exit(room, direction: int):
        return None if room is None else room.get_exit(direction)

    @staticmethod
    def get_exit_flag(_enum_obj, primary: str, _fallback: str = "") -> int:
        return {"EX_CLOSED": 1, "EX_NOPASS": 2}.get(primary, 0)

    @staticmethod
    def sector_cost(_sector_type) -> int:
        return 1


class _Context(SimpleNamespace):
    def finish(self):
        self.done = True


_stub_module("injector", inject=lambda target: target)
_stub_package("server")
_stub_module("server.LoggerFactory", LoggerFactory=_LoggerFactory)
_stub_package("util")
_load_module("util.GenericUtil", "util/GenericUtil.py")
_stub_module("util.MovementUtil", MovementUtil=_MovementUtil)
_stub_module("util.MobileUtil", MobileUtil=SimpleNamespace(is_train_trainer=lambda *_args, **_kwargs: False))
_stub_package("game")
_stub_module("game.GameData", GameData=object)
_stub_module("game.RegistryService", RegistryService=object)
_load_module("game.GamePayload", "game/GamePayload.py")
_stub_package("fight")
_stub_module("fight.FightHandler", FightHandler=object)
_stub_package("player")
_stub_module("player.Character", Character=object)
_stub_module("player.CharacterApi", CharacterMacros=_CharacterMacros)
_stub_package("interp")
_stub_module("interp.Context", Context=_Context)

Command = _load_module("interp.Command", "interp/Command.py").Command
_load_module("interp.InterpView", "interp/InterpView.py")
_load_module("interp.InterpCheck", "interp/InterpCheck.py")
_load_module("interp.InterpActionDefinition", "interp/InterpActionDefinition.py")
_load_module("interp.InterpPlan", "interp/InterpPlan.py")
InterpApi = _load_module("interp.InterpApi", "api/InterpApi.py").InterpApi
MovementApi = sys.modules["interp.MovementApi"].MovementApi
Movement = _load_module("interp.commands.Movement", "interp/commands/Movement.py").Movement


def _load_command(name: str) -> Command:
    with open(COMMANDS_PATH, "r", encoding="utf-8") as handle:
        commands = json.load(handle)
    for entry in commands:
        if entry.get("name") == name:
            payload = deepcopy(entry)
            payload.setdefault("shortcuts", "")
            payload.setdefault("function", [])
            payload.setdefault("usage", "")
            return Command.from_json(payload)
    raise KeyError(name)


class _Exit(SimpleNamespace):
    pass


class _Room(SimpleNamespace):
    def get_exit(self, direction: int):
        return self.exits.get(direction)

    def player_targets(self, _character):
        return []

    def remove_player_from_room(self, character):
        self.removed = character.id

    def add_player_to_room(self, character):
        self.added = character.id

    def is_private(self, _room_flags):
        return bool(getattr(self, "private_room", False))

    def is_air_room(self, _sector_types):
        return bool(getattr(self, "air_room", False))

    def requires_boat(self, _sector_types):
        return bool(getattr(self, "boat_required", False))


class TestMovementDynamicCommands(unittest.TestCase):
    def _commands(self):
        registry_service = SimpleNamespace(room_registry=SimpleNamespace(get_or_none=lambda **_kwargs: None))
        commands = Movement(
            registry_service=registry_service,
            game_data=SimpleNamespace(),
            fight_handler=SimpleNamespace(aggressive_entry_rounds=lambda *_args, **_kwargs: []),
        )
        commands.exit_flags = SimpleNamespace()
        commands.room_flags = SimpleNamespace()
        commands.affected_bits = SimpleNamespace()
        commands.act_bits = SimpleNamespace()
        commands.sector_types = SimpleNamespace()
        return commands, registry_service.room_registry

    def test_direction_invalid_exit_uses_command_check(self):
        commands, room_registry = self._commands()
        room_registry.get_or_none = lambda **kwargs: None if "id" in kwargs else None
        character = SimpleNamespace(
            id="char-1",
            room_id="room-1",
            movement=10,
            character_attributes=SimpleNamespace(position="POS_STANDING"),
            status_flags=SimpleNamespace(invis_level=0),
            effects={},
        )
        context = _Context(character=character, command=_load_command("north"), done=False, player_handler=lambda: SimpleNamespace(room_registry=room_registry))

        payload = commands.do_north(character, context)

        self.assertEqual("Alas, you cannot go that way.\r\n", payload["to_char"])
        self.assertFalse(hasattr(context, "move_exit"))

    def test_direction_checks_can_compile_with_movement_util_available(self):
        command = _load_command("north")

        self.assertIs(_MovementUtil, InterpApi._lambda_locals()["MovementUtil"])
        self.assertIs(MovementApi, InterpApi._lambda_locals()["MovementApi"])
        self.assertTrue(callable(InterpApi._compile_lambda(command.guards[0]["predicate"])))

    def test_direction_closed_uses_keyword_payload_token(self):
        commands, room_registry = self._commands()
        current_room = _Room(id="room-1", exits={0: _Exit(to_room_vnum="200", to_room_id="room-2", exit_flags=1, keyword="gate")}, sector_type="field")
        destination = _Room(id="room-2", exits={}, sector_type="field")

        def _get_or_none(**kwargs):
            if kwargs.get("id") == "room-1":
                return current_room
            if kwargs.get("vnum") == "200":
                return destination
            return None

        room_registry.get_or_none = _get_or_none
        character = SimpleNamespace(
            id="char-1",
            room_id="room-1",
            movement=10,
            character_attributes=SimpleNamespace(position="POS_STANDING"),
            status_flags=SimpleNamespace(invis_level=0),
            effects={},
        )
        context = _Context(
            character=character,
            command=_load_command("north"),
            done=False,
            room=current_room,
            player_handler=lambda: SimpleNamespace(room_registry=room_registry),
        )

        payload = commands.do_north(character, context)

        self.assertEqual("The gate is closed.\r\n", payload["to_char"])
        self.assertFalse(hasattr(context, "move_keyword"))

    def test_direction_success_moves_character_after_check_passes(self):
        commands, room_registry = self._commands()
        current_room = _Room(id="room-1", exits={0: _Exit(to_room_vnum="200", to_room_id="room-2", exit_flags=0, keyword="door")}, sector_type="field")
        destination = _Room(id="room-2", exits={}, sector_type="field")

        def _get_or_none(**kwargs):
            if kwargs.get("id") == "room-1":
                return current_room
            if kwargs.get("vnum") == "200":
                return destination
            return None

        room_registry.get_or_none = _get_or_none
        character = SimpleNamespace(
            id="char-1",
            name="Tester",
            room_id="room-1",
            movement=5,
            character_attributes=SimpleNamespace(position="POS_STANDING"),
            status_flags=SimpleNamespace(invis_level=0),
            effects={},
            has_boat=lambda: False,
        )
        context = _Context(
            character=character,
            command=_load_command("north"),
            done=False,
            room=current_room,
            player_handler=lambda: SimpleNamespace(room_registry=room_registry),
        )

        payload = commands.do_north(character, context)

        self.assertEqual("room-2", character.room_id)
        self.assertEqual(4, character.movement)
        self.assertEqual("Tester leaves north.\r\n", payload["from_room_message"])
        self.assertEqual("Tester has arrived.\r\n", payload["to_room_message"])
        self.assertFalse(hasattr(context, "move_cost"))


if __name__ == "__main__":
    unittest.main()
