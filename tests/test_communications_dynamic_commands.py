import json
import os
import sys
import unittest
from copy import deepcopy
from types import ModuleType
from types import SimpleNamespace
from unittest.mock import Mock

SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
RESOURCES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "collections", "SOMDB.Commands.json"))
sys.path.insert(0, SRC_PATH)


def _stub_package(package_name: str) -> None:
    if package_name in sys.modules:
        return
    package = ModuleType(package_name)
    package.__path__ = [os.path.join(SRC_PATH, package_name)]
    sys.modules[package_name] = package


for package_name in ["area", "game", "interp", "player", "server", "util"]:
    _stub_package(package_name)

if "injector" not in sys.modules:
    sys.modules["injector"] = SimpleNamespace(inject=lambda target: target)


class _Context(SimpleNamespace):
    def finish(self):
        self.done = True

    def player_handler(self):
        handler_service = getattr(self, "handler_service", None)
        if handler_service is None:
            return None
        return handler_service.get_handler("ph")


sys.modules["interp.Context"] = SimpleNamespace(Context=_Context)


class _CharacterMacros:
    @staticmethod
    def get_enum(_name: str):
        return SimpleNamespace(
            COMM_DEAF=SimpleNamespace(value=1),
            COMM_QUIET=SimpleNamespace(value=2),
            COMM_AFK=SimpleNamespace(value=4),
            COMM_NOTELL=SimpleNamespace(value=8),
            COMM_NOGOSSIP=SimpleNamespace(value=16),
            COMM_NOAUCTION=SimpleNamespace(value=32),
            COMM_NOMUSIC=SimpleNamespace(value=64),
            COMM_NOQUESTION=SimpleNamespace(value=128),
            COMM_NOQUOTE=SimpleNamespace(value=256),
            COMM_NOGRATS=SimpleNamespace(value=512),
            COMM_NOWIZ=SimpleNamespace(value=1024),
            COMM_NOSHOUT=SimpleNamespace(value=2048),
            COMM_NOCHANNELS=SimpleNamespace(value=4096),
            COMM_NOEMOTE=SimpleNamespace(value=8192),
            COMM_SHOUTSOFF=SimpleNamespace(value=16384),
        )

    @staticmethod
    def find_playing_character(name: str, session_handler):
        wanted = (name or "").strip().lower()
        for session in session_handler.get_playing_sessions():
            character = getattr(session, "character", None)
            if character is None:
                continue
            current = str(getattr(character, "name", "") or "").lower()
            if current == wanted or current.startswith(wanted):
                return character
        return None

    @staticmethod
    def is_immortal(_character):
        return False


sys.modules["api.CharacterApi"] = SimpleNamespace(CharacterApi=_CharacterMacros)
sys.modules["player.CharacterApi"] = SimpleNamespace(CharacterMacros=_CharacterMacros)
sys.modules["player.Character"] = SimpleNamespace(Character=object)
sys.modules["game.RegistryService"] = SimpleNamespace(RegistryService=object)
sys.modules["player.CharacterService"] = SimpleNamespace(CharacterService=object)
sys.modules["server.session.SessionHandler"] = SimpleNamespace(SessionHandler=object)

from api.CommunicationsApi import BufferedMessage, CommunicationsApi
from api.InterpApi import InterpApi
from interp.Command import Command
from interp.commands.Communications import Communications


class _StatusFlags:
    def __init__(self, comm: int = 0):
        self.comm = comm

    def set_flag(self, name: str, bit: int):
        setattr(self, name, int(getattr(self, name, 0)) | int(bit))

    def unset_flag(self, name: str, bit: int):
        setattr(self, name, int(getattr(self, name, 0)) & ~int(bit))


class _HandlerService:
    def __init__(self, player_handler):
        self._player_handler = player_handler

    def get_handler(self, key: str):
        if key == "ph":
            return self._player_handler
        return None


class _LookupRegistry:
    def __init__(self, values_by_id=None):
        self.values_by_id = dict(values_by_id or {})

    def get_or_none(self, **kwargs):
        if "id" in kwargs:
            return self.values_by_id.get(kwargs["id"])
        return None


def _load_command(name: str) -> Command:
    with open(RESOURCES_PATH, "r", encoding="utf-8") as handle:
        commands = json.load(handle)
    for entry in commands:
        if entry.get("name") == name:
            payload = deepcopy(entry)
            payload.setdefault("shortcuts", "")
            payload.setdefault("function", [])
            payload.setdefault("usage", "")
            return Command.from_json(payload)
    raise KeyError(name)


def _character(name: str, character_id: str) -> SimpleNamespace:
    return SimpleNamespace(
        id=character_id,
        name=name,
        context={},
        status_flags=_StatusFlags(),
        area_id="area-1",
        room_id="room-1",
    )


class TestCommunicationsDynamicCommands(unittest.TestCase):
    def setUp(self):
        CommunicationsApi._tell_buffer = {}

    def test_interp_api_check_emits_all_payload_channels_for_message_key(self):
        command = Command.from_json(
            {
                "_id": {"$oid": "cmd-check"},
                "name": "demo",
                "shortcuts": "",
                "role": "player",
                "position": "POS_DEAD",
                "enabled": True,
                "lambdas": [],
                "function": [],
                "usage": "",
                "level": 0,
                "maxArguments": 0,
                "payload": {
                    "toChar": {"blockedEverywhere": "Actor blocked."},
                    "toRoom": {"blockedEverywhere": "%c cannot do that."},
                    "toVictim": {},
                },
                "guards": [
                    {
                        "predicate": "lambda v: True",
                        "messageKey": "blockedEverywhere",
                    }
                ],
            }
        )
        context = _Context(character=_character("Tester", "actor"), command=command, result="", parameters=[], done=False)

        payload = InterpApi().run_action(context, command.name)

        self.assertTrue(payload["blocked"])
        self.assertEqual("Actor blocked.\r\n", payload["to_char"])
        self.assertEqual("Tester cannot do that.\r\n", payload["to_room"])

    def test_do_tell_uses_command_check_for_missing_target(self):
        actor = _character("Actor", "actor")
        registry_service = SimpleNamespace(
            character_registry=_LookupRegistry(),
            room_registry=Mock(),
        )
        session_handler = Mock()
        session_handler.get_playing_sessions.return_value = []
        character_service = Mock()

        communications = Communications(registry_service, session_handler, character_service, SimpleNamespace(get=lambda _name: SimpleNamespace()), InterpApi())
        communications.lazy_load()

        player_handler = SimpleNamespace(communications_commands=communications, character_registry=registry_service.character_registry)
        context = _Context(
            character=actor,
            command=_load_command("tell"),
            handler_service=_HandlerService(player_handler),
            result="nobody hello there",
            parameters=[],
            done=False,
        )

        payload = communications.do_tell(actor, context)

        self.assertTrue(payload["blocked"])
        self.assertEqual("They aren't here.\r\n", payload["to_char"])

    def test_do_reply_uses_command_check_for_missing_message(self):
        actor = _character("Actor", "actor")
        victim = _character("Victim", "victim")
        actor.context["reply_to"] = victim.id
        registry_service = SimpleNamespace(
            character_registry=_LookupRegistry({victim.id: victim}),
            room_registry=Mock(),
        )
        session_handler = Mock()
        character_service = Mock()

        communications = Communications(registry_service, session_handler, character_service, SimpleNamespace(get=lambda _name: SimpleNamespace()), InterpApi())
        communications.lazy_load()

        player_handler = SimpleNamespace(communications_commands=communications, character_registry=registry_service.character_registry)
        context = _Context(
            character=actor,
            command=_load_command("reply"),
            handler_service=_HandlerService(player_handler),
            result="",
            parameters=[],
            done=False,
        )

        payload = communications.do_reply(actor, context)

        self.assertTrue(payload["blocked"])
        self.assertEqual("Reply what?\r\n", payload["to_char"])

    def test_do_save_uses_command_payload_for_failure_message(self):
        actor = _character("Actor", "actor")
        registry_service = SimpleNamespace(
            character_registry=_LookupRegistry(),
            room_registry=Mock(),
        )
        session_handler = Mock()
        character_service = Mock()
        character_service.save_character.return_value = False

        communications = Communications(registry_service, session_handler, character_service, SimpleNamespace(get=lambda _name: SimpleNamespace()), InterpApi())
        context = _Context(character=actor, command=_load_command("save"), result="", parameters=[], done=False)

        payload = communications.do_save(actor, context)

        self.assertEqual("Save failed.\r\n", payload["to_char"])

    def test_do_tell_buffers_victim_message_in_communications_api(self):
        actor = _character("Actor", "actor")
        victim = _character("Victim", "victim")
        registry_service = SimpleNamespace(
            character_registry=_LookupRegistry({victim.id: victim}),
            room_registry=Mock(),
        )
        session_handler = Mock()
        session_handler.get_playing_sessions.return_value = [SimpleNamespace(character=victim)]
        character_service = Mock()

        communications = Communications(registry_service, session_handler, character_service, SimpleNamespace(get=lambda _name: SimpleNamespace()), InterpApi())
        communications.lazy_load()

        context = _Context(
            character=actor,
            command=_load_command("tell"),
            result="Victim hello there",
            parameters=[],
            done=False,
        )

        payload = communications.do_tell(actor, context)

        self.assertEqual("You tell Victim 'hello there'\r\n", payload["to_char"])
        history = CommunicationsApi.get_tell_buffer(victim)
        self.assertEqual(1, len(history))
        self.assertEqual("Actor", history[0].sender)
        self.assertEqual("Actor tells you 'hello there'\r\n", history[0].message)

    def test_do_replay_reads_tells_from_communications_api_buffer(self):
        actor = _character("Actor", "actor")
        registry_service = SimpleNamespace(
            character_registry=_LookupRegistry(),
            room_registry=Mock(),
        )
        session_handler = Mock()
        character_service = Mock()
        CommunicationsApi._tell_buffer[actor.name] = [
            BufferedMessage(sender="Victim", message="Victim tells you 'hello'\r\n")
        ]

        communications = Communications(registry_service, session_handler, character_service, SimpleNamespace(get=lambda _name: SimpleNamespace()), InterpApi())
        communications.lazy_load()

        context = _Context(
            character=actor,
            command=_load_command("replay"),
            result="",
            parameters=[],
            done=False,
        )

        payload = communications.do_replay(actor, context)

        self.assertEqual("Victim tells you 'hello'\r\n", payload["to_char"])
        self.assertEqual([], CommunicationsApi.get_tell_buffer(actor))


if __name__ == "__main__":
    unittest.main()
