import requests

from injector import inject
from registry.SkillRegistry import SkillRegistry
from server.ServiceConfig import ServiceConfig
from server.LoggerFactory import LoggerFactory
from skill.Skill import Skill


class SkillService:
    @inject
    def __init__(self, config: ServiceConfig, skill_registry: SkillRegistry):
        self.__name__ = "SkillService"
        self.skills_endpoint = config.skills_endpoint
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.skill_registry = skill_registry
        self._load_skills()
        self.logger.info("Initialized SkillService instance with a total of "+str(len(self.skill_registry.registry))+" in memory.")

    def _load_skills(self) -> None:
        try:
            url = self.skills_endpoint
            response = requests.get(url)
            skills = response.json()
            for skill in skills:
                self.skill_registry.register_skill(Skill.from_json(skill))
        except Exception as e:
            self.logger.error("Failed to load skills: " + str(e))
