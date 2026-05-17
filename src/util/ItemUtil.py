from enum import IntEnum
from typing import Any, TYPE_CHECKING

from api.GameApi import GameApi
from game.RandomNumberGenerator import RandomNumberGenerator
from item.ItemRegistry import ItemRegistry
from util.GenericUtil import GenericUtil
from item.ExtraDescriptionData import ExtraDescriptionData
from api.ItemApi import ItemApi
from player.Character import Character
from api.CharacterApi import CharacterApi
from server.LoggerFactory import LoggerFactory
from item.Item import Item
from item.Effect import Effect, AffectWhere
from game.Equipped import Equipped, WEAR_SLOT_ORDER
from util.InterpUtil import InterpUtil

if TYPE_CHECKING:
    from area.Room import Room

rng = RandomNumberGenerator()
logger = LoggerFactory.get_logger('ItemUtil')


class ItemUtil:
    WEAR_SLOT_ORDER = WEAR_SLOT_ORDER

    @staticmethod
    def create_money(gold: int, silver: int, item_registry: ItemRegistry, WellKnownObjEnums: IntEnum) -> Item:
        if gold < 0 or silver < 0 or (gold == 0 and silver == 0):
            gold = max(1, gold)
            silver = max(1, silver)

        if gold == 0 and silver == 1:
            money = ItemUtil.create_object(item_registry.get(vnum=WellKnownObjEnums.OBJ_VNUM_SILVER_ONE.value))
        elif gold == 1 and silver == 0:
            money = ItemUtil.create_object(item_registry.get(vnum=WellKnownObjEnums.OBJ_VNUM_GOLD_ONE.value))
        elif silver == 0:
            money = ItemUtil.create_object(item_registry.get(vnum=WellKnownObjEnums.OBJ_VNUM_GOLD_SOME.value))
            money.value1 = str(gold)
            money.cost = gold
            money.short_description = money.short_description.replace("%d", str(gold))
            money.weight = gold / 5
        elif gold == 0:
            money = ItemUtil.create_object(item_registry.get(vnum=WellKnownObjEnums.OBJ_VNUM_SILVER_SOME.value))
            money.value0 = str(silver)
            money.cost = silver
            money.short_description = money.short_description.replace("%d", str(silver))
            money.weight = silver / 20
        else:
            money = ItemUtil.create_object(item_registry.get(vnum=WellKnownObjEnums.OBJ_VNUM_COINS.value))
            money.value0 = str(gold)
            money.value1 = str(silver)
            money.cost = 100 * gold + silver
            money.weight = gold / 5 + silver / 20
            money.short_description = money.short_description % (silver, gold)
        return money

    @staticmethod
    def normalize_item_data(item_data, liquids, skill_registry) -> Item:
        ItemUtil.convert_extra_and_wear_flags(item_data)
        item_types = ItemApi.get_enum("itemTypes")
        damage_types = ItemApi.get_enum("damageTypes")
        ItemUtil.normalize_value_fields(item_data, item_types)
        ItemUtil.update_item_type(item_data, damage_types, item_types, liquids, skill_registry)
        ItemUtil.update_condition(item_data)

        item = Item.from_json(item_data)
        if len(item.affect_data) > 0:
            item.effects = []
            ItemUtil.update_affect_data(item)

        ItemUtil.update_extra_descr(item)
        return item

    @staticmethod
    def update_affect_data(item):
        for affect in item.affect_data:
            affect_elements = affect.split(",")
            affect_data = Effect(valid=True, where=-1, type=-1, level=item.level, duration=-1, location=-1, modifier=-1, bitvector=-1)
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
        if ItemUtil._matches_item_type(item_type, "ITEM_WEAPON"):
            item_data['value1'] = GenericUtil.convert_numeric_to_string(item_data.get('value1', '0'))
            item_data['value2'] = GenericUtil.convert_numeric_to_string(item_data.get('value2', '0'))
            item_data['value4'] = ItemUtil.read_flag(item_data.get('value4', '0'))
        elif ItemUtil._matches_item_type(item_type, "ITEM_CONTAINER"):
            item_data['value0'] = GenericUtil.convert_numeric_to_string(item_data.get('value0', '0'))
            item_data['value1'] = ItemUtil.read_flag(item_data.get('value1', '0'))
            item_data['value2'] = GenericUtil.convert_numeric_to_string(item_data.get('value2', '0'))
            item_data['value3'] = GenericUtil.convert_numeric_to_string(item_data.get('value3', '0'))
            item_data['value4'] = GenericUtil.convert_numeric_to_string(item_data.get('value4', '0'))
        elif ItemUtil._matches_item_type(item_type, "ITEM_DRINK_CON", "ITEM_FOUNTAIN"):
            item_data['value0'] = GenericUtil.convert_numeric_to_string(item_data.get('value0', '0'))
            item_data['value1'] = GenericUtil.convert_numeric_to_string(item_data.get('value1', '0'))
            item_data['value3'] = GenericUtil.convert_numeric_to_string(item_data.get('value3', '0'))
            item_data['value4'] = GenericUtil.convert_numeric_to_string(item_data.get('value4', '0'))
        elif ItemUtil._matches_item_type(item_type, "ITEM_WAND", "ITEM_STAFF"):
            item_data['value0'] = GenericUtil.convert_numeric_to_string(item_data.get('value0', '0'))
            item_data['value1'] = GenericUtil.convert_numeric_to_string(item_data.get('value1', '0'))
            item_data['value2'] = GenericUtil.convert_numeric_to_string(item_data.get('value2', '0'))
            item_data['value4'] = GenericUtil.convert_numeric_to_string(item_data.get('value4', '0'))
        elif ItemUtil._matches_item_type(item_type, "ITEM_POTION", "ITEM_PILL", "ITEM_SCROLL"):
            item_data['value0'] = GenericUtil.convert_numeric_to_string(item_data.get('value0', '0'))
        else:
            for i in range(5):
                value_key = f'value{i}'
                item_data[value_key] = ItemUtil.read_flag(item_data.get(value_key, '0'))

    @staticmethod
    def update_item_type(item_data, DamageTypes: type[IntEnum], ItemTypes: type[IntEnum], liquids, skill_registry):
        item_type = item_data.get("itemType", "").strip().lower()
        if ItemUtil._matches_item_type(item_type, "ITEM_WEAPON"):
            ItemUtil.attack_type(DamageTypes, item_data)
        elif ItemUtil._matches_item_type(item_type, "ITEM_DRINK_CON", "ITEM_FOUNTAIN"):
            ItemUtil.update_fountain(liquids, item_data)
        elif ItemUtil._matches_item_type(item_type, "ITEM_STAFF"):
            ItemUtil.update_staff(skill_registry, item_data)
        elif ItemUtil._matches_item_type(item_type, "ITEM_SCROLL"):
            ItemUtil.update_scroll(skill_registry, item_data)

    @staticmethod
    def _matches_item_type(raw_item_type: str, *enum_names: str) -> bool:
        item_type = str(raw_item_type or "").strip().lower()
        if not item_type:
            return False

        aliases = {name.strip().lower() for name in enum_names if name}
        try:
            item_table = ItemApi._item_table_map()
        except RuntimeError:
            item_table = {}

        for alias, config in item_table.items():
            mapped_type = str((config or {}).get("type", "")).strip().upper()
            if mapped_type in enum_names:
                aliases.add(str(alias or "").strip().lower())

        return item_type in aliases

    @staticmethod
    def update_fountain(liquids, item_data):
        ItemUtil.liq_lookup(liquids, item_data)

    @staticmethod
    def update_staff(skill_registry, item_data):
        try:
            skill_name = item_data['value3']
            skill = skill_registry.get(name=skill_name)
            item_data['value3'] = str(skill)
        except Exception as e:
            logger.warning(f"Failed to update staff skill: {e}")

    @staticmethod
    def update_scroll(skill_registry, item_data):
        for skill_key in ['value1', 'value2', 'value3', 'value4']:
            try:
                skill_name = item_data[skill_key]
                if skill_name != "":
                    skill = skill_registry.get(name=skill_name)
                    item_data[skill_key] = str(skill)
            except Exception as e:
                logger.warning(f"Failed to update scroll skill: {e}")

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

    @staticmethod
    def container_volume_description(obj: Item):
        try:
            cap = max(0, int(obj.value0))
            cur = max(0, int(obj.value1))
        except (TypeError, ValueError):
            cap = 0
            cur = 0

        if cur <= 0:
            text = "It is empty.\r\n"
        else:
            if cap <= 0:
                fill = "partly "
            elif cur < cap / 4:
                fill = "less than half-"
            elif cur < (3 * cap) / 4:
                fill = "about half-"
            else:
                fill = "more than half-"
            color = getattr(obj, "liquid_color", None) or "unknown"
            text = f"It's {fill}filled with a {color} liquid.\r\n"
        return text

    @staticmethod
    def items_in_container(obj: Item) -> str:
        text = f"{obj.name} holds\r\n"
        contents = obj.contents()
        if contents:
            text = text + contents
        else:
            text = text + f"\tNothing.\r\n"
        return text

    @staticmethod
    def is_drink_container(item) -> bool:
        t = (item.item_type or "").strip().lower()
        return ("drink" in t) or ("fountain" in t)

    @staticmethod
    def is_fountain(item) -> bool:
        t = (getattr(item, "item_type", "") or "").strip().lower()
        return "fountain" in t

    @staticmethod
    def is_edible(item) -> bool:
        t = (getattr(item, "item_type", "") or "").strip().lower()
        return ("food" in t) or ("pill" in t)

    @staticmethod
    def is_container_like(item) -> bool:
        t = (item.item_type or "").strip().lower()
        return ("container" in t) or ("corpse" in t)

    @staticmethod
    def find_item(character: Character, room: Room, name: str):
        wanted = (name or "").strip().lower()
        if not wanted:
            return None
        for item in character.get_items():
            nm = (item.name or "").lower()
            if nm == wanted or nm.startswith(wanted):
                return item
        for item in room.contents.values():
            nm = (item.name or "").lower()
            if nm == wanted or nm.startswith(wanted):
                return item
        return None

    @staticmethod
    def room_items(room: Room) -> list:
        lines = []
        for item in room.contents.values():
            raw_long = item.long_description or ""
            line = raw_long.rstrip("\r\n")
            if not raw_long.strip():
                line = item.short_description or item.name
            if line:
                line = f"    {line}"
                lines.append(line)
        return lines

    @staticmethod
    def _is_item_flag_set(obj: Item, flag_value: int) -> bool:
        try:
            flags = int(getattr(obj, "extra_flags", 0) or 0)
        except (TypeError, ValueError):
            try:
                flags = GameApi.convert_flags(str(getattr(obj, "extra_flags", "0") or "0"))
            except Exception:
                flags = 0
        return (flags & int(flag_value)) != 0

    @staticmethod
    def format_obj_to_char(obj: Item, item_flags_enum=None, f_short: bool = True) -> str:
        if obj is None:
            return ""

        labels = []
        if item_flags_enum is not None:
            if hasattr(item_flags_enum, "ITEM_INVIS") and ItemUtil._is_item_flag_set(obj, item_flags_enum.ITEM_INVIS.value):
                labels.append("(Invis)")
            if hasattr(item_flags_enum, "ITEM_GLOW") and ItemUtil._is_item_flag_set(obj, item_flags_enum.ITEM_GLOW.value):
                labels.append("(Glowing)")
            if hasattr(item_flags_enum, "ITEM_HUM") and ItemUtil._is_item_flag_set(obj, item_flags_enum.ITEM_HUM.value):
                labels.append("(Humming)")

        base = (obj.short_description if f_short else obj.long_description) or obj.name or "something"
        prefix = (" ".join(labels) + " ") if labels else ""
        return prefix + base

    @staticmethod
    def create_object(pObjIndex: Item):
        if pObjIndex is None:
            logger.error("create_object: NULL pObjIndex.")
            raise ValueError("Cannot create item from None index")

        extra_descr = list(getattr(pObjIndex, "extra_descr", []) or [])
        affect_data = list(getattr(pObjIndex, "affect_data", []) or [])
        item = Item.from_json(
            {
                "id": GenericUtil.generate_mongo_id(),
                "area_id": pObjIndex.area_id,
                "vnum": pObjIndex.vnum,
                "name": pObjIndex.name,
                "short_description": pObjIndex.short_description,
                "long_description": pObjIndex.long_description,
                "item_type": pObjIndex.item_type,
                "material": pObjIndex.material,
                "extra_flags": pObjIndex.extra_flags,
                "wear_flags": pObjIndex.wear_flags,
                "value0": pObjIndex.value0,
                "value1": pObjIndex.value1,
                "value2": pObjIndex.value2,
                "value3": pObjIndex.value3,
                "value4": pObjIndex.value4,
                "weight": pObjIndex.weight,
                "condition": pObjIndex.condition,
                "affect_data": affect_data,
                "extra_descr": extra_descr,
                "contains": [],
                "level": pObjIndex.level,
                "cost": pObjIndex.cost,
            }
        )
        item.enchanted = False
        ItemUtil.update_extra_descr(item)

        item_type = (item.item_type or "").strip().lower()
        if "light" in item_type and str(item.value2) == "999":
            item.value2 = "-1"
        elif "jukebox" in item_type:
            item.value0 = "-1"
            item.value1 = "-1"
            item.value2 = "-1"
            item.value3 = "-1"
            item.value4 = "-1"

        return item

    @staticmethod
    def find_world_object_instance(room_registry, target_vnum: str):
        def _walk(items, in_room: bool):
            for obj in items:
                if str(getattr(obj, "vnum", "")) == target_vnum:
                    return obj, in_room
                found_obj, found_in_room = _walk(getattr(obj, "contains", []) or [], False)
                if found_obj is not None:
                    return found_obj, found_in_room
            return None, False

        for room_id in room_registry.all_rooms():
            room = room_registry.get_or_none(id=room_id)
            if room is None:
                continue
            obj, in_room = _walk(room.contents.values(), True)
            if obj is not None:
                return obj, in_room
        return None, False

    @staticmethod
    def count_obj_list(target_vnum: str, items: list) -> int:
        count = 0
        for obj in items or []:
            if str(getattr(obj, "vnum", "")) == target_vnum:
                count += 1
        return count

    @staticmethod
    def can_see_object(room: Room, character: Character, obj: Item) -> bool:
        ItemFlags = CharacterApi.get_enum('itemFlags')
        ItemTypes = CharacterApi.get_enum('itemTypes')
        AffectBits = CharacterApi.get_enum('affectedBy')
        PlayerActBits = CharacterApi.get_enum('playerActBits')
        if not CharacterApi.is_npc(character) and CharacterApi.is_set(character.status_flags.act, PlayerActBits.PLR_HOLYLIGHT.value):
            return True

        if CharacterApi.is_set(GameApi.convert_flags(obj.extra_flags), ItemFlags.ITEM_VIS_DEATH.value):
            return False

        if CharacterApi.is_affected(character, AffectBits.AFF_BLIND.value) and obj.item_type != ItemTypes.ITEM_POTION.value:
            return False

        if obj.item_type == ItemTypes.ITEM_LIGHT.value and int(obj.value2) != 0:
            return True

        if CharacterApi.is_set(GameApi.convert_flags(obj.extra_flags), ItemFlags.ITEM_INVIS.value and not CharacterApi.is_affected(character, AffectBits.AFF_DETECT_INVIS.value)):
            return False

        if CharacterApi.is_set(GameApi.convert_flags(obj.extra_flags), ItemFlags.ITEM_GLOW.value):
            return True

        if room.is_room_dark() and not CharacterApi.is_affected(character, AffectBits.AFF_DARK_VISION.value):
            return False

        return True

    @staticmethod
    def parse_raw_arguments(raw_result, parameters) -> tuple[str, str]:
        text = (raw_result if isinstance(raw_result, str) else "").strip()
        if not text:
            text = " ".join(parameters or []).strip()
        a1, rest = InterpUtil.one_argument(text)
        a2, rest2 = InterpUtil.one_argument(rest)
        if a2 in ("from", "in", "on"):
            a2, rest2 = InterpUtil.one_argument(rest2)
        return a1, f"{a2} {rest2}".strip()

    @staticmethod
    def has_flag(raw_flags, bit_value: int) -> bool:
        return (GameApi.flags_to_int(raw_flags) & int(bit_value)) != 0

    @staticmethod
    def ensure_equipped(character):
        if hasattr(character, "ensure_equipped"):
            return character.ensure_equipped()
        return Equipped.ensure_on(character)

    @staticmethod
    def find_inventory_item(character, wanted: str):
        if hasattr(character, "find_inventory_item"):
            return character.find_inventory_item(wanted)
        q = (wanted or "").strip().lower()
        if not q:
            return None
        for item in list(getattr(character, "loot", []) or []):
            name = (getattr(item, "name", "") or "").lower()
            if name == q or name.startswith(q):
                return item
        return None

    @staticmethod
    def find_room_item(room, wanted: str):
        if room is None:
            return None
        q = (wanted or "").strip().lower()
        if not q:
            return None
        for item in room.contents.values():
            name = (getattr(item, "name", "") or "").lower()
            if name == q or name.startswith(q):
                return item
        return None

    @staticmethod
    def find_container(character, room, wanted: str):
        return ItemUtil.find_inventory_item(character, wanted) or ItemUtil.find_room_item(room, wanted)

    @staticmethod
    def remove_from_inventory(character, item):
        if hasattr(character, "remove_item"):
            character.remove_item(item)
            return
        loot = getattr(character, "loot", None)
        if loot is None:
            return
        try:
            loot.remove(item)
        except ValueError:
            pass

    @staticmethod
    def add_to_inventory(character, item):
        if hasattr(character, "add_item"):
            character.add_item(item)
            return
        if getattr(character, "loot", None) is None:
            character.loot = []
        if item not in character.loot:
            character.loot.append(item)

    @staticmethod
    def equipped_slot_of(character, item):
        if hasattr(character, "equipped_slot_of"):
            return character.equipped_slot_of(item)
        equipped = getattr(character, "equipped", None)
        if equipped is None:
            return None
        for slot, equipped_item in equipped.__dict__.items():
            if equipped_item is item:
                return slot
        return None

    @staticmethod
    def equip_item(character, item, slot_name: str):
        if hasattr(character, "equip_item"):
            return character.equip_item(item, slot_name)
        return Equipped.equip_item(character, item, slot_name)

    @staticmethod
    def unequip_item(character, slot_name: str):
        if hasattr(character, "unequip_item"):
            return character.unequip_item(slot_name)
        return Equipped.unequip_item(character, slot_name)

    @staticmethod
    def find_wear_slot(character, item, wear_flags_enum, forced: str = ""):
        equipped = ItemUtil.ensure_equipped(character)
        if forced:
            slot = forced.strip().lower()
            return slot if hasattr(equipped, slot) and getattr(equipped, slot) is None else None

        flags = GameApi.flags_to_int(getattr(item, "wear_flags", 0))
        for flag_name, slots in ItemUtil.WEAR_SLOT_ORDER.items():
            if wear_flags_enum is None or not hasattr(wear_flags_enum, flag_name):
                continue
            bit = getattr(wear_flags_enum, flag_name).value
            if (flags & bit) == 0:
                continue
            for slot in slots:
                if getattr(equipped, slot) is None:
                    return slot
        return None

    @staticmethod
    def item_takeable(item, wear_flags_enum) -> bool:
        if wear_flags_enum is None or not hasattr(wear_flags_enum, "ITEM_TAKE"):
            return True
        return ItemUtil.has_flag(getattr(item, "wear_flags", 0), wear_flags_enum.ITEM_TAKE.value)

    @staticmethod
    def is_nodrop(item, item_flags_enum) -> bool:
        if item_flags_enum is None or not hasattr(item_flags_enum, "ITEM_NODROP"):
            return False
        return ItemUtil.has_flag(getattr(item, "extra_flags", 0), item_flags_enum.ITEM_NODROP.value)

    @staticmethod
    def is_nosac(item, item_flags_enum) -> bool:
        if item_flags_enum is None or not hasattr(item_flags_enum, "ITEM_NO_SAC"):
            return False
        return ItemUtil.has_flag(getattr(item, "extra_flags", 0), item_flags_enum.ITEM_NO_SAC.value)

    @staticmethod
    def item_type_name(item) -> str:
        return str(getattr(item, "item_type", "") or "").strip().upper()

    @staticmethod
    def is_pc_corpse(item) -> bool:
        return ItemUtil.item_type_name(item) == "ITEM_CORPSE_PC"

    @staticmethod
    def is_npc_corpse(item) -> bool:
        return ItemUtil.item_type_name(item) == "ITEM_CORPSE_NPC"

    @staticmethod
    def is_corpse(item) -> bool:
        item_type = ItemUtil.item_type_name(item)
        return item_type in {"ITEM_CORPSE_NPC", "ITEM_CORPSE_PC"}

    @staticmethod
    def sacrifice_silver_value(item) -> int:
        silver = max(1, GenericUtil.to_int(getattr(item, "level", 1), 0) * 3)
        if not ItemUtil.is_corpse(item):
            silver = min(silver, max(0, GenericUtil.to_int(getattr(item, "cost", 0), 0)))
        return max(3, silver)

    @staticmethod
    def sacrifice_reward_message(silver: int) -> str:
        if GenericUtil.to_int(silver, 0) == 1:
            return "Mota gives you one silver coin for your sacrifice.\r\n"
        return f"Mota gives you {GenericUtil.to_int(silver, 0)} silver coins for your sacrifice.\r\n"

    @staticmethod
    def is_container(item) -> bool:
        item_type = (getattr(item, "item_type", "") or "").upper()
        return "ITEM_CONTAINER" in item_type or "CONTAINER" in item_type

    @staticmethod
    def short(item) -> str | object | Any:
        short_fn = getattr(item, "short", None)
        if callable(short_fn):
            return short_fn()
        return getattr(item, "short_description", None) or getattr(item, "name", "it")

    @staticmethod
    def add_to_contains(container, obj):
        if hasattr(container, "add_contained_item"):
            container.add_contained_item(obj)
            return
        if getattr(container, "contains", None) is None:
            container.contains = []
        container.contains.append(obj)

    @staticmethod
    def remove_from_contains(container, obj):
        if hasattr(container, "remove_contained_item"):
            container.remove_contained_item(obj)
            return
        try:
            container.contains.remove(obj)
        except Exception:
            pass

    @staticmethod
    def find_in_contains(container, wanted: str):
        if hasattr(container, "find_contained_item"):
            return container.find_contained_item(wanted)
        q = (wanted or "").strip().lower()
        for obj in list(getattr(container, "contains", []) or []):
            name = (getattr(obj, "name", "") or "").lower()
            if name == q or name.startswith(q):
                return obj
        return None

    @staticmethod
    def first_fountain(room):
        if room is None:
            return None
        for item in room.contents.values():
            if "FOUNTAIN" in ((getattr(item, "item_type", "") or "").upper()):
                return item
        return None
