import asyncio
import unittest
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock

from tests.test_movement_rules_parity import MovementFixture, item
from api.CharacterApi import CharacterApi
from interp.PromptFormat import PromptFormat, prompt_exits, prompt_room_name
from item.Effect import Effect
from item.EffectUpdateHandler import EffectUpdateHandler
from game.Equipped import Equipped
from server.session.SessionState import SessionStatus


class EffectWeaponPromptTests(MovementFixture, unittest.TestCase):
    def weapon(self, weight=200, actor=None):
        actor = actor or self.actor
        actor.character_attributes.strength = 20
        weapon = item('heavy sword', itemType='weapon', weight=weight)
        actor.equip_item(weapon, 'wielded')
        return weapon

    def strength_effect(self, modifier, source=''):
        return Effect(where='TO_AFFECTS', type='test.strength', location='APPLY_STR',
                      modifier=modifier, duration=5, bitvector=0, source=source)

    def test_penalty_drops_weapon_with_contents_and_removes_weapon_affects(self):
        weapon = self.weapon(190)
        weapon.contains = [item('weight', weight=10)]
        weapon.effects = [Effect(where='TO_AFFECTS', type='weapon.hit', location='APPLY_HITROLL',
                                 modifier=3, duration=-1, bitvector=0)]
        before = self.actor.hit_roll
        self.effects.apply_item_effects(self.actor, weapon)
        self.assertEqual(before + 3, self.actor.hit_roll)
        notify = Mock()
        self.effects.weapon_drop_notifier = notify
        self.effects.affect_to_char(self.actor, self.strength_effect(-10))
        self.assertIsNone(self.actor.equipped.wielded)
        self.assertNotIn(weapon, self.actor.loot)
        self.assertIs(self.room.contents[weapon.id], weapon)
        self.assertEqual(-1, weapon.wear_loc)
        self.assertEqual(before, self.actor.hit_roll)
        self.assertEqual(1, len(self.actor.effects))
        notify.assert_called_once_with(self.actor, weapon, self.room)

    def test_expiring_strength_buff_drops_weapon(self):
        self.actor.character_attributes.strength = 10
        buff = self.effects.affect_to_char(self.actor, self.strength_effect(10))
        weapon = item('sword', itemType='weapon', weight=200)
        self.actor.equip_item(weapon, 'wielded')
        buff.duration = 0
        self.effects.tick_effects(self.actor)
        self.assertEqual(10, CharacterApi.current_stat(self.actor, 'strength'))
        self.assertIsNone(self.actor.equipped.wielded)
        self.assertIs(self.room.contents[weapon.id], weapon)

    def test_removing_weapon_strength_effect_does_not_recurse_or_reverse_twice(self):
        weapon = self.weapon()
        weapon.effects = [self.strength_effect(2)]
        self.effects.apply_item_effects(self.actor, weapon)
        self.effects.affect_to_char(self.actor, self.strength_effect(-12))
        self.assertIsNone(self.actor.equipped.wielded)
        self.assertEqual(8, self.actor.character_attributes.strength)
        self.assertEqual(1, len(self.actor.effects))

    def test_exact_weight_boundary_and_npc_exemption(self):
        self.actor.character_attributes.strength = 10
        allowance = CharacterApi.get_attribute_bonus('strength', '10')['wield'] * 10
        weapon = self.weapon(allowance)
        self.effects.affect_to_char(self.actor, self.strength_effect(-10))
        self.assertIs(self.actor.equipped.wielded, weapon)
        npc = self.npc()
        self.room.add_mobile_to_room(npc)
        npc_weapon = self.weapon(10000, npc)
        self.effects.affect_to_char(npc, self.strength_effect(-10))
        self.assertIs(npc.equipped.wielded, npc_weapon)

    def test_removing_strength_weapon_keeps_it_in_inventory(self):
        weapon = self.weapon()
        self.actor.character_attributes.strength = 10
        weapon.effects = [self.strength_effect(10)]
        self.effects.apply_item_effects(self.actor, weapon)
        Equipped._remove_item(self.actor, 'wielded', weapon, effect_handler=self.effects)
        self.assertIsNone(self.actor.equipped.wielded)
        self.assertIn(weapon, self.actor.loot)
        self.assertNotIn(weapon, self.room.contents.values())
        self.assertEqual(10, self.actor.character_attributes.strength)

    def test_worn_object_refresh_checks_final_contributions(self):
        weapon = self.weapon()
        self.actor.character_attributes.strength = 10
        weapon.effects = [self.strength_effect(10)]
        self.effects.apply_item_effects(self.actor, weapon)
        self.effects.affect_to_obj(weapon, Effect(where='TO_WEAPON', type='test.flag',
                                  location='APPLY_NONE', modifier=0, bitvector=0, duration=5))
        self.assertIs(self.actor.equipped.wielded, weapon)
        self.assertEqual(20, self.actor.character_attributes.strength)

    def test_prompt_room_name_obeys_darkness_blindness_and_holylight(self):
        self.room.room_flags = int(self.enums.get('roomFlags').ROOM_DARK)
        self.room.light = 0
        self.actor.prompt_format = PromptFormat(room_name=True, exits=True)
        self.exit.exit_flags |= self.exit_flags.EX_CLOSED
        output = self.actor.prompt_format.render_prompt(SessionStatus.PLAYING, self.actor,
                                                        self.room, NS()).data['text']
        self.assertIn('darkness', output)
        self.assertNotIn(self.room.name, output)
        self.assertNotIn('North', output)
        self.room.room_flags = 0
        self.flag(self.actor, 'AFF_BLIND')
        self.assertEqual('darkness', prompt_room_name(self.actor, self.room))
        self.actor.status_flags.set_flag('act', self.enums.get('playerActBits').PLR_HOLYLIGHT)
        self.assertEqual(self.room.name, prompt_room_name(self.actor, self.room))

    def test_prompt_exits_filter_closed_missing_and_restricted_destinations(self):
        self.assertEqual('North', prompt_exits(self.actor, self.room))
        self.exit.exit_flags |= self.exit_flags.EX_CLOSED
        self.assertEqual('none', prompt_exits(self.actor, self.room))
        self.exit.exit_flags &= ~self.exit_flags.EX_CLOSED
        self.destination.room_flags = int(self.enums.get('roomFlags').ROOM_IMP_ONLY)
        self.assertEqual('none', prompt_exits(self.actor, self.room))
        self.flag(self.actor, 'AFF_INFRARED')
        self.assertEqual('North', prompt_exits(self.actor, self.room))
        self.flag(self.actor, 'AFF_BLIND')
        self.assertEqual('none', prompt_exits(self.actor, self.room))
        self.flag(self.actor, 'AFF_BLIND', False)
        self.world.remove(self.destination)
        self.assertEqual('none', prompt_exits(self.actor, self.room))


class WeaponDropDeliveryTests(MovementFixture, unittest.IsolatedAsyncioTestCase):
    async def test_drop_emits_authored_payload_once_to_actor_and_observer(self):
        observer = self.follower('watcher')
        bus = NS(send_to_character=AsyncMock(), text_to_message=lambda text: text)
        updates = EffectUpdateHandler(self.registries, self.enums, self.effects, Mock(), bus)
        self.effects.weapon_drop_notifier = updates.weapon_dropped
        self.actor.character_attributes.strength = 20
        weapon = item('sword', itemType='weapon', weight=200)
        self.actor.equip_item(weapon, 'wielded')
        self.effects.affect_to_char(self.actor, Effect(where='TO_AFFECTS', type='spell.weaken',
                                  location='APPLY_STR', modifier=-10, duration=5, bitvector=0))
        await asyncio.sleep(0)
        messages = {call.args[0]: call.args[1] for call in bus.send_to_character.call_args_list}
        self.assertEqual(2, bus.send_to_character.await_count)
        self.assertIn('You drop', messages[self.actor.id])
        self.assertIn('drops', messages[observer.id])
        self.assertIn('sword', messages[self.actor.id])
