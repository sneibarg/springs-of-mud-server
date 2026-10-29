"""ROM24 theft failure consequences, attempt ordering, and currency aliases."""
import json
import sys
import unittest
from enum import IntEnum
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import AsyncMock, Mock, patch

from tests import test_object_consumption_parity as consumption

h = consumption.h
with patch.dict(sys.modules, {"api.SkillApi": NS(SkillApi=object)}):
    Movement = h._load_module("theft_movement", "interp/commands/Movement.py").Movement
with patch.dict(sys.modules, {name: NS(**{attr: object}) for name, attr in (
        ("api.AliasApi", "AliasApi"), ("api.CommunicationsApi", "CommunicationsApi"),
        ("player.CharacterService", "CharacterService"), ("server.session.SessionHandler", "SessionHandler"))}):
    CommunicationsModule = h._load_module("theft_communications", "interp/commands/Communications.py")
    Communications = CommunicationsModule.Communications
CommunicationsUtil = h._load_module("theft_communications_util", "util/CommunicationsUtil.py").CommunicationsUtil


class TestObjectTheftParity(unittest.TestCase):
    def setUp(self):
        self.base = consumption.TestObjectConsumptionParity()
        self.base.setUp()
        self.addCleanup(self.base.doCleanups)
        self.fixture = self.base.fixture
        self.actor, self.room, self.commands = self.base.actor, self.base.room, self.base.commands
        self.actor.guild = "loner"
        data = json.loads((Path(h.ROOT) / "resources/collections/SOMDB.GameData.json").read_text())[0]
        self.enums = {key: IntEnum(key, value) for key, value in data["enums"].items()}
        self.commands.item_flags = self.enums["itemFlags"]
        self.commands.PlayerActBits = self.enums["playerActBits"]
        self.commands.affected_bits = self.enums["affectedBy"]
        self.base.effects.affected_by = self.enums["affectedBy"]
        self.positions = self.enums["positions"]
        self.swap(h._CharacterApi, "get_enum", side_effect=self.enums.__getitem__)
        self.swap(h._CharacterApi, "position_value", side_effect=lambda ch: ch.character_attributes.position, create=True)
        self.swap(h._CharacterApi, "pos_value", side_effect=lambda key: self.positions[key].value, create=True)
        self.swap(h._CharacterApi, "is_awake", side_effect=lambda ch: ch.character_attributes.position > self.positions.POS_SLEEPING.value, create=True)
        self.swap(h._CharacterApi, "is_affected_by_name", create=True,
                  side_effect=lambda ch, enum, name: bool(ch.status_flags.affected_by & enum[name].value))
        self.swap(h._CharacterApi, "set_position", create=True,
                  side_effect=lambda ch, name: setattr(ch.character_attributes, "position", self.positions[name].value))
        self.swap(sys.modules[h.InterpApi.__module__], "CommunicationsUtil", new=CommunicationsUtil)
        self.swap(CommunicationsModule, "CommunicationsUtil", new=CommunicationsUtil)
        self.movement = Movement.__new__(Movement)
        self.swap(Movement.do_stand.__globals__['MovementApi'], 'argument_text',
                  new=lambda context: str(getattr(context, 'result', '') or ''), create=True)
        self.movement.affected_bits = self.enums["affectedBy"]
        self.communications = Communications.__new__(Communications)
        self.communications.interp_api = self.commands.interp_api
        self.communications.session_handler = NS(get_playing_sessions=lambda: [NS(character=ch) for ch in (self.actor, self.victim, self.base.witness)])
        self.player_handler = NS(movement_commands=self.movement, communications_commands=self.communications)
        self.save = Mock()
        self.commands.fight_handler = NS(is_safe=Mock(return_value=(False, "")),
            character_service=NS(queue_save_character=self.save), multi_hit=Mock(return_value={"hit": True}),
            build_round_payload=Mock(return_value={"to_victim": "Retaliation!", "victim": self.actor}))
        self.improve = Mock()
        self.commands._improve_item_skill = self.improve
        self.victim = self.character("Victim")
        self.actor.character_attributes.position = self.positions.POS_STANDING.value
        self.actor.area_id = self.victim.area_id = self.base.witness.area_id = "area"
        self.actor.status_flags.comm = 0
        self.room.characters[self.actor.id] = self.actor
        self.room.characters[self.victim.id] = self.victim

    def swap(self, target, name, **kwargs):
        swap = patch.object(target, name, **kwargs)
        result = swap.start()
        self.addCleanup(swap.stop)
        return result

    def character(self, name, npc=False):
        ch = self.fixture._build_character(name=name, is_npc=npc)
        ch.area_id = "area"
        ch.character_attributes.position = self.positions.POS_STANDING.value
        ch.status_flags.affected_by = ch.status_flags.comm = 0
        return ch

    def context(self, raw="coins Victim"):
        context = self.fixture._build_context(raw, self.room, self.actor, "steal")
        context.player_handler = lambda: self.player_handler
        return context

    def attempt(self, raw="coins Victim", rolls=(100, 0)):
        with patch.object(sys.modules[h.Object.__module__].random, "randint", side_effect=rolls):
            return self.commands.do_steal(self.actor, self.context(raw))

    def test_clanless_player_fails_successful_item_roll_and_triggers_player_consequences(self):
        item = self.base.item("ring", item_type="jewelry", value4="0")
        self.victim.loot.append(item)
        self.actor.guild = ""
        self.actor.skill_level = lambda name: 100
        self.actor.level = self.victim.level = 10
        parts = self.attempt("ring Victim", rolls=(1, 0))["payloads"]
        self.assertEqual("Oops.\r\n", parts[0]["to_char"])
        self.assertIn(item, self.victim.loot)
        self.assertNotIn(item, self.actor.loot)
        self.assertEqual(24, self.actor.status_flags.pulse_wait)
        self.assertTrue(self.actor.status_flags.act & self.enums["playerActBits"].PLR_THIEF.value)
        self.assertTrue(any("to_wiznet" in part for part in parts))
        self.save.assert_called_once_with(self.actor)
        self.improve.assert_not_called()

    def test_clanless_currency_attempts_never_transfer_or_roll_amounts(self):
        self.actor.guild = None
        self.actor.skill_level = lambda name: 100
        self.actor.level = self.victim.level = 10
        self.actor.gold, self.actor.silver = 2, 3
        self.victim.gold, self.victim.silver = 100, 200
        for selector in ("coin", "coins", "gold", "silver"):
            with self.subTest(selector=selector):
                parts = self.attempt(selector + " Victim", rolls=(1, 0))["payloads"]
                self.assertEqual("Oops.\r\n", parts[0]["to_char"])
                self.assertEqual((2, 3, 100, 200), (self.actor.gold, self.actor.silver,
                                                   self.victim.gold, self.victim.silver))
        self.save.assert_called_once_with(self.actor)
        self.improve.assert_not_called()

    def test_clanless_npc_victim_failure_strips_sneak_and_retaliates(self):
        self.actor.guild = "0"
        self.actor.skill_level = lambda name: 100
        self.victim.is_npc = True
        self.actor.status_flags.affected_by |= self.enums["affectedBy"].AFF_SNEAK.value
        parts = self.attempt(rolls=(1, 0))["payloads"]
        self.assertEqual("Oops.\r\n", parts[0]["to_char"])
        self.assertFalse(self.actor.status_flags.affected_by & self.enums["affectedBy"].AFF_SNEAK.value)
        self.commands.fight_handler.multi_hit.assert_called_once_with(self.victim, self.actor, dt="TYPE_UNDEFINED")
        self.improve.assert_called_once_with(self.actor, "steal", False)
        self.save.assert_not_called()

    def test_membership_uses_existing_guild_contract_and_accepts_loner(self):
        self.actor.skill_level = lambda name: 100
        self.actor.level = self.victim.level = 10
        for guild, expected in [(None, False), ("", False), ("0", False), (" none ", False),
                                ("NO", False), ("clanless", False), ("loner", True),
                                ("independent", True), ("rom", True)]:
            with self.subTest(guild=guild):
                self.actor.guild = guild
                with patch.object(sys.modules[h.Object.__module__].random, "randint", return_value=1) as roll:
                    self.assertEqual(expected, self.commands._steal_succeeds(self.actor, self.victim, self.room))
                roll.assert_called_once_with(1, 100)

    def test_npc_thief_is_exempt_from_clan_requirement(self):
        self.actor.is_npc, self.actor.guild = True, ""
        item = self.base.item("ring", item_type="jewelry")
        self.victim.loot.append(item)
        payload = self.attempt("ring Victim", rolls=())
        self.assertEqual("You pocket ring.\r\n", payload["to_char"])
        self.assertIn(item, self.actor.loot)
        self.assertNotIn(item, self.victim.loot)
        self.save.assert_not_called()

    def test_safe_target_still_blocks_clanless_thief_before_wait_and_roll(self):
        self.actor.guild = ""
        self.commands.fight_handler.is_safe.return_value = (True, "safe")
        payload = self.attempt(rolls=())
        self.assertEqual("safe\r\n", payload["to_char"])
        self.assertEqual(0, self.actor.status_flags.pulse_wait)
        self.save.assert_not_called()

    def test_clanless_failure_precedes_inventory_lookup_even_with_good_roll(self):
        self.actor.guild = ""
        self.actor.skill_level = lambda name: 100
        self.actor.level = self.victim.level = 10
        with patch.object(self.commands, "_inventory_item") as lookup:
            parts = self.attempt("missing Victim", rolls=(1, 0))["payloads"]
        self.assertEqual("Oops.\r\n", parts[0]["to_char"])
        lookup.assert_not_called()
        self.assertEqual(24, self.actor.status_flags.pulse_wait)

    def test_failed_npc_theft_strips_sneak_wakes_yells_and_retaliates_immediately(self):
        self.victim.is_npc = True
        self.victim.character_attributes.position = self.positions.POS_SLEEPING.value
        from item.Effect import Effect
        self.base.effects.affect_join(self.actor, Effect(type="skill.sneak", bitvector="AFF_SNEAK", duration=5))
        other = Effect(type="spell.armor", duration=5)
        self.actor.effects.append(other)
        self.actor.status_flags.affected_by |= self.enums["affectedBy"].AFF_HIDE.value
        self.commands.fight_handler.multi_hit.side_effect = lambda victim, thief, dt: {
            "awake": h._CharacterApi.is_awake(victim), "sneaking": bool(thief.status_flags.affected_by & self.enums["affectedBy"].AFF_SNEAK.value)}
        payload = self.attempt()
        self.assertEqual([other], self.actor.effects)
        self.assertEqual(self.enums["affectedBy"].AFF_HIDE.value, self.actor.status_flags.affected_by)
        self.assertEqual(self.positions.POS_STANDING.value, self.victim.character_attributes.position)
        self.assertEqual(24, self.actor.status_flags.pulse_wait)
        parts = payload["payloads"]
        self.assertEqual("Oops.\r\n", parts[0]["to_char"])
        self.assertIs(self.victim, parts[1]["actor"])
        self.assertEqual("stand", parts[1]["context"].command.name)
        self.assertEqual("Victim yells 'Tester is a lousy thief!'\r\n", parts[2]["payloads"][0]["global_message"])
        self.commands.fight_handler.build_round_payload.assert_called_once_with(
            self.victim, self.actor, self.room, {"awake": True, "sneaking": False})
        self.assertIs(self.victim, parts[3]["actor"])
        self.improve.assert_called_once_with(self.actor, "steal", False)
        self.save.assert_not_called()

    def test_magical_sleep_blocks_wake_and_yell_but_not_retaliation_attempt(self):
        self.victim.is_npc = True
        self.victim.character_attributes.position = self.positions.POS_SLEEPING.value
        self.victim.status_flags.affected_by = self.enums["affectedBy"].AFF_SLEEP.value
        parts = self.attempt()["payloads"]
        self.assertEqual(3, len(parts))  # detection, failed wake, combat attempt
        self.assertEqual("can_t_wake_up", parts[1]["payloads"][0]["message_key"])
        self.assertEqual(self.positions.POS_SLEEPING.value, self.victim.character_attributes.position)
        self.commands.fight_handler.multi_hit.assert_called_once_with(self.victim, self.actor, dt="TYPE_UNDEFINED")

    def test_player_failure_marks_and_saves_only_once_and_does_not_train_failure(self):
        for _ in range(2):
            parts = self.attempt()["payloads"]
            self.assertTrue(any("to_wiznet" in p for p in parts))
        self.save.assert_called_once_with(self.actor)
        self.assertTrue(self.actor.status_flags.act & self.enums["playerActBits"].PLR_THIEF.value)
        self.improve.assert_not_called()
        self.commands.fight_handler.multi_hit.assert_not_called()

    def test_four_reaction_variants_yell_with_victim_as_speaker(self):
        for roll, text in ((0, "is a lousy thief!"), (1, "paper bag!"), (2, "tried to rob me!"), (3, "Keep your hands")):
            with self.subTest(roll=roll):
                yell = self.attempt(rolls=(100, roll))["payloads"][1]
                self.assertIs(self.victim, yell["actor"])
                reaction = yell["payloads"][0]
                self.assertIn(text, reaction["global_message"])
                self.assertIn(self.actor, reaction["global_targets"])
                self.assertNotIn(self.victim, reaction["global_targets"])

    def test_noshout_victim_cannot_yell(self):
        self.victim.status_flags.comm = self.enums["commFlags"].COMM_NOSHOUT.value
        yell = self.attempt()["payloads"][1]["payloads"][0]
        self.assertEqual("You can't yell.\r\n", yell["to_char"])
        self.assertNotIn("global_message", yell)

    def test_failed_missing_item_attempt_never_looks_up_item(self):
        lookup = Mock(wraps=self.victim.find_inventory_item)
        self.victim.find_inventory_item = lookup
        self.attempt("missing Victim")
        lookup.assert_not_called()
        self.assertEqual(24, self.actor.status_flags.pulse_wait)
        self.save.assert_called_once_with(self.actor)

    def test_successful_attempt_checks_item_after_roll_and_wait_for_all_rejections(self):
        for kind, message in (("missing", "You can't find it."), ("nodrop", "You can't pry it away."),
                              ("inventory", "You can't pry it away."), ("level", "You can't pry it away."),
                              ("count", "You have your hands full."), ("weight", "You can't carry that much weight.")):
            with self.subTest(kind=kind):
                self.actor.status_flags.pulse_wait = 0
                self.actor.character_attributes.max_items = 10
                self.actor.character_attributes.max_weight = 100
                item = consumption.TestObjectConsumptionParity.item("gem", level=1, weight=1, extra_flags="0")
                self.victim.loot.clear()
                if kind != "missing":
                    self.victim.loot.append(item)
                if kind in ("nodrop", "inventory"):
                    item.extra_flags = str(self.enums["itemFlags"]["ITEM_NODROP" if kind == "nodrop" else "ITEM_INVENTORY"].value)
                if kind == "level":
                    item.level = self.actor.level + 1
                if kind == "count":
                    self.actor.character_attributes.max_items = 1
                    self.actor.loot[:] = [NS()]
                if kind == "weight":
                    item.weight = 1000
                with patch.object(self.commands, "_steal_succeeds", side_effect=lambda *args: self.actor.status_flags.pulse_wait == 24):
                    payload = self.commands.do_steal(self.actor, self.context("gem Victim"))
                self.assertEqual(message + "\r\n", payload["to_char"])
                self.assertEqual(24, self.actor.status_flags.pulse_wait)
                self.assertNotIn(item, self.actor.loot)
                self.actor.loot.clear()
        self.improve.assert_not_called()
        self.save.assert_not_called()

    def test_early_rejections_do_not_charge_wait_or_react(self):
        for argument in ("", "coins absent", "coins Tester"):
            payload = self.commands.do_steal(self.actor, self.context(argument))
            self.assertNotIn("payloads", payload)
            self.assertEqual(0, self.actor.status_flags.pulse_wait)
        self.commands.fight_handler.is_safe.return_value = (True, "safe")
        self.commands.do_steal(self.actor, self.context())
        self.assertEqual(0, self.actor.status_flags.pulse_wait)
        self.save.assert_not_called()

    def test_all_currency_selectors_roll_and_transfer_both_balances(self):
        for selector in ("coin", "coins", "gold", "silver"):
            with self.subTest(selector=selector):
                self.actor.gold, self.actor.silver = 2, 3
                self.victim.gold, self.victim.silver = 61, 121
                with patch.object(self.commands, "_steal_succeeds", return_value=True), \
                        patch.object(sys.modules[h.Object.__module__].random, "randint", side_effect=[2, 3]) as roll:
                    payload = self.commands.do_steal(self.actor, self.context(selector + " Victim"))
                self.assertEqual((4, 9, 59, 115), (self.actor.gold, self.actor.silver, self.victim.gold, self.victim.silver))
                self.assertEqual("Bingo!  You got 6 silver and 2 gold coins.\r\n", payload["to_char"])
                self.assertEqual([(1, 10), (1, 10)], [call.args for call in roll.call_args_list])
        self.assertEqual(4, self.improve.call_count)

    def test_zero_currency_result_does_not_train_or_transfer(self):
        self.victim.gold = self.victim.silver = 1
        with patch.object(self.commands, "_steal_succeeds", return_value=True):
            payload = self.attempt("gold Victim", rolls=(1, 1))
        self.assertEqual("You couldn't get any coins.\r\n", payload["to_char"])
        self.assertEqual((0, 0, 1, 1), (self.actor.gold, self.actor.silver, self.victim.gold, self.victim.silver))
        self.improve.assert_not_called()

    def test_reaction_payloads_reach_correct_recipients_through_real_emitter(self):
        replacements = {name: NS(**{attr: object}) for name, attr in (
            ("game.WizHandler", "WizHandler"), ("interp.CommandAccess", "CommandAccess"),
            ("interp.CommandExecutor", "CommandExecutor"), ("interp.commands.Info", "Info"),
            ("interp.commands.Movement", "Movement"), ("interp.commands.Communications", "Communications"),
            ("interp.commands.Fight", "Fight"), ("interp.commands.Wiz", "Wiz"),
            ("notes.NoteHandler", "NoteHandler"), ("server.messaging", "MessageBus"))}
        replacements["skill.Ability"] = NS(Ability=NS(take_improve_messages=lambda _entity: ""))
        with patch.dict(sys.modules, replacements):
            PlayerHandler = h._load_module("theft_player_handler", "player/PlayerHandler.py").PlayerHandler
        self.victim.is_npc = True
        self.victim.character_attributes.position = self.positions.POS_SLEEPING.value
        payload = self.attempt()
        emitter = PlayerHandler.__new__(PlayerHandler)
        emitter.message_bus = NS(send_to_character=AsyncMock(), send_to_room=AsyncMock(), text_to_message=lambda text: text)
        emitter.interp_api = self.commands.interp_api
        emitter._send_prompt = AsyncMock()
        # All I/O collaborators complete immediately; no platform event loop is needed.
        emission = emitter._emit_standard_payload(self.actor, payload, context=self.context())
        with self.assertRaises(StopIteration):
            emission.send(None)
        sent = emitter.message_bus.send_to_character.call_args_list
        self.assertIn(((self.actor.id, "Oops.\r\n"), {}), [(call.args, call.kwargs) for call in sent])
        self.assertTrue(any(call.args == (self.actor.id, "Retaliation!") for call in sent))
        self.assertFalse(any("You yell" in call.args[1] or "You wake" in call.args[1] for call in sent))
        self.assertTrue(any("Victim yells" in call.args[0] for call in emitter.message_bus.send_to_room.call_args_list))


if __name__ == "__main__":
    unittest.main()
