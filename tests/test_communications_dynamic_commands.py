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
        if _name == "playerActBits":
            return _enum_like(
                PLR_NOFOLLOW=SimpleNamespace(value=131072),
            )
        if _name == "affectedBy":
            return _enum_like(
                AFF_CHARM=SimpleNamespace(value=262144),
            )
        if _name == "gameParameters":
            return _enum_like(
                PULSE_VIOLENCE=SimpleNamespace(value=12),
                LEVEL_IMMORTAL=SimpleNamespace(value=55),
            )
        return _enum_like(
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
        return bool(getattr(_character, "immortal", False))

    @staticmethod
    def get_trust(character):
        return int(getattr(character, "trust", getattr(character, "level", 0)) or 0)

    @staticmethod
    def is_npc(character):
        return str(getattr(character, "role", "") or "").lower() == "mobile"

    @staticmethod
    def is_set(value, bit):
        return bool(int(value or 0) & int(getattr(bit, "value", bit) or 0))

    @staticmethod
    def enum_bit(enum_obj, bit_name: str) -> int:
        return int(getattr(getattr(enum_obj, bit_name, None), "value", 0) or 0)

    @staticmethod
    def unset_act_flags(character, bit: int):
        character.status_flags.unset_flag("act", bit)

    @staticmethod
    def can_see(viewer, target, _room=None):
        hidden_from = set(getattr(target, "hidden_from", set()) or set())
        return getattr(viewer, "id", None) not in hidden_from

    @staticmethod
    def is_same_group(left, right):
        if left is None or right is None:
            return False
        if getattr(left, "leader", None) is not None:
            left = left.leader
        if getattr(right, "leader", None) is not None:
            right = right.leader
        return left == right


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


class _EnumLike(SimpleNamespace):
    def __getitem__(self, name):
        return self.__members__[name]


def _enum_like(**members):
    enum_obj = _EnumLike(**members)
    enum_obj.__members__ = members
    return enum_obj


def _enum_provider():
    return SimpleNamespace(get=lambda name: _CharacterMacros.get_enum(name))


class _StatusFlags:
    def __init__(self, comm: int = 0, act: int = 0, affected_by: int = 0):
        self.comm = comm
        self.act = act
        self.affected_by = affected_by

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

    def all_rooms(self):
        return list(self.values_by_id.values())


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
        character_flags=SimpleNamespace(no_follow=False),
        area_id="area-1",
        room_id="room-1",
        role="player",
        sex="male",
        level=1,
        trust=0,
        hit=10,
        max_hit=10,
        mana=20,
        max_mana=20,
        movement=30,
        max_movement=30,
        gold=0,
        silver=0,
        character_class=SimpleNamespace(name="mage", who_name="Mag"),
        character_attributes=SimpleNamespace(experience=0),
        master=None,
        leader=None,
        immortal=False,
    )


class _Room:
    def __init__(self, *people):
        self.id = "room-1"
        self.characters = {person.id: person for person in people}
        self.mobiles = {}

    def people(self):
        return list(self.characters.values()) + list(self.mobiles.values())

    def find_visible_target(self, observer, wanted: str):
        query = (wanted or "").strip().lower()
        if query == "self":
            return observer
        for person in self.characters.values():
            if not _CharacterMacros.can_see(observer, person, self):
                continue
            name = str(getattr(person, "name", "") or "").lower()
            if name == query or name.startswith(query):
                return person
        return None


class TestCommunicationsDynamicCommands(unittest.TestCase):
    def setUp(self):
        CommunicationsApi._tell_buffer = {}
        CommunicationsApi.get_enum = classmethod(lambda _cls, name: _CharacterMacros.get_enum(name))

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

        communications = Communications(registry_service, session_handler, character_service, _enum_provider(), InterpApi())

        player_handler = SimpleNamespace(communications_commands=communications, character_registry=registry_service.character_registry)
        context = _Context(
            character=actor,
            command=_load_command("tell"),
            handler_service=_HandlerService(player_handler),
            result="nobody hello there",
            parameters=[],
            done=False,
        )

        payload = communications.do_tell(context)

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

        communications = Communications(registry_service, session_handler, character_service, _enum_provider(), InterpApi())

        player_handler = SimpleNamespace(communications_commands=communications, character_registry=registry_service.character_registry)
        context = _Context(
            character=actor,
            command=_load_command("reply"),
            handler_service=_HandlerService(player_handler),
            result="",
            parameters=[],
            done=False,
        )

        payload = communications.do_reply(context)

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

        communications = Communications(registry_service, session_handler, character_service, _enum_provider(), InterpApi())
        context = _Context(character=actor, command=_load_command("save"), result="", parameters=[], done=False)

        payload = communications.do_save(context)

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

        communications = Communications(registry_service, session_handler, character_service, _enum_provider(), InterpApi())

        context = _Context(
            character=actor,
            command=_load_command("tell"),
            result="Victim hello there",
            parameters=[],
            done=False,
        )

        payload = communications.do_tell(context)

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
            BufferedMessage(sender="Victim", message="hello")
        ]

        communications = Communications(registry_service, session_handler, character_service, _enum_provider(), InterpApi())

        context = _Context(
            character=actor,
            command=_load_command("replay"),
            result="",
            parameters=[],
            done=False,
        )

        payload = communications.do_replay(context)

        self.assertEqual("Victim tells you 'hello'\r\n", payload["to_char"])
        self.assertEqual([], CommunicationsApi.get_tell_buffer(actor))

    def _communications_for_room(self, room):
        registry_service = SimpleNamespace(
            character_registry=_LookupRegistry(),
            room_registry=_LookupRegistry({getattr(room, "id", "room-1"): room, "room-1": room}),
        )
        session_handler = Mock()
        character_service = Mock()
        return Communications(registry_service, session_handler, character_service, _enum_provider(), InterpApi())

    def _follow_context(self, actor, room, argument: str):
        return self._command_context("follow", actor, room, argument)

    def _command_context(self, command_name: str, actor, room, argument: str):
        communications = self._communications_for_room(room)
        player_handler = SimpleNamespace(
            communications_commands=communications,
            character_registry=communications.character_registry,
            room_registry=communications.room_registry,
        )
        return communications, _Context(
            character=actor,
            command=_load_command(command_name),
            handler_service=_HandlerService(player_handler),
            room=room,
            result=argument,
            parameters=[],
            done=False,
        )

    def test_do_follow_without_argument_matches_rom_message(self):
        actor = _character("Actor", "actor")
        room = _Room(actor)
        communications, context = self._follow_context(actor, room, "")

        payload = communications.do_follow(context)

        self.assertTrue(payload["blocked"])
        self.assertEqual("Follow whom?\r\n", payload["to_char"])

    def test_do_follow_self_without_master_matches_rom_message(self):
        actor = _character("Actor", "actor")
        room = _Room(actor)
        communications, context = self._follow_context(actor, room, "self")

        payload = communications.do_follow(context)

        self.assertTrue(payload["blocked"])
        self.assertEqual("You already follow yourself.\r\n", payload["to_char"])
        self.assertIsNone(actor.master)

    def test_do_follow_self_with_master_stops_following(self):
        actor = _character("Actor", "actor")
        leader = _character("Leader", "leader")
        actor.master = leader
        room = _Room(actor, leader)
        communications, context = self._follow_context(actor, room, "self")

        payload = communications.do_follow(context)

        self.assertIsNone(actor.master)
        self.assertEqual("You stop following Leader.\r\n", payload["to_char"])
        self.assertEqual("Actor stops following you.\r\n", payload["to_victim"])
        self.assertIs(payload["victim"], leader)

    def test_do_follow_charmed_with_master_is_blocked_before_self_stop(self):
        actor = _character("Actor", "actor")
        leader = _character("Leader", "leader")
        actor.master = leader
        actor.status_flags.set_flag("affected_by", 262144)
        room = _Room(actor, leader)
        communications, context = self._follow_context(actor, room, "self")

        payload = communications.do_follow(context)

        self.assertTrue(payload["blocked"])
        self.assertIs(actor.master, leader)
        self.assertEqual("But you'd rather follow Leader!\r\n", payload["to_char"])

    def test_do_follow_respects_target_nofollow_for_mortals(self):
        actor = _character("Actor", "actor")
        target = _character("Target", "target")
        target.status_flags.set_flag("act", 131072)
        room = _Room(actor, target)
        communications, context = self._follow_context(actor, room, "tar")

        payload = communications.do_follow(context)

        self.assertTrue(payload["blocked"])
        self.assertIsNone(actor.master)
        self.assertEqual("Target doesn't seem to want any followers.\r\n", payload["to_char"])

    def test_do_follow_sets_master_clears_nofollow_and_uses_resolved_name(self):
        actor = _character("Actor", "actor")
        actor.status_flags.set_flag("act", 131072)
        actor.character_flags.no_follow = True
        target = _character("Target", "target")
        room = _Room(actor, target)
        communications, context = self._follow_context(actor, room, "tar")

        payload = communications.do_follow(context)

        self.assertIs(actor.master, target)
        self.assertIsNone(actor.leader)
        self.assertFalse(_CharacterMacros.is_set(actor.status_flags.act, 131072))
        self.assertFalse(actor.character_flags.no_follow)
        self.assertEqual("You now follow Target.\r\n", payload["to_char"])
        self.assertEqual("Actor now follows you.\r\n", payload["to_victim"])
        self.assertIs(payload["victim"], target)

    def test_do_follow_changing_master_emits_stop_then_follow_payloads(self):
        actor = _character("Actor", "actor")
        old = _character("Old", "old")
        new = _character("New", "new")
        actor.master = old
        room = _Room(actor, old, new)
        communications, context = self._follow_context(actor, room, "new")

        payload = communications.do_follow(context)

        self.assertIs(actor.master, new)
        self.assertEqual(2, len(payload["payloads"]))
        self.assertEqual("You stop following Old.\r\n", payload["payloads"][0]["to_char"])
        self.assertEqual("Actor stops following you.\r\n", payload["payloads"][0]["to_victim"])
        self.assertIs(payload["payloads"][0]["victim"], old)
        self.assertEqual("You now follow New.\r\n", payload["payloads"][1]["to_char"])
        self.assertEqual("Actor now follows you.\r\n", payload["payloads"][1]["to_victim"])
        self.assertIs(payload["payloads"][1]["victim"], new)

    def test_do_follow_omits_victim_notice_when_target_cannot_see_actor(self):
        actor = _character("Actor", "actor")
        target = _character("Target", "target")
        actor.hidden_from = {target.id}
        room = _Room(actor, target)
        communications, context = self._follow_context(actor, room, "target")

        payload = communications.do_follow(context)

        self.assertIs(actor.master, target)
        self.assertEqual("You now follow Target.\r\n", payload["to_char"])
        self.assertNotIn("to_victim", payload)

    def test_do_order_blocks_delete_before_other_validation(self):
        actor = _character("Actor", "actor")
        room = _Room(actor)
        communications, context = self._command_context("order", actor, room, "all delete")

        payload = communications.do_order(context)

        self.assertTrue(payload["blocked"])
        self.assertEqual("That will NOT be done.\r\n", payload["to_char"])

    def test_do_order_rejects_non_charmed_target(self):
        actor = _character("Actor", "actor")
        target = _character("Target", "target")
        target.master = actor
        room = _Room(actor, target)
        communications, context = self._command_context("order", actor, room, "target smile")

        payload = communications.do_order(context)

        self.assertTrue(payload["blocked"])
        self.assertEqual("Do it yourself!\r\n", payload["to_char"])

    def test_do_order_all_targets_charmed_followers_and_sets_wait(self):
        actor = _character("Actor", "actor")
        follower = _character("Follower", "follower")
        follower.master = actor
        follower.status_flags.set_flag("affected_by", 262144)
        bystander = _character("Bystander", "bystander")
        bystander.status_flags.set_flag("affected_by", 262144)
        room = _Room(actor, follower, bystander)
        communications, context = self._command_context("order", actor, room, "all smile happily")

        payload = communications.do_order(context)

        self.assertEqual("Ok.\r\n", payload["to_char"])
        self.assertEqual(12, actor.status_flags.pulse_wait)
        self.assertEqual([{"victim": follower, "command": "smile happily"}], payload["ordered_commands"])
        self.assertEqual("ordered", payload["order_message_key"])

    def test_do_order_without_charmed_followers_matches_rom_message(self):
        actor = _character("Actor", "actor")
        room = _Room(actor)
        communications, context = self._command_context("order", actor, room, "all smile")

        payload = communications.do_order(context)

        self.assertTrue(payload["blocked"])
        self.assertEqual("You have no followers here.\r\n", payload["to_char"])

    def test_do_group_without_argument_lists_same_group(self):
        actor = _character("Actor", "actor")
        member = _character("Member", "member")
        member.leader = actor
        outsider = _character("Outsider", "outsider")
        room = _Room(actor, member, outsider)
        communications, context = self._command_context("group", actor, room, "")

        payload = communications.do_group(context)

        self.assertIn("Actor's group:\r\n", payload["to_char"])
        self.assertIn("[ 1 Mag] Actor", payload["to_char"])
        self.assertIn("[ 1 Mag] Member", payload["to_char"])
        self.assertNotIn("Outsider", payload["to_char"])

    def test_do_group_adds_follower_to_group(self):
        actor = _character("Actor", "actor")
        follower = _character("Follower", "follower")
        follower.master = actor
        room = _Room(actor, follower)
        communications, context = self._command_context("group", actor, room, "follower")

        payload = communications.do_group(context)

        self.assertIs(follower.leader, actor)
        self.assertEqual("Follower joins your group.\r\n", payload["to_char"])
        self.assertEqual("You join Actor's group.\r\n", payload["to_victim"])
        self.assertEqual("Follower joins Actor's group.\r\n", payload["to_room"])

    def test_do_group_removes_group_member(self):
        actor = _character("Actor", "actor")
        follower = _character("Follower", "follower")
        follower.master = actor
        follower.leader = actor
        room = _Room(actor, follower)
        communications, context = self._command_context("group", actor, room, "follower")

        payload = communications.do_group(context)

        self.assertIsNone(follower.leader)
        self.assertEqual("You remove Follower from your group.\r\n", payload["to_char"])
        self.assertEqual("Actor removes you from his group.\r\n", payload["to_victim"])

    def test_do_group_blocks_actor_following_someone_else(self):
        actor = _character("Actor", "actor")
        master = _character("Master", "master")
        follower = _character("Follower", "follower")
        actor.master = master
        follower.master = actor
        room = _Room(actor, master, follower)
        communications, context = self._command_context("group", actor, room, "follower")

        payload = communications.do_group(context)

        self.assertTrue(payload["blocked"])
        self.assertEqual("But you are following someone else!\r\n", payload["to_char"])

    def test_do_group_actor_charmed_sends_rom_message_to_victim(self):
        actor = _character("Actor", "actor")
        follower = _character("Follower", "follower")
        follower.master = actor
        actor.status_flags.set_flag("affected_by", 262144)
        room = _Room(actor, follower)
        communications, context = self._command_context("group", actor, room, "follower")

        payload = communications.do_group(context)

        self.assertTrue(payload["blocked"])
        self.assertIs(payload["victim"], follower)
        self.assertEqual("You like your master too much to leave him!\r\n", payload["to_victim"])

    def test_do_split_divides_coins_among_non_charmed_group_members(self):
        actor = _character("Actor", "actor")
        actor.silver = 10
        actor.gold = 5
        member = _character("Member", "member")
        member.leader = actor
        charmed = _character("Charmed", "charmed")
        charmed.leader = actor
        charmed.status_flags.set_flag("affected_by", 262144)
        room = _Room(actor, member, charmed)
        communications, context = self._command_context("split", actor, room, "9 3")

        payload = communications.do_split(context)

        self.assertEqual(6, actor.silver)
        self.assertEqual(4, actor.gold)
        self.assertEqual(4, member.silver)
        self.assertEqual(1, member.gold)
        self.assertEqual(0, charmed.silver)
        self.assertEqual(0, charmed.gold)
        self.assertEqual("You split 9 silver coins. Your share is 5 silver.\r\nYou split 3 gold coins. Your share is 2 gold.\r\n", payload["to_char"])
        self.assertEqual([{"id": "member", "text": "Actor splits 9 silver and 3 gold coins, giving you 4 silver and 1 gold.\r\n"}], payload["target_messages"])

    def test_do_split_uses_rom_guard_order(self):
        actor = _character("Actor", "actor")
        actor.silver = 10
        room = _Room(actor)
        communications, context = self._command_context("split", actor, room, "-1")

        payload = communications.do_split(context)

        self.assertTrue(payload["blocked"])
        self.assertEqual("Your group wouldn't like that.\r\n", payload["to_char"])


if __name__ == "__main__":
    unittest.main()
