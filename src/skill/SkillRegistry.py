from registries import Registry
from server.LoggerFactory import LoggerFactory
from skill.Skill import Skill


class SkillRegistry(Registry[Skill]):
    def __init__(self):
        super().__init__()

        self.__name__ = "SkillRegistry"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def all_skills(self) -> set[Skill]:
        return self._items
