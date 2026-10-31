"""Build item prototypes and construct independent runtime instances."""
from api.ItemApi import ItemApi
from server.LoggerFactory import LoggerFactory
from item.Effect import Effect, AffectWhere
from item.ItemRegistry import ItemRegistry
from api.GameApi import GameApi
from enum import IntEnum
from copy import deepcopy
from dataclasses import asdict, fields

from item.Item import Item
from util.GenericUtil import GenericUtil


class ItemFactory:
    @staticmethod
    def from_data(item_data, liquids, skill_registry) -> Item:
        """Build a content-service prototype, preserving its identity and values."""

        ItemFactory.convert_extra_and_wear_flags(item_data)
        item_types = ItemApi.get_enum("itemTypes")
        damage_types = ItemApi.get_enum("damageTypes")
        ItemFactory.normalize_value_fields(item_data, item_types)
        ItemFactory.update_item_type(item_data, damage_types, item_types, liquids, skill_registry)
        ItemFactory.update_condition(item_data)

        item = Item.from_json(item_data)
        if len(item.affect_data) > 0:
            item.effects = []
            ItemFactory.update_affect_data(item)
        return item

    @staticmethod
    def create(prototype: Item) -> Item:
        """Spawn an empty item with a fresh identity and independent content state."""
        if prototype is None:
            raise ValueError("Cannot create item from None index")

        data = {field.name: deepcopy(getattr(prototype, field.name))
                for field in fields(prototype) if field.name not in ("contains", "room_data")}
        if data.get("extra_description") is not None:
            data["extra_description"] = asdict(data["extra_description"])
        data["room_data"] = {}
        data["id"] = GenericUtil.generate_mongo_id()
        data["contains"] = []
        data["enchanted"] = False

        item = Item.from_json(data)

        item_type = (getattr(item, "item_type", "") or "").strip().lower()
        if "light" in item_type and str(getattr(item, "value2", None)) == "999":
            item.value2 = "-1"
        elif "jukebox" in item_type:
            for v in ("value0", "value1", "value2", "value3", "value4"):
                setattr(item, v, "-1")

        return item

    @staticmethod
    def copy_instance(obj: Item, item_filter=None) -> Item:
        """Copy state with fresh identities, optionally filtering each contained item."""
        clone = ItemFactory.create(obj)
        clone.description = getattr(obj, "description", "")
        for field_name in ("value0", "value1", "value2", "value3", "value4"):
            setattr(clone, field_name, getattr(obj, field_name, "0"))
        clone.enchanted = bool(getattr(obj, "enchanted", False))
        clone.extra_descr = list(getattr(obj, "extra_descr", []) or [])
        if len(clone.extra_descr) >= 2:
            Item.update_extra_description(clone)
        effects = getattr(obj, "effects", None)
        clone.effects = deepcopy(effects) if effects is not None else None
        clone.contains = [ItemFactory.copy_instance(item, item_filter=item_filter)
                          for item in list(getattr(obj, "contains", []) or [])
                          if item_filter is None or item_filter(item)]
        return clone

    @staticmethod
    def create_money(gold: int, silver: int, item_registry: ItemRegistry, WellKnownObjEnums: type[IntEnum]) -> Item:
        if gold < 0 or silver < 0 or (gold == 0 and silver == 0):
            gold = max(1, gold)
            silver = max(1, silver)

        if gold == 0 and silver == 1:
            money = ItemFactory.create(item_registry.get(vnum=str(WellKnownObjEnums.OBJ_VNUM_SILVER_ONE.value)))
        elif gold == 1 and silver == 0:
            money = ItemFactory.create(item_registry.get(vnum=str(WellKnownObjEnums.OBJ_VNUM_GOLD_ONE.value)))
        elif silver == 0:
            money = ItemFactory.create(item_registry.get(vnum=str(WellKnownObjEnums.OBJ_VNUM_GOLD_SOME.value)))
            money.value1 = str(gold)
            money.cost = gold
            money.short_description = money.short_description.replace("%d", str(gold))
            money.weight = gold // 5
        elif gold == 0:
            money = ItemFactory.create(item_registry.get(vnum=str(WellKnownObjEnums.OBJ_VNUM_SILVER_SOME.value)))
            money.value0 = str(silver)
            money.cost = silver
            money.short_description = money.short_description.replace("%d", str(silver))
            money.weight = silver // 20
        else:
            money = ItemFactory.create(item_registry.get(vnum=str(WellKnownObjEnums.OBJ_VNUM_COINS.value)))
            money.value0 = str(silver)
            money.value1 = str(gold)
            money.cost = 100 * gold + silver
            money.weight = gold // 5 + silver // 20
            money.short_description = money.short_description % (silver, gold)
        return money

    @staticmethod
    def update_affect_data(item):
        for affect in item.affect_data:
            affect_elements = affect.split(",")
            affect_data = Effect(valid=True, where=AffectWhere.TO_OBJECT.value, type=-1,
                                 level=item.level, duration=-1, location=0, modifier=0, bitvector=0)
            if affect_elements[0] == "A":
                affect_data.where = AffectWhere.TO_OBJECT.value
                affect_data.location = affect_elements[1]
                affect_data.modifier = affect_elements[2]
            elif affect_elements[0] == "F":
                affect_data.location = affect_elements[2]
                affect_data.modifier = affect_elements[3]

                bitvector_raw = affect_elements[4]
                if bitvector_raw.isdigit() or (bitvector_raw.startswith('-') and bitvector_raw[1:].isdigit()):
                    affect_data.bitvector = bitvector_raw
                else:
                    affect_data.bitvector = GameApi.convert_flags(bitvector_raw)

                if affect_elements[1] == "A":
                    affect_data.where = AffectWhere.TO_AFFECTS.value
                elif affect_elements[1] == "I":
                    affect_data.where = AffectWhere.TO_IMMUNE.value
                elif affect_elements[1] == "R":
                    affect_data.where = AffectWhere.TO_RESIST.value
                elif affect_elements[1] == "V":
                    affect_data.where = AffectWhere.TO_VULN.value

            item.effects.append(affect_data)

    @staticmethod
    def convert_extra_and_wear_flags(item_data):
        """
        Each letter represents a bit: A = 1<<0 = 1, B = 1<<1 = 2, etc.
        Multiple letters are OR'd together: "AN" = (1<<0) | (1<<13) = 1 | 8192 = 8193
        """
        for flag_field in ['extra_flags', 'wear_flags']:
            flag_value = item_data.get(flag_field, "0")
            if isinstance(flag_value, int) or (isinstance(flag_value, str) and flag_value.lstrip('-').isdigit()):
                continue

            item_data[flag_field] = str(GameApi.convert_flags(flag_value))

    @staticmethod
    def read_flag(flag_value):
        if isinstance(flag_value, int):
            return str(flag_value)

        flag_str = str(flag_value).strip()
        if not flag_str or flag_str.lstrip('-').isdigit():
            return flag_str if flag_str else '0'

        return str(GameApi.convert_flags(flag_str))

    @staticmethod
    def normalize_value_fields(item_data, ItemTypes: type[IntEnum]):
        item_type = item_data.get("itemType", "").strip().lower()
        if ItemFactory._matches_item_type(item_type, "ITEM_WEAPON"):
            item_data['value1'] = GenericUtil.convert_numeric_to_string(item_data.get('value1', '0'))
            item_data['value2'] = GenericUtil.convert_numeric_to_string(item_data.get('value2', '0'))
            item_data['value4'] = ItemFactory.read_flag(item_data.get('value4', '0'))
        elif ItemFactory._matches_item_type(item_type, "ITEM_CONTAINER"):
            item_data['value0'] = GenericUtil.convert_numeric_to_string(item_data.get('value0', '0'))
            item_data['value1'] = ItemFactory.read_flag(item_data.get('value1', '0'))
            item_data['value2'] = GenericUtil.convert_numeric_to_string(item_data.get('value2', '0'))
            item_data['value3'] = GenericUtil.convert_numeric_to_string(item_data.get('value3', '0'))
            item_data['value4'] = GenericUtil.convert_numeric_to_string(item_data.get('value4', '0'))
        elif ItemFactory._matches_item_type(item_type, "ITEM_DRINK_CON", "ITEM_FOUNTAIN"):
            item_data['value0'] = GenericUtil.convert_numeric_to_string(item_data.get('value0', '0'))
            item_data['value1'] = GenericUtil.convert_numeric_to_string(item_data.get('value1', '0'))
            item_data['value3'] = GenericUtil.convert_numeric_to_string(item_data.get('value3', '0'))
            item_data['value4'] = GenericUtil.convert_numeric_to_string(item_data.get('value4', '0'))
        elif ItemFactory._matches_item_type(item_type, "ITEM_WAND", "ITEM_STAFF"):
            item_data['value0'] = GenericUtil.convert_numeric_to_string(item_data.get('value0', '0'))
            item_data['value1'] = GenericUtil.convert_numeric_to_string(item_data.get('value1', '0'))
            item_data['value2'] = GenericUtil.convert_numeric_to_string(item_data.get('value2', '0'))
            item_data['value4'] = GenericUtil.convert_numeric_to_string(item_data.get('value4', '0'))
        elif ItemFactory._matches_item_type(item_type, "ITEM_POTION", "ITEM_PILL", "ITEM_SCROLL"):
            item_data['value0'] = GenericUtil.convert_numeric_to_string(item_data.get('value0', '0'))
        else:
            for i in range(5):
                value_key = f'value{i}'
                item_data[value_key] = ItemFactory.read_flag(item_data.get(value_key, '0'))

    @staticmethod
    def update_item_type(item_data, DamageTypes: type[IntEnum], ItemTypes: type[IntEnum], liquids, skill_registry):
        item_type = item_data.get("itemType", "").strip().lower()
        if ItemFactory._matches_item_type(item_type, "ITEM_WEAPON"):
            ItemFactory.attack_type(DamageTypes, item_data)
        elif ItemFactory._matches_item_type(item_type, "ITEM_DRINK_CON", "ITEM_FOUNTAIN"):
            ItemFactory.liq_lookup(liquids, item_data)
        elif ItemFactory._matches_item_type(item_type, "ITEM_STAFF"):
            ItemFactory.update_staff(skill_registry, item_data)
        elif ItemFactory._matches_item_type(item_type, "ITEM_SCROLL"):
            ItemFactory.update_scroll(skill_registry, item_data)

    @staticmethod
    def _matches_item_type(raw_item_type: str, *enum_names: str) -> bool:
        item_type = str(raw_item_type or "").strip().lower()
        if not item_type:
            return False

        aliases = {name.strip().lower() for name in enum_names if name}
        try:
            item_table = ItemApi.item_table_map()
        except RuntimeError:
            item_table = {}

        for alias, config in item_table.items():
            mapped_type = str((config or {}).get("type", "")).strip().upper()
            if mapped_type in enum_names:
                aliases.add(str(alias or "").strip().lower())

        return item_type in aliases

    @staticmethod
    def update_staff(skill_registry, item_data):
        try:
            skill_name = item_data['value3']
            skill = ItemFactory.resolve_item_skill(skill_registry, skill_name)
            item_data['value3'] = skill
        except Exception as e:
            LoggerFactory.get_logger("ItemFactory").warning(f"Failed to update staff skill: {e}; vnum={item_data['vnum']}")

    @staticmethod
    def update_scroll(skill_registry, item_data):
        for skill_key in ['value1', 'value2', 'value3', 'value4']:
            try:
                skill_name = item_data[skill_key]
                if skill_name != "":
                    skill = ItemFactory.resolve_item_skill(skill_registry, skill_name)
                    item_data[skill_key] = skill
            except Exception as e:
                LoggerFactory.get_logger("ItemFactory").warning(f"Failed to update scroll skill: {e}; vnum={item_data['vnum']}")

    @staticmethod
    def resolve_item_skill(skill_registry, skill_name):
        candidates: list[str] = []
        primary = str(skill_name or "").strip()
        if primary:
            candidates.append(primary)
            trimmed = primary.rstrip(". ").strip()
            if trimmed and trimmed not in candidates:
                candidates.append(trimmed)

        registries = skill_registry if isinstance(skill_registry, (list, tuple)) else [skill_registry]
        last_error = None
        for candidate in candidates:
            for registry in registries:
                if registry is None or not hasattr(registry, "get"):
                    continue
                try:
                    return registry.get(name=candidate)
                except Exception as exc:
                    last_error = exc

        if last_error is not None:
            raise last_error
        raise LookupError(f"No item skill registered with name={primary}")

    @staticmethod
    def attack_type(damage_types, item_data):
        damage_type = item_data['value3']
        if damage_type in ['blast', 'pound', 'crush', 'suction', 'beating', 'charge', 'slap', 'punch', 'peckb', 'smash', 'thwack']:
            item_data['damage_type'] = damage_types.DAM_BASH.value
        elif damage_type in ['slash', 'whip', 'claw', 'grep', 'cleave', 'chop', 'slice']:
            item_data['damage_type'] = damage_types.DAM_SLASH.value
        elif damage_type in ['pierce', 'stab', 'bite', 'scratch', 'sting', 'chomp', 'thrust']:
            item_data['damage_type'] = damage_types.DAM_PIERCE.value
        elif damage_type in ['digestion', 'acbite', 'slime']:
            item_data['damage_type'] = damage_types.DAM_ACID.value
        elif damage_type in ['flame', 'flbite']:
            item_data['damage_type'] = damage_types.DAM_FIRE.value
        elif damage_type in ['frbite', 'chill']:
            item_data['damage_type'] = damage_types.DAM_COLD.value
        elif damage_type in ['shbite', 'shock']:
            item_data['damage_type'] = damage_types.DAM_LIGHTNING.value
        elif damage_type in ['wrath', 'magic']:
            item_data['damage_type'] = damage_types.DAM_ENERGY.value
        elif damage_type in ['divine']:
            item_data['damage_type'] = damage_types.DAM_HOLY.value
        elif damage_type in ['drain']:
            item_data['damage_type'] = damage_types.DAM_NEGATIVE.value
        else:
            LoggerFactory.get_logger("ItemFactory").warning(f"Unknown damage type: {damage_type} for item {item_data}")
            item_data['damage_type'] = damage_types.DAM_NONE.value

    @staticmethod
    def liq_lookup(liquids, item_data):
        liquid_name = item_data['value2'].replace("'", "")
        liquid = liquids[liquid_name]
        liquid_affect_data = liquid['affect']
        liquid_color = liquid['color']
        item_data['liquid_affect_data'] = liquid_affect_data
        item_data['liquid_color'] = liquid_color

    @staticmethod
    def update_condition(item_data):
        condition = item_data["condition"]
        if condition == "P":
            item_data["condition"] = "100"
        elif condition == "G":
            item_data["condition"] = "90"
        elif condition == "A":
            item_data["condition"] = "75"
        elif condition == "W":
            item_data["condition"] = "50"
        elif condition == "D":
            item_data["condition"] = "25"
        elif condition == "B":
            item_data["condition"] = "10"
        elif condition == "R":
            item_data["condition"] = "0"
        else:
            item_data["condition"] = "100"
