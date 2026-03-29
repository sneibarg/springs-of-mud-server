import requests

from injector import inject
from game import GameData
from object.AffectData import AffectData, AffectWhere
from object.ExtraDescriptionData import ExtraDescriptionData
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig
from skill.SkillService import SkillService


class ItemService:
    @inject
    def __init__(self, config: ServiceConfig, skill_service: SkillService, game_data: GameData):
        self.__name__ = "ItemService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.items_endpoint = config.items_endpoint
        self.game_data = game_data
        self.enums = self.game_data.enums
        self.skill_service = skill_service
        self.all_items = {}
        self.load_items()
        self.logger.info("Initialized ItemService instance with a total of " + str(len(self.all_items)) + " in memory.")

    def return_item_by_id(self, item_id):
        return self.all_items[item_id]

    def get_item_by_id(self, item_id):
        try:
            return requests.get(self.items_endpoint + "/" + item_id).json()
        except Exception as e:
            self.logger.error("Failed to get item data: " + str(e))
        return None

    def load_items(self):
        try:
            all_items = requests.get(self.items_endpoint).json()
            for item_data in all_items:
                item_id = item_data['id']
                self.all_items[item_id] = self._normalize_item_data(item_data)
        except Exception as e:
            self.logger.error("Failed to get items: " + str(e))
        return None

    def _normalize_item_data(self, item_data):
        self._update_item_type(item_data)
        self._update_condition(item_data)

        item = Item.from_json(item_data)
        if len(item.affect_data) > 0:
            item.effects = []
            self._update_affect_data(item)

        self._update_extra_descr(item)
        return item

    def _update_item_type(self, item_data):
        item_types = self.enums['itemType']
        item_type = item_data.get("itemType")
        if not isinstance(item_type, int):
            raw_value = str(item_type or "").strip()
            enum_lookup = self.enums.get("itemType", {})
            if raw_value.isdigit():
                item_type = int(raw_value)
            else:
                item_type = enum_lookup.get(raw_value.upper(), item_type)
        if item_type == item_types.ITEM_WEAPON:
            self._attack_type(item_data)
        elif item_type == item_types.ITEM_FOUNTAIN:
            self._update_fountain(item_data)
        elif item_type == item_types.ITEM_STAFF:
            self._update_staff(item_data)
        elif item_type == item_types.ITEM_SCROLL:
            self._update_scroll(item_data)

    def _update_fountain(self, item_data):
        self._liq_lookup(item_data)

    def _update_staff(self, item_data):
        try:
            skill_name = item_data['value3']
            skill = self.skill_service.get_skill_by_name(skill_name)
            item_data['value3'] = str(skill)
        except Exception as e:
            print(f"Failed to update staff skill: {e}")

    def _update_scroll(self, item_data):
        for skill_key in ['value1', 'value2', 'value3', 'value4']:
            try:
                skill_name = item_data[skill_key]
                if skill_name != "":
                    skill = self.skill_service.get_skill_by_name(skill_name)
                    item_data[skill_key] = str(skill)
            except Exception as e:
                print(f"Failed to update scroll skill: {e}")

    # even if it's slower, it still loads all in the same second
    def _attack_type(self, item_data):
        damages_types = self.enums['damageType']
        damage_type = item_data['value3']
        if damage_type in ['blast', 'pound', 'crush', 'suction', 'beating', 'charge', 'slap', 'punch', 'peckb', 'smash',
                           'thwack']:
            item_data['damage_type'] = damages_types.DAM_BASH
        elif damage_type in ['slash', 'whip', 'claw', 'grep', 'cleave', 'chop', 'slice']:
            item_data['damage_type'] = damages_types.DAM_SLASH
        elif damage_type in ['pierce', 'stab', 'bite', 'scratch', 'sting', 'chomp', 'thrust']:
            item_data['damage_type'] = damages_types.DAM_PIERCE
        elif damage_type in ['digestion', 'acbite', 'slime']:
            item_data['damage_type'] = damages_types.DAM_ACID
        elif damage_type in ['flame', 'flbite']:
            item_data['damage_type'] = damages_types.DAM_FIRE
        elif damage_type in ['frbite', 'chill']:
            item_data['damage_type'] = damages_types.DAM_COLD
        elif damage_type in ['shbite', 'shock']:
            item_data['damage_type'] = damages_types.DAM_LIGHTNING
        elif damage_type in ['wrath', 'magic']:
            item_data['damage_type'] = damages_types.DAM_ENERGY
        elif damage_type in ['divine']:
            item_data['damage_type'] = damages_types.DAM_HOLY
        elif damage_type in ['drain']:
            item_data['damage_type'] = damages_types.DAM_NEGATIVE
        else:
            self.logger.warn(f"Unknown damage type: {damage_type} for item {item_data}")
            item_data['damage_type'] = damages_types.DAM_NONE

    def _liq_lookup(self, item_data):
        liq_table = self.game_data.get('liquids')
        liquid_name = item_data['value2'].replace("'", "")
        liquid = liq_table[liquid_name]
        liquid_affect_data = liquid['affect']
        liquid_color = liquid['color']
        item_data['liquid_affect_data'] = liquid_affect_data
        item_data['liquid_color'] = liquid_color

    @staticmethod
    def _update_condition(item_data):
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
    def _update_affect_data(item):
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
                affect_data.bitvector = affect_elements[4]

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
    def _update_extra_descr(item):
        if len(item.extra_descr) > 0:
            item.extra_description = ExtraDescriptionData(valid=True, keyword=item.extra_descr[0], description=item.extra_descr[1])
