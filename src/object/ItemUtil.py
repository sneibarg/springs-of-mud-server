from object.ExtraDescriptionData import ExtraDescriptionData
from server.LoggerFactory import LoggerFactory
from enum import IntEnum
from object.Item import Item
from object.AffectData import AffectData, AffectWhere


logger = LoggerFactory.get_logger('ItemUtil')


class ItemUtil:
    pass

    @staticmethod
    def normalize_item_data(object_macros, item_data, liquids, skill_registry) -> Item:
        ItemUtil.convert_extra_and_wear_flags(item_data)
        ItemUtil.normalize_value_fields(item_data, object_macros.ItemTypes)
        ItemUtil.update_item_type(item_data, object_macros.DamageTypes, object_macros.ItemTypes, liquids, skill_registry)
        ItemUtil.update_condition(item_data)

        item = Item.from_json(item_data)
        if len(item.affect_data) > 0:
            item.effects = []
            ItemUtil.update_affect_data(item)

        ItemUtil.update_extra_descr(item)
        return item

    @staticmethod
    def update_affect_data(item):
        from server.ServerUtil import ServerUtil
        for affect in item.affect_data:
            affect_elements = affect.split(",")
            affect_data = AffectData(valid=True, where=-1, type=-1, level=item.level, duration=-1, location=-1, modifier=-1, bitvector=-1)
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
                    affect_data.bitvector = ServerUtil.convert_flags(bitvector_raw)

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
        from server.ServerUtil import ServerUtil
        for flag_field in ['extra_flags', 'wear_flags']:
            flag_value = item_data.get(flag_field, "0")
            if isinstance(flag_value, int) or (isinstance(flag_value, str) and flag_value.lstrip('-').isdigit()):
                continue

            item_data[flag_field] = str(ServerUtil.convert_flags(flag_value))

    @staticmethod
    def convert_numeric_to_string(value):
        if isinstance(value, int):
            return str(value)
        if isinstance(value, str):
            if value.lstrip('-').isdigit():
                return value
        return str(value) if value else '0'

    @staticmethod
    def read_flag(flag_value):
        if isinstance(flag_value, int):
            return str(flag_value)

        flag_str = str(flag_value).strip()
        if not flag_str or flag_str.lstrip('-').isdigit():
            return flag_str if flag_str else '0'

        from server.ServerUtil import ServerUtil
        return str(ServerUtil.convert_flags(flag_str))

    # Matches load_objects() logic from ROM db2.c:341-389
    @staticmethod
    def normalize_value_fields(item_data, ItemTypes: type[IntEnum]):
        item_type = item_data.get("itemType", "").strip().lower()
        if item_type == ItemTypes.ITEM_WEAPON.name:
            item_data['value1'] = ItemUtil.convert_numeric_to_string(item_data.get('value1', '0'))
            item_data['value2'] = ItemUtil.convert_numeric_to_string(item_data.get('value2', '0'))
            item_data['value4'] = ItemUtil.read_flag(item_data.get('value4', '0'))
        elif item_type == ItemTypes.ITEM_WEAPON.name:
            item_data['value0'] = ItemUtil.convert_numeric_to_string(item_data.get('value0', '0'))
            item_data['value1'] = ItemUtil.read_flag(item_data.get('value1', '0'))
            item_data['value2'] = ItemUtil.convert_numeric_to_string(item_data.get('value2', '0'))
            item_data['value3'] = ItemUtil.convert_numeric_to_string(item_data.get('value3', '0'))
            item_data['value4'] = ItemUtil.convert_numeric_to_string(item_data.get('value4', '0'))
        elif item_type in [ItemTypes.ITEM_DRINK_CON.name, ItemTypes.ITEM_FOUNTAIN.name]:
            item_data['value0'] = ItemUtil.convert_numeric_to_string(item_data.get('value0', '0'))
            item_data['value1'] = ItemUtil.convert_numeric_to_string(item_data.get('value1', '0'))
            item_data['value3'] = ItemUtil.convert_numeric_to_string(item_data.get('value3', '0'))
            item_data['value4'] = ItemUtil.convert_numeric_to_string(item_data.get('value4', '0'))
        elif item_type in [ItemTypes.ITEM_WAND.name, ItemTypes.ITEM_STAFF.name]:
            item_data['value0'] = ItemUtil.convert_numeric_to_string(item_data.get('value0', '0'))
            item_data['value1'] = ItemUtil.convert_numeric_to_string(item_data.get('value1', '0'))
            item_data['value2'] = ItemUtil.convert_numeric_to_string(item_data.get('value2', '0'))
            item_data['value4'] = ItemUtil.convert_numeric_to_string(item_data.get('value4', '0'))
        elif item_type in [ItemTypes.ITEM_POTION.name, ItemTypes.ITEM_PILL.name, ItemTypes.ITEM_SCROLL.name]:
            item_data['value0'] = ItemUtil.convert_numeric_to_string(item_data.get('value0', '0'))
        else:
            for i in range(5):
                value_key = f'value{i}'
                item_data[value_key] = ItemUtil.read_flag(item_data.get(value_key, '0'))

    @staticmethod
    def update_item_type(item_data, DamageTypes: type[IntEnum], ItemTypes: type[IntEnum], liquids, skill_registry):
        item_type = item_data.get("itemType", "").strip().lower()
        if item_type == ItemTypes.ITEM_WEAPON.name:
            ItemUtil.attack_type(DamageTypes, item_data)
        elif item_type == ItemTypes.ITEM_FOUNTAIN.name:
            ItemUtil.update_fountain(liquids, item_data)
        elif item_type == ItemTypes.ITEM_STAFF.name:
            ItemUtil.update_staff(skill_registry, item_data)
        elif item_type == ItemTypes.ITEM_SCROLL.name:
            ItemUtil.update_scroll(skill_registry, item_data)

    @staticmethod
    def update_fountain(liquids, item_data):
        ItemUtil.liq_lookup(liquids, item_data)

    @staticmethod
    def update_staff(skill_registry, item_data):
        try:
            skill_name = item_data['value3']
            skill = skill_registry.get_skill_by_name(skill_name)
            item_data['value3'] = str(skill)
        except Exception as e:
            print(f"Failed to update staff skill: {e}")

    @staticmethod
    def update_scroll(skill_registry, item_data):
        for skill_key in ['value1', 'value2', 'value3', 'value4']:
            try:
                skill_name = item_data[skill_key]
                if skill_name != "":
                    skill = skill_registry.get_skill_by_name(skill_name)
                    item_data[skill_key] = str(skill)
            except Exception as e:
                print(f"Failed to update scroll skill: {e}")

    # even if it's slower, it still loads all in the same second
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
            logger.warn(f"Unknown damage type: {damage_type} for item {item_data}")
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

    @staticmethod
    def update_extra_descr(item):
        if len(item.extra_descr) > 0:
            item.extra_description = ExtraDescriptionData(valid=True, keyword=item.extra_descr[0], description=item.extra_descr[1])
            