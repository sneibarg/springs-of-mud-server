"""Read-only production probes for the second October 31 parity review.

Historical pre-remediation assertions are retained as review evidence and no
longer pass after the fixes. Desired behavior is covered by
tests/test_additional_repository_parity_fixes.py.
"""
import asyncio
from copy import deepcopy
import json
from pathlib import Path
import sys
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tests.test_repository_parity_remediation import PublicInputTests
from api.CharacterApi import CharacterApi
from api.SpellApi import SpellApi
from devtools.collection_query import load_collections
from player.CharacterService import CharacterService
from skill.Spell import Spell
from skill.SpellContext import SpellContext
from interp.commands.Info import Info
from server.handlers.ConnectionHandler import ConnectionHandler
from server.session.SessionState import SessionState
from combat.CombatHandler import FightHandler
from util.ElementalExposure import ElementalExposure
from tests.test_movement_rules_parity import item


async def main():
    PublicInputTests.setUpClass()
    holder = PublicInputTests()
    holder.setUp()
    f = holder.fixture
    results = {}
    try:
        async def command(text):
            for connection in f.connections.values():
                connection.send_message.reset_mock()
            await f.interpreter.handle_command(None, f.actor, text)
            return {person.name: f.messages(person) for person in (f.actor, f.bob, f.cara)}

        results['comma'] = await command(',waves')
        results['emote_control'] = await command('emote waves')
        assert results['comma']['Bob'] == [] and results['emote_control']['Bob']
        results['semicolon'] = await command(';private group message')
        results['gtell_control'] = await command('gtell private group message')
        assert results['semicolon']['Bob'] == [] and results['gtell_control']['Bob']

        flags = f.enums.get('commFlags')
        f.bob.status_flags.set_flag('comm', flags.COMM_NOGOSSIP)
        f.cara.status_flags.set_flag('comm', flags.COMM_NOGRATS)
        results['dot_with_channel_optouts'] = await command('.hello')
        results['gossip_control'] = await command('gossip hello')
        assert results['dot_with_channel_optouts']['Bob'] and not results['dot_with_channel_optouts']['Cara']
        assert not results['gossip_control']['Bob'] and results['gossip_control']['Cara']

        for person in (f.actor, f.bob, f.cara):
            person.status_flags.assign_bitfield('comm', 0)
        try:
            await command('pose')
        except AttributeError as error:
            results['pose_exception'] = str(error)
        assert '_room_targets' in results.get('pose_exception', '')

        f.room.remove_player_from_room(f.bob)
        f.destination.add_player_to_room(f.bob)
        f.bob.room_id, f.bob.area_id = f.destination.id, f.destination.area_id
        f.flag(f.actor, 'AFF_INVISIBLE')
        assert not CharacterApi.can_see(f.cara, f.actor, f.room)
        document = next(doc for doc in load_collections(ROOT / 'resources/collections', ['spells'])['spells'].documents
                        if doc['name'] == 'teleport')
        spell = Spell.from_json(deepcopy(document))
        api = SpellApi(f.effects, f.api)
        handler = NS(spell_api=api, registry_service=f.registries)
        context = SpellContext(f.actor, spell, handler, f.room, target=f.actor)
        with patch.object(api, 'random_room', return_value=f.destination):
            assert api.execute_lambdas(context)
        assert not CharacterApi.can_see(f.bob, f.actor, f.destination)
        results['invisible_teleport_notices'] = [
            {'text': str(payload['to_room']), 'targets': [target.name for target in payload['targets']]}
            for payload in context.payloads if payload.get('to_room')]
        assert any('Alice vanishes!' in row['text'] for row in results['invisible_teleport_notices'])
        assert any('Alice slowly fades' in row['text'] for row in results['invisible_teleport_notices'])

        # Persisted timing fields survive a fresh login; no HTTP or real socket.
        now = 1800000000
        f.actor.status_flags.played = 3600
        f.actor.status_flags.logon = now - 72000
        account = NS(first_name='Test', last_name='Player', current_characters=[], ansi_enabled=False)
        login = ConnectionHandler.__new__(ConnectionHandler)
        login.registry_service = NS(player_registry=NS(get_or_none=lambda **kw: account, get=lambda **kw: account),
                                    character_registry=NS(set_playing=Mock()))
        login._login_error = Mock(return_value='')
        login.logger = Mock()
        session = SessionState('fresh-login', player_id='account')
        await login._nanny(f.actor, session, NS(get_peer_info=lambda: None))
        with patch('interp.commands.Info.datetime') as clock:
            clock.now.return_value.timestamp.return_value = now
            score = Info.do_score(Info.__new__(Info), f.actor, f.ctx('score'))
        # Info.do_score returns before other collaborators are needed in this fixture.
        snapshot = CharacterService._serialize_character(f.actor)
        results['fresh_login_time'] = {'played': f.actor.status_flags.played,
                                       'logon': f.actor.status_flags.logon,
                                       'score_first_line': score.splitlines()[0],
                                       'saved_played': snapshot['statusFlags']['played'],
                                       'saved_logon': snapshot['statusFlags']['logon']}
        assert f.actor.status_flags.logon == now - 72000
        assert '21 hours' in score
        assert snapshot['statusFlags']['played'] == 3600
        victim = f.npc()
        victim.status_flags.set_flag('act', f.enums.get('actBits').ACT_NOALIGN)
        f.actor.current_time = now
        with patch('combat.CombatHandler.random.randint', side_effect=lambda low, high: low):
            inflated_xp = FightHandler.xp_compute(FightHandler.__new__(FightHandler), f.actor, victim, f.actor.level)
            f.actor.status_flags.logon = now
            actual_playtime_xp = FightHandler.xp_compute(FightHandler.__new__(FightHandler), f.actor, victim, f.actor.level)
        results['fresh_login_time'].update(stale_logon_xp=inflated_xp, fresh_logon_xp=actual_playtime_xp)
        assert inflated_xp > actual_playtime_xp

        f.destination.remove_player_from_room(f.actor)
        f.room.add_player_to_room(f.actor)
        f.actor.room_id, f.actor.area_id = f.room.id, f.room.area_id
        f.destination.remove_player_from_room(f.bob)
        f.room.add_player_to_room(f.bob)
        f.bob.room_id, f.bob.area_id = f.room.id, f.room.area_id
        f.flag(f.actor, 'AFF_INVISIBLE', False)
        weapon = item('blade', itemType='weapon', shortDescription='an invisible blade',
                      extraFlags=int(f.enums.get('itemFlags').ITEM_INVIS))
        rules = f.game_document['combat']['weaponHitEffects']['flaming']
        notice = ElementalExposure._messages(rules, 'hit', f.actor, f.bob, weapon, f.room)
        before = notice['to_room'].for_recipient(f.cara.id)
        assert 'something' in before and 'invisible blade' not in before
        combined = FightHandler._merge_attack_payloads({'to_room': 'Base hit.\r\n'}, notice)
        combined['targets'] = [f.cara]
        with patch.object(f.commands, 'execute', return_value=combined):
            await f.execute('gossip', 'ignored')
        results['weapon_proc_merge'] = {'before_merge_for_Cara': before,
                                         'merged_type': type(combined['to_room']).__name__,
                                         'delivered_to_Cara': f.messages(f.cara)}
        assert any('invisible blade' in text for text in f.messages(f.cara))
    finally:
        holder.doCleanups()
    output = json.dumps(results, indent=2)
    Path(__file__).with_suffix('.json').write_text(output, encoding='utf-8')
    print(output)


if __name__ == '__main__':
    asyncio.run(main())
