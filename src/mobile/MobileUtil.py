import json

from enum import IntEnum
from typing import Tuple

from game.GameMacros import GameMacros
from game.Equipped import Equipped, WEAR_LOC_TO_EQUIPPED_SLOT
from game.GenericUtil import GenericUtil
from mobile.Mobile import Mobile
from mobile.ArmorClass import ArmorClass
from mobile.Dice import Dice
from mobile.MobileFlags import MobileFlags
from game.RandomNumberGenerator import RandomNumberGenerator
from object.AffectData import AffectWhere, AffectData
from object.ObjectMacros import ObjectMacros
from player.CharacterMacros import CharacterMacros
from server.LoggerFactory import LoggerFactory

logger = LoggerFactory.get_logger('MobileUtil')
rng = RandomNumberGenerator()


class MobileUtil:
    pass

    @staticmethod
    def build_mobile(mobile_id: str, races: dict, mobile_data: dict, npc_flag: int, enums: dict[str, type[IntEnum]]) -> tuple[Mobile, int]:
        player_name = str(mobile_data.get("name", "") or "")
        race_name = MobileUtil.resolve_race_name(races, mobile_data.get("race"), player_name)
        race = races[race_name] or {}
        flag_letters = enums.get("flagLetters")
        flags = MobileUtil.resolve_mobile_flags(mobile_data, race, npc_flag, flag_letters)
        level = GenericUtil.to_int(mobile_data.get("level", 0), default=0)
        normalized = MobileUtil.build_normalized_mobile_data(mobile_id, mobile_data, player_name, race_name, level)

        mobile = Mobile.from_json(normalized)
        mobile.flags = flags
        MobileUtil.apply_extended_mobile_fields(mobile, mobile_data)
        return mobile, level

    @staticmethod
    def convert_form(race: str, form: int, object_macros: ObjectMacros):
        return object_macros.set_bit(form, object_macros.races[race].get(form, 0))

    @staticmethod
    def convert_parts(race: str, parts: int, object_macros: ObjectMacros):
        return object_macros.set_bit(parts, object_macros.races[race].get(parts, 0))

    @staticmethod
    def resolve_mobile_id(mobile_data: dict, raw_mobile: dict) -> str | None:
        mobile_id = str(mobile_data.get("id") or mobile_data.get("_id") or mobile_data.get("vnum") or "").strip()
        if mobile_id:
            return mobile_id
        logger.error("Skipping mobile with missing id/vnum: " + str(raw_mobile))
        return None

    @staticmethod
    def resolve_mobile_flags(mobile_data: dict, race: dict, npc_flag: int, flag_letters: type[IntEnum] | None) -> MobileFlags:
        raw_act = GenericUtil.to_int(mobile_data.get("actFlags") or mobile_data.get("act_flags"), 0)
        raw_aff = GenericUtil.to_int(mobile_data.get("affectFlags") or mobile_data.get("affect_flags"), 0)
        combat_raw = MobileUtil.parse_combat_flags(mobile_data.get("combat_flags"))
        raw_off = MobileUtil.resolve_combat_flag(mobile_data, combat_raw, "off_flags", "offFlags", flag_letters)
        raw_imm = MobileUtil.resolve_combat_flag(mobile_data, combat_raw, "imm_flags", "immFlags", flag_letters)
        raw_res = MobileUtil.resolve_combat_flag(mobile_data, combat_raw, "res_flags", "resFlags", flag_letters)
        raw_vuln = MobileUtil.resolve_combat_flag(mobile_data, combat_raw, "vuln_flags", "vulnFlags", flag_letters)
        raw_form = GenericUtil.to_int(mobile_data.get("form"), 0)
        raw_parts = GenericUtil.to_int(mobile_data.get("parts"), 0)
        race_act = MobileUtil.race_flag_value(race, "act", mobile_data.get("race"))
        race_aff = MobileUtil.race_flag_value(race, "aff", mobile_data.get("race"))
        race_off = MobileUtil.race_flag_value(race, "off", mobile_data.get("race"))
        race_imm = MobileUtil.race_flag_value(race, "imm", mobile_data.get("race"))
        race_res = MobileUtil.race_flag_value(race, "res", mobile_data.get("race"))
        race_vuln = MobileUtil.race_flag_value(race, "vuln", mobile_data.get("race"))
        race_form = MobileUtil.race_flag_value(race, "form", mobile_data.get("race"))
        race_parts = MobileUtil.race_flag_value(race, "parts", mobile_data.get("race"))
        mobile_flags = MobileFlags(
            act=raw_act | npc_flag | race_act,
            affected_by=raw_aff | race_aff,
            off=raw_off | race_off,
            imm=raw_imm | race_imm,
            res=raw_res | race_res,
            vuln=raw_vuln | race_vuln,
            form=raw_form | race_form,
            parts=raw_parts | race_parts,
        )
        MobileUtil.apply_flag_removes(mobile_flags, mobile_data.get("flag_removes",[]))  # this always defaults to [] - there are no flag removal entries in ROM2.4.
        return mobile_flags

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
            return GameMacros.parse_flag_string(value, flag_letters)
        return GenericUtil.to_int(value, default=0)

    @staticmethod
    def increment_kill_table(kill_table: dict[int, int], level: int):
        level_bucket = max(0, min(level, 100))
        kill_table[level_bucket] = kill_table.get(level_bucket, 0) + 1

    @staticmethod
    def resolve_npc_flag(game_data) -> int:
        for domain in ("act", "mob", "mobile", "mob_act"):
            for flag_name in ("ACT_IS_NPC", "IS_NPC"):
                try:
                    return game_data.flag_value(domain, flag_name)
                except KeyError:
                    pass
        logger.warning("ACT_IS_NPC not found in GameData; defaulting to 1.")
        return 1

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
            logger.warn("AC is None for mobile: {mobile_data")
            return ArmorClass(bash=0, pierce=0, slash=0, exotic=0)
        return ArmorClass.from_json(mobile_data.get("armor_class"))

    @staticmethod
    def apply_extended_mobile_fields(mobile: Mobile, mobile_data: dict):
        mobile.armor_class = MobileUtil.parse_ac(mobile_data)
        mobile.hit_dice, mobile.mana_dice, mobile.damage_dice = MobileUtil.parse_dice(mobile_data)
        mobile.hitroll = GenericUtil.to_int(mobile_data.get("hitroll", 0), default=0)
        mobile.wealth = GenericUtil.to_int(mobile_data.get("wealth", mobile_data.get("gold", 0)), default=0)

    @staticmethod
    def build_normalized_mobile_data(mobile_id: str, mobile_data: dict, player_name: str, race_name: str, level: int) -> dict:
        start_pos = mobile_data.get("start_pos")
        default_pos = mobile_data.get("default_pos")
        sex_value = mobile_data.get("sex")
        return {
            "area_id": str(mobile_data.get("area_id", "") or ""),
            "vnum": str(mobile_data.get("vnum", mobile_id) or mobile_id),
            "name": player_name,
            "short_description": str(mobile_data.get("short_description", "") or ""),
            "long_description": MobileUtil.capitalize_first(mobile_data.get("long_description", "")),
            "description": MobileUtil.capitalize_first(mobile_data.get("description", "")),
            "race": race_name,
            "act_flags": None,  # str(flags["act_flags"]),
            "affect_flags": None,  # str(flags["affect_flags"]),
            "alignment": str(mobile_data.get("alignment", "0") or "0"),
            "group": str(GenericUtil.to_int(mobile_data.get("group", 0), default=0)),
            "act": str(mobile_data.get("act", "") or ""),
            "dam_type": str(mobile_data.get("dam_type", "") or ""),
            "combat_flags": str(mobile_data.get("combat_flags", "") or ""),
            "start_pos": str(start_pos),
            "default_pos": str(default_pos),
            "sex": str(sex_value),
            "form": None,
            "parts": None,
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
            "pulse_wait": GenericUtil.to_int(mobile_data.get("pulse_wait", 0), default=0),
            "pulse_daze": GenericUtil.to_int(mobile_data.get("pulse_daze", 0), default=0),
            "mobile_flags": None,
            "lock": mobile_data.get("lock"),
        }

    @staticmethod
    def capitalize_first(value) -> str:
        text = str(value or "")
        return text[:1].upper() + text[1:] if text else ""

    @staticmethod
    def apply_flag_removes(flags: MobileFlags, removals: list):
        for removal in removals:
            domain = str(removal.get("domain", "")).lower().strip()
            vector = GenericUtil.to_int(removal.get("vector", 0))
            if domain == "act":
                flags.act &= ~vector
            elif domain.startswith("aff"):
                flags.affected_by &= ~vector
            elif domain == "off":
                flags.off &= ~vector
            elif domain == "imm":
                flags.imm &= ~vector
            elif domain == "res":
                flags.res &= ~vector
            elif domain.startswith("vul"):
                flags.vuln &= ~vector
            elif domain.startswith("for"):
                flags.form &= ~vector
            elif domain.startswith("par"):
                flags.parts &= ~vector

    @staticmethod
    def _random_dam_type() -> int:
        dam_type = {0: 3, 1: 7, 2: 11}
        return dam_type[rng.dice(0, 2)]

    @staticmethod
    def _apply_mob_stat_bonuses(mob: Mobile, enums: dict[str, type[IntEnum]]):
        act_bits = enums.get('actBits')
        off_bits = enums.get('offenseTypes')

        mob.perm_stat.strength = min(25, 11 + mob.level // 4)
        mob.perm_stat.intelligence = min(25, 11 + mob.level // 4)
        mob.perm_stat.wisdom = min(25, 11 + mob.level // 4)
        mob.perm_stat.dexterity = min(25, 11 + mob.level // 4)
        mob.perm_stat.constitution = min(25, 11 + mob.level // 4)

        if GameMacros.is_set(mob.mobile_flags.act, act_bits.ACT_WARRIOR.value):
            mob.perm_stat.strength += 3
            mob.perm_stat.intelligence -= 1
            mob.perm_stat.constitution += 2
        elif GameMacros.is_set(mob.mobile_flags.act, act_bits.ACT_THIEF.value):
            mob.perm_stat.dexterity += 3
            mob.perm_stat.intelligence += 1
            mob.perm_stat.wisdom -= 1
        elif GameMacros.is_set(mob.mobile_flags.act, act_bits.ACT_CLERIC.value):
            mob.perm_stat.wisdom += 3
            mob.perm_stat.dexterity -= 1
            mob.perm_stat.strength += 1
        elif GameMacros.is_set(mob.mobile_flags.act, act_bits.ACT_MAGE.value):
            mob.perm_stat.intelligence += 3
            mob.perm_stat.strength -= 1
            mob.perm_stat.dexterity += 1

        if GameMacros.is_set(mob.mobile_flags.off, off_bits.OFF_FAST.value):
            mob.perm_stat.dexterity += 2

        size_key = "SIZE_" + mob.size.upper()
        size_bonus = enums["size"][size_key] - 2
        mob.perm_stat.strength += size_bonus
        mob.perm_stat.constitution += size_bonus // 2

    #  aff_type needs to be replaced with the result of skill_lookup("haste") etc.
    @staticmethod
    def _apply_affected_by(mob: Mobile, enums: dict[str, type[IntEnum]], character_macros: CharacterMacros):
        affect_bits = enums.get('affectedBy')
        apply_types = enums.get('applyTypes')
        if character_macros.is_affected(mob, affect_bits.AFF_SANCTUARY):
            sanctuary = MobileUtil._build_affect_data(mob.level, 0, AffectWhere.TO_AFFECTS.value, -1, 0, apply_types.APPLY_NONE.value, affect_bits.AFF_SANCTUARY.value)
        if character_macros.is_affected(mob, affect_bits.AFF_HASTE):
            modifier = 1 + (mob.level >= 18) + (mob.level >= 25) + (mob.level >= 32)
            haste = MobileUtil._build_affect_data(mob.level, 0, AffectWhere.TO_AFFECTS.value, -1, modifier, apply_types.APPLY_DEX.value, affect_bits.AFF_HASTE.value)
        if character_macros.is_affected(mob, affect_bits.AFF_PROTECT_EVIL):
            protect_evil = MobileUtil._build_affect_data(mob.level, 0, AffectWhere.TO_AFFECTS.value, -1, -1, apply_types.APPLY_SAVES.value, affect_bits.AFF_PROTECT_EVIL.value)
        if character_macros.is_affected(mob, affect_bits.AFF_PROTECT_GOOD):
            protect_good = MobileUtil._build_affect_data(mob.level, 0, AffectWhere.TO_AFFECTS.value, -1, -1, apply_types.APPLY_SAVES.value, affect_bits.AFF_PROTECT_GOOD.value)

    @staticmethod
    def _build_affect_data(level: int, aff_type: int, where: int, duration: int, modifier: int, location: int, bitvector: int) -> AffectData:
        return AffectData(valid=True, level=level, where=where, type=aff_type, duration=duration, modifier=modifier, location=location, bitvector=bitvector)

    @staticmethod
    def create_mobile(pMobIndex: Mobile, enums: dict[str, type[IntEnum]], character_macros: CharacterMacros) -> Mobile:
        from player.CharacterAttributes import CharacterAttributes
        if pMobIndex is None:
            logger.error("create_mobile: NULL pMobIndex.")
            raise ValueError("Cannot create mobile from None index")

        mob = Mobile.from_json({
            "area_id": pMobIndex.area_id,
            "vnum": pMobIndex.vnum,
            "id": GenericUtil.generate_mongo_id(),
            "name": pMobIndex.name,
            "short_description": pMobIndex.short_description,
            "long_description": pMobIndex.long_description,
            "description": pMobIndex.description,
            "race": pMobIndex.race,
            "act_flags": pMobIndex.act_flags,
            "affect_flags": pMobIndex.affect_flags,
            "alignment": pMobIndex.alignment,
            "group": pMobIndex.group,
            "dam_type": pMobIndex.dam_type,
            "start_pos": pMobIndex.start_pos,
            "default_pos": pMobIndex.default_pos,
            "sex": pMobIndex.sex,
            "form": pMobIndex.form,
            "parts": pMobIndex.parts,
            "size": pMobIndex.size,
            "material": pMobIndex.material,
            "level": pMobIndex.level,
            "hit_roll": pMobIndex.hit_roll,
            "gold": 0,
            "silver": 0,
            "flags": None,
            "act": None,
            "pulse_wait": 0,
            "pulse_daze": 0,
            "perm_stat": CharacterAttributes.default()
        })

        if pMobIndex.gold and pMobIndex.gold > 0:
            wealth = rng.number_range(pMobIndex.gold // 2, 3 * pMobIndex.gold // 2)
            mob.gold = rng.number_range(wealth // 200, wealth // 100)
            mob.silver = wealth - (mob.gold * 100)
        else:
            mob.gold = 0
            mob.silver = 0

        if True:
            mob.act = pMobIndex.act_flags
            mob.affect_flags = pMobIndex.affect_flags
            mob.alignment = pMobIndex.alignment
            mob.level = pMobIndex.level
            mob.hit_roll = pMobIndex.hit_roll

            mob.hit_dice = pMobIndex.hit_dice
            mob.mana_dice = pMobIndex.mana_dice
            mob.damage_dice = pMobIndex.damage_dice

            mob.max_hit = rng.dice(pMobIndex.hit_dice.number, pMobIndex.hit_dice.type) + pMobIndex.hit_dice.bonus
            mob.hit = mob.max_hit
            mob.max_mana = rng.dice(pMobIndex.mana_dice.number, pMobIndex.mana_dice.type) + pMobIndex.mana_dice.bonus
            mob.mana = mob.max_mana

            mob.dam_type = pMobIndex.dam_type
            if not mob.dam_type or mob.dam_type == "none":
                mob.dam_type = MobileUtil._random_dam_type()

            mob.armor_class = pMobIndex.armor_class
            if pMobIndex.mobile_flags is not None:
                mob.mobile_flags = MobileFlags(
                    act=pMobIndex.mobile_flags.act,
                    affected_by=pMobIndex.mobile_flags.affected_by,
                    off=pMobIndex.mobile_flags.off,
                    imm=pMobIndex.mobile_flags.imm,
                    res=pMobIndex.mobile_flags.res,
                    vuln=pMobIndex.mobile_flags.vuln,
                    form=pMobIndex.mobile_flags.form,
                    parts=pMobIndex.mobile_flags.parts
                )
            mob.start_pos = pMobIndex.start_pos
            mob.default_pos = pMobIndex.default_pos
            mob.perm_stat.position = mob.start_pos
            mob.sex = pMobIndex.sex
            if mob.sex == "3":
                mob.sex = str(rng.number_range(1, 2))

            mob.size = pMobIndex.size
            mob.material = pMobIndex.material

            MobileUtil._apply_mob_stat_bonuses(mob, enums)
            MobileUtil._apply_affected_by(mob, enums, character_macros)

        mob.position = mob.start_pos
        pMobIndex.count = getattr(pMobIndex, 'count', 0) + 1

        return mob

    @staticmethod
    def add_inventory_item(mob: Mobile, item):
        if not hasattr(mob, "inventory") or getattr(mob, "inventory", None) is None:
            mob.inventory = []
        mob.inventory.append(item)

    @staticmethod
    def equip_item(mob: Mobile, item, wear_loc: int):
        MobileUtil.add_inventory_item(mob, item)
        if not hasattr(mob, "equipped") or getattr(mob, "equipped", None) is None:
            mob.equipped = Equipped()

        slot = WEAR_LOC_TO_EQUIPPED_SLOT.get(int(wear_loc))
        if slot and hasattr(mob.equipped, slot):
            setattr(mob.equipped, slot, item)
        item.wear_loc = int(wear_loc)
