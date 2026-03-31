import threading

from skill.Skill import Skill


class SkillRegistry:
    def __init__(self):
        self.registry = {}
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