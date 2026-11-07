import unittest
from copy import deepcopy
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock

from tests.test_movement_rules_parity import MovementFixture, item
from tests.test_review_application_fixes import ROOT
from api.CharacterApi import CharacterApi
from api.GameApi import GameApi
from area.RoomHandler import RoomHandler
from area.Special import Special
from combat.CombatDeathHandler import CombatDeathHandler
from devtools.collection_query import load_collections
from game.EntityUpdateHandler import EntityUpdateHandler
from game.GameData import GameData
from interp.InterpHandler import InterpHandler
from interp.commands.Info import Info
from mobile.MobileHandler import MobileHandler
from player.PlayerHandler import PlayerHandler
from server.messaging.MessageBus import MessageBus


class Rom24ReportTests(MovementFixture, unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        data = load_collections(ROOT / "resources/collections", ["specials"])
        cls.specials = [Special.from_json(doc) for doc in data["specials"].documents
                        if doc["name"] in ("spec_fido", "spec_mayor")]

    def setUp(self):
        super().setUp()
        self.messages = {}
        manager = NS(get_connection_by_character=self.messages.get)
        sessions = NS(get_session_by_character=lambda _: None)
        self.bus = MessageBus(manager, sessions)
        self.listen(self.actor)

        player = PlayerHandler.__new__(PlayerHandler)
        player.interp_api = self.api
        player.room_registry = self.rooms
        player.info_commands = Info.__new__(Info)
        player.info_commands.interp_api = self.api
        player.message_bus = self.bus
        player._send_prompt = AsyncMock()
        room_handler = RoomHandler(self.bus, sessions, self.registries)
        services = NS(get_handler={"ph": player, "rh": room_handler}.get)

        self.interpreter = InterpHandler.__new__(InterpHandler)
        self.interpreter.registry_service = self.registries
        self.interpreter.handler_service = services
        self.interpreter.connection_manager = manager
        self.interpreter.room_registry = self.rooms
        self.interpreter.message_bus = self.bus

        self.mobile_handler = MobileHandler.__new__(MobileHandler)
        self.mobile_handler.logger = Mock()
        self.mobile_handler.registry_service = self.registries
        self.mobile_handler.special_registry = NS(all_specials=lambda: self.specials)
        self.mobile_handler._special_library_cache = None
        self.mobile_handler.weather_handler = NS(time_info=NS(hour=12))
        self.mobile_handler.handler_service = services
        self.mobile_handler.movement_commands = self.movement
        self.mobile_handler.player_handler = player
        self.mobile_handler.message_bus = self.bus

        self.entity_updates = EntityUpdateHandler.__new__(EntityUpdateHandler)
        self.entity_updates.PositionsEnum = self.enums.get("positions")
        self.entity_updates.message_bus = self.bus
        self.entity_updates.effect_update_handler = NS(effect_handler=self.effects)

    def listen(self, entity):
        self.messages[entity.id] = NS(is_closed=lambda: False, send_message=AsyncMock())
        return entity

    def heard(self, entity):
        return [call.args[0].data["text"] for call in self.messages[entity.id].send_message.await_args_list]

    def special_actor(self, name):
        mobile = self.npc()
        mobile.short_description = name
        self.room.add_mobile_to_room(mobile)
        return mobile

    async def mayor_step(self, mayor, step):
        mayor._special_state = {"path": step + ".", "move": True, "pos": 0}
        return await self.mobile_handler._execute_generic_special(mayor, self.room, "spec_mayor")

    async def test_mayor_opens_and_closes_both_sides_and_announces_each(self):
        mayor = self.special_actor("the mayor")
        far = self.listen(self.character("far"))
        far.room_id = self.destination.id
        self.destination.add_player_to_room(far)
        self.exit.keyword = "iron gate"
        self.reverse.keyword = "city gate"
        closed = self.exit_flags.EX_CLOSED
        self.exit.exit_flags |= closed
        self.reverse.exit_flags |= closed

        self.assertTrue(await self.mayor_step(mayor, "O"))
        self.assertFalse((self.exit.exit_flags | self.reverse.exit_flags) & closed)
        self.assertFalse(await self.mayor_step(mayor, "O"))
        self.assertTrue(await self.mayor_step(mayor, "C"))
        self.assertTrue((self.exit.exit_flags & self.reverse.exit_flags) & closed)
        self.assertFalse(await self.mayor_step(mayor, "C"))
        self.assertEqual(["the mayor opens iron.\r\n", "the mayor closes iron.\r\n"], self.heard(self.actor))
        self.assertEqual(["The city opens.\r\n", "The city closes.\r\n"], self.heard(far))

    async def test_mayor_respects_lock_and_only_mirrors_a_reciprocal_exit(self):
        mayor = self.special_actor("the mayor")
        door, closed, locked = (self.exit_flags.EX_ISDOOR, self.exit_flags.EX_CLOSED, self.exit_flags.EX_LOCKED)
        self.exit.exit_flags = door | closed | locked
        self.reverse.exit_flags = door | closed
        self.assertFalse(await self.mayor_step(mayor, "O"))
        self.assertEqual((door | closed | locked, door | closed), (self.exit.exit_flags, self.reverse.exit_flags))
        self.assertEqual([], self.heard(self.actor))
        for exits in ([], [self.reverse]):
            with self.subTest(exits=exits):
                self.destination.exits = exits
                self.reverse.to_room_id = self.temple.id
                self.exit.exit_flags = door | closed
                self.assertTrue(await self.mayor_step(mayor, "O"))
                self.assertEqual((door, door | closed), (self.exit.exit_flags, self.reverse.exit_flags))

    async def test_directional_look_prints_description_then_authored_door_state(self):
        door, closed = self.exit_flags.EX_ISDOOR, self.exit_flags.EX_CLOSED
        cases = [
            ("An iron gate.", door | closed, [self.exit], "An iron gate.\r\nThe iron is closed.\r\n"),
            ("An iron gate.", door, [self.exit], "An iron gate.\r\nThe iron is open.\r\n"),
            ("", door, [self.exit], "Nothing special there.\r\nThe iron is open.\r\n"),
            ("A road.", 0, [self.exit], "A road.\r\n"),
            ("", 0, [], "Nothing special there.\r\n"),
        ]
        for description, flags, exits, expected in cases:
            with self.subTest(description=description, flags=flags, exits=exits):
                self.messages[self.actor.id].send_message.reset_mock()
                self.exit.keyword, self.exit.description, self.exit.exit_flags = "iron gate", description, flags
                self.room.exits = exits
                await self.interpreter._handle_lambdas(self.actor, self.command("look"), "north", raw_command="look north")
                self.assertEqual(expected, "".join(self.heard(self.actor)))

    def test_criminal_cleanup_uses_the_configured_clan_independence(self):
        document = deepcopy(self.game_document)
        document["clans"]["3"] = {"name": "hermits", "independent": True}
        GameApi.configure(GameData.from_json(document), self.enums)
        flags = self.enums.get("playerActBits")
        killer, thief = flags.PLR_KILLER, flags.PLR_THIEF
        for first, second, remaining in (("", "", thief), ("loner", "loner", thief),
                                         ("hermits", "hermits", thief), ("rom", "rom", killer | thief),
                                         ("rom", "loner", thief)):
            with self.subTest(first=first, second=second):
                self.actor.guild, self.victim.guild = first, second
                self.victim.status_flags.assign_bitfield("act", killer | thief)
                CombatDeathHandler.cleanup_flags(self.actor, self.victim, flags)
                self.assertEqual(remaining, self.victim.status_flags.act)
        self.victim.status_flags.assign_bitfield("act", thief)
        for attacker in (self.victim, self.npc()):
            CombatDeathHandler.cleanup_flags(attacker, self.victim, flags)
            self.assertEqual(thief, self.victim.status_flags.act)
        CombatDeathHandler.cleanup_flags(self.actor, self.victim, flags)
        self.assertFalse(self.victim.status_flags.act & thief)

    async def test_light_extinction_uses_visibility_after_fuel_reaches_zero(self):
        unaware = self.listen(self.follower("unaware"))
        asleep = self.listen(self.follower("asleep"))
        switched = self.listen(self.special_actor("switched witness"))
        switched.context = {"controller_original": self.victim}
        self.flag(switched, "AFF_DETECT_INVIS")
        CharacterApi.set_position(asleep, "POS_SLEEPING")
        CharacterApi.set_position(self.actor, "POS_SLEEPING")
        invisible = self.enums.get("itemFlags").ITEM_INVIS
        lamp = item("secret lamp", itemType="light", value2="1", extraFlags=int(invisible))
        self.actor.add_item(lamp)
        self.actor.equip_item(lamp, "light")

        await self.entity_updates.emit_character_tick(self.actor, self.room, self.actor.tick_light_source(self.room))

        self.assertEqual(("0", 0), (lamp.value2, self.room.light))
        self.assertIsNone(self.actor.equipped.light)
        self.assertNotIn(lamp, self.actor.loot)
        self.assertEqual(["something goes out.\r\n"], self.heard(unaware))
        self.assertEqual(["secret lamp goes out.\r\n"], self.heard(switched))
        self.assertEqual([], self.heard(asleep))
        self.assertEqual([], self.heard(self.actor))

    async def test_flicker_is_private_and_permanent_lights_do_not_burn(self):
        viewer = self.listen(self.follower())
        lamp = item("lamp", itemType="light", value2="2")
        self.actor.add_item(lamp)
        self.actor.equip_item(lamp, "light")
        for fuel in ("2", "-1"):
            lamp.value2 = fuel
            await self.entity_updates.emit_character_tick(self.actor, self.room, self.actor.tick_light_source(self.room))
        self.assertEqual("-1", lamp.value2)
        self.assertEqual(["lamp flickers.\r\n"], self.heard(self.actor))
        self.assertEqual([], self.heard(viewer))

    async def test_fido_notice_respects_visibility_and_posture_and_spills_contents(self):
        fido = self.special_actor("the beastly fido")
        detects = self.listen(self.follower("detects"))
        sleeper = self.listen(self.follower("sleeper"))
        switched = self.npc()
        switched.id = "switched"
        switched.context = {"controller_original": self.victim}
        self.room.add_mobile_to_room(self.listen(switched))
        self.flag(fido, "AFF_INVISIBLE")
        self.flag(detects, "AFF_DETECT_INVIS")
        CharacterApi.set_position(sleeper, "POS_SLEEPING")
        bone = item("bone")
        corpse = item("corpse", itemType="corpse_npc", contains=[bone])
        self.room.add_item_to_room(corpse)

        self.assertTrue(await self.mobile_handler._execute_generic_special(fido, self.room, "spec_fido"))

        self.assertEqual(["Someone savagely devours a corpse.\r\n"], self.heard(self.actor))
        self.assertEqual(["The beastly fido savagely devours a corpse.\r\n"], self.heard(detects))
        self.assertEqual(["Someone savagely devours a corpse.\r\n"], self.heard(switched))
        self.assertEqual([], self.heard(sleeper))
        self.assertEqual({bone.id: bone}, self.room.contents)
        self.assertEqual([], corpse.contains)

    async def test_mayor_route_notices_use_the_same_listener_rules(self):
        mayor = self.special_actor("the mayor")
        sleeper = self.listen(self.follower("sleeper"))
        CharacterApi.set_position(sleeper, "POS_SLEEPING")
        self.flag(mayor, "AFF_INVISIBLE")

        self.assertTrue(await self.mayor_step(mayor, "W"))
        self.flag(mayor, "AFF_INVISIBLE", False)
        self.assertTrue(await self.mayor_step(mayor, "S"))

        self.assertEqual(["Someone awakens and groans loudly.\r\n",
                          "The mayor lies down and falls asleep.\r\n"], self.heard(self.actor))
        self.assertEqual([], self.heard(sleeper))
