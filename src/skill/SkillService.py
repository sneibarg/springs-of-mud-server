from injector import inject
from game import GameData
from skill.Skill import Skill
from skill.GroupRegistry import GroupRegistry
from skill.GroupType import GroupType
from skill.SkillRegistry import SkillRegistry
from server.FetchAndRegisterMixin import FetchAndRegisterMixin
from server.ServiceConfig import ServiceConfig
from server.LoggerFactory import LoggerFactory


class SkillService(FetchAndRegisterMixin):
    @inject
    def __init__(self, config: ServiceConfig, skill_registry: SkillRegistry, group_registry: GroupRegistry, game_data: GameData):
        self.__name__ = "SkillService"
        self.skills_endpoint = config.skills_endpoint
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.skill_registry = skill_registry
        self.group_registry = group_registry
        self.groups = game_data.groups
        self.load_skills()
        self.load_groups()

    def reload_skills(self) -> bool:
        return self._reload_collection(self.skills_endpoint, "skills", self.skill_registry)

    def reload_groups(self) -> bool:
        try:
            candidate = type(self.group_registry)()
            for name, data in self.groups.items():
                candidate.register(GroupType.from_json(dict(data, name=name)))
            candidate.populate()
            self._publish_registry(self.group_registry, candidate)
            self.logger.info("Groups reload completed.")
            return True
        except Exception as error:
            self.logger.error(f"Failed to reload groups; previous registry retained: {error}", exc_info=True)
            return False

    def load_groups(self):
        for group_data in self.groups:
            group = self.groups[group_data]
            group['name'] = group_data
            self.group_registry.register(GroupType.from_json(group))
        self.logger.info(f"Loaded {len(self.groups)} groups.")

    def load_group(self, group_name: str):
        for group_data in self.groups:
            if self.groups[group_data] == group_name:
                group = self.groups[group_data]
                group['name'] = group_data
                self.group_registry.register(GroupType.from_json(group))
                self.logger.info(f"Loaded group '{group_name}'.")
                return group
        return None

    def reset_groups(self):
        self.group_registry.reset()

    def load_skills(self):
        self._fetch_and_register(self.skills_endpoint, "all skills")

    def load_skill(self, skill_name: str):
        url = f"{self.skills_endpoint}/name/{skill_name}"
        return self._fetch_and_register(url, f"skill '{skill_name}'")

    def _build_fetch_item(self, skill_data) -> Skill:
        return Skill.from_json(skill_data)

    def _register_fetch_item(self, skill: Skill) -> None:
        self.skill_registry.register(skill)
