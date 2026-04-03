import requests

from typing import Optional
from injector import inject
from game import GameData
from skill import Skill
from skill.GroupRegistry import GroupRegistry
from skill.GroupType import GroupType
from skill.SkillRegistry import SkillRegistry
from server.ServiceConfig import ServiceConfig
from server.LoggerFactory import LoggerFactory


class SkillService:
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

    def reload_skills(self) -> None:
        self.logger.info("Reloading all skills...")
        self.skill_registry.reset()
        self.load_skills()
        self.logger.info("Skills reload completed.")

    def reload_groups(self) -> None:
        self.logger.info("Reloading all groups...")
        self.group_registry.reset()
        self.load_groups()
        self.logger.info("Groups reload completed.")

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
        return self._fetch_and_register(url, f"item '{skill_name}'")

    def _fetch_and_register(self, url: str, description: str) -> Optional[Skill]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                count = 0
                for skill_data in data:
                    self.skill_registry.register(Skill.from_json(skill_data))
                    count += 1
                self.logger.info(f"Loaded {count} {description}.")
                return None
            else:
                skill = Skill.from_json(data)
                self.skill_registry.register(skill)
                self.logger.info(f"Loaded {description}.")
                return skill

        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {description} from {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error processing {description}: {e}", exc_info=True)
            return None
