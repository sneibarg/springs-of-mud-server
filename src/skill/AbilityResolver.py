class AbilityResolver:
    """Resolve definitions without caching mutable registry contents.

    Practice names and IDs prefer skills; effect owners prefer spells. The
    spell-only entry point preserves the dispel facade's historical namespace.
    """

    def __init__(self, skill_registry=None, spell_registry=None):
        self.skill_registry = skill_registry
        self.spell_registry = spell_registry

    @staticmethod
    def _entries(registry, method):
        fetch = getattr(registry, method, None)
        if not callable(fetch):
            return []
        try:
            return list(fetch() or [])
        except TypeError:
            return []

    def by_name(self, name):
        wanted = str(name or "").strip().lower()
        if not wanted:
            return None
        for registry, method in ((self.skill_registry, "all_skills"), (self.spell_registry, "all_spells")):
            for ability in self._entries(registry, method):
                if str(ability.name or "").strip().lower() == wanted:
                    return ability
        return None

    def by_id(self, ability_id):
        for registry, collection in ((self.skill_registry, "skills"), (self.spell_registry, "spells")):
            ability = registry.get_or_none(id=ability_id) if registry is not None else None
            if ability is not None:
                return ability, collection
        return None, "skills"

    def effect_owner(self, effect_type, *, spell_only=False):
        wanted = str(effect_type or "").strip().lower()
        if not wanted:
            return None
        # Periodic effects historically accept prefixed names as aliases.
        candidates = {wanted} if spell_only else {
            wanted, wanted.replace("spell.", ""), wanted.replace("skill.", "")}
        sources = [(self.spell_registry, "all_spells")]
        if not spell_only:
            sources.append((self.skill_registry, "all_skills"))
        for registry, method in sources:
            for ability in self._entries(registry, method):
                names = {str(getattr(ability, key, "") or "").strip().lower()
                         for key in ("handler_id", "name", "id")}
                if candidates & names:
                    return ability
        return None
