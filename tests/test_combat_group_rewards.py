import importlib.util
import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch
import asyncio

from tests import test_combat_handler_aggression as fixtures


ROOT = Path(__file__).resolve().parents[1]
Runtime = sys.modules[fixtures.FightHandler.__module__]


def _advancement_class():
    spec = importlib.util.spec_from_file_location("_group_reward_advancement", ROOT / "src/player/CharacterAdvancement.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.CharacterAdvancement


Advancement = _advancement_class()


class TestCombatGroupRewards(unittest.TestCase):
    def setUp(self):
        self.fixtures = fixtures.TestFightHandlerAggression()
        self.killer = self._player("killer", 10)
        self.ally = self._player("ally", 20)
        self.ally.leader = self.killer
        self.pet = self.fixtures._mob("pet")
        self.pet.level = 9
        self.pet.leader = self.killer
        self.outsider = self._player("outsider", 50)
        self.victim = self.fixtures._mob("victim")
        self.victim.name = "Victim"
        self.victim.hit = 1
        self.entities = [self.killer, self.ally, self.pet, self.outsider, self.victim]
        self.room = self.fixtures._safety_room(*self.entities)
        self.room.id = "room-1"
        self.room.people = lambda: list(self.entities)
        self.room.player_targets = lambda actor: [x for x in self.entities if not x.is_npc and x is not actor]
        self.room.add_item_to_room = Mock()
        self.handler = self.fixtures._handler(self.room)
        config = json.loads((ROOT / "resources/collections/SOMDB.GameData.json").read_text())[0]
        self.handler.group_reward_payload = Runtime.GamePayload.from_json(config["combat"]["groupRewards"]["payload"])
        self.handler.ItemFlags = SimpleNamespace(ITEM_ANTI_EVIL=1, ITEM_ANTI_GOOD=2, ITEM_ANTI_NEUTRAL=4)
        self.handler.effect_handler.remove_item_effects = Mock()
        self.handler.message_bus = SimpleNamespace(text_to_message=lambda text: text,
                                                   send_to_character=AsyncMock(), send_to_room=AsyncMock())
        self.advancement = patch.object(Runtime, "CharacterAdvancement", Advancement)
        self.advancement.start()
        self.addCleanup(self.advancement.stop)
        self.flag_api = patch.object(Runtime, "ItemApi", SimpleNamespace(
            has_item_flag=lambda item, enums, name: bool(item.extra_flags & getattr(enums, name))))
        self.flag_api.start()
        self.addCleanup(self.flag_api.stop)
        for name, predicate in (
            ("is_good", lambda entity: entity.character_attributes.alignment >= 350),
            ("is_evil", lambda entity: entity.character_attributes.alignment <= -350),
            ("is_neutral", lambda entity: -350 < entity.character_attributes.alignment < 350),
        ):
            patcher = patch.object(Runtime.CharacterApi, name, predicate, create=True)
            patcher.start()
            self.addCleanup(patcher.stop)

    def _player(self, name, level):
        player = self.fixtures._player(name)
        player.name, player.level = name, level
        player.character_attributes.alignment = 0
        player.character_attributes.experience = 0
        player.character_attributes.accumulated_experience = 0
        player.character_attributes.experience_per_level = 10000
        player.inventory = []
        player.equipped = SimpleNamespace()
        player.get_alignment = lambda: player.character_attributes.alignment
        player.set_alignment = lambda value: setattr(player.character_attributes, "alignment", value)
        def unequip(slot):
            item = getattr(player.equipped, slot)
            setattr(player.equipped, slot, None)
            player.inventory.append(item)
        player.unequip_item = unequip
        player.remove_item = lambda item: player.inventory.remove(item)
        return player

    def test_room_group_rewards_use_player_levels_and_truncated_half_npc_levels(self):
        self.handler.xp_compute = Mock(side_effect=[11, 22])
        result = self.handler.group_gain(self.killer, self.victim)
        self.assertEqual([(self.killer, self.victim, 34), (self.ally, self.victim, 34)],
                         [call.args for call in self.handler.xp_compute.call_args_list])
        self.assertEqual(11, self.killer.character_attributes.experience)
        self.assertEqual(22, self.ally.character_attributes.experience)
        self.assertEqual(0, self.outsider.character_attributes.experience)
        self.assertEqual(11, result["xp_gain"])
        self.assertEqual([self.killer, self.ally], [payload["victim"] for payload in result["reward_payloads"]])
        self.assertIn("22 experience points", result["reward_payloads"][1]["to_victim"])

    def test_npc_killing_blow_rewards_grouped_players(self):
        self.handler.xp_compute = Mock(return_value=30)
        result = self.handler.group_gain(self.pet, self.victim)
        self.assertEqual(2, self.handler.xp_compute.call_count)
        self.assertTrue(all(call.args[2] == 34 for call in self.handler.xp_compute.call_args_list))
        self.assertEqual(30, self.killer.character_attributes.experience)
        self.assertEqual(30, self.ally.character_attributes.experience)
        self.assertEqual(0, result["xp_gain"])
        self.assertEqual(2, len(result["reward_payloads"]))
        payload = self.handler.build_round_payload(self.pet, self.victim, self.room, {"killed": True, **result})
        asyncio.run(self.handler.emit_round_payload(self.pet, payload))
        self.handler.message_bus.send_to_character.assert_any_await("killer", "You receive 30 experience points.\r\n")
        self.handler.message_bus.send_to_character.assert_any_await("ally", "You receive 30 experience points.\r\n")

    def test_off_room_members_do_not_contribute_or_receive_rewards(self):
        self.entities.remove(self.ally)
        self.room.characters.pop(self.ally.id)
        self.ally.room_id = "another-room"
        self.handler.xp_compute = Mock(return_value=10)
        self.handler.group_gain(self.killer, self.victim)
        self.handler.xp_compute.assert_called_once_with(self.killer, self.victim, 14)
        self.assertEqual(0, self.ally.character_attributes.experience)

    def test_each_member_gets_their_own_level_messages_with_original_group_total(self):
        self.handler.xp_compute = Mock(side_effect=[11, 22])
        def level_up(member, _xp):
            member.level += 1
            return SimpleNamespace(level_up_messages=f"{member.name} level gained\r\n")
        with patch.object(Advancement, "gain_experience", side_effect=level_up):
            result = self.handler.group_gain(self.killer, self.victim)
        self.assertEqual([34, 34], [call.args[2] for call in self.handler.xp_compute.call_args_list])
        self.assertEqual("killer level gained\r\n", result["level_up_messages"])
        self.assertEqual("You receive 11 experience points.\r\nkiller level gained\r\n",
                         result["reward_payloads"][0]["to_victim"])
        self.assertEqual("You receive 22 experience points.\r\nally level gained\r\n",
                         result["reward_payloads"][1]["to_victim"])

    def test_self_death_and_ungrouped_npc_kills_do_not_reward_players(self):
        self.handler.xp_compute = Mock()
        for attacker, victim in ((self.killer, self.killer), (None, self.victim), (self.victim, self.pet)):
            with self.subTest(attacker=attacker):
                result = self.handler.group_gain(attacker, victim)
                self.assertEqual([], result["reward_payloads"])
        self.handler.xp_compute.assert_not_called()

    def test_player_victim_is_not_excluded_by_local_rom_code(self):
        target = self._player("player_target", 10)
        self.entities.append(target)
        self.handler.xp_compute = Mock(return_value=10)
        self.handler.group_gain(self.killer, target)
        self.assertEqual(10, self.killer.character_attributes.experience)
        self.assertEqual(10, self.ally.character_attributes.experience)
        self.assertEqual(0, target.character_attributes.experience)

    def test_real_xp_alignment_change_drops_killers_incompatible_equipment(self):
        self.entities.remove(self.ally)
        self.entities.remove(self.pet)
        self.killer.character_attributes.alignment = -340
        self.victim.get_alignment = lambda: 1000
        blade = SimpleNamespace(name="blade", short_description="the blade", extra_flags=1)
        self.killer.equipped.wielded = blade
        with patch.object(Runtime.random, "randint", side_effect=lambda low, _high: low):
            result = self.handler.group_gain(self.killer, self.victim)
        self.assertEqual(-479, self.killer.get_alignment())
        self.assertIsNone(self.killer.equipped.wielded)
        self.assertEqual([], self.killer.inventory)
        self.handler.effect_handler.remove_item_effects.assert_called_once_with(self.killer, blade)
        self.room.add_item_to_room.assert_called_once_with(blade)
        self.assertIn("You are zapped by the blade", result["reward_payloads"][1]["to_victim"])
        self.assertEqual([self.outsider], result["reward_payloads"][1]["targets"])

    def test_real_xp_computation_changes_each_members_alignment_independently(self):
        self.killer.set_alignment(-340)
        self.ally.set_alignment(-340)
        self.victim.get_alignment = lambda: 1000
        with patch.object(Runtime.random, "randint", side_effect=lambda low, _high: low):
            self.handler.group_gain(self.killer, self.victim)
        self.assertEqual(-380, self.killer.get_alignment())
        self.assertEqual(-341, self.ally.get_alignment())
        self.assertEqual(0, self.outsider.get_alignment())

    def test_equipment_check_matches_original_killer_not_each_rewarded_member(self):
        killer_item = SimpleNamespace(name="killer blade", extra_flags=1)
        ally_item = SimpleNamespace(name="ally blade", extra_flags=1)
        self.killer.equipped.wielded = killer_item
        self.ally.equipped.wielded = ally_item
        def xp(member, _victim, _total):
            member.set_alignment(-500)
            return 1
        self.handler.xp_compute = Mock(side_effect=xp)
        self.handler.group_gain(self.killer, self.victim)
        self.assertIsNone(self.killer.equipped.wielded)
        self.assertIs(self.ally.equipped.wielded, ally_item)
        self.room.add_item_to_room.assert_called_once_with(killer_item)

    def test_lethal_damage_rewards_group_before_extracting_victim(self):
        self.handler.check_killer = Mock(return_value={})
        self.handler._set_fighting = Mock()
        self.handler._check_immunity = Mock(return_value="IS_NORMAL")
        self.handler.dam_message = Mock(return_value={"to_char": "hit"})
        self.handler.xp_compute = Mock(side_effect=[5, 7])
        def kill(victim):
            self.assertEqual(5, self.killer.character_attributes.experience)
            self.assertEqual(7, self.ally.character_attributes.experience)
            self.entities.remove(victim)
        self.handler.raw_kill = Mock(side_effect=kill)
        result = self.handler.damage(self.killer, self.victim, 1)
        self.assertTrue(result["killed"])
        self.assertEqual(5, result["xp_gain"])
        self.assertEqual(2, len(result["reward_payloads"]))
        self.handler.raw_kill.assert_called_once_with(self.victim)

    def test_round_payload_and_emitter_deliver_each_reward_without_duplicates(self):
        self.handler.xp_compute = Mock(side_effect=[5, 7])
        rewards = self.handler.group_gain(self.killer, self.victim)
        self.handler._find_latest_corpse = Mock(return_value=None)
        payload = self.handler.build_round_payload(self.killer, self.victim, self.room,
                                                  {"killed": True, **rewards})
        self.assertNotIn("experience points", payload["payloads"][0]["to_char"])
        prompted = asyncio.run(self.handler.emit_round_payload(self.killer, payload))
        sent = self.handler.message_bus.send_to_character.await_args_list
        xp_notices = [(call.args[0], call.args[1]) for call in sent if "experience points" in call.args[1]]
        self.assertEqual([("killer", "You receive 5 experience points.\r\n"),
                          ("ally", "You receive 7 experience points.\r\n")], xp_notices)
        self.assertIn(self.ally, prompted)

    def test_reward_payloads_survive_multiple_attack_and_weapon_proc_merges(self):
        first, second = {"victim": self.killer, "to_victim": "first"}, {"victim": self.ally, "to_victim": "second"}
        left, right = {"reward_payloads": [first], "xp_gain": 3}, {"reward_payloads": [second], "xp_gain": 4}
        from tests.test_weapon_hit_effects import WeaponHitHandler
        for merge in (Runtime.FightHandler._merge_attack_payloads, WeaponHitHandler._merge):
            result = merge(left, right)
            self.assertEqual([first, second], result["reward_payloads"])
            self.assertEqual(7, result["xp_gain"])

    def test_spell_damage_queues_each_recipient_reward(self):
        self.handler.xp_compute = Mock(side_effect=[5, 7])
        rewards = self.handler.group_gain(self.killer, self.victim)
        SpellApi = self.fixtures._spell_api_class()
        spell_api = SpellApi(effect_handler=Mock(), interp_api=Mock())
        spell_api.send = Mock()
        ctx = SimpleNamespace(queue_payload=Mock())
        spell_api._queue_damage_payload(ctx, {"to_char": "hit", **rewards}, self.victim)
        self.assertEqual(rewards["reward_payloads"], [call.args[0] for call in ctx.queue_payload.call_args_list])
        spell_api.send.assert_called_once_with(ctx, to_char="hit", to_room="", to_victim="", victim=self.victim)

    def test_nested_command_payloads_deliver_rewards_and_deduplicate_prompts(self):
        replacements = {name: SimpleNamespace(**{attr: object}) for name, attr in (
            ("api.InterpApi", "InterpApi"), ("interp.Context", "Context"),
            ("interp.CommandAccess", "CommandAccess"), ("interp.CommandExecutor", "CommandExecutor"),
            ("interp.commands.Info", "Info"), ("interp.commands.Movement", "Movement"),
            ("interp.commands.Communications", "Communications"), ("interp.commands.Fight", "Fight"),
            ("interp.commands.Object", "Object"), ("interp.commands.Wiz", "Wiz"),
            ("notes.NoteHandler", "NoteHandler"), ("util.PlayerUtil", "PlayerUtil"))}
        replacements["combat.CombatHandler"] = SimpleNamespace(FightHandler=Runtime.FightHandler)
        replacements["skill.Ability"] = SimpleNamespace(Ability=SimpleNamespace(take_improve_messages=lambda _entity: ""))
        with patch.dict(sys.modules, replacements):
            spec = importlib.util.spec_from_file_location("_group_reward_player_handler", ROOT / "src/player/PlayerHandler.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        player_handler = module.PlayerHandler.__new__(module.PlayerHandler)
        player_handler.message_bus = self.handler.message_bus
        player_handler._send_prompt = AsyncMock()
        self.handler.xp_compute = Mock(side_effect=[5, 7])
        rewards = self.handler.group_gain(self.killer, self.victim)["reward_payloads"]
        asyncio.run(player_handler._handle_fight_payload(self.killer, None, {
            "payloads": [{"to_char": "attack"}, {"payloads": rewards}]}))
        self.assertEqual([("killer", "attack"), ("killer", "You receive 5 experience points.\r\n"),
                          ("ally", "You receive 7 experience points.\r\n")],
                         [call.args for call in player_handler.message_bus.send_to_character.await_args_list])
        player_handler._send_prompt.assert_awaited_once_with(self.ally, None, prefer_context_room=False)


if __name__ == "__main__":
    unittest.main()
