import unittest
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import Mock

from tests import test_runtime_factories as runtime
from tests.test_update_handler_active_players import build_character_data
from api.CharacterApi import CharacterApi
from api.GameApi import GameApi
from api.InterpApi import InterpApi
from api.ItemApi import ItemApi
from api.MobileApi import MobileApi
from area.Room import Room
from combat.CombatHandler import FightHandler
from devtools.collection_query import load_collections
from game.EnumProvider import EnumProvider
from game.GameData import GameData
from interp.Command import Command
from interp.Context import Context
from interp.commands.Object import Object
from item.Item import Item
from player.Character import Character
from util.GenericUtil import GenericUtil


class CollectionApiBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        collections = load_collections(Path(__file__).resolve().parents[1] / 'resources/collections',
                                       ['commands', 'gamedata'])
        cls.commands = {doc['name']: doc for doc in collections['commands'].documents}
        cls.game = collections['gamedata'].documents[0]

    def setUp(self):
        GameApi.reset_for_tests()
        self.addCleanup(GameApi.reset_for_tests)
        data = GameData.from_json(deepcopy(self.game))
        self.enums = EnumProvider({name: GenericUtil.build_int_enum(name, values)
                                  for name, values in data.enums.items()})
        GameApi.configure(data, self.enums)
        CharacterApi.lazy_load(None, NS())
        self.actor = Character.from_json(build_character_data())
        self.room = Room(id=self.actor.room_id, light=1)
        self.room.add_player_to_room(self.actor)

    def item(self, identifier, **changes):
        document = runtime.item_fixtures.TestItemPersistence._document(identifier)
        document.update(changes)
        return Item.from_json(document)

    def command(self, name):
        document = deepcopy(self.commands[name])
        for key, default in [('shortcuts', ''), ('usage', ''), ('function', [])]:
            document.setdefault(key, default)
        return Command.from_json(document)

    def test_lambda_environment_and_documents_do_not_expose_removed_utilities(self):
        namespace = InterpApi._lambda_locals()
        self.assertNotIn('ItemUtil', namespace)
        self.assertNotIn('MobileUtil', namespace)
        for document in self.commands.values():
            for guard in document.get('guards', []):
                for source in (guard.get('predicate', ''), guard.get('tokenFactory', '')):
                    self.assertNotIn('ItemUtil.', source)
                    self.assertNotIn('MobileUtil.', source)

    def test_get_and_take_pit_guards_accept_string_and_integer_vnums(self):
        pit = self.enums.get('wellKnownObjectVnums').OBJ_VNUM_PIT.value
        for name in ('get', 'take'):
            guard = next(g for g in self.commands[name]['guards'] if g['messageKey'] == 'isNewbiePit')
            predicate = InterpApi._compile_lambda(guard['predicate'])
            for vnum in (pit, str(pit)):
                with self.subTest(command=name, vnum=vnum):
                    item = self.item('pit', vnum=vnum)
                    view = NS(context=NS(get_all_from_container=True, container=item, character=self.actor))
                    self.assertTrue(predicate(view))
                    self.actor.level = self.enums.get('gameParameters').LEVEL_IMMORTAL.value
                    self.assertFalse(predicate(view))
                    self.actor.level = 1

    def test_pour_error_tokens_use_the_item_model(self):
        for key, attribute in [('missingLiquid', 'pour_source'), ('filled', 'pour_target_container')]:
            guard = next(g for g in self.commands['pour']['guards'] if g['messageKey'] == key)
            item = self.item('flask', shortDescription='a blue flask')
            tokens = InterpApi._compile_lambda(guard['tokenFactory'])(NS(context=NS(**{attribute: item})))
            self.assertEqual({'t': 'a blue flask'}, tokens)

    def test_sacrifice_occupant_lookup_and_guard_preserve_state(self):
        chair = self.item('chair')
        self.room.add_item_to_room(chair)
        occupant = Character.from_json(build_character_data('occupant'))
        occupant.name = 'occupant'
        occupant.on = chair
        self.room.add_player_to_room(occupant)
        self.assertIs(occupant, ItemApi.find_item_occupant(self.room, chair))
        context = Context(character=self.actor, room=self.room, command=self.command('sacrifice'),
                          result='chair', parameters=[])
        commands = Object.__new__(Object)
        commands.interp_api = InterpApi()
        before = self.actor.silver
        payload = commands.do_sacrifice(self.actor, context)
        self.assertTrue(payload['blocked'])
        self.assertIn('occupant', payload['to_char'])
        self.assertIn(chair.id, self.room.contents)
        self.assertEqual(before, self.actor.silver)
        self.assertIs(occupant, context.item_occupant)

    def test_autosacrifice_uses_live_command_payload(self):
        corpse = self.item('corpse', itemType='corpse_npc', level=2)
        self.room.add_item_to_room(corpse)
        command = self.command('sacrifice')
        command.payload.to_char['multiple_silver'] = 'Custom reward: %d.'
        command.payload.to_room['default'] = '%c offers %t.'
        combat = FightHandler.__new__(FightHandler)
        combat.registry_service = NS(interp_registry=NS(get_or_none=Mock(return_value=command)))
        combat.WearFlags = self.enums.get('wearFlags')
        combat.ItemFlags = self.enums.get('itemFlags')
        payload = combat._autosacrifice_corpse(self.actor, corpse, self.room)
        self.assertEqual('Custom reward: 6.\r\n', payload['to_char'])
        self.assertIn('offers corpse.', payload['to_room'])
        self.assertNotIn(corpse.id, self.room.contents)

    def test_scavenged_items_use_entity_inventory_contract(self):
        fixture = runtime.mobile_fixtures.MobileArmorIsolationTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        mobile = runtime.MobileFactory.create(fixture.prototype, fixture.enums)
        item = self.item('gem')
        self.room.add_item_to_room(item)
        MobileApi.give_room_item_to_mobile(self.room, mobile, item)
        self.assertIn(item, mobile.owned_items())
        self.assertNotIn(item.id, self.room.contents)


if __name__ == '__main__':
    unittest.main()
