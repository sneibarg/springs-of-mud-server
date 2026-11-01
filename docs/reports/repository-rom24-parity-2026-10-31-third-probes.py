"""Read-only production probes for the third October 31 ROM24 review.

Assertions reproduce discrepancies, not desired behavior.
"""
import asyncio
from copy import deepcopy
import json
from pathlib import Path
import sys
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tests import test_repository_parity_remediation as fixtures
from api.CharacterApi import CharacterApi
from area.RoomHandler import RoomHandler
from area.RoomService import RoomService
from combat.CombatHandler import FightHandler
from devtools.collection_query import load_collections
from interp.commands.Info import Info
from item.Effect import Effect
from item.EffectUpdateHandler import EffectUpdateHandler
from item.ItemHandler import ItemHandler
from item.ExtraDescriptionData import ExtraDescriptionData


async def main():
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
        message = combat.dam_message(f.actor, f.bob, 10)
        payload = combat.build_round_payload(f.actor, f.bob, f.room, message)
        with patch.object(f.commands, 'execute', return_value=payload):
            await f.execute('gossip', 'ignored')
        results['invisible_damage_victim'] = {'Alice': f.messages(f.actor), 'Cara': f.messages(f.cara)}
        assert 'Bob' in results['invisible_damage_victim']['Alice'][0]
        assert 'Bob' in results['invisible_damage_victim']['Cara'][0]

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
        assert any('Bob' in text for text in f.messages(f.actor))
        assert f.messages(f.cara)
        f.flag(f.bob, 'AFF_INVISIBLE', False)
        f.cara.set_position(int(f.enums.get('positions').POS_STANDING))

        # Actual public look/exits commands with production domain handlers.
        player = f.interpreter.handler_service.get_handler('ph')
        f.rooms.get = f.rooms.get_or_none
        rh = RoomHandler.__new__(RoomHandler)
        rh.room_registry, rh.message_bus = f.rooms, f.bus
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
        assert results['look_mural'] == ['You do not see that here.\r\n']

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
            assert any('Hidden Vault' in text for text in f.messages(f.actor))
        f.flag(f.actor, 'AFF_BLIND', False)

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
        for original_off, body_off in ((True, False), (False, True)):
            f.bob.status_flags.assign_bitfield('comm', int(flags.COMM_NOGOSSIP) if original_off else 0)
            body.status_flags.assign_bitfield('comm', int(flags.COMM_NOGOSSIP) if body_off else 0)
            clear()
            await f.interpreter.handle_command(None, f.actor, 'gossip hello')
            results['switched_gossip_original_off_' + str(original_off)] = f.messages(f.bob)
            assert bool(f.messages(f.bob)) == original_off
    finally:
        holder.doCleanups()
    output = json.dumps(results, indent=2)
    Path(__file__).with_suffix('.json').write_text(output, encoding='utf-8')
    print(output)


if __name__ == '__main__':
    asyncio.run(main())
