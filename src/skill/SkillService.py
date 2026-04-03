import requests

from injector import inject
from game import GameData
from skill.SkillRegistry import SkillRegistry
from server.ServiceConfig import ServiceConfig
from server.LoggerFactory import LoggerFactory
from skill.GroupType import GroupType
from skill.Skill import Skill


class SkillService:
    @inject
    def __init__(self, config: ServiceConfig, skill_registry: SkillRegistry, game_data: GameData):
        self.__name__ = "SkillService"
        self.skills_endpoint = config.skills_endpoint
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.skill_registry = skill_registry
        self.groups = game_data.groups
        self.load_skills()
        self.load_groups()
        self.logger.info(f"Initialized SkillService instance with a total of {str(len(self.skill_registry.registry))} skills and {str(len(self.skill_registry.group_registry))} groups in memory.")

    def load_skills(self) -> None:
        try:
            url = self.skills_endpoint
            response = requests.get(url)
            skills = response.json()
            for skill in skills:
                self.skill_registry.register_skill(Skill.from_json(skill))
        except Exception as e:
            self.logger.error("Failed to load skills: " + str(e))

    def load_groups(self):
        for group_data in self.groups:
            group_json = self.groups.get(group_data)
            group_json['name'] = group_data
            group = GroupType.from_json(group_json)
            self.skill_registry.register_group(group)
