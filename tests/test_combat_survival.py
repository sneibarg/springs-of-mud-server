import asyncio
import importlib.util
import json
import sys
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from tests import test_combat_handler_aggression as fixtures


ROOT = Path(__file__).resolve().parents[1]
Runtime = sys.modules[fixtures.FightHandler.__module__]


def _load_components():
    replacements = {name: SimpleNamespace(**{attr: object}) for name, attr in (
        ("api.FightApi", "FightApi"), ("api.InterpApi", "InterpApi"), ("api.SkillApi", "SkillApi"),
        ("api.SpellApi", "SpellApi"), ("game.WeatherHandler", "WeatherHandler"),
        ("item.Effect", "Effect"), ("skill.SpellContext", "SpellContext"),
        ("util.MovementUtil", "MovementUtil"), ("util.PlayerUtil", "PlayerUtil"),
        ("util.MobileUtil", "MobileUtil"),
        ("game.HandlerService", "HandlerService"), ("server.session.SessionHandler", "SessionHandler"),
        ("server.connection.ConnectionManager", "ConnectionManager"))}
    replacements["combat.CombatHandler"] = SimpleNamespace(FightHandler=Runtime.FightHandler)
    replacements["api.MovementApi"] = SimpleNamespace(MovementApi=SimpleNamespace(
        flag_value=lambda enums, *names: next((int(getattr(getattr(enums, name, None), "value", 0))
                                             for name in names if getattr(enums, name, None) is not None), 0),
        has_flag=lambda flags, bit: bool(flags & bit)))
    replacements["player.CharacterAdvancement"] = SimpleNamespace(
        CharacterAdvancement=SimpleNamespace(gain_experience=Mock()))
    with patch.dict(sys.modules, replacements):
        loaded = {}
        for name, path in (
            ("game.Equipped", "game/Equipped.py"),
            ("player.CharacterAttributes", "player/CharacterAttributes.py"),
            ("game.AnimateEntity", "game/AnimateEntity.py"),
            ("interp.Context", "interp/Context.py"),
            ("util.PayloadUtil", "util/PayloadUtil.py"),
            ("interp.commands.Fight", "interp/commands/Fight.py"),
            ("interp.commands.Movement", "interp/commands/Movement.py"),
            ("combat.CombatEscapeHandler", "combat/CombatEscapeHandler.py"),
        ):
            spec = importlib.util.spec_from_file_location(name, ROOT / "src" / path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)
            loaded[name] = module
    return loaded


Components = _load_components()
EscapeHandler = Components["combat.CombatEscapeHandler"].CombatEscapeHandler
AnimateEntity = Components["game.AnimateEntity"].AnimateEntity
Equipped = Components["game.Equipped"].Equipped


class TestCombatSurvival(unittest.TestCase):
    def setUp(self):
        self.fixtures = fixtures.TestFightHandlerAggression()

    def test_corpse_transfer_detaches_inventory_equipment_and_floating_items_once(self):
        for player in (False, True):
            with self.subTest(player=player):
                entity = AnimateEntity.__new__(AnimateEntity)
                entity.lock = threading.RLock()
                entity.inventory = []
                if player:
                    entity.loot = []
                carried = SimpleNamespace(name="carried", item_type="weapon")
                worn = SimpleNamespace(name="worn", item_type="armor", wear_location="WEAR_BODY")
                floating = SimpleNamespace(name="floating", item_type="light", wear_location="WEAR_FLOAT")
                entity.equipped = Equipped(torso=worn, floating_nearby=floating)
                entity.add_item(carried)
                entity.add_item(worn)  # a legacy duplicate inventory/equipment reference
                corpse = SimpleNamespace(contains=[])
                room = SimpleNamespace(add_item_to_room=Mock())
                handler = self.fixtures._handler(room)
                handler.effect_handler.remove_item_effects = Mock()

                handler._transfer_victim_property(corpse, room, entity)

                self.assertEqual([], entity.owned_items())
                self.assertEqual([], entity._item_collection())
                self.assertIsNone(entity.equipped.torso)
                self.assertIsNone(entity.equipped.floating_nearby)
                self.assertEqual([carried, worn], corpse.contains)
                room.add_item_to_room.assert_called_once_with(floating)
                self.assertEqual(2, handler.effect_handler.remove_item_effects.call_count)
                self.assertEqual("", floating.wear_location)

    def test_immortal_survival_uses_actual_player_level_before_death_processing(self):
        threshold = Runtime.CharacterApi.GameParameters.LEVEL_IMMORTAL.value
        for npc, level, survives in ((False, threshold, True), (False, threshold + 1, True),
                                     (False, threshold - 1, False), (True, threshold + 1, False)):
            with self.subTest(npc=npc, level=level):
                attacker = self.fixtures._mob("attacker")
                victim = self.fixtures._mob("victim") if npc else self.fixtures._player("victim")
                victim.level, victim.hit, victim.is_immortal = level, 1, True
                victim.status_flags.drunk = 0
                room = self.fixtures._safety_room(attacker, victim)
                handler = self.fixtures._damage_handler(room)
                handler.AffectBits = SimpleNamespace(AFF_CHARM=SimpleNamespace(value=2),
                                                     AFF_SANCTUARY=4, AFF_PROTECT_EVIL=8, AFF_PROTECT_GOOD=16)
                handler.group_gain = Mock(return_value={"xp_gain": 0, "reward_payloads": []})
                with patch.object(Runtime.CharacterApi, "is_affected", return_value=False):
                    result = handler.damage(attacker, victim, 13)
                self.assertEqual(not survives, result["killed"])
                self.assertEqual(not survives, handler.raw_kill.called)
                self.assertEqual(not survives, handler.group_gain.called)
                if survives:
                    self.assertEqual(1, victim.hit)

    def _escape(self, *, npc=False, connected=True):
        self.attacker = self.fixtures._player("attacker")
        self.victim = self.fixtures._mob("victim") if npc else self.fixtures._player("victim")
        self.victim.name = "Victim"
        self.victim.hit, self.victim.max_hit = 20, 100
        self.victim.movement = 20
        self.victim.character_attributes.wimpy = 20
        self.victim.status_flags.pulse_wait = 0
        self.room = self.fixtures._safety_room(self.attacker, self.victim)
        self.room.id, self.room.area_id = "room-1", "area-1"
        self.registry = SimpleNamespace(room_registry=SimpleNamespace(get_or_none=Mock(return_value=self.room)),
                                        interp_registry=SimpleNamespace(get_or_none=Mock(side_effect=lambda **kw: SimpleNamespace(name=kw["name"]))))
        self.fight = SimpleNamespace(do_flee=Mock(return_value={"to_char": "flee"}))
        self.movement = SimpleNamespace(do_recall=Mock(return_value={"to_char": "recall"}))
        self.player_handler = SimpleNamespace(_emit_standard_payload=AsyncMock(return_value=[]))
        sessions = SimpleNamespace(get_session_by_character=Mock(return_value=SimpleNamespace(character=self.victim)))
        self.connection = SimpleNamespace(is_closed=Mock(return_value=False)) if connected else None
        connections = SimpleNamespace(get_connection_by_character=Mock(return_value=self.connection))
        self.enums = {"actBits": fixtures._ActBits, "affectedBy": fixtures._AffectBits,
                      "gameParameters": SimpleNamespace(PULSE_VIOLENCE=SimpleNamespace(value=12))}
        handler = EscapeHandler(self.fight, self.movement, self.registry,
                               SimpleNamespace(player_handler=self.player_handler), sessions, connections,
                               SimpleNamespace(get=self.enums.get))
        handler.rng = Mock(number_range=Mock(return_value=0), number_bits=Mock(return_value=0))
        return handler

    def test_player_wimpy_threshold_and_wait_boundary(self):
        for hit, wait, expected in ((20, 5, True), (21, 5, False), (20, 6, False), (0, 0, False)):
            with self.subTest(hit=hit, wait=wait):
                handler = self._escape()
                self.victim.hit, self.victim.status_flags.pulse_wait = hit, wait
                result = handler.after_damage(self.attacker, self.victim, 1)
                self.assertEqual(expected, self.fight.do_flee.called)
                if expected:
                    self.assertIs(result[0]["actor"], self.victim)
                    self.assertEqual("flee", result[0]["context"].command.name)
                self.movement.do_recall.assert_not_called()

    def test_linkdead_recall_precedes_wimpy_even_at_high_wait_or_when_recall_fails(self):
        handler = self._escape(connected=False)
        self.victim.status_flags.pulse_wait = 100
        self.movement.do_recall.return_value = {}
        self.assertEqual([], handler.after_damage(self.attacker, self.victim, 1))
        handler.rng.number_range.assert_called_once_with(0, 100)
        self.movement.do_recall.assert_called_once()
        self.fight.do_flee.assert_not_called()

    def test_failed_linkdead_recall_roll_can_fall_through_to_player_flee(self):
        handler = self._escape(connected=False)
        self.victim.status_flags.pulse_wait = 4
        handler.rng.number_range.return_value = 1
        handler.after_damage(self.attacker, self.victim, 1)
        self.movement.do_recall.assert_not_called()
        self.fight.do_flee.assert_called_once()

    def test_closed_connection_and_switched_original_are_linkdead(self):
        for switched in (False, True):
            with self.subTest(switched=switched):
                handler = self._escape()
                if switched:
                    handler.session_handler.get_session_by_character.return_value.character = self.attacker
                else:
                    self.connection.is_closed.return_value = True
                handler.after_damage(self.attacker, self.victim, 1)
                self.movement.do_recall.assert_called_once()

    def test_npc_wimpy_requires_random_roll_strict_hp_threshold_and_low_wait(self):
        for hit, wait, roll, expected in ((19, 5, 0, True), (20, 5, 0, False),
                                         (19, 5, 1, False), (19, 6, 0, False)):
            with self.subTest(hit=hit, wait=wait, roll=roll):
                handler = self._escape(npc=True)
                self.victim.status_flags.act = int(fixtures._ActBits.ACT_WIMPY)
                self.victim.status_flags.pulse_wait, self.victim.hit = wait, hit
                handler.rng.number_bits.return_value = roll
                handler.after_damage(self.attacker, self.victim, 1)
                self.assertEqual(expected, self.fight.do_flee.called)
                handler.session_handler.get_session_by_character.assert_not_called()

    def test_separated_charmed_npc_flees_even_when_healthy(self):
        for separated, charmed, expected in ((True, True, True), (False, True, False), (True, False, False)):
            with self.subTest(separated=separated, charmed=charmed):
                handler = self._escape(npc=True)
                self.victim.hit = 99
                self.victim.status_flags.act = 0
                self.victim.status_flags.affected_by = int(fixtures._AffectBits.AFF_CHARM) if charmed else 0
                self.victim.master = SimpleNamespace(room_id="another" if separated else self.victim.room_id)
                handler.after_damage(self.attacker, self.victim, 1)
                self.assertEqual(expected, self.fight.do_flee.called)
                handler.rng.number_bits.assert_not_called()

    def test_self_damage_and_zero_damage_do_not_attempt_escape(self):
        handler = self._escape(connected=False)
        self.assertEqual([], handler.after_damage(self.victim, self.victim, 10))
        self.assertEqual([], handler.after_damage(self.attacker, self.victim, 0))
        self.fight.do_flee.assert_not_called()
        self.movement.do_recall.assert_not_called()
        handler.rng.number_range.assert_not_called()

    def test_real_flee_command_moves_before_returning_and_preserves_its_context(self):
        handler = self._escape()
        self.attacker.fighting, self.victim.fighting = self.victim, self.attacker
        destination = SimpleNamespace(id="room-2", area_id="area-2", add_player_to_room=Mock(),
                                      player_targets=lambda _actor: [])
        self.room.exits = [SimpleNamespace(direction=direction) for direction in range(6)]
        self.room.player_targets = lambda _actor: [self.attacker]
        self.room.remove_player_from_room = Mock()
        commands = Components["interp.commands.Fight"].Fight.__new__(Components["interp.commands.Fight"].Fight)
        commands.room_registry = self.registry.room_registry
        commands.interp_api = SimpleNamespace(evaluate_guards_only=Mock(return_value=None))
        commands._flee_destination = Mock(return_value=destination)
        commands._movement_cost = Mock(return_value=2)
        def stop(character, both):
            self.assertTrue(both)
            character.fighting = None
            self.attacker.fighting = None
        commands.fight_handler = SimpleNamespace(stop_fighting=Mock(side_effect=stop),
                                                 aggressive_entry_rounds=Mock(return_value=[]))
        handler.fight_commands = commands
        result = handler.after_damage(self.attacker, self.victim, 1)
        self.assertEqual("room-2", self.victim.room_id)
        self.assertEqual(18, self.victim.movement)
        self.assertIsNone(self.attacker.fighting)
        self.assertIsNone(self.victim.fighting)
        self.assertEqual("flee", result[0]["context"].command.name)
        self.assertIn("payloads", result[0]["payloads"][0])

    def test_real_recall_command_stops_fighting_and_updates_area(self):
        handler = self._escape(connected=False)
        temple = SimpleNamespace(id="temple", area_id="temple-area", add_player_to_room=Mock(),
                                 player_targets=lambda _actor: [])
        self.room.room_flags = 0
        self.room.player_targets = lambda _actor: []
        self.room.remove_player_from_room = Mock()
        commands = Components["interp.commands.Movement"].Movement.__new__(Components["interp.commands.Movement"].Movement)
        commands.room_registry = SimpleNamespace(get_or_none=Mock(return_value=temple))
        commands.room_flags = SimpleNamespace(ROOM_NO_RECALL=SimpleNamespace(value=1))
        commands.fight_handler = SimpleNamespace(stop_fighting=Mock(), aggressive_entry_rounds=Mock(return_value=[]))
        handler.movement_commands = commands
        result = handler.after_damage(self.attacker, self.victim, 1)
        self.assertEqual(("temple", "temple-area"), (self.victim.room_id, self.victim.area_id))
        commands.fight_handler.stop_fighting.assert_called_once_with(self.victim, both=True)
        self.assertEqual("recall", result[0]["context"].command.name)

    def test_world_action_emission_uses_the_escaping_actor_and_command_context(self):
        handler = self._escape()
        action = handler.after_damage(self.attacker, self.victim, 1)[0]
        prompted = asyncio.run(handler.emit(action))
        self.player_handler._emit_standard_payload.assert_awaited_once_with(
            self.victim, action, context=action["context"], prompt_victims=False)
        self.assertEqual([self.victim], prompted)

    def test_damage_escape_stops_later_swings_and_weapon_effects(self):
        attacker, victim, handler = self.fixtures._killer_pair()
        room = self.fixtures._safety_room(attacker, victim)
        room.id = "room-1"
        handler.room_registry.get = Mock(return_value=room)
        handler.is_safe = Mock(return_value=(False, ""))
        handler.check_killer = Mock(return_value={})
        handler._check_immunity = Mock(return_value="IS_NORMAL")
        handler.dam_message = Mock(return_value={"to_char": "hit"})
        handler._thac0 = Mock(return_value=0)
        handler._victim_ac_for_damage_type = Mock(return_value=0)
        handler._to_hit_roll = Mock(return_value=19)
        handler._attack_damage = Mock(return_value=1)
        handler.check_parry = Mock(return_value=False)
        handler.check_dodge = Mock(return_value=False)
        handler.check_shield_block = Mock(return_value=False)
        attacker.equipped = SimpleNamespace(wielded=SimpleNamespace(
            name="blade", item_type="weapon", value0=1, value3="stab"))
        attacker.fighting, victim.fighting = victim, attacker
        victim.hit, victim.status_flags.drunk = 100, 0
        action = {"actor": victim, "context": object(), "payloads": [{"to_char": "escaped"}]}
        def escape(*args):
            attacker.fighting = victim.fighting = None
            return [action]
        handler.escape_handler = SimpleNamespace(after_damage=Mock(side_effect=escape))
        handler.weapon_hit_handler = SimpleNamespace(apply=Mock())
        result = handler.multi_hit(attacker, victim)
        handler._attack_damage.assert_called_once()
        handler.weapon_hit_handler.apply.assert_not_called()
        self.assertEqual([action], result["post_damage_actions"])
        self.assertEqual(99, victim.hit)

    def test_escape_actions_survive_merges_and_spell_queue(self):
        from tests.test_weapon_hit_effects import WeaponHitHandler
        first, second = {"actor": "first"}, {"actor": "second"}
        for merge in (Runtime.FightHandler._merge_attack_payloads, WeaponHitHandler._merge):
            result = merge({"post_damage_actions": [first]}, {"post_damage_actions": [second]})
            self.assertEqual([first, second], result["post_damage_actions"])
        spell_api = self.fixtures._spell_api_class()(effect_handler=Mock(), interp_api=Mock())
        spell_api.send = Mock()
        context = SimpleNamespace(queue_payload=Mock())
        spell_api._queue_damage_payload(context, {"post_damage_actions": [first, second]}, None)
        self.assertEqual([first, second], [call.args[0] for call in context.queue_payload.call_args_list])

    def test_standard_emission_retains_escape_context_and_skips_npc_socket(self):
        replacements = {name: SimpleNamespace(**{attr: object}) for name, attr in (
            ("api.InterpApi", "InterpApi"), ("interp.CommandAccess", "CommandAccess"),
            ("interp.CommandExecutor", "CommandExecutor"), ("interp.commands.Info", "Info"),
            ("interp.commands.Movement", "Movement"), ("interp.commands.Fight", "Fight"),
            ("interp.commands.Communications", "Communications"), ("interp.commands.Object", "Object"),
            ("interp.commands.Wiz", "Wiz"), ("notes.NoteHandler", "NoteHandler"),
            ("util.PlayerUtil", "PlayerUtil"))}
        replacements["combat.CombatHandler"] = SimpleNamespace(FightHandler=Runtime.FightHandler)
        replacements["skill.Ability"] = SimpleNamespace(Ability=SimpleNamespace(take_improve_messages=lambda _entity: ""))
        with patch.dict(sys.modules, replacements):
            spec = importlib.util.spec_from_file_location("_survival_player_handler", ROOT / "src/player/PlayerHandler.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        for npc in (False, True):
            handler = self._escape(npc=npc)
            emitter = module.PlayerHandler.__new__(module.PlayerHandler)
            emitter.message_bus = SimpleNamespace(send_to_character=AsyncMock(), text_to_message=lambda text: text)
            emitter._resolve_standard_payload = Mock(return_value={"to_char": "escaped"})
            context = SimpleNamespace(command=SimpleNamespace(name="flee"))
            action = {"actor": self.victim, "context": context, "payloads": [{"to_char": "key"}]}
            asyncio.run(emitter._emit_standard_payload(self.attacker, action))
            emitter._resolve_standard_payload.assert_called_once_with(self.victim, {"to_char": "key"}, context=context)
            if npc:
                emitter.message_bus.send_to_character.assert_not_awaited()
            else:
                emitter.message_bus.send_to_character.assert_awaited_once_with(self.victim.id, "escaped")


if __name__ == "__main__":
    unittest.main()
