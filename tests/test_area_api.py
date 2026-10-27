import unittest
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock, patch

from tests import test_runtime_factories as runtime
from tests.test_update_handler_active_players import build_character_data
from api.AreaApi import AreaApi
from api.InterpApi import InterpApi
from api.MovementApi import MovementApi
from api.WizApi import WizApi
from area.Exit import Exit
from area.AreaHandler import AreaHandler
from area.Room import Room
from area.RoomHandler import RoomHandler
from interp.Context import Context
from interp.commands.Wiz import Wiz
from player.Character import Character
from util.WizUtil import WizUtil


def exit_to(direction, destination='destination'):
    return Exit(direction, '', 'gate', 0, 0, 0, destination, 'origin')


class AreaApiTests(unittest.TestCase):
    def setUp(self):
        self.origin = Room(id='origin', area_id='area', vnum='10', name='Market Square')
        self.destination = Room(id='destination', area_id='other', vnum='20', name='Castle Hall')
        self.rooms = [self.origin, self.destination]
        self.registry = NS(all_rooms=lambda: self.rooms, get_or_none=self.room_lookup)
        self.actor = Character.from_json(build_character_data())
        self.actor.room_id = self.origin.id
        self.origin.add_player_to_room(self.actor)
        self.characters = NS(all_characters=lambda: [self.actor])

    def room_lookup(self, **query):
        return next((room for room in self.rooms if room is not None
                     and all(str(getattr(room, key)) == str(value) for key, value in query.items())), None)

    def find(self, value, characters=True):
        return AreaApi.find_location(value, self.registry, self.characters if characters else None,
                                     WizUtil.name_matches)

    def test_numeric_room_lookup_precedes_matching_character(self):
        self.actor.name = '20'
        self.assertIs(self.destination, self.find(' 20 '))

    def test_character_lookup_precedes_mobile_and_room_name_matches(self):
        self.actor.name = 'Scout'
        self.destination.name = 'Scout Hall'
        self.destination.mobiles['scout'] = NS(name='scout', short_description='a scout')
        self.assertIs(self.origin, self.find('scout'))

    def test_room_mobile_keywords_and_descriptions_work_without_character_registry(self):
        self.destination.mobiles['guard'] = NS(name='guard sentry', short_description='a silver sentinel')
        self.rooms.insert(0, None)
        for query in ('sentry', 'silver'):
            self.assertIs(self.destination, self.find(query, characters=False))

    def test_room_name_fallback_and_missing_locations(self):
        self.assertIs(self.destination, self.find('castle'))
        self.assertIsNone(self.find('unmapped'))
        self.assertIsNone(self.find(''))
        self.assertIsNone(AreaApi.find_location('10', None, None, WizUtil.name_matches))

    def test_wizard_context_adapters_share_area_lookup(self):
        handler = NS(room_registry=self.registry, character_registry=self.characters)
        context = NS(result='20', parameters=[], player_handler=lambda: handler)
        view = NS(context=context)
        self.assertIs(self.destination, WizApi.location(view))
        self.assertIs(self.destination, WizApi.violate_location(view))
        context.result = '20 look'
        self.assertIs(self.destination, WizApi.at_location(view))
        namespace = InterpApi._lambda_locals()
        self.assertIs(AreaApi, namespace['AreaApi'])

    def test_goto_uses_area_lookup_and_updates_room_membership(self):
        commands = Wiz.__new__(Wiz)
        commands.room_registry, commands.character_registry = self.registry, self.characters
        commands.interp_api = NS(evaluate_guards_only=lambda *_: None)
        commands._visible_room_targets = lambda *_: []
        commands._poof_text = lambda actor, field, fallback: fallback
        context = Context(character=self.actor, room=self.origin, result='20', parameters=[], command=NS(name='goto'))
        payload = commands.do_goto(self.actor, context)
        self.assertEqual(self.destination.id, self.actor.room_id)
        self.assertEqual(self.destination.area_id, self.actor.area_id)
        self.assertNotIn(self.actor.id, self.origin.characters)
        self.assertIs(self.actor, self.destination.characters[self.actor.id])
        self.assertIs(self.destination, payload['to_room_obj'])


class AreaModelTests(unittest.TestCase):
    def test_reverse_door_updates_use_the_destination_room_exit(self):
        outgoing = exit_to(0, 'destination')
        incoming = exit_to(2, 'origin')
        incoming.exit_flags = 10
        origin = Room(id='origin', exits=[outgoing])
        destination = Room(id='destination', exits=[incoming])
        registry = NS(get_or_none=lambda **query: destination if query.get('id') == destination.id else None)
        MovementApi._mirror_exit_flags(registry, origin, outgoing, set_mask=4, clear_mask=2)
        self.assertEqual(12, incoming.exit_flags)
        incoming.to_room_id = 'another-room'
        MovementApi._mirror_exit_flags(registry, origin, outgoing, clear_mask=4)
        self.assertEqual(12, incoming.exit_flags)
        destination.exits.clear()
        MovementApi._mirror_exit_flags(registry, origin, outgoing, set_mask=2)
        self.assertIsNone(destination.get_exit(2))

    def test_exit_formatting_and_direction_aliases_share_names(self):
        for direction, name in enumerate(Exit.DIRECTION_NAMES):
            exit_obj = exit_to(direction)
            self.assertEqual(direction, Room.direction_index(name))
            self.assertEqual(direction, Room.direction_index(name[0]))
            self.assertEqual(f'{name.capitalize():6}- Castle (20)',
                             exit_obj.format_destination('Castle', '20', width=6))
            self.assertEqual(f'{name.capitalize():6}- Castle',
                             exit_obj.format_destination('Castle', width=6))
        room = Room(exits=[exit_to(0), exit_to(4)])
        self.assertEqual('North, Up', room.get_formatted_exits())
        self.assertEqual('none', Room().get_formatted_exits())
        self.assertEqual('none', Room(exits=None).get_formatted_exits())

    def test_door_reset_preserves_unrelated_flags_and_handles_aliases(self):
        for prefix in ('', 'EX_'):
            flags = NS(**{prefix + 'CLOSED': NS(value=2), prefix + 'LOCKED': NS(value=4)})
            for state, expected in ((0, 8), (1, 10), (2, 14)):
                exit_obj = exit_to(0)
                exit_obj.exit_flags = 14
                exit_obj.apply_door_reset(state, flags)
                self.assertEqual(expected, exit_obj.exit_flags)

    def test_sparse_exit_randomization_preserves_objects_destinations_and_outside_slots(self):
        north, south, up = exit_to(0, 'north'), exit_to(2, 'south'), exit_to(4, 'up')
        room = Room(exits=[north, south, up])
        rng = NS(number_range=Mock(side_effect=lambda low, high: high))
        room.randomize_exits(3, rng)
        self.assertIs(south, room.get_exit(0))
        self.assertIs(north, room.get_exit(1))
        self.assertIs(up, room.get_exit(4))
        self.assertEqual('north', north.to_room_id)
        self.assertEqual('south', south.to_room_id)
        self.assertEqual('north', room.destination_id_for_direction('east'))
        self.assertIsNone(room.destination_id_for_direction('invalid'))

    def test_area_resets_mutate_the_live_room_and_exit_models(self):
        north, south = exit_to(0, 'north'), exit_to(2, 'south')
        room = Room(id='origin', vnum='10', exits=[north, south])
        handler = AreaHandler.__new__(AreaHandler)
        handler.room_registry = NS(get_or_none=Mock(return_value=room))
        handler.ExitFlags = NS(EX_CLOSED=NS(value=2), EX_LOCKED=NS(value=4))
        self.assertTrue(handler._do_door_reset(False, NS(arg1='10', arg2='0', arg3='2')))
        self.assertEqual(6, north.exit_flags)
        with patch('area.AreaHandler.rng.number_range', side_effect=lambda low, high: high):
            handler._do_randomize_reset(NS(arg1='10', arg2='3'))
        self.assertIs(south, room.get_exit(0))
        self.assertIs(north, room.get_exit(1))
        self.assertEqual(6, north.exit_flags)


class RoomDirectionTests(unittest.TestCase):
    def test_looking_toward_missing_exit_finishes_without_exception(self):
        handler = RoomHandler.__new__(RoomHandler)
        handler.message_bus = NS(send_to_character=AsyncMock())
        context = NS(room=Room(), parameters=['north'], finish=Mock())
        operation = handler.look_direction(NS(id='actor'), context)
        self.addCleanup(operation.close)
        with self.assertRaises(StopIteration):
            operation.send(None)
        context.finish.assert_called_once_with()
        handler.message_bus.send_to_character.assert_not_called()


if __name__ == '__main__':
    unittest.main()
