from copy import deepcopy
import json
from pathlib import Path
import unittest
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
from tests import test_repository_parity_remediation as fixtures
from api.CharacterApi import CharacterApi
from area.RoomHandler import RoomHandler
from area.RoomService import RoomService
from combat.CombatHandler import FightHandler
from combat.CombatDeathHandler import CombatDeathHandler
from devtools.collection_query import load_collections
from interp.commands.Info import Info
from item.Effect import Effect
from item.EffectUpdateHandler import EffectUpdateHandler
from item.ItemHandler import ItemHandler
from item.ItemUpdateHandler import ItemUpdateHandler
from item.ExtraDescriptionData import ExtraDescriptionData


async def check_public_paths(test):
    fixtures.PublicInputTests.setUpClass()
    holder = fixtures.PublicInputTests()
    holder.setUp()
    f = holder.fixture
    results = {}
    try:
        def clear():
            for connection in f.connections.values():
                connection.send_message.reset_mock()

        f.flag(f.bob, 'AFF_INVISIBLE')
        assert not CharacterApi.can_see(f.actor, f.bob, f.room)
        combat = FightHandler.__new__(FightHandler)
        combat.room_registry = f.rooms
        message = combat.dam_message(f.actor, f.bob, 10)
        message = combat._merge_attack_payloads(message, {"to_room": "A second combat notice.\r\n"})
        payload = combat.build_round_payload(f.actor, f.bob, f.room, message)
        with patch.object(f.commands, 'execute', return_value=payload):
            await f.execute('gossip', 'ignored')
        results['invisible_damage_victim'] = {'Alice': f.messages(f.actor), 'Cara': f.messages(f.cara)}
        test.assertIn('someone', results['invisible_damage_victim']['Alice'][0].lower())
        test.assertIn('someone', results['invisible_damage_victim']['Cara'][0].lower())
        test.assertIn('A second combat notice.', results['invisible_damage_victim']['Cara'][0])

        f.cara.set_position(int(f.enums.get('positions').POS_SLEEPING))
        death = CombatDeathHandler.__new__(CombatDeathHandler)
        death.text = lambda channel, key, **tokens: f"{tokens['victim']} is DEAD!\r\n"
        notice = death.room_notice(f.room, "dead", f.bob)
        test.assertIn(f.actor, notice["targets"])
        test.assertNotIn(f.cara, notice["targets"])
        test.assertEqual("someone is DEAD!\r\n", notice["to_room"].for_recipient(f.actor.id))
        f.flag(f.actor, 'AFF_DETECT_INVIS')
        notice = death.room_notice(f.room, "dead", f.bob)
        test.assertEqual("Bob is DEAD!\r\n", notice["to_room"].for_recipient(f.actor.id))
        f.flag(f.actor, 'AFF_DETECT_INVIS', False)

        for damage_type, immune, expected in (
            ('TYPE_HIT', False, 'You hit yourself.'),
            ('fireball', False, 'Your fireball hits you.'),
            ('fireball', True, 'Luckily, you are immune to that.'),
        ):
            result = combat.dam_message(f.actor, f.actor, 10, dt=damage_type, immune=immune)
            round_payload = combat.build_round_payload(f.actor, f.actor, f.room, result)
            test.assertEqual(round_payload['to_char'].strip(), expected)
            test.assertFalse(round_payload.get('to_victim'))
            test.assertNotIn(f.cara, round_payload['targets'])
            test.assertIn(f.bob, round_payload['targets'])
        f.cara.set_position(int(f.enums.get('positions').POS_STANDING))


        documents = load_collections(ROOT / 'resources/collections', ['spells'])['spells'].documents
        from skill.Spell import Spell
        poison = Spell.from_json(deepcopy(next(doc for doc in documents if doc['name'] == 'poison')))
        f.registries.spell_registry = NS(all_spells=lambda: [poison],
                                       get_or_none=lambda **kw: poison if kw.get('name') in ('poison', 'spell.poison') else None)
        f.registries.interp_registry = f.interpreter.interp_registry
        poison_effect = Effect(type='spell.poison', level=20, duration=5, location='APPLY_STR', modifier=-1,
                               bitvector='AFF_POISON')
        f.effects.affect_to_char(f.bob, poison_effect)
        periodic = EffectUpdateHandler(f.registries, f.enums, f.effects,
                                      NS(apply_periodic_damage=AsyncMock()), f.bus)
        f.cara.set_position(int(f.enums.get('positions').POS_SLEEPING))
        clear()
        await periodic.tick_status_effects(f.bob, f.room)
        results['invisible_poison_tick'] = {'Alice': f.messages(f.actor), 'sleeping_Cara': f.messages(f.cara)}
        test.assertTrue(any('someone' in text.lower() for text in f.messages(f.actor)))
        test.assertEqual(f.messages(f.cara), [])
        f.flag(f.bob, 'AFF_INVISIBLE', False)
        f.cara.set_position(int(f.enums.get('positions').POS_STANDING))

        # Actual public look/exits commands with production domain handlers.
        player = f.interpreter.handler_service.get_handler('ph')
        f.rooms.get = f.rooms.get_or_none
        rh = RoomHandler.__new__(RoomHandler)
        rh.room_registry, rh.message_bus, rh.registry_service = f.rooms, f.bus, f.registries
        ih = ItemHandler.__new__(ItemHandler)
        ih.room_registry, ih.message_bus = f.rooms, f.bus
        info = Info.__new__(Info)
        info.room_registry, info.interp_api = f.rooms, f.api
        player.info_commands = info
        f.interpreter.handler_service = NS(get_handler=lambda key: {'ph': player, 'rh': rh, 'ih': ih}[key])

        room_service = RoomService.__new__(RoomService)
        f.room.extra_description = room_service._load_extra_description({'extra_description': json.dumps({
            'valid': True, 'keyword': 'banner', 'description': 'A bright banner.',
            'next': {'valid': True, 'keyword': 'mural', 'description': 'A hidden mural.'}})})
        assert len(list(ExtraDescriptionData.entries(f.room.extra_description))) == 2
        for token in ('banner', 'mural'):
            clear()
            await f.interpreter.handle_command(None, f.actor, 'look ' + token)
            results['look_' + token] = f.messages(f.actor)
        assert results['look_banner'] == ['A bright banner.\r\n']
        assert results['look_mural'] == ['A hidden mural.\r\n']

        f.destination.name = 'Hidden Vault'
        exit_bits, room_bits = f.enums.get('exitFlags'), f.enums.get('roomFlags')
        for scenario in ('closed', 'restricted', 'dark_destination', 'blind'):
            f.exit.exit_flags = int(exit_bits.EX_ISDOOR)
            f.destination.room_flags = 0
            f.flag(f.actor, 'AFF_BLIND', False)
            if scenario == 'closed':
                f.exit.exit_flags |= int(exit_bits.EX_CLOSED)
            elif scenario == 'restricted':
                f.destination.room_flags = int(room_bits.ROOM_IMP_ONLY)
                assert not CharacterApi.can_see_room(f.actor, f.destination)
            elif scenario == 'dark_destination':
                f.destination.room_flags = int(room_bits.ROOM_DARK)
                assert f.destination.is_room_dark()
            else:
                f.flag(f.actor, 'AFF_BLIND')
            clear()
            await f.interpreter.handle_command(None, f.actor, 'exits')
            results['exits_' + scenario] = f.messages(f.actor)
            test.assertTrue(f.messages(f.actor))
            expected = {'closed': 'None.', 'restricted': 'None.', 'dark_destination': 'Too dark to tell',
                        'blind': "You can't see a thing!"}[scenario]
            test.assertIn(expected, f.messages(f.actor)[0])
            test.assertNotIn('Hidden Vault', f.messages(f.actor)[0])
        f.flag(f.actor, 'AFF_BLIND', False)

        f.destination.room_flags = int(room_bits.ROOM_DARK)
        clear()
        await rh.print_exits(f.actor, automatic=True)
        test.assertEqual(f.messages(f.actor), ['[Exits: north]\r\n'])

        f.actor.trust = 60
        f.destination.room_flags = 0
        clear()
        await f.interpreter.handle_command(None, f.actor, 'exits')
        test.assertIn(f'({f.destination.vnum})', f.messages(f.actor)[0])
        f.actor.trust = 0

        decay = ItemUpdateHandler.__new__(ItemUpdateHandler)
        decay.message_bus = f.bus
        item = NS(item_type="ITEM_TRASH", short_description="a hidden trinket")
        f.cara.set_position(int(f.enums.get('positions').POS_SLEEPING))
        clear()
        with patch("util.LookupUtil.LookupUtil.object_visible", side_effect=lambda observer, room, obj: observer is f.bob):
            await decay._emit_item_message("$p crumbles into dust.", item, "room", f.room, f.room, decay=True)
        test.assertEqual(["Something crumbles into dust.\r\n"], f.messages(f.actor))
        test.assertEqual(["A hidden trinket crumbles into dust.\r\n"], f.messages(f.bob))
        test.assertFalse(f.messages(f.cara))
        f.cara.set_position(int(f.enums.get('positions').POS_STANDING))

        # A switched recipient's descriptor uses the original's preferences in C.
        f.bob.trust = 60
        body = f.npc()
        body.context = {'controller_original': f.bob}
        f.connections[body.id] = f.connections[f.bob.id]
        f.room.add_mobile_to_room(body)
        sessions = NS(get_playing_sessions=lambda: [NS(character=f.actor),
                                                   NS(character=body, metadata={'switched_original': f.bob})])
        f.commands.session_handler = sessions
        flags = f.enums.get('commFlags')
        for original_flags, body_flags in ((flags.COMM_NOGOSSIP, 0), (0, flags.COMM_NOGOSSIP),
                                           (flags.COMM_QUIET, 0), (0, flags.COMM_QUIET)):
            f.bob.status_flags.assign_bitfield('comm', int(original_flags))
            body.status_flags.assign_bitfield('comm', int(body_flags))
            clear()
            await f.interpreter.handle_command(None, f.actor, 'gossip hello')
            test.assertEqual(bool(f.messages(f.bob)), not original_flags)
    finally:
        holder.doCleanups()


class RepositoryVisibilityParityTests(unittest.IsolatedAsyncioTestCase):
    async def test_public_visibility_paths(self):
        await check_public_paths(self)

