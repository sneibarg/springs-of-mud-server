import unittest

from tests.test_movement_rules_parity import MovementFixture, item
from api.CharacterApi import CharacterApi


class WakeFurnitureTests(MovementFixture, unittest.TestCase):
    def sleeping_player(self, name):
        target = self.follower(name)
        CharacterApi.set_position(target, 'POS_SLEEPING')
        return target

    def test_wake_rejects_invisible_targets_without_mutation(self):
        target = self.sleeping_player('Secret')
        target.status_flags.invis_level = 60
        self.assertEqual('target_missing', self.attempt('wake', 'Secret')['message_key'])
        self.assertEqual(CharacterApi.pos_value('POS_SLEEPING'), CharacterApi.position_value(target))
        target.status_flags.invis_level = 0
        self.flag(target, 'AFF_INVISIBLE')
        self.assertEqual('target_missing', self.attempt('wake', 'Secret')['message_key'])
        self.flag(self.actor, 'AFF_DETECT_INVIS')
        self.assertEqual('wake_target', self.attempt('wake', 'Secret')['message_key'])

    def test_wake_resolves_npc_keywords_and_uses_short_description(self):
        npc = self.npc()
        npc.name = 'guard city sentinel'
        npc.short_description = 'a city guard'
        CharacterApi.set_position(npc, 'POS_SLEEPING')
        self.room.add_mobile_to_room(npc)
        output = self.attempt('wake', 'sentinel')
        self.assertIs(npc, output['victim'])
        self.assertEqual('a city guard', output['tokens']['t'])
        self.assertEqual(CharacterApi.pos_value('POS_STANDING'), CharacterApi.position_value(npc))

    def test_wake_numbered_targets_skips_unseen_matches(self):
        hidden = self.sleeping_player('guard hidden')
        hidden.status_flags.invis_level = 60
        first = self.sleeping_player('guard first')
        second = self.sleeping_player('guard second')
        output = self.attempt('wake', '2.guard')
        self.assertIs(second, output['victim'])
        self.assertEqual(CharacterApi.pos_value('POS_SLEEPING'), CharacterApi.position_value(first))
        self.assertEqual(CharacterApi.pos_value('POS_SLEEPING'), CharacterApi.position_value(hidden))

    def test_wake_retains_self_prefix_sleep_and_already_awake_paths(self):
        self.assertEqual('target_awake', self.attempt('wake', 'self')['message_key'])
        self.assertEqual({'self_stand': True}, self.attempt('wake'))
        target = self.sleeping_player('Sleeper')
        self.flag(target, 'AFF_SLEEP')
        self.assertEqual('affect_sleep', self.attempt('wake', 'sleep')['message_key'])
        self.assertEqual(CharacterApi.pos_value('POS_SLEEPING'), CharacterApi.position_value(target))
        self.flag(target, 'AFF_SLEEP', False)
        self.assertIs(target, self.attempt('wake', 'sleep')['victim'])
        CharacterApi.set_position(self.actor, 'POS_SLEEPING')
        self.assertEqual('is_asleep', self.attempt('wake', 'Sleeper')['message_key'])

    def test_furniture_relations_for_each_posture_and_entity_kind(self):
        target = self.follower('Occupant')
        npc = self.npc()
        npc.start_pos = -1
        self.room.add_mobile_to_room(npc)
        furniture = item('bed', itemType='furniture')
        self.room.add_item_to_room(furniture)
        flags = self.enums.get('furnitureFlags')
        for occupant in (target, npc):
            occupant.on = furniture
            for action, verb in (('SLEEP', 'sleeping'), ('REST', 'resting'),
                                 ('SIT', 'sitting'), ('STAND', 'standing')):
                position = {'SLEEP': 'POS_SLEEPING', 'REST': 'POS_RESTING',
                            'SIT': 'POS_SITTING', 'STAND': 'POS_STANDING'}[action]
                CharacterApi.set_position(occupant, position)
                for relation in ('AT', 'ON', 'IN'):
                    with self.subTest(occupant=occupant.name, action=action, relation=relation):
                        furniture.value2 = int(getattr(flags, action + '_' + relation))
                        output = (self.room.get_players_in_room(self.actor) if occupant is target
                                  else self.room.get_mobiles_in_room(self.actor))
                        self.assertIn(f'is {verb} {relation.lower()} {furniture.short()}.', output)

    def test_furniture_relation_precedence_and_no_furniture_fallback(self):
        target = self.sleeping_player('Sleeper')
        flags = self.enums.get('furnitureFlags')
        target.on = item('bed', itemType='furniture', value2=int(flags.SLEEP_AT | flags.SLEEP_ON))
        self.assertIn('sleeping at', self.room.get_players_in_room(self.actor))
        target.on = None
        self.assertIn('sleeping here.', self.room.get_players_in_room(self.actor))

    def test_npc_start_position_long_description_still_takes_precedence(self):
        npc = self.npc()
        npc.start_pos = CharacterApi.pos_value('POS_SLEEPING')
        CharacterApi.set_position(npc, 'POS_SLEEPING')
        npc.long_description = 'A guard snores peacefully.'
        npc.on = item('bed', itemType='furniture')
        self.room.add_mobile_to_room(npc)
        output = self.room.get_mobiles_in_room(self.actor)
        self.assertIn(npc.long_description, output)
        self.assertNotIn('sleeping in', output)
