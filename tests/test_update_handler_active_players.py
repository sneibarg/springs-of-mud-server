import asyncio
import os
import sys
import unittest
from enum import IntEnum
from types import ModuleType
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, SRC_PATH)


def _stub_package(package_name: str) -> None:
    if package_name in sys.modules:
        return
    package = ModuleType(package_name)
    package.__path__ = [os.path.join(SRC_PATH, package_name)]
    sys.modules[package_name] = package


for package_name in ["area", "combat", "game", "interp", "item", "mobile", "player", "server", "skill", "util"]:
    _stub_package(package_name)

from game.UpdateHandler import UpdateHandler
from game.GamePayload import GamePayload
from item.Effect import Effect
from player.Character import Character


def build_character_data(character_id: str = "char_001") -> dict:
    return {
        "id": character_id,
        "accountId": "acct_001",
        "title": "the Tester",
        "description": "A test character.",
        "cloaked": False,
        "guild": "",
        "characterRace": {
            "whoName": "Human",
            "points": 0,
            "classMult": 100,
            "skills": [""],
            "strength": 13,
            "maxStrength": 18,
            "intelligence": 13,
            "maxIntelligence": 18,
            "wisdom": 13,
            "maxWisdom": 18,
            "dexterity": 13,
            "maxDexterity": 18,
            "constitution": 13,
            "maxConstitution": 18,
            "size": "SIZE_MEDIUM",
        },
        "name": "Tester",
        "areaId": "area_001",
        "roomId": "room_001",
        "role": "player",
        "sex": "male",
        "level": 5,
        "hit": 25,
        "maxHit": 30,
        "mana": 15,
        "maxMana": 20,
        "movement": 18,
        "maxMovement": 20,
        "gold": 10,
        "silver": 5,
        "trust": 0,
        "inventory": [],
        "effects": [],
        "skills": [],
        "spells": [],
        "statusFlags": {
            "act": 0,
            "comm": 0,
            "affectedBy": 0,
            "off": 0,
            "imm": 0,
            "res": 0,
            "vuln": 0,
            "form": 0,
            "parts": 0,
            "hunger": 48,
            "thirst": 48,
            "drunk": 0,
            "invisLevel": 0,
            "incogLevel": 0,
            "played": 0,
            "logon": 0,
            "pulseWait": 0,
            "pulseDaze": 0,
        },
        "characterAttributes": {
            "strength": 13,
            "intelligence": 12,
            "wisdom": 11,
            "dexterity": 10,
            "constitution": 9,
            "alignment": 0,
            "maxWeight": 100,
            "maxItems": 10,
            "position": 8,
            "wimpy": 0,
            "trains": 0,
            "practices": 0,
            "points": 0,
            "experience": 100,
            "accumulatedExperience": 100,
            "experiencePerLevel": 1000,
        },
        "armorClass": {
            "piercing": 100,
            "bashing": 100,
            "slashing": 100,
            "magic": 100,
        },
        "characterClass": {
            "name": "Mage",
            "attrPrime": 0,
            "weapon": 0,
            "guild": 0,
            "skillAdept": 75,
            "thac000": 20,
            "thac032": -4,
            "hpMin": 8,
            "hpMax": 12,
            "manaGain": True,
            "baseGroup": "mage basics",
            "defaultGroup": "mage default",
        },
        "promptFormat": {
            "hp": True,
            "max_hp": True,
            "mana": True,
            "max_mana": False,
            "movement": True,
            "max_movement": False,
            "xp": False,
            "max_xp": False,
            "gold": False,
            "silver": False,
            "alignment": False,
            "room_name": False,
            "exits": False,
            "room_vnum": False,
            "area_name": False,
            "carriage_return": False,
        },
        "equipped": {},
    }


class Positions(IntEnum):
    POS_DEAD = 0
    POS_MORTAL = 1
    POS_INCAP = 2
    POS_STUNNED = 3
    POS_SLEEPING = 4
    POS_RESTING = 5
    POS_SITTING = 6
    POS_FIGHTING = 7
    POS_STANDING = 8


class AffectedBy(IntEnum):
    AFF_POISON = 4096
    AFF_PLAGUE = 8388608
    AFF_HASTE = 2097152
    AFF_SLOW = 536870912
    AFF_REGENERATION = 268435456


class TestUpdateHandlerActivePlayers(unittest.TestCase):
    def _handler(self, playing_characters):
        registry_service = Mock()
        registry_service.character_registry.all_characters.return_value = []
        registry_service.room_registry.all_rooms.return_value = []
        registry_service.skill_registry = Mock()
        registry_service.spell_registry = Mock()
        registry_service.combat_registry = Mock()

        message_bus = Mock()
        message_bus.text_to_message.side_effect = lambda text: text
        message_bus.send_to_character = AsyncMock()
        message_bus.send_to_room = AsyncMock()

        session_handler = Mock()
        session_handler.get_playing_sessions.return_value = [
            SimpleNamespace(character=character) for character in playing_characters
        ]
        effect_handler = Mock()
        effect_handler.tick_effects.return_value = SimpleNamespace(expired_effects=[])

        handler = UpdateHandler(
            weather_handler=Mock(),
            area_handler=Mock(),
            mobile_handler=Mock(),
            fight_handler=Mock(),
            message_bus=message_bus,
            registry_service=registry_service,
            character_service=Mock(),
            session_handler=session_handler,
            enum_provider=Mock(get=Mock(return_value=None)),
            effect_handler=effect_handler,
        )
        handler.PositionsEnum = Positions
        handler.AffectedBits = AffectedBy
        registry_service.room_registry.get_or_none.return_value = SimpleNamespace(heal_rate=100, mana_rate=100)
        return handler, registry_service, message_bus

    @staticmethod
    def _spell_payload(name: str, handler_id: str, payload: dict):
        game_payload = GamePayload.from_json(payload)
        return SimpleNamespace(
            id=handler_id,
            name=name,
            handler_id=handler_id,
            message=lambda channel, key, fallback="", **tokens: game_payload.render(channel, key, fallback=fallback,
                                                                                   **tokens),
        )

    def test_char_update_does_not_tick_offline_registry_characters(self):
        async def run_test():
            offline = Character.from_json(build_character_data("offline_char"))
            offline.status_flags.thirst = 1
            offline.status_flags.hunger = 1

            handler, registry_service, message_bus = self._handler([])
            registry_service.character_registry.all_characters.return_value = [offline]

            with patch("game.UpdateHandler.CharacterApi.is_immortal", return_value=False):
                await handler.char_update()

            self.assertEqual(1, offline.status_flags.thirst)
            self.assertEqual(1, offline.status_flags.hunger)
            message_bus.send_to_character.assert_not_awaited()

        asyncio.run(run_test())

    def test_rom_player_regen_uses_stats_skills_conditions_class_and_room_rates(self):
        character = Character.from_json(build_character_data("active_char"))
        character.level = 20
        character.hit = 50
        character.max_hit = 100
        character.mana = 40
        character.max_mana = 100
        character.movement = 30
        character.max_movement = 100
        character.character_attributes.constitution = 16
        character.character_attributes.wisdom = 12
        character.character_attributes.intelligence = 14
        character.character_attributes.dexterity = 10
        character.character_attributes.position = Positions.POS_RESTING.value
        character.character_class.hp_max = 12
        character.character_class.mana_gain = False
        character.status_flags.hunger = 0
        character.status_flags.thirst = 20
        character.skills = [
            {"name": "fast healing", "level": 50},
            {"name": "meditation", "level": 50},
        ]
        room = SimpleNamespace(heal_rate=150, mana_rate=200)
        handler, _, _ = self._handler([character])
        handler.rng.number_percent = Mock(side_effect=[25, 25])

        with patch("game.UpdateHandler.Ability.check_improve_by_name") as improve:
            self.assertEqual(10, handler.hit_gain(character, room))
            self.assertEqual(6, handler.mana_gain(character, room))
            self.assertEqual(18, handler.move_gain(character, room))

        self.assertEqual(
            [
                (character, "fast healing", True, 8),
                (character, "meditation", True, 8),
            ],
            [call.args for call in improve.call_args_list],
        )

    def test_rom_npc_regen_uses_level_position_and_affects(self):
        npc = SimpleNamespace(
            level=10,
            hit=50,
            max_hit=100,
            mana=50,
            max_mana=100,
            movement=50,
            max_movement=100,
            position=Positions.POS_FIGHTING.value,
            status_flags=SimpleNamespace(
                affected_by=AffectedBy.AFF_REGENERATION.value | AffectedBy.AFF_SLOW.value
            ),
        )
        room = SimpleNamespace(heal_rate=100, mana_rate=100)
        handler, _, _ = self._handler([])

        with patch("game.UpdateHandler.CharacterApi.is_npc", return_value=True):
            self.assertEqual(5, handler.hit_gain(npc, room))
            self.assertEqual(2, handler.mana_gain(npc, room))
            self.assertEqual(5, handler.move_gain(npc, room))

    def test_char_update_regenerates_before_condition_decay(self):
        async def run_test():
            active = Character.from_json(build_character_data("active_char"))
            active.hit = 25
            active.max_hit = 30
            active.status_flags.thirst = 1
            active.status_flags.hunger = 1
            handler, _, message_bus = self._handler([active])
            handler.rng.number_percent = Mock(return_value=100)

            with patch("game.UpdateHandler.CharacterApi.is_immortal", return_value=False):
                await handler.char_update()

            self.assertEqual(27, active.hit)
            self.assertEqual(0, active.status_flags.thirst)
            self.assertEqual(0, active.status_flags.hunger)
            self.assertIn(
                ("active_char", "You are thirsty.\r\n"),
                [call.args for call in message_bus.send_to_character.await_args_list],
            )

        asyncio.run(run_test())

    def test_rom_light_source_burns_out_and_is_removed(self):
        async def run_test():
            active = Character.from_json(build_character_data("active_char"))
            viewer = Character.from_json(build_character_data("viewer_char"))
            lamp = SimpleNamespace(
                item_type="ITEM_LIGHT",
                value2="1",
                name="lamp",
                short_description="a brass lamp",
                display_name=lambda: "a brass lamp",
            )
            active.equipped.light = lamp
            room = SimpleNamespace(
                light=1,
                characters={"active_char": active, "viewer_char": viewer},
                players_in_room=lambda: [active, viewer],
            )
            handler, _, message_bus = self._handler([active, viewer])

            with patch("game.UpdateHandler.CharacterApi.is_immortal", return_value=False):
                await handler._tick_light_source(active, room)

            self.assertEqual("0", lamp.value2)
            self.assertEqual(0, room.light)
            self.assertIsNone(active.equipped.light)
            message_bus.send_to_character.assert_awaited_once_with(
                "active_char",
                "a brass lamp flickers and goes out.\r\n",
            )
            message_bus.send_to_room.assert_awaited_once_with(
                "a brass lamp goes out.\r\n",
                [viewer],
            )

        asyncio.run(run_test())

    def test_rom_poison_tick_sends_messages_and_applies_periodic_damage(self):
        async def run_test():
            poisoned = Character.from_json(build_character_data("poisoned_char"))
            poisoned.name = "Tester"
            poisoned.hit = 20
            poisoned.status_flags.assign_bitfield("affected_by", AffectedBy.AFF_POISON.value)
            poisoned.effects = [
                Effect(type="spell.poison", level=20, duration=3, bitvector="AFF_POISON")
            ]
            viewer = Character.from_json(build_character_data("viewer_char"))
            room = SimpleNamespace(
                characters={"poisoned_char": poisoned, "viewer_char": viewer},
                mobiles={},
                players_in_room=lambda: [poisoned, viewer],
                people=lambda: [poisoned, viewer],
            )
            handler, _, message_bus = self._handler([poisoned, viewer])
            handler.spell_registry.all_spells.return_value = [
                self._spell_payload(
                    "poison",
                    "spell.poison",
                    {
                        "toVictim": {"tick": "You shiver and suffer.\r\n"},
                        "toRoom": {"tick": "{victim} shivers and suffers.\r\n"},
                    },
                )
            ]

            await handler._tick_rom_status_effects(poisoned, room)

            self.assertEqual(17, poisoned.hit)
            handler.fight_handler.update_pos.assert_called_once_with(poisoned)
            handler.fight_handler.raw_kill.assert_not_called()
            message_bus.send_to_character.assert_awaited_once_with("poisoned_char", "You shiver and suffer.\r\n")
            message_bus.send_to_room.assert_awaited_once_with(
                "Tester shivers and suffers.\r\n",
                [viewer],
            )

        asyncio.run(run_test())

    def test_rom_plague_tick_spreads_and_drains_before_periodic_damage(self):
        async def run_test():
            carrier = Character.from_json(build_character_data("carrier_char"))
            carrier.name = "Carrier"
            carrier.level = 30
            carrier.hit = 50
            carrier.mana = 20
            carrier.movement = 20
            carrier.status_flags.assign_bitfield("affected_by", AffectedBy.AFF_PLAGUE.value)
            carrier.effects = [
                Effect(type="spell.plague", level=10, duration=3, bitvector="AFF_PLAGUE")
            ]
            victim = Character.from_json(build_character_data("victim_char"))
            victim.name = "Victim"
            room = SimpleNamespace(
                characters={"carrier_char": carrier, "victim_char": victim},
                mobiles={},
                players_in_room=lambda: [carrier, victim],
                people=lambda: [carrier, victim],
            )
            handler, _, message_bus = self._handler([carrier, victim])
            handler.spell_registry.all_spells.return_value = [
                self._spell_payload(
                    "plague",
                    "spell.plague",
                    {
                        "toVictim": {
                            "tick": "You writhe in agony from the plague.\r\n",
                            "spread": "You feel hot and feverish.\r\n",
                        },
                        "toRoom": {
                            "tick": "{victim} writhes in agony as plague sores erupt from {possessive} skin.\r\n",
                            "spread": "{victim} shivers and looks very ill.\r\n",
                        },
                    },
                )
            ]
            handler.rng.number_range = Mock(return_value=4)
            handler.rng.number_bits = Mock(return_value=0)

            def join_effect(target, effect):
                target.effects.append(effect)
                target.status_flags.assign_bitfield(
                    "affected_by",
                    target.status_flags.affected_by | AffectedBy.AFF_PLAGUE.value,
                )

            handler.effect_handler.affect_join.side_effect = join_effect

            with patch("game.UpdateHandler.CharacterApi.is_immortal", return_value=False), \
                    patch("game.UpdateHandler.EffectUtil.saves_spell", return_value=False):
                await handler._tick_rom_status_effects(carrier, room)

            self.assertEqual(47, carrier.hit)
            self.assertEqual(17, carrier.mana)
            self.assertEqual(17, carrier.movement)
            self.assertTrue(victim.status_flags.affected_by & AffectedBy.AFF_PLAGUE.value)
            handler.effect_handler.affect_join.assert_called_once()
            handler.fight_handler.update_pos.assert_called_once_with(carrier)
            self.assertEqual(
                [
                    ("carrier_char", "You writhe in agony from the plague.\r\n"),
                    ("victim_char", "You feel hot and feverish.\r\n"),
                ],
                [call.args for call in message_bus.send_to_character.await_args_list],
            )
            self.assertIn(
                ("Carrier writhes in agony as plague sores erupt from his skin.\r\n", [victim]),
                [call.args for call in message_bus.send_to_room.await_args_list],
            )

        asyncio.run(run_test())

    def test_rom_mortal_tick_applies_quiet_periodic_damage(self):
        async def run_test():
            character = Character.from_json(build_character_data("mortal_char"))
            character.hit = -6
            character.character_attributes.position = Positions.POS_MORTAL.value
            handler, _, message_bus = self._handler([character])

            await handler._tick_rom_status_effects(character, SimpleNamespace())

            self.assertEqual(-7, character.hit)
            handler.fight_handler.update_pos.assert_called_once_with(character)
            message_bus.send_to_character.assert_not_awaited()
            message_bus.send_to_room.assert_not_awaited()

        asyncio.run(run_test())

    def test_tick_effects_sends_msg_off_and_ignores_placeholder_messages(self):
        async def run_test():
            active = Character.from_json(build_character_data("active_char"))
            armor = self._spell_payload(
                "armor",
                "spell.armor",
                {"toChar": {"msgOff": "You feel less armored.", "msgObj": ""}},
            )
            teleport = self._spell_payload(
                "teleport",
                "spell.teleport",
                {"toChar": {"msgOff": "!Teleport!", "msgObj": ""}},
            )
            expired = [
                SimpleNamespace(type="spell.armor"),
                SimpleNamespace(type="spell.teleport"),
            ]

            handler, registry_service, message_bus = self._handler([active])
            registry_service.spell_registry.all_spells.return_value = [armor, teleport]
            handler.effect_handler.tick_effects.return_value = SimpleNamespace(expired_effects=expired)

            await handler._tick_effects(active)

            message_bus.send_to_character.assert_awaited_once_with("active_char", "You feel less armored.\r\n")

        asyncio.run(run_test())

    def test_tick_item_effects_sends_msg_obj_to_holder(self):
        async def run_test():
            holder = SimpleNamespace(id="char_001")
            item = SimpleNamespace(id="item_001", name="sword", short_description="a bright sword")
            spell = self._spell_payload(
                "bless",
                "spell.bless",
                {"toChar": {"msgOff": "", "msgObj": "$p's holy aura fades."}},
            )

            handler, registry_service, message_bus = self._handler([])
            registry_service.spell_registry.all_spells.return_value = [spell]
            handler.effect_handler.tick_effects.return_value = SimpleNamespace(expired_effects=[SimpleNamespace(type="spell.bless")])
            handler._locate_item = Mock(return_value={"kind": "char_loot", "parent": holder, "room": None})

            await handler._tick_item_effects(item)

            message_bus.send_to_character.assert_awaited_once_with("char_001", "a bright sword's holy aura fades.\r\n")

        asyncio.run(run_test())

    def test_char_update_ticks_active_session_characters(self):
        async def run_test():
            active = Character.from_json(build_character_data("active_char"))
            active.status_flags.thirst = 1
            active.status_flags.hunger = 1

            handler, _, message_bus = self._handler([active])

            with patch("game.UpdateHandler.CharacterApi.is_immortal", return_value=False):
                await handler.char_update()

            self.assertEqual(0, active.status_flags.thirst)
            self.assertEqual(0, active.status_flags.hunger)
            self.assertEqual(
                [
                    ("active_char", "You are thirsty.\r\n"),
                    ("active_char", "You are hungry.\r\n"),
                ],
                [call.args for call in message_bus.send_to_character.await_args_list],
            )

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()
