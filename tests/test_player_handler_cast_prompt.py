import asyncio
import os
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock


SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)


def _stub_module(name: str, **attrs):
    module = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    sys.modules[name] = module
    return module


for package_name in ["api", "combat", "game", "interp", "interp.commands", "player", "server", "skill", "util"]:
    package = sys.modules.get(package_name) or types.ModuleType(package_name)
    package.__path__ = [os.path.join(SRC_PATH, *package_name.split("."))]
    sys.modules[package_name] = package

_stub_module("api.InterpApi", InterpApi=object)
_stub_module("combat.FightHandler", FightHandler=object)
_stub_module("game.WizHandler", WizHandler=object)
_stub_module("game.RegistryService", RegistryService=object)
_stub_module("interp.Context", Context=object)
_stub_module("interp.commands.Info", Info=object)
_stub_module("interp.commands.Movement", Movement=object)
_stub_module("interp.commands.Communications", Communications=object)
_stub_module("interp.commands.Fight", Fight=object)
_stub_module("interp.commands.Object", Object=object)
_stub_module("interp.commands.Wiz", Wiz=object)
_stub_module("player.Character", Character=object)
_stub_module("api.CharacterApi", CharacterApi=SimpleNamespace(is_npc=lambda entity: bool(getattr(entity, "is_npc", False))))
_stub_module("util.GenericUtil", GenericUtil=SimpleNamespace(to_int=lambda value, default=0: int(value or default)))
_stub_module("util.InfoUtil", InfoUtil=SimpleNamespace())
_stub_module("util.InterpUtil", InterpUtil=SimpleNamespace())
_stub_module("util.CommunicationsUtil", CommunicationsUtil=SimpleNamespace())
_stub_module("util.ItemUtil", ItemUtil=SimpleNamespace())
_stub_module("util.PlayerUtil", PlayerUtil=SimpleNamespace())
_stub_module("skill.Ability", Ability=SimpleNamespace(take_improve_messages=lambda _character: ""))
_stub_module("server.messaging", MessageBus=object)
_stub_module("server.LoggerFactory", LoggerFactory=SimpleNamespace(get_logger=lambda _name: SimpleNamespace()))

from player.PlayerHandler import PlayerHandler


class TestPlayerHandlerCastPrompt(unittest.TestCase):
    def test_do_cast_does_not_send_duplicate_caster_prompt(self):
        async def run_test():
            character = SimpleNamespace(id="char_1", room_id="room_1", area_id="area_1")
            room = SimpleNamespace(id="room_1", area_id="area_1")
            area = SimpleNamespace(id="area_1")
            context = SimpleNamespace(room=room)
            events = []

            handler = PlayerHandler.__new__(PlayerHandler)
            handler.fight_commands = Mock()
            handler.fight_commands.do_cast.return_value = {"payloads": [{"to_char": "Cast result.\r\n"}]}
            handler.room_registry = Mock()
            handler.room_registry.get_or_none.return_value = room
            handler.area_registry = Mock()
            handler.area_registry.get_or_none.return_value = area
            handler.message_bus = Mock()
            handler.message_bus.text_to_message.side_effect = lambda text: text

            async def send_to_character(*_args):
                events.append("payload")

            async def send_prompt(*_args):
                events.append("prompt")

            handler.message_bus.send_to_character = AsyncMock(side_effect=send_to_character)
            handler.message_bus.send_prompt = AsyncMock(side_effect=send_prompt)
            handler._resolve_standard_payload = lambda _character, payload, context=None: payload

            await handler.do_cast(character, context)

            self.assertEqual(["payload"], events)
            handler.message_bus.send_prompt.assert_not_awaited()

        asyncio.run(run_test())

    def test_victim_payload_sends_prompt_after_payload(self):
        async def run_test():
            character = SimpleNamespace(id="char_1", room_id="room_1", area_id="area_1")
            victim = SimpleNamespace(id="char_2", room_id="room_1", area_id="area_1", is_npc=False)
            room = SimpleNamespace(id="room_1", area_id="area_1")
            area = SimpleNamespace(id="area_1")
            context = SimpleNamespace(room=room)
            events = []

            handler = PlayerHandler.__new__(PlayerHandler)
            handler.room_registry = Mock()
            handler.room_registry.get_or_none.return_value = room
            handler.area_registry = Mock()
            handler.area_registry.get_or_none.return_value = area
            handler.message_bus = Mock()
            handler.message_bus.text_to_message.side_effect = lambda text: text
            handler._resolve_standard_payload = lambda _character, payload, context=None: payload

            async def send_to_character(character_id, _message):
                events.append(f"payload:{character_id}")

            async def send_prompt(prompt_character, *_args):
                events.append(f"prompt:{prompt_character.id}")

            handler.message_bus.send_to_character = AsyncMock(side_effect=send_to_character)
            handler.message_bus.send_prompt = AsyncMock(side_effect=send_prompt)

            await handler._emit_standard_payload(
                character,
                {"victim": victim, "to_victim": "You feel faster.\r\n"},
                context=context,
            )

            self.assertEqual(["payload:char_2", "prompt:char_2"], events)
            handler.message_bus.send_prompt.assert_awaited_once_with(victim, area, room)

        asyncio.run(run_test())

    def test_batched_victim_payloads_send_one_prompt_after_all_payloads(self):
        async def run_test():
            character = SimpleNamespace(id="char_1", room_id="room_1", area_id="area_1")
            victim = SimpleNamespace(id="char_2", room_id="room_1", area_id="area_1", is_npc=False)
            room = SimpleNamespace(id="room_1", area_id="area_1")
            area = SimpleNamespace(id="area_1")
            context = SimpleNamespace(room=room)
            events = []

            handler = PlayerHandler.__new__(PlayerHandler)
            handler.room_registry = Mock()
            handler.room_registry.get_or_none.return_value = room
            handler.area_registry = Mock()
            handler.area_registry.get_or_none.return_value = area
            handler.message_bus = Mock()
            handler.message_bus.text_to_message.side_effect = lambda text: text
            handler._resolve_standard_payload = lambda _character, payload, context=None: payload

            async def send_to_character(character_id, message):
                events.append(f"payload:{character_id}:{message.strip()}")

            async def send_prompt(prompt_character, *_args):
                events.append(f"prompt:{prompt_character.id}")

            handler.message_bus.send_to_character = AsyncMock(side_effect=send_to_character)
            handler.message_bus.send_prompt = AsyncMock(side_effect=send_prompt)

            await handler._emit_standard_payloads(
                character,
                [
                    {"victim": victim, "to_victim": "You feel yourself slow down.\r\n"},
                    {"victim": victim, "to_victim": "You feel weaker.\r\n"},
                ],
                context=context,
            )

            self.assertEqual(
                [
                    "payload:char_2:You feel yourself slow down.",
                    "payload:char_2:You feel weaker.",
                    "prompt:char_2",
                ],
                events,
            )
            handler.message_bus.send_prompt.assert_awaited_once_with(victim, area, room)

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()
