"""Historical pre-remediation probes, retained as review evidence.

Their discrepancy assertions no longer pass after the fixes. Current desired
behavior is covered by tests/test_repository_parity_remediation.py.
"""
import asyncio
import json
import sys
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import Mock, AsyncMock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tests.test_speech_text_parity import SpeechTextTests
from mobile.MobileFactory import MobileFactory
from api.SpellApi import SpellApi
from api.CharacterApi import CharacterApi
from skill.SpellContext import SpellContext
from game.EntityUpdateHandler import EntityUpdateHandler


async def main():
    SpeechTextTests.setUpClass()
    fixture = SpeechTextTests()
    fixture.setUp()
    results = {}
    try:
        interpreter = fixture.interpreter
        commands = {name: fixture.command(name) for name in fixture.documents}
        registry = NS(get_or_none=lambda **kw: commands.get(kw.get('name')),
                      all_commands=lambda: list(commands.values()))
        interpreter.registry_service = NS(interp_registry=registry)
        interpreter.interp_registry = registry
        interpreter.social_registry = NS(get_or_none=lambda **kw: None)
        interpreter.command_not_found_message = fixture.bus.text_to_message('Huh?\r\n')
        interpreter.logger = Mock()
        interpreter.command_audit = None
        for text in ('say hello   brave world', "'hello", '.hello', 'recal', 'say hello'):
            for connection in fixture.connections.values():
                connection.send_message.reset_mock()
            await interpreter.handle_command(None, fixture.actor, text)
            results[text] = {'actor': fixture.messages(fixture.actor), 'bob': fixture.messages(fixture.bob)}
        assert results['say hello   brave world']['bob'] == ["Alice says 'hello brave world'\r\n"]
        assert results["'hello"]['actor'] == ['Huh?\r\n']
        assert results['.hello']['actor'] == ['Huh?\r\n']
        assert results['recal']['actor'] == ['Huh?\r\n']
        assert results['say hello']['bob'] == ["Alice says 'hello'\r\n"]

        results['fallback_attack_types'] = sorted({MobileFactory._random_dam_type() for _ in range(100)})
        assert results['fallback_attack_types'] == [3]

        fixture.flag(fixture.actor, 'AFF_INVISIBLE')
        assert not CharacterApi.can_see(fixture.bob, fixture.actor, fixture.room)
        api = SpellApi.__new__(SpellApi)
        context = SpellContext(actor=fixture.actor, spell=NS(name='armor'), handler=NS(),
                               room=fixture.room, target=fixture.actor, target_kind='char')
        api.queue_cast_announcement(context)
        results['invisible_cast_announcement'] = [
            {'text': p['to_room'], 'targets': [c.name for c in p['targets']]}
            for p in context.payloads if 'to_room' in p
        ]
        assert any('Alice utters' in row['text'] and 'Bob' in row['targets']
                   for row in results['invisible_cast_announcement'])

        mobile = fixture.npc()
        mobile.zone = NS(id='home-area')
        mobile.area_id = 'home-area'
        mobile.hit = mobile.max_hit = mobile.mana = mobile.max_mana = 100
        mobile.movement = mobile.max_movement = 100
        fixture.room.add_mobile_to_room(mobile)
        ticker = EntityUpdateHandler.__new__(EntityUpdateHandler)
        ticker.PositionsEnum = fixture.enums.get('positions')
        ticker.AffectedBits = fixture.enums.get('affectedBy')
        ticker.rng = Mock(number_percent=Mock(return_value=1))
        ticker.fight_handler = Mock()
        ticker.effect_update_handler = NS(tick_effects=AsyncMock(), tick_status_effects=AsyncMock())
        await ticker._tick(mobile, fixture.room)
        results['foreign_area_mobile_tick'] = {
            'home_area': mobile.zone.id, 'current_area': fixture.room.area_id,
            'retained_in_room': mobile.id in fixture.room.mobiles,
            'home_roll_calls': ticker.rng.number_percent.call_count}
        assert mobile.id in fixture.room.mobiles
        assert ticker.rng.number_percent.call_count == 0
    finally:
        fixture.doCleanups()
    output = json.dumps(results, indent=2)
    Path(__file__).with_name('repository-rom24-parity-2026-10-31-probes.json').write_text(output, encoding='utf-8')
    print(output)


if __name__ == '__main__':
    asyncio.run(main())
