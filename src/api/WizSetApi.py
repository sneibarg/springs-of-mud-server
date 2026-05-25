from __future__ import annotations

from injector import inject

from api.CharacterApi import CharacterApi
from api.GameApi import GameApi
from game.RegistryService import RegistryService
from game.WizHandler import WizHandler
from player.CharacterClass import CharacterClass
from player.CharacterRace import CharacterRace
from util.GenericUtil import GenericUtil
from util.SkillUtil import SkillUtil
from util.WizUtil import WizUtil


class WizSetApi:
    STAT_FIELDS = {
        "str": ("strength", 0, "Strength"),
        "int": ("intelligence", 1, "Intelligence"),
        "wis": ("wisdom", 2, "Wisdom"),
        "dex": ("dexterity", 3, "Dexterity"),
        "con": ("constitution", 4, "Constitution"),
    }

    @inject
    def __init__(self,
                 registry_service: RegistryService,
                 wiz_handler: WizHandler):
        self.registry_service = registry_service
        self.wiz_handler = wiz_handler
        self.character_registry = registry_service.character_registry
        self.room_registry = registry_service.room_registry
        self.item_registry = registry_service.item_registry
        self.skill_registry = registry_service.skill_registry
        self.spell_registry = registry_service.spell_registry

    def dispatch(self, actor, context) -> dict:
        raw = WizUtil.argument_text(context.result, context.parameters)
        set_type, rest = WizUtil.split_argument(raw)
        kind = str(set_type or "").strip().lower()
        if not kind:
            context.finish()
            return self._payload("syntax")

        if kind in ("mob", "mobile", "char", "character"):
            return self._set_mobile(context, rest)
        if kind in ("skill", "spell"):
            return self._set_skill(context, rest)
        if kind in ("obj", "object"):
            return self._set_object(context, rest)
        if kind == "room":
            return self._set_room(actor, context, rest)

        context.finish()
        return self._payload("syntax")

    def _set_skill(self, context, raw: str) -> dict:
        parts = str(raw or "").split(maxsplit=2)
        if len(parts) < 3:
            context.finish()
            return self._payload("skill_syntax")

        target_name, skill_name, value_text = parts
        victim = WizUtil.find_world_entity(
            self.character_registry,
            self.room_registry,
            target_name,
            include_mobiles=False,
        )
        if victim is None:
            context.finish()
            return self._payload("target_missing")
        if CharacterApi.is_npc(victim):
            context.finish()
            return self._payload("no_npcs")
        if not value_text.lstrip("-").isdigit():
            context.finish()
            return self._payload("value_must_be_numeric")

        value = GenericUtil.to_int(value_text, -1)
        if value < 0 or value > 100:
            context.finish()
            return self._payload("skill_range")

        if str(skill_name or "").strip().lower() == "all":
            for skill in sorted(self.skill_registry.all_skills(), key=lambda entry: str(getattr(entry, "name", "") or "").lower()):
                SkillUtil.set_character_learned_level(victim, getattr(skill, "name", ""), value, collection_name="skills")
            for spell in sorted(self.spell_registry.all_spells(), key=lambda entry: str(getattr(entry, "name", "") or "").lower()):
                SkillUtil.set_character_learned_level(victim, getattr(spell, "name", ""), value, collection_name="spells")
            context.finish()
            return {"to_char": ""}

        ability, collection_name = self._ability_lookup(skill_name)
        if ability is None:
            context.finish()
            return self._payload("unknown_skill")

        SkillUtil.set_character_learned_level(victim, getattr(ability, "name", skill_name), value, collection_name=collection_name)
        context.finish()
        return {"to_char": ""}

    def _set_mobile(self, context, raw: str) -> dict:
        parts = str(raw or "").split(maxsplit=2)
        if len(parts) < 3:
            context.finish()
            return self._payload("mobile_syntax")

        target_name, field_name, value_text = parts
        victim = WizUtil.find_world_entity(self.character_registry, self.room_registry, target_name)
        if victim is None:
            context.finish()
            return self._payload("target_missing")

        field = str(field_name or "").strip().lower()
        value = GenericUtil.to_int(value_text, -1)

        if field in self.STAT_FIELDS:
            return self._set_stat_field(context, victim, field, value)

        if field.startswith("sex"):
            if value < 0 or value > 2:
                context.finish()
                return self._payload("sex_range")
            victim.sex = str(value)
            context.finish()
            return {"to_char": ""}

        if field.startswith("class"):
            if CharacterApi.is_npc(victim):
                context.finish()
                return self._payload("mobiles_have_no_class")
            class_data = CharacterApi.class_data(value_text)
            if not class_data:
                context.finish()
                return self._payload("invalid_class", tokens={"s": " ".join(CharacterApi.class_names())})
            victim.character_class = CharacterClass.from_json({"name": value_text, **class_data})
            race_data = CharacterApi.pc_races_map().get(str(getattr(victim, "race", "") or "").strip().lower(), {})
            if race_data:
                victim.character_race = CharacterRace.from_json(race_data, character_class=victim.character_class)
            context.finish()
            return {"to_char": ""}

        if field.startswith("level"):
            if not CharacterApi.is_npc(victim):
                context.finish()
                return self._payload("pc_invalid")
            max_level = GenericUtil.to_int(getattr(CharacterApi.get_enum("gameParameters"), "MAX_LEVEL", 0).value if hasattr(CharacterApi.get_enum("gameParameters"), "MAX_LEVEL") else 0, 0)
            if value < 0 or value > max_level:
                context.finish()
                return self._payload("level_range", tokens={"d": max_level})
            victim.level = value
            context.finish()
            return {"to_char": ""}

        if field.startswith("gold"):
            victim.gold = value
            context.finish()
            return {"to_char": ""}

        if field.startswith("silver"):
            victim.silver = value
            context.finish()
            return {"to_char": ""}

        if field.startswith("hp"):
            if value < -10 or value > 30000:
                context.finish()
                return self._payload("hp_range")
            victim.max_hit = value
            context.finish()
            return {"to_char": ""}

        if field.startswith("mana"):
            if value < 0 or value > 30000:
                context.finish()
                return self._payload("mana_range")
            victim.max_mana = value
            context.finish()
            return {"to_char": ""}

        if field.startswith("move"):
            if value < 0 or value > 30000:
                context.finish()
                return self._payload("move_range")
            victim.max_movement = value
            context.finish()
            return {"to_char": ""}

        if field.startswith("practice") or field == "prac":
            if value < 0 or value > 250:
                context.finish()
                return self._payload("practice_range")
            victim.character_attributes.practices = value
            context.finish()
            return {"to_char": ""}

        if field.startswith("train"):
            if value < 0 or value > 50:
                context.finish()
                return self._payload("train_range")
            victim.character_attributes.trains = value
            context.finish()
            return {"to_char": ""}

        if field.startswith("align"):
            if value < -1000 or value > 1000:
                context.finish()
                return self._payload("align_range")
            victim.character_attributes.alignment = value
            context.finish()
            return {"to_char": ""}

        if field in ("thirst", "drunk", "full", "hunger"):
            if CharacterApi.is_npc(victim):
                context.finish()
                return self._payload("npc_invalid")
            if value < -1 or value > 100:
                context.finish()
                return self._payload("condition_range", tokens={"t": field.capitalize()})
            status_flags = getattr(victim, "status_flags", None)
            if status_flags is not None:
                target_field = "hunger" if field == "full" else field
                setattr(status_flags, target_field, value)
            context.finish()
            return {"to_char": ""}

        if field.startswith("race"):
            return self._set_race_field(context, victim, value_text)

        if field.startswith("group"):
            if not CharacterApi.is_npc(victim):
                context.finish()
                return self._payload("group_npc_only")
            victim.group = str(value)
            context.finish()
            return {"to_char": ""}

        context.finish()
        return self._payload("mobile_syntax")

    def _set_object(self, context, raw: str) -> dict:
        parts = str(raw or "").split(maxsplit=2)
        if len(parts) < 3:
            context.finish()
            return self._payload("object_syntax")

        target_name, field_name, value_text = parts
        obj = WizUtil.find_world_item(self.character_registry, self.room_registry, target_name)
        if obj is None:
            context.finish()
            return self._payload("no_such_object")

        field = str(field_name or "").strip().lower()
        value = GenericUtil.to_int(value_text, 0)
        if field in ("value0", "v0"):
            obj.value0 = str(min(50, value))
        elif field in ("value1", "v1"):
            obj.value1 = str(value)
        elif field in ("value2", "v2"):
            obj.value2 = str(value)
        elif field in ("value3", "v3"):
            obj.value3 = str(value)
        elif field in ("value4", "v4"):
            obj.value4 = str(value)
        elif field.startswith("extra"):
            obj.extra_flags = str(GameApi.flags_to_int(value_text))
        elif field.startswith("wear"):
            obj.wear_flags = str(GameApi.flags_to_int(value_text))
        elif field.startswith("level"):
            obj.level = value
        elif field.startswith("weight"):
            obj.weight = value
        elif field.startswith("cost"):
            obj.cost = value
        elif field.startswith("timer"):
            obj.timer = value
        else:
            context.finish()
            return self._payload("object_syntax")

        context.finish()
        return {"to_char": ""}

    def _set_room(self, actor, context, raw: str) -> dict:
        parts = str(raw or "").split(maxsplit=2)
        if len(parts) < 3:
            context.finish()
            return self._payload("room_syntax")

        location_name, field_name, value_text = parts
        location = CharacterApi.find_location(location_name, self.room_registry, self.character_registry, WizUtil.name_matches)
        if location is None:
            context.finish()
            return self._payload("no_such_location")
        if self.wiz_handler.room_is_private_for_actor(actor, location, implementor_only=True):
            context.finish()
            return self._payload("private_room")
        if not value_text.lstrip("-").isdigit():
            context.finish()
            return self._payload("value_must_be_numeric")

        value = GenericUtil.to_int(value_text, 0)
        field = str(field_name or "").strip().lower()
        if field.startswith("flags"):
            location.room_flags = value
        elif field.startswith("sector"):
            location.sector_type = value
        else:
            context.finish()
            return self._payload("room_syntax")

        context.finish()
        return {"to_char": ""}

    def _set_stat_field(self, context, victim, field: str, value: int) -> dict:
        attr_name, stat_index, label = self.STAT_FIELDS[field]
        attributes = getattr(victim, "character_attributes", None)
        if attributes is None:
            context.finish()
            return self._payload("mobile_syntax")

        current_value = GenericUtil.to_int(getattr(attributes, attr_name, 0), 0)
        max_train = self._max_train_for(victim, stat_index, current_value)
        if value < 3 or value > max_train:
            context.finish()
            return self._payload("stat_range", tokens={"t": label, "n": max_train})
        setattr(attributes, attr_name, value)
        context.finish()
        return {"to_char": ""}

    def _set_race_field(self, context, victim, race_name: str) -> dict:
        if CharacterApi.is_npc(victim):
            race_key = self._lookup_race_name(race_name, include_pc=True, include_mobile=True)
            if not race_key:
                context.finish()
                return self._payload("invalid_race")
            victim.race = race_key
            context.finish()
            return {"to_char": ""}

        race_key = self._lookup_race_name(race_name, include_pc=True, include_mobile=False)
        if not race_key:
            if self._lookup_race_name(race_name, include_pc=False, include_mobile=True):
                context.finish()
                return self._payload("invalid_player_race")
            context.finish()
            return self._payload("invalid_race")

        race_data = CharacterApi.pc_races_map().get(race_key, {})
        victim.character_race = CharacterRace.from_json(race_data, character_class=getattr(victim, "character_class", None))
        context.finish()
        return {"to_char": ""}

    def _ability_lookup(self, wanted: str):
        query = str(wanted or "").strip().lower()
        if not query:
            return None, ""

        skill_prefix = None
        for skill in self.skill_registry.all_skills():
            name = str(getattr(skill, "name", "") or "").strip().lower()
            if not name:
                continue
            if name == query:
                return skill, "skills"
            if skill_prefix is None and name.startswith(query):
                skill_prefix = skill

        spell_prefix = None
        for spell in self.spell_registry.all_spells():
            name = str(getattr(spell, "name", "") or "").strip().lower()
            if not name:
                continue
            if name == query:
                return spell, "spells"
            if spell_prefix is None and name.startswith(query):
                spell_prefix = spell

        if skill_prefix is not None:
            return skill_prefix, "skills"
        if spell_prefix is not None:
            return spell_prefix, "spells"
        return None, ""

    @staticmethod
    def _lookup_race_name(wanted: str, *, include_pc: bool, include_mobile: bool) -> str:
        query = str(wanted or "").strip().lower()
        if not query:
            return ""

        exact = ""
        prefix = ""
        maps = []
        if include_mobile:
            maps.append(CharacterApi.races_map())
        if include_pc:
            maps.append(CharacterApi.pc_races_map())

        for mapping in maps:
            for key in mapping.keys():
                label = str(key or "").strip().lower()
                if not label:
                    continue
                if label == query:
                    return label
                if not prefix and label.startswith(query):
                    prefix = label
                if not exact and query == str((mapping.get(key) or {}).get("name", "")).strip().lower():
                    exact = label
        return exact or prefix

    @staticmethod
    def _max_train_for(victim, stat_index: int, current_value: int) -> int:
        max_train = CharacterApi.get_max_train(victim, stat_index, current_value)
        if CharacterApi.is_npc(victim) and max_train <= current_value:
            return max(25, current_value)
        return max(3, max_train)

    @staticmethod
    def _payload(message_key: str, **extra) -> dict:
        payload = {"message_key": str(message_key or "")}
        payload.update(extra)
        return payload
