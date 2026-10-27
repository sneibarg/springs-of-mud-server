import importlib.util
import ast
import json
import re
import sys
import types
import unittest
from enum import IntEnum
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def _module(name: str, **attrs):
    module = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    return module


from item.ItemFactory import ItemFactory

class _CharacterApi:
    @staticmethod
    def is_npc(entity):
        return bool(getattr(entity, "is_npc", False))

    @staticmethod
    def is_same_group(left, right):
        return (getattr(left, 'leader', None) or left) is (getattr(right, 'leader', None) or right)


class _Item:
    @staticmethod
    def short(item):
        return str(getattr(item, "short_description", "") or getattr(item, "name", "something"))


class _Logger:
    def error(self, *_args, **_kwargs):
        return None


class _LoggerFactory:
    @staticmethod
    def get_logger(_name):
        return _Logger()


def _load_spell_api():
    module_name = "_test_spell_api_module"
    replacements = {
        "api": _module("api"),
        "api.GameApi": _module("api.GameApi", GameApi=SimpleNamespace()),
        "api.CharacterApi": _module("api.CharacterApi", CharacterApi=_CharacterApi),
        "api.InterpApi": _module("api.InterpApi", InterpApi=object),
        "item.EffectHandler": _module("item.EffectHandler", EffectHandler=object),
        "item.Item": _module("item.Item", Item=_Item),
        "item.Effect": _module("item.Effect", Effect=object),
        "util": _module("util"),
        "util.ElementalExposure": _module("util.ElementalExposure", ElementalExposure=object),
        "util.DisplayUtil": _module(
            "util.DisplayUtil",
            DisplayUtil=SimpleNamespace(
                display_effect_message=lambda message: str(message or "").strip(),
                entity_name=lambda entity, is_npc: str(getattr(entity, "name", "someone") or "someone"),
                room_text=lambda text, render, room: text,
            ),
        ),
        "util.GenericUtil": _module(
            "util.GenericUtil",
            GenericUtil=SimpleNamespace(
                camel_to_snake_case=lambda dictionary: _camel_to_snake_case(dictionary),
                to_int=lambda value, default=0: int(value or default),
                trunc_div=lambda a, b: (abs(a) // abs(b)) * (-1 if (a < 0) != (b < 0) else 1),
            ),
        ),
        "util.FightUtil": _module("util.FightUtil", FightUtil=SimpleNamespace(spell_handler_name=lambda name: f"spell.{name.replace(' ', '_')}")),
        "util.EffectUtil": _module("util.EffectUtil", EffectUtil=SimpleNamespace(handler=lambda: Mock())),
        "util.ItemUtil": _module("util.ItemUtil", ItemUtil=SimpleNamespace()),
        "util.PlayerUtil": _module("util.PlayerUtil", PlayerUtil=SimpleNamespace()),
        "server.LoggerFactory": _module("server.LoggerFactory", LoggerFactory=_LoggerFactory),
        "skill.SpellContext": _module("skill.SpellContext", SpellContext=object),
        "skill.SpellSpeech": _module("skill.SpellSpeech", SpellSpeech=SimpleNamespace(utterance=lambda *_args, **_kwargs: "")),
        "skill.Ability": _module("skill.Ability", Ability=SimpleNamespace(check_improve=Mock())),
    }
    originals = {name: sys.modules.get(name) for name in replacements}
    try:
        sys.modules.update(replacements)
        spec = importlib.util.spec_from_file_location(module_name, SRC / "api" / "SpellApi.py")
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module.SpellApi
    finally:
        sys.modules.pop(module_name, None)
        for name, original in originals.items():
            if original is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = original


SpellApi = _load_spell_api()


def _camel_to_snake_case(dictionary):
    def convert(key: str) -> str:
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", str(key))
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    return {convert(key): value for key, value in (dictionary or {}).items()}


def _load_spell_class():
    replacements = {
        "api.CharacterApi": _module("api.CharacterApi", CharacterApi=_CharacterApi),
        "game.RandomNumberGenerator": _module("game.RandomNumberGenerator", RandomNumberGenerator=lambda: SimpleNamespace()),
        "player.Character": _module("player.Character", Character=object),
        "player.CharacterAdvancement": _module("player.CharacterAdvancement", CharacterAdvancement=object),
        "server.LoggerFactory": _module("server.LoggerFactory", LoggerFactory=_LoggerFactory),
        "util.GenericUtil": _module(
            "util.GenericUtil",
            GenericUtil=SimpleNamespace(camel_to_snake_case=_camel_to_snake_case, to_int=lambda value, default=0: int(value or default)),
        ),
        "item.Effect": _module("item.Effect", Effect=SimpleNamespace(from_json=lambda value: value)),
    }
    originals = {name: sys.modules.get(name) for name in replacements}
    loaded = []
    try:
        sys.modules.update(replacements)
        for name, relative in [
            ("game.GamePayload", "game/GamePayload.py"),
            ("skill.Ability", "skill/Ability.py"),
            ("skill.Spell", "skill/Spell.py"),
        ]:
            spec = importlib.util.spec_from_file_location(name, SRC / relative)
            module = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            sys.modules[name] = module
            loaded.append(name)
            spec.loader.exec_module(module)
        return sys.modules["skill.Spell"].Spell
    finally:
        for name in loaded:
            sys.modules.pop(name, None)
        for name, original in originals.items():
            if original is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = original


Spell = _load_spell_class()


class _Spell:
    name = "haste"


class TestSpellAffectPayloadMessages(unittest.TestCase):
    def test_announcement_preserves_earlier_killer_notices(self):
        notice = {"to_wiznet": "notice"}
        payloads = [notice]
        ctx = SimpleNamespace(actor=SimpleNamespace(id="actor", name="Caster"), victim=None,
                              spell=SimpleNamespace(name="blindness"), room=SimpleNamespace(characters={}),
                              payloads=payloads, queue_payload=payloads.append, is_player_source=True)
        api = SpellApi(Mock(), Mock())
        api.queue_cast_announcement(ctx)
        self.assertIs(notice, payloads[0])
        self.assertEqual("You cast blindness.\r\n", payloads[1]["to_char"])

    def test_retaliation_checks_current_room_followers_and_existing_combat(self):
        for reason in ("eligible", "follower", "self", "busy", "departed", "caster_moved", "defensive", "object"):
            with self.subTest(reason=reason):
                actor = SimpleNamespace(id="actor", room_id="room")
                victim = SimpleNamespace(id="victim", master=actor if reason == "follower" else None,
                                         fighting=actor if reason == "busy" else None)
                if reason == "self":
                    victim = actor
                if reason == "object":
                    victim = None  # SpellContext.victim excludes object targets.
                room = SimpleNamespace(id="room", characters={"actor": actor}, mobiles={})
                if victim is not None and reason != "departed":
                    room.characters["victim"] = victim
                if reason == "caster_moved":
                    actor.room_id = "elsewhere"
                fight = Mock()
                fight.check_killer.return_value = {"to_char": "notice"}
                fight.multi_hit.return_value = {"hit": True}
                fight.build_round_payload.return_value = {"to_char": "attack"}
                ctx = SimpleNamespace(actor=actor, victim=victim, room=room,
                                      spell=SimpleNamespace(target="CHAR_DEFENSIVE" if reason == "defensive" else "OBJ_CHAR_OFF"),
                                      queue_payload=Mock())
                api = SpellApi(Mock(), Mock())
                api._fight_handler = Mock(return_value=fight)
                api._find_room_for_entity = Mock(return_value=SimpleNamespace(id="elsewhere", characters={}, mobiles={}))
                api.start_offensive_combat(ctx)
                fight.set_fighting.assert_not_called()
                if reason == "eligible":
                    fight.check_killer.assert_called_once_with(victim, actor)
                    fight.multi_hit.assert_called_once_with(victim, actor, dt="TYPE_UNDEFINED")
                    ctx.queue_payload.assert_called_once_with({"actor": victim, "payloads": [
                        {"to_char": "notice"}, {"to_char": "attack"}]})
                else:
                    fight.check_killer.assert_not_called()
                    fight.multi_hit.assert_not_called()

    def test_offensive_caster_is_marked_before_announcement_and_concentration(self):
        actor = SimpleNamespace(is_npc=False, mana=100, status_flags=SimpleNamespace(pulse_wait=0))
        victim = object()
        fight = SimpleNamespace(check_killer=Mock(return_value={"to_wiznet": "notice"}))
        spell = SimpleNamespace(id="spell", beats=12, target="CHAR_OFFENSIVE")
        events = []
        ctx = SimpleNamespace(actor=actor, victim=victim, spell=spell,
                              handler=SimpleNamespace(fight_handler=fight),
                              command_context=object(), queue_payload=lambda payload: events.append(payload))
        api = SpellApi(Mock(), Mock())
        api.queue_cast_announcement = Mock(side_effect=lambda c: events.append("announce"))
        api.interp_api.render_message_key.return_value = {"to_char": "failure"}
        with patch.object(api, "casting_proficiency", return_value=0), \
             patch.object(SpellApi.cast.__globals__["random"], "randint", return_value=100), \
             patch.object(SpellApi.cast.__globals__["Ability"], "check_improve"):
            api.check_offensive_cast(ctx)
            self.assertFalse(api.cast(ctx, 10))
        fight.check_killer.assert_called_once_with(actor, victim)
        self.assertEqual([{"to_wiznet": "notice"}, "announce", {"to_char": "failure"}], events)
        self.assertEqual(95, actor.mana)

    def test_collection_join_option_reaches_effect_handler_with_effective_level(self):
        actor, victim, spell = object(), object(), object()
        for cast_level in (None, 18):
            with self.subTest(cast_level=cast_level):
                ctx = SimpleNamespace(actor=actor, target=victim, spell=spell,
                                      cast_level=cast_level, level=18,
                                      mark_performed=Mock(return_value=True))
                api = SpellApi(Mock(), Mock())
                api._queue_apply_affect_messages = Mock()
                self.assertTrue(api.apply_affect_data(ctx, join=True))
                options = {"join": True}
                if cast_level is not None:
                    options["caster_level"] = 18
                api.effect_handler.apply_spell_effects.assert_called_once_with(actor, victim, spell, **options)
                api._queue_apply_affect_messages.assert_called_once_with(ctx, victim)

    def test_immune_blindness_stops_collection_lambdas_before_applying_effect(self):
        from tests.test_effect_util_affects import EffectUtil as SaveUtil

        documents = json.loads((ROOT / "resources/collections/SOMDB.Spells.json").read_text(encoding="utf-8"))
        document = next(d for d in documents if d["name"] == "blindness")
        fight = SimpleNamespace(_check_immunity=Mock(return_value="IS_IMMUNE"))
        victim = SimpleNamespace(level=10, saving_throw=0)
        ctx = SimpleNamespace(spell=SimpleNamespace(name="blindness", lambdas=document["lambdas"]),
                              actor=object(), victim=victim, level=10, done=False, performed=False,
                              handler=SimpleNamespace(fight_handler=fight), resolve=lambda value: value)
        ctx.stop = Mock(side_effect=lambda: setattr(ctx, "done", True))
        api = SpellApi(Mock(), Mock())
        api.stop_if_affected = Mock(return_value=False)
        api.apply_affect_data = Mock()
        ctx.stop_if_affected = lambda *args: api.stop_if_affected(ctx, *args)
        ctx.stop_if_saved = lambda *args, **kwargs: api.stop_if_saved(ctx, *args, **kwargs)
        ctx.apply_affect_data = lambda: api.apply_affect_data(ctx)
        char_api = SimpleNamespace(get_enum=lambda _: None, is_affected_by_name=lambda *_: False,
                                   is_npc=lambda _: False)
        with patch.dict(SpellApi.saves_spell.__globals__, EffectUtil=SaveUtil), \
             patch.dict(SaveUtil.saves_spell.__globals__, CharacterApi=char_api), \
             patch.object(SaveUtil.saves_spell.__globals__["random"], "randint") as rng:
            self.assertFalse(api.execute_lambdas(ctx))
            rng.assert_not_called()
        fight._check_immunity.assert_called_once_with(victim, "DAM_OTHER")
        api.apply_affect_data.assert_not_called()
        ctx.stop.assert_called_once()

    def test_damage_saves_receive_actual_type_target_level_and_immunity(self):
        victim = SimpleNamespace()
        fight = SimpleNamespace(_check_immunity=Mock(), damage=Mock(return_value={}),
                                is_safe_spell=Mock(return_value=False))
        ctx = SimpleNamespace(actor=object(), victim=victim, target=victim, level=20,
                              spell=SimpleNamespace(name="test", noun_damage="test"), room=object(),
                              handler=SimpleNamespace(fight_handler=fight),
                              resolve=lambda value: value, mark_performed=Mock(return_value=True))
        api = SpellApi(Mock(), Mock())
        api.eval_int = Mock(return_value=80)
        api._queue_damage_payload = Mock()
        api._room_entities = Mock(return_value=[victim])
        for kind in ("DAM_FIRE", "DAM_COLD", "DAM_ACID", "DAM_LIGHTNING", "DAM_ENERGY", "DAM_HARM", "DAM_HOLY"):
            with self.subTest(kind=kind), \
                 patch.object(SpellApi.saves_spell.__globals__["EffectUtil"], "saves_spell", return_value=True, create=True) as save:
                api.damage_expr(ctx, "80", kind, save_level_adjust=-2)
                save.assert_called_once_with(18, victim, kind, immunity=fight._check_immunity)
                self.assertEqual(40, fight.damage.call_args.args[2])
                save.reset_mock()
                api.damage_room_expr(ctx, "80", kind)
                save.assert_called_once_with(20, victim, kind, immunity=fight._check_immunity)
                self.assertEqual(40, fight.damage.call_args.args[2])
                save.reset_mock()
                api.damage_expr(ctx, "80", kind, save_half=False)
                save.assert_not_called()
                self.assertEqual(80, fight.damage.call_args.args[2])

    def test_typed_save_gate_preserves_alias_level_and_message(self):
        victim = object()
        fight = SimpleNamespace(_check_immunity=Mock())
        ctx = SimpleNamespace(victim=object(), level=20,
                              handler=SimpleNamespace(fight_handler=fight),
                              resolve=lambda alias: victim if alias == "secondary" else alias,
                              fail=Mock(), stop=Mock())
        api = SpellApi(Mock(), Mock())
        with patch.object(SpellApi.saves_spell.__globals__["EffectUtil"], "saves_spell", return_value=True, create=True) as save:
            self.assertTrue(api.stop_if_saved(ctx, -4, target="secondary", message="Saved!", dam_type="DAM_CHARM"))
            save.assert_called_once_with(16, victim, "DAM_CHARM", immunity=fight._check_immunity)
        ctx.fail.assert_called_once_with("Saved!")
        ctx.stop.assert_not_called()

    def test_effect_operations_preserve_effective_cast_level(self):
        actor = SimpleNamespace(is_npc=False, level=24)
        victim = SimpleNamespace(is_npc=False, level=1, fighting=None, leader=actor)
        spell = SimpleNamespace()
        room = SimpleNamespace()
        ctx = SimpleNamespace(actor=actor, victim=victim, target=victim, spell=spell,
                              room=room, level=18, cast_level=18,
                              mark_performed=lambda: True)
        api = SpellApi(Mock(), Mock())
        api._queue_apply_affect_messages = Mock()
        api._room_entities = Mock(return_value=[actor, victim])
        api._room_combatants = Mock(return_value=[victim])
        api._effect_active = Mock(return_value=False)
        api.send = Mock()
        api.saves_spell = Mock(return_value=False)
        for operation in ("apply_affect_data",):
            with self.subTest(operation=operation), \
                 patch.object(SpellApi.cast.__globals__["random"], "randint", return_value=0):
                api.effect_handler.reset_mock()
                self.assertTrue(getattr(api, operation)(ctx))
                calls = api.effect_handler.apply_spell_effects.call_args_list
                self.assertTrue(calls)
                self.assertTrue(all(call.kwargs == {"caster_level": 18} for call in calls))

    def test_casting_proficiency_uses_spells_and_rom_condition_penalties(self):
        for level, learned, daze, drunk, npc, expected in [
            (20, 100, 0, 10, False, 100), (20, 1, 0, 0, False, 1),
            (20, 99, 1, 11, False, 44), (9, 100, 0, 0, False, 0),
            (20, 0, 0, 0, False, 0), (50, 0, 1, 99, True, 70),
        ]:
            with self.subTest(level=level, learned=learned, daze=daze, drunk=drunk, npc=npc):
                actor = SimpleNamespace(level=level, is_npc=npc,
                                        status_flags=SimpleNamespace(pulse_daze=daze, drunk=drunk),
                                        get_learned=Mock(return_value=learned),
                                        learned_entry_level=Mock(return_value=learned))
                spell = SimpleNamespace(name="armor")
                with patch.object(SpellApi.casting_proficiency.__globals__["FightUtil"],
                                  "level_for_class", return_value=10, create=True):
                    self.assertEqual(expected, SpellApi.casting_proficiency(actor, spell))
                if npc or level < 10:
                    actor.get_learned.assert_not_called()
                else:
                    actor.get_learned.assert_called_once_with("armor", collection_name="spells")

    def test_cast_attempt_charges_and_improves_independently_of_spell_effect(self):
        for roll, mana_gain, npc, expected_cost, expected_level in [
            (51, True, False, 16, None),
            (50, True, False, 33, 22),
            (1, False, False, 33, 16),
            (1, False, True, 33, 22),
        ]:
            with self.subTest(roll=roll, mana_gain=mana_gain, npc=npc):
                events = []
                actor = SimpleNamespace(level=22, mana=100, is_npc=npc,
                                        character_class=SimpleNamespace(mana_gain=mana_gain),
                                        status_flags=SimpleNamespace(pulse_wait=0))
                spell = SimpleNamespace(id="spell-id", beats=12)
                ctx = SimpleNamespace(actor=actor, spell=spell, cast_level=None, performed=False,
                                      command_context=object(), queue_payload=lambda p: events.append(p))
                api = SpellApi(Mock(), Mock())
                api.interp_api.render_message_key.return_value = {"to_char": "concentration failure"}
                api.queue_cast_announcement = Mock(side_effect=lambda c: events.append("announcement"))

                def execute(c):
                    # A save, duplicate or missing component returns without performing.
                    self.assertEqual(67, c.actor.mana)
                    self.assertEqual(expected_level, c.cast_level)
                    self.assertEqual(12, c.actor.status_flags.pulse_wait)
                    self.assertEqual(["announcement"], events)
                    return False

                api.execute_lambdas = Mock(side_effect=execute)
                ability = SpellApi.cast.__globals__["Ability"]
                rng = SpellApi.cast.__globals__["random"]
                with patch.object(api, "casting_proficiency", return_value=50), \
                     patch.object(rng, "randint", return_value=roll), \
                     patch.object(ability, "check_improve") as improve:
                    self.assertEqual(roll <= 50, api.cast(ctx, 33))
                    improve.assert_called_once_with(actor, "spell-id", roll <= 50, 1)
                self.assertEqual(100 - expected_cost, actor.mana)
                self.assertEqual(12, actor.status_flags.pulse_wait)
                if roll > 50:
                    api.execute_lambdas.assert_not_called()
                    api.interp_api.render_message_key.assert_called_once_with(ctx.command_context, "skill_failure")
                    self.assertEqual(["announcement", {"to_char": "concentration failure"}], events)
                else:
                    api.execute_lambdas.assert_called_once_with(ctx)
                    api.interp_api.render_message_key.assert_not_called()

    def test_cast_preserves_longer_wait_and_explicit_cast_level(self):
        actor = SimpleNamespace(mana=100, status_flags=SimpleNamespace(pulse_wait=24))
        ctx = SimpleNamespace(actor=actor, spell=SimpleNamespace(id="spell-id", beats=12), cast_level=7)
        api = SpellApi(Mock(), Mock())
        api.queue_cast_announcement = Mock()
        api.execute_lambdas = Mock()
        with patch.object(api, "casting_proficiency", return_value=100), \
             patch.object(SpellApi.cast.__globals__["random"], "randint", return_value=100), \
             patch.object(SpellApi.cast.__globals__["Ability"], "check_improve"):
            self.assertTrue(api.cast(ctx, 5))
        self.assertEqual(24, actor.status_flags.pulse_wait)
        self.assertEqual(7, ctx.cast_level)

    def test_apply_affect_data_queues_spell_payload_messages(self):
        actor = SimpleNamespace(id="caster", name="Caster")
        victim = SimpleNamespace(id="target", name="Target")
        observer = SimpleNamespace(id="observer", name="Observer")
        room = SimpleNamespace(characters={actor.id: actor, victim.id: victim, observer.id: observer})
        payloads = []
        ctx = SimpleNamespace(
            actor=actor,
            target=victim,
            victim=victim,
            room=room,
            spell=_Spell(),
            is_player_source=True,
            is_object_target=lambda: False,
            resolve=lambda value: value,
            queue_payload=payloads.append,
            mark_performed=lambda: True,
        )
        effect_handler = Mock()
        interp_api = Mock()
        interp_api.evaluate_guards_only.return_value = {
            "blocked": True,
            "blocked_key": "apply",
            "to_char": "Ok.\r\n",
            "to_victim": "You feel yourself moving more quickly.\r\n",
            "to_room": "Target is moving more quickly.\r\n",
        }

        self.assertTrue(SpellApi(effect_handler=effect_handler, interp_api=interp_api).apply_affect_data(ctx))

        effect_handler.apply_spell_effects.assert_called_once_with(actor, victim, ctx.spell)
        interp_api.evaluate_guards_only.assert_called_once_with(ctx, "haste")
        self.assertEqual(
            [
                {
                    "to_char": "Ok.\r\n",
                    "victim": victim,
                    "to_victim": "You feel yourself moving more quickly.\r\n",
                    "to_room": "Target is moving more quickly.\r\n",
                    "targets": [observer],
                }
            ],
            payloads,
        )

    def test_apply_affect_data_prefers_victim_message_for_self_target(self):
        actor = SimpleNamespace(id="caster", name="Caster")
        room = SimpleNamespace(characters={actor.id: actor})
        payloads = []
        ctx = SimpleNamespace(
            actor=actor,
            target=actor,
            victim=actor,
            room=room,
            spell=_Spell(),
            is_player_source=True,
            is_object_target=lambda: False,
            resolve=lambda value: value,
            queue_payload=payloads.append,
            mark_performed=lambda: True,
        )
        effect_handler = Mock()
        interp_api = Mock()
        interp_api.evaluate_guards_only.return_value = {
            "blocked": True,
            "blocked_key": "apply",
            "to_char": "Ok.\r\n",
            "to_victim": "You feel yourself moving more quickly.\r\n",
        }

        self.assertTrue(SpellApi(effect_handler=effect_handler, interp_api=interp_api).apply_affect_data(ctx))

        self.assertEqual([{"to_char": "You feel yourself moving more quickly.\r\n"}], payloads)

    def test_stop_if_affected_uses_other_target_message_key(self):
        actor = SimpleNamespace(id="caster", name="Caster")
        victim = SimpleNamespace(id="target", name="Janky", effects=[SimpleNamespace(type="spell.haste")])
        payloads = []
        ctx = SimpleNamespace(
            actor=actor,
            target=victim,
            spell=SimpleNamespace(name="haste"),
            payload_tokens=lambda: {"victim": "Janky"},
            resolve=lambda value: value,
            fail=lambda text: payloads.append({"to_char": text}) or False,
        )
        interp_api = Mock()
        interp_api.render_message_key.return_value = {"to_char": "Janky is already moving as fast as they can.\r\n"}

        self.assertTrue(
            SpellApi(effect_handler=Mock(), interp_api=interp_api).stop_if_affected(
                ctx,
                "spell.haste",
                "alreadyAffected",
                "alreadyAffectedOther",
            )
        )

        interp_api.render_message_key.assert_called_once_with(
            ctx,
            "already_affected_other",
            channel="to_char",
            victim="Janky",
        )
        self.assertEqual([{"to_char": "Janky is already moving as fast as they can.\r\n"}], payloads)

    def test_stop_if_affected_uses_self_message_key_for_self_target(self):
        actor = SimpleNamespace(id="caster", name="Caster", effects=[SimpleNamespace(type="spell.haste")])
        payloads = []
        ctx = SimpleNamespace(
            actor=actor,
            target=actor,
            spell=SimpleNamespace(name="haste"),
            payload_tokens=lambda: {"victim": "Caster"},
            resolve=lambda value: value,
            fail=lambda text: payloads.append({"to_char": text}) or False,
        )
        interp_api = Mock()
        interp_api.render_message_key.return_value = {"to_char": "You can't move any faster!\r\n"}

        self.assertTrue(
            SpellApi(effect_handler=Mock(), interp_api=interp_api).stop_if_affected(
                ctx,
                "spell.haste",
                "alreadyAffected",
                "alreadyAffectedOther",
            )
        )

        interp_api.render_message_key.assert_called_once_with(
            ctx,
            "already_affected",
            channel="to_char",
            victim="Caster",
        )
        self.assertEqual([{"to_char": "You can't move any faster!\r\n"}], payloads)

    def test_dispel_effects_queues_each_removed_effect_msg_off_for_victim(self):
        actor = SimpleNamespace(id="caster", name="Caster")
        victim = SimpleNamespace(id="target", name="Target")
        haste = SimpleNamespace(
            handler_id="spell.haste",
            name="haste",
            id="haste-id",
            message=lambda channel, key, **_tokens: "You feel yourself slow down." if (channel, key) == ("to_char", "msg_off") else "",
        )
        giant_strength = SimpleNamespace(
            handler_id="spell.giant_strength",
            name="giant strength",
            id="giant-id",
            message=lambda channel, key, **_tokens: "You feel weaker." if (channel, key) == ("to_char", "msg_off") else "",
        )
        payloads = []
        ctx = SimpleNamespace(
            actor=actor,
            target=victim,
            victim=victim,
            level=50,
            handler=SimpleNamespace(spell_registry=SimpleNamespace(all_spells=lambda: [haste, giant_strength])),
            payload_tokens=lambda: {"victim": "Target"},
            queue_payload=payloads.append,
            mark_performed=lambda: True,
        )
        effect_handler = Mock()
        effect_handler.dispel_effects.side_effect = lambda _level, _victim, effect_name: {
            "spell.haste": [SimpleNamespace(type="spell.haste"), SimpleNamespace(type="spell.haste")],
            "spell.giant_strength": [SimpleNamespace(type="spell.giant_strength")],
        }.get(effect_name, [])

        self.assertTrue(SpellApi(effect_handler=effect_handler, interp_api=Mock()).dispel_effects(ctx, "spell.giant_strength", "spell.haste"))

        self.assertEqual(
            [
                {"victim": victim, "to_victim": "You feel weaker.\r\n"},
                {"victim": victim, "to_victim": "You feel yourself slow down.\r\n"},
            ],
            payloads,
        )

    def test_selected_spell_records_define_apply_payloads(self):
        spells = json.loads((ROOT / "resources" / "collections" / "SOMDB.Spells.json").read_text())
        by_name = {spell["name"]: spell for spell in spells}

        for name in ("armor", "bless", "giant strength", "haste", "shield"):
            payload = by_name[name].get("payload", {})
            self.assertTrue(payload, name)

        self.assertEqual("You feel yourself moving more quickly.\r\n", by_name["haste"]["payload"]["toVictim"]["apply"])
        self.assertEqual("{victim} is moving more quickly.\r\n", by_name["haste"]["payload"]["toRoom"]["apply"])
        self.assertEqual("You can't move any faster!", by_name["haste"]["payload"]["toChar"]["alreadyAffected"])
        self.assertEqual(
            "{victim} is already moving as fast as they can.",
            by_name["haste"]["payload"]["toChar"]["alreadyAffectedOther"],
        )
        self.assertEqual("apply", by_name["haste"]["guards"][0]["messageKey"])
        self.assertEqual(["applyObject", "apply"], [entry["messageKey"] for entry in by_name["bless"]["guards"]])

    def test_spell_from_json_hydrates_apply_payload_messages(self):
        spells = json.loads((ROOT / "resources" / "collections" / "SOMDB.Spells.json").read_text())
        haste_data = dict(next(spell for spell in spells if spell["name"] == "haste"))
        haste_data.setdefault("levelByClass", {})
        haste_data.setdefault("ratingByClass", {})
        haste = Spell.from_json(haste_data)

        self.assertEqual(
            "You feel yourself moving more quickly.\r\n",
            haste.message("to_victim", "apply", victim="Target"),
        )
        self.assertEqual(
            "Target is moving more quickly.\r\n",
            haste.message("to_room", "apply", victim="Target"),
        )


class TestTableDamageSpells(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        replacements = {
            "api.CharacterApi": _module("api.CharacterApi", CharacterApi=_CharacterApi),
            "util.DisplayUtil": _module("util.DisplayUtil", DisplayUtil=SpellApi.send.__globals__["DisplayUtil"]),
        }
        with patch.dict(sys.modules, replacements):
            spec = importlib.util.spec_from_file_location("_table_spell_context", SRC / "skill/SpellContext.py")
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            cls.Context = module.SpellContext
        cls.documents = {d["name"]: d for d in json.loads(
            (ROOT / "resources/collections/SOMDB.Spells.json").read_text(encoding="utf-8"))}
        data = json.loads((ROOT / "resources/collections/SOMDB.GameData.json").read_text(encoding="utf-8"))[0]
        cls.enums = {name: IntEnum(name, values) for name, values in data['enums'].items()}
        cls.item_table = data['itemTable']
        position_base = type('_PositionBase', (), {'is_set': staticmethod(lambda raw, bit: bool(int(raw) & int(bit)))})
        with patch.dict(sys.modules, {
            'api.GameApi': _module('api.GameApi', GameApi=position_base),
            'mobile.Mobile': _module('mobile.Mobile', Mobile=type('_PositionMobile', (), {})),
            'player.Character': _module('player.Character', Character=object),
            'game.RandomNumberGenerator': _module('game.RandomNumberGenerator', RandomNumberGenerator=lambda: SimpleNamespace()),
            'util.GenericUtil': _module('util.GenericUtil', GenericUtil=SpellApi.eval_int.__globals__['GenericUtil']),
        }):
            spec = importlib.util.spec_from_file_location('_sleep_character_api', SRC / 'api/CharacterApi.py')
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            cls.PositionApi = module.CharacterApi
            cls.PositionApi.positions = cls.enums['positions']
            cls.PositionApi.is_npc = staticmethod(_CharacterApi.is_npc)
        with patch.dict(sys.modules, {'item.Item': _module('item.Item', Item=_Item)}):
            spec = importlib.util.spec_from_file_location('_spell_equipped', SRC / 'game/Equipped.py')
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            cls.Equipped = module.Equipped
        with patch.dict(sys.modules, {
            'api.CharacterApi': _module('api.CharacterApi', CharacterApi=_CharacterApi),
            'area.Exit': _module('area.Exit', Exit=SimpleNamespace(DIRECTION_NAMES=('north', 'east', 'south', 'west', 'up', 'down'))),
            'mobile.Mobile': _module('mobile.Mobile', Mobile=object),
            'item.ExtraDescriptionData': _module('item.ExtraDescriptionData', ExtraDescriptionData=object),
            'util.PlayerUtil': _module('util.PlayerUtil', PlayerUtil=object),
            'util.GenericUtil': _module('util.GenericUtil', GenericUtil=SpellApi.eval_int.__globals__['GenericUtil']),
        }):
            spec = importlib.util.spec_from_file_location('_spell_travel_room', SRC / 'area/Room.py')
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            cls.TravelRoom = module.Room
        with patch.dict(sys.modules, {
            "api.CharacterApi": _module("api.CharacterApi", CharacterApi=_CharacterApi),
            "util.GenericUtil": _module("util.GenericUtil", GenericUtil=SpellApi.eval_int.__globals__["GenericUtil"]),
        }):
            spec = importlib.util.spec_from_file_location("_spell_advancement", SRC / "player/CharacterAdvancement.py")
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            cls.advancement_module = module

    def setUp(self):
        self.effects = Mock()
        self.api = SpellApi(self.effects, Mock())
        self.api._queue_apply_affect_messages = Mock()
        self.api._queue_damage_payload = Mock()
        self.fight = SimpleNamespace(damage=Mock(return_value={}), _check_immunity=Mock(return_value='IS_NORMAL'))
        self.api._fight_handler = Mock(return_value=self.fight)
        self.api._effect_active = Mock(return_value=False)
        self.api.saves_spell = Mock(return_value=False)
        self.victim = SimpleNamespace(name="Target")
        self.enterContext(patch.object(_CharacterApi, 'is_awake', side_effect=self.PositionApi.is_awake, create=True))
        self.enterContext(patch.object(_CharacterApi, 'set_position', side_effect=self.PositionApi.set_position, create=True))
        self.enterContext(patch.object(_CharacterApi, 'pos_value', side_effect=self.PositionApi.pos_value, create=True))
        self.enterContext(patch.object(_CharacterApi, 'position_value', side_effect=self.PositionApi.position_value, create=True))
        self.enterContext(patch.object(_CharacterApi, 'is_immortal', return_value=False, create=True))
        self.enterContext(patch.object(_CharacterApi, 'can_see', return_value=True, create=True))

    def context(self, name, level):
        document = dict(self.documents[name], levelByClass={}, ratingByClass={})
        spell = Spell.from_json(document)
        registry = SimpleNamespace(all_spells=lambda: [Spell.from_json(dict(
            self.documents[name], levelByClass={}, ratingByClass={})) for name in ('blindness', 'curse', 'bless', 'frenzy')])
        return self.Context(actor=SimpleNamespace(level=level), spell=spell,
                            handler=SimpleNamespace(spell_api=self.api, spell_registry=registry),
                            room=object(), target=self.victim, cast_level=level)

    def test_cause_spell_content_deals_full_damage_without_rolling_a_save(self):
        for name, dice_count, expected in [('cause light', 1, 15),
                                            ('cause serious', 2, 26),
                                            ('cause critical', 3, 40)]:
            with self.subTest(spell=name):
                ctx = self.context(name, 25)
                self.api.saves_spell = Mock(return_value=True)
                self.fight.damage.reset_mock()
                with patch('random.randint', return_value=7) as roll:
                    self.assertTrue(self.api.execute_lambdas(ctx))
                self.api.saves_spell.assert_not_called()
                self.assertEqual(dice_count, roll.call_count)
                self.assertTrue(all(call.args == (1, 8) for call in roll.call_args_list))
                self.fight.damage.assert_called_once_with(
                    ctx.actor, self.victim, expected, dt='spell', dam_type='DAM_HARM')
                self.assertTrue(ctx.performed)

    def game_api(self):
        def flags_to_int(value):
            try:
                return int(value or 0)
            except ValueError:
                return sum(1 << (ord(c) - ord('A')) for c in str(value))
        return SimpleNamespace(get_enum=self.enums.get, item_table_map=lambda: self.item_table,
                               flags_to_int=flags_to_int, is_set=lambda v, bit: bool(int(v) & int(bit)),
                               flags_to_letters=str, unset_bit=lambda v, bit: int(v) & ~int(bit))

    def guard_context(self, name, level=20):
        ctx = self.room_context(name, level)
        for entity in (ctx.actor, ctx.victim):
            entity.level = level
            entity.is_npc = False
            entity.master = entity.leader = None
            entity.sex = '1'
            entity.effects = []
            entity.status_flags = SimpleNamespace(affected_by=0, act=0, off=0, imm=0, invis_level=0)
            entity.status_flags.assign_bitfield = lambda field, value, owner=entity: setattr(owner.status_flags, field, value)
            if name in ('sleep', 'calm'):
                self.PositionApi.set_position(entity, 'POS_STANDING')
        self.enterContext(patch.dict(SpellApi.character_flag.__globals__, GameApi=self.game_api()))
        self.enterContext(patch.object(SpellApi.is_affected.__globals__['CharacterApi'], 'get_enum',
            side_effect=self.enums.get, create=True))
        self.enterContext(patch.object(SpellApi.is_affected.__globals__['CharacterApi'], 'is_affected_by_name',
            side_effect=lambda entity, enums, flag: bool(int(entity.status_flags.affected_by) & int(enums[flag])), create=True))
        self.api._effect_active = SpellApi._effect_active.__get__(self.api)
        self.fight.is_safe = Mock(return_value=False)
        self.api._room_flag = Mock(return_value=False)
        return ctx

    def test_innate_duplicate_flags_block_all_nine_buffs_without_spell_records(self):
        for name, flag in [('detect evil', 'AFF_DETECT_EVIL'), ('detect good', 'AFF_DETECT_GOOD'),
                ('detect hidden', 'AFF_DETECT_HIDDEN'), ('detect invis', 'AFF_DETECT_INVIS'),
                ('detect magic', 'AFF_DETECT_MAGIC'), ('fly', 'AFF_FLYING'),
                ('infravision', 'AFF_INFRARED'), ('pass door', 'AFF_PASS_DOOR'), ('sanctuary', 'AFF_SANCTUARY')]:
            for self_target in (False, True):
                with self.subTest(spell=name, self_target=self_target):
                    ctx = self.guard_context(name)
                    if self_target:
                        ctx.set_target(ctx.actor)
                    ctx.victim.status_flags.affected_by = int(self.enums['affectedBy'][flag])
                    self.effects.reset_mock()
                    self.assertFalse(self.api.execute_lambdas(ctx))
                    self.effects.apply_spell_effects.assert_not_called()
                    self.assertEqual([], ctx.victim.effects)
                    self.assertTrue(ctx.payloads[-1]['to_char'])

    def test_sleep_rejects_undead_level_and_existing_flag_before_save(self):
        for scenario, saves, applied in [('sleeping', 0, False), ('undead', 0, False),
                                       ('high', 0, False), ('saved', 1, False),
                                       ('boundary', 1, True), ('undead_pc', 1, True)]:
            with self.subTest(scenario=scenario):
                ctx = self.guard_context('sleep')
                ctx.victim.is_npc = scenario == 'undead'
                if scenario in ('undead', 'undead_pc'):
                    ctx.victim.status_flags.act = int(self.enums['actBits'].ACT_UNDEAD)
                if scenario == 'sleeping':
                    ctx.victim.status_flags.affected_by = int(self.enums['affectedBy'].AFF_SLEEP)
                ctx.victim.level = 23 if scenario == 'high' else 22
                self.api.saves_spell = Mock(return_value=scenario == 'saved')
                self.effects.reset_mock()
                self.api.execute_lambdas(ctx)
                self.assertEqual(saves, self.api.saves_spell.call_count)
                self.assertEqual(applied, self.effects.apply_spell_effects.called)
                if saves:
                    self.api.saves_spell.assert_called_once_with(ctx, 'DAM_CHARM', -4, target=ctx.victim)

    def test_charm_guard_matrix_and_law_follows_charm_save(self):
        for scenario, save_count, applied in [('safe', 0, False), ('self', 0, False),
                ('victim_charmed', 0, False), ('caster_charmed', 0, False), ('higher', 0, False),
                ('immune', 0, False), ('saved', 1, False), ('law', 1, False), ('allowed', 1, True)]:
            with self.subTest(scenario=scenario):
                ctx = self.guard_context('charm person')
                if scenario == 'self':
                    ctx.set_target(ctx.actor)
                if scenario in ('victim_charmed', 'caster_charmed'):
                    entity = ctx.actor if scenario == 'caster_charmed' else ctx.victim
                    entity.status_flags.affected_by = int(self.enums['affectedBy'].AFF_CHARM)
                if scenario == 'immune':
                    ctx.victim.status_flags.imm = int(self.enums['mobImmunity'].IMM_CHARM)
                if scenario == 'higher':
                    ctx.victim.level += 1
                self.fight.is_safe.return_value = scenario == 'safe'
                self.api._room_flag.return_value = scenario == 'law'
                self.api.saves_spell = Mock(return_value=scenario == 'saved')
                self.effects.reset_mock()
                self.api.execute_lambdas(ctx)
                self.assertEqual(save_count, self.api.saves_spell.call_count)
                self.assertEqual(applied, self.effects.apply_spell_effects.called)
                if save_count:
                    self.api.saves_spell.assert_called_once_with(ctx, 'DAM_CHARM', 0, target=ctx.victim)
                if scenario == 'law':
                    self.assertIn('mayor', ctx.payloads[-1]['to_char'])

    def test_plague_saves_before_undead_and_still_joins_eligible_recasts(self):
        for undead, npc, saved, applied in [(True, True, False, False), (False, False, True, False),
                                           (True, False, False, True), (False, True, False, True)]:
            with self.subTest(undead=undead, npc=npc, saved=saved):
                ctx = self.guard_context('plague')
                ctx.victim.is_npc = npc
                ctx.victim.status_flags.act = int(self.enums['actBits'].ACT_UNDEAD) if undead else 0
                self.api.saves_spell = Mock(return_value=saved)
                self.effects.reset_mock()
                self.api.execute_lambdas(ctx)
                self.api.saves_spell.assert_called_once_with(ctx, 'DAM_DISEASE')
                self.assertEqual(applied, self.effects.apply_spell_effects.called)
                if applied:
                    self.assertTrue(self.effects.apply_spell_effects.call_args.kwargs['join'])

    def test_change_sex_weaken_and_faerie_fire_duplicates_stop_before_save_or_mutation(self):
        for name, effect in [('change sex', 'spell.change_sex'), ('weaken', 'spell.weaken'), ('faerie fire', 'AFF_FAERIE_FIRE')]:
            with self.subTest(spell=name):
                ctx = self.guard_context(name)
                if effect.startswith('AFF_'):
                    ctx.victim.status_flags.affected_by = int(self.enums['affectedBy'][effect])
                else:
                    ctx.victim.effects.append(SimpleNamespace(type=effect))
                self.api.saves_spell = Mock()
                self.effects.reset_mock()
                with patch('random.choice') as choice:
                    self.assertFalse(self.api.execute_lambdas(ctx))
                self.api.saves_spell.assert_not_called()
                choice.assert_not_called()
                self.effects.apply_spell_effects.assert_not_called()
                self.assertEqual('1', ctx.victim.sex)
        ctx = self.guard_context('change sex')
        self.api.saves_spell = Mock(return_value=True)
        with patch('random.choice') as choice:
            self.assertFalse(self.api.execute_lambdas(ctx))
        choice.assert_not_called()

    def test_change_sex_guard_has_a_temporary_record_and_removal_restores_original(self):
        from tests.test_effect_util_affects import _load_effect_runtime
        Handler, _Effect, Generic, _Rng = _load_effect_runtime()
        ctx = self.guard_context('change sex')
        ctx.victim.status_flags.assign_bitfield = lambda field, value: setattr(ctx.victim.status_flags, field, value)
        self.api.effect_handler = Handler(SimpleNamespace(get=self.enums.get))
        with patch.dict(sys.modules, {'util.GenericUtil': SimpleNamespace(GenericUtil=Generic)}), \
                patch('random.randint', side_effect=[1, 2]) as roll:
            self.assertTrue(self.api.execute_lambdas(ctx))
        self.assertEqual(2, roll.call_count)
        self.assertEqual('2', ctx.victim.sex)
        self.assertEqual(1, len(ctx.victim.effects))
        effect = ctx.victim.effects[0]
        self.assertEqual(('spell.change_sex', 40, 1), (effect.type, effect.duration, effect.modifier))
        self.api.saves_spell.reset_mock()
        ctx.done = ctx.performed = False
        with patch('random.randint') as roll:
            self.api.execute_lambdas(ctx)
        roll.assert_not_called()
        self.api.saves_spell.assert_not_called()
        self.api.effect_handler.affect_strip(ctx.victim, 'spell.change_sex')
        self.assertEqual('1', ctx.victim.sex)
        self.assertEqual('0', ctx.spell.affect_data[0]['modifier'])
        ctx.done = ctx.performed = False
        with patch.dict(sys.modules, {'util.GenericUtil': SimpleNamespace(GenericUtil=Generic)}), \
                patch('random.randint', return_value=0):
            self.assertTrue(self.api.execute_lambdas(ctx))
        self.assertEqual('0', ctx.victim.sex)
        ctx.victim.effects[0].duration = 0
        self.api.effect_handler.tick_effects(ctx.victim)
        self.assertEqual('1', ctx.victim.sex)

    def test_sleep_guard_owns_persistent_flag_until_effect_removal(self):
        from tests.test_effect_util_affects import _load_effect_runtime
        Handler, _Effect, Generic, _Rng = _load_effect_runtime()
        ctx = self.guard_context('sleep')
        ctx.victim.status_flags.assign_bitfield = lambda field, value: setattr(ctx.victim.status_flags, field, value)
        self.api.effect_handler = Handler(SimpleNamespace(get=self.enums.get))
        with patch.dict(sys.modules, {'util.GenericUtil': SimpleNamespace(GenericUtil=Generic)}):
            self.assertTrue(self.api.execute_lambdas(ctx))
        self.assertEqual(24, ctx.victim.effects[0].duration)
        self.assertTrue(ctx.victim.status_flags.affected_by & int(self.enums['affectedBy'].AFF_SLEEP))
        self.api.saves_spell.reset_mock()
        ctx.done = ctx.performed = False
        self.api.execute_lambdas(ctx)
        self.api.saves_spell.assert_not_called()
        self.api.effect_handler.affect_strip(ctx.victim, 'spell.sleep')
        self.assertEqual(0, ctx.victim.status_flags.affected_by)

    def live_sleep_context(self):
        return self.live_effect_context('sleep')

    def object_context(self, name, level=20):
        from tests.test_effect_util_affects import _load_effect_runtime, EffectUtil as RealEffects
        Handler, Effect, Generic, _ = _load_effect_runtime()
        ctx, room, destination, rooms = self.travel_context(name, level)
        self.api.effect_handler = Handler(SimpleNamespace(get=self.enums.get))
        self.enterContext(patch.dict(SpellApi.eval_int.__globals__, GenericUtil=Generic, EffectUtil=RealEffects))
        game = self.game_api()
        game.set_bit = lambda raw, bit: int(raw) | int(bit)
        game.flags_to_letters = lambda raw: ''.join(chr(ord('A') + bit) for bit in range(26) if raw & (1 << bit))
        game.liquids_map = lambda: {'water': {'color': 'clear', 'affect': [0,1,10,0,16]}, 'beer': {'color': 'amber'}}
        self.enterContext(patch.dict(SpellApi.eval_int.__globals__, GameApi=game))
        # Load the real lookup/parser and item models without bootstrapping networking.
        with patch.dict(sys.modules, {
            'interp.Command': _module('interp.Command', Command=object),
            'interp.InterpView': _module('interp.InterpView', InterpView=object),
            'interp.Context': _module('interp.Context', Context=object),
            'server.LoggerFactory': _module('server.LoggerFactory', LoggerFactory=_LoggerFactory),
            'api.CharacterApi': _module('api.CharacterApi', CharacterApi=_CharacterApi),
            'api.GameApi': _module('api.GameApi', GameApi=game),
            'player.Character': _module('player.Character', Character=object),
            'item.ExtraDescriptionData': _module('item.ExtraDescriptionData', ExtraDescriptionData=object),
            'item.Effect': _module('item.Effect', Effect=Effect),
            'util.GenericUtil': _module('util.GenericUtil', GenericUtil=Generic),
        }):
            loaded = {}
            for mod, path in [('util.InterpUtil', 'util/InterpUtil.py'),
                              ('util.LookupUtil', 'util/LookupUtil.py'), ('item.Item', 'item/Item.py')]:
                spec = importlib.util.spec_from_file_location(mod, SRC / path)
                module = importlib.util.module_from_spec(spec)
                loaded[mod] = module
                sys.modules[mod] = module
                spec.loader.exec_module(module)
        self.enterContext(patch.dict(sys.modules, loaded))
        RealItem = loaded['item.Item'].Item
        self.enterContext(patch.object(SpellApi.find_carried_object.__globals__['ItemApi'], 'can_see_object', return_value=True, create=True))
        def item(item_name='ring', kind='armor', **extras):
            args = dict(id=item_name, area_id='', vnum='900', name=item_name, short_description=item_name,
                        long_description='', material='metal', item_type=kind, extra_flags='', wear_flags='',
                        value0='0', value1='0', value2='0', value3='0', value4='0', condition='100', level=10,
                        weight=25, cost=100, affect_data=[], contains=[], effects=[], enchanted=False)
            args.update(extras)
            return RealItem(**args)
        ctx.actor.owned_items = lambda: list(ctx.actor.loot) + [v for v in ctx.actor.equipped.__dict__.values() if v is not None]
        ctx.actor.equipped_slot_of = ctx.actor.equipped.slot_of
        obj = item()
        ctx.actor.loot.append(obj)
        ctx.set_target(obj)
        ctx.actor.his_her = lambda: 'his'
        self.PositionApi.set_position(ctx.actor, 'POS_STANDING')
        # Execute actual combat position recovery with isolated dependencies.
        tree = ast.parse((SRC / 'combat/CombatHandler.py').read_text())
        fight_class = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'FightHandler')
        methods = [n for n in fight_class.body if isinstance(n, ast.FunctionDef) and n.name in ('update_pos', '_set_position')]
        isolated = ast.Module(body=[ast.ClassDef(name='PositionRecovery', bases=[], keywords=[], body=methods, decorator_list=[])], type_ignores=[])
        namespace = dict(GenericUtil=Generic, CharacterApi=_CharacterApi,
                         FightUtil=SimpleNamespace(entity_position_value=self.PositionApi.position_value))
        exec(compile(ast.fix_missing_locations(isolated), str(SRC / 'combat/CombatHandler.py'), 'exec'), namespace)
        recovery = namespace['PositionRecovery']()
        recovery.PositionsEnum = self.enums['positions']
        self.fight.update_pos = Mock(side_effect=recovery.update_pos)
        self.enterContext(patch.object(SpellApi.create_object.__globals__['ItemFactory'], 'create',
            side_effect=lambda prototype: item('created-' + str(len(room.contents) + len(ctx.actor.loot)),
                                              kind=getattr(prototype, 'item_type', 'container')), create=True))
        return ctx, obj, item, Effect, room, destination

    def test_enchant_all_result_bands_and_boundaries(self):
        for name, kind, rolls in [('enchant armor', 'armor', [(3,'destroyed'),(4,'disenchanted'),(5,'disenchanted'),(6,'failed'),(20,'failed'),(21,'success'),(89,'success'),(90,'exceptional')]),
                                  ('enchant weapon','weapon', [(2,'destroyed'),(3,'disenchanted'),(8,'disenchanted'),(9,'failed'),(18,'failed'),(19,'success'),(99,'success'),(100,'exceptional')])]:
            for roll, result in rolls:
                with self.subTest(spell=name, roll=roll, expected=result):
                    ctx, obj, _, _, room, _ = self.object_context(name, 5)
                    obj.item_type = kind
                    with patch('random.randint', return_value=roll) as rng:
                        self.api.execute_lambdas(ctx)
                    rng.assert_called_once_with(1, 100)
                    if result == 'destroyed':
                        self.assertNotIn(obj, ctx.actor.loot)
                    elif result == 'disenchanted':
                        self.assertTrue(obj.enchanted)
                        self.assertEqual([], obj.effects)
                        self.assertEqual('', obj.extra_flags)
                    elif result == 'failed':
                        self.assertFalse(obj.enchanted)
                        self.assertEqual([], obj.effects)
                        self.assertEqual([{'to_char': 'Nothing seemed to happen.\r\n'}], ctx.payloads)
                    else:
                        added = (-1 if kind == 'armor' else 1) * (2 if result == 'exceptional' else 1)
                        self.assertEqual([added] * (1 if kind == 'armor' else 2), [e.modifier for e in obj.effects])
                        self.assertTrue(all(e.duration == -1 and e.level == 5 for e in obj.effects))
                        self.assertEqual(11, obj.level)
                        self.assertTrue(self.game_api().flags_to_int(obj.extra_flags) & int(self.enums['itemFlags'].ITEM_MAGIC))
                    if result != 'failed':
                        self.assertIn('to_room', ctx.payloads[0])
                        self.assertIn('to_char', ctx.payloads[0])
                        self.assertNotIn(ctx.actor, ctx.payloads[0]['targets'])

    def test_enchant_risk_counts_existing_records_once_preserves_durations_and_adds_hum(self):
        ctx, obj, _, Effect, _, _ = self.object_context('enchant weapon', 51)
        obj.item_type, obj.level = 'weapon', 50
        obj.effects = [Effect(type=-1, where='TO_OBJECT', location='APPLY_HITROLL', modifier=3, level=60, duration=-1),
                       Effect(type='spell.old', where='TO_OBJECT', location='APPLY_DAMROLL', modifier=4, level=20, duration=8)]
        obj.affect_data = ['A,18,3']  # canonical instance records already include the prototype
        with patch('random.randint', return_value=100):
            self.assertTrue(self.api.execute_lambdas(ctx))
        self.assertEqual(2, len(obj.effects))
        self.assertEqual([5, 6], [e.modifier for e in obj.effects])
        self.assertEqual([60, 51], [e.level for e in obj.effects])
        self.assertEqual([-1, 8], [e.duration for e in obj.effects])
        self.assertEqual(50, obj.level)
        self.assertTrue(self.game_api().flags_to_int(obj.extra_flags) & int(self.enums['itemFlags'].ITEM_HUM))

    def test_enchant_worn_and_wrong_types_stop_without_rolls(self):
        for name in ('enchant weapon', 'enchant armor'):
            for worn in (False, True):
                ctx, obj, _, _, _, _ = self.object_context(name)
                obj.item_type = ('weapon' if name.endswith('weapon') else 'armor') if worn else 'food'
                if worn: self.Equipped.equip_item(ctx.actor, obj, 'held')
                with patch('random.randint') as rng:
                    self.assertFalse(self.api.execute_lambdas(ctx))
                rng.assert_not_called()
                self.assertFalse(obj.enchanted)

    def test_enchant_risk_bounds_flag_reductions_and_repeated_disenchantment(self):
        for level, bonus, flags, roll, success in [(20,-3,0,50,False),(20,-3,0,51,True),
                (20,-3,int(self.enums['itemFlags'].ITEM_BLESS | self.enums['itemFlags'].ITEM_GLOW),30,False),
                (20,-3,int(self.enums['itemFlags'].ITEM_BLESS | self.enums['itemFlags'].ITEM_GLOW),31,True),
                (1,-20,0,85,False),(1,-20,0,86,True),(60,0,0,5,False),(60,0,0,6,True)]:
            with self.subTest(level=level,bonus=bonus,flags=flags,roll=roll):
                ctx,obj,_,Effect,_,_=self.object_context('enchant armor',level)
                obj.extra_flags=str(flags)
                obj.effects=[Effect(type=-1,where='TO_OBJECT',location='APPLY_AC',modifier=bonus,level=1,duration=-1)]
                with patch('random.randint',return_value=roll):self.assertEqual(success,self.api.execute_lambdas(ctx))
        ctx,obj,_,Effect,_,_=self.object_context('enchant armor',5)
        obj.effects=[Effect(type=-1,where='TO_OBJECT',location='APPLY_STR',modifier=1,level=10,duration=-1)]
        obj.affect_data=['A,1,1']
        with patch('random.randint',return_value=10):self.assertTrue(self.api.execute_lambdas(ctx))
        self.assertTrue(obj.enchanted)
        self.assertEqual([],obj.effects)
        ctx.done=ctx.performed=False
        with patch('random.randint',return_value=30):self.assertTrue(self.api.execute_lambdas(ctx))
        self.assertEqual(['APPLY_AC'],[e.location for e in obj.effects])
        self.assertEqual([-1],[e.modifier for e in obj.effects])

    def test_prototype_affect_conversion_has_neutral_flags_and_enchants_without_duplication(self):
        ctx,obj,_,Effect,_,_=self.object_context('enchant weapon',60)
        obj.item_type='weapon'
        obj.affect_data=['A,18,2']
        tree=ast.parse((SRC/'item/ItemFactory.py').read_text())
        utility=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ItemFactory')
        method=next(n for n in utility.body if isinstance(n,ast.FunctionDef) and n.name=='update_affect_data')
        method.decorator_list=[]
        namespace=dict(Effect=Effect,AffectWhere=SimpleNamespace(TO_OBJECT=SimpleNamespace(value=1)),
                       GameApi=SimpleNamespace(convert_flags=self.game_api().flags_to_int))
        exec(compile(ast.fix_missing_locations(ast.Module(body=[method],type_ignores=[])),str(SRC/'item/ItemFactory.py'),'exec'),namespace)
        with patch.object(SpellApi.object_affects.__globals__['ItemFactory'],'update_affect_data',side_effect=namespace['update_affect_data'],create=True):
            with patch('random.randint',return_value=10):self.assertTrue(self.api.execute_lambdas(ctx))
        self.assertEqual(2,len(obj.effects))
        self.assertEqual([0,0],[e.bitvector for e in obj.effects])
        effects_util=SpellApi.object_affects.__globals__['EffectUtil']
        self.assertEqual({int(self.enums['applyTypes'].APPLY_DAMROLL):1,int(self.enums['applyTypes'].APPLY_HITROLL):3},
                         {effects_util.enum_value(self.enums['applyTypes'],e.location,-1):e.modifier for e in obj.effects})
        self.assertEqual(int(self.enums['itemFlags'].ITEM_MAGIC),self.game_api().flags_to_int(obj.extra_flags))

    def test_recharge_bands_consumed_eligibility_capacity_loss_and_named_references(self):
        # level 20, armor ordinal 2, max 10/current 5 => chance 53.
        for roll, expected in [(25, ('0','10')), (26,('0','6')), (53,('0','7')), (54,('9','5')), (79,('9','5')), (80,None)]:
            with self.subTest(roll=roll):
                ctx, obj, _, _, _, _ = self.object_context('recharge', 20)
                obj.item_type, obj.value1, obj.value2, obj.value3 = 'wand', '10', '5', SimpleNamespace(name='armor')
                with patch('random.randint', return_value=roll): self.api.execute_lambdas(ctx)
                if expected is None:
                    self.assertNotIn(obj, ctx.actor.loot)
                else:
                    self.assertEqual(expected, (obj.value1, obj.value2))
                    if expected[0] == '0':
                        ctx.done = ctx.performed = False
                        with patch('random.randint') as rng: self.assertFalse(self.api.execute_lambdas(ctx))
                        rng.assert_not_called()
                        self.assertIn('already been recharged', ctx.payloads[-1]['to_char'])
                if 26 <= roll <= 53:
                    self.assertEqual([{'to_char':'ring glows softly.\r\n'}] * 2, ctx.payloads[:2])
                if roll == 25:
                    self.assertEqual('ring glows softly.\r\n', ctx.payloads[0]['to_room'])

    def test_recharge_advanced_spell_and_zero_capacity_fail_before_rng(self):
        for kind, reference, maximum in [('armor','armor','10'),('staff','heal','10'),('staff','detect evil','10'),('wand','armor','0')]:
            ctx, obj, _, _, _, _ = self.object_context('recharge', 20)
            obj.item_type, obj.value3, obj.value1 = kind, reference, maximum
            with patch('random.randint') as rng: self.assertFalse(self.api.execute_lambdas(ctx))
            rng.assert_not_called()

    def test_creation_scaling_inventory_timers_and_disc_replacement(self):
        for name in ('create food','create rose','create spring','floating disc','continual light'):
            with self.subTest(spell=name):
                ctx, _, item, _, room, _ = self.object_context(name, 21)
                ctx.set_target(None)
                ctx.target_name = ''
                ctx.actor.level = 30
                old = item('old disc', 'container')
                self.Equipped.equip_item(ctx.actor, old, 'floating_nearby')
                ctx.handler.registry_service.item_registry = SimpleNamespace(get_or_none=lambda **kwargs: item('prototype', 'container'))
                with patch('random.randint', return_value=7): self.assertTrue(self.api.execute_lambdas(ctx))
                created = ctx.get_alias('created_item')
                if name == 'create food': self.assertEqual(('10','21'), (created.value0,created.value1))
                if name == 'create spring': self.assertEqual(21,created.timer)
                if name == 'create rose': self.assertIn(created,ctx.actor.loot)
                if name == 'floating disc':
                    self.assertEqual(('300','150',53),(created.value0,created.value3,created.timer))
                    self.assertIs(created,ctx.actor.equipped.floating_nearby)
                    self.assertIn(old,ctx.actor.loot)
                    self.assertIn('You stop using old disc.', ''.join(p.get('to_char','') for p in ctx.payloads))
                if name not in ('create rose','floating disc'): self.assertIs(created,room.contents[created.id])
                self.assertTrue(any('to_room' in p for p in ctx.payloads))

    def test_disc_noremove_blocks_creation_and_randomness(self):
        ctx, _, item, _, _, _ = self.object_context('floating disc')
        old = item('old disc', 'container', extra_flags=str(int(self.enums['itemFlags'].ITEM_NOREMOVE)))
        self.Equipped.equip_item(ctx.actor, old, 'floating_nearby')
        with patch('random.randint') as rng: self.assertFalse(self.api.execute_lambdas(ctx))
        rng.assert_not_called()
        self.assertEqual("You can't remove old disc.\r\n",ctx.payloads[0]['to_char'])
        self.assertIs(old,ctx.actor.equipped.floating_nearby)

    def test_continual_light_carried_glow_missing_repeat_and_equipped_exclusion(self):
        for scenario in ('success','missing','repeat','worn'):
            ctx, obj, _, _, room, _ = self.object_context('continual light')
            ctx.target_name = 'ring' if scenario != 'missing' else 'absent'
            if scenario == 'repeat': obj.extra_flags = str(int(self.enums['itemFlags'].ITEM_GLOW))
            if scenario == 'worn': self.Equipped.equip_item(ctx.actor,obj,'held')
            self.api.execute_lambdas(ctx)
            self.assertEqual({},room.contents)
            if scenario == 'success':
                self.assertTrue(self.game_api().flags_to_int(obj.extra_flags) & int(self.enums['itemFlags'].ITEM_GLOW))
                self.assertEqual('ring glows with a white light.\r\n',ctx.payloads[0]['to_room'])
            else: self.assertEqual(1,len(ctx.payloads))

    def test_create_water_liquid_protection_rain_capacity_and_keyword(self):
        for kind, liquid, current, capacity, rain, expected in [
                ('fountain','water',0,100,False,None),('drink_con','beer',1,100,False,None),
                ('drink_con','beer',0,100,False,20),('drink_con','water',95,100,True,100),
                ('drink_con','water',0,100,True,40),('drink_con','water',0,0,False,0)]:
            with self.subTest(kind=kind, liquid=liquid,current=current,capacity=capacity,rain=rain):
                ctx,obj,_,_,_,_=self.object_context('create water',10)
                obj.item_type,obj.value0,obj.value1,obj.value2=kind,str(capacity),str(current),liquid
                obj.liquid_color,obj.liquid_affect_data='amber',[1,2,3]
                ctx.handler.weather_handler=SimpleNamespace(weather_info=SimpleNamespace(sky=int(self.enums['timeAndWeather'].SKY_RAINING) if rain else 0))
                self.api.execute_lambdas(ctx)
                self.assertEqual(current if expected is None else expected,int(obj.value1))
                if expected is not None and expected>current:
                    self.assertEqual('water',obj.value2)
                    self.assertEqual(('clear',[0,1,10,0,16]),(obj.liquid_color,obj.liquid_affect_data))
                    self.assertEqual('ring water',obj.name)
                    self.assertEqual('ring is filled.\r\n',ctx.payloads[0]['to_char'])
                elif expected==0: self.assertEqual([],ctx.payloads)

    def test_locate_objects_traverses_inventory_equipment_nested_and_floor_ownership(self):
        ctx, _, item, _, room, destination = self.object_context('locate object', 20)
        ctx.target_name = 'gem'
        bag = item('bag', 'container', contains=[item('red gem')])
        room.contents[bag.id] = bag
        carried = item('pack', 'container', contains=[item('blue gem')])
        ctx.actor.loot.append(carried)
        worn = item('green gem')
        self.Equipped.equip_item(ctx.actor, worn, 'held')
        destination.contents['far'] = item('far gem')
        with patch('random.randint', return_value=1): self.assertTrue(self.api.execute_lambdas(ctx))
        text = ''.join(p.get('to_char','') for p in ctx.payloads)
        self.assertEqual(2,text.count('One is carried by Caster'))
        self.assertEqual(2,text.count('One is in '))
        self.assertNotIn('red gem',text)  # C reports locations, not object descriptions
        self.assertNotIn('[Room',text)

    def test_locate_filters_order_no_locate_visibility_name_chance_and_actor_level(self):
        ctx, _, item, _, room, _ = self.object_context('locate object',20)
        ctx.target_name = 'gem'
        objects = [item('invisible gem'),item('stone'),item('protected gem',extra_flags=str(int(self.enums['itemFlags'].ITEM_NOLOCATE))),
                   item('high gem',level=21),item('resistant gem'),item('found gem')]
        room.contents.update({o.id:o for o in objects})
        with patch.object(SpellApi.locate_objects.__globals__['ItemApi'],'can_see_object',side_effect=lambda room,actor,obj:obj.name!='invisible gem'), \
                patch('random.randint',side_effect=[1,100,1]) as rng:
            self.api.execute_lambdas(ctx)
        self.assertEqual(3,rng.call_count)
        self.assertEqual(1,len(ctx.payloads))
        self.assertEqual('One is in \r\n',ctx.payloads[0]['to_char'])

    def test_locate_limits_and_hidden_carrier_do_not_reveal_rooms(self):
        for immortal, maximum in [(False,2),(True,200)]:
            ctx, _, item, _, room, _ = self.object_context('locate object',1)
            ctx.target_name='gem'
            ctx.actor.loot.extend(item('gem '+str(i),level=1) for i in range(205))
            with patch.object(_CharacterApi,'is_immortal',return_value=immortal), \
                    patch.object(_CharacterApi,'can_see',return_value=False),patch('random.randint',return_value=1):
                self.api.execute_lambdas(ctx)
            self.assertEqual(maximum,len(ctx.payloads))
            self.assertTrue(all(p['to_char']=='One is in somewhere\r\n' for p in ctx.payloads))

    def test_identify_exposes_type_specific_runtime_properties_and_named_spell_refs(self):
        cases=[('weapon',dict(value0='1',value1='3',value2='6',value4=str(int(self.enums['weaponType'].WEAPON_POISON))),['Weapon type is sword.','Damage is 3d6 (average 10).','Weapons flags: poison']),
               ('armor',dict(value0='1',value1='2',value2='3',value3='4'),['Armor class is 1 pierce, 2 bash, 3 slash, and 4 vs. magic.']),
               ('wand',dict(value0='20',value2='7',value3=SimpleNamespace(name='armor')),["Has 7 charges of level 20 'armor'."]),
               ('scroll',dict(value0='20',value1='armor',value2='-1',value3='heal',value4=''),["Level 20 spells of: 'armor' 'heal'."]),
               ('drink_con',dict(value2='beer'),['It holds amber-colored beer.']),
               ('container',dict(value0='30',value1='1',value3='5',value4='50'),['Capacity: 30#  Maximum weight: 5#  flags: closeable','Weight multiplier: 50%'])]
        for kind,values,expected in cases:
            with self.subTest(kind=kind):
                ctx,obj,_,_,_,_=self.object_context('identify')
                obj.item_type=kind
                for field,value in values.items():setattr(obj,field,value)
                self.assertTrue(self.api.execute_lambdas(ctx))
                text=ctx.payloads[0]['to_char']
                self.assertIn('Weight is 2, value is 100, level is 10.',text)
                for line in expected:self.assertIn(line,text)

    def test_identify_lists_prototype_and_timed_affects_once_and_handles_old_weapon_format(self):
        ctx,obj,_,Effect,_,_=self.object_context('identify')
        obj.item_type='weapon'
        obj.new_format=False
        obj.value1,obj.value2='5','10'
        obj.effects=[Effect(type=-1,where='TO_OBJECT',location='APPLY_STR',modifier=2,duration=-1),
                     Effect(type='spell.bless',where='TO_OBJECT',location='APPLY_SAVES',modifier=-1,duration=3,bitvector='ITEM_BLESS'),
                     Effect(type='spell.unknown',where=99,location='APPLY_STR',modifier=1,duration=-1,bitvector=2)]
        self.assertTrue(self.api.execute_lambdas(ctx))
        text=ctx.payloads[0]['to_char']
        self.assertIn('Damage is 5 to 10 (average 7).',text)
        self.assertEqual(1,text.count('Affects strength by 2.'))
        self.assertIn('Affects saves by -1, 3 hours.',text)
        self.assertIn('Adds bless object flag.',text)
        self.assertIn('Unknown bit 99: 2',text)

    def test_healing_calls_real_position_recovery_and_routes_self_other_feedback(self):
        for name in ('cure light','cure serious','cure critical','heal'):
            for self_target in (False,True):
                ctx,_,_,_,_,_=self.object_context(name,20)
                victim=ctx.actor if self_target else next(e for e in ctx.handler.room_registry.all_rooms()[1].characters.values() if e.name=='Target')
                victim.hit,victim.max_hit=-2,200
                self.PositionApi.set_position(victim,'POS_INCAP')
                ctx.set_target(victim)
                with patch('random.randint',return_value=1):self.assertTrue(self.api.execute_lambdas(ctx))
                self.assertGreater(victim.hit,0)
                self.assertEqual(int(self.enums['positions'].POS_STANDING),self.PositionApi.position_value(victim))
                self.fight.update_pos.assert_called_once_with(victim)
                self.assertEqual('A warm feeling fills your body.\r\n' if name=='heal' else 'You feel better!\r\n',ctx.payloads[0]['to_victim'])
                self.assertEqual(1 if self_target else 2,len(ctx.payloads))
                if not self_target:self.assertEqual('Ok.\r\n',ctx.payloads[-1]['to_char'])

    def test_refresh_full_partial_and_mass_healing_use_owned_spell_payloads(self):
        for current,expected in [(90,'You feel fully refreshed!\r\n'),(10,'You feel less tired.\r\n')]:
            ctx,_,_,_,_,destination=self.object_context('refresh',20)
            victim=destination.characters['victim'];victim.movement,victim.max_movement=current,100
            ctx.set_target(victim);self.api.execute_lambdas(ctx)
            self.assertEqual(expected,ctx.payloads[0]['to_victim'])
        ctx,_,_,_,room,_=self.object_context('mass healing',20)
        ctx.set_target(None)
        for entity in room.characters.values():
            entity.hit,entity.max_hit=1,200
            entity.movement,entity.max_movement=1,100
            self.PositionApi.set_position(entity,'POS_STUNNED')
        pet=self.effect_room_member('Pet',npc=True);pet.hit,pet.max_hit=1,200
        room.add_mobile_to_room(pet)
        spellbook=[Spell.from_json(dict(doc,levelByClass={},ratingByClass={})) for doc in self.documents.values()]
        ctx.handler.spell_registry=SimpleNamespace(all_spells=lambda:spellbook)
        self.assertTrue(self.api.execute_lambdas(ctx))
        self.assertTrue(all(e.hit==101 and e.movement==21 for e in room.characters.values()))
        self.assertEqual(1,pet.hit)
        self.assertEqual(2,self.fight.update_pos.call_count)
        self.assertEqual(2,sum(p.get('to_char')=='Ok.\r\n' for p in ctx.payloads))

    def test_alignment_seven_strict_bands_and_detect_poison_other_objects(self):
        for alignment,key in [(701,'pure'),(700,'excellent'),(351,'excellent'),(350,'kind'),(101,'kind'),(100,'neutral'),(-99,'neutral'),(-100,'liar'),(-349,'liar'),(-350,'murderer'),(-699,'murderer'),(-700,'evil')]:
            ctx,_,_,_,_,destination=self.object_context('know alignment')
            victim=destination.characters['victim'];victim.character_attributes.alignment=alignment;ctx.set_target(victim)
            self.api.execute_lambdas(ctx)
            self.assertEqual(self.api._ability_message(ctx.spell,'to_char',key,ctx,victim),ctx.payloads[0]['to_char'])
        for kind,poison,expected in [('food','1','poisonous fumes'),('drink_con','0','delicious'),('fountain','1',"doesn't look poisoned"),('weapon','0',"doesn't look poisoned")]:
            ctx,obj,_,_,_,_=self.object_context('detect poison');obj.item_type,obj.value3=kind,poison
            self.api.execute_lambdas(ctx);self.assertIn(expected,ctx.payloads[0]['to_char'])

    def test_ventriloquate_saves_per_awake_listener_including_caster_excluding_named_speaker(self):
        ctx,_,_,_,room,_=self.object_context('ventriloquate')
        speaker=self.effect_room_member('bob guard');room.add_player_to_room(speaker)
        asleep=self.effect_room_member('Sleeping');self.PositionApi.set_position(asleep,'POS_SLEEPING');room.add_player_to_room(asleep)
        ctx.target_name="bob Follow me"
        self.api.saves_spell=Mock(side_effect=lambda context,kind,target:target is ctx.actor)
        self.assertTrue(self.api.execute_lambdas(ctx))
        listeners=[call.kwargs['target'] for call in self.api.saves_spell.call_args_list]
        self.assertIn(ctx.actor,listeners);self.assertNotIn(speaker,listeners);self.assertNotIn(asleep,listeners)
        self.assertEqual(2,len(listeners))
        self.assertEqual("Someone makes bob say 'Follow me'.\r\n",ctx.payloads[0]['to_victim'])
        self.assertEqual("Bob says 'Follow me'.\r\n",ctx.payloads[1]['to_victim'])
        self.assertIs(ctx.actor,ctx.payloads[0]['victim'])

    def test_control_weather_changes_only_tendency_with_c_dice_and_feedback(self):
        for command,change,rolls in [('better',12,4),('worse',-12,4),('sunny',0,0)]:
            ctx,_,_,_,_,_=self.object_context('control weather',12)
            weather=SimpleNamespace(change=5,mmhg=1000)
            ctx.handler.weather_handler=SimpleNamespace(weather_info=weather)
            ctx.target_name=command
            with patch('random.randint',return_value=3) as rng:self.api.execute_lambdas(ctx)
            self.assertEqual(rolls,rng.call_count)
            self.assertEqual(5+change,weather.change)
            self.assertEqual(1000,weather.mmhg)
            self.assertEqual('Ok.\r\n',ctx.payloads[-1]['to_char'])

    def travel_context(self, name, level=40):
        ctx = self.guard_context(name, level)
        source = self.TravelRoom(id='source', vnum='100', area_id='area1')
        destination = self.TravelRoom(id='destination', vnum='200', area_id='area2')
        rooms = [source, destination]
        for entity, room in ((ctx.actor, source), (ctx.victim, destination)):
            entity.room_id, entity.area_id = room.id, room.area_id
            entity.guild = ''
            entity.trust = 0
            entity.fighting = None
            entity.movement = 81
            entity.equipped = self.Equipped()
            entity.loot = []
            room.add_player_to_room(entity)
        ctx.victim.level = 20
        for room in rooms:
            observer = self.effect_room_member(room.id + '-observer')
            observer.room_id, observer.area_id = room.id, room.area_id
            room.add_player_to_room(observer)
        def get_room(**kwargs):
            return next((r for r in rooms if all(str(getattr(r, k)) == str(v) for k, v in kwargs.items())), None)
        registry = SimpleNamespace(all_rooms=lambda: rooms, get_or_none=get_room)
        shops = SimpleNamespace(find_by_keeper_vnum=Mock(return_value=None))
        prototype = SimpleNamespace(vnum='25', name='portal')
        ctx.handler.registry_service = SimpleNamespace(room_registry=registry, shop_registry=shops,
            item_registry=SimpleNamespace(get_or_none=lambda **kw: prototype if kw.get('vnum') == '25' else None))
        ctx.handler.room_registry = registry
        ctx.room = source
        ctx.target_name = 'Target'
        ctx.aliases['room'] = source
        self.api._find_world_character = Mock(return_value=ctx.victim)
        self.api._room_flag = SpellApi._room_flag.__get__(self.api)
        self.enterContext(patch.object(_CharacterApi, 'get_enum', side_effect=self.enums.get, create=True))
        self.enterContext(patch.object(_CharacterApi, 'enum_bit', side_effect=lambda enum, name: int(enum[name]), create=True))
        self.enterContext(patch.object(_CharacterApi, 'is_set', side_effect=lambda raw, bit: bool(int(raw) & int(bit)), create=True))
        self.enterContext(patch.object(_CharacterApi, 'is_clan', side_effect=self.PositionApi.is_clan, create=True))
        self.enterContext(patch.object(self.PositionApi, 'get_enum', side_effect=self.enums.get, create=True))
        self.enterContext(patch.object(self.PositionApi, 'flags_to_int', side_effect=self.game_api().flags_to_int, create=True))
        self.enterContext(patch.object(self.PositionApi, 'get_trust', side_effect=lambda e: getattr(e, 'trust', 0) or e.level))
        self.enterContext(patch.object(self.PositionApi, 'is_immortal', side_effect=lambda e: _CharacterApi.is_immortal(e)))
        self.enterContext(patch.object(_CharacterApi, 'can_see_room', side_effect=self.PositionApi.can_see_room, create=True))
        self.enterContext(patch.dict(sys.modules, {'game.Equipped': _module('game.Equipped', Equipped=self.Equipped)}))
        created = []
        def create(_prototype):
            portal = SimpleNamespace(id='portal-' + str(len(created)), name='a portal', short_description='a portal')
            created.append(portal)
            return portal
        self.enterContext(patch.object(SpellApi.create_portals.__globals__['ItemFactory'], 'create', side_effect=create, create=True))
        ctx.set_alias('created_portals', created)
        return ctx, source, destination, rooms

    def test_portal_nexus_components_timers_endpoints_and_same_room(self):
        for name, count, timer in [('portal', 1, 4), ('nexus', 2, 6)]:
            for immortal in (False, True):
                with self.subTest(spell=name, immortal=immortal):
                    ctx, source, destination, _ = self.travel_context(name, 51)
                    stone = SimpleNamespace(id='stone', name='warp stone', item_type='warp_stone')
                    self.Equipped.equip_item(ctx.actor, stone, 'held')
                    with patch.object(_CharacterApi, 'is_immortal', return_value=immortal):
                        self.assertTrue(self.api.execute_lambdas(ctx))
                    self.assertIsNone(ctx.actor.equipped.held)
                    self.assertNotIn(stone, ctx.actor.loot)
                    self.effects.remove_item_effects.assert_called_with(ctx.actor, stone)
                    portals = ctx.get_alias('created_portals')
                    self.assertEqual(count, len(portals))
                    self.assertTrue(all(p.timer == timer for p in portals))
                    self.assertEqual('200', portals[0].value3)
                    self.assertIs(portals[0], source.contents[portals[0].id])
                    if count == 2:
                        self.assertEqual('100', portals[1].value3)
                        self.assertIs(portals[1], destination.contents[portals[1].id])
                        self.assertEqual('a portal rises up from the ground.\r\n', ctx.payloads[-1]['to_room'])
                        self.assertIn(ctx.victim, ctx.payloads[-1]['targets'])
                    self.assertIn('It flares brightly and vanishes!', ctx.payloads[0]['to_char'])
                    self.assertEqual('a portal rises up before you.\r\n', ctx.payloads[2]['to_char'])
        ctx, source, destination, _ = self.travel_context('nexus', 1)
        ctx.victim.level = 1
        destination.remove_player_from_room(ctx.victim)
        ctx.victim.room_id = source.id
        source.add_player_to_room(ctx.victim)
        with patch.object(_CharacterApi, 'is_immortal', return_value=True):
            self.assertTrue(self.api.execute_lambdas(ctx))
        self.assertEqual(1, len(ctx.get_alias('created_portals')))
        self.assertEqual(1, ctx.get_alias('created_portals')[0].timer)
        self.assertEqual('100', ctx.get_alias('created_portals')[0].value3)

    def test_portal_component_guard_immortal_exemption_and_destination_guard_order(self):
        for name in ('portal', 'nexus'):
            for immortal, kind, success in [(False, None, False), (False, 'gem', False),
                                          (True, None, True), (True, 'gem', True)]:
                with self.subTest(spell=name, immortal=immortal, kind=kind):
                    ctx, _, _, _ = self.travel_context(name)
                    held = SimpleNamespace(name='gem', item_type=kind) if kind else None
                    ctx.actor.equipped.held = held
                    with patch.object(_CharacterApi, 'is_immortal', return_value=immortal):
                        self.assertEqual(success, self.api.execute_lambdas(ctx))
                    self.assertIs(held, ctx.actor.equipped.held)
                    if not success:
                        self.assertEqual('You lack the proper component for this spell.\r\n', ctx.payloads[0]['to_char'])
            for room_flag in ('ROOM_SAFE', 'ROOM_PRIVATE', 'ROOM_SOLITARY', 'ROOM_NO_RECALL'):
                ctx, _, dest, _ = self.travel_context(name)
                dest.room_flags = int(self.enums['roomFlags'][room_flag])
                stone = SimpleNamespace(name='stone', item_type='warp_stone')
                ctx.actor.equipped.held = stone
                self.assertFalse(self.api.execute_lambdas(ctx))
                self.assertIs(stone, ctx.actor.equipped.held)
                self.assertEqual([], ctx.get_alias('created_portals'))
                self.assertEqual('You failed.\r\n', ctx.payloads[0]['to_char'])

    def test_portal_nexus_gate_target_guards_and_typed_npc_saves(self):
        for name in ('portal', 'nexus', 'gate'):
            for scenario in ('missing', 'self', 'roomless', 'unseen', 'level', 'hero', 'clan', 'immune', 'saved'):
                with self.subTest(spell=name, scenario=scenario):
                    ctx, source, dest, _ = self.travel_context(name, 60)
                    ctx.actor.equipped.held = SimpleNamespace(name='stone', item_type='warp_stone')
                    if scenario == 'missing': self.api._find_world_character.return_value = None
                    if scenario == 'self': self.api._find_world_character.return_value = ctx.actor
                    if scenario == 'roomless': ctx.victim.room_id = 'missing'
                    if scenario == 'unseen':
                        dest.room_flags = int(self.enums['roomFlags'].ROOM_IMP_ONLY)
                        ctx.actor.trust = 59
                    if scenario == 'level': ctx.victim.level = 63
                    if scenario == 'hero': ctx.victim.level = int(self.enums['gameParameters'].LEVEL_HERO)
                    if scenario == 'clan': ctx.victim.guild = 'other'
                    if scenario in ('immune', 'saved'):
                        ctx.victim.is_npc = True
                        if scenario == 'immune': ctx.victim.status_flags.imm = int(self.enums['mobImmunity'].IMM_SUMMON)
                    self.api.saves_spell = Mock(return_value=scenario == 'saved')
                    self.assertFalse(self.api.execute_lambdas(ctx))
                    self.assertEqual('source', ctx.actor.room_id)
                    self.assertEqual([], ctx.get_alias('created_portals'))
                    self.assertIsNotNone(ctx.actor.equipped.held)
                    if scenario == 'saved':
                        self.api.saves_spell.assert_called_once_with(ctx, 'DAM_OTHER' if name == 'gate' else 'DAM_NONE')
                    elif scenario != 'clan':
                        self.api.saves_spell.assert_not_called()

    def test_gate_pet_moves_only_when_initially_colocated_and_not_on_failure(self):
        for colocated in (False, True):
            ctx, source, destination, _ = self.travel_context('gate')
            pet = self.effect_room_member('Pet', npc=True)
            pet.room_id, pet.area_id = (source.id, source.area_id) if colocated else (destination.id, destination.area_id)
            (source if colocated else destination).add_mobile_to_room(pet)
            ctx.actor.pet = pet
            self.assertTrue(self.api.execute_lambdas(ctx))
            self.assertEqual(destination.id, ctx.actor.room_id)
            self.assertEqual(destination.id, pet.room_id)
            self.assertNotIn(ctx.actor.id, source.characters)
            self.assertNotIn(pet.id, source.mobiles)
            pet_departures = [p for p in ctx.payloads if p.get('to_room') == 'Pet steps through a gate and vanishes.\r\n']
            self.assertEqual(1 if colocated else 0, len(pet_departures))
            self.assertEqual('You step through a gate and vanish.\r\n', ctx.payloads[1]['to_victim'])
            self.assertEqual('Caster has arrived through a gate.\r\n', ctx.payloads[2]['to_room'])
            self.assertIs(ctx.actor, ctx.payloads[3]['view_character'])
        ctx, source, destination, _ = self.travel_context('gate')
        pet = self.effect_room_member('Pet', npc=True)
        pet.room_id = source.id
        source.add_mobile_to_room(pet)
        ctx.actor.pet = pet
        destination.room_flags = int(self.enums['roomFlags'].ROOM_SAFE)
        self.assertFalse(self.api.execute_lambdas(ctx))
        self.assertEqual(source.id, ctx.actor.room_id)
        self.assertEqual(source.id, pet.room_id)
        self.assertIs(pet, source.mobiles[pet.id])

    def test_portal_nexus_gate_source_restrictions_and_npc_clan_save_order(self):
        for name in ('portal', 'nexus', 'gate'):
            for flag in ('ROOM_SAFE', 'ROOM_IMP_ONLY', 'ROOM_NO_RECALL'):
                with self.subTest(spell=name, flag=flag):
                    ctx, source, destination, _ = self.travel_context(name)
                    source.room_flags = int(self.enums['roomFlags'][flag])
                    with patch.object(_CharacterApi, 'is_immortal', return_value=True):
                        self.assertEqual(name != 'nexus' and flag != 'ROOM_NO_RECALL', self.api.execute_lambdas(ctx))
            ctx, source, destination, _ = self.travel_context(name)
            ctx.victim.is_npc = True
            ctx.victim.guild = 'other'
            self.api.saves_spell = Mock(return_value=False)
            self.assertFalse(self.api.execute_lambdas(ctx))
            self.assertEqual(0 if name == 'gate' else 1, self.api.saves_spell.call_count)
            self.assertEqual([], ctx.get_alias('created_portals'))

    def test_room_visibility_flags_levels_clans_and_privacy_match_reference(self):
        ctx, _, _, _ = self.travel_context('teleport')
        actor = ctx.actor
        with patch.object(_CharacterApi, 'is_immortal', side_effect=lambda e: (e.trust or e.level) >= 55):
            for flag, level, allowed in [('ROOM_IMP_ONLY', 59, False), ('ROOM_IMP_ONLY', 60, True),
                    ('ROOM_GODS_ONLY', 54, False), ('ROOM_GODS_ONLY', 55, True),
                    ('ROOM_HEROES_ONLY', 51, False), ('ROOM_HEROES_ONLY', 55, True),
                    ('ROOM_NEWBIES_ONLY', 5, True), ('ROOM_NEWBIES_ONLY', 6, False),
                    ('ROOM_NEWBIES_ONLY', 55, True)]:
                with self.subTest(flag=flag, level=level):
                    room = self.TravelRoom(room_flags=int(self.enums['roomFlags'][flag]))
                    actor.level = level
                    self.assertEqual(allowed, self.PositionApi.can_see_room(actor, room))
            room = self.TravelRoom(clan='loner')
            self.assertEqual('loner', room.clan)
            actor.level, actor.guild = 40, 'other'
            self.assertFalse(self.PositionApi.can_see_room(actor, room))
            actor.guild = 'loner'
            self.assertTrue(self.PositionApi.can_see_room(actor, room))
            actor.level, actor.guild = 55, 'other'
            self.assertTrue(self.PositionApi.can_see_room(actor, room))
        flags = self.enums['roomFlags']
        room = self.TravelRoom(room_flags=int(flags.ROOM_PRIVATE))
        self.assertFalse(room.is_private(flags))
        room.mobiles.update(a=object(), b=object())
        self.assertTrue(room.is_private(flags))
        room.mobiles.pop('b')
        self.assertFalse(room.is_private(flags))
        room.room_flags = int(flags.ROOM_SOLITARY)
        self.assertTrue(room.is_private(flags))
        room.mobiles.clear()
        self.assertFalse(room.is_private(flags))
        room.owner = 'Someone'
        self.assertTrue(room.is_private(flags))
        room.owner, room.room_flags = '', int(flags.ROOM_IMP_ONLY)
        self.assertTrue(room.is_private(flags))

    def test_summon_protected_targets_reject_before_npc_save(self):
        for scenario in ('level', 'immortal', 'shop', 'nosummon', 'aggressive', 'fighting', 'immune', 'saved'):
            with self.subTest(scenario=scenario):
                ctx, source, destination, _ = self.travel_context('summon', 60)
                if scenario == 'level': ctx.victim.level = 63
                if scenario == 'immortal': ctx.victim.level = int(self.enums['gameParameters'].LEVEL_IMMORTAL)
                if scenario == 'fighting': ctx.victim.fighting = ctx.actor
                if scenario == 'nosummon': ctx.victim.status_flags.act = int(self.enums['playerActBits'].PLR_NOSUMMON)
                if scenario in ('shop', 'aggressive', 'immune', 'saved'):
                    ctx.victim.is_npc = True
                    ctx.victim.vnum = '999'
                    if scenario == 'shop': ctx.handler.registry_service.shop_registry.find_by_keeper_vnum.return_value = object()
                    if scenario == 'aggressive': ctx.victim.status_flags.act = int(self.enums['actBits'].ACT_AGGRESSIVE)
                    if scenario == 'immune': ctx.victim.status_flags.imm = int(self.enums['mobImmunity'].IMM_SUMMON)
                self.api.saves_spell = Mock(return_value=scenario == 'saved')
                self.assertFalse(self.api.execute_lambdas(ctx))
                self.assertEqual(destination.id, ctx.victim.room_id)
                self.assertEqual('You failed.\r\n', ctx.payloads[0]['to_char'])
                if scenario != 'saved': self.api.saves_spell.assert_not_called()

    def test_summon_valid_target_moves_then_receives_summoner_notice_and_look(self):
        ctx, source, destination, _ = self.travel_context('summon', 40)
        ctx.victim.level = 42
        self.assertTrue(self.api.execute_lambdas(ctx))
        self.assertEqual(source.id, ctx.victim.room_id)
        self.assertNotIn(ctx.victim.id, destination.characters)
        self.assertIs(ctx.victim, source.characters[ctx.victim.id])
        self.assertEqual('Target disappears suddenly.\r\n', ctx.payloads[0]['to_room'])
        self.assertEqual('Target arrives suddenly.\r\n', ctx.payloads[1]['to_room'])
        self.assertIn(ctx.actor, ctx.payloads[1]['targets'])
        self.assertEqual('Caster has summoned you!\r\n', ctx.payloads[2]['to_victim'])
        self.assertIs(ctx.victim, ctx.payloads[3]['view_character'])

    def test_teleport_caster_target_combat_matrix_and_minus_five_save(self):
        for npc in (False, True):
            for self_target in (False, True):
                for fighting in (False, True):
                    with self.subTest(npc=npc, self_target=self_target, fighting=fighting):
                        ctx, source, destination, _ = self.travel_context('teleport', 23)
                        ctx.actor.is_npc = npc
                        if npc:
                            source.remove_player_from_room(ctx.actor)
                            source.add_mobile_to_room(ctx.actor)
                        if self_target: ctx.set_target(ctx.actor)
                        ctx.victim.fighting = object() if fighting else None
                        self.api.random_room = Mock(return_value=destination if self_target else source)
                        self.api.saves_spell = Mock(return_value=False)
                        allowed = npc or not fighting
                        self.assertEqual(allowed, self.api.execute_lambdas(ctx))
                        if allowed:
                            self.assertEqual(destination.id if self_target else source.id, ctx.victim.room_id)
                        else:
                            self.api.random_room.assert_not_called()
                        if allowed and not self_target:
                            self.api.saves_spell.assert_called_once_with(ctx, 'DAM_OTHER', level_adjust=-5)
                        else:
                            self.api.saves_spell.assert_not_called()

    def test_random_room_filters_visibility_owner_flags_and_law_but_allows_no_recall(self):
        for npc, aggressive, law_allowed in [(False, False, False), (False, True, True), (True, False, True)]:
            with self.subTest(npc=npc, aggressive=aggressive):
                ctx, _, _, rooms = self.travel_context('teleport')
                victim = ctx.victim
                victim.is_npc = npc
                if aggressive: victim.status_flags.act = int(self.enums['actBits'].ACT_AGGRESSIVE)
                rooms.clear()
                for flag in ('ROOM_SAFE', 'ROOM_PRIVATE', 'ROOM_SOLITARY', 'ROOM_IMP_ONLY', 'ROOM_LAW', 'ROOM_NO_RECALL'):
                    rooms.append(self.TravelRoom(id=flag, room_flags=int(self.enums['roomFlags'][flag])))
                rooms.append(self.TravelRoom(id='owned', owner='Someone'))
                with patch('random.choice', side_effect=lambda candidates: candidates[0]) as choice:
                    self.api.random_room(ctx)
                self.assertEqual((['ROOM_LAW'] if law_allowed else []) + ['ROOM_NO_RECALL'],
                                 [r.id for r in choice.call_args.args[0]])

    def test_teleport_immunity_saved_target_and_source_rejections_precede_randomness(self):
        for scenario in ('source', 'immune', 'saved'):
            with self.subTest(scenario=scenario):
                ctx, _, destination, _ = self.travel_context('teleport', 23)
                if scenario == 'source': destination.room_flags = int(self.enums['roomFlags'].ROOM_NO_RECALL)
                if scenario == 'immune': ctx.victim.status_flags.imm = int(self.enums['mobImmunity'].IMM_SUMMON)
                self.api.saves_spell = Mock(return_value=scenario == 'saved')
                self.api.random_room = Mock()
                self.assertFalse(self.api.execute_lambdas(ctx))
                self.api.random_room.assert_not_called()
                self.assertEqual(destination.id, ctx.victim.room_id)
                if scenario == 'saved': self.api.saves_spell.assert_called_once_with(ctx, 'DAM_OTHER', level_adjust=-5)
                else: self.api.saves_spell.assert_not_called()

    def test_teleport_same_room_selection_still_emits_notices_and_automatic_look(self):
        ctx, _, destination, _ = self.travel_context('teleport')
        self.api.random_room = Mock(return_value=destination)
        self.assertTrue(self.api.execute_lambdas(ctx))
        self.assertEqual('You have been teleported!\r\n', ctx.payloads[0]['to_victim'])
        self.assertEqual('Target vanishes!\r\n', ctx.payloads[1]['to_room'])
        self.assertEqual('Target slowly fades into existence.\r\n', ctx.payloads[2]['to_room'])
        self.assertIs(ctx.victim, ctx.payloads[3]['view_character'])

    def test_recall_charges_caster_stops_both_and_preserves_same_room_side_effects(self):
        for same_room in (False, True):
            with self.subTest(same_room=same_room):
                ctx, source, temple, _ = self.travel_context('word of recall')
                temple.vnum = '3001'
                if same_room:
                    source.remove_player_from_room(ctx.actor)
                    ctx.actor.room_id = temple.id
                    temple.add_player_to_room(ctx.actor)
                    ctx.room = temple
                else:
                    temple.remove_player_from_room(ctx.victim)
                    ctx.victim.room_id = source.id
                    source.add_player_to_room(ctx.victim)
                victim = ctx.victim
                victim.fighting = ctx.actor
                victim.movement = 47
                self.fight.stop_fighting = Mock()
                self.assertTrue(self.api.execute_lambdas(ctx))
                self.fight.stop_fighting.assert_called_once_with(victim, both=True)
                self.assertEqual(40, ctx.actor.movement)
                self.assertEqual(47, victim.movement)
                self.assertEqual(temple.id, victim.room_id)
                self.assertEqual('Target disappears.\r\n', ctx.payloads[0]['to_room'])
                self.assertEqual('Target appears in the room.\r\n', ctx.payloads[1]['to_room'])
                self.assertIs(victim, ctx.payloads[-1]['view_character'])

    def test_recall_failures_address_victim_without_charging_or_stopping_combat(self):
        for scenario in ('npc', 'missing', 'no_recall', 'curse'):
            with self.subTest(scenario=scenario):
                ctx, _, temple, rooms = self.travel_context('word of recall')
                temple.vnum = '3001'
                if scenario == 'npc': ctx.victim.is_npc = True
                if scenario == 'missing': rooms.remove(temple)
                if scenario == 'no_recall': temple.room_flags = int(self.enums['roomFlags'].ROOM_NO_RECALL)
                if scenario == 'curse': ctx.victim.status_flags.affected_by = int(self.enums['affectedBy'].AFF_CURSE)
                self.fight.stop_fighting = Mock()
                self.assertFalse(self.api.execute_lambdas(ctx))
                self.assertEqual(81, ctx.actor.movement)
                self.fight.stop_fighting.assert_not_called()
                if scenario == 'npc': self.assertEqual([], ctx.payloads)
                else:
                    self.assertEqual(1, len(ctx.payloads))
                    self.assertIs(ctx.victim, ctx.payloads[0]['victim'])
                    self.assertEqual('You are completely lost.\r\n' if scenario == 'missing' else 'Spell failed.\r\n',
                                     ctx.payloads[0]['to_victim'])
                    self.assertNotIn('to_char', ctx.payloads[0])

    def test_farsight_scans_exits_depth_closed_doors_visibility_and_invalid_names(self):
        ctx, source, destination, rooms = self.travel_context('farsight')
        ctx.target_name = 'north'
        previous = source
        for depth in range(1, 5):
            room = destination if depth == 1 else self.TravelRoom(id='north' + str(depth), area_id='area2')
            if depth > 1: rooms.append(room)
            previous.exits.append(SimpleNamespace(direction=0, to_room_id=room.id, to_room_vnum='', exit_flags=2))
            if depth > 1:
                entity = self.effect_room_member('Depth' + str(depth))
                room.add_player_to_room(entity)
            previous = room
        hidden = self.effect_room_member('Hidden')
        destination.add_player_to_room(hidden)
        with patch.object(_CharacterApi, 'can_see', side_effect=lambda viewer, target, room: target is not hidden) as visible:
            self.assertTrue(self.api.execute_lambdas(ctx))
        self.assertTrue(all(c.args[2] is source for c in visible.call_args_list))
        lines = [p['to_char'] for p in ctx.payloads if 'to_char' in p]
        self.assertEqual('You peer intently north.\r\n', lines[0])
        self.assertIn('Target, nearby to the north.\r\n', lines)
        self.assertIn('Depth2, not far north.\r\n', lines)
        self.assertIn('Depth3, off in the distance north.\r\n', lines)
        self.assertFalse(any('Depth4' in line for line in lines))
        self.assertFalse(any('Hidden' in line for line in lines))
        ctx.done = ctx.performed = False
        ctx.payloads.clear()
        ctx.target_name = 'Target'
        self.api._find_world_character.reset_mock()
        self.api.execute_lambdas(ctx)
        self.assertEqual([{'to_char': 'Which way do you want to scan?\r\n'}], ctx.payloads)
        self.api._find_world_character.assert_not_called()

    def test_farsight_no_argument_and_blind_guard(self):
        for blind in (False, True):
            with self.subTest(blind=blind):
                ctx, source, destination, _ = self.travel_context('farsight')
                source.exits.append(SimpleNamespace(direction=1, to_room_id=destination.id, to_room_vnum=''))
                ctx.target_name = ''
                if blind: ctx.actor.status_flags.affected_by = int(self.enums['affectedBy'].AFF_BLIND)
                self.api.execute_lambdas(ctx)
                if blind:
                    self.assertEqual([{'to_char': 'Maybe it would help if you could see?\r\n'}], ctx.payloads)
                else:
                    lines = [p['to_char'] for p in ctx.payloads if 'to_char' in p]
                    self.assertEqual('Looking around you see:\r\n', lines[0])
                    self.assertIn('source-observer, right here.\r\n', lines)
                    self.assertIn('Target, nearby to the east.\r\n', lines)

    def test_charm_transfers_following_pet_and_group_relationships_before_affect(self):
        for previous_master in (False, True):
            for visible in (False, True):
                with self.subTest(previous_master=previous_master, visible=visible):
                    ctx = self.live_effect_context('charm person', 23)
                    old = self.effect_room_member('Old')
                    if previous_master:
                        ctx.victim.master = ctx.victim.leader = old
                        old.pet = ctx.victim
                    self.fight.multi_hit = Mock()
                    self.fight.check_killer = Mock()
                    trace = []
                    apply = self.api.effect_handler.apply_spell_effects
                    def check_relationships(*args, **kwargs):
                        trace.append((ctx.victim.master is ctx.actor, ctx.victim.leader is ctx.actor))
                        return apply(*args, **kwargs)
                    with patch.object(_CharacterApi, 'can_see', return_value=visible), \
                            patch.object(self.api.effect_handler, 'apply_spell_effects', side_effect=check_relationships):
                        self.assertTrue(self.api.execute_lambdas(ctx))
                    self.assertEqual([(True, True)], trace)
                    self.assertIs(ctx.actor, ctx.victim.master)
                    self.assertIs(ctx.actor, ctx.victim.leader)
                    if previous_master:
                        self.assertIsNone(old.pet)
                    self.assertEqual('spell.charm_person', ctx.victim.effects[0].type)
                    self.assertTrue(ctx.victim.status_flags.affected_by & int(self.enums['affectedBy'].AFF_CHARM))
                    messages = [p.get('to_victim', '') for p in ctx.payloads]
                    self.assertEqual(previous_master and visible, 'Target stops following you.\r\n' in messages)
                    self.assertEqual(visible, 'Target now follows you.\r\n' in messages)
                    self.assertIn('You now follow Caster.\r\n', messages)
                    self.assertEqual("Isn't Caster just so nice?\r\n", ctx.payloads[-1]['to_victim'])
                    self.assertEqual('Target looks at you with adoring eyes.\r\n', ctx.payloads[-1]['to_char'])
                    self.api.start_offensive_combat(ctx)
                    self.fight.multi_hit.assert_not_called()

    def test_change_sex_success_messages_follow_the_new_sex_and_skip_saved_targets(self):
        for self_target in (False, True):
            for saved in (False, True):
                with self.subTest(self_target=self_target, saved=saved):
                    ctx = self.live_effect_context('change sex')
                    if self_target:
                        ctx.set_target(ctx.actor)
                    victim = ctx.victim
                    victim.him_her = lambda: 'her' if victim.sex == '2' else 'him'
                    self.api.saves_spell = Mock(return_value=saved)
                    with patch('random.randint', return_value=2):
                        self.assertEqual(not saved, self.api.execute_lambdas(ctx))
                    if saved:
                        self.assertEqual([], ctx.payloads)
                        self.assertEqual('1', victim.sex)
                    else:
                        self.assertEqual('2', victim.sex)
                        self.assertEqual('You feel different.\r\n', ctx.payloads[0]['to_victim'])
                        self.assertEqual(victim.name + " doesn't look like herself anymore...\r\n",
                                         ctx.payloads[0]['to_room'])
                        self.assertNotIn(victim, ctx.payloads[0]['targets'])

    def test_charmed_npc_is_grouped_and_does_not_retaliate_against_new_master(self):
        ctx = self.live_effect_context('charm person', 23)
        ctx.victim.is_npc = True
        self.fight.multi_hit = Mock()
        self.assertTrue(self.api.execute_lambdas(ctx))
        self.assertIs(ctx.actor, ctx.victim.master)
        self.assertIs(ctx.actor, ctx.victim.leader)
        self.assertEqual(1, len(ctx.victim.effects))
        self.assertTrue(all(p.get('victim') is not ctx.victim for p in ctx.payloads))
        self.api.start_offensive_combat(ctx)
        self.fight.multi_hit.assert_not_called()

    def test_haste_duration_uses_effective_level_and_self_other_identity(self):
        for self_target in (False, True):
            with self.subTest(self_target=self_target):
                ctx = self.live_effect_context('haste', 23)
                ctx.actor.level = 80
                ctx.victim.character_attributes.dexterity = 15
                if self_target:
                    ctx.actor.character_attributes.dexterity = 15
                    ctx.set_target(ctx.actor)
                self.assertTrue(self.api.execute_lambdas(ctx))
                effect = ctx.victim.effects[0]
                self.assertEqual((23, 11 if self_target else 5, 2), (effect.level, effect.duration, effect.modifier))
                self.assertEqual(17, ctx.victim.character_attributes.dexterity)
                self.assertEqual('level/4', self.api.effect_handler.as_effect(ctx.spell.affect_data[0]).duration)
                self.api.effect_handler.affect_strip(ctx.victim, 'spell.haste')
                self.assertEqual(15, ctx.victim.character_attributes.dexterity)

    def test_poison_character_duration_join_save_and_restoration_use_content(self):
        for saved in (False, True):
            with self.subTest(saved=saved):
                ctx = self.live_effect_context('poison', 23)
                ctx.victim.character_attributes.strength = 15
                self.api.saves_spell = Mock(return_value=saved)
                self.assertEqual(not saved, self.api.execute_lambdas(ctx))
                self.api.saves_spell.assert_called_once_with(ctx, 'DAM_POISON')
                if saved:
                    self.assertEqual([], ctx.victim.effects)
                    self.assertEqual(15, ctx.victim.character_attributes.strength)
                    self.assertEqual('You feel momentarily ill, but it passes.\r\n', ctx.payloads[0]['to_victim'])
                else:
                    effect = ctx.victim.effects[0]
                    self.assertEqual((23, 23, -2), (effect.level, effect.duration, effect.modifier))
                    self.assertEqual(13, ctx.victim.character_attributes.strength)
                    self.assertEqual('You feel very sick.\r\n', ctx.payloads[0]['to_victim'])
                    ctx.performed = False
                    self.assertTrue(self.api.execute_lambdas(ctx))
                    self.assertEqual(1, len(ctx.victim.effects))
                    self.assertEqual((23, 46, -4), (ctx.victim.effects[0].level,
                                     ctx.victim.effects[0].duration, ctx.victim.effects[0].modifier))
                    self.api.effect_handler.affect_strip(ctx.victim, 'spell.poison')
                    self.assertEqual(15, ctx.victim.character_attributes.strength)
                self.assertNotIn(ctx.victim, ctx.payloads[0]['targets'])
                self.assertIn(ctx.actor, ctx.payloads[0]['targets'])

    def test_fog_strips_all_concealment_sources_but_preserves_saved_and_immortal_targets(self):
        from tests.test_effect_util_affects import _load_effect_runtime
        _, Effect, _, _ = _load_effect_runtime()
        ctx = self.live_effect_context('faerie fog', 23)
        saved = self.effect_room_member('Saved')
        immortal = self.effect_room_member('Immortal')
        immortal.status_flags.invis_level = 1
        ctx.room.characters.update(saved=saved, immortal=immortal)
        hide = int(self.enums['affectedBy'].AFF_HIDE)
        invisible = int(self.enums['affectedBy'].AFF_INVISIBLE)
        sneak = int(self.enums['affectedBy'].AFF_SNEAK)
        flying = int(self.enums['affectedBy'].AFF_FLYING)
        for entity in (ctx.actor, ctx.victim, saved, immortal):
            entity.status_flags.affected_by = hide | invisible | sneak | flying
            for effect_type in ('spell.invis', 'spell.mass_invis', 'skill.sneak', 'sneak', 'spell.other'):
                entity.effects.append(Effect(type=effect_type, where='TO_AFFECTS', level=40,
                    duration=10, location='APPLY_NONE', modifier=0, bitvector=0))
        self.api.saves_spell = Mock(side_effect=lambda scoped, *args, **kwargs: scoped.victim is saved)
        self.assertTrue(self.api.execute_lambdas(ctx))
        self.assertEqual([ctx.victim, saved], [c.args[0].victim for c in self.api.saves_spell.call_args_list])
        self.assertEqual(['spell.other'], [e.type for e in ctx.victim.effects])
        self.assertEqual(flying, ctx.victim.status_flags.affected_by)
        for entity in (ctx.actor, saved, immortal):
            self.assertEqual(5, len(entity.effects))
            self.assertEqual(hide | invisible | sneak | flying, entity.status_flags.affected_by)
        self.assertEqual('You conjure a cloud of purple smoke.\r\n', ctx.payloads[0]['to_char'])
        self.assertEqual('You are revealed!\r\n', ctx.payloads[1]['to_victim'])
        self.assertEqual('Target is revealed!\r\n', ctx.payloads[1]['to_room'])
        self.assertNotIn(ctx.victim, ctx.payloads[1]['targets'])
        self.assertIn(ctx.actor, ctx.payloads[1]['targets'])

    def test_dispel_collection_order_level_bonus_and_excluded_ailments(self):
        expected = ['armor', 'bless', 'blindness', 'calm', 'change_sex', 'charm_person', 'chill_touch',
                    'curse', 'detect_evil', 'detect_good', 'detect_hidden', 'detect_invis', 'detect_magic',
                    'faerie_fire', 'fly', 'frenzy', 'giant_strength', 'haste', 'infravision', 'invis',
                    'mass_invis', 'pass_door', 'protection_evil', 'protection_good', 'sanctuary',
                    'shield', 'sleep', 'slow', 'stone_skin', 'weaken']
        for name, level in [('cancellation', 25), ('dispel magic', 23)]:
            with self.subTest(spell=name):
                ctx = self.guard_context(name, 23)
                self.effects.reset_mock()
                self.effects.dispel_effects.return_value = []
                self.api.saves_spell = Mock(return_value=False)
                self.assertFalse(self.api.execute_lambdas(ctx))
                calls = self.effects.dispel_effects.call_args_list
                self.assertEqual(['spell.' + s for s in expected], [c.args[2] for c in calls])
                self.assertTrue(all(c.args[:2] == (level, ctx.victim) for c in calls))
                self.assertEqual(1 if name == 'dispel magic' else 0, self.api.saves_spell.call_count)
                self.assertEqual('Spell failed.\r\n', ctx.payloads[-1]['to_char'])

    def test_dispel_raw_sanctuary_fallback_rolls_after_record_and_only_for_dispel_magic(self):
        from tests.test_effect_util_affects import _load_effect_runtime
        _, Effect, _, _ = _load_effect_runtime()
        for name in ('cancellation', 'dispel magic'):
            for record in (False, True):
                for resisted in (False, True):
                    with self.subTest(spell=name, record=record, resisted=resisted):
                        ctx = self.live_effect_context(name, 23)
                        flag = int(self.enums['affectedBy'].AFF_SANCTUARY)
                        ctx.victim.status_flags.affected_by = flag
                        if record:
                            ctx.victim.effects.append(Effect(type='spell.sanctuary', where='TO_AFFECTS',
                                level=50, duration=10, location='APPLY_NONE', modifier=0, bitvector='AFF_SANCTUARY'))
                        util = self.api.effect_handler.dispel_effects.__globals__['EffectUtil']
                        calls = []
                        def save(level, effect_level, duration):
                            calls.append((level, effect_level, duration))
                            return True if duration == 10 else resisted
                        with patch.object(util, 'saves_dispel', side_effect=save), \
                                patch.object(SpellApi.dispel_flag.__globals__['EffectUtil'], 'saves_dispel', side_effect=save, create=True):
                            removed = self.api.execute_lambdas(ctx)
                        self.assertEqual(name == 'dispel magic' and not record and not resisted, removed)
                        expected = [(25 if name == 'cancellation' else 23, 50, 10)] if record else []
                        if name == 'dispel magic':
                            expected.append((23, 23, -1))
                        self.assertEqual(expected, calls)
                        self.assertEqual(0 if removed else flag, ctx.victim.status_flags.affected_by)
                        if record:
                            self.assertEqual(49, ctx.victim.effects[0].level)

    def test_dispel_live_records_messages_and_excluded_poison_plague(self):
        from tests.test_effect_util_affects import _load_effect_runtime
        _, Effect, _, _ = _load_effect_runtime()
        for name in ('cancellation', 'dispel magic'):
            with self.subTest(spell=name):
                ctx = self.live_effect_context(name, 23)
                spellbook = {name: Spell.from_json(dict(doc, levelByClass={}, ratingByClass={}))
                             for name, doc in self.documents.items()}
                ctx.handler.spell_registry = SimpleNamespace(all_spells=lambda: list(spellbook.values()))
                ctx.victim.saving_throw = 5
                ctx.victim.character_attributes.dexterity = 15
                for effect in ('curse', 'haste'):
                    self.api.effect_handler.apply_spell_effects(ctx.actor, ctx.victim, spellbook[effect], caster_level=40)
                for effect in ('plague', 'poison'):
                    ctx.victim.effects.append(Effect(type='spell.' + effect, where='TO_AFFECTS',
                        level=40, duration=10, location='APPLY_NONE', modifier=0, bitvector=0))
                util = self.api.effect_handler.dispel_effects.__globals__['EffectUtil']
                with patch.object(util, 'saves_dispel', return_value=False) as saves:
                    self.assertTrue(self.api.execute_lambdas(ctx))
                self.assertEqual(2, saves.call_count)
                self.assertTrue(all(c.args[0] == (25 if name == 'cancellation' else 23) for c in saves.call_args_list))
                self.assertEqual(['spell.plague', 'spell.poison'], [e.type for e in ctx.victim.effects])
                self.assertEqual((10, 5, 15), (ctx.victim.hit_roll, ctx.victim.saving_throw,
                                               ctx.victim.character_attributes.dexterity))
                victim_text = [p['to_victim'] for p in ctx.payloads if 'to_victim' in p]
                self.assertEqual(['The curse wears off.\r\n', 'You feel yourself slow down.\r\n'], victim_text)
                self.assertEqual('Target is no longer moving so quickly.\r\n', ctx.payloads[-2]['to_room'])
                self.assertIn(ctx.actor, ctx.payloads[-2]['targets'])
                self.assertNotIn(ctx.victim, ctx.payloads[-2]['targets'])
                self.assertEqual('Ok.\r\n', ctx.payloads[-1]['to_char'])

    def test_worn_bless_curse_adjust_saves_and_reverse_counters_without_applying_opposite(self):
        for name, opposite, delta in [('bless', 'curse', -1), ('curse', 'bless', 1)]:
            with self.subTest(spell=name):
                ctx = self.live_effect_context(name, 23)
                wearer = ctx.actor
                wearer.saving_throw = 10
                obj = SimpleNamespace(id='ring', name='ring', item_type='armor', effects=[], extra_flags='', level=40)
                wearer.equipped = SimpleNamespace(held=obj)
                self.api.effect_handler.apply_item_effects(wearer, obj)
                ctx.set_target(obj)
                game = self.game_api()
                game.flags_to_letters = lambda raw: ''.join(chr(ord('A') + bit) for bit in range(26) if raw & (1 << bit))
                self.enterContext(patch.dict(SpellApi.character_flag.__globals__, GameApi=game))
                self.assertTrue(self.api.execute_lambdas(ctx))
                self.assertEqual(10 + delta, wearer.saving_throw)
                self.assertEqual(1, len(obj.effects))
                self.assertEqual(1, len(wearer.effects))
                self.assertEqual('spell.' + name, obj.effects[0].type)
                ctx.spell = Spell.from_json(dict(self.documents[opposite], levelByClass={}, ratingByClass={}))
                for resisted in (True, False):
                    ctx.done = ctx.performed = False
                    with patch.object(SpellApi.counter_item_flag.__globals__['EffectUtil'], 'saves_dispel',
                                      return_value=resisted, create=True) as save:
                        self.assertEqual(not resisted, self.api.execute_lambdas(ctx))
                    save.assert_called_once_with(23, 23, 0)
                    self.assertEqual(10 + delta if resisted else 10, wearer.saving_throw)
                    self.assertEqual(1 if resisted else 0, len(obj.effects))
                    self.assertEqual(1 if resisted else 0, len(wearer.effects))
                self.assertEqual('', obj.extra_flags)

    def test_worn_object_affect_expiration_and_reequip_restore_saves_exactly_once(self):
        ctx = self.live_effect_context('bless', 23)
        wearer = ctx.actor
        wearer.saving_throw = 10
        wearer.loot = []
        obj = SimpleNamespace(id='ring', name='ring', item_type='armor', effects=[], extra_flags='', level=40)
        wearer.equipped = SimpleNamespace(held=obj)
        self.api.effect_handler.apply_item_effects(wearer, obj)
        ctx.set_target(obj)
        self.assertTrue(self.api.execute_lambdas(ctx))
        self.assertEqual(9, wearer.saving_throw)
        self.api.effect_handler.remove_item_effects(wearer, obj)
        self.Equipped.unequip_item(wearer, 'held')
        self.assertEqual(10, wearer.saving_throw)
        self.Equipped.equip_item(wearer, obj, 'held')
        self.api.effect_handler.apply_item_effects(wearer, obj)
        self.assertEqual(9, wearer.saving_throw)
        obj.effects[0].duration = 0
        self.api.effect_handler.tick_effects(obj)
        self.assertEqual(10, wearer.saving_throw)
        self.assertEqual([], obj.effects)
        self.assertEqual([], wearer.effects)
        self.api.effect_handler.remove_item_effects(wearer, obj)
        self.assertEqual(10, wearer.saving_throw)

    def test_cure_content_resists_weakens_and_removes_only_matching_ailment(self):
        from tests.test_effect_util_affects import _load_effect_runtime
        _, Effect, _, _ = _load_effect_runtime()
        for name, ailment, notice in [('cure blindness', 'blindness', 'Your vision returns!'),
                ('cure disease', 'plague', 'Your sores vanish.'),
                ('cure poison', 'poison', 'A warm feeling runs through your body.')]:
            for self_target in (False, True):
                for resisted in (False, True):
                    with self.subTest(spell=name, self_target=self_target, resisted=resisted):
                        ctx = self.live_effect_context(name, 23)
                        if self_target:
                            ctx.set_target(ctx.actor)
                        ctx.victim.his_her = lambda: 'her'
                        ailment_effect = Effect(type='spell.' + ailment, level=70, duration=10,
                                                where='TO_AFFECTS', location='APPLY_NONE', modifier=0, bitvector=0)
                        other = Effect(type='spell.other', level=70, duration=10,
                                       where='TO_AFFECTS', location='APPLY_NONE', modifier=0, bitvector=0)
                        ctx.victim.effects.extend([ailment_effect, other])
                        util = self.api.effect_handler.dispel_effects.__globals__['EffectUtil']
                        with patch.object(util, 'saves_dispel', return_value=resisted) as save:
                            self.assertEqual(not resisted, self.api.execute_lambdas(ctx))
                        save.assert_called_once_with(23, 70, 10)
                        remaining = {effect.type: effect for effect in ctx.victim.effects}
                        self.assertEqual(70, remaining['spell.other'].level)
                        if resisted:
                            self.assertEqual(69, remaining['spell.' + ailment].level)
                            self.assertEqual([{'to_char': 'Spell failed.\r\n'}], ctx.payloads)
                        else:
                            self.assertNotIn('spell.' + ailment, remaining)
                            self.assertEqual(notice + '\r\n', ctx.payloads[0]['to_victim'])
                            self.assertIs(ctx.victim, ctx.payloads[0]['victim'])
                            self.assertNotIn(ctx.victim, ctx.payloads[0]['targets'])
                            if not self_target:
                                self.assertIn(ctx.actor, ctx.payloads[0]['targets'])
                            if ailment == 'plague':
                                self.assertIn('her sores vanish', ctx.payloads[0]['to_room'])

    def test_cure_absent_record_does_not_roll_even_with_innate_ailment_flag(self):
        for name, flag, absent in [('cure blindness', 'AFF_BLIND', "You aren't blind."),
                ('cure disease', 'AFF_PLAGUE', "You aren't ill."),
                ('cure poison', 'AFF_POISON', "You aren't poisoned.")]:
            for self_target in (False, True):
                with self.subTest(spell=name, self_target=self_target):
                    ctx = self.guard_context(name)
                    if self_target:
                        ctx.set_target(ctx.actor)
                    ctx.victim.status_flags.affected_by = int(self.enums['affectedBy'][flag])
                    self.effects.reset_mock()
                    self.assertFalse(self.api.execute_lambdas(ctx))
                    self.effects.dispel_effects.assert_not_called()
                    self.effects.affect_strip.assert_not_called()
                    self.assertEqual(1, len(ctx.payloads))
                    if self_target:
                        self.assertEqual(absent + '\r\n', ctx.payloads[0]['to_char'])
                    else:
                        self.assertIn("Target doesn't appear", ctx.payloads[0]['to_char'])

    def test_remove_curse_carried_order_level_and_first_success_feedback(self):
        for self_target in (False, True):
            for character_cured in (False, True):
                with self.subTest(self_target=self_target, character_cured=character_cured):
                    ctx = self.guard_context('remove curse', 23)
                    if self_target:
                        ctx.set_target(ctx.actor)
                    flags = self.enums['itemFlags']
                    def item(name, bits):
                        return SimpleNamespace(name=name, level=40, item_type='armor', extra_flags=int(bits))
                    clean = item('clean', 0)
                    permanent = item('permanent', flags.ITEM_NODROP | flags.ITEM_NOUNCURSE)
                    failed = item('failed', flags.ITEM_NOREMOVE)
                    first = item('first', flags.ITEM_NODROP | flags.ITEM_NOREMOVE)
                    untouched = item('untouched', flags.ITEM_NODROP)
                    ctx.victim.owned_items = lambda: [clean, permanent, failed, first, untouched]
                    self.effects.dispel_effects.return_value = [SimpleNamespace(type='spell.curse')] if character_cured else []
                    with patch.object(_CharacterApi, 'get_enum', side_effect=self.enums.get, create=True), \
                            patch.object(SpellApi.uncurse_item.__globals__['EffectUtil'], 'saves_dispel',
                                         side_effect=[True, False], create=True) as save:
                        self.assertTrue(self.api.execute_lambdas(ctx))
                    self.assertEqual([(23, 40, 0), (23, 40, 0)], [c.args for c in save.call_args_list])
                    self.assertEqual(0, int(first.extra_flags))
                    self.assertNotEqual(0, int(failed.extra_flags))
                    self.assertNotEqual(0, int(untouched.extra_flags))
                    self.effects.dispel_effects.assert_called_with(23, ctx.victim, 'spell.curse')
                    self.assertEqual(2 if character_cured else 1, len(ctx.payloads))
                    self.assertEqual('Your first glows blue.\r\n', ctx.payloads[-1]['to_victim'])
                    self.assertEqual(ctx.victim.name + "'s first glows blue.\r\n", ctx.payloads[-1]['to_room'])
                    self.assertNotIn(ctx.victim, ctx.payloads[-1]['targets'])
                    if character_cured:
                        self.assertEqual('You feel better.\r\n', ctx.payloads[0]['to_victim'])

    def test_remove_curse_direct_object_keeps_bonus_and_never_attempts_character(self):
        for bits, resisted, expected in [('clean', False, "There doesn't seem to be a curse"),
                ('permanent', False, 'beyond your power'), ('cursed', True, 'beyond your power'),
                ('cursed', False, 'glows blue')]:
            with self.subTest(bits=bits, resisted=resisted):
                ctx = self.guard_context('remove curse', 23)
                flags = self.enums['itemFlags']
                raw = 0 if bits == 'clean' else int(flags.ITEM_NODROP | flags.ITEM_NOREMOVE)
                if bits == 'permanent':
                    raw |= int(flags.ITEM_NOUNCURSE)
                obj = SimpleNamespace(name='ring', item_type='armor', extra_flags=raw, level=40)
                ctx.set_target(obj)
                self.effects.reset_mock()
                with patch.object(_CharacterApi, 'get_enum', side_effect=self.enums.get, create=True), \
                        patch.object(SpellApi.uncurse_item.__globals__['EffectUtil'], 'saves_dispel',
                                     return_value=resisted, create=True) as save:
                    self.assertEqual(bits == 'cursed' and not resisted, self.api.execute_lambdas(ctx))
                if bits == 'cursed':
                    save.assert_called_once_with(25, 40, 0)
                else:
                    save.assert_not_called()
                self.effects.dispel_effects.assert_not_called()
                self.assertIn(expected, ctx.payloads[0]['to_char'])
                self.assertEqual(0 if bits == 'cursed' and not resisted else raw, int(obj.extra_flags))

    def test_remove_curse_resisted_character_still_attempts_all_resistant_items_quietly(self):
        ctx = self.guard_context('remove curse', 23)
        flag = int(self.enums['itemFlags'].ITEM_NODROP)
        items = [SimpleNamespace(name=name, item_type='armor', extra_flags=flag, level=40)
                 for name in ('first', 'second')]
        ctx.victim.owned_items = lambda: items
        self.effects.dispel_effects.return_value = []
        with patch.object(_CharacterApi, 'get_enum', side_effect=self.enums.get, create=True), \
                patch.object(SpellApi.uncurse_item.__globals__['EffectUtil'], 'saves_dispel',
                             return_value=True, create=True) as save:
            self.assertFalse(self.api.execute_lambdas(ctx))
        self.assertEqual([(23, 40, 0)] * 2, [c.args for c in save.call_args_list])
        self.assertEqual([], ctx.payloads)
        self.assertTrue(all(int(item.extra_flags) == flag for item in items))

    def live_effect_context(self, name, level=20):
        from tests.test_effect_util_affects import _load_effect_runtime
        Handler, _Effect, Generic, _Rng = _load_effect_runtime()
        ctx = self.guard_context(name, level)
        for entity in (ctx.actor, ctx.victim):
            entity.hit_roll, entity.dam_roll = 10, 20
            entity.fighting = None
            self.PositionApi.set_position(entity, 'POS_STANDING')
            entity.status_flags.assign_bitfield = lambda field, value, owner=entity: setattr(owner.status_flags, field, value)
        self.api.effect_handler = Handler(SimpleNamespace(get=self.enums.get))
        self.enterContext(patch.dict(sys.modules, {'util.GenericUtil': SimpleNamespace(GenericUtil=Generic)}))
        return ctx

    def effect_room_member(self, name, *, npc=False, level=20, leader=None):
        member = SimpleNamespace(id=name, name=name, is_npc=npc, level=level, leader=leader,
            character_attributes=SimpleNamespace(position=int(self.enums['positions'].POS_STANDING)),
            status_flags=SimpleNamespace(affected_by=0, act=0, imm=0, off=0),
            effects=[], hit_roll=10, dam_roll=20, fighting=None)
        member.status_flags.assign_bitfield = lambda field, value: setattr(member.status_flags, field, value)
        self.PositionApi.set_position(member, 'POS_STANDING')
        return member

    def test_mass_invisibility_live_group_effects_messages_and_repeat_completion(self):
        ctx = self.live_effect_context('mass invis', 21)
        ctx.victim.leader = ctx.actor
        ctx.victim.fighting = object()
        self.PositionApi.set_position(ctx.victim, 'POS_FIGHTING')
        pet = self.effect_room_member('Pet', npc=True, leader=ctx.actor)
        pet.fighting = ctx.victim
        stranger = self.effect_room_member('Stranger')
        innate = self.effect_room_member('Innate', leader=ctx.actor)
        innate.status_flags.affected_by = int(self.enums['affectedBy'].AFF_INVISIBLE)
        ctx.room.characters.update(stranger=stranger, innate=innate)
        ctx.room.mobiles = {'pet': pet}
        applied_after_messages = []
        apply = self.api.effect_handler.apply_spell_effects
        def apply_with_trace(actor, victim, spell, **kwargs):
            applied_after_messages.append((victim, len(ctx.payloads)))
            apply(actor, victim, spell, **kwargs)
        with patch.object(self.api.effect_handler, 'apply_spell_effects', side_effect=apply_with_trace):
            self.assertTrue(self.api.execute_lambdas(ctx))
        self.assertEqual([(ctx.actor, 1), (ctx.victim, 2), (pet, 3)], applied_after_messages)
        for member in (ctx.actor, ctx.victim, pet):
            self.assertEqual(1, len(member.effects))
            effect = member.effects[0]
            self.assertEqual(('spell.mass_invis', 10, 24), (effect.type, effect.level, effect.duration))
            self.assertTrue(member.status_flags.affected_by & int(self.enums['affectedBy'].AFF_INVISIBLE))
        self.assertEqual([], stranger.effects)
        self.assertEqual([], innate.effects)
        self.assertEqual(int(self.enums['positions'].POS_FIGHTING), ctx.victim.character_attributes.position)
        self.assertIs(pet.fighting, ctx.victim)
        self.assertEqual('You slowly fade out of existence.\r\n', ctx.payloads[1]['to_victim'])
        self.assertEqual('Target slowly fades out of existence.\r\n', ctx.payloads[1]['to_room'])
        self.assertIn(ctx.actor, ctx.payloads[1]['targets'])
        self.assertNotIn(ctx.victim, ctx.payloads[1]['targets'])
        self.assertEqual({'to_char': 'Ok.\r\n'}, ctx.payloads[-1])
        ctx.payloads.clear()
        ctx.performed = ctx.done = False
        self.api.execute_lambdas(ctx)
        self.assertEqual([{'to_char': 'Ok.\r\n'}], ctx.payloads)
        self.assertEqual(1, len(ctx.actor.effects))

    def test_calm_idle_room_applies_separate_pc_penalties_and_restores_stats(self):
        ctx = self.live_effect_context('calm', 21)
        self.fight.stop_fighting = Mock()
        with patch('random.randint', return_value=0) as roll:
            self.assertTrue(self.api.execute_lambdas(ctx))
        roll.assert_called_once_with(0, 84)
        self.fight.stop_fighting.assert_not_called()
        for member in (ctx.actor, ctx.victim):
            self.assertEqual((5, 15), (member.hit_roll, member.dam_roll))
            self.assertEqual(2, len(member.effects))
            self.assertEqual([-5, -5], [effect.modifier for effect in member.effects])
            self.assertTrue(all(effect.duration == 5 and effect.level == 21 for effect in member.effects))
            self.assertTrue(member.status_flags.affected_by & int(self.enums['affectedBy'].AFF_CALM))
        self.assertEqual(['A wave of calm passes over you.\r\n'] * 2,
                         [payload['to_victim'] for payload in ctx.payloads])
        for member in (ctx.actor, ctx.victim):
            self.api.effect_handler.affect_strip(member, 'spell.calm')
            self.assertEqual((10, 20, 0), (member.hit_roll, member.dam_roll, member.status_flags.affected_by))

    def test_calm_chance_counts_only_fighting_positions_and_accepts_equality(self):
        for rolled, success in [(13, False), (14, True)]:
            with self.subTest(roll=rolled):
                ctx = self.live_effect_context('calm', 10)
                ctx.victim.level = 11
                self.PositionApi.set_position(ctx.victim, 'POS_FIGHTING')
                npc = self.effect_room_member('Npc', npc=True, level=9)
                self.PositionApi.set_position(npc, 'POS_FIGHTING')
                pointer = self.effect_room_member('PointerOnly', level=100)
                pointer.fighting = ctx.victim
                ctx.room.characters['pointer'] = pointer
                ctx.room.mobiles = {'npc': npc}
                def stop(member, both):
                    member.fighting = None
                    self.PositionApi.set_position(member, 'POS_STANDING')
                self.fight.stop_fighting = Mock(side_effect=stop)
                with patch('random.randint', return_value=rolled) as roll:
                    self.assertEqual(success, self.api.execute_lambdas(ctx))
                roll.assert_called_once_with(0, 33)
                self.assertEqual({'count': 2, 'highest': 11, 'total': 14}, ctx.get_alias('combat_totals'))
                if success:
                    self.assertEqual([ctx.victim, pointer, npc], [call.args[0] for call in self.fight.stop_fighting.call_args_list])
                    self.assertTrue(all(call.kwargs == {'both': False} for call in self.fight.stop_fighting.call_args_list))
                    self.assertEqual((8, 18), (npc.hit_roll, npc.dam_roll))
                    self.assertEqual([-2, -2], [effect.modifier for effect in npc.effects])
                else:
                    self.assertEqual([], ctx.payloads)
                    self.fight.stop_fighting.assert_not_called()
                    self.assertTrue(all(not member.effects for member in (ctx.actor, ctx.victim, pointer, npc)))

    def test_calm_immortal_override_and_negative_chance_range_match_rom(self):
        for immortal in (False, True):
            with self.subTest(immortal=immortal):
                ctx = self.live_effect_context('calm', 1)
                ctx.victim.level = 100
                self.PositionApi.set_position(ctx.victim, 'POS_FIGHTING')
                npc = self.effect_room_member('Npc', npc=True, level=100)
                self.PositionApi.set_position(npc, 'POS_FIGHTING')
                ctx.room.mobiles['npc'] = npc
                self.fight.stop_fighting = Mock()
                with patch.object(_CharacterApi, 'is_immortal', return_value=immortal), patch('random.randint') as roll:
                    self.assertEqual(immortal, self.api.execute_lambdas(ctx))
                roll.assert_not_called()  # number_range(0, -92) returns its lower endpoint.
                self.assertEqual(0 if immortal else 150, ctx.get_alias('calm_threshold'))
                self.assertEqual(2 if immortal else 0, len(ctx.actor.effects))

    def test_calm_in_order_blockers_preserve_earlier_effects_and_stop_later_targets(self):
        for guard in ('IMM_MAGIC', 'ACT_UNDEAD', 'AFF_CALM', 'AFF_BERSERK', 'spell.frenzy'):
            for first in (False, True):
                with self.subTest(guard=guard, first=first):
                    ctx = self.live_effect_context('calm')
                    blocker = self.effect_room_member('Blocker', npc=guard in ('IMM_MAGIC', 'ACT_UNDEAD'))
                    tail = self.effect_room_member('Tail')
                    tail.fighting = ctx.actor
                    if guard == 'IMM_MAGIC':
                        blocker.status_flags.imm = int(self.enums['mobImmunity'].IMM_MAGIC)
                    elif guard == 'ACT_UNDEAD':
                        blocker.status_flags.act = int(self.enums['actBits'].ACT_UNDEAD)
                    elif guard.startswith('AFF_'):
                        blocker.status_flags.affected_by = int(self.enums['affectedBy'][guard])
                    else:
                        blocker.effects = [SimpleNamespace(type='spell.frenzy')]
                    occupants = [blocker, ctx.actor, tail] if first else [ctx.actor, blocker, tail]
                    ctx.room.characters = {member.id: member for member in occupants}
                    self.fight.stop_fighting = Mock()
                    with patch('random.randint', return_value=0):
                        self.assertEqual(not first, self.api.execute_lambdas(ctx))
                    self.assertTrue(ctx.done)
                    self.assertEqual(0 if first else 2, len(ctx.actor.effects))
                    self.assertEqual([], tail.effects)
                    self.assertIs(tail.fighting, ctx.actor)
                    self.fight.stop_fighting.assert_not_called()
                    self.assertEqual(0 if first else 1, len(ctx.payloads))

    def test_calm_does_not_apply_npc_only_immunity_guards_to_players(self):
        ctx = self.live_effect_context('calm')
        ctx.victim.status_flags.imm = int(self.enums['mobImmunity'].IMM_MAGIC)
        ctx.victim.status_flags.act = int(self.enums['actBits'].ACT_UNDEAD)
        self.fight.stop_fighting = Mock()
        with patch('random.randint', return_value=0):
            self.assertTrue(self.api.execute_lambdas(ctx))
        self.assertEqual(2, len(ctx.victim.effects))

    def test_sleep_messages_and_position_match_awake_asleep_and_unconscious_targets(self):
        for position in ('POS_STANDING', 'POS_RESTING', 'POS_FIGHTING', 'POS_SLEEPING', 'POS_STUNNED', 'POS_DEAD'):
            with self.subTest(position=position):
                ctx = self.live_sleep_context()
                self.PositionApi.set_position(ctx.victim, position)
                observer = SimpleNamespace(id='observer', name='Observer')
                ctx.room.characters['observer'] = observer
                awake = self.PositionApi.is_awake(ctx.victim)
                self.assertTrue(self.api.execute_lambdas(ctx))
                expected = self.enums['positions'].POS_SLEEPING if awake else self.enums['positions'][position]
                self.assertEqual(int(expected), ctx.victim.position)
                self.assertEqual(int(expected), ctx.victim.character_attributes.position)
                self.assertEqual(24, ctx.victim.effects[0].duration)
                self.assertFalse(ctx.failed)
                if awake:
                    self.assertEqual(1, len(ctx.payloads))
                    payload = ctx.payloads[0]
                    self.assertEqual('You feel very sleepy ..... zzzzzz.\r\n', payload['to_victim'])
                    self.assertEqual('Target goes to sleep.\r\n', payload['to_room'])
                    self.assertIs(ctx.victim, payload['victim'])
                    self.assertIn(ctx.actor, payload['targets'])
                    self.assertIn(observer, payload['targets'])
                    self.assertNotIn(ctx.victim, payload['targets'])
                else:
                    self.assertEqual([], ctx.payloads)

    def test_sleep_self_and_npc_targets_keep_sleep_flag_and_correct_recipients(self):
        for self_target, npc in [(True, False), (False, True)]:
            with self.subTest(self_target=self_target, npc=npc):
                ctx = self.live_sleep_context()
                if self_target:
                    ctx.set_target(ctx.actor)
                ctx.victim.is_npc = npc
                self.assertTrue(self.api.execute_lambdas(ctx))
                self.assertEqual(int(self.enums['positions'].POS_SLEEPING), self.PositionApi.position_value(ctx.victim))
                self.assertTrue(ctx.victim.status_flags.affected_by & int(self.enums['affectedBy'].AFF_SLEEP))
                payload = ctx.payloads[0]
                self.assertEqual(not npc, 'to_victim' in payload)
                self.assertNotIn(ctx.victim, payload['targets'])

    def test_sleep_blocks_stand_and_targeted_wake_until_expiry_or_dispel(self):
        # Load the real movement handler through its existing isolated dependency fixture.
        with patch.dict(sys.modules):
            spec = importlib.util.spec_from_file_location('_sleep_movement_fixture', ROOT / 'tests/test_movement_dynamic_commands.py')
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            movement_api = module._load_module('_sleep_movement_api', 'api/MovementApi.py').MovementApi
        for removal in ('expiry', 'dispel'):
            with self.subTest(removal=removal):
                ctx = self.live_sleep_context()
                self.assertTrue(self.api.execute_lambdas(ctx))
                movement = module.Movement.__new__(module.Movement)
                movement.affected_bits = self.enums['affectedBy']
                def command_context(result=''):
                    context = SimpleNamespace(room=ctx.room, result=result, done=False)
                    context.finish = lambda: setattr(context, 'done', True)
                    return context
                with patch.dict(module.Movement.do_stand.__globals__, CharacterApi=self.PositionApi,
                                MovementApi=movement_api):
                    self.assertEqual('can_t_wake_up', movement.do_stand(ctx.victim, command_context())['message_key'])
                    self.assertEqual('affect_sleep', movement.do_wake(ctx.actor, command_context('Target'))['message_key'])
                    self.assertEqual(int(self.enums['positions'].POS_SLEEPING), self.PositionApi.position_value(ctx.victim))
                    if removal == 'expiry':
                        ctx.victim.effects[0].duration = 1
                        with patch('random.randint', return_value=1):
                            tick = self.api.effect_handler.tick_effects(ctx.victim)
                        self.assertEqual([], tick.expired_effects)
                        self.assertEqual('can_t_wake_up', movement.do_stand(ctx.victim, command_context())['message_key'])
                        tick = self.api.effect_handler.tick_effects(ctx.victim)
                        self.assertEqual('spell.sleep', tick.expired_effects[0].type)
                    else:
                        util = self.api.effect_handler.dispel_effects.__globals__['EffectUtil']
                        with patch.object(util, 'saves_dispel', return_value=False):
                            removed = self.api.effect_handler.dispel_effects(20, ctx.victim, 'spell.sleep')
                        self.assertEqual(1, len(removed))
                    self.assertEqual([], ctx.victim.effects)
                    self.assertEqual(0, ctx.victim.status_flags.affected_by)
                    # Ending the affect permits waking; it does not itself stand the victim.
                    self.assertEqual(int(self.enums['positions'].POS_SLEEPING), self.PositionApi.position_value(ctx.victim))
                    self.assertEqual('wake_stand_up', movement.do_stand(ctx.victim, command_context())['message_key'])
                    self.PositionApi.set_position(ctx.victim, 'POS_SLEEPING')
                    self.assertEqual('wake_target', movement.do_wake(ctx.actor, command_context('Target'))['message_key'])
                    self.assertEqual(int(self.enums['positions'].POS_STANDING), ctx.victim.character_attributes.position)

    def test_opposing_protection_flags_are_exclusive_without_effect_records(self):
        for name in ('protection evil', 'protection good'):
            for flag in ('AFF_PROTECT_EVIL', 'AFF_PROTECT_GOOD'):
                with self.subTest(spell=name, flag=flag):
                    ctx = self.guard_context(name)
                    ctx.victim.status_flags.affected_by = int(self.enums['affectedBy'][flag])
                    self.effects.reset_mock()
                    self.assertFalse(self.api.execute_lambdas(ctx))
                    self.effects.apply_spell_effects.assert_not_called()

    def test_haste_innate_fast_and_slow_save_immunity_precede_counter_dispel(self):
        for scenario in ('haste', 'fast', 'slow', 'saved', 'immune'):
            with self.subTest(scenario=scenario):
                ctx = self.guard_context('haste' if scenario in ('haste', 'fast') else 'slow')
                if scenario in ('haste', 'slow'):
                    ctx.victim.status_flags.affected_by = int(self.enums['affectedBy']['AFF_' + scenario.upper()])
                if scenario == 'fast':
                    ctx.victim.status_flags.off = int(self.enums['offenseTypes'].OFF_FAST)
                if scenario == 'immune':
                    ctx.victim.status_flags.imm = int(self.enums['mobImmunity'].IMM_MAGIC)
                self.api.saves_spell = Mock(return_value=scenario == 'saved')
                self.effects.reset_mock()
                self.assertFalse(self.api.execute_lambdas(ctx))
                self.effects.dispel_effects.assert_not_called()
                self.effects.apply_spell_effects.assert_not_called()
                self.assertEqual(1 if scenario in ('saved', 'immune') else 0, self.api.saves_spell.call_count)

    def test_opposed_speed_flags_only_attempt_dispel_and_never_apply_new_speed(self):
        for name, flag, effect in [('haste', 'AFF_SLOW', 'spell.slow'), ('slow', 'AFF_HASTE', 'spell.haste')]:
            for removed in (False, True):
                with self.subTest(spell=name, removed=removed):
                    ctx = self.guard_context(name)
                    ctx.victim.status_flags.affected_by = int(self.enums['affectedBy'][flag])
                    self.effects.reset_mock()
                    self.effects.dispel_effects.return_value = [SimpleNamespace(type=effect)] if removed else []
                    self.api._queue_removed_effect_messages = Mock()
                    self.api.saves_spell = Mock(return_value=False)
                    self.assertEqual(removed, self.api.execute_lambdas(ctx))
                    self.effects.dispel_effects.assert_called_once_with(20, ctx.victim, effect)
                    self.effects.apply_spell_effects.assert_not_called()
                    self.assertTrue(ctx.done)

    def test_cancellation_npc_player_matrix_master_exception_and_no_initial_save(self):
        for actor_npc, victim_npc, master, expected in [(False, False, False, True), (True, True, False, True),
                (False, True, False, False), (True, False, False, False), (False, True, True, True)]:
            with self.subTest(actor=actor_npc, victim=victim_npc, master=master):
                ctx = self.guard_context('cancellation')
                ctx.actor.is_npc, ctx.victim.is_npc = actor_npc, victim_npc
                if master:
                    ctx.actor.status_flags.affected_by = int(self.enums['affectedBy'].AFF_CHARM)
                    ctx.actor.master = ctx.victim
                self.api.dispel_sequence = Mock(side_effect=lambda scoped, *args, **kwargs: scoped.mark_performed())
                self.api.saves_spell = Mock()
                self.assertEqual(expected, self.api.execute_lambdas(ctx))
                self.assertEqual(expected, self.api.dispel_sequence.called)
                self.api.saves_spell.assert_not_called()
        ctx = self.guard_context('dispel magic')
        self.api.dispel_sequence = Mock()
        self.api.saves_spell = Mock(return_value=True)
        self.assertFalse(self.api.execute_lambdas(ctx))
        self.api.dispel_sequence.assert_not_called()
        self.assertIn('tingling', ctx.payloads[-1]['to_victim'])

    def guard_object(self, name, kind='weapon', flags=0, weapon_flags=0):
        ctx = self.guard_context(name)
        item = SimpleNamespace(item_type=kind, name='Item', short_description='the item', extra_flags=flags,
                               value4=weapon_flags, value3='0', level=40, effects=[])
        ctx.set_target(item)
        return ctx, item

    def test_bless_and_curse_object_duplicates_and_opposed_flags_stop_before_new_effect(self):
        for name, own, opposite, effect in [('bless', 'ITEM_BLESS', 'ITEM_EVIL', 'spell.curse'),
                                          ('curse', 'ITEM_EVIL', 'ITEM_BLESS', 'spell.bless')]:
            for duplicate, saved, recorded in [(True, False, False), (False, True, False),
                                              (False, False, False), (False, False, True)]:
                with self.subTest(spell=name, duplicate=duplicate, saved=saved, recorded=recorded):
                    bit = int(self.enums['itemFlags'][own if duplicate else opposite])
                    ctx, item = self.guard_object(name, flags=bit)
                    if recorded:
                        item.effects = [SimpleNamespace(type=effect, level=12)]
                    self.effects.reset_mock()
                    with patch.object(SpellApi.counter_item_flag.__globals__['EffectUtil'], 'saves_dispel',
                                      return_value=saved, create=True) as saves:
                        self.assertEqual(not duplicate and not saved, self.api.execute_lambdas(ctx))
                    self.effects.apply_spell_effects.assert_not_called()
                    self.assertTrue(ctx.done)
                    if duplicate:
                        saves.assert_not_called()
                    else:
                        saves.assert_called_once_with(20, 12 if recorded else 40, 0)
                        self.assertEqual(bit if saved else 0, int(item.extra_flags))
                        if recorded and not saved:
                            self.effects.remove_effect.assert_called_once_with(item, item.effects[0])
                    self.assertFalse(int(item.extra_flags) & int(self.enums['itemFlags'][own]) if not duplicate else False)

    def test_poison_object_type_protection_incompatible_weapon_and_duplicate_guards(self):
        exclusions = ['WEAPON_FLAMING', 'WEAPON_FROST', 'WEAPON_VAMPIRIC', 'WEAPON_SHARP',
                      'WEAPON_VORPAL', 'WEAPON_SHOCKING', 'WEAPON_POISON']
        cases = [('armor', 0, 0)]
        for kind in ('food', 'drink', 'weapon'):
            for flag in ('ITEM_BLESS', 'ITEM_BURN_PROOF'):
                cases.append((kind, int(self.enums['itemFlags'][flag]), 0))
        cases += [('weapon', 0, int(self.enums['weaponType'][flag])) for flag in exclusions]
        for kind, flags, weapon in cases:
            with self.subTest(kind=kind, flags=flags, weapon=weapon):
                ctx, item = self.guard_object('poison', kind, flags, weapon)
                self.effects.reset_mock()
                self.api.saves_spell = Mock()
                self.assertFalse(self.api.execute_lambdas(ctx))
                self.effects.apply_spell_effects.assert_not_called()
                self.api.saves_spell.assert_not_called()
                self.assertEqual('0', item.value3)
                self.assertTrue(ctx.payloads[-1]['to_char'])

    def test_poison_food_drink_state_and_allowed_weapon_do_not_use_character_save(self):
        for kind in ('food', 'drink', 'weapon'):
            with self.subTest(kind=kind):
                ctx, item = self.guard_object('poison', kind)
                self.effects.reset_mock()
                self.api.saves_spell = Mock()
                self.assertTrue(self.api.execute_lambdas(ctx))
                self.api.saves_spell.assert_not_called()
                if kind == 'weapon':
                    self.effects.apply_spell_effects.assert_called_once()
                else:
                    self.assertEqual('1', item.value3)
                    self.effects.apply_spell_effects.assert_not_called()
                    self.assertIn('poisonous vapors', ctx.payloads[-1]['to_char'])

    def test_frenzy_rejection_feedback_distinguishes_self_other_calm_and_alignment(self):
        for flag, expected in [('AFF_BERSERK', 'already in a frenzy'), ('spell.calm', 'want to fight'),
                                ('alignment', "god doesn't seem to like")]:
            with self.subTest(flag=flag):
                ctx = self.guard_context('frenzy')
                if flag == 'alignment':
                    ctx.victim.character_attributes.alignment = 350
                elif flag.startswith('AFF_'):
                    ctx.victim.status_flags.affected_by = int(self.enums['affectedBy'][flag])
                else:
                    ctx.victim.effects = [SimpleNamespace(type=flag)]
                self.effects.reset_mock()
                self.assertFalse(self.api.execute_lambdas(ctx))
                self.effects.apply_spell_effects.assert_not_called()
                self.assertIn(expected, ctx.payloads[-1]['to_char'])
        ctx = self.guard_context('frenzy')
        ctx.set_target(ctx.actor)
        ctx.actor.status_flags.affected_by = int(self.enums['affectedBy'].AFF_BERSERK)
        self.api.execute_lambdas(ctx)
        self.assertEqual('You are already in a frenzy.\r\n', ctx.payloads[-1]['to_char'])

    def test_fog_invisibility_level_and_save_guards_prevent_strip_and_application(self):
        for invisible, saved, applied in [(True, False, False), (False, True, False), (False, False, True)]:
            with self.subTest(invisible=invisible, saved=saved):
                ctx = self.guard_context('faerie fog')
                ctx.victim.status_flags.invis_level = 1 if invisible else 0
                self.api.saves_spell = Mock(return_value=saved)
                self.effects.reset_mock()
                self.api.execute_lambdas(ctx)
                self.assertEqual(0 if invisible else 1, self.api.saves_spell.call_count)
                self.assertEqual(applied, self.effects.affect_strip.called)
                self.effects.apply_spell_effects.assert_not_called()

    def test_mass_invis_group_filter_includes_fighting_pet_and_skips_ungrouped_pc(self):
        ctx = self.guard_context('mass invis')
        pet = SimpleNamespace(name='Pet', is_npc=True, leader=ctx.actor, fighting=object(), effects=[],
                              status_flags=SimpleNamespace(affected_by=0))
        invisible = SimpleNamespace(name='Innate', leader=ctx.actor, effects=[],
                                    status_flags=SimpleNamespace(affected_by=int(self.enums['affectedBy'].AFF_INVISIBLE)))
        ctx.victim.leader = None
        ctx.room.mobiles = {'pet': pet, 'invisible': invisible}
        self.assertTrue(self.api.execute_lambdas(ctx))
        applied = [call.args[1] for call in self.effects.apply_spell_effects.call_args_list]
        self.assertEqual(2, len(applied))
        self.assertIs(ctx.actor, applied[0])
        self.assertIs(pet, applied[1])

    def room_context(self, name, level=8):
        ctx = self.context(name, level)
        ctx.actor.id = 'actor'
        ctx.actor.name = 'Caster'
        ctx.actor.hit = 101
        ctx.actor.movement = 55
        ctx.actor.character_attributes = SimpleNamespace(alignment=0)
        ctx.victim.id = 'victim'
        ctx.victim.character_attributes = SimpleNamespace(alignment=0)
        ctx.room = SimpleNamespace(area_id='area', characters={'actor': ctx.actor, 'victim': ctx.victim}, mobiles={})
        self.api._find_room_for_entity = Mock(return_value=ctx.room)
        self.fight.is_safe_spell = Mock(return_value=False)
        return ctx

    def test_holy_word_full_alignment_matrix_and_exhaustion(self):
        for caster_alignment in (-350, 0, 350):
            with self.subTest(caster=caster_alignment):
                ctx = self.room_context('holy word')
                ctx.actor.character_attributes.alignment = caster_alignment
                targets = [SimpleNamespace(id=str(a), name=str(a), character_attributes=SimpleNamespace(alignment=a))
                           for a in (-350, 0, 350)]
                ctx.room.characters = {'actor': ctx.actor, **{p.id: p for p in targets}}
                events = []
                self.effects.apply_spell_effects.side_effect = lambda actor, victim, spell, **kw: events.append(
                    (victim, spell.name, kw['caster_level']))
                self.fight.damage.side_effect = lambda actor, victim, damage, **kw: events.append((victim, 'damage', damage)) or {}
                with patch('random.randint', return_value=2):
                    self.assertTrue(self.api.execute_lambdas(ctx))
                self.assertEqual((50, 0), (ctx.actor.hit, ctx.actor.movement))
                self.assertEqual([(ctx.actor, 'frenzy', 8), (ctx.actor, 'bless', 8)], events[:2])
                for victim in targets:
                    actual = [(name, value) for entity, name, value in events if entity is victim]
                    alignment = victim.character_attributes.alignment
                    if alignment == caster_alignment:
                        expected = [('frenzy', 8), ('bless', 8)]
                    elif caster_alignment == 0:
                        expected = [('curse', 4), ('damage', 16)]
                    elif alignment == -caster_alignment:
                        expected = [('curse', 8), ('damage', 16)]
                    else:
                        expected = []
                    self.assertEqual(expected, actual)
                # The only saves are those owned by the invoked curse content.
                self.assertTrue(all(call.args[1] == 'DAM_NEGATIVE' for call in self.api.saves_spell.call_args_list))
                self.api.saves_spell.reset_mock()

    def test_holy_word_safe_enemy_is_skipped_but_caster_still_exhausted(self):
        ctx = self.room_context('holy word')
        ctx.actor.character_attributes.alignment = 350
        ctx.victim.character_attributes.alignment = -350
        self.fight.is_safe_spell.return_value = True
        self.api.execute_lambdas(ctx)
        self.fight.damage.assert_not_called()
        self.assertEqual(['frenzy', 'bless'], [call.args[2].name for call in self.effects.apply_spell_effects.call_args_list])
        self.assertEqual((50, 0), (ctx.actor.hit, ctx.actor.movement))

    def test_holy_word_invoked_buff_guards_preserve_calm_and_fighting_restrictions(self):
        ctx = self.room_context('holy word')
        ctx.victim.position = int(self.enums['positions'].POS_FIGHTING)
        self.api._effect_active.side_effect = lambda victim, name: victim is ctx.victim and name == 'spell.calm'
        with patch.dict(SpellApi.has_position.__globals__, GameApi=self.game_api()), \
                patch.object(_CharacterApi, 'position_value', side_effect=lambda victim: int(victim.position), create=True):
            self.assertTrue(self.api.execute_lambdas(ctx))
        applied = [call.args[1] for call in self.effects.apply_spell_effects.call_args_list]
        self.assertTrue(all(victim is ctx.actor for victim in applied))
        self.assertEqual(2, len(applied))

    def test_call_lightning_guards_shared_roll_opposite_side_and_weather(self):
        for indoors, raining, caster_npc in [(True, True, False), (False, False, False),
                                             (False, True, False), (False, True, True)]:
            with self.subTest(indoors=indoors, raining=raining, npc=caster_npc):
                ctx = self.room_context('call lightning', 9)
                ctx.actor.is_npc = caster_npc
                ctx.victim.is_npc = not caster_npc
                second = SimpleNamespace(id='second', name='Second', is_npc=not caster_npc)
                ally = SimpleNamespace(id='ally', name='Ally', is_npc=caster_npc)
                ctx.room.characters.update(second=second, ally=ally)
                sky = self.enums['timeAndWeather'].SKY_RAINING if raining else self.enums['timeAndWeather'].SKY_CLOUDLESS
                ctx.handler.weather_handler = SimpleNamespace(weather_info=SimpleNamespace(sky=sky))
                self.api._room_flag = Mock(return_value=indoors)
                self.api.area_message = Mock()
                self.fight.damage.reset_mock()
                self.api.saves_spell = Mock(side_effect=[False, True])
                with patch.dict(SpellApi.is_raining.__globals__, GameApi=self.game_api()), patch('random.randint', return_value=3) as roll:
                    self.api.execute_lambdas(ctx)
                if indoors or not raining:
                    roll.assert_not_called()
                    self.fight.damage.assert_not_called()
                    self.assertIn('out of doors' if indoors else 'bad weather', ctx.payloads[0]['to_char'])
                else:
                    self.assertEqual(4, roll.call_count)
                    self.assertEqual([12, 6], [call.args[2] for call in self.fight.damage.call_args_list])
                    self.assertEqual([ctx.victim, second], [call.args[1] for call in self.fight.damage.call_args_list])
                    self.api.area_message.assert_called_once_with(ctx, 'distant', outdoors=True, awake=True)
                self.fight.is_safe_spell.assert_not_called()

    def test_area_notices_filter_rooms_outdoors_and_awake_and_use_recipient_payloads(self):
        ctx = self.room_context('call lightning')
        awake = SimpleNamespace(name='Awake', is_npc=False, awake=True)
        asleep = SimpleNamespace(name='Asleep', is_npc=False, awake=False)
        indoor = SimpleNamespace(name='Inside', is_npc=False, awake=True)
        remote = SimpleNamespace(name='Elsewhere', is_npc=False, awake=True)
        outdoor_room = SimpleNamespace(area_id='area', indoor=False, characters={'a': awake, 'b': asleep}, mobiles={})
        indoor_room = SimpleNamespace(area_id='area', indoor=True, characters={'i': indoor}, mobiles={})
        remote_room = SimpleNamespace(area_id='other', indoor=False, characters={'r': remote}, mobiles={})
        ctx.handler.room_registry = SimpleNamespace(all_rooms=lambda: [ctx.room, outdoor_room, indoor_room, remote_room])
        self.api._room_flag = Mock(side_effect=lambda room, flag: getattr(room, 'indoor', False))
        with patch.object(_CharacterApi, 'is_awake', side_effect=lambda victim: victim.awake, create=True):
            self.api.area_message(ctx, 'distant', outdoors=True, awake=True)
        self.assertEqual([awake], [p['victim'] for p in ctx.payloads])
        ctx.payloads.clear()
        ctx.spell = self.context('earthquake', 8).spell
        self.api.area_message(ctx, 'distant')
        self.assertEqual([awake, asleep, indoor], [p['victim'] for p in ctx.payloads])

    def test_earthquake_ground_flying_and_safe_targets_never_roll_saves(self):
        ctx = self.room_context('earthquake', 9)
        flyer = SimpleNamespace(id='flyer', name='Flyer')
        safe = SimpleNamespace(id='safe', name='Safe')
        ctx.room.characters.update(flyer=flyer, safe=safe)
        self.api._effect_active = Mock(side_effect=lambda victim, flag: victim is flyer)
        self.fight.is_safe_spell.side_effect = lambda actor, victim, area: victim is safe
        self.api.area_message = Mock()
        self.api.saves_spell = Mock(return_value=True)
        with patch('random.randint', return_value=3) as roll:
            self.assertTrue(self.api.execute_lambdas(ctx))
        self.assertEqual(2, roll.call_count)
        self.assertEqual([15, 0], [call.args[2] for call in self.fight.damage.call_args_list])
        self.api.saves_spell.assert_not_called()
        self.api.area_message.assert_called_once_with(ctx, 'distant')

    def test_all_breath_collection_damage_depends_on_hp_and_keeps_exposure_first(self):
        for name, expected in [('acid breath', 56), ('frost breath', 56), ('fire breath', 68),
                               ('lightning breath', 68), ('gas breath', 42)]:
            for hp, damage in [(1, 16), (600, expected)]:
                with self.subTest(spell=name, hp=hp):
                    ctx = self.room_context(name, 2)
                    ctx.actor.hit = hp
                    events = []
                    self.api.acid_effect = Mock(side_effect=lambda *a, **kw: events.append('expose'))
                    self.api.elemental_effect = Mock(side_effect=lambda *a, **kw: events.append('expose'))
                    self.api.poison_effect = Mock(side_effect=lambda *a, **kw: events.append('expose'))
                    self.fight.damage.side_effect = lambda *a, **kw: events.append('damage') or {}
                    self.api.saves_spell = Mock(return_value=False)
                    with patch('random.randint', side_effect=lambda low, high: 8 if high in (12, 16, 20) else low), \
                            patch.object(SpellApi.elemental_breath.__globals__['EffectUtil'], 'saves_spell', return_value=False, create=True):
                        self.assertTrue(self.api.execute_lambdas(ctx))
                    self.assertEqual(damage, self.fight.damage.call_args.args[2])
                    self.assertEqual('damage', events[-1])
                    self.assertIn('expose', events[:-1])

    def test_gas_npc_exclusion_matches_either_fighting_direction(self):
        for actor_fights, victim_fights, expected in [(False, False, 1), (True, False, 0),
                                                     (False, True, 0), (True, True, 0)]:
            with self.subTest(actor=actor_fights, victim=victim_fights):
                ctx = self.room_context('gas breath', 2)
                ctx.actor.is_npc = ctx.victim.is_npc = True
                ctx.actor.fighting = ctx.victim if actor_fights else None
                ctx.victim.fighting = ctx.actor if victim_fights else None
                self.api.poison_effect = Mock()
                self.fight.damage.reset_mock()
                with patch('random.randint', return_value=2), patch.object(
                        SpellApi.damage_room_expr.__globals__['EffectUtil'], 'saves_spell', return_value=False, create=True):
                    self.api.execute_lambdas(ctx)
                self.assertEqual(expected, self.fight.damage.call_count)
                self.assertIs(ctx.room, self.api.poison_effect.call_args_list[0].kwargs['target'])

    def heat_context(self, kind='armor', worn=True, flags=0, weight=10, level=12, flaming=False):
        ctx = self.room_context('heat metal', 20)
        victim = ctx.victim
        victim.level = 20
        victim.race = 'human'
        victim.character_class = SimpleNamespace(attr_prime=3)
        victim.character_attributes.dexterity = 10
        victim.status_flags = SimpleNamespace(imm=0)
        item = SimpleNamespace(id='item', name='Equipment', short_description='some equipment',
                               item_type=kind, extra_flags=flags, level=level, weight=weight,
                               value4=int(self.enums['weaponType'].WEAPON_FLAMING) if flaming else 0)
        item.can_remove = lambda item_flags: not bool(item.extra_flags & int(item_flags.ITEM_NOREMOVE))
        victim.inventory = [] if worn else [item]
        victim.equipped = SimpleNamespace(torso=item if worn else None)
        victim.owned_items = lambda: list(victim.inventory) + [v for v in vars(victim.equipped).values() if v is not None]
        victim.equipped_slot_of = lambda obj: 'torso' if victim.equipped.torso is obj else None
        def unequip(slot):
            obj = getattr(victim.equipped, slot)
            setattr(victim.equipped, slot, None)
            victim.inventory.append(obj)
            return obj
        victim.unequip_item = Mock(side_effect=unequip)
        victim.remove_item = lambda obj: victim.inventory.remove(obj)
        ctx.room.contents = {}
        ctx.room.add_item_to_room = lambda obj: ctx.room.contents.update({obj.id: obj})
        return ctx, item

    def run_heat(self, ctx, saved=False, initial_save=False):
        self.api.saves_spell = Mock(side_effect=[initial_save, False, saved])
        with patch.dict(SpellApi.heat_equipment.__globals__, GameApi=self.game_api()), \
                patch.dict(sys.modules, {'game.Equipped': SimpleNamespace(Equipped=self.Equipped)}), \
                patch.object(_CharacterApi, 'is_immortal', return_value=False, create=True), \
                patch.object(_CharacterApi, 'get_max_train', return_value=18, create=True), \
                patch('random.randint', side_effect=lambda low, high: high):
            return self.api.execute_lambdas(ctx)

    def test_heat_equipment_worn_and_carried_damage_removal_drops_and_final_save(self):
        nodrop = int(self.enums['itemFlags'].ITEM_NODROP)
        for kind in ('armor', 'weapon'):
            for worn in (False, True):
                for stuck in (False, True):
                    for saved in (False, True):
                        with self.subTest(kind=kind, worn=worn, stuck=stuck, saved=saved):
                            ctx, item = self.heat_context(kind, worn, nodrop if stuck else 0)
                            self.effects.reset_mock()
                            self.fight.damage.reset_mock()
                            self.assertTrue(self.run_heat(ctx, saved))
                            damage = 12 if worn and stuck else 1 if worn and kind == 'weapon' else 4 if worn else 6 if stuck else 2
                            self.fight.damage.assert_called_once_with(ctx.actor, ctx.victim,
                                2 * damage // 3 if saved else damage, dt='spell', dam_type='DAM_FIRE')
                            self.assertEqual(3, self.api.saves_spell.call_count)
                            self.assertEqual(2, self.api.saves_spell.call_args_list[0].kwargs['level_adjust'])
                            if stuck:
                                self.assertNotIn(item.id, ctx.room.contents)
                                ctx.victim.unequip_item.assert_not_called()
                            else:
                                self.assertIs(item, ctx.room.contents[item.id])
                                self.assertNotIn(item, ctx.victim.owned_items())
                            if worn and not stuck:
                                self.effects.remove_item_effects.assert_called_once_with(ctx.victim, item)

    def test_heat_equipment_no_effect_save_immunity_flags_and_flaming_weapon(self):
        flags = self.enums['itemFlags']
        for scenario in ('empty', 'saved', 'immune', 'nonmetal', 'burnproof', 'flaming', 'other', 'highlevel'):
            with self.subTest(scenario=scenario):
                extra = int(flags.ITEM_NONMETAL) if scenario == 'nonmetal' else int(flags.ITEM_BURN_PROOF) if scenario == 'burnproof' else 0
                ctx, item = self.heat_context('weapon' if scenario == 'flaming' else 'potion' if scenario == 'other' else 'armor',
                                            flags=extra, flaming=scenario == 'flaming', level=40 if scenario == 'highlevel' else 12)
                if scenario == 'empty':
                    ctx.victim.equipped.torso = None
                if scenario == 'immune':
                    ctx.victim.status_flags.imm = int(self.enums['mobImmunity'].IMM_FIRE)
                self.fight.damage.reset_mock()
                self.assertFalse(self.run_heat(ctx, initial_save=scenario == 'saved'))
                self.fight.damage.assert_not_called()
                self.assertEqual({}, ctx.room.contents)
                self.assertEqual('Your spell had no effect.\r\n', ctx.payloads[-1]['to_char'])
                self.assertEqual('You feel momentarily warmer.\r\n', ctx.payloads[-1]['to_victim'])

    def test_heat_equipment_strict_weight_check_no_remove_and_zero_damage_drop(self):
        for flags, weight, level, expected, dropped in [
                (0, 200, 12, 12, False),
                (int(self.enums['itemFlags'].ITEM_NOREMOVE), 10, 12, 12, False),
                (0, 10, 1, 0, True)]:
            with self.subTest(flags=flags, weight=weight, level=level):
                ctx, item = self.heat_context(flags=flags, weight=weight, level=level)
                self.assertTrue(self.run_heat(ctx))
                self.assertEqual(expected, self.fight.damage.call_args.args[2])
                self.assertEqual(dropped, item.id in ctx.room.contents)

    def test_dispels_alignment_matrix_npc_exemption_and_saved_damage(self):
        for name, sign, kind in [('dispel evil', 1, 'DAM_HOLY'), ('dispel good', -1, 'DAM_NEGATIVE')]:
            for npc in (False, True):
                for caster_align in (-350, 0, 350):
                    for target_align in (-350, 0, 350):
                        for saved in (False, True):
                            with self.subTest(name=name, npc=npc, caster=caster_align, target=target_align, saved=saved):
                                ctx = self.context(name, 7)
                                ctx.actor.level = 20
                                ctx.actor.hit = 80
                                ctx.actor.is_npc = npc
                                ctx.actor.character_attributes = SimpleNamespace(alignment=caster_align)
                                ctx.victim.hit = 21
                                ctx.victim.character_attributes = SimpleNamespace(alignment=target_align)
                                original = ctx.target
                                redirected = not npc and sign * caster_align <= -350
                                victim = ctx.actor if redirected else original
                                affected = sign * (caster_align if redirected else target_align) <= -350
                                self.fight.damage.reset_mock()
                                self.api.saves_spell = Mock(return_value=saved)
                                with patch('random.randint', return_value=2) as roll:
                                    self.api.execute_lambdas(ctx)
                                if not affected:
                                    self.fight.damage.assert_not_called()
                                    self.api.saves_spell.assert_not_called()
                                    roll.assert_not_called()
                                else:
                                    base = 80 if redirected else 21
                                    self.fight.damage.assert_called_once_with(ctx.actor, victim,
                                        base // 2 if saved else base, dt=name, dam_type=kind)
                                    self.assertEqual(7, roll.call_count)
                                    self.assertIs(original, ctx.target)

    def test_dispel_low_hp_branch_uses_actor_level_threshold_and_keeps_dice_floor(self):
        for hp, expected in [(1, 14), (80, 80), (81, 14)]:
            with self.subTest(hp=hp):
                ctx = self.context('dispel evil', 7)
                ctx.actor.level = 20
                ctx.victim.hit = hp
                ctx.actor.character_attributes = SimpleNamespace(alignment=0)
                ctx.victim.character_attributes = SimpleNamespace(alignment=-350)
                with patch('random.randint', return_value=2):
                    self.assertTrue(self.api.execute_lambdas(ctx))
                self.assertEqual(expected, self.fight.damage.call_args.args[2])

    def test_demonfire_redirect_alignment_and_independent_curse_save(self):
        for npc, alignment in [(False, -350), (False, -349), (False, 350), (True, 350), (True, -990)]:
            for damage_save, curse_save, cursed in [(False, False, False), (True, False, False),
                                                   (False, True, False), (False, False, True)]:
                with self.subTest(npc=npc, alignment=alignment, damage_save=damage_save, curse_save=curse_save, cursed=cursed):
                    ctx = self.context('demonfire', 7)
                    ctx.actor.is_npc = npc
                    ctx.actor.character_attributes = SimpleNamespace(alignment=alignment)
                    original = ctx.target
                    victim = ctx.actor if not npc and alignment > -350 else original
                    self.effects.reset_mock()
                    self.api._effect_active = Mock(return_value=cursed)
                    self.api.saves_spell = Mock(side_effect=[damage_save, curse_save])
                    order = []
                    self.fight.damage.side_effect = lambda *a, **kw: order.append('damage') or {}
                    self.effects.apply_spell_effects.side_effect = lambda *a, **kw: order.append('curse')
                    with patch('random.randint', return_value=7) as roll:
                        self.assertTrue(self.api.execute_lambdas(ctx))
                    self.assertEqual(7, roll.call_count)
                    self.assertTrue(all(call.args == (1, 10) for call in roll.call_args_list))
                    self.assertEqual(max(-1000, alignment-50), ctx.actor.character_attributes.alignment)
                    self.assertIs(victim, self.fight.damage.call_args.args[1])
                    self.assertEqual(24 if damage_save else 49, self.fight.damage.call_args.args[2])
                    self.assertIs(original, ctx.target)
                    self.assertEqual(1 if cursed else 2, self.api.saves_spell.call_count)
                    if not cursed:
                        child = self.api.saves_spell.call_args_list[1].args[0]
                        self.assertEqual(5, child.level)
                        self.assertEqual('DAM_NEGATIVE', self.api.saves_spell.call_args_list[1].args[1])
                    applied = not curse_save and not cursed
                    self.assertEqual(['damage', 'curse'] if applied else ['damage'], order)
                    if applied:
                        self.assertIs(victim, self.effects.apply_spell_effects.call_args.args[1])
                        self.assertEqual('curse', self.effects.apply_spell_effects.call_args.args[2].name)
                        self.assertEqual(5, self.effects.apply_spell_effects.call_args.kwargs['caster_level'])

    def chain_context(self, level, extras=()):
        ctx = self.context('chain lightning', level)
        ctx.actor.id = 'actor'
        ctx.actor.name = 'Caster'
        ctx.victim.id = 'target'
        ctx.room = SimpleNamespace(characters={p.id: p for p in [ctx.actor, ctx.victim, *extras]}, mobiles={})
        self.api._find_room_for_entity = Mock(return_value=ctx.room)
        self.fight.is_safe_spell = Mock(side_effect=lambda actor, victim, area: victim is actor or getattr(victim, 'protected', False))
        return ctx

    def test_curse_character_guards_do_not_add_a_save_to_object_application(self):
        ctx = self.context('curse', 7)
        ctx.set_target(SimpleNamespace(item_type='weapon', name='Sword', extra_flags=0))
        self.api.apply_affect_data = Mock(side_effect=lambda scoped: scoped.mark_performed())
        with patch.dict(SpellApi.item_has_flag.__globals__, GameApi=self.game_api()):
            self.assertTrue(self.api.execute_lambdas(ctx))
        self.api.apply_affect_data.assert_called_once_with(ctx)
        self.api.saves_spell.assert_not_called()
        self.api._effect_active.assert_not_called()

    def test_chain_initial_hit_is_not_an_area_search_and_stops_at_zero_level(self):
        ctx = self.chain_context(4)
        ctx.victim.protected = True
        with patch('random.randint', return_value=1):
            self.assertTrue(self.api.execute_lambdas(ctx))
        self.fight.is_safe_spell.assert_not_called()
        self.fight.damage.assert_called_once_with(ctx.actor, ctx.victim, 4, dt='lightning', dam_type='DAM_LIGHTNING')

    def test_chain_rebounds_then_can_revisit_first_target_with_one_third_saves(self):
        ctx = self.chain_context(12)
        self.api.saves_spell = Mock(return_value=True)
        with patch('random.randint', return_value=1) as roll:
            self.assertTrue(self.api.execute_lambdas(ctx))
        calls = self.fight.damage.call_args_list
        self.assertEqual([ctx.victim, ctx.actor, ctx.victim], [c.args[1] for c in calls])
        self.assertEqual([4, 2, 1], [c.args[2] for c in calls])
        self.assertEqual([12, 8, 4], [c.args[0].level for c in self.api.saves_spell.call_args_list])
        self.assertEqual(24, roll.call_count)
        self.assertEqual(12, ctx.level)
        self.assertIs(self.victim, ctx.target)
        self.assertTrue(all(c.kwargs['area'] for c in self.fight.is_safe_spell.call_args_list))

    def test_chain_repeated_sweeps_skip_safe_bystanders_and_consecutive_targets(self):
        safe = SimpleNamespace(id='safe', name='Grouped or protected bystander', protected=True)
        b = SimpleNamespace(id='b', name='B')
        c = SimpleNamespace(id='c', name='C')
        ctx = self.chain_context(22, (safe, b, c))
        with patch('random.randint', return_value=1):
            self.assertTrue(self.api.execute_lambdas(ctx))
        calls = self.fight.damage.call_args_list
        self.assertEqual([ctx.victim, b, c, ctx.victim, b, c], [call.args[1] for call in calls])
        self.assertEqual([22, 18, 14, 10, 6, 2], [call.args[2] for call in calls])
        self.assertFalse(any(call.args[1] is safe for call in calls))

    def test_chain_finishes_sweep_even_after_level_runs_out(self):
        b = SimpleNamespace(id='b', name='B')
        c = SimpleNamespace(id='c', name='C')
        ctx = self.chain_context(6, (b, c))
        with patch('random.randint', return_value=1):
            self.assertTrue(self.api.execute_lambdas(ctx))
        self.assertEqual([6, 2, 0], [call.args[2] for call in self.fight.damage.call_args_list])
        self.assertEqual([6, 2, -2], [call.args[0].level for call in self.api.saves_spell.call_args_list])

    def test_chain_removed_target_rebounds_once_then_grounds_out(self):
        ctx = self.chain_context(12)
        def damage(actor, victim, amount, **kwargs):
            if victim is ctx.victim:
                ctx.room.characters.pop('target', None)
            return {}
        self.fight.damage.side_effect = damage
        with patch('random.randint', return_value=1):
            self.assertTrue(self.api.execute_lambdas(ctx))
        self.assertEqual([ctx.victim, ctx.actor], [call.args[1] for call in self.fight.damage.call_args_list])
        self.assertEqual('The bolt grounds out through your body.\r\n', ctx.payloads[-1]['to_char'])

    def test_harm_minimum_caps_and_save_use_the_collection_formula(self):
        for hp, saved, expected in [(1, False, 20), (1, True, 10), (24, False, 21),
                                     (24, True, 10), (103, False, 100), (1000, False, 100),
                                     (1000, True, 50)]:
            with self.subTest(hp=hp, saved=saved):
                ctx = self.context('harm', 25)
                ctx.victim.hit = hp
                self.api.saves_spell = Mock(return_value=saved)
                with patch('random.randint', return_value=3) as roll:
                    self.assertTrue(self.api.execute_lambdas(ctx))
                roll.assert_called_once_with(1, 4)
                self.api.saves_spell.assert_called_once_with(ctx, 'DAM_HARM', 0, target=ctx.victim)
                self.assertEqual(expected, self.fight.damage.call_args.args[2])

    def drain_context(self, victim_level=20, self_target=False):
        ctx = self.context('energy drain', 25)
        ctx.actor.hit = 98
        ctx.actor.max_hit = 100
        ctx.actor.character_attributes = SimpleNamespace(alignment=-980)
        if self_target:
            ctx.set_target(ctx.actor)
        ctx.victim.level = victim_level
        ctx.victim.hit = 98 if self_target else 200
        ctx.victim.mana = 101
        ctx.victim.movement = 81
        ctx.victim.character_attributes = SimpleNamespace(
            alignment=0 if self_target else 100, experience=200, accumulated_experience=500,
            experience_per_level=1000)
        return ctx

    def test_energy_drain_save_changes_only_caster_alignment_and_sends_chill(self):
        ctx = self.drain_context()
        self.api.saves_spell = Mock(return_value=True)
        with patch('random.randint') as roll:
            self.api.execute_lambdas(ctx)
        roll.assert_not_called()
        self.fight.damage.assert_not_called()
        self.assertEqual(-1000, ctx.actor.character_attributes.alignment)
        self.assertEqual((20, 200, 101, 81), (ctx.victim.level, ctx.victim.hit, ctx.victim.mana, ctx.victim.movement))
        self.assertEqual(200, ctx.victim.character_attributes.experience)
        self.assertEqual('You feel a momentary chill.\r\n', ctx.payloads[0]['to_victim'])
        self.api.saves_spell.assert_called_once_with(ctx, 'DAM_NEGATIVE')

    def test_energy_drain_experience_resources_uncapped_heal_and_single_damage(self):
        ctx = self.drain_context()
        with patch.dict(sys.modules, {'player.CharacterAdvancement': self.advancement_module}), \
                patch('random.randint', side_effect=[37, 19]) as roll:
            self.assertTrue(self.api.execute_lambdas(ctx))
        self.assertEqual([(12, 37), (1, 25)], [call.args for call in roll.call_args_list])
        self.assertEqual((163, 463), (ctx.victim.character_attributes.experience,
                                    ctx.victim.character_attributes.accumulated_experience))
        self.assertEqual((20, 200, 50, 40), (ctx.victim.level, ctx.victim.hit, ctx.victim.mana, ctx.victim.movement))
        self.assertEqual(117, ctx.actor.hit)
        self.fight.damage.assert_called_once_with(ctx.actor, ctx.victim, 19, dt='energy drain', dam_type='DAM_NEGATIVE')
        self.assertEqual(1, self.api.saves_spell.call_count)
        self.assertEqual('Wow....what a rush!\r\n', ctx.payloads[0]['to_char'])
        self.assertEqual('You feel your life slipping away!\r\n', ctx.payloads[0]['to_victim'])

    def test_energy_drain_low_level_branch_uses_caster_hit_without_resource_drain(self):
        for level in (1, 2):
            with self.subTest(level=level):
                ctx = self.drain_context(level)
                self.fight.damage.reset_mock()
                with patch('random.randint') as roll:
                    self.assertTrue(self.api.execute_lambdas(ctx))
                roll.assert_not_called()
                self.assertEqual(99, self.fight.damage.call_args.args[2])
                self.assertEqual((98, 200, 101, 81), (ctx.actor.hit, ctx.victim.hit, ctx.victim.mana, ctx.victim.movement))
                self.assertEqual(200, ctx.victim.character_attributes.experience)

    def test_energy_drain_self_cast_preserves_alignment_and_npc_experience_is_unchanged(self):
        for self_target, npc in [(True, False), (False, True)]:
            with self.subTest(self_target=self_target, npc=npc):
                ctx = self.drain_context(self_target=self_target)
                ctx.victim.is_npc = npc
                before = ctx.actor.character_attributes.alignment
                with patch.dict(sys.modules, {'player.CharacterAdvancement': self.advancement_module}), \
                        patch('random.randint', side_effect=[12, 5]):
                    self.assertTrue(self.api.execute_lambdas(ctx))
                self.assertEqual(200 if npc else 188, ctx.victim.character_attributes.experience)
                self.assertEqual(20, ctx.victim.level)
                if self_target:
                    self.assertEqual(before, ctx.actor.character_attributes.alignment)
                self.assertEqual(103, ctx.actor.hit)

    def test_energy_drain_respects_existing_experience_floor_and_hero_exemption(self):
        for level, expected in [(20, 0), (51, 3)]:
            with self.subTest(level=level):
                ctx = self.drain_context(level)
                ctx.victim.character_attributes.experience = 3
                with patch.dict(sys.modules, {'player.CharacterAdvancement': self.advancement_module}), \
                        patch('random.randint', side_effect=[12, 5]):
                    self.assertTrue(self.api.execute_lambdas(ctx))
                self.assertEqual(expected, ctx.victim.character_attributes.experience)
                self.assertEqual(level, ctx.victim.level)

    def test_ray_protection_message_reaches_caster_and_target_through_payloads(self):
        ctx = self.context('ray of truth', 7)
        ctx.actor.id = 'caster'
        ctx.actor.character_attributes = SimpleNamespace(alignment=0)
        ctx.victim.id = 'victim'
        ctx.victim.character_attributes = SimpleNamespace(alignment=350)
        observer = SimpleNamespace(id='observer')
        ctx.room = SimpleNamespace(characters={'caster': ctx.actor, 'victim': ctx.victim, 'observer': observer})
        self.api.execute_lambdas(ctx)
        protected = ctx.payloads[-1]
        self.assertEqual('Target seems unharmed by the light.\r\n', protected['to_room'])
        self.assertIn(ctx.actor, protected['targets'])
        self.assertIn(observer, protected['targets'])
        self.assertNotIn(ctx.victim, protected['targets'])
        self.assertEqual('The light seems powerless to affect you.\r\n', protected['to_victim'])

    def test_ray_alignment_matrix_save_rounding_and_blindness_after_damage(self):
        for alignment, expected in [(350, None), (1000, None), (349, 0), (0, 6),
                                     (-350, 24), (-650, 49), (-651, 49), (-1000, 61)]:
            for saved in (False, True):
                with self.subTest(alignment=alignment, saved=saved):
                    ctx = self.context('ray of truth', 7)
                    ctx.actor.character_attributes = SimpleNamespace(alignment=0)
                    ctx.victim.character_attributes = SimpleNamespace(alignment=alignment)
                    self.fight.damage.reset_mock()
                    self.api.saves_spell = Mock(side_effect=[saved, True])
                    order = []
                    self.fight.damage.side_effect = lambda *a, **kw: order.append('damage') or {}
                    self.api._effect_active.side_effect = lambda *a: order.append('blindness') or False
                    with patch('random.randint', return_value=7) as roll:
                        self.api.execute_lambdas(ctx)
                    if expected is None:
                        self.fight.damage.assert_not_called()
                        self.api.saves_spell.assert_not_called()
                        roll.assert_not_called()
                        self.assertIn('powerless', ctx.payloads[-1]['to_victim'])
                        continue
                    saved_expected = {349: 0, 0: 2, -350: 11, -650: 24, -651: 24, -1000: 29}[alignment]
                    self.assertEqual(saved_expected if saved else expected, self.fight.damage.call_args.args[2])
                    self.assertEqual(['damage', 'blindness'], order)
                    calls = self.api.saves_spell.call_args_list
                    self.assertEqual('DAM_HOLY', calls[0].args[1])
                    self.assertEqual('DAM_OTHER', calls[1].args[1])
                    self.assertEqual(5, calls[1].args[0].level)

    def test_evil_ray_caster_takes_backlash_and_blindness_target_is_restored(self):
        for alignment in (-350, -1000):
            for blind_save in (False, True):
                with self.subTest(alignment=alignment, blind_save=blind_save):
                    ctx = self.context('ray of truth', 7)
                    ctx.actor.character_attributes = SimpleNamespace(alignment=alignment)
                    ctx.victim.character_attributes = SimpleNamespace(alignment=1000)
                    original = ctx.target
                    self.api.saves_spell = Mock(side_effect=[False, blind_save])
                    self.effects.reset_mock()
                    with patch('random.randint', return_value=7):
                        self.assertTrue(self.api.execute_lambdas(ctx))
                    self.assertIs(ctx.actor, self.fight.damage.call_args.args[1])
                    self.assertIs(original, ctx.target)
                    self.assertEqual('The energy explodes inside you!\r\n', ctx.payloads[0]['to_char'])
                    if blind_save:
                        self.effects.apply_spell_effects.assert_not_called()
                    else:
                        self.assertIs(ctx.actor, self.effects.apply_spell_effects.call_args.args[1])
                        self.assertEqual(5, self.effects.apply_spell_effects.call_args.kwargs['caster_level'])

    def test_table_bounds_uniform_roll_endpoints_and_typed_save_level(self):
        # ROM dam_each: first nonzero entry, level 49, level 50.
        cases = [('burning hands', 'FIRE', 5, 14, 48, 48),
                 ('chill touch', 'COLD', 3, 6, 26, 27),
                 ('colour spray', 'LIGHT', 11, 30, 79, 79),
                 ('fireball', 'FIRE', 15, 30, 128, 130),
                 ('lightning bolt', 'LIGHTNING', 9, 25, 63, 64),
                 ('magic missile', 'ENERGY', 1, 3, 14, 14),
                 ('shocking grasp', 'LIGHTNING', 7, 20, 57, 57)]
        for name, kind, start, first, penultimate, last in cases:
            for level, entry in [(-3, 0), (0, 0), (start-1, 0), (start, first),
                                 (49, penultimate), (50, last), (100, last)]:
                for saved in [False, True]:
                    for upper in [False, True]:
                        with self.subTest(name=name, level=level, saved=saved, upper=upper):
                            ctx = self.context(name, level)
                            self.api.saves_spell = Mock(return_value=saved)
                            # Exercise the common table path; follow-ups are tested separately.
                            with patch('random.randint', side_effect=lambda low, high: high if upper else low) as roll:
                                self.api.damage_table(ctx, 'DAM_' + kind)
                            roll.assert_called_once_with(entry // 2, entry * 2)
                            call = self.api.saves_spell.call_args
                            self.assertEqual(max(0, min(level, 50)), call.args[0].level)
                            self.assertEqual('DAM_' + kind, call.args[1])
                            self.assertEqual(1, self.api.saves_spell.call_count)
                            damage = entry * 2 if upper else entry // 2
                            self.assertEqual(damage // 2 if saved else damage, self.fight.damage.call_args.args[2])
                            self.assertEqual(level, ctx.level)
                            self.assertTrue(ctx.performed)

    def test_chill_collection_uses_one_save_and_joins_effect_before_damage(self):
        for saved in [False, True]:
            with self.subTest(saved=saved):
                ctx = self.context('chill touch', 100)
                order = []
                self.api.saves_spell = Mock(return_value=saved)
                self.effects.reset_mock()
                self.effects.apply_spell_effects.side_effect = lambda *a, **kw: order.append('effect')
                self.fight.damage.side_effect = lambda *a, **kw: order.append('damage') or {}
                with patch('random.randint', return_value=54):
                    self.api.execute_lambdas(ctx)
                self.assertEqual(['damage'] if saved else ['effect', 'damage'], order)
                self.api.saves_spell.assert_called_once()
                self.assertEqual(27 if saved else 54, self.fight.damage.call_args.args[2])
                if not saved:
                    call = self.effects.apply_spell_effects.call_args
                    self.assertEqual({'caster_level': 50, 'join': True}, call.kwargs)
                    effect = ctx.spell.affect_data[0]
                    self.assertEqual(('APPLY_STR', '-1', '6'), (effect['location'], effect['modifier'], effect['duration']))

    def test_colour_spray_invokes_blindness_at_half_bounded_level_before_damage(self):
        for light_save, blind_save, already_blind in [(True, False, False), (False, True, False),
                                                     (False, False, False), (False, False, True)]:
            with self.subTest(light_save=light_save, blind_save=blind_save, already_blind=already_blind):
                ctx = self.context('colour spray', 100)
                self.api.saves_spell = Mock(side_effect=[light_save, blind_save])
                self.api._effect_active.return_value = already_blind
                self.effects.reset_mock()
                order = []
                self.effects.apply_spell_effects.side_effect = lambda *a, **kw: order.append('blindness')
                self.fight.damage.side_effect = lambda *a, **kw: order.append('damage') or {}
                with patch('random.randint', return_value=158):
                    self.assertTrue(self.api.execute_lambdas(ctx))
                calls = self.api.saves_spell.call_args_list
                self.assertEqual('DAM_LIGHT', calls[0].args[1])
                self.assertEqual(50, calls[0].args[0].level)
                self.assertEqual(1 if light_save or already_blind else 2, len(calls))
                if len(calls) == 2:
                    self.assertEqual(25, calls[1].args[0].level)
                    self.assertEqual('DAM_OTHER', calls[1].args[1])
                applied = not light_save and not blind_save and not already_blind
                self.assertEqual(['blindness', 'damage'] if applied else ['damage'], order)
                if applied:
                    call = self.effects.apply_spell_effects.call_args
                    self.assertEqual('blindness', call.args[2].name)
                    self.assertEqual(25, call.kwargs['caster_level'])
                self.assertEqual(79 if light_save else 158, self.fight.damage.call_args.args[2])
                self.assertFalse(ctx.done)
                self.assertEqual(100, ctx.level)


if __name__ == "__main__":
    unittest.main()
