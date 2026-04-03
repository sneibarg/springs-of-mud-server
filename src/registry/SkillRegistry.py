import threading

from skill.GroupTable import GroupTable
from skill.Skill import Skill


class SkillRegistry:
    def __init__(self):
        self.registry = {}
        self.group_registry = {}
        self.lock = threading.Lock()

    def get_skill_by_id(self, skill_id) -> Skill | None:
        try:
            return self.registry[skill_id]
        except KeyError:
            return None

    def get_skill_by_name(self, skill_name) -> Skill | None:
        for skill in self.registry.values():
            if skill.name == skill_name:
                return skill
        return None

    def register_skill(self, skill: Skill):
        with self.lock:
            self.registry[skill.id] = skill

    def unregister_skill(self, skill: Skill):
        with self.lock:
            del self.registry[skill.id]

    def register_group(self, group_table: GroupTable):
        with self.lock:
            self.group_registry[group_table.name] = group_table

    def unregister_group(self, group_name: str):
        with self.lock:
            del self.group_registry[group_name]

    def get_group_by_name(self, group_name: str) -> GroupTable | None:
        try:
            return self.group_registry[group_name]
        except KeyError:
            return None
