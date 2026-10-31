"""Historical review probes; all N01-N07 findings are now resolved and skipped.

Run from the checkout with .venv/Scripts/python.exe <this file>.
Current validation: python -m unittest tests.test_remaining_gameplay_parity.
Original probe bodies use real models/enums and narrow collaborators, not a C executable.
"""
import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tests.test_movement_rules_parity import MovementFixture, item
from api.MobileApi import MobileApi
from api.SpellApi import SpellApi
from combat.CombatHandler import FightHandler
from devtools.collection_query import load_collections
from item.Effect import Effect
from mobile.MobileContext import MobileContext
from skill.Spell import Spell
from skill.SpellContext import SpellContext
from util.EffectUtil import EffectUtil


class Fixture(MovementFixture, unittest.TestCase):
    pass


Fixture.setUpClass()
results = []
RESOLVED = {'N01', 'N02', 'N03', 'N04', 'N05', 'N06', 'N07'}


def probe(name, operation):
    if name[:3] in RESOLVED:
        return
    fixture = Fixture()
    fixture.setUp()
    try:
        results.append({'finding': name, 'observed': operation(fixture)})
    finally:
        fixture.doCleanups()


def permanent_dispel(f):
    mob = f.npc()
    f.effects.affect_to_char(mob, Effect(type='spell.sanctuary', level=20, duration=-1,
                                        bitvector='AFF_SANCTUARY'))
    with patch('util.EffectUtil.random.randint', return_value=60):
        removed = f.effects.check_dispel(20, mob, 'spell.sanctuary')
    assert removed
    return {'roll': 60, 'Python': 'permanent sanctuary removed',
            'C': 'resists (60 < 75), effect level reduced to 19'}


probe('N01 permanent-effect dispel resistance', permanent_dispel)


def npc_backstab(f):
    mob = f.npc()
    mob.level = 20
    mob.status_flags.set_flag('act', f.enums.get('actBits').ACT_THIEF)
    handler = FightHandler.__new__(FightHandler)
    handler.ActBits = f.enums.get('actBits')
    handler._current_hitroll = lambda entity: 0
    reduction = handler._thac0(mob, 'TYPE_HIT', 100) - handler._thac0(mob, 'backstab', 100)
    rating = f.skill_api.get_rating(mob, f.skills['backstab'])
    assert reduction == 1000 and rating == 60
    return {'Python_hit_THAC0_bonus': reduction, 'activation_proficiency': rating, 'C_hit_THAC0_bonus': 400}


probe('N02 NPC backstab proficiency in hit calculation', npc_backstab)


def nasty_opening(f):
    mob = f.npc()
    mob.level = 10
    f.actor.level = 15
    f.room.add_player_to_room(f.actor)
    fight = NS(is_safe=Mock(return_value=(False, '')), set_fighting=Mock(),
               multi_hit=Mock(return_value={}), do_backstab=Mock(), do_murder=Mock())
    context = MobileContext(actor=mob, room=f.room, handler=NS(fight_handler=fight))
    assert MobileApi.nasty_opening_attack(context, (1, 9), ['backstab', 'murder'])
    fight.multi_hit.assert_called_once_with(mob, f.actor, dt='TYPE_UNDEFINED')
    return {'Python': 'ordinary multi_hit; skills argument unused', 'C': 'do_backstab, then do_murder only if not fighting'}


probe('N03 spec_nasty opening attack', nasty_opening)


def nasty_flee(f):
    mob = f.npc()
    mob.fighting = f.actor
    f.room.add_mobile_to_room(mob)
    fight = NS(stop_fighting=Mock(side_effect=lambda entity, **kw: setattr(entity, 'fighting', None)))
    context = MobileContext(actor=mob, room=f.room, handler=NS(fight_handler=fight))
    with patch.object(MobileApi, 'choose_weighted', return_value='flee'):
        assert MobileApi.nasty_combat_turn(context)
    assert mob.room_id == f.room.id and mob.fighting is None
    return {'Python': 'drops combat without moving or trying an exit', 'C': 'do_flee attempts physical escape'}


probe('N04 spec_nasty flee', nasty_flee)


def world_target(f):
    first, second = f.npc(), f.npc()
    first.id, first.room_id = 'guard-a', f.destination.id
    second.id, second.room_id = 'guard-b', f.temple.id
    first.name = second.name = 'guard'
    f.destination.add_mobile_to_room(first)
    f.temple.add_mobile_to_room(second)
    api = SpellApi(f.effects, f.api)
    api._room_registry = lambda ctx: f.rooms
    context = SpellContext(actor=f.actor, spell=NS(), handler=NS(), room=f.room, target_name='guard')
    try:
        api.find_world_target(context)
    except TypeError as error:
        assert '4 were given' in str(error)
        docs = load_collections(ROOT / 'resources/collections', ['spells'])['spells'].documents
        failed = []
        for document in docs:
            if document['name'] not in ('summon', 'gate', 'portal', 'nexus'):
                continue
            spell = Spell.from_json(document)
            cast = SpellContext(actor=f.actor, spell=spell, handler=NS(spell_api=api),
                                room=f.room, target_name='guard')
            with patch.object(api.logger, 'error'):
                api.execute_lambdas(cast)
            assert cast.failed
            failed.append(spell.name)
        assert len(failed) == 4
        return {'Python': str(error), 'C': 'resolves a visible world guard',
                'actual_spell_documents_fizzled': failed}
    raise AssertionError('Expected the invalid PlayerUtil.get_target call')


probe('N05 world spell target lookup raises', world_target)


def conflicting_defenses(f):
    mob = f.npc()
    handler = FightHandler.__new__(FightHandler)
    handler.MobImmunity = f.enums.get('mobImmunity')
    handler.MobResistance = f.enums.get('mobResistance')
    handler.MobVulnerability = f.enums.get('mobVulnerability')
    mob.status_flags.set_flag('vuln', handler.MobVulnerability.VULN_FIRE)
    mob.status_flags.set_flag('imm', handler.MobImmunity.IMM_FIRE)
    immune = handler._check_immunity(mob, 'DAM_FIRE')
    mob.status_flags.unset_flag('imm', handler.MobImmunity.IMM_FIRE)
    mob.status_flags.set_flag('res', handler.MobResistance.RES_FIRE)
    resistant = handler._check_immunity(mob, 'DAM_FIRE')
    assert (immune, resistant) == ('IS_RESISTANT', 'IS_NORMAL')
    return {'Python_immune_plus_vulnerable': immune, 'C_immune_plus_vulnerable': 'IS_IMMUNE',
            'Python_resistant_plus_vulnerable': resistant, 'C_resistant_plus_vulnerable': 'IS_RESISTANT'}


probe('N06 simultaneous immunity/resistance and vulnerability', conflicting_defenses)


def trusted_mortal_ticks(f):
    f.actor.level = 20
    f.actor.trust = int(f.enums.get('gameParameters').LEVEL_IMMORTAL)
    f.actor.status_flags.hunger = f.actor.status_flags.thirst = 10
    f.actor.status_flags.drunk = 12
    lamp = item('lamp', itemType='light', value2='3')
    f.actor.equip_item(lamp, 'light')
    f.actor.tick_conditions()
    f.actor.tick_light_source(f.room)
    actual = (f.actor.status_flags.hunger, f.actor.status_flags.thirst,
              f.actor.status_flags.drunk, int(lamp.value2))
    assert actual == (10, 10, 12, 3)
    return {'level': 20, 'trust': f.actor.trust, 'Python_hunger_thirst_drunk_fuel': actual,
            'C_hunger_thirst_drunk_fuel': (9, 9, 11, 2)}


probe('N07 trusted mortals skip condition and light ticks', trusted_mortal_ticks)
print(json.dumps({'resolved': sorted(RESOLVED), 'open_probes': results}, indent=2))
