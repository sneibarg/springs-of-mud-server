import requests

from injector import inject
from server.ServiceConfig import ServiceConfig
from server.LoggerFactory import LoggerFactory
from skill import Skill


class SkillService:
    @inject
    def __init__(self, config: ServiceConfig):
        self.skills_endpoint = config.skills_endpoint
        self.logger = LoggerFactory.get_logger(self.__class__.__name__)
        self.all_skills = dict()
        self._load_skills()
        self.logger.info("Initialized SkillService instance with a total of "+str(len(self.all_skills))+" in memory.")

    def get_skill_by_id(self, skill_id) -> Skill:
        return self.all_skills.get(skill_id)

    def get_skill_by_name(self, skill_name) -> Skill | None:
        for skill in self.all_skills.values():
            if skill['name'] == skill_name:
                return skill
        return None

    def _load_skills(self) -> None:
        try:
            url = self.skills_endpoint
            response = requests.get(url)
            skills = response.json()
            for skill in skills:
                self.all_skills[skill['id']] = skill
        except Exception as e:
            self.logger.error("Failed to load skills: " + str(e))
