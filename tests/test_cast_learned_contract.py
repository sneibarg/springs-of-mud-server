import sys
import unittest
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from api.CharacterApi import CharacterApi
from api.CommunicationsApi import CommunicationsApi
from api.GameApi import GameApi
from api.InterpApi import InterpApi
from api.MobileApi import MobileApi
from api.SpellApi import SpellApi
from area.Room import Room
from devtools.collection_query import load_collections
from game.EnumProvider import EnumProvider
from game.GameData import GameData
from game.WizHandler import WizHandler
from interp.Command import Command
from interp.Context import Context
from interp.InterpHandler import InterpHandler
from interp.commands.Fight import Fight
from interp.commands.Communications import Communications
from item.EffectHandler import EffectHandler
from mobile.MobileContext import MobileContext
from player.Character import Character
from player.PlayerHandler import PlayerHandler
from server.connection.ConnectionManager import ConnectionManager
from server.handlers.ConnectionHandler import ConnectionHandler
from server.protocol.Message import Message, MessageType
from server.session.SessionHandler import SessionHandler
from server.session.SessionState import SessionState, SessionStatus
from skill.Ability import Ability
from skill.Spell import Spell
from skill.SpellRegistry import SpellRegistry
from util.FightUtil import FightUtil
from util.GenericUtil import GenericUtil
from tests.test_immortal_priority_parity import mobile_entity


class TestCastLearnedContract(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.collections = load_collections(
            ROOT / "resources" / "collections", ["characters", "commands", "spells", "gamedata"])

    def setUp(self):
        GameApi.reset_for_tests()
        self.addCleanup(GameApi.reset_for_tests)
        game_data = GameData.from_json(self.collections["gamedata"].documents[0])
        enums = EnumProvider({name: GenericUtil.build_int_enum(name, members)
                              for name, members in game_data.enums.items()})
        GameApi.configure(game_data, enums)
        CharacterApi.load_enums(**CharacterApi.ACTOR_ENUM_ALIASES)

        document = deepcopy(next(doc for doc in self.collections["characters"].documents
                                 if doc["name"] == "Fizban"))
        document["id"] = document.pop("_id")["$oid"]
        document.pop("_class", None)
        document.setdefault("description", "")
        document.update(level=20, mana=100, inventory=[], equipped={}, effects=[],
                        skills=[{"name": "armor", "level": 100}],
                        spells=[{"name": "armor", "level": 75}])
        self.character = Character.from_json(document)
        self.character.status_flags.pulse_daze = 0
        self.character.status_flags.pulse_wait = 0
        self.character.status_flags.drunk = 0
        self.character.character_attributes.position = CharacterApi.pos_value("POS_STANDING")

        spell_document = deepcopy(next(doc for doc in self.collections["spells"].documents
                                       if doc["name"] == "armor"))
        # Supply the class metadata required by the runtime ability contract.
        spell_document.update(levelByClass={"mage": 10}, ratingByClass={"mage": 1})
        self.spell = Spell.from_json(spell_document)
        registry = SpellRegistry()
        registry.register(self.spell)

        command_document = deepcopy(next(doc for doc in self.collections["commands"].documents
                                         if doc["name"] == "cast"))
        command_document.update(usage="")
        command = Command.from_json(command_document)
        room = Room(id=self.character.room_id, area_id=self.character.area_id)
        room.add_player_to_room(self.character)
        self.context = Context(character=self.character, command=command, room=room,
                               registry_service=SimpleNamespace(spell_registry=registry),
                               parameters=[], result="armor")
        interp_api = InterpApi()
        self.spell_api = SpellApi(EffectHandler(enums), interp_api)
        self.commands = Fight.__new__(Fight)
        self.commands.registry_service = self.context.registry_service
        self.commands.spell_registry = registry
        self.commands.interp_api = interp_api
        self.commands.spell_api = self.spell_api

    async def test_ordered_npc_cast_requires_control_of_that_body(self):
        caster = self.character
        room = self.context.room
        follower = mobile_entity('follower', caster.status_flags)
        follower.level, follower.mana, follower.room_id = 20, 100, room.id
        follower.character_attributes = deepcopy(caster.character_attributes)
        follower.master = caster
        follower.status_flags.set_flag('affected_by', CharacterApi.get_enum('affectedBy').AFF_CHARM)
        room.add_mobile_to_room(follower)

        order_data = deepcopy(next(doc for doc in self.collections['commands'].documents if doc['name'] == 'order'))
        order_data.update(usage='')
        order = Command.from_json(order_data)
        commands = {'order': order, 'cast': self.context.command}
        registries = self.context.registry_service
        registries.interp_registry = SimpleNamespace(
            all_commands=lambda: list(commands.values()), get_or_none=lambda *, name: commands.get(name))
        registries.room_registry = SimpleNamespace(get_or_none=lambda **_: room)
        registries.social_registry = None
        sessions, connections = SessionHandler(), ConnectionManager()
        session = sessions.create_session('caster')
        session.character, session.status = caster, SessionStatus.PLAYING
        connections.add_connection(SimpleNamespace(session_id=session.session_id))
        connections.bind_character(caster.id, session.session_id)
        wiz = WizHandler(registries, sessions, connections)
        bus = SimpleNamespace(connection_manager=connections, text_to_message=lambda text: text,
                              send_to_character=AsyncMock(), send_to_room=AsyncMock())
        player = PlayerHandler.__new__(PlayerHandler)
        player.message_bus, player.command_audit = bus, None
        player.room_registry, player.interp_registry = registries.room_registry, registries.interp_registry
        player.interp_api, player.fight_commands = self.commands.interp_api, self.commands
        player.communications_commands = Communications.__new__(Communications)
        player.communications_commands.interp_api = player.interp_api
        player.communications_commands.communications_api = CommunicationsApi
        interpreter = InterpHandler(
            SimpleNamespace(get=lambda _: connections), bus, registries,
            SimpleNamespace(social_handler=None, get_handler={'ph': player, 'wh': wiz}.get),
        )

        with patch('api.SpellApi.random.randint', return_value=1):
            await interpreter.handle_command(caster, 'order follower cast armor')
            self.assertGreater(caster.status_flags.pulse_wait, 0)
            self.assertEqual((100, 0, []), (follower.mana, follower.status_flags.pulse_wait, follower.effects))
            follower.master = None
            follower.status_flags.unset_flag('affected_by', CharacterApi.get_enum('affectedBy').AFF_CHARM)
            wiz.switch_character(caster, follower)
            await interpreter.handle_command(follower, 'cast armor')
        self.assertEqual(100 - FightUtil.cast_mana_cost(follower, self.spell), follower.mana)
        self.assertEqual(self.spell.beats, follower.status_flags.pulse_wait)
        self.assertTrue(any(effect.type == 'spell.armor' for effect in follower.effects))

    def test_unswitched_mobile_special_can_cast_independently(self):
        actor = mobile_entity('caster', self.character.status_flags)
        actor.level = 20
        handler = SimpleNamespace(spell_registry=self.commands.spell_registry, spell_api=self.spell_api,
                                  skill_registry=SimpleNamespace(all_skills=lambda: []))
        context = MobileContext(actor, self.context.room, handler)
        self.assertTrue(MobileApi.cast_spell(context, 'armor', target=self.character))
        self.assertTrue(any(effect.type == 'spell.armor' for effect in self.character.effects))

    async def test_invalid_casts_leave_session_ready_for_a_valid_cast(self):
        character = self.character
        command = self.context.command
        room = self.context.room
        command_registry = SimpleNamespace(
            all_commands=lambda: [command],
            get_or_none=lambda *, name: command if name == "cast" else None,
        )
        room_registry = SimpleNamespace(get_or_none=lambda **_: room)
        registry_service = SimpleNamespace(
            interp_registry=command_registry, room_registry=room_registry, social_registry=None,
        )
        resources_after_command = []
        bus = SimpleNamespace(
            text_to_message=lambda text: text,
            send_to_character=AsyncMock(),
            send_prompt=AsyncMock(side_effect=lambda actor, *_: resources_after_command.append(
                (actor.mana, actor.status_flags.pulse_wait))),
        )
        player = PlayerHandler.__new__(PlayerHandler)
        player.fight_commands = self.commands
        player.message_bus = bus
        interpreter = InterpHandler(
            SimpleNamespace(get=lambda _: SimpleNamespace(get_connection_by_character=lambda _: None)),
            bus, registry_service,
            SimpleNamespace(social_handler=None, get_handler={"ph": player}.get),
        )
        connection_handler = ConnectionHandler.__new__(ConnectionHandler)
        connection_handler.command_handler = interpreter
        connection_handler.session_handler = SimpleNamespace(is_session_idle=lambda _: False)
        connection_handler.message_bus = bus
        connection_handler.logger = Mock()
        connection_handler._get_area_and_room = lambda _: (None, room)
        connection_handler._wait_for_message = AsyncMock(side_effect=[
            Message(MessageType.GAME, {"text": "cast"}),
            Message(MessageType.GAME, {"text": "cast unrecognized-spell"}),
            Message(MessageType.GAME, {"text": "cast armor"}),
            None,
        ])
        session = SessionState("cast-session", status=SessionStatus.PLAYING, character=character)
        connection = SimpleNamespace(is_closed=lambda: False)
        cost = FightUtil.cast_mana_cost(character, self.spell)

        with patch("api.SpellApi.random.randint", return_value=1), patch.object(Ability, "check_improve") as improve:
            await connection_handler._game_loop(connection, session, None, character)

        connection_handler.logger.error.assert_not_called()
        messages = [call.args[1].strip() for call in bus.send_to_character.await_args_list]
        self.assertEqual(["Cast which what where?", "You don't know any spells of that name."], messages[:2])
        self.assertEqual([(100, 0), (100, 0), (100 - cost, self.spell.beats)], resources_after_command)
        self.assertTrue(any(effect.type == "spell.armor" for effect in character.effects))
        improve.assert_called_once_with(character, self.spell.id, True, 1)

    def test_learned_spell_resolves_guards_casts_and_applies_its_content(self):
        self.assertIs(self.spell, FightUtil.find_spell(self.commands.spell_registry, "arm", self.character))
        self.assertEqual(75, self.spell_api.casting_proficiency(self.character, self.spell))
        initial_armor = self.character.armor_class.piercing
        cost = FightUtil.cast_mana_cost(self.character, self.spell)
        with patch("api.SpellApi.random.randint", return_value=1), \
                patch.object(Ability, "check_improve") as improve:
            payload = self.commands.do_cast(self.character, self.context)

        self.assertTrue(self.context.done)
        self.assertEqual(100 - cost, self.character.mana)
        self.assertEqual(self.spell.beats, self.character.status_flags.pulse_wait)
        self.assertEqual(initial_armor - 20, self.character.armor_class.piercing)
        self.assertTrue(any(effect.type == "spell.armor" for effect in self.character.effects))
        text = "".join(entry.get("to_char", "") for entry in payload["payloads"])
        self.assertIn("You cast armor", text)
        self.assertIn("You feel someone protecting you.", text)
        improve.assert_called_once_with(self.character, self.spell.id, True, 1)

    def test_same_named_skill_does_not_satisfy_the_spell_guard(self):
        self.character.spells.clear()
        self.assertEqual(0, self.spell_api.casting_proficiency(self.character, self.spell))
        with patch.object(self.spell_api, "cast") as cast:
            payload = self.commands.do_cast(self.character, self.context)
        self.assertTrue(payload["blocked"])
        self.assertEqual("spell_not_learned", payload["blocked_key"])
        self.assertIn("don't know any spells", payload["to_char"])
        cast.assert_not_called()
        self.assertEqual(100, self.character.mana)
        self.assertEqual([], self.character.effects)

    def test_script_failure_keeps_applied_effect_and_cost_but_skips_learning_and_retaliation(self):
        self.spell.lambdas = ['lambda ctx: ctx.resource_expr("movement", "current - 1")', 'lambda ctx: 1 / 0',
                              'lambda ctx: setattr(ctx.actor, "mana", 0)']
        initial_movement = self.character.movement
        cost = FightUtil.cast_mana_cost(self.character, self.spell)
        with patch("api.SpellApi.random.randint", return_value=1), \
                patch.object(self.spell_api.logger, "error") as log, \
                patch.object(Ability, "check_improve") as improve, \
                patch.object(self.spell_api, "start_offensive_combat") as retaliate:
            payload = self.commands.do_cast(self.character, self.context)

        self.assertTrue(self.context.done)
        self.assertEqual(100 - cost, self.character.mana)
        self.assertEqual(self.spell.beats, self.character.status_flags.pulse_wait)
        self.assertEqual(initial_movement - 1, self.character.movement)
        self.assertIn({"to_char": "Your spell fizzles and dies.\r\n"}, payload["payloads"])
        log.assert_called_once()
        improve.assert_not_called()
        retaliate.assert_not_called()

    def test_proficiency_miss_still_charges_half_mana_and_runs_attempt_followup(self):
        cost = FightUtil.cast_mana_cost(self.character, self.spell)
        with patch("api.SpellApi.random.randint", return_value=100), \
                patch.object(self.spell_api, "execute_lambdas") as execute, \
                patch.object(Ability, "check_improve") as improve, \
                patch.object(self.spell_api, "start_offensive_combat") as retaliate:
            self.commands.do_cast(self.character, self.context)
        self.assertEqual(100 - cost // 2, self.character.mana)
        execute.assert_not_called()
        improve.assert_called_once_with(self.character, self.spell.id, False, 1)
        retaliate.assert_called_once()

    def test_below_class_level_is_rejected_before_casting(self):
        self.character.level = 9
        self.assertEqual(0, self.spell_api.casting_proficiency(self.character, self.spell))
        with patch.object(self.spell_api, "cast") as cast:
            payload = self.commands.do_cast(self.character, self.context)
        self.assertEqual("spell_not_learned", payload["blocked_key"])
        cast.assert_not_called()

    def test_real_learned_entry_preserves_daze_and_drunk_penalties(self):
        self.character.set_learned("armor", 99, collection_name="spells")
        self.character.status_flags.pulse_daze = 1
        self.character.status_flags.drunk = 11
        self.assertEqual(44, self.spell_api.casting_proficiency(self.character, self.spell))


if __name__ == "__main__":
    unittest.main()
