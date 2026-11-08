from itertools import chain


class AbilityResolver:
    """Resolve definitions without caching mutable registry contents.

    Practice names and IDs prefer skills; effect owners prefer spells. The
    spell-only entry point preserves the dispel facade's historical namespace.
    """

    def __init__(self, skill_registry=None, spell_registry=None):
        self.skill_registry = skill_registry
        self.spell_registry = spell_registry

    def _skills(self):
        if self.skill_registry is not None:
            yield from list(self.skill_registry.all_skills())

    def _spells(self):
        if self.spell_registry is not None:
            yield from list(self.spell_registry.all_spells())

    def by_name(self, name):
        wanted = str(name or "").strip().lower()
        if not wanted:
            return None
        for ability in chain(self._skills(), self._spells()):
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
        definitions = self._spells() if spell_only else chain(self._spells(), self._skills())
        for ability in definitions:
            names = {str(value or "").strip().lower()
                     for value in (ability.handler_id, ability.name, ability.id)}
            if candidates & names:
                return ability
        return None
