"""Read-only production-method probes for the fresh gameplay review.

Run from the repository root with .venv/Scripts/python.exe <this file>.
R01-R15 are now covered by regression tests and skipped here. The historical assertions describe pre-remediation discrepancies, not desired behavior.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import json
import unittest
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch
from tests.test_movement_rules_parity import MovementFixture, item
from api.CharacterApi import CharacterApi
from api.MobileApi import MobileApi
from area.AreaHandler import AreaHandler
from combat.CombatHandler import FightHandler
from game.Equipped import Equipped
from game.AnimateEntity import RegenerationContext
from interp.Context import Context
from interp.commands.Fight import Fight
from item.Effect import Effect

class Fixture(MovementFixture, unittest.TestCase):
    pass

Fixture.setUpClass()
results = []
def probe(name, operation):
    if name[:3] in {'R01', 'R02', 'R03', 'R04', 'R05', 'R06', 'R07', 'R08', 'R09', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15'}:
        return
    fixture = Fixture()
    fixture.setUp()
    try:
        observed = operation(fixture)
        results.append({'finding': name, 'observed': observed})
    finally:
        fixture.doCleanups()

def wear(f, obj):
    f.actor.add_item(obj)
    return Equipped.wear_item(f.actor, obj, f.enums.get('wearFlags'), f.enums.get('itemFlags'),
                              replace=True, effect_handler=f.effects)

def armor(f):
    before = FightHandler._victim_ac_for_damage_type(f.actor, 'DAM_PIERCE')
    obj = item('armor', itemType='armor', wearFlags=int(f.enums.get('wearFlags').ITEM_WEAR_BODY), value0='10')
    assert not wear(f, obj).blocked_key
    after = FightHandler._victim_ac_for_damage_type(f.actor, 'DAM_PIERCE')
    assert before == after
    return {'combat_ac_before': before, 'combat_ac_after': after, 'C_raw_AC_delta': -30}
probe('R01 armor', armor)

def alignment(f):
    f.actor.set_alignment(800)
    obj = item('unholy-ring', wearFlags=int(f.enums.get('wearFlags').ITEM_WEAR_FINGER),
               extraFlags=int(f.enums.get('itemFlags').ITEM_ANTI_GOOD))
    assert not wear(f, obj).blocked_key
    assert f.actor.equipped.finger1 is obj
    return {'good_actor_equips_anti_good': True, 'C': 'zaps and drops item'}
probe('R02 alignment', alignment)

def light(f):
    f.room.light = 0
    obj = item('lamp', itemType='light', value2='10')
    assert not wear(f, obj).blocked_key
    assert f.room.light == 0
    f.attempt('north')
    assert f.room.light == f.destination.light == 0
    return {'source_light': f.room.light, 'destination_light': f.destination.light, 'C_destination_light': 1}
probe('R03 light', light)

def reset_handler(f):
    handler = AreaHandler.__new__(AreaHandler)
    handler.room_registry = f.rooms
    handler.ItemFlags = f.enums.get('itemFlags')
    handler._is_shopkeeper = lambda mob: False
    handler._count_live_items = lambda vnum: 0
    return handler

def give_resets(f):
    h = reset_handler(f)
    obj = item('first', itemType='potion')
    h.item_registry = NS(get=lambda **kw: obj)
    mob = f.npc()
    for vnum in ('first', 'second'):
        obj.id = obj.vnum = vnum
        assert h._do_mob_item_reset(True, NS(command='G', arg1=vnum, arg2=10, arg3=0), mob)
    assert len(mob.inventory) == 0 and mob.equipped.light.vnum == 'second'
    assert len(mob.owned_items()) == 1
    return {'inventory_count': len(mob.inventory), 'owned_count_after_two_G_resets': len(mob.owned_items()),
            'equipped_light_type': mob.equipped.light.item_type, 'C_owned_count': 2}
probe('R04 G resets', give_resets)

def equip_reset(f):
    h = reset_handler(f)
    obj = item('hp-ring', effects=[dict(where='TO_OBJECT', type=-1, duration=-1, location='APPLY_HIT', modifier=25)])
    h.item_registry = NS(get=lambda **kw: obj)
    mob = f.npc()
    mob.max_hit = 100
    before = mob.max_hit
    assert h._do_mob_item_reset(True, NS(command='E', arg1='100', arg2=10, arg3=1), mob)
    assert mob.equipped.finger1 is not None and mob.max_hit == before and not mob.effects
    return {'max_hit_before': before, 'max_hit_after': mob.max_hit, 'C_delta': 25}
probe('R05 E affects', equip_reset)

def trainer(f):
    mob = f.npc()
    mob.status_flags.set_flag('act', f.enums.get('actBits').ACT_TRAIN)
    f.room.add_mobile_to_room(mob)
    f.actor.character_attributes.trains = 5

def prime_cap(f):
    trainer(f)
    f.actor.character_class.attr_prime = 0
    f.actor.character_race.who_name = 'human'
    f.actor.character_race.max_strength = 18
    f.actor.character_attributes.strength = 18
    result = f.attempt('train', 'str')
    assert f.actor.character_attributes.strength == 18
    return {'Python_cap': CharacterApi.get_max_train(f.actor, 0, 18), 'C_human_prime_cap': 21,
            'result': result.get('message_key')}
probe('R06 training prime cap', prime_cap)

def debuffed_train(f):
    trainer(f)
    f.actor.character_race.max_strength = 18
    f.actor.character_class.attr_prime = 1
    f.actor.character_attributes.strength = 18
    f.effects.affect_to_char(f.actor, Effect(type='spell.weaken', where='TO_AFFECTS', duration=5, location='APPLY_STR', modifier=-5))
    f.attempt('train', 'str')
    f.effects.affect_strip(f.actor, 'spell.weaken')
    assert f.actor.character_attributes.strength == 19
    return {'permanent_strength_after_debuff_train_expiry': 19, 'C': 'reject training at permanent cap 18'}
probe('R07 training modified stats', debuffed_train)

def raw_regen(f):
    mob = f.npc()
    mob.character_attributes.dexterity = 30
    # PCs use the same raw stat path; a sleeping level-20 PC gets 20+30 instead of 20+25.
    f.actor.character_attributes.dexterity = 30
    context = RegenerationContext(f.enums.get('positions'), f.enums.get('affectedBy'), NS(number_percent=lambda: 100))
    gain = f.actor._base_move_gain(20, CharacterApi.pos_value('POS_SLEEPING'), context)
    assert gain == 50
    return {'sleeping_move_gain_raw_dex30': gain, 'C_maximum_with_dex_cap25': 45}
probe('R08 current-stat clamp', raw_regen)

def capacity(f):
    before = (f.actor.max_items(), f.actor.max_weight())
    f.actor.character_attributes.dexterity += 4
    f.actor.character_attributes.strength += 4
    f.actor.level += 1
    after = (f.actor.max_items(), f.actor.max_weight())
    assert before == after
    return {'before': before, 'after_stat_and_level_increase': after, 'C_item_capacity_delta': 9}
probe('R09 carry capacity', capacity)

def plague_entry(f):
    f.effects.affect_to_char(f.actor, Effect(type='spell.plague', where='TO_AFFECTS', duration=5, level=20, location='APPLY_STR', modifier=-5, bitvector='AFF_PLAGUE'))
    f.victim.room_id = f.destination.id
    f.destination.add_player_to_room(f.victim)
    with patch('util.EffectUtil.EffectUtil.saves_spell', return_value=False) as saves:
        f.attempt('north')
    assert not f.victim.effects and saves.call_count == 0
    return {'entry_saving_throw_calls': saves.call_count, 'C': 'entry spread save and 1/64 infection roll'}
probe('R10 plague on entry', plague_entry)

def wander(f):
    mob = f.npc()
    f.room.add_mobile_to_room(mob)
    f.destination.owner = 'somebody else'
    f.destination.room_flags = int(f.enums.get('roomFlags').ROOM_IMP_ONLY)
    handler = NS(room_registry=f.rooms, exit_flags=f.enums.get('exitFlags'), room_flags=f.enums.get('roomFlags'), act_bits=f.enums.get('actBits'))
    ctx = NS(actor=mob, room=f.room, handler=handler, set_alias=Mock(), mark_performed=lambda: True)
    assert MobileApi._move_mobile_direction(ctx, 0)
    assert mob.room_id == f.destination.id
    return {'entered_private_implementor_room': True, 'C': 'move_char rejects room visibility/private checks'}
probe('R11 wandering travel', wander)

def flee_followers(f):
    follower = f.follower()
    cmd = Fight.__new__(Fight)
    cmd.room_registry, cmd.interp_api, cmd.fight_handler = f.rooms, f.api, f.fight
    cmd.AffectBits = f.enums.get('affectedBy')
    f.actor.fighting = f.victim
    with patch('interp.commands.Fight.random.randint', return_value=0):
        cmd.do_flee(f.actor, f.ctx('flee'))
    assert f.actor.room_id == f.destination.id and follower.room_id == f.room.id
    return {'leader_room': f.actor.room_id, 'standing_follower_room': follower.room_id,
            'C': 'eligible standing follower follows move_char during flee'}
probe('R12 flee followers', flee_followers)

def backstab(f):
    combat = FightHandler.__new__(FightHandler)
    combat._current_hitroll = lambda actor: 0
    combat._skill_percent = lambda actor, name: 50
    normal = combat._thac0(f.actor, 'TYPE_HIT', 100)
    stabbed = combat._thac0(f.actor, 'backstab', 100)
    assert normal - stabbed == 5
    return {'Python_backstab_thac0_reduction_at_50_percent': normal - stabbed, 'C_reduction': 500}
probe('R13 backstab THAC0', backstab)

def multiclass_mobile(f):
    from mobile.MobileFactory import MobileFactory
    from devtools.collection_query import load_collections
    from api.GameApi import GameApi
    mob = f.npc()
    mob.level = 10
    bits = f.enums.get('actBits')
    mob.status_flags.set_flag('act', int(bits.ACT_WARRIOR) | int(bits.ACT_CLERIC))
    MobileFactory._apply_mob_stat_bonuses(mob, f.enums)
    stats = mob.character_attributes
    assert (stats.strength, stats.wisdom, stats.dexterity) == (16, 13, 13)
    masks = [int(bits[name]) for name in ('ACT_WARRIOR', 'ACT_THIEF', 'ACT_CLERIC', 'ACT_MAGE')]
    docs = load_collections(Path(__file__).resolve().parents[2] / 'resources/collections', ['mobiles'])['mobiles'].documents
    multi = [d['vnum'] for d in docs if sum(bool(GameApi.flags_to_int(d.get('statusFlags', {}).get('act', 0)) & m) for m in masks) > 1]
    return {'Python_str_wis_dex': [stats.strength, stats.wisdom, stats.dexterity],
            'C_str_wis_dex': [17, 16, 12], 'bundled_multi_class_mobiles': len(multi), 'example_vnums': multi[:5]}
probe('R14 mobile class modifiers', multiclass_mobile)

def give_mobile(f):
    from interp.commands.Object import Object
    commands = Object.__new__(Object)
    mob = f.npc()
    gift = item('gift')
    f.actor.add_item(gift)
    commands._inventory_item = lambda *args: gift
    commands._find_give_target = lambda *args: mob
    commands._is_shopkeeper = lambda *args: False
    commands.item_flags = f.enums.get('itemFlags')
    try:
        commands._prepare_give_context(f.actor, f.ctx('give', 'gift npc'))
    except AttributeError as exc:
        assert 'max_items' in str(exc)
        return {'actual': str(exc), 'C': 'checks NPC capacity and transfers a permitted item'}
    raise AssertionError('Expected the missing mobile capacity method')
probe('R15 giving objects to mobiles', give_mobile)

print(json.dumps(results, indent=2))
