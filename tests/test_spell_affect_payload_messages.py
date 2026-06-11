import importlib.util
import json
import re
import sys
import types
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def _module(name: str, **attrs):
    module = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    return module


class _CharacterApi:
    @staticmethod
    def is_npc(entity):
        return bool(getattr(entity, "is_npc", False))


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
        "util.GenericUtil": _module(
            "util.GenericUtil",
            GenericUtil=SimpleNamespace(
                camel_to_snake_case=lambda dictionary: _camel_to_snake_case(dictionary),
                to_int=lambda value, default=0: int(value or default),
            ),
        ),
        "util.FightUtil": _module("util.FightUtil", FightUtil=SimpleNamespace(spell_handler_name=lambda name: f"spell.{name.replace(' ', '_')}")),
        "util.EffectUtil": _module("util.EffectUtil", EffectUtil=SimpleNamespace(handler=lambda: Mock())),
        "util.ItemUtil": _module("util.ItemUtil", ItemUtil=SimpleNamespace()),
        "util.PlayerUtil": _module("util.PlayerUtil", PlayerUtil=SimpleNamespace()),
        "server.LoggerFactory": _module("server.LoggerFactory", LoggerFactory=_LoggerFactory),
        "skill.SpellContext": _module("skill.SpellContext", SpellContext=object),
        "skill.SpellSpeech": _module("skill.SpellSpeech", SpellSpeech=SimpleNamespace(utterance=lambda *_args, **_kwargs: "")),
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

    def test_dispel_magic_queues_each_removed_effect_msg_off_for_victim(self):
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
            "spell.haste": [SimpleNamespace(type="spell.haste")],
            "spell.giant_strength": [SimpleNamespace(type="spell.giant_strength")],
        }.get(effect_name, [])

        self.assertTrue(SpellApi(effect_handler=effect_handler, interp_api=Mock()).dispel_magic(ctx))

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


if __name__ == "__main__":
    unittest.main()
