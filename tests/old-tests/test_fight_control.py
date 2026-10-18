import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from combat.CombatHandler import FightHandler
from game.UpdateHandler import UpdateHandler
from interp.commands.Fight import Fight


class TestFightControl(unittest.TestCase):
    def test_do_kill_rejects_repeat_attack_on_same_target(self):
        registry_service = Mock()
        registry_service.room_registry = Mock()
        registry_service.skill_registry = Mock()
        registry_service.spell_registry = Mock()
        fight_handler = Mock()
        fight_handler.is_safe.return_value = (False, "")

        commands = Fight(
            registry_service=registry_service,
            room_helper=Mock(),
            fight_handler=fight_handler,
        )

        victim = SimpleNamespace(id="mob1", name="monster", short_description="the monster")
        character = SimpleNamespace(room_id="room1", fighting=victim)
        room = SimpleNamespace(id="room1")
        registry_service.room_registry.get_or_none.return_value = room
        context = SimpleNamespace(result="monster", parameters=[], finish=Mock())

        with patch("interp.commands.Fight.PlayerUtil.get_target", return_value=victim), \
             patch("interp.commands.Fight.CharacterApi.is_npc", return_value=False):
            payload = commands.do_kill(character, context)

        self.assertEqual("You are already fighting the monster.\r\n", payload["to_char"])

    def test_damage_sets_fighting_for_both_combatants(self):
        message_bus = Mock()
        combat_registry = Mock()
        combat_registry.get_by_combatant.return_value = []
        room_registry = Mock()
        room = SimpleNamespace(id="room1", characters={}, mobiles={}, contents={})
        room_registry.get_or_none.return_value = room

        attacker = SimpleNamespace(
            id="char1",
            room_id="room1",
            fighting=None,
            level=10,
            experience=0,
            hit=30,
            character_attributes=SimpleNamespace(position=8, alignment=0, strength=14),
        )
        victim = SimpleNamespace(
            id="mob1",
            room_id="room1",
            fighting=None,
            hit=20,
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

        handler = FightHandler(
            message_bus=message_bus,
            combat_registry=combat_registry,
            room_registry=room_registry,
            item_registry=Mock(),
            mobile_registry=Mock(),
        )

        positions = SimpleNamespace(
            POS_DEAD=SimpleNamespace(value=0),
            POS_STUNNED=SimpleNamespace(value=3),
            POS_FIGHTING=SimpleNamespace(value=7),
        )

        with patch("combat.FightHandler.CharacterApi.get_enum", return_value=positions), \
             patch("combat.FightHandler.CharacterApi.is_npc", side_effect=lambda entity: entity is victim):
            handler.damage(attacker, victim, 2)

        self.assertIs(attacker.fighting, victim)
        self.assertIs(victim.fighting, attacker)
        self.assertEqual(2, combat_registry.upsert.call_count)

    def test_one_hit_allows_mobile_without_room_id_when_room_contains_both(self):
        message_bus = Mock()
        combat_registry = Mock()
        room_registry = Mock()
        item_registry = Mock()
        mobile_registry = Mock()
        room = SimpleNamespace(id="room1", characters={}, mobiles={}, contents={})

        attacker = SimpleNamespace(
            id="char1",
            room_id="room1",
            level=10,
            character_attributes=SimpleNamespace(position=8, strength=14, alignment=0),
        )
        victim = SimpleNamespace(
            id="mob1",
            hit=20,
            max_hit=20,
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
        room_registry.get_or_none.return_value = room
        room_registry.all_rooms.return_value = [room]

        handler = FightHandler(
            message_bus=message_bus,
            combat_registry=combat_registry,
            room_registry=room_registry,
            item_registry=item_registry,
            mobile_registry=mobile_registry,
        )

        positions = SimpleNamespace(POS_DEAD=SimpleNamespace(value=0))

        with patch("combat.FightHandler.CharacterApi.get_enum", return_value=positions), \
             patch("combat.FightHandler.CharacterApi.is_npc", side_effect=lambda entity: entity is victim), \
             patch("combat.FightHandler.random.randint", return_value=5), \
             patch.object(handler, "check_dodge", return_value=False), \
             patch.object(handler, "check_parry", return_value=False), \
             patch.object(handler, "check_shield_block", return_value=False):
            result = handler.one_hit(attacker, victim, dt="TYPE_HIT")

        self.assertIn("monster", result["to_char"].lower())

    def test_build_round_payload_appends_condition_line_for_player(self):
        message_bus = Mock()
        combat_registry = Mock()
        room_registry = Mock()
        item_registry = Mock()
        mobile_registry = Mock()
        room = SimpleNamespace(id="room1", characters={}, mobiles={}, contents={})

        attacker = SimpleNamespace(id="char1", name="Tester")
        victim = SimpleNamespace(id="mob1", name="monster", short_description="the monster", hit=10, max_hit=20)
        room.characters = {"char1": attacker}
        room.mobiles = {"mob1": victim}

        handler = FightHandler(
            message_bus=message_bus,
            combat_registry=combat_registry,
            room_registry=room_registry,
            item_registry=item_registry,
            mobile_registry=mobile_registry,
        )

        with patch("combat.FightHandler.CharacterApi.is_npc", side_effect=lambda entity: entity is victim):
            payload = handler.build_round_payload(
                attacker,
                victim,
                room,
                {"to_char": "You hit the monster.\r\n", "to_room": "", "killed": False},
            )

        self.assertIn("You hit the monster.", payload["to_char"])
        self.assertIn("the monster has quite a few wounds.", payload["to_char"].lower())

    def test_one_hit_uses_wielded_weapon_attack_verb(self):
        message_bus = Mock()
        combat_registry = Mock()
        room_registry = Mock()
        item_registry = Mock()
        mobile_registry = Mock()
        room = SimpleNamespace(id="room1", characters={}, mobiles={}, contents={})

        sword = SimpleNamespace(item_type="weapon", value1="1", value2="6", value3="slash")
        attacker = SimpleNamespace(
            id="char1",
            room_id="room1",
            level=10,
            equipped=SimpleNamespace(wielded=sword),
            character_attributes=SimpleNamespace(position=8, strength=14, alignment=0),
        )
        victim = SimpleNamespace(
            id="mob1",
            hit=20,
            max_hit=20,
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
        room_registry.get_or_none.return_value = room
        room_registry.all_rooms.return_value = [room]

        handler = FightHandler(
            message_bus=message_bus,
            combat_registry=combat_registry,
            room_registry=room_registry,
            item_registry=item_registry,
            mobile_registry=mobile_registry,
        )

        positions = SimpleNamespace(POS_DEAD=SimpleNamespace(value=0))

        with patch("combat.FightHandler.CharacterApi.get_enum", return_value=positions), \
             patch("combat.FightHandler.CharacterApi.is_npc", side_effect=lambda entity: entity is victim), \
             patch.object(handler, "check_dodge", return_value=False), \
             patch.object(handler, "check_parry", return_value=False), \
             patch.object(handler, "check_shield_block", return_value=False), \
             patch("combat.FightHandler.random.randint", return_value=3):
            result = handler.one_hit(attacker, victim, dt="TYPE_UNDEFINED")

        self.assertIn("your slash", result["to_char"].lower())

    def test_attack_damage_uses_wielded_weapon_dice(self):
        handler = FightHandler(
            message_bus=Mock(),
            combat_registry=Mock(),
            room_registry=Mock(),
            item_registry=Mock(),
            mobile_registry=Mock(),
        )
        sword = SimpleNamespace(item_type="weapon", value1="1", value2="6", value3="slash")
        attacker = SimpleNamespace(
            equipped=SimpleNamespace(wielded=sword),
            character_attributes=SimpleNamespace(strength=10),
            level=1,
        )

        with patch("combat.FightHandler.random.randint", return_value=4):
            damage = handler._attack_damage(attacker)

        self.assertEqual(4, damage)

    def test_multi_hit_uses_second_attack_skill(self):
        handler = FightHandler(
            message_bus=Mock(),
            combat_registry=Mock(),
            room_registry=Mock(),
            item_registry=Mock(),
            mobile_registry=Mock(),
        )
        attacker = SimpleNamespace(
            fighting=None,
            skills=[{"name": "second attack", "level": 100}],
            stats_flags=SimpleNamespace(pulse_wait=0, pulse_daze=0),
            character_attributes=SimpleNamespace(position=8),
        )
        victim = SimpleNamespace(id="mob1")
        attacker.fighting = victim

        with patch("combat.FightHandler.CharacterApi.get_enum", return_value=SimpleNamespace(POS_RESTING=SimpleNamespace(value=5))), \
             patch("combat.FightHandler.CharacterApi.is_npc", return_value=False), \
             patch.object(handler, "one_hit", side_effect=[
                 {"to_char": "first\r\n", "to_victim": "", "to_room": "", "killed": False},
                 {"to_char": "second\r\n", "to_victim": "", "to_room": "", "killed": False},
             ]), \
             patch("combat.FightHandler.random.randint", return_value=1):
            payload = handler.multi_hit(attacker, victim, dt="TYPE_UNDEFINED")

        self.assertEqual("first\r\nsecond\r\n", payload["to_char"])

    def test_multi_hit_ignores_second_attack_before_skill_is_visible(self):
        handler = FightHandler(
            message_bus=Mock(),
            combat_registry=Mock(),
            room_registry=Mock(),
            item_registry=Mock(),
            mobile_registry=Mock(),
        )
        attacker = SimpleNamespace(
            fighting=None,
            level=1,
            character_class=SimpleNamespace(name="thief", skill_adept=75),
            skills=[{"name": "second attack", "level": 100}],
            spells=[],
            stats_flags=SimpleNamespace(pulse_wait=0, pulse_daze=0),
            character_attributes=SimpleNamespace(position=8),
        )
        victim = SimpleNamespace(id="mob1")
        attacker.fighting = victim
        registry = SimpleNamespace(
            skill_registry=SimpleNamespace(
                all_skills=Mock(return_value=[
                    SimpleNamespace(name="second attack", level_by_class={"thief": 12}, rating_by_class={"thief": 5}),
                ])
            ),
            spell_registry=SimpleNamespace(all_spells=Mock(return_value=[])),
        )

        with patch("combat.FightHandler.CharacterApi.get_enum", return_value=SimpleNamespace(POS_RESTING=SimpleNamespace(value=5))), \
             patch("combat.FightHandler.CharacterApi.is_npc", return_value=False), \
             patch("util.SkillUtil.CharacterApi.get_registry", return_value=registry), \
             patch.object(handler, "one_hit", return_value={"to_char": "first\r\n", "to_victim": "", "to_room": "", "killed": False}) as one_hit, \
             patch.object(handler, "_entity_has_affect", return_value=False), \
             patch("combat.FightHandler.random.randint", return_value=1):
            payload = handler.multi_hit(attacker, victim, dt="TYPE_UNDEFINED")

        self.assertEqual("first\r\n", payload["to_char"])
        self.assertEqual(1, one_hit.call_count)

    def test_mob_hit_uses_off_fast_extra_attack(self):
        handler = FightHandler(
            message_bus=Mock(),
            combat_registry=Mock(),
            room_registry=Mock(),
            item_registry=Mock(),
            mobile_registry=Mock(),
        )
        attacker = SimpleNamespace(
            fighting=None,
            level=20,
            mobile_flags=SimpleNamespace(off=128, act=0),
            pulse_wait=0,
            pulse_daze=0,
        )
        victim = SimpleNamespace(id="char1")
        attacker.fighting = victim

        with patch("combat.FightHandler.CharacterApi.is_npc", return_value=True), \
             patch.object(handler, "one_hit", side_effect=[
                 {"to_char": "first\r\n", "to_victim": "", "to_room": "", "killed": False},
                 {"to_char": "fast\r\n", "to_victim": "", "to_room": "", "killed": False},
             ]), \
             patch.object(handler, "_entity_has_affect", return_value=False), \
             patch.object(handler, "_mob_has_off", side_effect=lambda entity, name: name == "OFF_FAST"), \
             patch.object(handler, "_skill_percent", return_value=0):
            payload = handler.mob_hit(attacker, victim, dt="TYPE_UNDEFINED")

        self.assertEqual("first\r\nfast\r\n", payload["to_char"])

    def test_violence_update_emits_round_payload(self):
        player_helper = Mock()
        weather_handler = Mock()
        area_handler = Mock()
        mobile_handler = Mock()
        fight_handler = Mock()
        message_bus = Mock()
        message_bus.text_to_message.side_effect = lambda text: text
        message_bus.send_to_character = AsyncMock()
        message_bus.send_to_room = AsyncMock()
        message_bus.send_prompt = AsyncMock()
        registry_service = Mock()
        registry_service.area_registry = Mock()
        registry_service.character_registry = Mock()
        registry_service.room_registry = Mock()
        registry_service.skill_registry = Mock()
        registry_service.spell_registry = Mock()
        registry_service.combat_registry = Mock()
        character_service = Mock()
        session_handler = Mock()

        attacker = SimpleNamespace(id="char1", character_attributes=SimpleNamespace(position=8))
        attacker.room_id = "room1"
        attacker.area_id = "area1"
        victim = SimpleNamespace(id="mob1", position=8)
        watcher = SimpleNamespace(id="char2")
        room = SimpleNamespace(id="room1", area_id="area1", characters={"char1": attacker, "char2": watcher}, mobiles={"mob1": victim})
        area = SimpleNamespace(id="area1")
        event = SimpleNamespace(id="evt1", room_id="room1", attacker_id="char1", defender_id="mob1")

        registry_service.room_registry.get_or_none.return_value = room
        registry_service.area_registry.get_or_none.return_value = area
        registry_service.combat_registry.all_events.return_value = [event]
        fight_handler.multi_hit.return_value = {"to_char": "You hit.\r\n", "to_room": "Tester hits monster.\r\n"}
        fight_handler.build_round_payload.return_value = {
            "to_char": "You hit.\r\n",
            "to_room": "Tester hits monster.\r\n",
            "targets": [watcher],
        }

        handler = UpdateHandler(
            player_helper=player_helper,
            weather_handler=weather_handler,
            area_handler=area_handler,
            mobile_handler=mobile_handler,
            fight_handler=fight_handler,
            message_bus=message_bus,
            registry_service=registry_service,
            character_service=character_service,
            session_handler=session_handler,
        )
        handler.PositionsEnum = SimpleNamespace()

        with patch("game.UpdateHandler.CharacterApi.get_enum", return_value=SimpleNamespace()), \
             patch("game.UpdateHandler.CharacterApi.is_awake", return_value=True), \
             patch("game.UpdateHandler.CharacterApi.is_npc", side_effect=lambda entity: entity is victim):
            asyncio.run(handler._violence_update())

        fight_handler.multi_hit.assert_called_once_with(attacker, victim, dt="TYPE_UNDEFINED")
        message_bus.send_to_character.assert_awaited_once_with("char1", "You hit.\r\n")
        message_bus.send_to_room.assert_awaited_once_with("Tester hits monster.\r\n", [watcher])
        message_bus.send_prompt.assert_awaited_once_with(attacker, area, room)
