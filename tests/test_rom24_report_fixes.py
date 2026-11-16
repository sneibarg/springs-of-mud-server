import unittest
from copy import deepcopy
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock, call, patch

from tests.test_movement_rules_parity import MovementFixture, item
from tests.test_review_application_fixes import ROOT
from api.CharacterApi import CharacterApi
from api.GameApi import GameApi
from api.MobileApi import MobileApi
from api.SpellApi import SpellApi
from area.AreaHandler import AreaHandler
from area.Reset import Reset
from area.RoomHandler import RoomHandler
from area.RoomService import RoomService
from area.Special import Special
from area.SpecialRegistry import SpecialRegistry
from combat.CombatDeathHandler import CombatDeathHandler
from devtools.collection_query import load_collections
from game.EntityUpdateHandler import EntityUpdateHandler
from game.GameData import GameData
from interp.InterpHandler import InterpHandler
from interp.PromptFormat import PromptFormat
from interp.commands.Info import Info
from mobile.MobileHandler import MobileHandler
from player.PlayerHandler import PlayerHandler
from server.connection.TelnetConnection import TelnetConnection
from server.messaging.MessageBus import MessageBus
from skill.Spell import Spell


class Rom24ReportTests(MovementFixture, unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        data = load_collections(ROOT / "resources/collections", ["specials", "spells"])
        cls.specials = [Special.from_json(doc) for doc in data["specials"].documents
                        if doc["name"] in ("spec_fido", "spec_mayor")]
        cls.mage_special = Special.from_json(next(doc for doc in data["specials"].documents
                                                  if doc["name"] == "spec_cast_mage"))
        cls.teleport = Spell.from_json(next(doc for doc in data["spells"].documents if doc["name"] == "teleport"))

    def setUp(self):
        super().setUp()
        self.messages = {}
        manager = NS(get_connection_by_character=self.messages.get)
        sessions = NS(get_session_by_character=lambda _: None)
        self.bus = MessageBus(manager, sessions)
        self.listen(self.actor)

        player = PlayerHandler.__new__(PlayerHandler)
        player.command_audit = None
        player.interp_api = self.api
        player.room_registry = self.rooms
        player.info_commands = Info.__new__(Info)
        player.info_commands.interp_api = self.api
        player.message_bus = self.bus
        player._send_prompt = AsyncMock()
        room_handler = RoomHandler(self.bus, sessions, self.registries)
        handlers = {"ph": player, "rh": room_handler}
        services = NS(get_handler=handlers.get)

        self.interpreter = InterpHandler.__new__(InterpHandler)
        self.interpreter.command_audit = None
        self.interpreter.registry_service = self.registries
        self.interpreter.handler_service = services
        self.interpreter.connection_manager = manager
        self.interpreter.room_registry = self.rooms
        self.interpreter.message_bus = self.bus

        self.mobile_handler = MobileHandler.__new__(MobileHandler)
        self.mobile_handler.logger = Mock()
        self.mobile_handler.room_registry = self.rooms
        self.mobile_handler.act_bits = self.enums.get("actBits")
        self.mobile_handler.room_flags = self.enums.get("roomFlags")
        self.mobile_handler.exit_flags = self.exit_flags
        self.mobile_handler.registry_service = self.registries
        self.mobile_handler.special_registry = SpecialRegistry()
        for special in self.specials:
            self.mobile_handler.special_registry.register(special)
        self.mobile_handler.weather_handler = NS(time_info=NS(hour=12))
        self.mobile_handler.handler_service = services
        self.mobile_handler.movement_commands = self.movement
        self.mobile_handler.player_handler = player
        self.mobile_handler.message_bus = self.bus
        handlers["mh"] = self.mobile_handler

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

    def bound_mayor(self):
        mayor = self.special_actor("the mayor")
        special = next(special for special in self.specials if special.name == "spec_mayor")
        mayor.special_name = special.name
        mayor.special_function = list(special.special_function)
        return mayor

    async def test_bundled_mage_teleport_sends_destination_look_then_prompt(self):
        mage = self.special_actor("the mage")
        mage.special_name = self.mage_special.name
        mage.special_function = list(self.mage_special.special_function)
        CharacterApi.set_position(mage, "POS_FIGHTING")
        CharacterApi.set_position(self.actor, "POS_FIGHTING")
        mage.fighting, self.actor.fighting = self.actor, mage
        self.destination.name = "A distant square"
        self.destination.description = "A dry fountain stands at the center."
        self.destination.light = 1
        self.actor.prompt_format = PromptFormat(room_name=True)
        self.messages[self.actor.id] = Mock(spec=TelnetConnection, is_closed=Mock(return_value=False),
                                            send_message=AsyncMock())
        self.rooms.get = self.rooms.get_or_none
        handler = self.mobile_handler
        player = handler.player_handler
        player.info_commands.PlayerActBits = self.enums.get("playerActBits")
        player.area_registry = NS(get_or_none=lambda **_: NS(name="Destination area"))
        player._send_prompt = PlayerHandler._send_prompt.__get__(player)
        handler.spell_registry = NS(all_spells=lambda: [self.teleport])
        handler.skill_registry = self.skill_registry
        handler.rng = NS(number_bits=lambda _: 0)
        handler.spell_api = SpellApi(self.effects, self.api)

        with patch.object(MobileApi, "choose_weighted", return_value="teleport"), \
                patch.object(handler.spell_api, "random_room", return_value=self.destination) as random_room, \
                patch.object(handler.spell_api, "saves_spell", return_value=True) as saves_spell:
            self.assertTrue(await handler.execute_special_function(mage, self.room))
            random_room.assert_not_called()
            self.assertEqual([], self.heard(self.actor))
            self.assertIs(self.actor, self.room.characters[self.actor.id])

            saves_spell.return_value = False
            self.assertTrue(await handler.execute_special_function(mage, self.room))

        self.assertIs(self.actor, self.destination.characters[self.actor.id])
        self.assertNotIn(self.actor.id, self.room.characters)
        self.assertIs(mage, self.room.mobiles[mage.id])
        messages = self.heard(self.actor)
        self.assertGreaterEqual(len(messages), 4)
        self.assertIn("casts teleport", messages[0])
        self.assertEqual("You have been teleported!\r\n", messages[1])
        self.assertIn(self.destination.name, messages[2])
        self.assertIn(self.destination.description, messages[2])
        self.assertEqual(f"\r\n< {self.destination.name}>", messages[-1].rstrip())
        handler.logger.error.assert_not_called()

    async def test_bundled_mage_teleport_looks_and_prompts_in_switched_body(self):
        mage = self.special_actor("the mage")
        mage.bind_special(self.mage_special)
        body = self.npc()
        body.id = "switched-body"
        body.context = {"controller_original": self.actor}
        body.prompt_format = PromptFormat(room_name=True)
        body.carriage_return = True
        mage.fighting, body.fighting = body, mage
        CharacterApi.set_position(mage, "POS_FIGHTING")
        CharacterApi.set_position(body, "POS_FIGHTING")
        self.room.add_mobile_to_room(body)
        self.messages[body.id] = Mock(spec=TelnetConnection, is_closed=Mock(return_value=False),
                                      send_message=AsyncMock())
        self.registries.character_registry.get = lambda id: body if id == body.id else self.actor
        self.rooms.get = self.rooms.get_or_none
        self.destination.name = "A distant square"
        self.destination.description = "A dry fountain stands at the center."
        self.destination.light = 1

        handler = self.mobile_handler
        player = handler.player_handler
        player.info_commands.PlayerActBits = self.enums.get("playerActBits")
        player.area_registry = NS(get_or_none=lambda **_: NS(name="Destination area"))
        player._send_prompt = PlayerHandler._send_prompt.__get__(player)
        handler.spell_registry = NS(all_spells=lambda: [self.teleport])
        handler.skill_registry = self.skill_registry
        handler.rng = NS(number_bits=lambda _: 0)
        handler.spell_api = SpellApi(self.effects, self.api, connection_manager=self.bus.connection_manager)

        with patch.object(MobileApi, "choose_weighted", return_value="teleport"), \
                patch.object(handler.spell_api, "random_room", return_value=self.destination), \
                patch.object(handler.spell_api, "saves_spell", return_value=False):
            self.assertTrue(await handler.execute_special_function(mage, self.room))

        self.assertIs(body, self.destination.mobiles[body.id])
        notices = self.heard(body)
        self.assertEqual("You have been teleported!\r\n", notices[0])
        self.assertIn(self.destination.description, notices[1])
        self.assertEqual(f"\r\n< {self.destination.name}>", notices[-1].rstrip())
        handler.logger.error.assert_not_called()

    async def test_mobile_special_skips_invalid_and_stale_room_views(self):
        mobile = self.special_actor("a mobile")
        mobile.special_function = [
            "lambda ctx: ctx.queue_payload({'to_room_obj': ctx.room})",
            "lambda ctx: ctx.queue_payload({'to_room_obj': ctx.handler.room_registry.get_or_none(vnum='101'), "
            "'view_character': ctx.room.players_in_room()[0]})",
            "lambda ctx: ctx.queue_payload({'to_room': 'Still here.\\r\\n', 'targets': ctx.room.players_in_room()})",
        ]

        self.assertFalse(await self.mobile_handler.execute_special_function(mobile, self.room))

        self.assertEqual(["Still here.\r\n"], self.heard(self.actor))
        self.mobile_handler.player_handler._send_prompt.assert_not_awaited()
        self.mobile_handler.logger.error.assert_called_once()

    async def test_mayor_initializes_and_pauses_a_due_route_during_combat(self):
        mayor = self.bound_mayor()
        handler = self.mobile_handler
        mage = Special(id="test-delegate", name="spec_cast_mage")
        handler.special_registry.register(mage)
        cases = (
            (6, "ctx.finish()", False, "Oe"),
            (6, "False", False, "Oe"),
            (20, "ctx.mark_performed()", True, "CE"),
        )
        for hour, outcome, cast, path_marker in cases:
            with self.subTest(hour=hour, outcome=outcome):
                mayor._special_state = {}
                mayor.fighting = self.actor
                CharacterApi.set_position(mayor, "POS_FIGHTING")
                handler.weather_handler.time_info.hour = hour
                mage.special_function = [f"lambda ctx: {outcome}"]
                self.messages[self.actor.id].send_message.reset_mock()

                self.assertEqual(cast, await handler.execute_special_function(mayor, self.room))
                self.assertTrue(mayor._special_state["move"])
                self.assertIn(path_marker, mayor._special_state["path"])
                self.assertEqual(0, mayor._special_state["pos"])

                handler.weather_handler.time_info.hour = 12
                self.assertEqual(cast, await handler.execute_special_function(mayor, self.room))
                self.assertEqual(0, mayor._special_state["pos"])
                self.assertEqual([], self.heard(self.actor))

                mayor.fighting = None
                CharacterApi.set_position(mayor, "POS_SLEEPING")
                self.assertFalse(await handler.execute_special_function(mayor, self.room))
                self.assertEqual(1, mayor._special_state["pos"])
                self.assertEqual(CharacterApi.pos_value("POS_STANDING"), CharacterApi.position_value(mayor))
                self.assertEqual(["The mayor awakens and groans loudly.\r\n"], self.heard(self.actor))

    async def test_mayor_route_move_leaves_generic_processing_in_the_destination(self):
        mayor = self.bound_mayor()
        mayor._special_state = {"path": "0.", "move": True, "pos": 0}
        handler = self.mobile_handler
        handler.area_registry = NS(get_or_none=lambda **_: None)
        handler.shop_registry = NS(find_by_keeper_vnum=lambda _: None)
        handler._execute_generic_special = AsyncMock()

        await handler.mobile_update()

        self.assertIs(mayor, self.destination.mobiles[mayor.id])
        self.assertEqual(1, mayor._special_state["pos"])
        self.assertEqual([
            call(mayor, self.destination, "spec_scavenge"),
            call(mayor, self.destination, "spec_wander"),
        ], handler._execute_generic_special.await_args_list)

    async def test_mayor_replays_both_bundled_midgaard_routes(self):
        mayor = self.bound_mayor()
        self.room.remove_mobile_from_room(mayor)
        special = next(special for special in self.specials if special.name == mayor.special_name)
        collections = load_collections(ROOT / "resources/collections", ["rooms", "resets"])
        room_service = RoomService.__new__(RoomService)
        room_service.logger = Mock()
        rooms = {}
        for document in collections["rooms"].documents:
            if document["areaId"] == special.area_id:
                data = {key: value for key, value in document.items() if key not in {"_id", "_class", "mobiles"}}
                room = room_service._build_fetch_item({**data, "id": document["_id"]["$oid"]})
                rooms[str(room.vnum)] = room
        self.world[:] = rooms.values()
        area_handler = AreaHandler.__new__(AreaHandler)
        area_handler.room_registry = self.rooms
        area_handler.ExitFlags = self.exit_flags
        for document in collections["resets"].documents:
            if document["areaId"] == special.area_id and document.get("command") == "D":
                data = {key: value for key, value in document.items() if key not in {"_id", "_class"}}
                reset = Reset.from_json({**data, "id": document["_id"]["$oid"]})
                self.assertTrue(area_handler._do_door_reset(False, reset))

        office = rooms["3138"]
        office.add_mobile_to_room(mayor)
        CharacterApi.set_position(mayor, "POS_SLEEPING")
        self.assertTrue(int(rooms["3105"].room_flags) & self.enums.get("roomFlags").ROOM_NO_MOB)
        gates = {
            "3041": (rooms["3041"].get_exit(1), rooms["3053"].get_exit(3)),
            "3040": (rooms["3040"].get_exit(3), rooms["3052"].get_exit(1)),
        }
        closed_bit = self.exit_flags.EX_CLOSED
        for sides in gates.values():
            for gate in sides:
                gate.exit_flags |= closed_bit

        handler = self.mobile_handler
        for hour, expected_closed in ((6, False), (20, True)):
            with self.subTest(hour=hour):
                gate_rooms = []
                visited = set()
                handler.weather_handler.time_info.hour = hour
                for _ in range(64):
                    room = self.rooms.get_or_none(id=mayor.room_id)
                    visited.add(str(room.vnum))
                    before = {vnum: sides[0].exit_flags for vnum, sides in gates.items()}
                    self.assertFalse(await handler.execute_special_function(mayor, room))
                    for vnum, (gate, _) in gates.items():
                        if (before[vnum] ^ gate.exit_flags) & closed_bit:
                            self.assertEqual(vnum, str(room.vnum))
                            gate_rooms.append(vnum)
                    if not mayor._special_state["move"]:
                        break
                    handler.weather_handler.time_info.hour = hour + 1
                self.assertFalse(mayor._special_state["move"])
                self.assertIn("3105", visited)
                self.assertEqual(["3041", "3040"], gate_rooms)
                for sides in gates.values():
                    for gate in sides:
                        self.assertEqual(expected_closed, bool(gate.exit_flags & closed_bit))
                self.assertIs(mayor, office.mobiles[mayor.id])
                self.assertEqual(CharacterApi.pos_value("POS_SLEEPING"), CharacterApi.position_value(mayor))
        handler.logger.error.assert_not_called()

    async def test_mayor_route_respects_a_closed_door_and_advances(self):
        mayor = self.bound_mayor()
        self.exit.exit_flags |= self.exit_flags.EX_CLOSED

        self.assertFalse(await self.mayor_step(mayor, "0"))

        self.assertIs(mayor, self.room.mobiles[mayor.id])
        self.assertEqual(1, mayor._special_state["pos"])
        self.mobile_handler.logger.error.assert_not_called()

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

        self.assertFalse(await self.mayor_step(mayor, "O"))
        self.assertFalse((self.exit.exit_flags | self.reverse.exit_flags) & closed)
        self.assertFalse(await self.mayor_step(mayor, "O"))
        self.assertFalse(await self.mayor_step(mayor, "C"))
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
                self.assertFalse(await self.mayor_step(mayor, "O"))
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

    async def test_fido_devours_the_newest_corpse_first(self):
        fido = self.special_actor("fido")
        older = item("older corpse", itemType="corpse_npc")
        newer = item("newer corpse", itemType="corpse_npc")
        spill = item("spilled coin")
        newer.contains.append(spill)
        self.room.add_item_to_room(older)
        self.room.add_item_to_room(newer)

        self.assertTrue(await self.mobile_handler._execute_generic_special(fido, self.room, "spec_fido"))

        self.assertEqual({older.id: older, spill.id: spill}, self.room.contents)
        self.assertEqual([], newer.contains)

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

        CharacterApi.set_position(mayor, "POS_SLEEPING")
        self.assertFalse(await self.mayor_step(mayor, "W"))
        self.assertEqual(CharacterApi.pos_value("POS_STANDING"), CharacterApi.position_value(mayor))
        self.flag(mayor, "AFF_INVISIBLE", False)
        self.assertFalse(await self.mayor_step(mayor, "S"))
        self.assertEqual(CharacterApi.pos_value("POS_SLEEPING"), CharacterApi.position_value(mayor))

        self.assertEqual(["Someone awakens and groans loudly.\r\n",
                          "The mayor lies down and falls asleep.\r\n"], self.heard(self.actor))
        self.assertEqual([], self.heard(sleeper))
