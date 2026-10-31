"""Build mobile prototypes and construct independent runtime instances."""
from server.LoggerFactory import LoggerFactory
from mobile.ArmorClass import ArmorClass
from mobile.Dice import Dice
from typing import Tuple
from enum import IntEnum
import json
from item.ItemFactory import ItemFactory
from copy import copy, deepcopy

from api.CharacterApi import CharacterApi
from api.GameApi import GameApi
from game.EnumProvider import EnumProvider
from game.Equipped import WEAR_LOC_TO_EQUIPPED_SLOT
from game.RandomNumberGenerator import RandomNumberGenerator
from game.StatusFlags import StatusFlags
from item.Effect import AffectWhere, Effect
from mobile.Mobile import Mobile
from util.GenericUtil import GenericUtil

rng = RandomNumberGenerator()


class MobileFactory:
    @staticmethod
    def from_data(raw_mobile: dict, races: dict) -> Mobile | None:
        """Build a content-service prototype without applying runtime spawn rules."""

        mobile_data = GenericUtil.camel_to_snake_case(raw_mobile)
        mobile_id = MobileFactory.resolve_mobile_id(mobile_data, raw_mobile)
        if mobile_id is None:
            return None
        player_name = str(mobile_data.get("name", "") or "")
        race_name = MobileFactory.resolve_race_name(races, mobile_data.get("race"), player_name)
        status_flags = MobileFactory.resolve_mobile_flags(mobile_data)
        level = GenericUtil.to_int(mobile_data.get("level", 0), default=0)
        normalized = MobileFactory.build_normalized_mobile_data(mobile_id, mobile_data, player_name, race_name, level)
        mobile = Mobile.from_json(normalized)
        mobile.status_flags = status_flags
        MobileFactory.apply_extended_mobile_fields(mobile, mobile_data)
        return mobile

    @staticmethod
    def _random_dam_type() -> int:
        dam_type = {0: 3, 1: 7, 2: 11}
        return dam_type[rng.dice(0, 2)]

    @staticmethod
    def _apply_mob_stat_bonuses(mob: Mobile, enum_provider: EnumProvider):
        act_bits = enum_provider.get('actBits')
        off_bits = enum_provider.get('offenseTypes')
        size_enum = enum_provider.get('size')
        mob.character_attributes.strength = min(25, 11 + mob.level // 4)
        mob.character_attributes.intelligence = min(25, 11 + mob.level // 4)
        mob.character_attributes.wisdom = min(25, 11 + mob.level // 4)
        mob.character_attributes.dexterity = min(25, 11 + mob.level // 4)
        mob.character_attributes.constitution = min(25, 11 + mob.level // 4)

        if GameApi.is_set(mob.status_flags.act, act_bits.ACT_WARRIOR):
            mob.character_attributes.strength += 3
            mob.character_attributes.intelligence -= 1
            mob.character_attributes.constitution += 2
        if GameApi.is_set(mob.status_flags.act, act_bits.ACT_THIEF):
            mob.character_attributes.dexterity += 3
            mob.character_attributes.intelligence += 1
            mob.character_attributes.wisdom -= 1
        if GameApi.is_set(mob.status_flags.act, act_bits.ACT_CLERIC):
            mob.character_attributes.wisdom += 3
            mob.character_attributes.dexterity -= 1
            mob.character_attributes.strength += 1
        if GameApi.is_set(mob.status_flags.act, act_bits.ACT_MAGE):
            mob.character_attributes.intelligence += 3
            mob.character_attributes.strength -= 1
            mob.character_attributes.dexterity += 1

        if GameApi.is_set(mob.status_flags.off, off_bits.OFF_FAST):
            mob.character_attributes.dexterity += 2

        size_key = "SIZE_" + mob.size.upper()
        size_bonus = size_enum[size_key] - 2
        mob.character_attributes.strength += size_bonus
        mob.character_attributes.constitution += GenericUtil.trunc_div(size_bonus, 2)

    @staticmethod
    def _apply_affected_by(mob: Mobile, enum_provider: EnumProvider):
        from item.EffectHandler import EffectHandler

        affect_bits = enum_provider.get('affectedBy')
        apply_types = enum_provider.get('applyTypes')
        handler = EffectHandler(enum_provider)
        haste_modifier = 1 + (mob.level >= 18) + (mob.level >= 25) + (mob.level >= 32)
        for flag, spell, location, modifier in (
                ('AFF_SANCTUARY', 'spell.sanctuary', 'APPLY_NONE', 0),
                ('AFF_HASTE', 'spell.haste', 'APPLY_DEX', haste_modifier),
                ('AFF_PROTECT_EVIL', 'spell.protection_evil', 'APPLY_SAVES', -1),
                ('AFF_PROTECT_GOOD', 'spell.protection_good', 'APPLY_SAVES', -1)):
            bit = affect_bits[flag]
            if CharacterApi.is_affected(mob, bit):
                effect = MobileFactory._build_affect_data(
                    mob.level, spell, AffectWhere.TO_AFFECTS.value, -1,
                    modifier, apply_types[location].value, bit.value)
                handler.affect_to_char(mob, effect)

    @staticmethod
    def _build_affect_data(level: int, aff_type: str, where: int, duration: int, modifier: int, location: int, bitvector: int) -> Effect:
        return Effect(valid=True, level=level, where=where, type=aff_type, duration=duration, modifier=modifier, location=location, bitvector=bitvector)

    @staticmethod
    def create(prototype: Mobile, enum_provider: EnumProvider) -> Mobile:
        """Spawn a fresh runtime mobile using prototype stats and spawn rules."""
        from player.CharacterAttributes import CharacterAttributes
        if prototype is None:
            raise ValueError("Cannot create mobile from None index")

        mob = Mobile.from_json({
            "area_id": prototype.area_id,
            "room_id": prototype.room_id,
            "vnum": prototype.vnum,
            "id": GenericUtil.generate_mongo_id(),
            "name": prototype.name,
            "short_description": prototype.short_description,
            "long_description": prototype.long_description,
            "description": prototype.description,
            "race": prototype.race,
            "alignment": str(prototype.get_alignment()),
            "group": prototype.group,
            "dam_type": prototype.dam_type,
            "start_pos": prototype.start_pos,
            "default_pos": prototype.default_pos,
            "sex": prototype.sex,
            "size": prototype.size,
            "material": prototype.material,
            "level": prototype.level,
            "hit_roll": prototype.hit_roll,
            "gold": 0,
            "silver": 0,
            "flags": None,
            "status_flags": prototype.status_flags,
            "special_name": prototype.special_name,
            "special_function": list(prototype.special_function),
            "character_attributes": CharacterAttributes.default()
        })

        if prototype.gold and prototype.gold > 0:
            wealth = rng.number_range(prototype.gold // 2, 3 * prototype.gold // 2)
            mob.gold = rng.number_range(wealth // 200, wealth // 100)
            mob.silver = wealth - (mob.gold * 100)
        else:
            mob.gold = 0
            mob.silver = 0

        mob.set_alignment(prototype.get_alignment())
        mob.level = prototype.level
        mob.hit_roll = prototype.hit_roll

        mob.hit_dice = prototype.hit_dice
        mob.mana_dice = prototype.mana_dice
        mob.damage_dice = prototype.damage_dice

        mob.max_hit = rng.dice(prototype.hit_dice.number, prototype.hit_dice.type) + prototype.hit_dice.bonus
        mob.hit = mob.max_hit
        mob.max_mana = rng.dice(prototype.mana_dice.number, prototype.mana_dice.type) + prototype.mana_dice.bonus
        mob.mana = mob.max_mana

        mob.dam_type = prototype.dam_type
        if not mob.dam_type or mob.dam_type == "none":
            mob.dam_type = MobileFactory._random_dam_type()

        # ROM copies all four armor values into each mobile's own runtime state.
        mob.armor_class = copy(prototype.armor_class)
        if prototype.status_flags is not None:
            mob.status_flags = StatusFlags.from_template(prototype.status_flags)
        mob.start_pos = prototype.start_pos
        mob.default_pos = prototype.default_pos
        mob.character_attributes.position = mob.start_pos
        mob.sex = prototype.sex
        if mob.sex == "3":
            mob.sex = str(rng.number_range(1, 2))

        mob.size = prototype.size
        mob.material = prototype.material

        MobileFactory._apply_mob_stat_bonuses(mob, enum_provider)
        MobileFactory._apply_affected_by(mob, enum_provider)

        mob.position = mob.start_pos
        return mob

    @staticmethod
    def copy_instance(mob: Mobile, enum_provider: EnumProvider, item_filter=None, effect_handler=None) -> Mobile:
        """Copy a mobile, optionally filtering possessions and their nested contents."""
        clone = MobileFactory.create(mob, enum_provider)
        clone.short_description = mob.short_description
        clone.long_description = mob.long_description
        clone.description = mob.description
        clone.name = mob.name
        clone.race = mob.race
        clone.flags = mob.flags
        clone.set_alignment(mob.get_alignment())
        clone.group = mob.group
        clone.dam_type = mob.dam_type
        clone.sex = mob.sex
        clone.size = mob.size
        clone.material = mob.material
        clone.level = mob.level
        clone.hit_roll = mob.hit_roll
        clone.gold = mob.gold
        clone.silver = mob.silver
        clone.start_pos = mob.start_pos
        clone.default_pos = mob.default_pos
        clone.status_flags = StatusFlags.from_template(mob.status_flags) if mob.status_flags is not None else None
        # create() supplies a fresh identity and spawn-only setup; a clone then
        # inherits live state, not the newly rolled resources or start position.
        for name in ('hit', 'max_hit', 'mana', 'max_mana', 'movement', 'max_movement',
                     'position', 'saving_throw', 'dam_roll', 'timer', 'wimpy',
                     'character_attributes', 'armor_class', 'hit_dice', 'mana_dice',
                     'damage_dice', 'effects', 'extra_flags', 'special_name', 'special_function'):
            if hasattr(mob, name):
                setattr(clone, name, deepcopy(getattr(mob, name)))
        clone.trust = 0
        item_ids = {}
        for item in mob.owned_items():
            if item_filter is not None and not item_filter(item):
                if effect_handler is not None:
                    effect_handler.remove_item_effects(clone, item)
                continue
            copied = ItemFactory.copy_instance(item, item_filter=item_filter)
            item_ids[str(item.id)] = str(copied.id)
            slot = mob.equipped_slot_of(item)
            if slot is None:
                slot = WEAR_LOC_TO_EQUIPPED_SLOT.get(GenericUtil.to_int(getattr(item, "wear_loc", -1), -1))
            if slot is not None:
                clone.equip_item(copied, slot)
                copied._effect_wearer = clone
            else:
                clone.add_item(copied)
        for effect in (getattr(clone, 'effects', []) or []):
            for old_id, new_id in item_ids.items():
                if effect.belongs_to_item(old_id):
                    effect.source = Effect.item_source(new_id)
                    break
        return clone

    @staticmethod
    def resolve_mobile_id(mobile_data: dict, raw_mobile: dict) -> str | None:
        mobile_id = str(mobile_data.get("id") or mobile_data.get("_id") or mobile_data.get("vnum") or "").strip()
        if mobile_id:
            return mobile_id
        LoggerFactory.get_logger("MobileFactory").error("Skipping mobile with missing id/vnum: " + str(raw_mobile))
        return None

    @staticmethod
    def resolve_mobile_flags(mobile_data: dict) -> StatusFlags:
        return StatusFlags.from_json(mobile_data.get("status_flags", {}))

    @staticmethod
    def parse_combat_flags(value) -> dict:
        if isinstance(value, dict):
            return value
        text = str(value or "").strip()
        if not text:
            return {}
        try:
            parsed = json.loads(text.replace("'", '"'))
            return parsed if isinstance(parsed, dict) else {}
        except json.JSONDecodeError:
            return {}

    @staticmethod
    def resolve_combat_flag(mobile_data: dict, combat_raw: dict, snake_key: str, camel_key: str, flag_letters: type[IntEnum] | None) -> int:
        value = combat_raw.get(snake_key, combat_raw.get(camel_key))
        if value in (None, ""):
            value = mobile_data.get(snake_key, mobile_data.get(camel_key))
        if isinstance(value, str):
            return GameApi.parse_flag_string(value, flag_letters)
        return GenericUtil.to_int(value, default=0)

    @staticmethod
    def resolve_race_name(races, explicit_race, player_name: str) -> str:
        candidates = []
        if explicit_race is not None:
            candidates.append(str(explicit_race).strip().lower())
        if player_name:
            first = player_name.strip().split()[0].lower()
            if first:
                candidates.append(first)
        candidates.append("human")

        for candidate in candidates:
            if candidate in races:
                race = races[candidate]
                race_id = race.get("id")
                if race_id:
                    return str(race_id)
                name = race.get("name")
                if name:
                    return str(name).lower()
                return candidate
        return "human"

    @staticmethod
    def race_flag_value(race: dict, key: str, race_name: str | None) -> int:
        race_data = race.get(race_name, {})
        if not race:
            return 0
        value = race_data.get(key, 0)
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def parse_dice(mobile_data: dict) -> Tuple[Dice, Dice, Dice]:
        hit_dice = Dice.from_json(str(mobile_data.get("hit_dice")))
        mana_dice = Dice.from_json(str(mobile_data.get("mana_dice")))
        damage_dice = Dice.from_json(str(mobile_data.get("damage_dice")))
        return hit_dice, mana_dice, damage_dice

    @staticmethod
    def parse_ac(mobile_data: dict) -> ArmorClass:
        ac = mobile_data.get("armor_class")
        if ac is None:
            LoggerFactory.get_logger("MobileFactory").warning("AC is None for mobile: {mobile_data")
            return ArmorClass(bash=0, pierce=0, slash=0, exotic=0)
        return ArmorClass.from_json(mobile_data.get("armor_class"))

    @staticmethod
    def apply_extended_mobile_fields(mobile: Mobile, mobile_data: dict):
        mobile.armor_class = MobileFactory.parse_ac(mobile_data)
        mobile.hit_dice, mobile.mana_dice, mobile.damage_dice = MobileFactory.parse_dice(mobile_data)
        mobile.hitroll = GenericUtil.to_int(mobile_data.get("hitroll", 0), default=0)
        mobile.wealth = GenericUtil.to_int(mobile_data.get("wealth", mobile_data.get("gold", 0)), default=0)

    @staticmethod
    def build_normalized_mobile_data(mobile_id: str, mobile_data: dict, player_name: str, race_name: str, level: int) -> dict:
        start_pos = mobile_data.get("start_pos")
        default_pos = mobile_data.get("default_pos")
        sex_value = mobile_data.get("sex")
        return {
            "area_id": str(mobile_data.get("area_id", "") or ""),
            "room_id": str(mobile_data.get("room_id", "") or ""),
            "vnum": str(mobile_data.get("vnum", mobile_id) or mobile_id),
            "name": player_name,
            "short_description": str(mobile_data.get("short_description", "") or ""),
            "long_description": MobileFactory.capitalize_first(mobile_data.get("long_description", "")),
            "description": MobileFactory.capitalize_first(mobile_data.get("description", "")),
            "race": race_name,
            "alignment": str(mobile_data.get("alignment", "0") or "0"),
            "group": str(GenericUtil.to_int(mobile_data.get("group", 0), default=0)),
            "dam_type": str(mobile_data.get("dam_type", "") or ""),
            "start_pos": GenericUtil.to_int(start_pos, default=0),
            "default_pos": GenericUtil.to_int(default_pos, default=0),
            "sex": str(sex_value),
            "size": str(mobile_data.get("size", "") or ""),
            "material": str(mobile_data.get("material", "") or ""),
            "flags": str(mobile_data.get("flags", "") or ""),
            "id": mobile_id,
            "level": level,
            "hit_roll": GenericUtil.to_int(mobile_data.get("hit_roll", 0), default=0),
            "hit_dice": None,
            "mana_dice": None,
            "damage_dice": None,
            "armor_class": None,
            "gold": GenericUtil.to_int(mobile_data.get("gold", 0), default=0),
            "silver": GenericUtil.to_int(mobile_data.get("silver", 0), default=0),
            "status_flags": None,
            "lock": mobile_data.get("lock"),
        }

    @staticmethod
    def capitalize_first(value) -> str:
        text = str(value or "")
        return text[:1].upper() + text[1:] if text else ""
