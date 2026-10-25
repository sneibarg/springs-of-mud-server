class GroupOwnership:
    """Explicit group ownership, independent of member proficiency."""

    @staticmethod
    def names(character) -> list[str]:
        return list(getattr(character, "groups", []) or [])

    @staticmethod
    def knows(character, name: str) -> bool:
        wanted = str(name or "").strip().casefold()
        return any(str(known).strip().casefold() == wanted for known in GroupOwnership.names(character))

    @staticmethod
    def add(character, name: str) -> None:
        name = str(name or "").strip()
        if name and not GroupOwnership.knows(character, name):
            character.groups = GroupOwnership.names(character) + [name]
