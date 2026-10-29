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


def _ensure_injector():
    current = sys.modules.get("injector")
    if current is not None and hasattr(current, "Injector"):
        return
    sys.modules.pop("injector", None)
    try:
        import injector  # noqa: F401
    except ImportError:
        _stub_module("injector", inject=lambda target: target, Injector=object, singleton=lambda target: target)


def _stub_module_if_missing(name: str, **attrs):
    if name not in sys.modules:
        _stub_module(name, **attrs)


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
        if _name == "gameParameters":
            return SimpleNamespace(ANGEL=53, IMPLEMENTOR=60)
        if _name == "exitFlags":
            return _enum_like(
                EX_CLOSED=SimpleNamespace(value=1),
                EX_NOPASS=SimpleNamespace(value=2),
                EX_LOCKED=SimpleNamespace(value=4),
                EX_PICKPROOF=SimpleNamespace(value=8),
                EX_ISDOOR=SimpleNamespace(value=16),
            )
        if _name == "roomFlags":
            return _enum_like(ROOM_NO_RECALL=SimpleNamespace(value=1))
        if _name == "containerState":
            return _enum_like(
                CONT_CLOSEABLE=SimpleNamespace(value=1),
                CONT_CLOSED=SimpleNamespace(value=4),
                CONT_LOCKED=SimpleNamespace(value=8),
            )
        if _name == "affectedBy":
            return _enum_like(AFF_CHARM=SimpleNamespace(value=262144))
        if _name == "sectorTypes":
            return _enum_like()
        return _enum_like()

    @staticmethod
    def skill_value_for_class(values: dict, class_name: str, default: int = 0) -> int:
        class_name = str(class_name or "").strip().lower()
        for key, value in dict(values or {}).items():
            if str(key).strip().lower() == class_name:
                return int(value)
        return default

    @staticmethod
    def can_see(_character, _target, _room) -> bool:
        return True

    @staticmethod
    def can_see_room(_character, room):
        return room is not None

    @staticmethod
    def classes_map():
        return {}

    @staticmethod
    def get_trust(character):
        return getattr(character, "level", 1)

    @staticmethod
    def is_set(flags, bit) -> bool:
        return (int(flags or 0) & int(bit or 0)) != 0

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

    @classmethod
    def set_position(cls, character, pos_name: str):
        value = cls.pos_value(pos_name)
        attrs = getattr(character, "character_attributes", None)
        if attrs is not None:
            attrs.position = value
        character.position = value


class _MovementUtil:
    DIR_NAME = ["north", "east", "south", "west", "up", "down"]
    REV_DIR = [2, 3, 0, 1, 5, 4]

    @staticmethod
    def direction_index(direction: str) -> int:
        return {"north": 0, "east": 1, "south": 2, "west": 3, "up": 4, "down": 5}.get(direction, -1)

    @staticmethod
    def sector_cost(_sector_type) -> int:
        return 1


class _EnumLike(SimpleNamespace):
    def __getitem__(self, name):
        return self.__members__[name]


def _enum_like(**members):
    enum_obj = _EnumLike(**members)
    enum_obj.__members__ = members
    return enum_obj


class _Context(SimpleNamespace):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        character = getattr(self, "character", None)
        if character is not None and not hasattr(character, "owned_items"):
            character.owned_items = lambda: getattr(character, "loot", [])
            character.equipped_slot_of = lambda _item: None
    def finish(self):
        self.done = True


_ensure_injector()
_stub_package("server")
_stub_module("server.LoggerFactory", LoggerFactory=_LoggerFactory)
_stub_package("util")
_load_module("util.GenericUtil", "util/GenericUtil.py")
_stub_module("util.MovementUtil", MovementUtil=_MovementUtil)
_stub_module("util.MobileUtil", MobileUtil=SimpleNamespace(is_train_trainer=lambda *_args, **_kwargs: False))
_stub_module("util.CommunicationsUtil", CommunicationsUtil=SimpleNamespace(
    ensure_message_break=lambda text: text if str(text).endswith("\r\n") else f"{text}\r\n",
    split_first=lambda text: tuple(((text or "").split(maxsplit=1) + ["", ""])[:2]),
))
_stub_module("util.FightUtil", FightUtil=SimpleNamespace())
_stub_module("util.InterpUtil", InterpUtil=SimpleNamespace(argument_text=lambda view: str(getattr(view.context, "result", "") or "")))
_stub_module("util.ItemUtil", ItemUtil=SimpleNamespace())
_stub_module("util.WizUtil", WizUtil=SimpleNamespace())
_stub_package("game")
_stub_module("game.GameData", GameData=object)
_stub_module("game.RegistryService", RegistryService=object)
_load_module("game.GamePayload", "game/GamePayload.py")
_stub_package("area")
_stub_module("area.Room", Room=object)
_stub_package("combat")
_stub_module_if_missing("combat.FightHandler", FightHandler=object)
_stub_module_if_missing("combat.CombatHandler", FightHandler=object)
_stub_package("player")
_stub_module("player.Character", Character=object)
_stub_module("player.CharacterApi", CharacterMacros=_CharacterMacros)
_stub_package("api")
_stub_module("api.CharacterApi", CharacterApi=_CharacterMacros)
_stub_module("api.CommunicationsApi", CommunicationsApi=SimpleNamespace())
_stub_module("api.ItemApi", ItemApi=SimpleNamespace(can_see_object=lambda *_args: True))
_stub_module("api.WizApi", WizApi=SimpleNamespace())
_stub_package("interp")
_stub_module("interp.Context", Context=_Context)
_stub_package("item")
_stub_module(
    "item.Item",
    Item=SimpleNamespace(
        short=lambda item: getattr(item, "short_description", "") or getattr(item, "name", "") or "it",
        is_container=lambda item: "container" in str(getattr(item, "item_type", "") or "").lower(),
        enum_type_name=lambda item: "ITEM_" + str(item.item_type).upper().removeprefix("ITEM_"),
    ),
)

Command = _load_module("interp.Command", "interp/Command.py").Command
_load_module("interp.InterpView", "interp/InterpView.py")
_load_module("util.InterpUtil", "util/InterpUtil.py")
_load_module("interp.InterpCheck", "interp/InterpCheck.py")
_load_module("interp.InterpActionDefinition", "interp/InterpActionDefinition.py")
_load_module("interp.InterpPlan", "interp/InterpPlan.py")
InterpApi = _load_module("interp.InterpApi", "api/InterpApi.py").InterpApi
if "api.MovementApi" not in sys.modules:
    _load_module("api.MovementApi", "api/MovementApi.py")
MovementApi = sys.modules["api.MovementApi"].MovementApi
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
    def __init__(self, **kwargs):
        kwargs['exit_flags'] = kwargs.get('exit_flags', 0) | 16
        super().__init__(**kwargs)


class _Room(SimpleNamespace):
    def get_exit(self, direction: int):
        return self.exits.get(direction)

    def find_door(self, arg: str) -> int:
        direction = _MovementUtil.direction_index(arg)
        if direction >= 0:
            return direction if self.get_exit(direction) is not None else -1
        wanted = (arg or "").strip().lower()
        for direction, ex in getattr(self, "exits", {}).items():
            keyword = str(getattr(ex, "keyword", "") or "").lower()
            if wanted == keyword or wanted in keyword.split():
                return int(direction)
        return -1

    def find_room_item(self, wanted: str):
        q = (wanted or "").strip().lower()
        if not q:
            return None
        for item in getattr(self, "contents", {}).values():
            name = str(getattr(item, "name", "") or "").lower()
            if name == q or name.startswith(q):
                return item
        return None

    def player_targets(self, _character):
        return [character for character in getattr(self, "characters", {}).values() if character != _character]

    def remove_player_from_room(self, character):
        if not hasattr(self, "characters"):
            self.characters = {}
        self.characters.pop(character.id, None)
        self.removed = character.id

    def add_player_to_room(self, character):
        if not hasattr(self, "characters"):
            self.characters = {}
        self.characters[character.id] = character
        self.added = character.id

    def remove_mobile_from_room(self, mobile):
        if not hasattr(self, "mobiles"):
            self.mobiles = {}
        self.mobiles.pop(mobile.id, None)
        self.removed = mobile.id

    def add_mobile_to_room(self, mobile):
        if not hasattr(self, "mobiles"):
            self.mobiles = {}
        self.mobiles[mobile.id] = mobile
        self.added = mobile.id

    def people(self):
        return list(getattr(self, "characters", {}).values()) + list(getattr(self, "mobiles", {}).values())

    def is_private(self, _room_flags):
        return bool(getattr(self, "private_room", False))

    def is_air_room(self, _sector_types):
        return bool(getattr(self, "air_room", False))

    def requires_boat(self, _sector_types):
        return bool(getattr(self, "boat_required", False))


class TestMovementDynamicCommands(unittest.TestCase):
    def _commands(self, *, group_registry=None, skill_registry=None, spell_registry=None):
        registry_service = SimpleNamespace(
            room_registry=SimpleNamespace(get_or_none=lambda **_kwargs: None),
            group_registry=group_registry or SimpleNamespace(all_groups=lambda: []),
            skill_registry=skill_registry or SimpleNamespace(all_skills=lambda: []),
            spell_registry=spell_registry or SimpleNamespace(all_spells=lambda: []),
        )
        commands = Movement(
            registry_service=registry_service,
            game_data=SimpleNamespace(),
            fight_handler=SimpleNamespace(aggressive_entry_rounds=lambda *_args, **_kwargs: []),
            enum_provider=SimpleNamespace(get=lambda _name: SimpleNamespace()),
            interp_api=InterpApi(),
            skill_api=SimpleNamespace(),
            effect_handler=SimpleNamespace(),
        )
        commands.exit_flags = _CharacterMacros.get_enum("exitFlags")
        commands.room_flags = _CharacterMacros.get_enum("roomFlags")
        commands.affected_bits = SimpleNamespace()
        commands.item_types = SimpleNamespace(ITEM_PORTAL=SimpleNamespace(value=29))
        commands.gate_flags = SimpleNamespace(
            GATE_NORMAL_EXIT=SimpleNamespace(value=1),
            GATE_NOCURSE=SimpleNamespace(value=2),
            GATE_GOWITH=SimpleNamespace(value=4),
            GATE_BUGGY=SimpleNamespace(value=8),
            GATE_RANDOM=SimpleNamespace(value=16),
        )
        commands.act_bits = SimpleNamespace(ACT_GAIN=SimpleNamespace(value=1), ACT_AGGRESSIVE=SimpleNamespace(value=2))
        commands.sector_types = SimpleNamespace()
        return commands, registry_service.room_registry

    def test_direction_invalid_exit_uses_command_check(self):
        commands, room_registry = self._commands()
        room_registry.get_or_none = lambda **kwargs: None if "id" in kwargs else None
        character = SimpleNamespace(
            id="char-1",
            name="Tester",
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
            name="Tester",
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
        self.assertEqual("default", payload["payloads"][0]["message_key"])
        self.assertEqual("arrived", payload["payloads"][1]["message_key"])
        self.assertEqual("to_room", payload["payloads"][0]["channel"])
        self.assertEqual("to_room", payload["payloads"][1]["channel"])
        self.assertEqual("Tester leaves north.", context.command.render_message("to_room", payload["payloads"][0]["message_key"], **payload["payloads"][0]["tokens"]))
        self.assertEqual("Tester has arrived.", context.command.render_message("to_room", payload["payloads"][1]["message_key"], **payload["payloads"][1]["tokens"]))
        self.assertIs(destination, payload["payloads"][1]["to_room_obj"])

    def test_direction_success_moves_standing_followers_with_master(self):
        commands, room_registry = self._commands()
        current_room = _Room(id="room-1", exits={0: _Exit(to_room_vnum="200", to_room_id="room-2", exit_flags=0, keyword="door")}, sector_type="field", characters={})
        destination = _Room(id="room-2", exits={}, sector_type="field", characters={})

        def _get_or_none(**kwargs):
            if kwargs.get("id") == "room-1":
                return current_room
            if kwargs.get("vnum") == "200":
                return destination
            return None

        room_registry.get_or_none = _get_or_none
        leader = SimpleNamespace(
            id="leader",
            name="Leader",
            room_id="room-1",
            movement=5,
            character_attributes=SimpleNamespace(position="POS_STANDING"),
            status_flags=SimpleNamespace(invis_level=0),
            effects={},
            has_boat=lambda: False,
        )
        follower = SimpleNamespace(
            id="follower",
            name="Follower",
            room_id="room-1",
            movement=5,
            master=leader,
            character_attributes=SimpleNamespace(position="POS_STANDING"),
            status_flags=SimpleNamespace(invis_level=0),
            effects={},
            has_boat=lambda: False,
        )
        current_room.characters = {leader.id: leader, follower.id: follower}
        context = _Context(
            character=leader,
            command=_load_command("north"),
            done=False,
            room=current_room,
            player_handler=lambda: SimpleNamespace(room_registry=room_registry),
        )

        payload = commands.do_north(leader, context)

        self.assertEqual("room-2", leader.room_id)
        self.assertEqual("room-2", follower.room_id)
        self.assertNotIn("leader", current_room.characters)
        self.assertNotIn("follower", current_room.characters)
        self.assertIn("leader", destination.characters)
        self.assertIn("follower", destination.characters)
        self.assertEqual("Follower leaves north.", context.command.render_message("to_room", payload["payloads"][2]["message_key"], **payload["payloads"][2]["tokens"]))
        self.assertEqual(
            [{"id": "follower", "text": "You follow Leader.\r\n"}],
            payload["payloads"][-1]["target_messages"],
        )

    def test_open_invalid_door_uses_guard_payload(self):
        commands, room_registry = self._commands()
        room = _Room(id="room-1", exits={}, sector_type="field")
        room_registry.get_or_none = lambda **kwargs: room if kwargs.get("id") == "room-1" else None
        character = SimpleNamespace(
            id="char-1",
            name="Tester",
            room_id="room-1",
            movement=5,
            character_attributes=SimpleNamespace(position="POS_STANDING"),
            status_flags=SimpleNamespace(invis_level=0),
            effects={},
        )
        context = _Context(
            character=character,
            command=_load_command("open"),
            result="gate",
            parameters=[],
            done=False,
            room=room,
            player_handler=lambda: SimpleNamespace(room_registry=room_registry),
        )

        payload = commands.do_open(character, context)

        self.assertEqual("I see no door here.\r\n", payload["to_char"])

    def test_open_success_returns_standard_payload_message_key(self):
        commands, room_registry = self._commands()
        exit_obj = _Exit(direction=0, to_room_id="room-2", exit_flags=1, keyword="gate")
        current_room = _Room(id="room-1", exits={0: exit_obj}, sector_type="field")
        destination = _Room(id="room-2", exits={2: _Exit(direction=2, to_room_id="room-1", exit_flags=1, keyword="gate")}, sector_type="field")

        def _get_or_none(**kwargs):
            if kwargs.get("id") == "room-1":
                return current_room
            if kwargs.get("id") == "room-2":
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
        )
        context = _Context(
            character=character,
            command=_load_command("open"),
            result="gate",
            parameters=[],
            done=False,
            room=current_room,
            player_handler=lambda: SimpleNamespace(room_registry=room_registry),
        )

        payload = commands.do_open(character, context)

        self.assertEqual("lock_success", payload["message_key"])
        self.assertEqual("You open gate.", context.command.render_message("to_char", payload["message_key"], **payload["tokens"]))
        self.assertEqual("Tester opens gate.", context.command.render_message("to_room", payload["message_key"], **payload["tokens"]))
        self.assertEqual(16, exit_obj.exit_flags)

    def test_close_container_returns_container_payload(self):
        commands, room_registry = self._commands()
        room = _Room(id="room-1", exits={}, sector_type="field", contents={})
        room_registry.get_or_none = lambda **kwargs: room if kwargs.get("id") == "room-1" else None
        chest = SimpleNamespace(
            id="obj-1",
            name="chest wooden",
            short_description="a wooden chest",
            item_type="container",
            value1="1",
            value2="-1",
        )
        chest.short = lambda: "a wooden chest"
        character = SimpleNamespace(
            id="char-1",
            name="Tester",
            room_id="room-1",
            movement=5,
            loot=[chest],
            character_attributes=SimpleNamespace(position="POS_STANDING"),
            status_flags=SimpleNamespace(invis_level=0),
            effects={},
            find_inventory_item=lambda wanted: chest if wanted == "chest" else None,
        )
        context = _Context(
            character=character,
            command=_load_command("close"),
            result="chest",
            parameters=[],
            done=False,
            room=room,
            player_handler=lambda: SimpleNamespace(room_registry=room_registry),
        )

        payload = commands.do_close(character, context)

        self.assertEqual("lock_success", payload["message_key"])
        self.assertEqual("You close a wooden chest.", context.command.render_message("to_char", payload["message_key"], **payload["tokens"]))
        self.assertEqual("%c closes %t.".replace("%c", "Tester").replace("%t", "a wooden chest"), context.command.render_message("to_room", payload["message_key"], **payload["tokens"]))
        self.assertEqual("5", chest.value1)

    def test_lock_container_returns_container_payload(self):
        commands, room_registry = self._commands()
        room = _Room(id="room-1", exits={}, sector_type="field", contents={})
        room_registry.get_or_none = lambda **kwargs: room if kwargs.get("id") == "room-1" else None
        chest = SimpleNamespace(
            id="obj-2",
            name="chest iron",
            short_description="an iron chest",
            item_type="container",
            value1="5",
            value2="123",
        )
        chest.short = lambda: "an iron chest"
        character = SimpleNamespace(
            id="char-1",
            name="Tester",
            room_id="room-1",
            movement=5,
            loot=[chest, SimpleNamespace(vnum="123")],
            character_attributes=SimpleNamespace(position="POS_STANDING"),
            status_flags=SimpleNamespace(invis_level=0),
            effects={},
            find_inventory_item=lambda wanted: chest if wanted == "chest" else None,
            has_key=lambda key: key == 123,
        )
        context = _Context(
            character=character,
            command=_load_command("lock"),
            result="chest",
            parameters=[],
            done=False,
            room=room,
            player_handler=lambda: SimpleNamespace(room_registry=room_registry),
        )

        payload = commands.do_lock(character, context)

        self.assertEqual("lock_success", payload["message_key"])
        self.assertEqual("You lock an iron chest.", context.command.render_message("to_char", payload["message_key"], **payload["tokens"]))
        self.assertEqual("%c locks %t.".replace("%c", "Tester").replace("%t", "an iron chest"), context.command.render_message("to_room", payload["message_key"], **payload["tokens"]))
        self.assertEqual("13", chest.value1)

    def test_enter_gain_and_go_metadata_route_to_movement_handler(self):
        with open(COMMANDS_PATH, "r", encoding="utf-8") as handle:
            commands = {entry.get("name"): entry for entry in json.load(handle)}

        self.assertEqual(["lambda ctx: ctx.player_handler().do_enter(ctx.character, ctx)"], commands["enter"]["lambdas"])
        self.assertEqual(["lambda ctx: ctx.player_handler().do_gain(ctx.character, ctx)"], commands["gain"]["lambdas"])
        self.assertEqual(["lambda ctx: ctx.player_handler().do_go(ctx.character, ctx)"], commands["go"]["lambdas"])

    def test_enter_portal_moves_character_to_destination(self):
        commands, room_registry = self._commands()
        portal = SimpleNamespace(
            id="portal-1",
            name="portal shimmering",
            short_description="a shimmering portal",
            item_type="ITEM_PORTAL",
            value0="0",
            value1="0",
            value2="1",
            value3="200",
        )
        current_room = _Room(id="room-1", vnum="100", exits={}, sector_type="field", contents={portal.id: portal}, characters={})
        destination = _Room(id="room-2", vnum="200", exits={}, sector_type="field", contents={}, characters={})

        def _get_or_none(**kwargs):
            if kwargs.get("id") == "room-1":
                return current_room
            if kwargs.get("id") == "room-2" or kwargs.get("vnum") == "200":
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
            is_npc=False,
            has_boat=lambda: False,
        )
        current_room.characters = {character.id: character}
        context = _Context(
            character=character,
            command=_load_command("enter"),
            result="portal",
            parameters=[],
            done=False,
            room=current_room,
            player_handler=lambda: SimpleNamespace(room_registry=room_registry),
        )

        payload = commands.do_enter(character, context)

        self.assertEqual("room-2", character.room_id)
        self.assertNotIn(character.id, current_room.characters)
        self.assertIn(character.id, destination.characters)
        self.assertEqual("steps_into", payload["payloads"][0]["message_key"])
        self.assertEqual("enter", payload["payloads"][1]["message_key"])
        self.assertEqual("arrived", payload["payloads"][2]["message_key"])
        self.assertEqual("You enter a shimmering portal.", context.command.render_message("to_char", "enter", **payload["payloads"][1]["tokens"]))
        self.assertIs(destination, payload["payloads"][2]["to_room_obj"])

    def test_gain_prefixes_and_invalid_suffixes(self):
        for argument, expected, practices, trains, points in (
            ("con", "helps_apply_practice_training", 0, 6, 50),
            ("CON extra", "helps_apply_practice_training", 0, 6, 50),
            ("po", "trains_feel_more_at", 10, 3, 49),
            ("convertjunk", "tells_i_do_not", 10, 5, 50),
            ("pointsjunk", "tells_i_do_not", 10, 5, 50),
            ("listjunk", "tells_i_do_not", 10, 5, 50),
            ("''", "tells_i_do_not", 10, 5, 50),
        ):
            with self.subTest(argument=argument):
                commands, _ = self._commands()
                trainer = SimpleNamespace(name="Trainer", status_flags=SimpleNamespace(act=1))
                room = _Room(id="room-1", exits={}, sector_type="field", mobiles={"trainer": trainer})
                attrs = SimpleNamespace(practices=10, trains=5, points=50)
                character = SimpleNamespace(name="Tester", is_npc=False, character_attributes=attrs,
                                            level=10, character_race=SimpleNamespace(class_mult=100))
                context = _Context(character=character, result=argument, parameters=[], room=room, done=False)
                payload = commands.do_gain(character, context)
                self.assertEqual(expected, payload["message_key"])
                self.assertEqual((practices, trains, points), (attrs.practices, attrs.trains, attrs.points))
                self.assertTrue(context.done)

    def test_gain_group_preserves_proficiency_expands_cycles_and_tracks_ownership(self):
        root = SimpleNamespace(name="mage default", skills=["sword", "combat"], spells=["combat", "missing"], rating=[2]*4)
        nested = SimpleNamespace(name="combat", skills=["sword", "dagger"],
                                 spells=["magic missile", "heal", "mage default"], rating=[1]*4)
        skills = [SimpleNamespace(name=name) for name in ("sword", "dagger")]
        spells = [SimpleNamespace(name="magic missile"), SimpleNamespace(name="heal")]
        commands, _ = self._commands(
            group_registry=SimpleNamespace(all_groups=lambda: [root, nested]),
            skill_registry=SimpleNamespace(all_skills=lambda: skills),
            spell_registry=SimpleNamespace(all_spells=lambda: spells))
        character = SimpleNamespace(skills=[{"name": "sword", "level": 80}, {"name": "dagger", "level": 0}],
                                    spells=[{"name": "magic missile", "level": 60}],
                                    groups=[], character_class=SimpleNamespace(name="mage"),
                                    character_attributes=SimpleNamespace(trains=5), is_npc=False)
        self.assertFalse(commands._knows_group(character, root))
        trainer = SimpleNamespace(name="Trainer", status_flags=SimpleNamespace(act=1))
        room = _Room(id="room-1", exits={}, sector_type="field", mobiles={"trainer": trainer})
        context = _Context(character=character, result="mage default", parameters=[], room=room)
        payload = commands.do_gain(character, context)
        self.assertEqual("trains_art", payload["message_key"])
        self.assertEqual(3, character.character_attributes.trains)
        self.assertEqual([{"name": "sword", "level": 80}, {"name": "dagger", "level": 1}], character.skills)
        self.assertEqual([{"name": "magic missile", "level": 60}, {"name": "heal", "level": 1}], character.spells)
        self.assertEqual(["mage default", "combat"], character.groups)
        self.assertTrue(commands._knows_group(character, nested))
        payload = commands.do_gain(character, context)
        self.assertEqual("tells_already_know_group", payload["message_key"])
        self.assertEqual(3, character.character_attributes.trains)
        commands._add_group(character, root)
        self.assertEqual(["mage default", "combat"], character.groups)

    def test_gain_can_purchase_group_when_all_members_are_individually_known(self):
        group = SimpleNamespace(name="weapons", skills=["sword"], spells=[], rating=[2]*4)
        commands, _ = self._commands(
            group_registry=SimpleNamespace(all_groups=lambda: [group]),
            skill_registry=SimpleNamespace(all_skills=lambda: [SimpleNamespace(name="sword")]))
        character = SimpleNamespace(skills=[{"name": "sword", "level": 90}], spells=[],
                                    groups=[], is_npc=False, character_class=SimpleNamespace(name="warrior"),
                                    character_attributes=SimpleNamespace(trains=2))
        self.assertFalse(commands._knows_group(character, group))
        self.assertIn("weapons", commands._gain_list(character))
        trainer = SimpleNamespace(name="Trainer", status_flags=SimpleNamespace(act=1))
        room = _Room(id="room-1", exits={}, sector_type="field", mobiles={"trainer": trainer})
        context = _Context(character=character, result="weapons", parameters=[], room=room)
        self.assertEqual("trains_art", commands.do_gain(character, context)["message_key"])
        self.assertEqual(0, character.character_attributes.trains)
        self.assertEqual(90, character.skills[0]["level"])
        self.assertEqual(["weapons"], character.groups)

    def test_gain_points_recalculates_cost_and_resets_level_progress(self):
        from player.CharacterAdvancement import CharacterAdvancement
        from unittest.mock import patch

        commands, _ = self._commands()
        trainer = SimpleNamespace(name="Trainer", status_flags=SimpleNamespace(act=1))
        room = _Room(id="room-1", exits={}, sector_type="field", mobiles={"trainer": trainer})
        for points, trains, expected_key in ((50, 2, "trains_feel_more_at"),
                                             (40, 2, "tells_would_no_point"),
                                             (50, 1, "tells_not_yet_ready2")):
            with self.subTest(points=points, trains=trains):
                attrs = SimpleNamespace(points=points, trains=trains, experience_per_level=1500,
                                        experience=700, accumulated_experience=15700)
                character = SimpleNamespace(name="Tester", level=10, is_npc=False,
                                            character_race=SimpleNamespace(class_mult=100),
                                            character_attributes=attrs)
                context = _Context(character=character, result="points", parameters=[], room=room)
                payload = commands.do_gain(character, context)
                self.assertEqual(expected_key, payload["message_key"])
                self.assertEqual(10, character.level)
                if points == 50 and trains == 2:
                    self.assertEqual((49, 0, 1450, 0, 14500),
                                     (attrs.points, attrs.trains, attrs.experience_per_level,
                                      attrs.experience, attrs.accumulated_experience))
                    # Subsequent XP awards use the newly cached cost.
                    with patch.object(CharacterAdvancement, "advance_level") as advance:
                        CharacterAdvancement.gain_experience(character, 1449)
                        advance.assert_not_called()
                        CharacterAdvancement.gain_experience(character, 1)
                        advance.assert_called_once()
                    self.assertEqual(11, character.level)
                    self.assertEqual(0, attrs.experience)
                    self.assertEqual(15950, attrs.accumulated_experience)
                else:
                    self.assertEqual((points, trains, 1500, 700, 15700),
                                     (attrs.points, attrs.trains, attrs.experience_per_level,
                                      attrs.experience, attrs.accumulated_experience))

    def test_creation_point_experience_formula(self):
        from player.CharacterAdvancement import CharacterAdvancement

        character = SimpleNamespace(is_npc=False, character_race=SimpleNamespace(class_mult=100))
        for points, expected in ((39, 1000), (40, 1000), (41, 1050), (49, 1450),
                                 (50, 1500), (59, 1950), (60, 2000), (61, 2100),
                                 (70, 3000), (80, 4000), (81, 4200), (90, 6000)):
            with self.subTest(points=points):
                self.assertEqual(expected, CharacterAdvancement.experience_per_level(character, points))
        character.character_race.class_mult = 125
        self.assertEqual(1812, CharacterAdvancement.experience_per_level(character, 49))
        character.is_npc = True
        self.assertEqual(1000, CharacterAdvancement.experience_per_level(character, 90))

    def test_gain_list_prefix(self):
        commands, _ = self._commands()
        trainer = SimpleNamespace(status_flags=SimpleNamespace(act=1))
        room = _Room(id="room-1", exits={}, sector_type="field", mobiles={"trainer": trainer})
        character = SimpleNamespace(is_npc=False)
        context = _Context(character=character, result="li extra", parameters=[], room=room)
        self.assertIn("group", commands.do_gain(character, context)["to_char"])

    def test_gain_requires_current_trainer_flag(self):
        commands, _ = self._commands()
        trainer = SimpleNamespace(status_flags=SimpleNamespace(act=0), mobile_flags=SimpleNamespace(act=1))
        room = _Room(id="room-1", exits={}, sector_type="field", mobiles={"trainer": trainer})
        character = SimpleNamespace(is_npc=False)
        context = _Context(character=character, result="con", parameters=[], room=room)
        self.assertEqual("can_t_do", commands.do_gain(character, context)["message_key"])

    def test_gain_name_prefix_uses_registry_order(self):
        first = SimpleNamespace(name="sword mastery")
        second = SimpleNamespace(name="sword")
        registry = SimpleNamespace(get_or_none=lambda **kwargs: second)
        self.assertIs(first, Movement._find_gain_entry("SWO", [first, second], registry))
        self.assertIs(first, Movement._find_gain_entry("sword", [first, second], registry))
        self.assertIsNone(Movement._find_gain_entry("swordjunk", [first, second], None))
        self.assertIsNone(Movement._find_gain_entry("", [first, second], registry))
        commands, _ = self._commands(
            group_registry=SimpleNamespace(all_groups=lambda: [SimpleNamespace(name="combat magic")]),
            spell_registry=SimpleNamespace(all_spells=lambda: [SimpleNamespace(name="fireball")]),
        )
        self.assertEqual("combat magic", commands._find_gain_group("combat m").name)
        self.assertEqual("fireball", commands._find_gain_spell("fireb").name)

    def test_gain_convert_turns_ten_practices_into_one_train(self):
        commands, room_registry = self._commands()
        trainer = SimpleNamespace(id="trainer", name="Trainer", short_description="A gain trainer", status_flags=SimpleNamespace(act=1))
        room = _Room(id="room-1", exits={}, sector_type="field", mobiles={trainer.id: trainer})
        room_registry.get_or_none = lambda **kwargs: room if kwargs.get("id") == "room-1" else None
        attrs = SimpleNamespace(position="POS_STANDING", practices=10, trains=0, points=40)
        character = SimpleNamespace(
            id="char-1",
            name="Tester",
            room_id="room-1",
            character_attributes=attrs,
            character_class=SimpleNamespace(name="thief"),
            skills=[],
            spells=[],
            is_npc=False,
        )
        context = _Context(character=character, command=_load_command("gain"), result="convert", parameters=[], done=False, room=room)

        payload = commands.do_gain(character, context)

        self.assertEqual(0, attrs.practices)
        self.assertEqual(1, attrs.trains)
        self.assertEqual("helps_apply_practice_training", payload["message_key"])
        self.assertEqual(
            "A gain trainer helps you apply your practice to training",
            context.command.render_message("to_char", payload["message_key"], **payload["tokens"]),
        )

    def test_gain_skill_purchase_spends_trains_and_adds_skill(self):
        skill = SimpleNamespace(name="dagger", kind="skill", rating_by_class={"thief": 2})
        skill_registry = SimpleNamespace(all_skills=lambda: [skill])
        commands, room_registry = self._commands(skill_registry=skill_registry)
        trainer = SimpleNamespace(id="trainer", name="Trainer", short_description="A gain trainer", status_flags=SimpleNamespace(act=1))
        room = _Room(id="room-1", exits={}, sector_type="field", mobiles={trainer.id: trainer})
        room_registry.get_or_none = lambda **kwargs: room if kwargs.get("id") == "room-1" else None
        attrs = SimpleNamespace(position="POS_STANDING", practices=0, trains=2, points=40)
        character = SimpleNamespace(
            id="char-1",
            name="Tester",
            room_id="room-1",
            character_attributes=attrs,
            character_class=SimpleNamespace(name="thief"),
            skills=[],
            spells=[],
            is_npc=False,
        )
        context = _Context(character=character, command=_load_command("gain"), result="dag", parameters=[], done=False, room=room)

        payload = commands.do_gain(character, context)

        self.assertEqual(0, attrs.trains)
        self.assertEqual([{"name": "dagger", "level": 1}], character.skills)
        self.assertEqual("trains_art2", payload["message_key"])
        self.assertEqual(
            "A gain trainer trains you in the art of dagger",
            context.command.render_message("to_char", payload["message_key"], **payload["tokens"]),
        )


if __name__ == "__main__":
    unittest.main()
