import asyncio
import sys
import types
import unittest
from enum import IntEnum
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))
for name in ("api", "area", "combat", "game", "interp", "item", "mobile", "notes", "player", "server", "skill", "util"):
    if name not in sys.modules:
        package = types.ModuleType(name)
        package.__path__ = [str(SRC / name)]
        sys.modules[name] = package

from api.CharacterApi import CharacterApi
from devtools.collection_query import load_collections
from game.GamePayload import GamePayload
from interp.Command import Command
from interp.CommandAccess import CommandAccess
from interp.Context import Context
from interp.InterpHandler import InterpHandler
from mobile.Mobile import Mobile
from player.Character import Character
from player.PlayerHandler import PlayerHandler


class TestCommandAuthorization(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        collections = load_collections(ROOT / "resources" / "collections", ["commands", "gamedata"])
        cls.documents = {doc["name"]: doc for doc in collections["commands"].documents}
        enums = collections["gamedata"].documents[0]["enums"]
        cls.parameters = IntEnum("Parameters", enums["gameParameters"])
        cls.positions = IntEnum("Positions", enums["positions"])

    def setUp(self):
        self.enterContext(patch.object(CharacterApi, "get_enum", side_effect=lambda name: {
            "gameParameters": self.parameters, "positions": self.positions,
        }.get(name)))
        self.enterContext(patch.object(CharacterApi, "GameParameters", self.parameters, create=True))
        self.enterContext(patch.object(CharacterApi, "positions", self.positions, create=True))
        self.actor = self._actor()

    def _actor(self, *, level=6, trust=0, role="player", position="POS_STANDING", mobile=False):
        actor = (Mobile if mobile else Character).__new__(Mobile if mobile else Character)
        actor.id = "mobile" if mobile else "actor"
        actor.name = "Tester"
        actor.room_id = "room"
        actor.context = {}
        actor.aliases = {}
        actor.level = level
        actor.trust = trust
        actor.role = role
        actor.character_attributes = SimpleNamespace(position=self.positions[position].value)
        return actor

    def _command(self, name="say", **changes):
        doc = self.documents[name]
        data = dict(_id="command", id="command", name=doc["name"], shortcuts=doc.get("shortcuts", ""),
                    role=doc["role"], position=doc["position"], enabled=doc["enabled"],
                    level=doc["level"], lambdas=doc.get("lambdas", []), function=[], usage="",
                    max_arguments=doc.get("maxArguments", 0), pipeline=doc.get("pipeline", False),
                    payload=GamePayload.from_json(doc.get("payload")))
        data.update(changes)
        return Command(**data)

    def _interpreters(self, command):
        player_commands = SimpleNamespace(do_wiz_command=AsyncMock(), do_communications_command=AsyncMock())
        services = SimpleNamespace(get_handler=lambda key: player_commands if key == "ph" else None)
        registry = SimpleNamespace(get_or_none=lambda **kw: command if kw.get("name") == command.name else None,
                                   all_commands=lambda: [command])
        bus = SimpleNamespace(text_to_message=lambda text: text, send_to_character=AsyncMock(),
                              connection_manager=SimpleNamespace(get_connection_by_character=lambda _id: None))
        normal = InterpHandler.__new__(InterpHandler)
        normal.logger = Mock()
        normal.message_bus = bus
        normal.registry_service = SimpleNamespace(interp_registry=registry)
        normal.interp_registry = registry
        normal.social_registry = SimpleNamespace(get_or_none=lambda **kw: None)
        normal.handler_service = services
        normal.connection_manager = bus.connection_manager
        normal.room_registry = SimpleNamespace(get_or_none=lambda **kw: None, all_rooms=lambda: [])
        normal.command_not_found_message = "Huh?\r\n"
        nested = PlayerHandler.__new__(PlayerHandler)
        nested.message_bus = bus
        nested.interp_registry = registry
        nested.social_registry = normal.social_registry
        nested.room_registry = normal.room_registry
        nested.interp_api = SimpleNamespace(render_message_key=lambda *args, **kw: {})
        return normal, nested, services, player_commands, bus

    def test_shutdown_is_blocked_before_normal_dispatch_has_side_effects(self):
        command = self._command("shutdown")
        normal, _, _, executors, bus = self._interpreters(command)
        asyncio.run(normal.handle_command(SimpleNamespace(usage="player"), self.actor, "shutdown"))
        executors.do_wiz_command.assert_not_awaited()
        bus.send_to_character.assert_awaited_once_with(self.actor.id, "Huh?\r\n")

    def test_alias_cannot_bypass_shutdown_authorization(self):
        command = self._command("shutdown")
        normal, _, _, executors, bus = self._interpreters(command)
        self.actor.aliases = {"bye": "shutdown"}
        asyncio.run(normal.handle_command(SimpleNamespace(usage="player"), self.actor, "bye"))
        executors.do_wiz_command.assert_not_awaited()
        bus.send_to_character.assert_awaited()

    def test_authorized_admin_can_execute_collection_shutdown(self):
        command = self._command("shutdown")
        normal, _, _, executors, _ = self._interpreters(command)
        admin = self._actor(level=60, role="admin")
        asyncio.run(normal.handle_command(SimpleNamespace(usage="admin"), admin, "shutdown"))
        executors.do_wiz_command.assert_awaited_once()

    def test_force_and_order_use_the_victims_permissions(self):
        for kind in ("force", "order"):
            with self.subTest(kind=kind):
                command = self._command("shutdown")
                _, nested, services, executors, bus = self._interpreters(command)
                admin = self._actor(level=60, role="admin")
                context = Context(character=admin, handler_service=services, command=command)
                entry = {"victim": self.actor, "command": "shutdown"}
                if kind == "force":
                    asyncio.run(nested._handle_force_payload(admin, context, {"forced_commands": [entry]}))
                else:
                    asyncio.run(nested._handle_order_payload(admin, context, {"ordered_commands": [entry]}))
                executors.do_wiz_command.assert_not_awaited()
                bus.send_to_character.assert_awaited_once_with(self.actor.id, "Huh?\r\n")

    def test_at_checks_the_executing_characters_permissions(self):
        command = self._command("shutdown")
        _, nested, services, executors, _ = self._interpreters(command)
        context = Context(character=self.actor, handler_service=services, command=command)
        asyncio.run(nested._handle_at_payload(self.actor, context, {"interpret_at": "shutdown"}))
        executors.do_wiz_command.assert_not_awaited()

    def test_nested_authorized_command_executes(self):
        command = self._command("shutdown")
        _, nested, services, executors, _ = self._interpreters(command)
        admin = self._actor(level=60, role="admin")
        context = Context(character=admin, handler_service=services, command=command)
        asyncio.run(nested._interpret_nested_command(admin, context, "shutdown"))
        executors.do_wiz_command.assert_awaited_once()

    def test_disabled_commands_never_execute_in_either_runner(self):
        for pipeline in (False, True):
            with self.subTest(pipeline=pipeline):
                command = self._command("shutdown", enabled=False, pipeline=pipeline)
                normal, nested, services, executors, _ = self._interpreters(command)
                admin = self._actor(level=60, role="admin")
                asyncio.run(normal._handle_lambdas(admin, command, ""))
                context = Context(character=admin, command=command, handler_service=services)
                asyncio.run(nested._execute_nested_lambdas(command, context))
                self.assertTrue(context.done)
                executors.do_wiz_command.assert_not_awaited()

    def test_level_and_position_denials_stop_both_execution_paths(self):
        for changes in ({"level": 7}, {"position": "POS_STANDING"}):
            for pipeline in (False, True):
                with self.subTest(changes=changes, pipeline=pipeline):
                    command = self._command(pipeline=pipeline, **changes)
                    normal, nested, services, executors, bus = self._interpreters(command)
                    actor = self._actor(position="POS_RESTING")
                    asyncio.run(normal._handle_lambdas(actor, command, ""))
                    context = Context(character=actor, command=command, handler_service=services)
                    asyncio.run(nested._execute_nested_lambdas(command, context))
                    executors.do_communications_command.assert_not_awaited()
                    self.assertEqual(2, bus.send_to_character.await_count)
                    self.assertTrue(context.done)

    def test_ordinary_player_command_still_executes_in_both_paths(self):
        command = self._command()
        normal, nested, services, executors, _ = self._interpreters(command)
        asyncio.run(normal.handle_command(SimpleNamespace(usage="player"), self.actor, "say hello"))
        context = Context(character=self.actor, command=command, handler_service=services)
        asyncio.run(nested._interpret_nested_command(self.actor, context, "say hello"))
        self.assertEqual(2, executors.do_communications_command.await_count)

    def test_numeric_and_symbolic_levels_use_effective_trust(self):
        cases = ((3, 3), ("5", 5), ("ML", 60), ("IM", 55)) + tuple((f"L{i}", 60 - i) for i in range(1, 9))
        for level, minimum in cases:
            with self.subTest(level=level):
                command = self._command(level=level)
                actor = self._actor(level=60, trust=minimum - 1, role="admin")
                self.assertIsNotNone(CommandAccess.check(actor, command))
                actor.trust = minimum
                self.assertIsNone(CommandAccess.check(actor, command))

    def test_immortal_role_is_checked_independently_of_command_level(self):
        command = self._command(role="immortal", level=0)
        self.assertIsNotNone(CommandAccess.check(self.actor, command))
        self.actor.trust = 55
        self.assertIsNone(CommandAccess.check(self.actor, command))

    def test_switched_mobile_uses_controller_trust_and_body_position(self):
        controller = self._actor(level=60, role="admin")
        body = self._actor(level=1, mobile=True, position="POS_SLEEPING")
        body.context["controller_original"] = controller
        self.assertIsNone(CommandAccess.check(body, self._command("return")))
        self.assertIsNotNone(CommandAccess.check(body, self._command("shutdown", position="POS_STANDING")))

    def test_unknown_metadata_and_controller_cycles_fail_closed(self):
        for changes in ({"level": "TYPO"}, {"level": 1.5}, {"level": True}, {"level": None},
                        {"position": "FLYING"}, {"role": "typo"}, {"enabled": "false"}):
            with self.subTest(changes=changes):
                self.assertIsNotNone(CommandAccess.check(self.actor, self._command(**changes)))
        self.actor.context["controller_original"] = self.actor
        self.assertIsNotNone(CommandAccess.check(self.actor, self._command()))

    def test_position_metadata_accepts_both_collection_conventions(self):
        for name in ("POS_STANDING", "STANDING"):
            with self.subTest(name=name):
                command = self._command(position=name)
                self.assertIsNone(CommandAccess.check(self.actor, command))
                self.actor.character_attributes.position = self.positions.POS_RESTING.value
                self.assertIsNotNone(CommandAccess.check(self.actor, command))
                self.actor.character_attributes.position = self.positions.POS_STANDING.value

    def test_all_collection_commands_are_available_to_a_standing_admin(self):
        admin = self._actor(level=60, role="admin")
        for name in self.documents:
            with self.subTest(command=name):
                self.assertIsNone(CommandAccess.check(admin, self._command(name)))

    def test_denials_render_optional_command_payload_overrides(self):
        command = self._command("shutdown", payload=GamePayload.from_json({
            "toChar": {"commandNotAllowed": "That command is restricted."}}))
        denial = CommandAccess.check(self.actor, command)
        self.assertEqual("That command is restricted.\r\n", denial.render(command))

    def test_position_denials_use_rom_messages_in_both_execution_paths(self):
        expected = {
            "POS_DEAD": "Lie still; you are DEAD.",
            "POS_MORTAL": "You are hurt far too bad for that.",
            "POS_INCAP": "You are hurt far too bad for that.",
            "POS_STUNNED": "You are too stunned to do that.",
            "POS_SLEEPING": "In your dreams, or what?",
            "POS_RESTING": "Nah... You feel too relaxed...",
            "POS_SITTING": "Better stand up first.",
            "POS_FIGHTING": "No way!  You are still fighting!",
        }
        for position, text in expected.items():
            with self.subTest(position=position):
                command = self._command("enter", lambdas=['lambda ctx: ctx.handler_service.run()'])
                normal, nested, services, _, bus = self._interpreters(command)
                services.run = Mock()
                actor = self._actor(position=position)
                asyncio.run(normal._handle_lambdas(actor, command, ""))
                context = Context(character=actor, command=command, handler_service=services)
                asyncio.run(nested._execute_nested_lambdas(command, context))
                self.assertTrue(context.done)
                self.assertEqual([call.args for call in bus.send_to_character.await_args_list],
                                 [(actor.id, text + '\r\n')] * 2)
                services.run.assert_not_called()

    def test_position_denial_uses_command_payload_override(self):
        command = self._command("enter", payload=GamePayload.from_json({
            "toChar": {"commandPositionSitting": "Rise before entering."}}))
        actor = self._actor(position="POS_SITTING")
        denial = CommandAccess.check(actor, command)
        self.assertEqual(denial.message_key, 'command_position_sitting')
        self.assertEqual(denial.render(command), 'Rise before entering.\r\n')

    def test_all_commands_have_payload_messages_for_every_disallowed_position(self):
        for name in self.documents:
            command = self._command(name)
            admin = self._actor(level=60, role='admin')
            for position in CommandAccess.POSITION_MESSAGE_KEYS:
                admin.character_attributes.position = self.positions[position].value
                denial = CommandAccess.check(admin, command)
                if denial is not None:
                    with self.subTest(command=name, position=position):
                        self.assertTrue(denial.message_key.startswith('command_position_'))
                        self.assertIn(denial.message_key, command.payload.to_char)
                        self.assertNotEqual(denial.render(command), 'Huh?\r\n')

    def test_look_interpreter_denials_do_not_replace_command_specific_messages(self):
        command = self._command('look')
        for position, text in [('POS_SLEEPING', 'In your dreams, or what?'),
                               ('POS_STUNNED', 'You are too stunned to do that.')]:
            with self.subTest(position=position):
                denial = CommandAccess.check(self._actor(position=position), command)
                self.assertEqual(denial.render(command), text + '\r\n')
        self.assertEqual(command.payload.to_char['sleeping'], "You can't see anything - you're sleeping!")
        self.assertEqual(command.payload.to_char['stunned'], "You can't see anything but stars!")


if __name__ == "__main__":
    unittest.main()
