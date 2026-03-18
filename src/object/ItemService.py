import requests

from injector import inject
from game import GameService
from object.Item import Item
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig
from skill.SkillService import SkillService


class ItemService:
    @inject
    def __init__(self, config: ServiceConfig, game_service: GameService, skill_service: SkillService):
        self.__name__ = "ItemService"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.items_endpoint = config.items_endpoint
        self.game_service = game_service
        self.skill_service = skill_service
        self.all_items = {}
        self.load_items()
        self.logger.info("Initialized ItemService instance with a total of "+str(len(self.all_items))+" in memory.")

    def return_item_by_id(self, item_id):
        return self.all_items[item_id]

    def get_item_by_id(self, item_id):
        url = self.items_endpoint + "/" + item_id
        try:
            return requests.get(url).json()
        except Exception as e:
            self.logger.error("Failed to get item data: "+str(e))
        return None

    def load_items(self):
        try:
            all_items = requests.get(self.items_endpoint).json()
            i = 0
            for item_data in all_items:
                i = i + 1
                item_id = item_data['id']
                item = self._normalize_item_data(item_data)
                self.all_items[item_id] = item
        except Exception as e:
            self.logger.error("Failed to get items: "+str(e))
        return None

    def _normalize_item_data(self, item_data) -> Item:
        self._update_item_type(item_data)
        self._update_condition(item_data)
        return Item.from_json(item_data)

    def _update_item_type(self, item_data):
        item_types = self.game_service.enums['itemType']
        item_type = item_data.get("itemType")
        if item_type == item_types.ITEM_WEAPON:
            self._attack_type(item_data)
        elif item_type == item_types.ITEM_CONTAINER:
            self._update_container(item_data)
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
        damages_types = self.game_service.enums['damageType']
        damage_type = item_data['value3']
        if damage_type in ['blast', 'pound', 'crush', 'suction', 'beating', 'charge', 'slap', 'punch', 'peckb', 'smash', 'thwack']:
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
        liq_table = self.game_service.game_data.liquids
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

    def _update_affect_data(self):
        pass

    def _update_extra_descr(self):
        pass
