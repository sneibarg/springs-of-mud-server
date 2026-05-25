import sys
import types
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch

if "registries" not in sys.modules:
    registries = types.ModuleType("registries")

    class Registry:
        def __class_getitem__(cls, _item):
            return cls

    registries.Registry = Registry
    sys.modules["registries"] = registries

if "injector" not in sys.modules:
    injector = types.ModuleType("injector")

    def inject(target):
        return target

    injector.inject = inject
    sys.modules["injector"] = injector

from fight.FightHandler import FightHandler
from game.Equipped import Equipped
from game.UpdateHandler import UpdateHandler
from mobile.MobileHandler import MobileHandler
from util.ItemUtil import ItemUtil
from player.CharacterAdvancement import CharacterAdvancement


class TestCombatInventoryRegressions(TestCase):
    def _build_fight_handler(self, combat_registry=None, room_registry=None):
        return FightHandler(
            message_bus=Mock(),
            combat_registry=combat_registry or Mock(),
            area_registry=Mock(),
            room_registry=room_registry or Mock(),
            room_helper=Mock(),
            item_registry=Mock(),
            mobile_registry=Mock(),
        )

    def test_stop_fighting_clears_reciprocal_target_without_registry_event(self):
        combat_registry = Mock()
        combat_registry.get_by_combatant.return_value = []
        room_registry = Mock()
        handler = self._build_fight_handler(combat_registry=combat_registry, room_registry=room_registry)

        attacker = SimpleNamespace(
            id="char1",
            hit=20,
            fighting=None,
            character_attributes=SimpleNamespace(position=7),
        )
        victim = SimpleNamespace(
            id="mob1",
            hit=20,
            fighting=attacker,
            character_attributes=SimpleNamespace(position=7),
        )
        attacker.fighting = victim

        positions = SimpleNamespace(POS_STANDING=SimpleNamespace(value=8))
        with patch("fight.FightHandler.CharacterApi.get_enum", return_value=positions), \
             patch("fight.FightHandler.CharacterApi.is_npc", return_value=False):
            handler.stop_fighting(victim, both=True)

        self.assertIsNone(attacker.fighting)
        self.assertIsNone(victim.fighting)

    def test_refresh_combat_registry_stops_dangling_fight_targets(self):
        registry_service = Mock()
        registry_service.room_registry = Mock()
        registry_service.area_registry = Mock()
        registry_service.character_registry = Mock()
        registry_service.skill_registry = Mock()
        registry_service.spell_registry = Mock()
        registry_service.combat_registry = Mock()

        attacker = SimpleNamespace(id="char1", fighting=SimpleNamespace(id="missing"))
        room = SimpleNamespace(id="room1", characters={"char1": attacker}, mobiles={})
        registry_service.room_registry.all_rooms.return_value = [room]

        fight_handler = Mock()
        handler = UpdateHandler(
            player_helper=Mock(),
            weather_handler=Mock(),
            area_handler=Mock(),
            mobile_handler=Mock(),
            fight_handler=fight_handler,
            message_bus=Mock(),
            registry_service=registry_service,
            character_service=Mock(),
            session_handler=Mock(),
        )

        handler._refresh_combat_registry_from_world()

        fight_handler.stop_fighting.assert_called_once_with(attacker, both=False)
        registry_service.combat_registry.upsert.assert_not_called()

    def test_damage_awards_current_and_accumulated_experience(self):
        combat_registry = Mock()
        combat_registry.get_by_combatant.return_value = []
        room_registry = Mock()
        room = SimpleNamespace(id="room1", characters={}, mobiles={}, contents={})
        room_registry.get_or_none.return_value = room
        room_registry.all_rooms.return_value = [room]
        handler = self._build_fight_handler(combat_registry=combat_registry, room_registry=room_registry)

        attacker = SimpleNamespace(
            id="char1",
            room_id="room1",
            fighting=None,
            level=10,
            hit=30,
            character_attributes=SimpleNamespace(
                position=8,
                alignment=0,
                strength=14,
                experience=980,
                accumulated_experience=5000,
                experience_per_level=1000,
            ),
        )
        victim = SimpleNamespace(
            id="mob1",
            room_id="room1",
            fighting=None,
            hit=10,
            level=5,
            position=8,
            start_pos=8,
            default_pos=8,
            short_description="the monster",
            name="monster",
            mobile_flags=SimpleNamespace(act=0, form=0, parts=0),
        )
        room.characters = {"char1": attacker}
        room.mobiles = {"mob1": victim}

        positions = SimpleNamespace(
            POS_DEAD=SimpleNamespace(value=0),
            POS_STUNNED=SimpleNamespace(value=3),
            POS_FIGHTING=SimpleNamespace(value=7),
        )

        with patch("fight.FightHandler.CharacterApi.get_enum", return_value=positions), \
             patch("fight.FightHandler.CharacterApi.is_npc", side_effect=lambda entity: entity is victim), \
             patch.object(handler, "xp_compute", return_value=75), \
             patch("fight.FightHandler.CharacterAdvancement.gain_experience", wraps=CharacterAdvancement.gain_experience), \
             patch.object(handler, "raw_kill") as raw_kill:
            result = handler.damage(attacker, victim, 20)

        self.assertTrue(result["killed"])
        self.assertEqual(75, result["xp_gain"])
        self.assertEqual(11, attacker.level)
        self.assertEqual(55, attacker.character_attributes.experience)
        self.assertEqual(5075, attacker.character_attributes.accumulated_experience)
        self.assertIn("You raise a level!!\r\n", result["level_up_messages"])
        raw_kill.assert_called_once_with(victim)

    def test_mobile_handler_rebuilds_kill_table_with_number_counts(self):
        registry_service = Mock()
        registry_service.mobile_registry.all_mobiles.return_value = [
            SimpleNamespace(level=5),
            SimpleNamespace(level=5),
            SimpleNamespace(level=7),
        ]
        handler = MobileHandler(
            message_bus=Mock(),
            registry_service=registry_service,
            area_registry=Mock(),
            room_registry=Mock(),
            shop_registry=Mock(),
            room_helper=Mock(),
            mobile_helper=Mock(),
            fight_handler=Mock(),
            weather_handler=Mock(),
        )

        handler.rebuild_kill_table()

        self.assertEqual(2, handler.kill_table[5].number)
        self.assertEqual(0, handler.kill_table[5].killed)
        self.assertEqual(1, handler.kill_table[7].number)

    def test_raw_kill_updates_mobile_template_and_handler_kill_table(self):
        combat_registry = Mock()
        combat_registry.get_by_combatant.return_value = []
        room_registry = Mock()
        room = SimpleNamespace(id="room1", characters={}, mobiles={}, contents={})
        room_registry.get_or_none.return_value = room
        room_registry.all_rooms.return_value = [room]
        handler = self._build_fight_handler(combat_registry=combat_registry, room_registry=room_registry)
        handler.mobile_handler = SimpleNamespace(record_mobile_kill=Mock())

        proto = SimpleNamespace(vnum="1000", count=3, killed=4)
        handler.mobile_registry.get_or_none.return_value = proto

        victim = SimpleNamespace(
            id="mob1",
            vnum="1000",
            room_id="room1",
            level=5,
            short_description="the monster",
            name="monster",
            mobile_flags=SimpleNamespace(act=0, form=0, parts=0),
            inventory=[],
            equipped=None,
            fighting=None,
        )
        room.mobiles = {"mob1": victim}

        with patch("fight.FightHandler.CharacterApi.is_npc", return_value=True), \
             patch.object(handler, "death_cry"), \
             patch.object(handler, "make_corpse"), \
             patch("fight.FightHandler.CharacterApi.get_enum", return_value=SimpleNamespace()):
            handler.raw_kill(victim)

        self.assertEqual(3, proto.count)
        self.assertEqual(5, proto.killed)
        handler.mobile_handler.record_mobile_kill.assert_called_once_with(victim)
